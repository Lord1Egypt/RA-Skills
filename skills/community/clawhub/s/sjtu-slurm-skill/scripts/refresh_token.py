#!/usr/bin/env python3
"""
Refresh bearer token from SJTU HPC API.

This script refreshes an existing bearer token using the PATCH /token endpoint.
A refreshed token can be used to extend the session without re-authenticating
with username and password.

Usage:
    python refresh_token.py [--workspace WORKSPACE]

Options:
    --workspace WORKSPACE  Absolute path to the agent's workspace (default: ~/.openclaw/workspace). Credentials will be read from WORKSPACE/credentials.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE_URL = "https://api.hpc.sjtu.edu.cn"
TOKEN_FILENAME = "hpc_token"


class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, http_code: int):
        super().__init__(message)
        self.http_code = http_code


def parse_error_response(e: urllib.error.HTTPError) -> tuple[str, bool]:
    """
    Parse error response from API.
    Returns (error_message, is_internal_error).
    - HTTP 500: internal error, body contains session ID and help info
    - Other codes: rejection, body contains reason
    """
    body = e.read().decode("utf-8")
    http_code = e.code
    return body, http_code == 500


def refresh_token(current_token: str) -> str:
    """
    Refresh bearer token using PATCH /token endpoint.
    
    The PATCH request sends the current token in the Authorization header
    and receives a new token in response.
    """
    url = f"{API_BASE_URL}/token"
    
    # PATCH request with current token to refresh it
    req = urllib.request.Request(
        url,
        data=json.dumps({}).encode("utf-8"),  # Empty body for refresh
        headers={
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {current_token}"
        },
        method="PATCH"
    )

    try:
        with urllib.request.urlopen(req) as response:
            new_token = response.read().decode("utf-8")
            # Token format is "Bearer ..."
            if new_token.startswith("Bearer "):
                new_token = new_token[7:]
            return new_token
    except urllib.error.HTTPError as e:
        error_body, is_internal = parse_error_response(e)
        if is_internal:
            raise APIError(
                f"刷新Token失败: {error_body}",
                e.code
            )
        else:
            raise APIError(
                f"刷新Token被拒绝: {error_body}",
                e.code
            )


def save_token(token_dir: str, token: str) -> str:
    """Save token to a file in the specified directory."""
    os.makedirs(token_dir, exist_ok=True)
    token_path = os.path.join(token_dir, TOKEN_FILENAME)
    with open(token_path, "w") as f:
        f.write(token)
    os.chmod(token_path, 0o600)
    return token_path


def load_token(token_dir: str) -> str | None:
    """Load token from the token directory."""
    token_path = os.path.join(token_dir, TOKEN_FILENAME)
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            return f.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Refresh bearer token from SJTU HPC API"
    )
    # Default workspace path
    default_workspace = os.path.expanduser("~/.openclaw/workspace")

    parser.add_argument(
        "--workspace",
        default=default_workspace,
        help=f"Absolute path to the agent's workspace (default: {default_workspace}). Credentials will be read from WORKSPACE/credentials."
    )

    args = parser.parse_args()

    # Credentials are always stored in WORKSPACE/credentials
    credentials_dir = os.path.join(args.workspace, "credentials")

    # Load existing token
    current_token = load_token(credentials_dir)
    if not current_token:
        print(
            f"Error: No token found in {credentials_dir}. "
            "Please run req_token.py first to obtain a token.",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        # Refresh token
        new_token = refresh_token(current_token)

        # Save new token
        token_path = save_token(credentials_dir, new_token)

        print(f"Token refreshed successfully and saved to {token_path}")
        print("Note: The old token is now invalid.")

    except APIError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()