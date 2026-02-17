# Supabase Panel OAuth MVP

A simple MVP of a Python Panel web app that demonstrates Google OAuth authentication via Supabase. Once logged in, the app displays a welcome page with the user's email address.

## Features

- Google OAuth login via Supabase
- Simple and clean user interface using Panel
- Session management
- Secure authentication flow
- Display user email after successful login

## Prerequisites

- Python 3.8 or higher
- A Supabase account and project
- Google OAuth configured in Supabase

## Setup

### 1. Supabase Configuration

1. Create a Supabase project at https://supabase.com
2. Go to Authentication → Providers in your Supabase dashboard
3. Enable Google provider:
   - Toggle "Enable Google" to ON
   - Add your Google OAuth credentials (Client ID and Client Secret)
   - Configure authorized redirect URIs (e.g., `http://localhost:5006`)
4. Note your Project URL and anon/public API key from Settings → API

### 2. Environment Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

## Running the Application

Start the Panel server:

```bash
panel serve app.py --show
```

The application will be available at `http://localhost:5006`

## Usage

1. Open the application in your browser
2. Click "Login with Google"
3. Complete the Google OAuth flow
4. You will be redirected back to the app with your email displayed
5. Click "Logout" to sign out

## Project Structure

```
.
├── app.py              # Main Panel application with OAuth logic
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .env               # Your actual environment variables (not in git)
└── README.md          # This file
```

## How It Works

1. **Login Flow**: When a user clicks "Login with Google", the app initiates OAuth through Supabase's `sign_in_with_oauth` method
2. **Redirect**: User is redirected to Google's OAuth consent screen
3. **Callback**: After authentication, Google redirects back to the app with an access token
4. **User Info**: The app retrieves user information from Supabase using the access token
5. **Display**: The welcome page shows the authenticated user's email address

## Troubleshooting

- **Missing environment variables**: Ensure your `.env` file is properly configured with valid Supabase credentials
- **OAuth redirect issues**: Make sure your redirect URL in Supabase matches your application URL
- **Login not working**: Verify that Google OAuth is properly configured in your Supabase dashboard

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Use environment variables for all sensitive configuration

## License

MIT
