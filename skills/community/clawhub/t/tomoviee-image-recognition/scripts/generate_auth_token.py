#!/usr/bin/env python3
"""
Generate authentication token for Tomoviee API.

Usage:
    python generate_auth_token.py <app_key> <app_secret>

Output:
    Base64 encoded access_token in the format required by Authorization header
"""

import base64
import sys


def generate_access_token(app_key: str, app_secret: str) -> str:
    """
    Generate access token for Tomoviee API authentication.
    
    Args:
        app_key: Application key from Tomoviee console
        app_secret: Application secret from Tomoviee console
    
    Returns:
        Base64 encoded string in format: base64(app_key:app_secret)
    """
    credentials = f"{app_key}:{app_secret}"
    access_token = base64.b64encode(credentials.encode()).decode()
    return access_token


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_auth_token.py <app_key> <app_secret>")
        sys.exit(1)
    
    app_key = sys.argv[1]
    app_secret = sys.argv[2]
    
    token = generate_access_token(app_key, app_secret)
    print(f"Access Token: {token}")
    print(f"\nUse in Authorization header as: Basic {token}")
