#!/usr/bin/env python3
"""
nxvet_poll.py — local-only NxVET voice-note poller (stdlib only, no pip installs).

Reads .env (NXVET_API_KEY) + config.json, fetches recent voice notes for the
configured source ("labels" or "nxhub"), skips already-processed and still-empty
transcripts, and prints the NEW transcripts as a JSON array on stdout for the
classifier (Claude) to bucket into calendar events / follow-ups / ideas.

Design notes (see reference/caching-and-state.md):
  * Idempotency via state/processed_ids.json — a note is only marked processed
    AFTER its outputs are written, so a crash re-processes rather than loses it.
    THIS SCRIPT DOES NOT MARK ANYTHING PROCESSED — it only reports new notes.
    Whatever writes the outputs is responsible for calling mark_processed().
  * Overlapping poll window: we always re-scan the last WINDOW_HOURS and rely on
    processed_ids to skip handled notes, so late-arriving (flaky-WiFi) notes are
    not dropped by a strict cursor.
  * Empty transcripts ("{}"/null) are left UNprocessed for the next poll.

The only network calls are authenticated GETs to https://app.nx.vet.
Never prints the full API key.

Usage:
    python3 nxvet_poll.py                 # print new transcripts as JSON
    python3 nxvet_poll.py --window-hours 48
    python3 nxvet_poll.py --mark ID1 ID2  # mark ids processed (call after outputs written)
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

BASE_URL = "https://app.nx.vet"
WINDOW_HOURS_DEFAULT = 24
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.getcwd()  # run from the project folder

CONFIG_PATH = os.path.join(PROJECT, "config.json")
STATE_DIR = os.path.join(PROJECT, "state")
PROCESSED_PATH = os.path.join(STATE_DIR, "processed_ids.json")
RUN_LOG = os.path.join(STATE_DIR, "run.log")


# ---------- small helpers ----------

def load_env_key():
    """Read NXVET_API_KEY from env or ./.env. Never returned to logs in full.
    Falls back to ANY .env variable whose value starts with nxvet_sk_ (users
    often name the key after their org, e.g. MYCLINIC_API_KEY)."""
    key = os.environ.get("NXVET_API_KEY")
    if key:
        return key.strip()
    env_path = os.path.join(PROJECT, ".env")
    fallback = None
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("NXVET_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                if "=" in line and not line.startswith("#"):
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v.startswith("nxvet_sk_"):
                        fallback = v
    if fallback:
        return fallback
    sys.exit("ERROR: NXVET_API_KEY not found in environment or ./.env")


def mask(key):
    return f"nxvet_sk_…{key[-4:]}" if key and len(key) >= 4 else "nxvet_sk_…"


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json_atomic(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def log_run(line):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(RUN_LOG, "a") as f:
        f.write(line + "\n")


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# ---------- HTTP with backoff ----------

def api_get(path, key, params=None, tries=5):
    url = BASE_URL + path
    if params:
        # urlencode-lite; supports repeated keys via list values
        parts = []
        for k, v in params.items():
            if isinstance(v, (list, tuple)):
                for item in v:
                    parts.append(f"{k}={urllib.request.quote(str(item))}")
            else:
                parts.append(f"{k}={urllib.request.quote(str(v))}")
        url += "?" + "&".join(parts)

    backoff = 1.0
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else None, dict(resp.headers)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                retry_after = e.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else backoff
                time.sleep(min(delay, 60))
                backoff *= 2
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < tries - 1:
                time.sleep(min(backoff, 60))
                backoff *= 2
                continue
            raise
    raise RuntimeError("exhausted retries")


# ---------- transcript extraction ----------

def parse_maybe_json(value):
    """metadata / note content are sometimes JSON strings inside JSON — parse twice."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value
    return value


def transcript_text(detail):
    """Best-effort extraction of transcript text from a label/conversation detail.
    Returns "" if empty/unprocessed (so caller leaves it for the next poll)."""
    if not detail:
        return ""
    # Labels: the raw transcript lives in ownedPatientNotes[] (populated only in
    # DETAIL responses). Each label typically has two notes — type "Transcript"
    # (plain text with speaker labels) and type "SOAP" (a JSON string). Prefer
    # the type field; fall back to "whichever entry isn't JSON" for robustness.
    # Verified against live production data (2026-07).
    notes_list = detail.get("ownedPatientNotes") or []
    for note in notes_list:
        c = (note.get("content") or "").strip()
        if note.get("type") == "Transcript" and c and c != "{}":
            return c
    for note in notes_list:
        c = (note.get("content") or "").strip()
        if not c or c == "{}":
            continue
        if isinstance(parse_maybe_json(c), (dict, list)):
            continue  # the SOAP/clinical-note JSON — not the raw transcript
        return c
    # NxHub conversations and other shapes:
    for field in ("transcript", "transcription", "text"):
        v = detail.get(field)
        if isinstance(v, str) and v.strip() and v.strip() != "{}":
            return v.strip()
    notes = parse_maybe_json(detail.get("notes") or detail.get("content"))
    if isinstance(notes, dict):
        for field in ("transcript", "text", "summary"):
            v = notes.get(field)
            if isinstance(v, str) and v.strip():
                return v.strip()
    if isinstance(notes, str) and notes.strip() and notes.strip() != "{}":
        return notes.strip()
    return ""


# ---------- sources ----------

def uuid7_ms(uid):
    """Label ids are UUIDv7: the first 48 bits are creation time in epoch ms.
    Used as a windowing fallback when a row carries no usable timestamp."""
    try:
        return int(uid.replace("-", "")[:12], 16)
    except (ValueError, AttributeError):
        return None


def fetch_labels(cfg, key, since_iso):
    """List label ids newer than since_iso, newest first.

    Gotchas verified against live production data (2026-07):
    - List rows have NO createdAt — window on `fromTime` (epoch ms), falling
      back to the UUIDv7 id timestamp.
    - The type filter is `types=` REPEATED (types=A&types=B). `types[]=` is
      silently ignored and returns an empty list — do not use it.
    """
    org = cfg["organizationId"]
    since_ms = datetime.fromisoformat(since_iso).timestamp() * 1000
    dev_serial = cfg.get("deviceSerial")
    out = []
    offset, limit = 0, 50
    while True:
        params = {"limit": limit, "offset": offset}
        types = cfg.get("labelTypes")
        if types:
            params["types"] = types  # list value → repeated types= params
        listing, _ = api_get(f"/api/organizations/{org}/labels", key, params)
        rows = listing if isinstance(listing, list) else listing.get("data", [])
        if not rows:
            break
        for row in rows:
            ms = row.get("fromTime") or uuid7_ms(row["id"])
            if ms and ms < since_ms:
                return out  # newest-first: everything past here is older
            if dev_serial and row.get("deviceSerial") not in (None, dev_serial):
                continue  # another device's label
            out.append(row["id"])
        offset += limit
        if len(rows) < limit:
            break
    return out


def fetch_label_detail(label_id, key):
    detail, _ = api_get(f"/api/labels/{label_id}", key)
    return detail


def fetch_nxhub(cfg, key, since_iso):
    org, dev = cfg["organizationId"], cfg.get("deviceId")
    out, token = [], None
    while True:
        params = {"organizationId": org, "pageSize": 50}
        if dev:
            params["deviceId"] = dev
        if token:
            params["pageToken"] = token
        listing, _ = api_get("/api/nxhub/conversations", key, params)
        rows = listing.get("conversations") or listing.get("data") or []
        for row in rows:
            created = row.get("createdAtIso") or row.get("createdAt") or ""
            if isinstance(created, str) and created and created < since_iso:
                return out
            out.append((dev or row.get("deviceId"), row.get("id") or row.get("conversationId")))
        if not listing.get("hasMore"):
            break
        token = listing.get("nextPageToken") or listing.get("pageToken")
        if not token:
            break
    return out


def fetch_nxhub_detail(dev, conv_id, key):
    detail, _ = api_get(f"/api/nxhub/conversations/{dev}/{conv_id}", key)
    return detail


# ---------- main ----------

def cmd_mark(ids):
    processed = load_json(PROCESSED_PATH, {"labels": [], "nxhub": [], "last_run_iso": None})
    src_key = "labels"  # ids are stored flat; keep both buckets deduped
    for bucket in ("labels", "nxhub"):
        processed.setdefault(bucket, [])
    seen = set(processed["labels"]) | set(processed["nxhub"])
    for i in ids:
        if i not in seen:
            processed[src_key].append(i)
    processed["last_run_iso"] = now_iso()
    save_json_atomic(PROCESSED_PATH, processed)
    print(f"marked {len(ids)} id(s) processed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window-hours", type=int, default=WINDOW_HOURS_DEFAULT)
    ap.add_argument("--mark", nargs="+", help="mark these ids processed and exit")
    args = ap.parse_args()

    if args.mark:
        cmd_mark(args.mark)
        return

    key = load_env_key()
    cfg = load_json(CONFIG_PATH, None)
    if not cfg:
        sys.exit(f"ERROR: {CONFIG_PATH} not found — run Phase 0/1 first")
    source = cfg.get("source")
    if source not in ("labels", "nxhub"):
        sys.exit('ERROR: config.json "source" must be "labels" or "nxhub" (run Phase 1)')

    processed = load_json(PROCESSED_PATH, {"labels": [], "nxhub": [], "last_run_iso": None})
    done = set(processed.get("labels", [])) | set(processed.get("nxhub", []))
    since = (datetime.now(timezone.utc) - timedelta(hours=args.window_hours)).isoformat()

    new_items, fetched, empty = [], 0, 0
    try:
        if source == "labels":
            ids = fetch_labels(cfg, key, since)
            fetched = len(ids)
            for lid in ids:
                if lid in done:
                    continue
                detail = fetch_label_detail(lid, key)
                text = transcript_text(detail)
                if not text:
                    empty += 1
                    continue
                # classifier resolves relative dates against the RECORDING's time
                ft = detail.get("fromTime")
                rec_iso = (datetime.fromtimestamp(ft / 1000, timezone.utc).isoformat()
                           if ft else None)
                new_items.append({"id": lid, "source": "labels",
                                  "recordedAt": rec_iso, "transcript": text})
        else:
            pairs = fetch_nxhub(cfg, key, since)
            fetched = len(pairs)
            for dev, cid in pairs:
                if cid in done:
                    continue
                text = transcript_text(fetch_nxhub_detail(dev, cid, key))
                if not text:
                    empty += 1
                    continue
                new_items.append({"id": cid, "source": "nxhub",
                                  "deviceId": dev, "transcript": text})
    except Exception as e:  # network/API failure → no-op run, exit 0
        log_run(f"{now_iso()}  API error: {e} — will retry next run  [key={mask(key)}]")
        print("[]")
        return

    log_run(f"{now_iso()}  fetched={fetched} new={len(new_items)} "
            f"empty-skipped={empty}  ok  [key={mask(key)}]")
    print(json.dumps(new_items, indent=2))


if __name__ == "__main__":
    main()
