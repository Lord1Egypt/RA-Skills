#!/usr/bin/env python3
"""
find-zip-email.py — Find files, zip them, and email to a recipient
=============================================================
A workflow script for: "Find files matching a pattern → zip them → send as email"

Environment variables required (same as agentmail-send.py):
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_NAME

Usage:
    python3 find-zip-email.py \
        --find "*.pdf" \
        --search-dir ~/Downloads \
        --to "recipient@example.com" \
        --subject "Requested files" \
        --body "Please find the requested files attached."

The script:
    1. Finds all files matching --find glob in --search-dir (non-recursive)
    2. Excludes .DS_Store, .git, and other system files
    3. Creates a timestamped zip at /tmp/
    4. Sends via SMTP using agentmail-send.py
    5. Removes the zip after sending
"""

import os
import sys
import glob
import zipfile
import argparse
import tempfile
from datetime import datetime
from pathlib import Path

# Import the send function from agentmail-send.py
# Assumes both scripts are in the same directory
script_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(script_dir))
from agentmail_send import send_email


def find_files(pattern: str, search_dir: str, recursive: bool = False) -> list:
    """Find files matching glob pattern in directory."""
    search_dir = os.path.expanduser(search_dir)
    if recursive:
        pattern = f"**/{pattern}"
        files = glob.glob(os.path.join(search_dir, pattern), recursive=True)
    else:
        files = glob.glob(os.path.join(search_dir, pattern))

    # Filter out system files and directories
    skip_names = {'.DS_Store', '.git', '.gitignore', 'Thumbs.db',
                  '.Spotlight-V100', '.Trashes', '.fseventsd'}
    result = []
    for f in files:
        basename = os.path.basename(f)
        if basename in skip_names:
            continue
        if os.path.isfile(f):
            result.append(f)
    return sorted(result)


def create_zip(file_list: list, base_dir: str = None) -> str:
    """
    Create a zip containing all files, preserving relative paths.
    Returns the path to the created zip file.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"files-{timestamp}.zip"
    zip_path = os.path.join(tempfile.gettempdir(), zip_name)

    base_dir = base_dir or os.path.commonprefix(file_list) or os.getcwd()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filepath in file_list:
            arcname = os.path.relpath(filepath, base_dir)
            zf.write(filepath, arcname)

    return zip_path


def main():
    parser = argparse.ArgumentParser(
        description="Find files, zip them, and email to a recipient"
    )
    parser.add_argument("--find",       required=True, help="Glob pattern (e.g. '*.pdf')")
    parser.add_argument("--search-dir", required=True,
                        help="Directory to search in (non-recursive)")
    parser.add_argument("--to",         required=True, help="Recipient email")
    parser.add_argument("--subject",    required=True, help="Email subject")
    parser.add_argument("--body",        default="Please find the attached files.",
                        help="Email body text")
    parser.add_argument("--recursive",  action="store_true",
                        help="Search subdirectories (use with ** glob, e.g. '**/*.pdf')")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="Don't delete the zip after sending (for debugging)")

    args = parser.parse_args()

    # Find files
    files = find_files(args.find, args.search_dir, recursive=args.recursive)

    if not files:
        print(f"No files found matching '{args.find}' in '{args.search_dir}'")
        sys.exit(1)

    print(f"Found {len(files)} file{'s' if len(files) != 1 else ''}:")
    for f in files:
        size = os.path.getsize(f)
        print(f"  {os.path.basename(f)} ({size:,} bytes)")

    # Create zip
    zip_path = create_zip(files, base_dir=os.path.expanduser(args.search_dir))
    zip_size = os.path.getsize(zip_path)
    print(f"\nCreated zip: {zip_path} ({zip_size:,} bytes)")

    # Send
    print(f"\nSending to {args.to}...")
    try:
        result = send_email(
            to=args.to,
            subject=args.subject,
            body=args.body,
            attachments=[zip_path]
        )
        print(f"Sent: {result['subject']} → {result['to']}")
    except Exception as e:
        print(f"Error sending: {e}", file=sys.stderr)
        sys.exit(1)

    # Cleanup
    if not args.no_cleanup:
        os.remove(zip_path)
        print("Zip removed after sending.")


if __name__ == "__main__":
    main()
