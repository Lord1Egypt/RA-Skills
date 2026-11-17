#!/usr/bin/env python3
"""Upload one file to a WoopSocial media upload session (standard library only).

WoopSocial uploads work in three steps:
  1. The agent calls `media_uploads_create_session` with the projectId and the file size in bytes.
  2. This script PUTs the file's bytes to each presigned part URL from that response.
  3. The agent calls `media_uploads_complete_session`. When the status is READY it includes the
     mediaId; otherwise poll `media_uploads_get_session` until it is READY (or report FAILED).

Usage:
    python3 scripts/upload_parts.py session.json shorts/clip-01.mp4

session.json is the JSON returned by `media_uploads_create_session`. It must contain
`partSizeInBytes`, `partCount` and `parts` (each with `partNumber` and `uploadUrl`).

If the PUT is blocked by a network allowlist, allow `*.r2.cloudflarestorage.com`.
"""
import json
import os
import subprocess
import sys
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
            request = urllib.request.Request(
                part["uploadUrl"], data=chunk, method="PUT",
                headers={"Content-Type": "application/octet-stream"})
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    status = response.status
            except urllib.error.HTTPError as err:
                sys.exit(f"Part {part['partNumber']} failed with HTTP {err.code}: {err.reason}")
            except urllib.error.URLError as err:
                if "CERTIFICATE_VERIFY_FAILED" in str(err.reason):
                    try:
                        status = put_with_curl(part["uploadUrl"], chunk)
                    except Exception as curl_err:
                        sys.exit(f"Part {part['partNumber']} failed: {curl_err}")
                else:
                    sys.exit(f"Part {part['partNumber']} could not connect ({err.reason}). "
                             "If a network allowlist is on, allow *.r2.cloudflarestorage.com")
            print(f"part {part['partNumber']}/{part_count} uploaded (HTTP {status})")
    print("All parts uploaded. Now call media_uploads_complete_session.")


if __name__ == "__main__":
    main()
