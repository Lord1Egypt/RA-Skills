#!/usr/bin/env python3
"""
UniFuncs Deep Research chat/completions client.
Usage: ./deep-research-report.py "query" [options]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

CHAT_COMPLETIONS_ENDPOINT = "https://api.unifuncs.com/deepresearch/v1/chat/completions"
DEFAULT_MODEL = "u3"
DEFAULT_OUTPUT_TYPE = "report"
DEFAULT_OUTPUT_LENGTH = 10000
DEFAULT_REQUEST_TIMEOUT_SECONDS = 180
DEFAULT_STREAM_TIMEOUT_SECONDS = 1800


class UniFuncsDeepResearchError(Exception):
    """Raised when the UniFuncs Deep Research API call fails."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="UniFuncs Deep Research client")
    parser.add_argument("query", nargs="?", help="User query sent to Deep Research.")
    parser.add_argument(
        "--model",
        choices=["u1", "u1-pro", "u2", "u3"],
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        default=True,
        help="Enable streaming mode (default: True).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_STREAM_TIMEOUT_SECONDS,
        help=f"Max streaming wait time in seconds (default: {DEFAULT_STREAM_TIMEOUT_SECONDS}).",
    )
    parser.add_argument(
        "--stream-file",
        type=str,
        help="Path to persist/read stream chunks. If omitted, temp file is auto-created when writable.",
    )
    parser.add_argument(
        "--read-stream-file",
        action="store_true",
        help="Read and render already received content from --stream-file, without calling API.",
    )
    parser.add_argument("--introduction", type=str, help="Researcher role/tone introduction.")
    parser.add_argument(
        "--plan-approval",
        action="store_true",
        help="Generate research plan and wait for approval before execution.",
    )
    parser.add_argument(
        "--reference-style",
        choices=["link", "character", "hidden"],
        help="Reference marker style.",
    )
    parser.add_argument("--max-depth", type=int, help="Maximum research depth.")
    parser.add_argument("--domain-scope", type=str, help="Comma-separated domain allowlist.")
    parser.add_argument("--domain-blacklist", type=str, help="Comma-separated domain blocklist.")
    parser.add_argument(
        "--output-type",
        choices=[
            "report",
            "summary",
            "wechat-article",
            "xiaohongshu-article",
            "toutiao-article",
            "zhihu-article",
            "zhihu-answer",
            "weibo-article",
        ],
        default=DEFAULT_OUTPUT_TYPE,
        help=f"Desired output style (default: {DEFAULT_OUTPUT_TYPE}).",
    )
    parser.add_argument("--output-prompt", type=str, help="Custom output prompt template.")
    parser.add_argument(
        "--output-length",
        type=int,
        default=DEFAULT_OUTPUT_LENGTH,
        help=f"Expected output length hint (default: {DEFAULT_OUTPUT_LENGTH}).",
    )
    parser.add_argument("--raw-response", action="store_true", help="Print full API response JSON.")
    parser.add_argument("--background-worker", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def get_api_key() -> str:
    """Read API key from UNIFUNCS_API_KEY."""
    api_key = os.environ.get("UNIFUNCS_API_KEY")
    if not api_key:
        print("Error: UNIFUNCS_API_KEY is not set.", file=sys.stderr)
        print("Visit https://unifuncs.com/account to get your API key.", file=sys.stderr)
        sys.exit(1)
    return api_key


def validate_args(args: argparse.Namespace) -> None:
    """Validate argument values."""
    if not args.read_stream_file and not args.background_worker:
        if not args.query or not args.query.strip():
            print("Error: query cannot be empty.", file=sys.stderr)
            sys.exit(1)
    if args.timeout <= 0:
        print("Error: timeout must be greater than 0.", file=sys.stderr)
        sys.exit(1)
    if args.max_depth is not None and args.max_depth <= 0:
        print("Error: max-depth must be greater than 0.", file=sys.stderr)
        sys.exit(1)
    if args.output_length <= 0:
        print("Error: output-length must be greater than 0.", file=sys.stderr)
        sys.exit(1)
    if args.read_stream_file and not args.stream_file:
        print("Error: --read-stream-file requires --stream-file.", file=sys.stderr)
        sys.exit(1)


def split_csv(value: Optional[str]) -> Optional[list[str]]:
    """Split comma-separated input into a trimmed list."""
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or None


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    """Build request payload for chat/completions."""
    payload: Dict[str, Any] = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.query}],
        "output_type": args.output_type,
        "output_length": args.output_length,
        "stream": args.stream,
    }
    if args.introduction:
        payload["introduction"] = args.introduction
    if args.plan_approval:
        payload["plan_approval"] = True
    if args.reference_style:
        payload["reference_style"] = args.reference_style
    if args.max_depth is not None:
        payload["max_depth"] = args.max_depth
    if args.domain_scope:
        payload["domain_scope"] = split_csv(args.domain_scope)
    if args.domain_blacklist:
        payload["domain_blacklist"] = split_csv(args.domain_blacklist)
    if args.output_prompt:
        payload["output_prompt"] = args.output_prompt
    return payload


def post_json(url: str, payload: Dict[str, Any], api_key: str) -> Dict[str, Any] | str:
    """POST JSON payload and parse JSON/text response."""
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        raise UniFuncsDeepResearchError(f"HTTP {err.code}: {error_body}") from err
    except urllib.error.URLError as err:
        raise UniFuncsDeepResearchError(f"Network error: {err.reason}") from err


def create_temp_stream_file() -> Optional[str]:
    """Create a writable temp file path for stream payload, if possible."""
    tmp_dir = tempfile.gettempdir()
    if not os.access(tmp_dir, os.W_OK):
        return None
    fd, path = tempfile.mkstemp(prefix="unifuncs-deep-research-", suffix=".stream", dir=tmp_dir)
    os.close(fd)
    return path


def resolve_stream_file_path(specified_path: Optional[str]) -> Optional[str]:
    """Return stream file path, preferring user-specified path."""
    if specified_path:
        abs_path = os.path.abspath(specified_path)
        parent_dir = os.path.dirname(abs_path) or "."
        if not os.path.isdir(parent_dir):
            raise UniFuncsDeepResearchError(f"Stream file directory does not exist: {parent_dir}")
        if not os.access(parent_dir, os.W_OK):
            raise UniFuncsDeepResearchError(f"Stream file directory is not writable: {parent_dir}")
        if not os.path.exists(abs_path):
            with open(abs_path, "w", encoding="utf-8"):
                pass
        return abs_path
    return create_temp_stream_file()


def extract_stream_text(chunk: Dict[str, Any]) -> str:
    """Extract incremental content text from a stream chunk."""
    choices = chunk.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            delta = first.get("delta")
            if isinstance(delta, dict):
                content = delta.get("content")
                if isinstance(content, str):
                    return content
            message = first.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str):
                    return content
    return ""


def extract_text_from_stream_file(stream_file_path: str) -> str:
    """Parse saved stream file and render currently available text."""
    if not os.path.isfile(stream_file_path):
        raise UniFuncsDeepResearchError(f"Stream file does not exist: {stream_file_path}")
    content_parts: list[str] = []
    try:
        with open(stream_file_path, "r", encoding="utf-8") as reader:
            for raw_line in reader:
                stripped = raw_line.strip()
                if not stripped:
                    continue
                if not stripped.startswith("data:"):
                    content_parts.append(raw_line)
                    continue
                data_raw = stripped[5:].strip()
                if data_raw == "[DONE]":
                    continue
                try:
                    chunk = json.loads(data_raw)
                except json.JSONDecodeError:
                    continue
                text = extract_stream_text(chunk)
                if text:
                    content_parts.append(text)
    except OSError as err:
        raise UniFuncsDeepResearchError(f"Failed to read stream file: {err}") from err
    return "".join(content_parts)


def is_stream_done(stream_file_path: str) -> bool:
    """Check whether stream file contains completion marker."""
    if not os.path.isfile(stream_file_path):
        return False
    try:
        with open(stream_file_path, "r", encoding="utf-8") as reader:
            for raw_line in reader:
                if raw_line.strip() == "data: [DONE]":
                    return True
    except OSError:
        return False
    return False


def cleanup_stream_file_if_done(stream_file_path: str) -> bool:
    """Remove stream file after completion to avoid leftovers."""
    if not is_stream_done(stream_file_path):
        return False
    try:
        os.remove(stream_file_path)
        return True
    except OSError:
        return False


def start_background_worker(args: argparse.Namespace, stream_file_path: str) -> None:
    """Start detached background worker to keep streaming after timeout."""
    cmd = [
        sys.executable,
        os.path.abspath(__file__),
        "--background-worker",
        "--stream-file",
        stream_file_path,
        "--model",
        args.model,
        "--timeout",
        str(args.timeout),
        "--output-type",
        args.output_type,
        "--output-length",
        str(args.output_length),
    ]
    if args.query:
        cmd.append(args.query)
    if args.introduction:
        cmd.extend(["--introduction", args.introduction])
    if args.plan_approval:
        cmd.append("--plan-approval")
    if args.reference_style:
        cmd.extend(["--reference-style", args.reference_style])
    if args.max_depth is not None:
        cmd.extend(["--max-depth", str(args.max_depth)])
    if args.domain_scope:
        cmd.extend(["--domain-scope", args.domain_scope])
    if args.domain_blacklist:
        cmd.extend(["--domain-blacklist", args.domain_blacklist])
    if args.output_prompt:
        cmd.extend(["--output-prompt", args.output_prompt])
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )


def stream_chat(
    payload: Dict[str, Any],
    api_key: str,
    stream_timeout_seconds: int,
    stream_file_path: Optional[str],
) -> tuple[str, bool, Optional[str]]:
    """Stream chat response and persist raw chunks to stream file."""
    req = urllib.request.Request(
        CHAT_COMPLETIONS_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    temp_path = resolve_stream_file_path(stream_file_path)
    content_parts: list[str] = []
    done = False
    started_at = time.monotonic()

    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) as response:
            writer = open(temp_path, "a", encoding="utf-8") if temp_path else None
            try:
                while True:
                    if time.monotonic() - started_at >= stream_timeout_seconds:
                        break
                    line = response.readline()
                    if not line:
                        done = True
                        break
                    decoded = line.decode("utf-8", errors="replace")
                    if writer:
                        writer.write(decoded)
                    stripped = decoded.strip()
                    if not stripped:
                        continue
                    if stripped.startswith("data:"):
                        data_raw = stripped[5:].strip()
                        if data_raw == "[DONE]":
                            done = True
                            break
                        try:
                            chunk = json.loads(data_raw)
                        except json.JSONDecodeError:
                            continue
                        text = extract_stream_text(chunk)
                        if text:
                            content_parts.append(text)
                    else:
                        content_parts.append(decoded)
            finally:
                if writer:
                    writer.close()
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        raise UniFuncsDeepResearchError(f"HTTP {err.code}: {error_body}") from err
    except urllib.error.URLError as err:
        raise UniFuncsDeepResearchError(f"Network error: {err.reason}") from err

    return ("".join(content_parts), done, temp_path)


def render_response(response: Dict[str, Any] | str, raw_response: bool) -> str:
    """Render response for CLI output."""
    if isinstance(response, str):
        return response
    if raw_response:
        return json.dumps(response, ensure_ascii=False, indent=2)
    choices = response.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    return content
    return json.dumps(response, ensure_ascii=False, indent=2)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    validate_args(args)
    try:
        if args.read_stream_file:
            stream_file_path = os.path.abspath(args.stream_file)
            print(extract_text_from_stream_file(stream_file_path))
            if cleanup_stream_file_if_done(stream_file_path):
                print(f"[Cleaned] Stream file removed: {stream_file_path}", file=sys.stderr)
            return

        api_key = get_api_key()
        payload = build_payload(args)
        if args.stream:
            temp_path = resolve_stream_file_path(args.stream_file)
            if not temp_path:
                raise UniFuncsDeepResearchError("No writable stream file available for streaming mode.")

            if args.background_worker:
                stream_chat(payload, api_key, 24 * 60 * 60, temp_path)
                return

            start_background_worker(args, temp_path)
            started_at = time.monotonic()
            while time.monotonic() - started_at < args.timeout:
                if is_stream_done(temp_path):
                    break
                time.sleep(0.5)

            output = extract_text_from_stream_file(temp_path)
            if not is_stream_done(temp_path):
                command = (
                    f'python3 "{os.path.abspath(__file__)}" --read-stream-file --stream-file "{temp_path}"'
                )
                notice_lines = [
                    "",
                    "",
                    f"[Unfinished] No complete response within {args.timeout}s; returning received partial content.",
                    "[Background] Streaming continues in the background.",
                    f"[Stream File] {temp_path}",
                    "[Read Later] Run this command to read received content:",
                    command,
                ]
                output += "\n".join(notice_lines)
            print(output)
        else:
            response = post_json(CHAT_COMPLETIONS_ENDPOINT, payload, api_key)
            print(render_response(response, args.raw_response))
    except UniFuncsDeepResearchError as err:
        print(f"Deep Research chat/completions failed: {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCanceled by user.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
