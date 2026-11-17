#!/usr/bin/env python3
"""Upload one file to a WoopSocial media upload session (standard library only).

WoopSocial uploads work in three steps:
  1. The agent calls `media_uploads_create_session` with the projectId and the file size in bytes.
  2. This script PUTs the file's bytes to each presigned part URL from that response.
  3. The agent calls `media_uploads_complete_session`. When the status is READY it includes the
     mediaId; otherwise poll `media_uploads_get_session` until it is READY (or report FAILED).

Usage:
    python3 scripts/upload_parts.py session.json final.mp4

session.json is the JSON returned by `media_uploads_create_session`. It must contain
`partSizeInBytes`, `partCount` and `parts` (each with `partNumber` and `uploadUrl`).

If the PUT is blocked by a network allowlist, allow `*.r2.cloudflarestorage.com`.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request


def put_with_curl(url, chunk):
    """Fallback for Python builds without system certificates (common on macOS)."""
    result = subprocess.run(
        ["curl", "-fsS", "-X", "PUT", "-H", "Content-Type: application/octet-stream",
         "--data-binary", "@-", "-o", os.devnull, "-w", "%{http_code}", url],
        input=chunk, capture_output=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="replace").strip() or "curl failed")
    return int(result.stdout.decode() or 0)


def put_once(url, chunk):
    request = urllib.request.Request(url, data=chunk, method="PUT",
                                     headers={"Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return response.status
    except urllib.error.URLError as err:
        if "CERTIFICATE_VERIFY_FAILED" in str(getattr(err, "reason", err)):
            return put_with_curl(url, chunk)
        raise


def put_part(part, chunk, tries=4):
    """PUT one part; a dropped connection or a server hiccup is retried with a growing pause, so
    one bad moment doesn't sink a multi-gigabyte upload."""
    n = part["partNumber"]
    for attempt in range(1, tries + 1):
        try:
            status = put_once(part["uploadUrl"], chunk)
            if 200 <= status < 300:
                return status
            problem = f"HTTP {status}"
        except urllib.error.HTTPError as err:
            if err.code == 403:
                sys.exit(f"Part {n} was refused (HTTP 403): the upload links have probably expired. "
                         "Create a new upload session and run this again.")
            problem = f"HTTP {err.code}: {err.reason}"
        except (urllib.error.URLError, OSError, RuntimeError, subprocess.TimeoutExpired) as err:
            problem = str(getattr(err, "reason", err))
        if attempt < tries:
            wait = 5 * attempt
            print(f"part {n}: {problem}; retrying in {wait} s", file=sys.stderr)
            time.sleep(wait)
    sys.exit(f"Part {n} failed after {tries} tries ({problem}). Check the connection; if a network "
             "allowlist is on, allow *.r2.cloudflarestorage.com. Then run this again.")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    session_path, file_path = sys.argv[1], sys.argv[2]
    with open(session_path, encoding="utf-8") as f:
        session = json.load(f)
    part_size = int(session["partSizeInBytes"])
    parts = sorted(session["parts"], key=lambda p: p["partNumber"])
    part_count = int(session.get("partCount", len(parts)))
    size = os.path.getsize(file_path)

    needed = -(-size // part_size)
    if needed != part_count or len(parts) != part_count:
        sys.exit(f"The session expects {part_count} part(s) but the file needs {needed}. "
                 "Create the session with the exact file size in bytes.")

    with open(file_path, "rb") as f:
        for part in parts:
            chunk = f.read(part_size)
            status = put_part(part, chunk)
            print(f"part {part['partNumber']}/{part_count} uploaded (HTTP {status})")
    print("All parts uploaded. Now call media_uploads_complete_session.")


if __name__ == "__main__":
    main()
