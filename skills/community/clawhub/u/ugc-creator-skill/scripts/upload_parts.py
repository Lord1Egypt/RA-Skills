#!/usr/bin/env python3
"""Upload one file to a WoopSocial media upload session (standard library only).

WoopSocial uploads work in three steps:
  1. The agent calls `media_uploads_create_session` with the projectId and the file size in bytes.
  2. This script PUTs the file's bytes to each presigned part URL from that response.
  3. The agent calls `media_uploads_complete_session`. When the status is READY it includes the
     mediaId; otherwise poll `media_uploads_get_session` until it is READY (or report FAILED).

Usage:
    python3 scripts/upload_parts.py session.json videos/tiktok.mp4
    python3 scripts/upload_parts.py --complete reply.json videos/tiktok.mp4

session.json is the JSON returned by `media_uploads_create_session`, saved as it came back. It
must contain `partSizeInBytes` and `parts` (each with `partNumber` and `uploadUrl`). The second
argument is the video to upload. Both paths are relative to the folder you run from.

It uploads only a file that a recorded yes (yes.json from plan.py --yes, less than 3 hours old)
covers with its exact fingerprint. When every part is in, it prints the file's SHA-256 and records
it, with the upload session id, in uploaded.json next to the video. Then save the reply of
`media_uploads_complete_session` (status READY) as reply.json and run --complete: it records the
mediaId against the same file and session. plan.py --media only accepts a mediaId recorded this way,
so a mediaId can never be swapped onto another file.

A part that fails on the network is tried three times. If the PUT is blocked by a network
allowlist, allow `*.r2.cloudflarestorage.com`.
"""
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ugclib import die, guard, iso, locked_update, now_utc, parse_time, read_json, reading, rel, sha256  # noqa: E402

YES_HOURS = 3


def covering_yes(file_path):
    """The yes.json (written by plan.py --yes) that covers this exact file: looked for in the folder
    you run from, then in the file's own folder and the folders above it."""
    full = os.path.abspath(file_path)
    dirs = [os.getcwd()]
    d = os.path.dirname(full)
    for _ in range(4):
        dirs.append(d)
        d = os.path.dirname(d)
    fp = sha256(full)
    for d in dirs:
        y = os.path.join(d, "yes.json")
        if not os.path.isfile(y):
            continue
        data = read_json(y, "the recorded yes")
        if not isinstance(data, dict) or data.get("written_by") != "plan.py":
            continue
        try:
            key = os.path.relpath(full, d).replace(os.sep, "/")
        except ValueError:   # another drive (Windows): this yes can't cover the file
            continue
        if (data.get("files") or {}).get(key) == fp:
            t = parse_time(data.get("at"))
            if not t or (now_utc() - t).total_seconds() > YES_HOURS * 3600:
                die(f"the yes in {y} is more than {YES_HOURS} hours old. Show the plan again and ask for a new yes "
                    "before uploading")
            return y
    die(f"no yes covers {file_path} as it is now (plan.py --yes writes yes.json with each file's fingerprint). Show "
        "the plan, get a clear yes, then upload. A file changed after the yes needs a new one")

USAGE = "usage: upload_parts.py session.json <video file>   or   upload_parts.py --complete reply.json <video file>"
NOT_A_SESSION = ("is not the reply of media_uploads_create_session: it needs partSizeInBytes and parts, each "
                 "with partNumber and uploadUrl. Save that reply as it came back and run this again")


def put_with_curl(url, chunk):
    """Fallback for Python builds without system certificates (common on macOS)."""
    result = subprocess.run(
        ["curl", "-fsS", "-X", "PUT", "-H", "Content-Type: application/octet-stream",
         "--data-binary", "@-", "-o", os.devnull, "-w", "%{http_code}", url],
        input=chunk, capture_output=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError((result.stderr.decode(errors="replace").strip().splitlines() or ["curl failed"])[-1])
    try:
        return int(result.stdout.decode() or 0)
    except ValueError:
        return 0


def plain(err):
    """A network error in a few plain words: 'Connection refused', not '[Errno 61] ...'."""
    text = getattr(err, "strerror", None) or str(err) or "no answer"
    text = re.sub(r"\[[^\]]*\]\s*", "", text).strip() or "no answer"
    return text.splitlines()[0][:120]


def put(url, chunk):
    request = urllib.request.Request(url, data=chunk, method="PUT",
                                     headers={"Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status
    except urllib.error.HTTPError:
        raise
    except urllib.error.URLError as err:
        if "CERTIFICATE_VERIFY_FAILED" in str(err.reason):
            return put_with_curl(url, chunk)
        raise


def load_session(session_path):
    """The parts to upload, in order, and the size of each. Dies with one line when the file is
    anything other than the saved reply of media_uploads_create_session."""
    session = read_json(session_path)
    for wrap in ("result", "data", "session", "structuredContent"):   # the whole tool reply was saved
        if isinstance(session, dict) and "parts" not in session and isinstance(session.get(wrap), dict):
            session = session[wrap]
    if not isinstance(session, dict):
        die(f"{session_path} {NOT_A_SESSION}")
    size, parts = session.get("partSizeInBytes"), session.get("parts")
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0 or not isinstance(parts, list) or not parts:
        die(f"{session_path} {NOT_A_SESSION}")
    for p in parts:
        number = p.get("partNumber") if isinstance(p, dict) else None
        if isinstance(number, bool) or not isinstance(number, int) or not isinstance(p.get("uploadUrl"), str):
            die(f"{session_path} {NOT_A_SESSION}")
        if not p["uploadUrl"].startswith("https://"):
            die(f"{session_path}: the uploadUrl of part {number} is not an https:// link. Create a new "
                "session (media_uploads_create_session) and save its reply as it came back")
    count = session.get("partCount", len(parts))
    if isinstance(count, bool) or not isinstance(count, int) or count != len(parts):
        die(f"{session_path} says {count} part(s) but lists {len(parts)}. Create a new session "
            "(media_uploads_create_session) and save its reply as it came back")
    numbers = sorted(p["partNumber"] for p in parts)
    if numbers != list(range(1, len(parts) + 1)):
        die(f"{session_path} lists part numbers {numbers}; they should run 1 to {len(parts)} once each. Create a new "
            "session (media_uploads_create_session) and save its reply as it came back")
    return size, sorted(parts, key=lambda p: p["partNumber"])


def unwrap(reply):
    for wrap in ("result", "data", "session", "structuredContent", "upload", "media"):
        if isinstance(reply, dict) and isinstance(reply.get(wrap), dict) and not any(
                k in reply for k in ("mediaId", "status")):
            reply = reply[wrap]
    return reply


def complete(reply_path, file_path):
    """--complete: record the mediaId from media_uploads_complete_session's reply against this file."""
    if not os.path.isfile(reply_path):
        die(f"{reply_path} not found. Save the reply of media_uploads_complete_session (or media_uploads_get_session once "
            "it is READY) as that file")
    if not os.path.isfile(file_path):
        die(f"{file_path} not found (the video you uploaded is the second argument)")
    reply = unwrap(read_json(reply_path, "the complete-session reply"))
    if not isinstance(reply, dict):
        die(f"{reply_path} is not the reply of media_uploads_complete_session")
    status = str(reply.get("status") or "").upper()
    mid = reply.get("mediaId")
    if mid is None and isinstance(reply.get("media"), dict):
        mid = reply["media"].get("id") or reply["media"].get("mediaId")
    if status and status != "READY":
        die(f"the upload session is {status}, not READY. Poll media_uploads_get_session until it is READY (or upload "
            "again if it FAILED), save that reply and run this again")
    if not isinstance(mid, str) or not mid.strip():
        die(f"{reply_path} has no mediaId. It appears once the session is READY: poll media_uploads_get_session")
    sid = next((reply.get(k) for k in ("uploadSessionId", "sessionId", "id") if isinstance(reply.get(k), str)
                and reply.get(k) != mid), None)
    full = os.path.abspath(file_path)
    sha = sha256(full)
    name = os.path.basename(full)
    rec_path = os.path.join(os.path.dirname(full), "uploaded.json")

    def change(rec):
        got = rec.get(name)
        if not isinstance(got, dict) or got.get("sha256") != sha:
            die(f"{rel(full)} as it is now was never uploaded with upload_parts.py (or it changed after). Upload it "
                "first, then record the mediaId")
        if sid and got.get("uploadSessionId") and got["uploadSessionId"] != sid:
            die(f"this reply is for upload session {sid}, and {name} went up in session {got['uploadSessionId']}. Save "
                "the reply of that session")
        for other, x in rec.items():
            if other != name and isinstance(x, dict) and x.get("mediaId") == mid:
                die(f"mediaId {mid} is already recorded for {other}. Each file has its own upload and mediaId")
        got["mediaId"] = mid.strip()
        got["completed"] = iso(now_utc())
    locked_update(rec_path, change, "the upload record")
    print(f"mediaId {mid} recorded for {rel(full)} (sha256 {sha[:12]}) in {rel(rec_path)}. Put it in media.json with "
          "that sha256")


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--complete":
        complete(sys.argv[2], sys.argv[3])
        return
    if len(sys.argv) != 3:
        die(USAGE)
    session_path, file_path = sys.argv[1], sys.argv[2]
    if not os.path.exists(session_path):
        die(f"{session_path} not found. Save the reply of media_uploads_create_session as that file first. {USAGE}")
    if os.path.isdir(file_path):
        die(f"{file_path} is a folder; give the one video file to upload")
    if not os.path.isfile(file_path):
        die(f"{file_path} not found (the video to upload is the second argument)")
    if not session_path.lower().endswith(".json") and file_path.lower().endswith(".json"):
        die(f"the two arguments are the wrong way round. {USAGE}")
    part_size, parts = load_session(session_path)
    covering_yes(file_path)
    raw = read_json(session_path)
    for wrap in ("result", "data", "session", "structuredContent"):
        if isinstance(raw, dict) and "parts" not in raw and isinstance(raw.get(wrap), dict):
            raw = raw[wrap]
    session_id = next((raw.get(k) for k in ("uploadSessionId", "sessionId", "id") if isinstance(raw.get(k), str)), None)
    reading(file_path)
    size = os.path.getsize(file_path)
    if not size:
        die(f"{file_path} is an empty file (0 bytes); there is nothing to upload")
    needed = -(-size // part_size)
    if needed != len(parts):
        die(f"the session expects {len(parts)} part(s) but {file_path} ({size} bytes) needs {needed}. Create "
            "the session again with this file's exact size in bytes (fileSizeInBytes)")

    digest = hashlib.sha256()
    with open(file_path, "rb") as f:
        for part in parts:
            chunk = f.read(part_size)
            digest.update(chunk)
            number = part["partNumber"]
            status, why = None, ""
            for attempt in range(3):
                if attempt:
                    time.sleep(attempt * 2 - 1)   # 1 s, then 3 s
                try:
                    status = put(part["uploadUrl"], chunk)
                    if 200 <= status < 300:
                        break
                    why, status = f"HTTP {status}", None
                except urllib.error.HTTPError as err:
                    if err.code in (400, 401, 403, 404, 410):
                        die(f"part {number} was refused (HTTP {err.code}): the upload link has expired or was "
                            "already used. Create a new session (media_uploads_create_session) and run this again")
                    why = f"HTTP {err.code}"
                except (urllib.error.URLError, OSError, http.client.HTTPException, RuntimeError,
                        subprocess.SubprocessError) as err:
                    why = plain(getattr(err, "reason", None) or err)
            if status is None:
                die(f"part {number} could not be uploaded after 3 tries ({why}). Check the internet connection "
                    "and run the same command again; if a network allowlist is on, allow *.r2.cloudflarestorage.com")
            print(f"part {number}/{len(parts)} uploaded (HTTP {status})")
    sha = digest.hexdigest()
    rec_path = os.path.join(os.path.dirname(os.path.abspath(file_path)), "uploaded.json")

    def change(rec):
        rec[os.path.basename(file_path)] = {"sha256": sha, "bytes": size, "uploaded": iso(now_utc()),
                                            "uploadSessionId": session_id}
    locked_update(rec_path, change, "the upload record")
    print(f"sha256 {sha} (recorded in {rel(rec_path)})")
    print("All parts uploaded. Now call media_uploads_complete_session, save its reply (status READY) as reply.json and "
          f"run: upload_parts.py --complete reply.json {file_path}. Then put the mediaId and this sha256 in media.json.")


if __name__ == "__main__":
    guard(main)
