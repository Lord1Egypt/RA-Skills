#!/usr/bin/env python3
"""
Telegram File Sender Helper

Sends a file to a Telegram user via bot, handling size limits.

Usage:
    python3 send_file.py <source_path> <target_user_id> [caption] [accountId]

Behavior:
    - Files <= 50MB: copy to tmp, send as document, clean up
    - Files > 50MB: try zip compression, send if result <= 50MB
    - Files still > 50MB after zip: print FAIL with suggestion
    - Exit code 0 on success, 1 on failure

Output (stdout):
    Lines prefixed with KEY=VALUE for agent to parse.
    Always prints "READY" on success with all needed values.
"""

import sys
import os
import shutil
import zipfile
import tempfile

MAX_SIZE = 50 * 1024 * 1024  # 50MB


def get_file_size(path):
    return os.path.getsize(path)


def try_zip(src, dst_zip):
    """Create a zip archive of the source file. Returns zip path or None."""
    try:
        with zipfile.ZipFile(dst_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(src, arcname=os.path.basename(src))
        return dst_zip
    except Exception:
        return None


def main():
    if len(sys.argv) < 3:
        print("FAIL: Missing required arguments")
        print("Usage: send_file.py <source_path> <target> [caption] [accountId]")
        sys.exit(1)

    src_path = sys.argv[1]
    target = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else ""
    account_id = sys.argv[4] if len(sys.argv) > 4 else "CyreneAssistant_bot"

    if not os.path.exists(src_path):
        print(f"FAIL: Source file not found: {src_path}")
        sys.exit(1)

    size = get_file_size(src_path)
    filename = os.path.basename(src_path)
    tmp_dir = tempfile.mkdtemp()
    send_path = None

    try:
        if size > MAX_SIZE:
            zip_path = os.path.join(tmp_dir, filename + ".zip")
            zipped = try_zip(src_path, zip_path)
            if zipped and get_file_size(zipped) <= MAX_SIZE:
                send_path = zipped
                send_filename = filename + ".zip"
                print(f"INFO: Compressed {size/1024/1024:.1f}MB -> {get_file_size(zipped)/1024/1024:.1f}MB")
            else:
                print(f"FAIL: File too large ({size/1024/1024:.1f}MB) — compression did not reduce below 50MB")
                print("SUGGESTION: Split the file into smaller parts, or send a summary + external link")
                sys.exit(1)
        else:
            tmp_path = os.path.join(tmp_dir, filename)
            shutil.copy2(src_path, tmp_path)
            send_path = tmp_path
            send_filename = filename

        print(f"SEND_PATH={send_path}")
        print(f"SEND_FILENAME={send_filename}")
        print(f"TARGET={target}")
        print(f"CAPTION={caption}")
        print(f"ACCOUNT_ID={account_id}")
        print("READY")

    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
