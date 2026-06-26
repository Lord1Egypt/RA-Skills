#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


IDLE_UPDATE_SECONDS = 300
FORWARD_STATE_ENV = "YOUTUBE_BATCH_FORWARD_STATE"
LAUNCH_SESSION_KEY_ENV = "YOUTUBE_LAUNCH_SESSION_KEY"


def emit_event(event: str, **payload: Any) -> None:
    record = {"event": event, **payload}
    print(json.dumps(record, ensure_ascii=False), file=sys.stderr)
    sys.stderr.flush()


def get_launch_session_key() -> str | None:
    preferred = os.environ.get(LAUNCH_SESSION_KEY_ENV, "").strip()
    if preferred:
        return preferred
    for key in ("OPENCLAW_SESSION_KEY", "SESSION_KEY", "OPENCLAW_PARENT_SESSION_KEY"):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return None


def load_forward_state(state_path: Path) -> dict[str, str]:
    if not state_path.exists():
        return {}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def save_forward_state(state_path: Path, state: dict[str, str]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def build_forward_message(event: str, payload: dict[str, Any]) -> str | None:
    if event == "video_started":
        title = payload.get("title") or payload.get("url") or "video"
        index = payload.get("index")
        total = payload.get("total")
        prefix = f"[{index}/{total}] " if index and total else ""
        return f"{prefix}Started: {title}"
    if event == "video_summary_done":
        title = payload.get("title") or payload.get("url") or "video"
        return f"Summary ready: {title}"
    if event == "batch_complete":
        success_count = payload.get("success_count")
        total = payload.get("total")
        failure_count = payload.get("failure_count")
        return f"Batch complete: {success_count}/{total} succeeded, {failure_count} failed"
    if event == "video_failed":
        title = payload.get("title") or payload.get("url") or "video"
        phase = payload.get("phase") or "unknown phase"
        error = str(payload.get("error") or "unknown error").strip()
        if len(error) > 220:
            error = error[:217] + "..."
        return f"Failed: {title} ({phase})\n{error}"
    return None


def forward_progress_update(event: str, **payload: Any) -> None:
    session_key = payload.get("sessionKey") or get_launch_session_key()
    message = build_forward_message(event, payload)
    if not session_key or not message:
        return

    state_file_raw = os.environ.get(FORWARD_STATE_ENV, "").strip()
    state_path = Path(state_file_raw) if state_file_raw else Path.home() / ".openclaw" / "tmp" / "youtube-anycaption-forward-state.json"
    state = load_forward_state(state_path)
    dedupe_key = str(payload.get("job_id") or payload.get("url") or payload.get("video_id") or "batch")
    fingerprint = hashlib.sha256(f"{event}\n{dedupe_key}\n{message}".encode("utf-8")).hexdigest()
    if state.get(dedupe_key) == fingerprint:
        return

    cmd = [
        "openclaw",
        "agent",
        "--session-id",
        session_key,
        "--message",
        message,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        return

    state[dedupe_key] = fingerprint
    try:
        save_forward_state(state_path, state)
    except OSError:
        pass


# Per-video timeout for the entire single-video workflow subprocess (seconds)
DEFAULT_VIDEO_TIMEOUT = 900  # 15 minutes
# Timeout for LLM summary generation per video (seconds)
DEFAULT_LLM_TIMEOUT = 300  # 5 minutes

PLACEHOLDER_MARKER = "Placeholder created by workflow script"
LANGUAGE_RE = re.compile(r"## Language\s*\n([^\n]+)")


def collect_urls(url: str | None, batch_file: str | None) -> list[str]:
    urls: list[str] = []
    if url:
        urls.append(url)
    if batch_file:
        for line in Path(batch_file).read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            urls.append(stripped)
    return urls


def run_command_with_updates(cmd: list[str], *, timeout: int, idle_label: str) -> subprocess.CompletedProcess[str]:
    start = time.time()
    last_update = start
    proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = "", ""
    try:
        while True:
            try:
                out, err = proc.communicate(timeout=5)
                stdout += out or ""
                stderr += err or ""
                break
            except subprocess.TimeoutExpired:
                now = time.time()
                if now - start > timeout:
                    proc.kill()
                    out, err = proc.communicate()
                    stdout += out or ""
                    stderr += err or ""
                    raise RuntimeError(f"Command timed out after {timeout}s: {' '.join(cmd)}")
                if now - last_update >= IDLE_UPDATE_SECONDS:
                    elapsed = int(now - start)
                    print(f"  ⏳ Still running: {idle_label} ({elapsed}s elapsed)", file=sys.stderr)
                    emit_event("heartbeat", label=idle_label, elapsed_seconds=elapsed)
                    last_update = now
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate()
    return subprocess.CompletedProcess(cmd, proc.returncode or 0, stdout, stderr)


def run_json(cmd: list[str], timeout: int = DEFAULT_VIDEO_TIMEOUT, idle_label: str = "working") -> dict[str, Any]:
    result = run_command_with_updates(cmd, timeout=timeout, idle_label=idle_label)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"Command failed: {' '.join(cmd)}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Command did not return JSON: {' '.join(cmd)}\n{result.stdout}") from exc


def run_workflow(url: str, args) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(Path(__file__).with_name("run_youtube_workflow.py")),
        url,
        "--parent", args.parent,
        "--model", args.model,
        "--models-dir", args.models_dir,
        "--language", args.language,
        "--summary-language", args.summary_language,
        "--retries", str(args.retries),
        "--retry-backoff", str(args.retry_backoff),
    ]
    if args.full_video:
        cmd.append("--full-video")
    if args.keep_intermediates:
        cmd.append("--keep-intermediates")
    if args.no_subtitle_first:
        cmd.append("--no-subtitle-first")
    if args.cookies:
        cmd.extend(["--cookies", args.cookies])
    if args.cookies_from_browser:
        cmd.extend(["--cookies-from-browser", args.cookies_from_browser])
    result = run_json(cmd, timeout=args.video_timeout, idle_label=f"extracting transcript for {url}")
    # Strip agent-instruction fields — batch handles summary generation directly
    for key in ("summary_prompt", "completion_command", "session_report_command",
                "finalize_command", "normalize_command", "language_backfill_command"):
        result.pop(key, None)
    return result


def detect_language_from_raw(raw_path: Path) -> str:
    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    match = LANGUAGE_RE.search(text)
    if not match:
        return "unknown"
    return match.group(1).strip() or "unknown"


def synthesize_summary(raw_path: Path, summary_path: Path, workflow_result: dict[str, Any], args) -> None:
    """Generate a real LLM-powered summary by calling generate_summary_llm.py."""
    language = detect_language_from_raw(raw_path)
    cmd = [
        sys.executable,
        str(Path(__file__).with_name("generate_summary_llm.py")),
        str(raw_path),
        str(summary_path),
    ]
    env = os.environ.copy()
    session_key = get_launch_session_key()
    if session_key:
        env[LAUNCH_SESSION_KEY_ENV] = session_key
    if language and language != "unknown":
        cmd.extend(["--language", language])
    if args.llm_model:
        cmd.extend(["--model", args.llm_model])

    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        timeout=DEFAULT_LLM_TIMEOUT,
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(f"LLM summary generation failed: {result.stderr.strip() or result.stdout.strip()}")

    # Verify the summary was actually written and is not empty/placeholder
    if not summary_path.exists() or summary_path.stat().st_size < 200:
        raise RuntimeError("LLM summary generation produced empty or missing output")

    # Log the method used (LLM vs fallback)
    if result.stdout.strip():
        try:
            status = json.loads(result.stdout.strip().splitlines()[-1])
            method = status.get("method", "unknown")
            print(f"  Summary generated via: {method}", file=sys.stderr)
        except (json.JSONDecodeError, IndexError):
            pass


def complete_item(raw_path: Path, summary_path: Path, language: str | None) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(Path(__file__).with_name("complete_youtube_summary.py")),
        str(raw_path),
        str(summary_path),
        "--summary-start-epoch",
        str(time.time()),
    ]
    if language and language != "unknown":
        cmd.extend(["--language", language])
    return run_json(cmd, timeout=120, idle_label=f"finalizing {summary_path.name}")  # completion step should be fast


def process_video(url: str, index: int, total: int, args) -> dict[str, Any]:
    last_error = None
    last_phase = None
    video_id = None
    print(f"\n[{index}/{total}] Processing: {url}", file=sys.stderr)
    for attempt in range(1, args.max_attempts + 1):
        attempt_phase = None
        try:
            if attempt > 1:
                print(f"  Retry attempt {attempt}/{args.max_attempts}", file=sys.stderr)
            workflow_result = run_workflow(url, args)
            video_id = workflow_result.get("video_id")
            title = workflow_result.get("title", "unknown")
            session_key = get_launch_session_key()
            emit_event("video_started", index=index, total=total, url=url, video_id=video_id, title=title, sessionKey=session_key)
            forward_progress_update("video_started", index=index, total=total, url=url, video_id=video_id, title=title, sessionKey=session_key)
            print(f"  Title: {title}", file=sys.stderr)
            print(f"  Transcript extracted via: {workflow_result.get('source_method', 'unknown')}", file=sys.stderr)
            raw_path = Path(workflow_result["raw_transcript"])
            summary_path = Path(workflow_result["summary"])
            attempt_phase = "summary_generation"
            print(f"  Generating LLM summary...", file=sys.stderr)
            synthesize_summary(raw_path, summary_path, workflow_result, args)
            attempt_phase = "completion"
            language = detect_language_from_raw(raw_path)
            print(f"  ✅ Summary generated successfully: {summary_path.name}", file=sys.stderr)
            emit_event(
                "video_summary_done",
                index=index,
                total=total,
                url=url,
                video_id=video_id,
                title=title,
                summary_path=str(summary_path),
                transcript_source=workflow_result.get("source_method", "unknown"),
                sessionKey=session_key,
            )
            forward_progress_update(
                "video_summary_done",
                index=index,
                total=total,
                url=url,
                video_id=video_id,
                title=title,
                summary_path=str(summary_path),
                transcript_source=workflow_result.get("source_method", "unknown"),
                sessionKey=session_key,
            )
            final_report = complete_item(raw_path, summary_path, language if language != "unknown" else None)
            final_report["attempts"] = attempt
            final_report["url"] = url
            print(f"  ✅ Complete ({final_report.get('end_to_end_total_seconds', '?')}s)", file=sys.stderr)
            return {"ok": True, "report": final_report}
        except Exception as exc:
            last_error = str(exc)
            last_phase = attempt_phase if attempt_phase else "extraction"
            print(f"  ⚠️ Failed at {last_phase}: {last_error[:120]}", file=sys.stderr)
            if attempt < args.max_attempts:
                time.sleep(3.0 * attempt)  # backoff between retries
            continue
    print(f"  ❌ Failed after {args.max_attempts} attempts", file=sys.stderr)
    failure = {
        "url": url,
        "video_id": video_id,
        "attempts": args.max_attempts,
        "phase": last_phase,
        "error": last_error or "Unknown error",
        "sessionKey": get_launch_session_key(),
    }
    emit_event("video_failed", **failure)
    forward_progress_update("video_failed", **failure)
    return {
        "ok": False,
        "failure": failure,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run YouTube batch workflow end-to-end with retry and final summary generation")
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument("--batch-file", help="Plain text file with one YouTube URL per line")
    parser.add_argument("--parent", default=str(Path.home() / "Downloads"))
    parser.add_argument("--model", default="ggml-medium")
    parser.add_argument("--models-dir", default=str(Path.home() / ".openclaw" / "workspace"))
    parser.add_argument("--language", default="auto")
    parser.add_argument("--summary-language", default="source")
    parser.add_argument("--full-video", action="store_true")
    parser.add_argument("--keep-intermediates", action="store_true")
    parser.add_argument("--cookies")
    parser.add_argument("--cookies-from-browser")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-backoff", type=float, default=3.0)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--no-subtitle-first", action="store_true")
    parser.add_argument("--video-timeout", type=int, default=DEFAULT_VIDEO_TIMEOUT,
                        help="Per-video timeout in seconds for the entire workflow subprocess (default: 900)")
    parser.add_argument("--llm-model", default="openai-codex/gpt-5.4",
                        help="LLM model for summary generation via OpenClaw gateway (default: openai-codex/gpt-5.4)")
    args = parser.parse_args()

    urls = collect_urls(args.url, args.batch_file)
    if not urls:
        parser.error("Provide a URL or --batch-file")

    print(f"Batch: {len(urls)} video(s) to process", file=sys.stderr)

    pending = list(urls)
    success_reports: list[dict[str, Any]] = []
    failures_map: dict[str, dict[str, Any]] = {}

    for idx, url in enumerate(pending, 1):
        result = process_video(url, idx, len(pending), args)
        if result["ok"]:
            report = result["report"]
            success_reports.append({
                "title": report.get("title"),
                "video_id": report.get("video_id"),
                "raw_transcript": report.get("raw_transcript"),
                "summary": report.get("summary"),
                "summary_language": report.get("summary_language"),
                "transcript_source": report.get("transcript_source"),
                "postprocess_complete": report.get("postprocess_complete"),
                "end_to_end_total_seconds": report.get("end_to_end_total_seconds"),
                "attempts": report.get("attempts"),
                "session_report": report.get("session_report"),
                "url": report.get("url"),
            })
        else:
            failure = result["failure"]
            failures_map[url] = failure

    print(f"\nBatch complete: {len(success_reports)}/{len(urls)} succeeded, {len(failures_map)} failed", file=sys.stderr)
    batch_payload = {
        "success_count": len(success_reports),
        "total": len(urls),
        "failure_count": len(failures_map),
        "sessionKey": get_launch_session_key(),
    }
    emit_event("batch_complete", **batch_payload)
    forward_progress_update("batch_complete", **batch_payload)

    final = {
        "queue_mode": len(urls) > 1,
        "count": len(urls),
        "success_count": len(success_reports),
        "failure_count": len(failures_map),
        "results": success_reports,
        "failures": list(failures_map.values()),
    }
    print(json.dumps(final, ensure_ascii=False, indent=2))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
