#!/usr/bin/env python3
"""
Request SSH key and certificate from SJTU HPC API.

This script performs the following steps using an existing bearer token:
1. Generate SSH key pair using the token
2. Sign the public key to get SSH certificate

Usage:
    python req_certificate.py <hpc_user> [--workspace WORKSPACE] [--valid-time VALID_TIME]

Arguments:
    hpc_user: HPC username (the user who will use the SSH key)

Options:
    --workspace WORKSPACE  Absolute path to the agent's workspace (default: ~/.openclaw/workspace). Credentials will be stored in WORKSPACE/credentials.
    --valid-time VALID_TIME  Certificate validity time in seconds (default: 3600)
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


def load_token(token_dir: str) -> str:
    """Load token from the token directory."""
    token_path = os.path.join(token_dir, TOKEN_FILENAME)
    if not os.path.exists(token_path):
        raise APIError(
            f"Token文件不存在: {token_path}。请先运行 req_token.py 获取token。",
            http_code=404
        )
    with open(token_path, "r") as f:
        token = f.read().strip()
    if not token:
        raise APIError(
            f"Token文件为空: {token_path}。请先运行 req_token.py 获取token。",
            http_code=400
        )
    return token


def generate_key_pair(token: str, hpc_user: str) -> dict:
    """Generate SSH key pair using HPC API."""
    url = f"{API_BASE_URL}/gen_key"
    payload = {
        "domain": "pi",
        "hpc_user": hpc_user
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body, is_internal = parse_error_response(e)
        if is_internal:
            raise APIError(
                f"生成密钥对失败: {error_body}",
                e.code
            )
        else:
            raise APIError(
                f"生成密钥对被拒绝: {error_body}",
                e.code
            )


def sign_cert(token: str, hpc_user: str, public_key: str, valid_time: int = 3600) -> str:
    """Sign SSH public key to get certificate."""
    url = f"{API_BASE_URL}/sign_cert"
    payload = {
        "domain": "pi",
        "hpc_user": hpc_user,
        "principals": [hpc_user],
        "public_key": public_key,
        "valid_time": valid_time
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            cert = response.read().decode("utf-8")
            return cert
    except urllib.error.HTTPError as e:
        error_body, is_internal = parse_error_response(e)
        if is_internal:
            raise APIError(
                f"签名证书失败: {error_body}",
                e.code
            )
        else:
            raise APIError(
                f"签名证书被拒绝: {error_body}",
                e.code
            )


def save_files(output_path: str, private_key: str, public_key: str, certificate: str):
    """Save SSH key and certificate to files."""
    os.makedirs(output_path, exist_ok=True)

    # API always returns Ed25519 keys
    key_name = "id_ed25519"

    private_key_path = os.path.join(output_path, key_name)
    public_key_path = os.path.join(output_path, f"{key_name}.pub")
    cert_path = os.path.join(output_path, f"{key_name}-cert.pub")

    # Save private key
    with open(private_key_path, "w") as f:
        f.write(private_key)
    os.chmod(private_key_path, 0o600)

    # Save public key
    with open(public_key_path, "w") as f:
        f.write(public_key)

    # Save certificate
    with open(cert_path, "w") as f:
        f.write(certificate)

    print(f"SSH key and certificate saved to {output_path}:")
    print(f"  - Private key: {private_key_path}")
    print(f"  - Public key: {public_key_path}")
    print(f"  - Certificate: {cert_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Request SSH key and certificate from SJTU HPC API"
    )
    parser.add_argument("hpc_user", help="HPC username (the user who will use the SSH key)")
    # Default workspace path
    default_workspace = os.path.expanduser("~/.openclaw/workspace")

    parser.add_argument(
        "--workspace",
        default=default_workspace,
        help=f"Absolute path to the agent's workspace (default: {default_workspace}). Credentials will be stored in WORKSPACE/credentials."
    )
    parser.add_argument(
        "--valid-time",
        type=int,
        default=3600,
        help="Certificate validity time in seconds (default: 3600)"
    )

    args = parser.parse_args()

    # Credentials are always stored in WORKSPACE/credentials
    credentials_dir = os.path.join(args.workspace, "credentials")

    # Use credentials_dir as output_path for SSH key/cert (same directory)
    output_path = credentials_dir

    try:
        # Step 1: Load token
        token = load_token(credentials_dir)

        # Step 2: Generate key pair
        key_pair = generate_key_pair(token, args.hpc_user)
        private_key = key_pair["private_key"]
        public_key = key_pair["public_key"]

        # Step 3: Sign certificate
        certificate = sign_cert(
            token,
            args.hpc_user,
            public_key,
            args.valid_time
        )

        # Step 4: Save files
        save_files(output_path, private_key, public_key, certificate)

        print(f"Done! SSH key and certificate have been stored into {output_path}")

    except APIError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()