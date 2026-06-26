#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Dict, Tuple


def _bootstrap_shared_senseaudio_env() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "_shared" / "senseaudio_env.py"
        if candidate.exists():
            candidate_dir = str(candidate.parent)
            if candidate_dir not in sys.path:
                sys.path.insert(0, candidate_dir)
            from senseaudio_env import ensure_senseaudio_env
            ensure_senseaudio_env()
            return


_bootstrap_shared_senseaudio_env()

from senseaudio_api_guard import ensure_runtime_api_key


OPENAPI_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
PLATFORM_URL = "https://platform.senseaudio.cn/api/audio/transcriptions"
SUPPORTED_SUFFIXES = {".mp3", ".wav", ".mp4"}
OPENAPI_MAX_BYTES = 10 * 1024 * 1024
PLATFORM_MAX_BYTES = 100 * 1024 * 1024
MAX_SECONDS = 7200


def detect_duration_seconds(path: Path) -> float:
    try:
        output = subprocess.check_output(["/usr/bin/afinfo", str(path)], stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0.0
    for raw_line in output.decode("utf-8", "ignore").splitlines():
        if "estimated duration:" not in raw_line:
            continue
        fragment = raw_line.split("estimated duration:", 1)[1].strip()
        seconds = fragment.split()[0]
        try:
            return float(seconds)
        except ValueError:
            return 0.0
    return 0.0


def build_multipart(fields: Dict[str, str], file_field: str, path: Path) -> Tuple[bytes, str]:
    boundary = f"----CodexSenseAudio{uuid.uuid4().hex}"
    chunks = []
    for key, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    chunks.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{path.name}"\r\n'.encode("utf-8"),
            f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
            path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return b"".join(chunks), boundary


def validate_input(path: Path, max_bytes: int) -> None:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise SystemExit("Unsupported file type. Expected one of: .mp3, .wav, .mp4")
    if path.stat().st_size > max_bytes:
        raise SystemExit(f"Input file exceeds the current endpoint limit of {max_bytes // (1024 * 1024)}MB.")
    duration = detect_duration_seconds(path)
    if duration and duration > MAX_SECONDS:
        raise SystemExit("Input audio exceeds the official 2-hour web limit.")


def send_request(request: urllib.request.Request) -> dict:
    return send_request_with_mode(request, stream=False)


def parse_stream_response(response) -> dict:
    events = []
    partial_texts = []
    final_text = ""
    for raw_line in response:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line:
            continue
        if line.startswith("data:"):
            line = line[5:].strip()
        if not line or line == "[DONE]":
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        events.append(payload)
        candidates = [
            payload.get("text"),
            payload.get("transcript"),
            (payload.get("data") or {}).get("text"),
            (payload.get("result") or {}).get("text"),
            payload.get("delta"),
            (payload.get("data") or {}).get("delta"),
        ]
        for value in candidates:
            if isinstance(value, str) and value:
                partial_texts.append(value)
                final_text = value
    if not final_text:
        final_text = "".join(partial_texts).strip()
    return {
        "text": final_text,
        "stream": True,
        "chunk_count": len(events),
        "events": events,
        "partials": partial_texts,
    }


def send_request_with_mode(request: urllib.request.Request, *, stream: bool) -> dict:
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                if stream:
                    return parse_stream_response(response)
                text = response.read().decode("utf-8", "replace")
                return json.loads(text) if text else {"text": ""}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                payload = {"message": body}
            if exc.code == 429 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = RuntimeError(f"HTTP {exc.code}: {json.dumps(payload, ensure_ascii=False)}")
            break
        except urllib.error.URLError as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = RuntimeError(f"Network error: {exc}")
            break
    if last_error:
        raise last_error
    raise RuntimeError("Unknown ASR request failure.")


def transcribe_openapi(path: Path, api_key: str, model: str, response_format: str, language: str, stream: bool) -> dict:
    if not model:
        raise SystemExit("Missing ASR model. Set SENSEAUDIO_ASR_MODEL or pass --model for openapi mode.")
    fields = {"model": model, "response_format": response_format}
    if language:
        fields["language"] = language
    if stream:
        fields["stream"] = "true"
    body, boundary = build_multipart(fields, "file", path)
    request = urllib.request.Request(
        OPENAPI_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "Codex-SenseAudio-ASR/1.0",
        },
        method="POST",
    )
    return send_request_with_mode(request, stream=stream)


def transcribe_platform(path: Path, token: str, response_format: str, stream: bool) -> dict:
    fields = {"purpose": "speech_to_text", "response_format": response_format}
    if stream:
        fields["stream"] = "true"
    body, boundary = build_multipart(fields, "file", path)
    request = urllib.request.Request(
        PLATFORM_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "Codex-SenseAudio-ASR/1.0",
            "x-platform": "WEB",
            "x-version": "1.0.2",
            "x-language": "zh-cn",
            "x-product": "SenseAudio",
        },
        method="POST",
    )
    return send_request_with_mode(request, stream=stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audio with SenseAudio official ASR endpoints.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--mode", choices=["auto", "openapi", "platform"], default="auto")
    parser.add_argument("--model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--response-format", choices=["json", "text"], default="json")
    parser.add_argument("--language", choices=["", "zh", "en"], default="")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    parser.add_argument("--platform-token-env", default="SENSEAUDIO_PLATFORM_TOKEN")
    args = parser.parse_args()

    path = Path(args.input)
    api_key = os.getenv(args.api_key_env, "")
    platform_token = os.getenv(args.platform_token_env, "")

    selected_mode = args.mode
    if selected_mode == "auto":
        selected_mode = "platform" if platform_token else "openapi"

    if selected_mode == "platform":
        if not platform_token:
            raise SystemExit(f"Missing platform token in ${args.platform_token_env}.")
        validate_input(path, PLATFORM_MAX_BYTES)
        response = transcribe_platform(path, platform_token, args.response_format, args.stream)
        endpoint = PLATFORM_URL
        model = ""
    else:
        api_key = ensure_runtime_api_key(api_key, args.api_key_env, purpose="asr")
        validate_input(path, OPENAPI_MAX_BYTES)
        response = transcribe_openapi(path, api_key, args.model, args.response_format, args.language, args.stream)
        endpoint = OPENAPI_URL
        model = args.model

    result = {
        "mode": selected_mode,
        "endpoint": endpoint,
        "input_path": str(path),
        "model": model,
        "response_format": args.response_format,
        "language": args.language,
        "stream": args.stream,
        "transcript": response.get("text", "") if isinstance(response, dict) else str(response),
        "stream_chunk_count": response.get("chunk_count", 0) if isinstance(response, dict) else 0,
        "raw_response": response,
    }
    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
