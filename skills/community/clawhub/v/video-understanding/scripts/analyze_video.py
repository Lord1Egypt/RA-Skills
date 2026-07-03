# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai>=1.0.0"]
# ///
"""Download a video and analyze it with Google Gemini."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

from google import genai
from google.genai import types

YOUTUBE_PATTERNS = [
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=",
    r"(?:https?://)?youtu\.be/",
    r"(?:https?://)?(?:www\.)?youtube\.com/shorts/",
]

DEFAULT_PROMPT = """Analyze this video and return a JSON object with the following fields:

1. "transcript": Full verbatim transcript of all spoken words, with timestamps in [MM:SS] format at natural paragraph breaks.
2. "description": Detailed description of the video including: what is shown visually, who appears on screen (describe them if unnamed), the setting/environment, any text/UI/graphics shown on screen, and the overall flow from start to finish.
3. "summary": A concise 2-3 sentence summary of what the video is about.
4. "duration_seconds": Estimated duration in seconds.
5. "speakers": List of speakers identified (by name if mentioned, otherwise descriptive labels like "male presenter").

Return ONLY valid JSON, no markdown fences."""

QUESTION_ADDENDUM = """

Additionally, answer the following question about the video:

6. "answer": {question}

Return ONLY valid JSON, no markdown fences."""

CACHE_SCHEMA_VERSION = 1
DEFAULT_CACHE_DIR = "~/.openclaw/cache/video-understanding"
CONVERSATION_CONTEXT_LIMIT = 6000


def is_youtube_url(url: str) -> bool:
    return any(re.search(p, url) for p in YOUTUBE_PATTERNS)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def state_name(value) -> str:
    if value is None:
        return ""
    name = getattr(value, "name", None)
    if name:
        return str(name).upper()
    return str(value).split(".")[-1].upper()


def is_active_file(gemini_file: types.File) -> bool:
    return state_name(getattr(gemini_file, "state", None)) == "ACTIVE"


def model_for_cache(model: str) -> str:
    return model if model.startswith("models/") else f"models/{model}"


def default_cache_dir() -> str:
    return os.path.abspath(os.path.expanduser(DEFAULT_CACHE_DIR))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def cache_hash(*parts: str | None) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update((part or "").encode("utf-8", errors="replace"))
        h.update(b"\0")
    return h.hexdigest()


def local_asset_id(file_path: str) -> str:
    stat = os.stat(file_path)
    return f"local:{os.path.abspath(file_path)}:{stat.st_size}:{stat.st_mtime_ns}"


def url_asset_id(url: str, kind: str) -> str:
    return f"{kind}:{url.strip()}"


def cache_record_path(cache_dir: str, session_key: str | None, asset_kind: str, asset_id: str) -> str:
    ensure_dir(cache_dir)
    digest = cache_hash(session_key or "global", asset_kind, asset_id)
    return os.path.join(cache_dir, f"{digest}.json")


def load_cache_record(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_cache_record(path: str, record: dict) -> None:
    ensure_dir(os.path.dirname(path))
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp_path, path)


def file_metadata(gemini_file: types.File) -> dict:
    return {
        "name": getattr(gemini_file, "name", None),
        "uri": getattr(gemini_file, "uri", None),
        "mime_type": getattr(gemini_file, "mime_type", None),
        "state": state_name(getattr(gemini_file, "state", None)),
        "expiration_time": isoformat(getattr(gemini_file, "expiration_time", None)),
        "uploaded_at": utc_now().isoformat(),
    }


def cache_metadata(cache) -> dict:
    return {
        "name": getattr(cache, "name", None),
        "model": getattr(cache, "model", None),
        "expire_time": isoformat(getattr(cache, "expire_time", None)),
        "created_at": utc_now().isoformat(),
        "cached_content_token_count": getattr(cache, "usage_metadata", None)
        and getattr(getattr(cache, "usage_metadata", None), "total_token_count", None),
    }


def expiration_is_valid(value: str | None, skew_seconds: int = 60) -> bool:
    expires = parse_time(value)
    if not expires:
        return True
    return expires.timestamp() - utc_now().timestamp() > skew_seconds


def append_turn(record: dict, question: str | None, output: str) -> None:
    turns = record.setdefault("turns", [])
    turns.append(
        {
            "at": utc_now().isoformat(),
            "question": question,
            "output": output[:CONVERSATION_CONTEXT_LIMIT],
        }
    )
    del turns[:-5]


def prior_conversation_context(record: dict) -> str | None:
    turns = record.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    snippets = []
    for turn in turns[-3:]:
        if not isinstance(turn, dict):
            continue
        question = turn.get("question") or "(initial analysis)"
        output = turn.get("output") or ""
        snippets.append(f"Question: {question}\nPrior output: {output}")
    context = "\n\n".join(snippets).strip()
    if not context:
        return None
    return context[-CONVERSATION_CONTEXT_LIMIT:]


def local_video_path(input_path: str) -> str | None:
    """Return a readable local path for file inputs, including file:// URLs."""
    if input_path.startswith("file://"):
        input_path = input_path.removeprefix("file://")
    expanded = os.path.abspath(os.path.expanduser(input_path))
    if os.path.isfile(expanded):
        return expanded
    return None


def download_video(url: str, output_path: str, max_size_mb: int = 500) -> str:
    """Download video using yt-dlp. Returns the actual output file path."""
    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "--remux-video", "mp4",
        "--no-playlist",
        "--max-filesize", f"{max_size_mb}M",
        "-o", output_path,
        url,
    ]
    print(f"Downloading: {url}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"yt-dlp stderr: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"yt-dlp failed (exit {result.returncode}): {result.stderr[:500]}")

    if not os.path.exists(output_path):
        base_dir = os.path.dirname(output_path)
        base_name = os.path.basename(output_path).replace(".%(ext)s", "")
        for f in os.listdir(base_dir):
            if f.startswith(base_name) and f.endswith(".mp4"):
                return os.path.join(base_dir, f)
        for f in os.listdir(base_dir):
            if f.endswith(".mp4"):
                return os.path.join(base_dir, f)
        raise RuntimeError(f"Downloaded file not found in {base_dir}")

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Downloaded: {size_mb:.1f} MB", file=sys.stderr)
    return output_path


def upload_to_gemini(client: genai.Client, file_path: str) -> types.File:
    """Upload file to Gemini and wait for processing."""
    print("Uploading to Gemini...", file=sys.stderr)
    uploaded = client.files.upload(file=file_path)
    print(f"Uploaded: {uploaded.name} (state: {uploaded.state})", file=sys.stderr)

    while uploaded.state == "PROCESSING":
        time.sleep(3)
        uploaded = client.files.get(name=uploaded.name)
        print(f"  Processing... (state: {uploaded.state})", file=sys.stderr)

    if uploaded.state == "FAILED":
        raise RuntimeError(f"Gemini processing failed for {uploaded.name}")

    print(f"Ready: {uploaded.name}", file=sys.stderr)
    return uploaded


def build_prompt(question: str | None = None, prior_context: str | None = None) -> str:
    """Build the analysis prompt, optionally with a custom question."""
    prompt = DEFAULT_PROMPT
    if prior_context:
        prompt += f"""

Conversation context from earlier turns about the same video:

{prior_context}

Use this prior context only for continuity with follow-up wording. Re-check the video itself when answering.
"""
    if question:
        prompt += QUESTION_ADDENDUM.format(question=question)
    return prompt


def is_transient_model_error(exc: Exception) -> bool:
    """Return whether a Gemini error is worth retrying or falling back from."""
    message = str(exc).lower()
    return any(
        marker in message
        for marker in [
            "503",
            "unavailable",
            "high demand",
            "temporarily",
            "rate limit",
            "resource exhausted",
        ]
    )


def generate_content_with_retry(
    client: genai.Client,
    contents,
    model: str,
    fallback_model: str | None = None,
    attempts: int = 3,
    cached_content: str | None = None,
) -> str:
    """Generate content, retrying transient model failures before optional fallback."""
    models_to_try = [model]
    # CachedContent is model-specific, so do not send a fallback model with a cache
    # created for the primary model.
    if cached_content:
        fallback_model = None
    if fallback_model and fallback_model != model:
        models_to_try.append(fallback_model)

    last_error: Exception | None = None
    for model_name in models_to_try:
        for attempt in range(1, attempts + 1):
            try:
                if model_name == model:
                    print(f"Analyzing with {model_name}...", file=sys.stderr)
                else:
                    print(f"Retrying with fallback model {model_name}...", file=sys.stderr)
                config = (
                    types.GenerateContentConfig(cached_content=cached_content)
                    if cached_content
                    else None
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                return response.text
            except Exception as exc:
                last_error = exc
                if not is_transient_model_error(exc) or attempt == attempts:
                    break
                delay = 2**attempt
                print(
                    f"Transient Gemini error on attempt {attempt}/{attempts}; retrying in {delay}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)

    if last_error:
        raise last_error
    raise RuntimeError("Gemini returned no response")


def analyze_with_file(
    client: genai.Client,
    gemini_file: types.File,
    prompt: str,
    model: str,
    fallback_model: str | None,
) -> str:
    """Analyze using an uploaded Gemini file."""
    contents = [
        types.Content(
            parts=[
                types.Part.from_uri(
                    file_uri=gemini_file.uri,
                    mime_type=gemini_file.mime_type,
                ),
                types.Part.from_text(text=prompt),
            ]
        )
    ]
    return generate_content_with_retry(client, contents, model, fallback_model)


def analyze_with_cache(
    client: genai.Client,
    cache_name: str,
    prompt: str,
    model: str,
    fallback_model: str | None,
) -> str:
    """Analyze using Gemini explicit CachedContent."""
    return generate_content_with_retry(
        client,
        prompt,
        model,
        fallback_model,
        cached_content=cache_name,
    )


def analyze_youtube(
    client: genai.Client,
    url: str,
    prompt: str,
    model: str,
    fallback_model: str | None,
) -> str:
    """Analyze a YouTube video directly by URL (no download needed)."""
    print(f"Analyzing YouTube URL directly with {model}...", file=sys.stderr)
    contents = [
        types.Content(
            parts=[
                types.Part.from_uri(file_uri=url, mime_type="video/mp4"),
                types.Part.from_text(text=prompt),
            ]
        )
    ]
    return generate_content_with_retry(client, contents, model, fallback_model)


def validate_cached_file(client: genai.Client, record: dict) -> types.File | None:
    """Return an ACTIVE cached Gemini file when the stored handle is still usable."""
    meta = record.get("gemini_file")
    if not isinstance(meta, dict):
        return None
    name = meta.get("name")
    if not name or not expiration_is_valid(meta.get("expiration_time")):
        return None
    try:
        gemini_file = client.files.get(name=name)
    except Exception as exc:
        print(f"Cached Gemini file is unavailable; will refresh ({exc})", file=sys.stderr)
        return None
    if not is_active_file(gemini_file):
        print(
            f"Cached Gemini file is not ACTIVE ({state_name(getattr(gemini_file, 'state', None))}); will refresh",
            file=sys.stderr,
        )
        return None
    if not getattr(gemini_file, "uri", None) or not getattr(gemini_file, "mime_type", None):
        print("Cached Gemini file is missing uri or mime_type; will refresh", file=sys.stderr)
        return None
    return gemini_file


def validate_cached_content(client: genai.Client, record: dict, model: str) -> str | None:
    """Return a cachedContent name when it still exists and matches the model."""
    meta = record.get("cached_content")
    if not isinstance(meta, dict):
        return None
    name = meta.get("name")
    if not name:
        return None
    expected_model = model_for_cache(model)
    if meta.get("model") and meta.get("model") != expected_model:
        return None
    if not expiration_is_valid(meta.get("expire_time")):
        return None
    try:
        cached = client.caches.get(name=name)
    except Exception as exc:
        print(f"CachedContent is unavailable; will refresh ({exc})", file=sys.stderr)
        return None
    if getattr(cached, "model", None) and getattr(cached, "model", None) != expected_model:
        return None
    if not expiration_is_valid(isoformat(getattr(cached, "expire_time", None))):
        return None
    return getattr(cached, "name", None)


def create_cached_content(
    client: genai.Client,
    gemini_file: types.File,
    model: str,
    ttl_seconds: int,
):
    """Create explicit Gemini CachedContent for repeated questions against a video."""
    print(f"Creating Gemini CachedContent for {ttl_seconds}s...", file=sys.stderr)
    return client.caches.create(
        model=model_for_cache(model),
        config=types.CreateCachedContentConfig(
            contents=[gemini_file],
            ttl=f"{ttl_seconds}s",
            system_instruction=(
                "The cached content is the source video for follow-up analysis. "
                "Answer questions by inspecting the video, not by guessing from prior chat alone."
            ),
        ),
    )


def get_or_create_cached_content(
    client: genai.Client,
    gemini_file: types.File,
    record: dict,
    model: str,
    ttl_seconds: int,
) -> str:
    cached_name = validate_cached_content(client, record, model)
    if cached_name:
        print(f"Reusing Gemini CachedContent: {cached_name}", file=sys.stderr)
        return cached_name
    cached = create_cached_content(client, gemini_file, model, ttl_seconds)
    record["cached_content"] = cache_metadata(cached)
    return getattr(cached, "name")


def analyze_with_optional_context_cache(
    client: genai.Client,
    gemini_file: types.File,
    prompt: str,
    record: dict,
    model: str,
    fallback_model: str | None,
    ttl_seconds: int,
) -> str:
    """Use explicit CachedContent when available, falling back to File API reuse."""
    try:
        cache_name = get_or_create_cached_content(
            client,
            gemini_file,
            record,
            model,
            ttl_seconds,
        )
        return analyze_with_cache(client, cache_name, prompt, model, fallback_model)
    except Exception as exc:
        record.pop("cached_content", None)
        print(
            f"Warning: couldn't use Gemini CachedContent; falling back to File API reuse ({exc})",
            file=sys.stderr,
        )
        return analyze_with_file(client, gemini_file, prompt, model, fallback_model)


def delete_remote_handles(client: genai.Client, record: dict) -> None:
    """Best-effort delete of cachedContent and File API handles in a cache record."""
    cache_meta = record.get("cached_content")
    if isinstance(cache_meta, dict) and cache_meta.get("name"):
        try:
            client.caches.delete(name=cache_meta["name"])
            print(f"Deleted CachedContent: {cache_meta['name']}", file=sys.stderr)
        except Exception as exc:
            print(f"Warning: couldn't delete CachedContent {cache_meta['name']}: {exc}", file=sys.stderr)
    file_meta = record.get("gemini_file")
    if isinstance(file_meta, dict) and file_meta.get("name"):
        try:
            client.files.delete(name=file_meta["name"])
            print(f"Deleted Gemini file: {file_meta['name']}", file=sys.stderr)
        except Exception as exc:
            print(f"Warning: couldn't delete Gemini file {file_meta['name']}: {exc}", file=sys.stderr)


def write_output(output: str, output_path: str | None) -> None:
    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Analysis saved to: {output_path}", file=sys.stderr)
    else:
        print(output)


def update_record_identity(
    record: dict,
    cache_key: str,
    session_key: str | None,
    asset_kind: str,
    asset_id: str,
    source: str,
) -> None:
    record.update(
        {
            "schema": CACHE_SCHEMA_VERSION,
            "cache_key": cache_key,
            "session_key": session_key,
            "asset_kind": asset_kind,
            "asset_id": asset_id,
            "source": source,
            "updated_at": utc_now().isoformat(),
        }
    )


def handle_result(
    output: str,
    raw_result: str,
    output_path: str | None,
    record: dict | None,
    record_path: str | None,
    question: str | None,
) -> None:
    write_output(output, output_path)
    if record is not None and record_path is not None:
        append_turn(record, question, raw_result)
        save_cache_record(record_path, record)


def format_output(raw_text: str) -> str:
    """Try to parse as JSON and pretty-print; fall back to raw text."""
    # Strip markdown fences if present
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    try:
        data = json.loads(cleaned)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return raw_text


def main():
    parser = argparse.ArgumentParser(description="Download and analyze video with Gemini")
    parser.add_argument("url", help="Video URL (Loom, YouTube, etc.)")
    parser.add_argument("--question", "-q", help="Additional question to answer about the video")
    parser.add_argument("--prompt", "-p", help="Override the entire prompt (ignores --question)")
    parser.add_argument("--model", "-m", default="gemini-2.5-flash")
    parser.add_argument(
        "--fallback-model",
        default="",
        help="Optional fallback model for transient Gemini errors",
    )
    parser.add_argument("--output", "-o", help="Save analysis to file (or mp4 with --download-only)")
    parser.add_argument("--keep", action="store_true", help="Keep downloaded video file")
    parser.add_argument("--download-only", action="store_true", help="Only download, skip analysis")
    parser.add_argument("--max-size", type=int, default=500, help="Max video size in MB")
    parser.add_argument("--raw", action="store_true", help="Output raw text instead of JSON")
    parser.add_argument(
        "--reuse-file-cache",
        action="store_true",
        help="Reuse ACTIVE Gemini File API uploads and keep new uploads for follow-up questions",
    )
    parser.add_argument(
        "--use-context-cache",
        action="store_true",
        help="Create/reuse Gemini CachedContent for repeated follow-up questions",
    )
    parser.add_argument(
        "--cache-ttl-seconds",
        type=int,
        default=3600,
        help="TTL for explicit Gemini CachedContent when --use-context-cache is enabled",
    )
    parser.add_argument(
        "--cache-dir",
        default=default_cache_dir(),
        help=f"Directory for local video asset cache records (default: {DEFAULT_CACHE_DIR})",
    )
    parser.add_argument(
        "--session-key",
        help="Conversation/thread key for follow-up reuse, such as a Slack thread timestamp",
    )
    parser.add_argument(
        "--continue-chat",
        action="store_true",
        help="Include prior cached outputs as conversation context for follow-up questions",
    )
    parser.add_argument(
        "--purge-cache",
        action="store_true",
        help="Delete cached Gemini handles for this asset/session and remove the local cache record",
    )
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.download_only:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key) if api_key else None
    local_path = local_video_path(args.url)
    fallback_model = args.fallback_model or None
    cache_dir = os.path.abspath(os.path.expanduser(args.cache_dir))

    if local_path:
        asset_kind = "local_file"
        asset_id = local_asset_id(local_path)
    elif is_youtube_url(args.url):
        asset_kind = "youtube_url"
        asset_id = url_asset_id(args.url, asset_kind)
    else:
        asset_kind = "downloaded_url"
        asset_id = url_asset_id(args.url, asset_kind)

    record_path = cache_record_path(cache_dir, args.session_key, asset_kind, asset_id)
    record = load_cache_record(record_path)
    update_record_identity(
        record,
        os.path.splitext(os.path.basename(record_path))[0],
        args.session_key,
        asset_kind,
        asset_id,
        args.url,
    )

    if args.purge_cache:
        if client:
            delete_remote_handles(client, record)
        if os.path.exists(record_path):
            os.unlink(record_path)
            print(f"Removed cache record: {record_path}", file=sys.stderr)
        return

    should_save_history = bool(
        args.reuse_file_cache or args.use_context_cache or args.continue_chat or args.session_key
    )
    prior_context = prior_conversation_context(record) if args.continue_chat else None

    # Build prompt
    if args.prompt:
        prompt = args.prompt
    else:
        prompt = build_prompt(args.question, prior_context)

    if local_path:
        if args.download_only:
            if args.output and os.path.abspath(os.path.expanduser(args.output)) != local_path:
                shutil.copyfile(local_path, os.path.abspath(os.path.expanduser(args.output)))
                print(f"Video saved to: {args.output}")
            else:
                print(f"Video saved to: {local_path}")
            return

        gemini_file = validate_cached_file(client, record) if args.reuse_file_cache else None
        if gemini_file:
            print(f"Reusing Gemini file: {gemini_file.name}", file=sys.stderr)
        else:
            gemini_file = upload_to_gemini(client, local_path)
            if args.reuse_file_cache or args.use_context_cache:
                record["gemini_file"] = file_metadata(gemini_file)
        try:
            if args.use_context_cache:
                result = analyze_with_optional_context_cache(
                    client,
                    gemini_file,
                    prompt,
                    record,
                    args.model,
                    fallback_model,
                    args.cache_ttl_seconds,
                )
            else:
                result = analyze_with_file(client, gemini_file, prompt, args.model, fallback_model)
            output = result if args.raw else format_output(result)
            handle_result(
                output,
                result,
                args.output,
                record if should_save_history else None,
                record_path if should_save_history else None,
                args.question,
            )
        finally:
            if not (args.reuse_file_cache or args.use_context_cache):
                try:
                    client.files.delete(name=gemini_file.name)
                    print(f"Cleaned up Gemini file: {gemini_file.name}", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: couldn't delete Gemini file: {e}", file=sys.stderr)
        return

    # YouTube shortcut: pass URL directly to Gemini
    if is_youtube_url(args.url) and not args.download_only:
        print("Detected YouTube URL — passing directly to Gemini (no download)", file=sys.stderr)
        if args.use_context_cache:
            print(
                "Warning: explicit CachedContent for direct YouTube URL inputs is not documented; sending URL directly",
                file=sys.stderr,
            )
        result = analyze_youtube(client, args.url, prompt, args.model, fallback_model)
        output = result if args.raw else format_output(result)
        handle_result(
            output,
            result,
            args.output,
            record if should_save_history else None,
            record_path if should_save_history else None,
            args.question,
        )
        return

    cached_file = validate_cached_file(client, record) if args.reuse_file_cache else None
    if cached_file:
        print(f"Reusing Gemini file: {cached_file.name}", file=sys.stderr)
        if args.use_context_cache:
            result = analyze_with_optional_context_cache(
                client,
                cached_file,
                prompt,
                record,
                args.model,
                fallback_model,
                args.cache_ttl_seconds,
            )
        else:
            result = analyze_with_file(client, cached_file, prompt, args.model, fallback_model)
        output = result if args.raw else format_output(result)
        handle_result(
            output,
            result,
            args.output,
            record if should_save_history else None,
            record_path if should_save_history else None,
            args.question,
        )
        return

    # Download for non-YouTube
    if args.download_only and args.output:
        video_path = args.output
    else:
        tmp_dir = tempfile.mkdtemp()
        video_path = os.path.join(tmp_dir, "video.%(ext)s")

    try:
        video_path = download_video(args.url, video_path, args.max_size)

        if args.download_only:
            print(f"Video saved to: {video_path}")
            return

        gemini_file = upload_to_gemini(client, video_path)
        if args.reuse_file_cache or args.use_context_cache:
            record["gemini_file"] = file_metadata(gemini_file)

        try:
            if args.use_context_cache:
                result = analyze_with_optional_context_cache(
                    client,
                    gemini_file,
                    prompt,
                    record,
                    args.model,
                    fallback_model,
                    args.cache_ttl_seconds,
                )
            else:
                result = analyze_with_file(client, gemini_file, prompt, args.model, fallback_model)
            output = result if args.raw else format_output(result)
            handle_result(
                output,
                result,
                args.output,
                record if should_save_history else None,
                record_path if should_save_history else None,
                args.question,
            )
        finally:
            if not (args.reuse_file_cache or args.use_context_cache):
                try:
                    client.files.delete(name=gemini_file.name)
                    print(f"Cleaned up Gemini file: {gemini_file.name}", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: couldn't delete Gemini file: {e}", file=sys.stderr)
    finally:
        if not args.keep and not args.download_only and os.path.exists(video_path):
            os.unlink(video_path)
            print("Cleaned up local video file", file=sys.stderr)


if __name__ == "__main__":
    main()
