"""
TextOps transcription script.
Usage:
  python transcribe.py --file <path_or_url> [--diarization true|false]
                       [--output-format json|text] [--output-path <path>]
  python transcribe.py --job-id <id> [--output-format json|text] [--output-path <path>]
"""

import argparse
import json
import os
import sys
import time
import requests

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── API config ───────────────────────────────────────────────────────────────

API_KEY = os.environ.get("TEXTOPS_API_KEY", "")



GET_UPLOAD_URL   = "https://text-ops-subs.com/api/v2/upload-url"
SUBMIT_MODAL_URL = "https://text-ops-subs.com/api/v2/transcribe"
CHECK_JOB_URL    = "https://text-ops-subs.com/api/v2/transcribe-status"
PROBE_URL        = "https://text-ops-subs.com/api/v2/probe"

SECS_PER_MIN     = 0.83   # 1 min of audio ≈ 0.83s → 1h file: first check ~40s (no diarization)
DIARIZATION_MULT = 2.25   # diarization ×2.25 → 1h file: first check ~90s
POLL_INTERVAL    = 5      # seconds between polls
SMALL_FILE_MB    = 20     # threshold in MB (local files)
SMALL_DURATION_SEC = 1200 # threshold in seconds = 20 min (URL files)
MAX_FILE_MB      = 2048   # 2 GB upload limit
MAX_POLLS        = 180    # 180 × 5s = 15 min max



_start_time = None

def log(msg):
    """Print with immediate flush so output streams in real time."""
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8"), flush=True)

def elapsed():
    """Seconds elapsed since script start, as integer."""
    return int(time.time() - _start_time) if _start_time else 0


# ── duration detection ───────────────────────────────────────────────────────

def _try_ffprobe(file_path):
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path],
        capture_output=True, text=True, timeout=10
    )
    info = json.loads(result.stdout)
    for stream in info["streams"]:
        if "duration" in stream:
            return float(stream["duration"])
    return None


def _try_moviepy(file_path):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()
    return float(duration) if duration else None


def get_duration_seconds(file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        return None
    for _, fn in [("ffprobe", _try_ffprobe), ("moviepy", _try_moviepy)]:
        try:
            result = fn(file_path)
            if result and result > 0:
                return result
        except Exception:
            pass
    return None


def calc_initial_wait(duration_sec, has_diarization):
    if duration_sec is None:
        return None
    wait = (duration_sec / 60) * SECS_PER_MIN
    if has_diarization:
        wait *= DIARIZATION_MULT
    return wait * 0.8  # start checking 20% before estimated finish


# ── probe URL ────────────────────────────────────────────────────────────────

def probe_url(url):
    """Check accessibility and metadata of a remote audio/video URL."""
    res = requests.post(PROBE_URL, json={"url": url},
                        headers={"textops-api-key": API_KEY})
    res.raise_for_status()
    return res.json()


# ── upload (for local files) ─────────────────────────────────────────────────

def get_signed_urls(filename):
    log(f"[UPLOAD] Getting signed URL for: {filename}")
    res = requests.post(GET_UPLOAD_URL, json={"filename": filename},
                        headers={"textops-api-key": API_KEY})
    res.raise_for_status()
    return res.json()


def upload_file(upload_url, file_path, filename):
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    log(f"[UPLOAD] Uploading: {filename} ({size_mb:.1f} MB)...")
    with open(file_path, "rb") as f:
        res = requests.put(upload_url, data=f)
    if res.status_code == 403:
        log("ERROR: Upload 403 — signed URL may have expired, try again")
        sys.exit(1)
    res.raise_for_status()
    log(f"[UPLOAD] Complete: {filename}")


# ── submit + poll ─────────────────────────────────────────────────────────────

def submit_job(download_url, has_diarization, word_timestamps=False, min_speakers=1, max_speakers=10):
    params = {
        "enable_diarization": has_diarization,
        "min_speakers": min_speakers,
        "max_speakers": max_speakers,
        "word_timestamps": word_timestamps,
    }
    log("[JOB] Submitting...")
    res = requests.post(SUBMIT_MODAL_URL,
                        json={"download_url": download_url, "params": params},
                        headers={"textops-api-key": API_KEY})
    res.raise_for_status()
    job_id = res.json()["textopsJobId"]
    log(f"[JOB] ID: {job_id}")
    log(f"[JOB] Tip: if interrupted, resume with --job-id {job_id}")
    return job_id


def poll_job(job_id, initial_wait, poll_interval=POLL_INTERVAL, max_polls=MAX_POLLS):
    if initial_wait is not None:
        log(f"[WAIT] First check in {initial_wait:.0f}s (estimated processing time)")
        time.sleep(initial_wait)
    else:
        log("[WAIT] Duration unknown — first check in 10s")
        time.sleep(10)

    last_progress = -1
    for attempt in range(1, max_polls + 1):
        res = requests.post(CHECK_JOB_URL,
                            json={"textopsJobId": job_id},
                            headers={"textops-api-key": API_KEY})
        res.raise_for_status()
        data = res.json()

        status   = data.get("status", "?")
        progress = data.get("progress", 0)

        if data.get("has_error"):
            log(f"ERROR: Processing failed: {data.get('user_messages') or status}")
            sys.exit(1)

        has_segments = bool(data.get("result", {}).get("segments"))
        if status == "done" or has_segments:
            log(f"[DONE] Processing complete ({elapsed()}s total)")
            return data

        # print progress only when it changes (avoid log spam)
        if progress != last_progress:
            log(f"[PROGRESS] {progress}% ({elapsed()}s elapsed)")
            last_progress = progress

        time.sleep(poll_interval)

    log(f"WARNING: Timeout after {elapsed()}s — job may still be running")
    log(f"WARNING: Resume with: python transcribe.py --job-id {job_id} ...")
    sys.exit(1)


def extract_segments(data):
    """
    API response structure can vary:
      - data["result"]["segments"]      (most common)
      - data["result"]["result"]["segments"]  (nested)
    Returns segments list and prints the actual structure if not found.
    """
    result = data.get("result", {})

    # try flat structure first
    segments = result.get("segments")
    if segments is not None:
        return segments

    # try nested structure
    inner = result.get("result", {})
    segments = inner.get("segments")
    if segments is not None:
        return segments

    # not found — print actual structure to help debug
    log("\nWARNING: No segments found in response. Actual response structure:")
    log(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
    log("\n  Tip: check the key that contains the text and open an issue with this structure")
    return []


# ── output writers ────────────────────────────────────────────────────────────

def write_json(data, output_path):
    result = data.get("result", data)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(output_path)
    if size < 10:
        log(f"WARNING: Empty JSON file ({size} bytes) — API response contained no content")
    return size


# ── output writer (shared by full-poll and --check-once paths) ────────────────

def save_output(data, output_path, has_diarize, output_format):
    import subprocess
    json_path = os.path.splitext(output_path)[0] + ".json"
    os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
    size = write_json(data, json_path)
    log(f"[FILE] JSON: {json_path} ({size:,} bytes)")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.splitext(output_path)[0] + ".txt"
    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, "json_to_text.py"),
         json_path, "--output", txt_path,
         "--diarization", "true" if has_diarize else "false"],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        log(f"WARNING: {result.stderr.strip()}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TextOps transcription")
    parser.add_argument("--file", default=None, help="Local file path or URL")
    parser.add_argument("--job-id", default=None,
                        help="Resume from existing Job ID (skip upload/submit)")
    parser.add_argument("--diarization", default="auto",
                        help="Enable speaker separation: true / false / auto (default: auto — server detects)")
    parser.add_argument("--min-speakers", type=int, default=1,
                        help="Minimum number of speakers (used with diarization)")
    parser.add_argument("--max-speakers", type=int, default=10,
                        help="Maximum number of speakers (used with diarization)")
    parser.add_argument("--word-timestamps", default="false",
                        help="Word-level timestamps (slower): true/false")
    parser.add_argument("--output-format", default="json",
                        choices=["json", "text"], help="Output format")
    parser.add_argument("--output-path", default=None,
                        help="Where to save the result (optional)")
    parser.add_argument("--submit-only", action="store_true",
                        help="Upload and submit, print Job ID + timing hints, exit immediately (no polling)")
    parser.add_argument("--check-once", action="store_true",
                        help="With --job-id: poll once. Exit 0=done (files saved), 3=still processing, 1=error")
    args = parser.parse_args()

    if not API_KEY:
        log("ERROR: Missing TEXTOPS_API_KEY — set the environment variable and try again.")
        log("  Get your API key at: https://text-ops-subs.com/api/keys")
        log("  Windows: set TEXTOPS_API_KEY=your_key")
        log("  Mac/Linux: export TEXTOPS_API_KEY=your_key")
        sys.exit(1)

    if not args.file and not args.job_id:
        log("ERROR: Required: --file or --job-id")
        sys.exit(1)

    global _start_time
    _start_time = time.time()

    _diar = args.diarization.lower()
    if _diar in ("true", "1", "yes"):
        has_diarize = True
    elif _diar in ("false", "0", "no"):
        has_diarize = False
    else:
        has_diarize = None   # auto — sends null to API → server auto-detects speakers
    has_word_ts      = args.word_timestamps.lower() in ("true", "1", "yes")
    min_speakers     = args.min_speakers
    max_speakers     = args.max_speakers
    output_format = args.output_format

    # ── determine output path ─────────────────────────────────────────────────
    if args.output_path:
        output_path = args.output_path
    elif args.job_id:
        ext = ".json" if output_format == "json" else ".txt"
        output_path = os.path.join(os.getcwd(), f"{args.job_id}_transcript{ext}")
    elif args.file.startswith("http://") or args.file.startswith("https://"):
        # output_path for URLs is finalized after probe (filename may come from there)
        output_path = None
    else:
        base = os.path.splitext(args.file)[0]
        ext  = ".json" if output_format == "json" else ".txt"
        output_path = base + "_transcript" + ext

    # ── resume / check-once from existing job ID ─────────────────────────────
    if args.job_id:
        if args.check_once:
            # Single poll — no sleep, exit immediately with status code
            res = requests.post(CHECK_JOB_URL,
                                json={"textopsJobId": args.job_id},
                                headers={"textops-api-key": API_KEY})
            res.raise_for_status()
            data = res.json()
            if data.get("has_error"):
                log(f"ERROR: Processing failed: {data.get('user_messages') or data.get('status', '?')}")
                sys.exit(1)
            has_segments = bool(data.get("result", {}).get("segments"))
            if data.get("status") == "done" or has_segments:
                log(f"[DONE] Processing complete ({elapsed()}s total)")
                if has_diarize is None:
                    _speakers = set(s.get("speaker", "") for s in extract_segments(data) if s.get("speaker"))
                    has_diarize = len(_speakers) > 1
                save_output(data, output_path, has_diarize, output_format)
                sys.exit(0)
            progress = data.get("progress", 0)
            log(f"[STATUS] processing {progress}%")
            sys.exit(3)

        log(f"[JOB] Resuming with existing Job ID: {args.job_id}")
        data = poll_job(args.job_id, initial_wait=None)
        if has_diarize is None:
            _speakers = set(s.get("speaker", "") for s in extract_segments(data) if s.get("speaker"))
            has_diarize = len(_speakers) > 1
    else:
        file_arg = args.file
        is_url   = file_arg.startswith("http://") or file_arg.startswith("https://")

        if is_url:
            log(f"[PROBE] Checking URL: {file_arg}")
            probe = probe_url(file_arg)
            if not probe.get("accessible"):
                log(f"ERROR: URL is not publicly accessible: {probe.get('error') or 'unknown error'}")
                log("  If this is a Google Drive link, set sharing to 'Anyone with the link'.")
                sys.exit(1)
            if not probe.get("transcribable"):
                log("ERROR: File format is not supported for transcription.")
                log("  Supported formats: mp3/mp4/wav/m4a/ogg/flac/aac/wma/opus/webm/mkv/avi/mov/wmv/3gp/ts")
                sys.exit(1)

            probe_filename = probe.get("filename") or "transcript"
            source_type    = probe.get("source_type", "direct")
            duration_sec   = probe.get("duration_seconds")
            size_bytes     = probe.get("size_bytes")

            size_str = f", {int(size_bytes) / (1024*1024):.1f} MB" if size_bytes else ""
            dur_str  = f", {duration_sec:.0f}s ({duration_sec/60:.1f} min)" if duration_sec else ", duration unknown"
            log(f"[PROBE] OK | source: {source_type} | file: {probe_filename}{size_str}{dur_str}")

            # finalize output_path now that we have the filename
            if not output_path:
                base = os.path.splitext(os.path.basename(probe_filename))[0]
                ext  = ".json" if output_format == "json" else ".txt"
                output_path = os.path.join(os.getcwd(), base + "_transcript" + ext)

            download_url = file_arg
            file_size_mb = int(size_bytes) / (1024 * 1024) if size_bytes else 0
        else:
            filename     = os.path.basename(file_arg)
            file_size_mb = os.path.getsize(file_arg) / (1024 * 1024)
            if file_size_mb > MAX_FILE_MB:
                log(f"ERROR: File is too large ({file_size_mb:.0f} MB). Maximum allowed size is {MAX_FILE_MB} MB (2 GB).")
                log("  Convert to a smaller format first, e.g.:")
                log("    ffmpeg -i input.mp4 -vn -ar 44100 -ac 2 -b:a 128k output.mp3")
                sys.exit(1)
            duration_sec = get_duration_seconds(file_arg)
            urls         = get_signed_urls(filename)
            upload_file(urls["upload_url"], file_arg, filename)
            download_url = urls["download_url"]

        initial_wait = calc_initial_wait(duration_sec, has_diarize)

        poll_interval = POLL_INTERVAL
        max_polls     = MAX_POLLS

        job_id = submit_job(download_url, has_diarize, has_word_ts, min_speakers, max_speakers)

        if args.submit_only:
            base_path = os.path.splitext(output_path)[0] if output_path else os.path.join(os.getcwd(), job_id + "_transcript")
            log(f"[OUTPUT] {base_path}")
            first_check  = int(initial_wait) if initial_wait else 10
            est_total    = int(initial_wait / 0.8) if initial_wait else "unknown"
            log(f"[TIMING] first_check={first_check}s poll_interval={poll_interval}s estimated_total={est_total}s")
            sys.exit(0)

        data   = poll_job(job_id, initial_wait, poll_interval, max_polls)
        if has_diarize is None:
            _speakers = set(s.get("speaker", "") for s in extract_segments(data) if s.get("speaker"))
            has_diarize = len(_speakers) > 1

    save_output(data, output_path, has_diarize, output_format)


if __name__ == "__main__":
    main()
