"""
Simple MVP of a Panel web app with Google OAuth via Supabase.

This app demonstrates:
1. User authentication via Google OAuth handled by Supabase
2. Display of a welcome page with the user's email after successful login
"""

import os
import panel as pn
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Panel
pn.extension()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables. Please check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


class AuthApp:
    """Main authentication application."""
    
    def __init__(self):
        self.user_email = pn.state.session_args.get('email', [b''])[0].decode('utf-8') if pn.state.session_args.get('email') else None
        self.access_token = pn.state.session_args.get('access_token', [b''])[0].decode('utf-8') if pn.state.session_args.get('access_token') else None
        
    def create_login_page(self):
        """Create the login page with Google OAuth button."""
        return pn.Column(
            pn.pane.Markdown("# Welcome to the App"),
            pn.pane.Markdown("Please log in to continue."),
            pn.pane.Markdown("---"),
            pn.pane.Markdown(
                "## How to log in:\n\n"
                "1. Click the button below to initiate Google OAuth login\n"
                "2. You will be redirected to Supabase authentication\n"
                "3. After successful login, you will be redirected back to this app"
            ),
            pn.widgets.Button(
                name="Login with Google",
                button_type="primary",
                width=200
            ).param.watch(self.initiate_oauth, 'clicks'),
            sizing_mode='stretch_width',
            styles={'padding': '20px'}
        )
    
    def initiate_oauth(self, *events):
        """Initiate OAuth flow with Supabase."""
        # Get the OAuth URL from Supabase for Google provider
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{pn.state.location.origin}{pn.state.location.pathname}"
            }
        })
        
        # Redirect to the OAuth URL
        if response.url:
            pn.state.location.href = response.url
    
    def create_welcome_page(self, email: str):
        """Create the welcome page after successful login."""
        return pn.Column(
            pn.pane.Markdown("# Welcome!"),
            pn.pane.Markdown(f"You are logged in as: **{email}**"),
            pn.pane.Markdown("---"),
            pn.pane.Markdown("## OAuth Login Successful"),
            pn.pane.Markdown(
                f"Your Google account email ({email}) has been successfully "
                "authenticated via Supabase."
            ),
            pn.widgets.Button(
                name="Logout",
                button_type="warning",
                width=200
            ).param.watch(self.logout, 'clicks'),
            sizing_mode='stretch_width',
            styles={'padding': '20px'}
        )
    
    def logout(self, *events):
        """Handle logout."""
        supabase.auth.sign_out()
        pn.state.location.href = pn.state.location.pathname
    
    def create_app(self):
        """Create the main application layout."""
        # Check for OAuth callback parameters in URL
        url_params = pn.state.location.query_params
        
        # Try to get user from Supabase session
        user_email = None
        
        # Check if we have an access_token in the URL (OAuth callback)
        if 'access_token' in url_params:
            try:
                access_token = url_params['access_token']
                # Set the session with the access token
                response = supabase.auth.get_user(access_token)
                if response and response.user:
                    user_email = response.user.email
            except Exception as e:
                print(f"Error getting user from token: {e}")
        
        # If no email from callback, check existing session
        if not user_email:
            try:
                user = supabase.auth.get_user()
                if user and user.user:
                    user_email = user.user.email
            except:
                pass
        
        # Display appropriate page based on authentication status
        if user_email:
            return self.create_welcome_page(user_email)
        else:
            return self.create_login_page()


# Create the application
app = AuthApp()
template = pn.template.FastListTemplate(
    title="Panel OAuth MVP",
    main=[app.create_app()],
    theme="default"
)

# Serve the application
template.servable()
