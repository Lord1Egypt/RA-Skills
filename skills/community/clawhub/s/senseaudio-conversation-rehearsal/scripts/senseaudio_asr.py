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
SUPPORTED_SUFFIXES = {".mp3", ".wav", ".mp4"}
OPENAPI_MAX_BYTES = 10 * 1024 * 1024
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


def validate_input(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise SystemExit("Unsupported file type. Expected one of: .mp3, .wav, .mp4")
    if path.stat().st_size > OPENAPI_MAX_BYTES:
        raise SystemExit("Input file exceeds the official HTTP API 10MB limit.")
    duration = detect_duration_seconds(path)
    if duration and duration > MAX_SECONDS:
        raise SystemExit("Input audio exceeds the official 2-hour limit.")


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


def transcribe(
    path: Path,
    api_key: str,
    model: str,
    response_format: str = "json",
    language: str = "",
    stream: bool = False,
) -> dict:
    return transcribe_with_stream(path, api_key, model, response_format=response_format, language=language, stream=stream)


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


def transcribe_with_stream(path: Path, api_key: str, model: str, response_format: str = "json", language: str = "", stream: bool = False) -> dict:
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
            "User-Agent": "Codex-SenseAudio-Rehearsal-ASR/1.0",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                if stream:
                    return parse_stream_response(response)
                text = response.read().decode("utf-8", "replace")
                return json.loads(text) if text else {"text": ""}
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(body_text)
            except json.JSONDecodeError:
                payload = {"message": body_text}
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe rehearsal user audio with SenseAudio ASR.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--response-format", choices=["json", "text"], default="json")
    parser.add_argument("--language", choices=["", "zh", "en"], default="")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    args = parser.parse_args()

    api_key = ensure_runtime_api_key(os.getenv(args.api_key_env), args.api_key_env, purpose="asr")
    path = Path(args.input)
    validate_input(path)
    response = transcribe_with_stream(path, api_key, args.model, args.response_format, args.language, stream=args.stream)

    result = {
        "endpoint": OPENAPI_URL,
        "input_path": str(path),
        "model": args.model,
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
