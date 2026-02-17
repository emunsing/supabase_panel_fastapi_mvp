# FastAPI MVP with Google OAuth via Supabase

This is a minimal viable product (MVP) implementation of a FastAPI web application that authenticates users via Google OAuth through Supabase.

## Features

- **Unauthenticated Access**: Users without authentication are shown a login page
- **Google OAuth**: Users can log in using their Google account via Supabase
- **Welcome Page**: After successful authentication, users see a welcome page with their email address
- **Clean UI**: Simple, responsive HTML interfaces for login and welcome pages

## Setup

### Prerequisites

- Python 3.12+
- A Supabase project with Google OAuth configured
- Supabase URL and API key

### Installation

1. Install dependencies:
```bash
pip install fastapi uvicorn supabase python-dotenv
```

2. Create a `.env` file in the project root with your Supabase credentials:
```env
SUPABASE_APP_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-anon-key-here
```

You can use `.env.example` as a template.

### Supabase Configuration

To use Google OAuth with Supabase:

1. Go to your Supabase project dashboard
2. Navigate to Authentication → Providers
3. Enable the Google provider
4. Configure the OAuth callback URL in your Google Cloud Console
5. Add your Google OAuth client ID and secret to Supabase

## Usage

### Running the Server

Run the application directly:

```bash
python supa_mvp/01_mvp_claude.py
```

Or use uvicorn:

```bash
uvicorn supa_mvp.01_mvp_claude:app --reload
```

The server will start on `http://localhost:8000`

### Endpoints

- `GET /` - Root endpoint
  - Without authentication: Shows login page
  - With authentication: Shows welcome page with user email
  
- `GET /login` - Initiates Google OAuth flow via Supabase
  - Redirects to Google login
  - After successful login, redirects back with access token
  
- `GET /health` - Health check endpoint
  - Returns `{"status": "healthy", "service": "supabase-oauth-mvp"}`

## How It Works

1. **Initial Visit**: When a user visits `/`, they see a login page with a "Login with Google" button
2. **OAuth Initiation**: Clicking the button redirects to `/login`, which calls `supabase.auth.sign_in_with_oauth()` with the Google provider
3. **Google Authentication**: Supabase redirects the user to Google's OAuth page
4. **Callback**: After successful authentication, Google redirects back to your app with an access token in the URL
5. **Welcome Page**: The root endpoint (`/`) detects the access token, fetches user info from Supabase, and displays the welcome page with the user's email

## Security Notes

- This is an MVP implementation for demonstration purposes
- In production, you should:
  - Use proper session management
  - Store tokens securely (e.g., in httpOnly cookies)
  - Implement CSRF protection
  - Add proper error handling and logging
  - Configure CORS appropriately
  - Use HTTPS for all connections

## Code Structure

```python
# Main components:
- FastAPI app initialization
- Environment variable loading (.env)
- Supabase client creation
- Root endpoint (/) - serves login or welcome page
- Login endpoint (/login) - initiates OAuth
- Health check endpoint (/health)
```

## Troubleshooting

**Error: "SUPABASE_APP_URL and SUPABASE_API_KEY must be set in .env file"**
- Make sure you have created a `.env` file with valid Supabase credentials

**OAuth redirect fails**
- Ensure your redirect URL is configured in Supabase and Google Cloud Console
- Check that the URL matches your application's base URL

**User email not showing**
- Verify that Google OAuth is properly configured in Supabase
- Ensure the user has granted email permission during OAuth flow
