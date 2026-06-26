#!/usr/bin/env python3
"""
OpenClaw Backup Script
Handles encrypted backup operations for OpenClaw Agent workspace files.
Uses tar + openssl (AES-256-CBC) encryption and soul-upload.com API.

Password Policy: Auto-generates a new random password for each backup.
Do not reuse passwords across backups.
"""

import argparse
import json
import os
import secrets
import string
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

# Constants
BASE_URL = "https://soul-upload.com"
MAX_BACKUP_SIZE = 20 * 1024 * 1024  # 20 MB in bytes
PASSWORD_LENGTH = 32  # Random password length


class BackupError(Exception):
    """Base exception for backup operations"""
    pass


def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length: Password length (default: 32 characters)

    Returns:
        Random password string containing letters, digits, and symbols
    """
    # Use all printable ASCII characters except space and quotes
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def check_dependencies():
    """Verify required system tools are available"""
    required_tools = ["tar", "openssl", "curl"]
    missing = []

    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,
                          check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(tool)

    if missing:
        raise BackupError(f"Missing required tools: {', '.join(missing)}")


def upload_backup(files: List[str], password: Optional[str] = None) -> Dict:
    """
    Encrypt files and upload to soul-upload.com

    Args:
        files: List of file paths to backup
        password: Encryption password (auto-generated if not provided)

    Returns:
        Dict with backupId, downloadUrl, sizeBytes, sha256, and password
    """
    # Auto-generate password if not provided
    if password is None:
        password = generate_password()
        print(f"Auto-generated password: {password}", file=sys.stderr)

    # Validate files exist
    missing_files = [f for f in files if not os.path.exists(f)]
    if missing_files:
        raise BackupError(f"Files not found: {', '.join(missing_files)}")

    temp_backup = None
    try:
        # Create temporary encrypted backup file
        temp_backup = tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False)
        temp_backup.close()

        # Step 1: Create tar archive and encrypt with openssl
        print(f"Encrypting {len(files)} file(s)...", file=sys.stderr)

        # Build tar command
        tar_cmd = ["tar", "-czf", "-"] + files

        # Build openssl command
        openssl_cmd = [
            "openssl", "enc", "-aes-256-cbc", "-salt",
            "-k", password, "-out", temp_backup.name
        ]

        # Pipe tar output to openssl
        tar_proc = subprocess.Popen(tar_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        openssl_proc = subprocess.Popen(openssl_cmd, stdin=tar_proc.stdout,
                                       stderr=subprocess.PIPE)
        tar_proc.stdout.close()  # Allow tar to receive SIGPIPE if openssl exits

        # Wait for both processes
        openssl_stderr = openssl_proc.communicate()[1]
        tar_proc.wait()

        if tar_proc.returncode != 0:
            raise BackupError("tar command failed")
        if openssl_proc.returncode != 0:
            raise BackupError(f"openssl encryption failed: {openssl_stderr.decode()}")

        # Step 2: Check file size
        backup_size = os.path.getsize(temp_backup.name)
        print(f"Encrypted backup size: {backup_size / 1024 / 1024:.2f} MB", file=sys.stderr)

        if backup_size > MAX_BACKUP_SIZE:
            raise BackupError(
                f"Backup size ({backup_size / 1024 / 1024:.2f} MB) exceeds "
                f"limit ({MAX_BACKUP_SIZE / 1024 / 1024} MB)"
            )

        # Step 3: Upload to API using application/octet-stream
        print("Uploading to soul-upload.com...", file=sys.stderr)

        with open(temp_backup.name, 'rb') as f:
            headers = {
                'Content-Type': 'application/octet-stream',
                'X-Backup-Filename': 'backup.tar.gz'
            }
            response = requests.post(
                f"{BASE_URL}/backup",
                data=f,
                headers=headers,
                timeout=300  # 5 minutes timeout
            )

        if response.status_code == 413:
            raise BackupError("File too large (413 Payload Too Large)")
        elif response.status_code != 200:
            raise BackupError(
                f"Upload failed with status {response.status_code}: {response.text}"
            )

        result = response.json()

        # Add password to result
        result['password'] = password

        print("Upload successful!", file=sys.stderr)

        return result

    finally:
        # Cleanup temporary file
        if temp_backup and os.path.exists(temp_backup.name):
            try:
                os.unlink(temp_backup.name)
            except Exception:
                pass


def download_backup(backup_id: str, password: str, output_dir: str = ".") -> List[str]:
    """
    Download and decrypt backup from soul-upload.com

    Args:
        backup_id: UUID of the backup to download
        password: Decryption password
        output_dir: Directory to extract files to

    Returns:
        List of extracted file paths
    """
    temp_backup = None
    try:
        # Create temporary file for download
        temp_backup = tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False)
        temp_backup.close()

        # Step 1: Download from API
        print(f"Downloading backup {backup_id}...", file=sys.stderr)

        response = requests.get(
            f"{BASE_URL}/backup/{backup_id}",
            allow_redirects=True,
            timeout=300
        )

        if response.status_code == 404:
            raise BackupError(f"Backup not found: {backup_id}")
        elif response.status_code != 200:
            raise BackupError(
                f"Download failed with status {response.status_code}: {response.text}"
            )

        # Save downloaded file
        with open(temp_backup.name, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {len(response.content) / 1024 / 1024:.2f} MB", file=sys.stderr)

        # Step 2: Decrypt and extract
        print("Decrypting and extracting...", file=sys.stderr)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Build openssl decrypt command
        openssl_cmd = [
            "openssl", "enc", "-aes-256-cbc", "-d",
            "-k", password, "-in", temp_backup.name
        ]

        # Build tar extract command
        tar_cmd = ["tar", "-xzf", "-", "-C", output_dir, "-v"]

        # Pipe openssl output to tar
        openssl_proc = subprocess.Popen(openssl_cmd, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        tar_proc = subprocess.Popen(tar_cmd, stdin=openssl_proc.stdout,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        openssl_proc.stdout.close()

        # Get output
        tar_stdout, tar_stderr = tar_proc.communicate()
        openssl_proc.wait()

        if openssl_proc.returncode != 0:
            raise BackupError(
                "Decryption failed - wrong password or corrupted file"
            )
        if tar_proc.returncode != 0:
            raise BackupError(f"tar extraction failed: {tar_stderr.decode()}")

        # Parse extracted file list
        extracted_files = [
            line.strip() for line in tar_stdout.decode().split('\n')
            if line.strip()
        ]

        print(f"Successfully extracted {len(extracted_files)} file(s)", file=sys.stderr)

        return extracted_files

    finally:
        # Cleanup temporary file
        if temp_backup and os.path.exists(temp_backup.name):
            try:
                os.unlink(temp_backup.name)
            except Exception:
                pass


def delete_backup(backup_id: str) -> Dict:
    """
    Delete backup from soul-upload.com

    Args:
        backup_id: UUID of the backup to delete

    Returns:
        Dict with success status and backupId
    """
    print(f"Deleting backup {backup_id}...", file=sys.stderr)

    response = requests.delete(
        f"{BASE_URL}/backup/{backup_id}",
        timeout=30
    )

    if response.status_code == 404:
        raise BackupError(f"Backup not found: {backup_id}")
    elif response.status_code != 200:
        raise BackupError(
            f"Delete failed with status {response.status_code}: {response.text}"
        )

    result = response.json()
    print("Delete successful!", file=sys.stderr)

    return result


def main():
    """Main entry point with argparse subcommands"""
    parser = argparse.ArgumentParser(
        description="OpenClaw Backup Tool - Encrypted backup for agent workspace files"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Upload subcommand
    upload_parser = subparsers.add_parser('upload', help='Upload encrypted backup')
    upload_parser.add_argument('--files', required=True,
                              help='Space-separated list of files to backup')
    upload_parser.add_argument('--password', required=False,
                              help='Encryption password (auto-generated if not provided)')

    # Download subcommand
    download_parser = subparsers.add_parser('download', help='Download and decrypt backup')
    download_parser.add_argument('--backup-id', required=True,
                                help='UUID of backup to download')
    download_parser.add_argument('--password', required=True,
                                help='Decryption password')
    download_parser.add_argument('--output-dir', default='.',
                                help='Directory to extract files to (default: current directory)')

    # Delete subcommand
    delete_parser = subparsers.add_parser('delete', help='Delete backup from server')
    delete_parser.add_argument('--backup-id', required=True,
                              help='UUID of backup to delete')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Check system dependencies
        check_dependencies()

        # Execute command
        if args.command == 'upload':
            files = args.files.split()
            result = upload_backup(files, args.password)
            print(json.dumps(result, indent=2))

        elif args.command == 'download':
            extracted = download_backup(args.backup_id, args.password, args.output_dir)
            result = {
                "success": True,
                "extractedFiles": extracted,
                "outputDir": os.path.abspath(args.output_dir)
            }
            print(json.dumps(result, indent=2))

        elif args.command == 'delete':
            result = delete_backup(args.backup_id)
            print(json.dumps(result, indent=2))

        sys.exit(0)

    except BackupError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(json.dumps({"error": f"Network error: {str(e)}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {str(e)}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
