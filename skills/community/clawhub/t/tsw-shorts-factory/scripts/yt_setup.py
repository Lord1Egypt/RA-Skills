#!/usr/bin/env python3
"""
One-time YouTube OAuth setup. Run this to authorize the factory to upload videos.
Saves token to ~/.yt_token.pickle for future use.
"""
import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN_FILE = os.path.expanduser('~/.yt_token.pickle')
CLIENT_SECRETS = 'yt_client_secrets.json'

def setup():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as f:
            creds = pickle.load(f)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS):
                print(f"""
ERROR: {CLIENT_SECRETS} not found.

To get this file:
1. Go to https://console.cloud.google.com/
2. Create a project (or select existing)
3. Enable YouTube Data API v3
4. Create OAuth 2.0 Client ID (Desktop app)
5. Download JSON and save as yt_client_secrets.json
""")
                return False
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)
        print(f"✅ YouTube auth saved to {TOKEN_FILE}")
    else:
        print("✅ YouTube token already valid")
    return True

if __name__ == '__main__':
    setup()
