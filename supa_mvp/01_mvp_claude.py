"""
FastAPI MVP with Google OAuth through Supabase

This app demonstrates:
- Unauthenticated users are redirected to Google OAuth login via Supabase
- After successful login, displays a welcome page with user's email
- Uses SUPABASE_APP_URL and SUPABASE_API_KEY from .env file
"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Supabase OAuth MVP")

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_APP_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_APP_URL and SUPABASE_API_KEY must be set in .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint - checks if user is authenticated.
    If not, shows login page. If yes, shows welcome page.
    """
    # Get access token from query parameters (after OAuth callback)
    access_token = request.query_params.get("access_token")
    
    if access_token:
        # User has access token, show welcome page
        try:
            # Get user info from Supabase
            user_response = supabase.auth.get_user(access_token)
            user = user_response.user
            
            if user and user.email:
                return HTMLResponse(content=f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Welcome</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                            background-color: #f5f5f5;
                        }}
                        .container {{
                            background-color: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }}
                        h1 {{
                            color: #333;
                            margin-bottom: 20px;
                        }}
                        .email {{
                            color: #0066cc;
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Welcome!</h1>
                        <p>You are successfully logged in.</p>
                        <p>Your email: <span class="email">{user.email}</span></p>
                    </div>
                </body>
                </html>
                """)
        except Exception as e:
            # Token is invalid or expired, show login page
            # Log the error for debugging (in production, use proper logging)
            print(f"Authentication error: {str(e)}")
    
    # No valid token, show login page
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            .login-button {
                display: inline-block;
                padding: 15px 30px;
                background-color: #4285f4;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
                transition: background-color 0.3s;
            }
            .login-button:hover {
                background-color: #357ae8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Supabase OAuth MVP</h1>
            <p>Please log in to continue</p>
            <a href="/login" class="login-button">Login with Google</a>
        </div>
    </body>
    </html>
    """)


@app.get("/login")
async def login(request: Request):
    """
    Initiates Google OAuth flow via Supabase.
    Redirects user to Google login page.
    """
    try:
        # Get the redirect URL (where to return after OAuth)
        # In production, this should be configurable
        redirect_to = str(request.base_url).rstrip("/")
        
        # Sign in with OAuth provider (Google)
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_to
            }
        })
        
        # Redirect to the OAuth URL
        if response and response.url:
            return RedirectResponse(url=response.url)
        else:
            raise HTTPException(status_code=500, detail="Failed to initiate OAuth flow")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth error: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "supabase-oauth-mvp"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
