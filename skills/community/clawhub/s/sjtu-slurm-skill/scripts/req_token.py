#!/usr/bin/env python3
"""
Request bearer token from SJTU HPC API.

This script authenticates with the HPC API and obtains a bearer token
which can be used for subsequent operations like key generation and
certificate signing.

Usage:
    python req_token.py <username> <password> [--workspace WORKSPACE] [--textfile TEXTFILE]

Arguments:
    username: HPC account username
    password: HPC account password

Options:
    --workspace WORKSPACE  Absolute path to the agent's workspace (default: ~/.openclaw/workspace). Credentials will be stored in WORKSPACE/credentials.
    --textfile TEXTFILE    Path to a file containing the password. If provided, the file will be deleted after the token is successfully saved to prevent password leak.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE_URL = "https://api.hpc.sjtu.edu.cn"
TOKEN_FILENAME = "hpc_token"


def delete_file_if_exists(file_path: str) -> None:
    """Delete the specified file if it exists."""
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted password file: {file_path}")
        except Exception as e:
            print(f"Warning: Failed to delete password file {file_path}: {e}", file=sys.stderr)


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


def request_token(operator: str, password: str) -> str:
    """Request bearer token from HPC API."""
    url = f"{API_BASE_URL}/token"
    payload = {
        "domain": "pi",
        "operator": operator,
        "password": password
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/plain"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            token = response.read().decode("utf-8")
            # Token format is "Bearer ..."
            if token.startswith("Bearer "):
                token = token[7:]
            return token
    except urllib.error.HTTPError as e:
        error_body, is_internal = parse_error_response(e)
        if is_internal:
            raise APIError(
                f"获取Token失败: {error_body}",
                e.code
            )
        else:
            raise APIError(
                f"获取Token被拒绝: {error_body}",
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


def main():
    parser = argparse.ArgumentParser(
        description="Request bearer token from SJTU HPC API"
    )
    parser.add_argument("username", help="HPC account username")
    parser.add_argument("password", help="HPC account password")
    # Default workspace path
    default_workspace = os.path.expanduser("~/.openclaw/workspace")

    parser.add_argument(
        "--workspace",
        default=default_workspace,
        help=f"Absolute path to the agent's workspace (default: {default_workspace}). Credentials will be stored in WORKSPACE/credentials."
    )

    parser.add_argument(
        "--textfile",
        default=None,
        help="Path to a file containing the password. If provided, the file will be deleted after the token is successfully saved to prevent password leak."
    )

    args = parser.parse_args()

    # Credentials are always stored in WORKSPACE/credentials
    credentials_dir = os.path.join(args.workspace, "credentials")

    try:
        # Request token
        token = request_token(args.username, args.password)

        # Save token
        token_path = save_token(credentials_dir, token)

        # Delete the password file if --textfile was specified
        if args.textfile:
            delete_file_if_exists(args.textfile)

        print(f"Token obtained and saved to {token_path}")
        print("Note: Keep this token secure. It can be used for subsequent API operations.")

    except APIError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()