#!/usr/bin/env python3
"""Submit local audio or a public YouTube video to UUScribe ASR."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

DEFAULT_API_BASE = "https://scribe.uustudio.cc"
MAX_FILE_SIZE = 1_073_741_824
TRANSIENT_STATUSES = {429, 500, 502, 503, 504}
SAFE_RETRY_ATTEMPTS = 5
API_REQUESTS_PER_MINUTE = 55

AUDIO_MIME_TYPES = {
    "aac": "audio/aac",
    "amr": "audio/amr",
    "awb": "audio/amr-wb",
    "flac": "audio/flac",
    "m4a": "audio/mp4",
    "mka": "audio/x-matroska",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "oga": "audio/ogg",
    "ogg": "audio/ogg",
    "opus": "audio/opus",
    "wav": "audio/wav",
    "weba": "audio/webm",
    "wma": "audio/x-ms-wma",
}


class UUScribeError(RuntimeError):
    """User-facing workflow error."""


class ApiError(UUScribeError):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"UUScribe API returned HTTP {status}: {message}")
        self.status = status


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Prevent API credentials from following redirects to another origin."""

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Any,
        new_url: str,
    ) -> None:
        return None


def youtube_video_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return False

    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False

    host = parsed.hostname.lower().rstrip(".")
    path_parts = [part for part in parsed.path.split("/") if part]
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if "list" in query:
        return False

    if host == "youtu.be":
        return len(path_parts) == 1

    youtube_host = (
        host == "youtube.com"
        or host.endswith(".youtube.com")
        or host == "youtube-nocookie.com"
        or host.endswith(".youtube-nocookie.com")
    )
    if not youtube_host:
        return False

    if parsed.path == "/watch":
        return bool(query.get("v", [""])[0])

    return len(path_parts) == 2 and path_parts[0] in {"embed", "live", "shorts"}


def audio_content_type(path: Path) -> str:
    extension = path.suffix.lower().lstrip(".")
    try:
        return AUDIO_MIME_TYPES[extension]
    except KeyError as exc:
        supported = ", ".join(sorted(AUDIO_MIME_TYPES))
        raise UUScribeError(
            f"Unsupported local audio extension '.{extension}'. Supported: {supported}"
        ) from exc


def probe_duration(path: Path) -> int:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise UUScribeError(
            "ffprobe is required for local audio. Install FFmpeg or pass an accurate --duration."
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "ffprobe could not read the file").strip()
        raise UUScribeError(f"Unable to determine audio duration: {detail}") from exc

    try:
        duration = math.ceil(float(result.stdout.strip()))
    except (TypeError, ValueError) as exc:
        raise UUScribeError("ffprobe did not return a valid duration") from exc

    if duration < 1:
        raise UUScribeError("Audio duration must be at least one second")

    return duration


def error_message(body: bytes, fallback: str) -> str:
    try:
        payload = json.loads(body.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return fallback

    if not isinstance(payload, dict):
        return fallback

    message = payload.get("message") or payload.get("error") or fallback
    errors = payload.get("errors")
    if isinstance(errors, dict):
        details = [
            str(item)
            for values in errors.values()
            for item in (values if isinstance(values, list) else [values])
        ]
        if details:
            message = f"{message} ({'; '.join(details)})"

    return str(message)


class UUScribeClient:
    def __init__(
        self,
        api_base: str,
        api_key: str,
        request_timeout: int = 60,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        parsed = urllib.parse.urlparse(api_base)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise UUScribeError("UUSCRIBE_API_BASE must be an HTTP or HTTPS URL")
        if parsed.scheme != "https" and parsed.hostname not in {
            "localhost",
            "127.0.0.1",
            "::1",
        }:
            raise UUScribeError(
                "UUSCRIBE_API_BASE must use HTTPS; HTTP is allowed only for localhost"
            )
        if not api_key.strip():
            raise UUScribeError("UUSCRIBE_API_KEY is required")

        self.api_base = api_base.rstrip("/")
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.sleep = sleep
        self.clock = clock
        self.last_api_request_at: float | None = None
        self.opener = urllib.request.build_opener(NoRedirectHandler())

    def pace_api_request(self) -> None:
        minimum_interval = 60 / API_REQUESTS_PER_MINUTE
        now = self.clock()
        if self.last_api_request_at is not None:
            delay = minimum_interval - (now - self.last_api_request_at)
            if delay > 0:
                self.sleep(delay)
        self.last_api_request_at = self.clock()

    @staticmethod
    def retry_delay(attempt: int, retry_after: str | None = None) -> float:
        if retry_after:
            try:
                return min(max(float(retry_after), 0.0), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    def request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        retry_transient: bool = False,
    ) -> dict[str, Any]:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "uusscribe-asr-skill/1.0",
        }
        if data is not None:
            headers["Content-Type"] = "application/json"

        attempts = SAFE_RETRY_ATTEMPTS if retry_transient else 1
        for attempt in range(attempts):
            request = urllib.request.Request(
                f"{self.api_base}{path}", data=data, headers=headers, method=method
            )
            self.pace_api_request()
            try:
                with self.opener.open(request, timeout=self.request_timeout) as response:
                    body = response.read()
                break
            except urllib.error.HTTPError as exc:
                body = exc.read()
                if (
                    retry_transient
                    and exc.code in TRANSIENT_STATUSES
                    and attempt + 1 < attempts
                ):
                    retry_after = (
                        exc.headers.get("Retry-After") if exc.headers is not None else None
                    )
                    self.sleep(self.retry_delay(attempt, retry_after))
                    continue
                raise ApiError(exc.code, error_message(body, exc.reason)) from exc
            except urllib.error.URLError as exc:
                if retry_transient and attempt + 1 < attempts:
                    self.sleep(self.retry_delay(attempt))
                    continue
                raise UUScribeError(f"Could not reach UUScribe API: {exc.reason}") from exc

        try:
            result = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise UUScribeError("UUScribe API returned invalid JSON") from exc
        if not isinstance(result, dict):
            raise UUScribeError("UUScribe API returned an unexpected response")
        return result

    def put_part(self, url: str, headers: dict[str, str], data: bytes) -> None:
        for attempt in range(SAFE_RETRY_ATTEMPTS):
            request = urllib.request.Request(url, data=data, headers=headers, method="PUT")
            try:
                with self.opener.open(request, timeout=self.request_timeout) as response:
                    response.read()
                return
            except urllib.error.HTTPError as exc:
                if exc.code in TRANSIENT_STATUSES and attempt + 1 < SAFE_RETRY_ATTEMPTS:
                    retry_after = (
                        exc.headers.get("Retry-After") if exc.headers is not None else None
                    )
                    self.sleep(self.retry_delay(attempt, retry_after))
                    continue
                raise ApiError(exc.code, "presigned upload failed") from exc
            except urllib.error.URLError as exc:
                if attempt + 1 < SAFE_RETRY_ATTEMPTS:
                    self.sleep(self.retry_delay(attempt))
                    continue
                raise UUScribeError(f"Could not upload audio part: {exc.reason}") from exc

    def remaining_balance(self) -> int:
        user = self.request_json("GET", "/api/user", retry_transient=True)
        balance = user.get("balance")
        if not isinstance(balance, dict):
            raise UUScribeError("UUScribe API returned invalid balance information")
        remaining = balance.get("remaining_seconds")
        if isinstance(remaining, bool) or not isinstance(remaining, int):
            raise UUScribeError("UUScribe API returned invalid balance information")
        return max(remaining, 0)

    def ensure_balance(self, required_seconds: int) -> None:
        remaining = self.remaining_balance()
        if remaining < required_seconds:
            raise UUScribeError(
                f"Insufficient balance: audio needs {required_seconds} seconds, "
                f"account has {remaining} seconds"
            )

    def create_youtube_task(self, url: str, name: str) -> int:
        if not youtube_video_url(url):
            raise UUScribeError("Only public YouTube single-video URLs are supported")
        task = self.request_json(
            "POST",
            "/api/tasks",
            {
                "disk": "youtube",
                "name": name,
                "path": url,
                "file": url,
            },
        )
        return required_int(task, "id", "task")

    def upload_audio(self, path: Path, name: str, duration: int) -> int:
        if not path.is_file():
            raise UUScribeError(f"Audio file does not exist: {path}")
        size = path.stat().st_size
        if size < 1:
            raise UUScribeError("Audio file is empty")
        if size > MAX_FILE_SIZE:
            raise UUScribeError("Audio file exceeds the 1 GiB upload limit")
        if duration < 1:
            raise UUScribeError("Audio duration must be at least one second")

        content_type = audio_content_type(path)
        upload = self.request_json(
            "POST",
            "/api/uploads/sign",
            {
                "file": path.name,
                "content_type": content_type,
                "size": size,
                "duration": duration,
            },
        )
        upload_path = required_str(upload, "path", "upload")
        upload_id = required_str(upload, "upload_id", "upload")

        try:
            part_size = required_int(upload, "part_size", "upload")
            part_count = required_int(upload, "part_count", "upload")
            if part_size < 1 or part_count != math.ceil(size / part_size):
                raise UUScribeError("UUScribe API returned invalid multipart upload metadata")

            uploaded_size = 0
            with path.open("rb") as handle:
                for part_number in range(1, part_count + 1):
                    part = handle.read(part_size)
                    if not part:
                        raise UUScribeError("Audio file ended before all upload parts were read")
                    uploaded_size += len(part)
                    signed = self.request_json(
                        "POST",
                        "/api/uploads/sign-part",
                        {
                            "path": upload_path,
                            "upload_id": upload_id,
                            "part_number": part_number,
                        },
                        retry_transient=True,
                    )
                    upload_url = required_str(signed, "url", "signed part")
                    raw_headers = signed.get("headers", {})
                    if not isinstance(raw_headers, dict):
                        raise UUScribeError("UUScribe API returned invalid upload headers")
                    self.put_part(
                        upload_url,
                        {str(key): str(value) for key, value in raw_headers.items()},
                        part,
                    )

                if uploaded_size != size or handle.read(1):
                    raise UUScribeError("Audio file changed while it was being uploaded")

        except Exception:
            try:
                self.request_json(
                    "POST",
                    "/api/uploads/abort",
                    {"path": upload_path, "upload_id": upload_id},
                    retry_transient=True,
                )
            except UUScribeError:
                pass
            raise

        # Completion may have created a billable task even if its response is lost.
        completed = self.request_json(
            "POST",
            "/api/uploads/complete",
            {
                "path": upload_path,
                "upload_id": upload_id,
                "original_name": path.name,
                "content_type": content_type,
                "size": size,
                "duration": duration,
                "name": name,
            },
        )
        task = completed.get("task")
        if not isinstance(task, dict):
            raise UUScribeError("UUScribe API did not return the created task")
        return required_int(task, "id", "task")

    def wait_for_task(
        self,
        task_id: int,
        timeout: int,
        poll_interval: float,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        quiet: bool = False,
    ) -> dict[str, Any]:
        deadline = clock() + timeout
        attempt = 0
        previous_status = None
        next_pending_balance_check = 0.0

        while True:
            if clock() >= deadline:
                raise UUScribeError(
                    f"Timed out waiting for task {task_id}; the remote task may still be running"
                )

            try:
                task = self.request_json(
                    "GET", f"/api/tasks/{task_id}", retry_transient=True
                )
            except ApiError as exc:
                if exc.status not in TRANSIENT_STATUSES:
                    raise
                if not quiet:
                    print(f"Temporary polling error: HTTP {exc.status}", file=sys.stderr)
            else:
                status = str(task.get("status", ""))
                if status != previous_status:
                    if not quiet:
                        print(f"Task {task_id}: {status or 'unknown'}", file=sys.stderr)
                    previous_status = status
                if status == "finished":
                    return task
                if status == "failed":
                    raise UUScribeError(f"UUScribe task {task_id} failed")
                duration = task.get("duration")
                if (
                    status == "pending"
                    and isinstance(duration, int)
                    and not isinstance(duration, bool)
                    and duration > 0
                    and clock() >= next_pending_balance_check
                ):
                    remaining = self.remaining_balance()
                    next_pending_balance_check = clock() + 60
                    if remaining < duration:
                        raise UUScribeError(
                            f"Task {task_id} is pending because it needs {duration} "
                            f"balance seconds but the account has {remaining}; "
                            "the remote task remains pending"
                        )

            delay = min(poll_interval * (1.5**attempt), 30.0)
            attempt += 1
            sleep(delay)


def required_str(payload: dict[str, Any], key: str, label: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise UUScribeError(f"UUScribe API returned an invalid {label} {key}")
    return value


def required_int(payload: dict[str, Any], key: str, label: str) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise UUScribeError(f"UUScribe API returned an invalid {label} {key}")
    return value


def transcript_from_segments(segments: Any) -> str:
    if not isinstance(segments, list):
        return ""
    return "\n".join(
        text
        for segment in segments
        if isinstance(segment, dict)
        and isinstance((text := segment.get("text")), str)
        and text.strip()
    )


def result_payload(task: dict[str, Any], task_id: int, api_base: str) -> dict[str, Any]:
    segments = task.get("segments") if isinstance(task.get("segments"), list) else []
    text_segments = [
        segment
        for segment in segments
        if isinstance(segment, dict) and str(segment.get("text", "")).strip()
    ]
    speaker_segments = [
        segment
        for segment in text_segments
        if isinstance(segment.get("speaker"), str)
        and str(segment.get("speaker")).strip()
    ]
    return {
        "task_id": task_id,
        "status": task.get("status"),
        "name": task.get("name"),
        "source_locale": task.get("source_locale"),
        "duration_seconds": task.get("duration"),
        "transcript": transcript_from_segments(segments),
        "segments": segments,
        "timestamps_unit": "milliseconds",
        "speaker_labels_present": bool(speaker_segments),
        "speaker_labeled_segments": len(speaker_segments),
        "text_segments": len(text_segments),
        "summary": task.get("summary"),
        "mindmap": task.get("mindmap"),
        "task_url": f"{api_base.rstrip('/')}/tasks/{task_id}",
    }


def receipt_payload(task_id: int, api_base: str) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "status": "submitted",
        "task_url": f"{api_base.rstrip('/')}/tasks/{task_id}",
    }


def render_result(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "text" and payload.get("status") == "finished":
        return str(payload.get("transcript", ""))
    return json.dumps(payload, ensure_ascii=False, indent=2)


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Transcribe local audio or a public YouTube video with UUScribe"
    )
    cli.add_argument(
        "source", nargs="?", help="Local audio file path or public YouTube video URL"
    )
    cli.add_argument(
        "--task-id", type=int, help="Resume polling an existing UUScribe task"
    )
    cli.add_argument(
        "--submit-only",
        action="store_true",
        help="Submit and print a task receipt without polling",
    )
    cli.add_argument("--name", help="Task name")
    cli.add_argument("--format", choices=("json", "text"), default="json")
    cli.add_argument("--output", type=Path, help="Also write the selected output to this file")
    cli.add_argument("--timeout", type=int, default=7200, help="Polling timeout in seconds")
    cli.add_argument("--poll-interval", type=float, default=5.0)
    cli.add_argument("--duration", type=int, help="Accurate audio duration in seconds")
    cli.add_argument("--quiet", action="store_true", help="Suppress progress on stderr")
    cli.add_argument(
        "--base-url",
        default=os.environ.get("UUSCRIBE_API_BASE", DEFAULT_API_BASE),
        help=argparse.SUPPRESS,
    )
    return cli


def main() -> int:
    args = parser().parse_args()
    if args.timeout < 1 or args.poll_interval <= 0:
        raise UUScribeError("timeout and poll interval must be positive")
    if (args.source is None) == (args.task_id is None):
        raise UUScribeError("Provide exactly one source or --task-id")
    if args.task_id is not None and args.task_id < 1:
        raise UUScribeError("task ID must be a positive integer")
    if args.task_id is not None and args.submit_only:
        raise UUScribeError("--submit-only cannot be combined with --task-id")

    source_kind: str | None = None
    audio_path: Path | None = None
    duration: int | None = None
    if args.source is not None:
        if youtube_video_url(args.source):
            source_kind = "youtube"
        elif urllib.parse.urlparse(args.source).scheme in {"http", "https"}:
            raise UUScribeError("Only public YouTube single-video URLs are supported")
        else:
            source_kind = "audio"
            audio_path = Path(args.source).expanduser().resolve()
            if not audio_path.is_file():
                raise UUScribeError("Audio file does not exist")
            audio_content_type(audio_path)
            duration = (
                args.duration if args.duration is not None else probe_duration(audio_path)
            )
            if duration < 1:
                raise UUScribeError("Audio duration must be at least one second")

    api_key = os.environ.get("UUSCRIBE_API_KEY", "")
    client = UUScribeClient(args.base_url, api_key)

    if args.task_id is not None:
        task_id = args.task_id
    elif source_kind == "youtube" and args.source is not None:
        task_name = args.name or "YouTube transcription"
        task_id = client.create_youtube_task(args.source, task_name)
    elif audio_path is not None and duration is not None:
        client.ensure_balance(duration)
        task_name = args.name or audio_path.stem
        task_id = client.upload_audio(audio_path, task_name, duration)
    else:
        raise UUScribeError("Unable to determine transcription source")

    if args.task_id is None and not args.quiet:
        print(f"Submitted UUScribe task {task_id}", file=sys.stderr)

    if args.submit_only:
        result = receipt_payload(task_id, args.base_url)
    else:
        task = client.wait_for_task(
            task_id, args.timeout, args.poll_interval, quiet=args.quiet
        )
        result = result_payload(task, task_id, args.base_url)
    rendered = render_result(result, args.format)

    if args.output:
        output_path = args.output.expanduser().resolve()
        output_path.write_text(rendered + "\n", encoding="utf-8")
        if not args.quiet:
            print("Wrote transcription result", file=sys.stderr)
    print(rendered)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UUScribeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
