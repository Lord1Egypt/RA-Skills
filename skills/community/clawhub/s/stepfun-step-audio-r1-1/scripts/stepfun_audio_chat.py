#!/usr/bin/env python3
"""
Call StepFun chat.completions with model step-audio-r1.1 and save a
non-streaming response object, returned audio, and transcript.
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import parse
from urllib import error, request


DEFAULT_API_BASE_URL = "https://api.stepfun.com"
DEFAULT_MODEL = "step-audio-r1.1"
DEFAULT_VOICE = "wenrounansheng"
DEFAULT_FORMAT = "wav"
MAX_INPUT_AUDIO_DATA_URL_BYTES = 10 * 1024 * 1024
OFFICIAL_VOICE_HINTS = [
    "wenrounansheng",
    "qingchunshaonv",
    "livelybreezy-female",
    "elegantgentle-female",
]
MIME_EXTENSION_MAP = {
    "audio/aac": "aac",
    "audio/flac": "flac",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/mp4": "m4a",
    "audio/ogg": "ogg",
    "audio/wav": "wav",
    "audio/webm": "webm",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Call StepFun /v1/chat/completions with model step-audio-r1.1 and "
            "save the non-streaming response payload."
        )
    )
    parser.add_argument(
        "--prompt",
        default="",
        help="User text prompt to send with the request.",
    )
    parser.add_argument(
        "--system",
        default="",
        help="Optional system instruction.",
    )
    parser.add_argument(
        "--input-audio",
        default="",
        help="Optional local audio file to send as input_audio.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name. Default: {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--voice",
        default=os.environ.get("STEPFUN_AUDIO_VOICE", DEFAULT_VOICE),
        help=(
            f"Output voice id. Default: {DEFAULT_VOICE}. "
            "Can also be set via STEPFUN_AUDIO_VOICE."
        ),
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        help=f"Output audio format for non-streaming replies. Default: {DEFAULT_FORMAT}.",
    )
    parser.add_argument(
        "--api-base-url",
        default=os.environ.get("STEP_API_BASE_URL", DEFAULT_API_BASE_URL),
        help=f"API base URL. Default: {DEFAULT_API_BASE_URL}.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Optional temperature override.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Optional max_tokens override.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Directory where request/response artifacts should be written.",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print request JSON in dry-run mode or response JSON after a call.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build the payload, save request.json, and stop before the network call.",
    )
    parser.add_argument(
        "--no-audio-output",
        action="store_true",
        help="Request text-only output instead of text plus audio.",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available custom/cloned voice ids from StepFun and exit.",
    )
    parser.add_argument(
        "--voice-limit",
        type=int,
        default=20,
        help="How many custom voices to fetch when using --list-voices. Default: 20.",
    )
    return parser.parse_args()


def ensure_request_has_content(args: argparse.Namespace) -> None:
    if args.list_voices:
        return
    if args.prompt or args.input_audio:
        return
    raise SystemExit("Provide --prompt, --input-audio, or both.")


def validate_args(args: argparse.Namespace) -> None:
    if args.list_voices:
        if args.voice_limit < 1 or args.voice_limit > 100:
            raise SystemExit("--voice-limit must be between 1 and 100.")
        return
    if not args.no_audio_output and args.format.lower() != "wav":
        raise SystemExit(
            "step-audio-r1.1 non-streaming audio replies should use --format wav."
        )


def convert_audio_to_wav_bytes(audio_path: Path) -> bytes:
    ffmpeg = shutil.which("ffmpeg")
    afconvert = shutil.which("afconvert")
    with tempfile.TemporaryDirectory(prefix="stepfun-audio-") as tmp_dir:
        wav_path = Path(tmp_dir) / f"{audio_path.stem}.wav"
        if ffmpeg:
            cmd = [
                ffmpeg,
                "-y",
                "-i",
                str(audio_path),
                "-ac",
                "1",
                str(wav_path),
            ]
        elif afconvert:
            cmd = [
                afconvert,
                "-f",
                "WAVE",
                "-d",
                "LEI16",
                str(audio_path),
                str(wav_path),
            ]
        else:
            raise SystemExit(
                "StepFun input_audio currently requires WAV. Provide a .wav file, "
                "or install ffmpeg/afconvert so this script can convert it."
            )

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not wav_path.is_file():
            stderr = result.stderr.strip()
            stdout = result.stdout.strip()
            detail = stderr or stdout or "unknown conversion failure"
            raise SystemExit(f"Failed to convert input audio to WAV: {detail}")
        return wav_path.read_bytes()


def audio_file_to_stepfun_input_data_url(audio_path: Path) -> str:
    if audio_path.suffix.lower() == ".wav":
        encoded = base64.b64encode(audio_path.read_bytes()).decode("ascii")
        data_url = f"data:audio/wav;base64,{encoded}"
    else:
        encoded = base64.b64encode(convert_audio_to_wav_bytes(audio_path)).decode("ascii")
        data_url = f"data:audio/wav;base64,{encoded}"
    if len(data_url.encode("ascii")) > MAX_INPUT_AUDIO_DATA_URL_BYTES:
        raise SystemExit(
            "Input audio exceeds StepFun's 10MB base64 limit after WAV normalization."
        )
    return data_url


def resolve_api_key() -> str:
    api_key = os.environ.get("STEPFUN_API_KEY", "").strip()
    if api_key:
        return api_key
    api_key = os.environ.get("STEP_API_KEY", "").strip()
    if api_key:
        return api_key
    raise SystemExit("Missing STEPFUN_API_KEY. STEP_API_KEY is also accepted as a legacy alias.")


def build_messages(args: argparse.Namespace) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})

    if args.input_audio:
        audio_path = Path(args.input_audio).expanduser().resolve()
        if not audio_path.is_file():
            raise SystemExit(f"Input audio file not found: {audio_path}")
        parts: List[Dict[str, Any]] = []
        if args.prompt:
            parts.append({"type": "text", "text": args.prompt})
        parts.append(
            {
                "type": "input_audio",
                "input_audio": {
                    "data": audio_file_to_stepfun_input_data_url(audio_path),
                },
            }
        )
        messages.append({"role": "user", "content": parts})
        return messages

    messages.append({"role": "user", "content": args.prompt})
    return messages


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": args.model,
        "messages": build_messages(args),
        "stream": False,
        "modalities": ["text"] if args.no_audio_output else ["text", "audio"],
    }
    if not args.no_audio_output:
        payload["audio"] = {
            "voice": args.voice,
            "format": args.format,
        }
    if args.temperature is not None:
        payload["temperature"] = args.temperature
    if args.max_tokens is not None:
        payload["max_tokens"] = args.max_tokens
    return payload


def create_output_dir(path_arg: str) -> Path:
    if path_arg:
        out_dir = Path(path_arg).expanduser().resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = Path.cwd() / f"stepfun-step-audio-r1-1-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def api_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/v1/chat/completions"


def list_voices_url(base_url: str, limit: int) -> str:
    query = parse.urlencode({"limit": limit, "order": "desc"})
    return base_url.rstrip("/") + f"/v1/audio/voices?{query}"


def post_json(url: str, api_key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"StepFun API returned HTTP {exc.code}: {detail.strip() or exc.reason}"
        ) from exc
    except error.URLError as exc:
        raise SystemExit(f"Failed to reach StepFun API: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"StepFun API did not return valid JSON: {exc}") from exc


def get_json(url: str, api_key: str) -> Dict[str, Any]:
    req = request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"StepFun API returned HTTP {exc.code}: {detail.strip() or exc.reason}"
        ) from exc
    except error.URLError as exc:
        raise SystemExit(f"Failed to reach StepFun API: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"StepFun API did not return valid JSON: {exc}") from exc


def extract_first_message(response: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise SystemExit("Response did not include choices[0].")
    first = choices[0]
    if not isinstance(first, dict):
        raise SystemExit("choices[0] was not an object.")
    message = first.get("message")
    if not isinstance(message, dict):
        raise SystemExit("choices[0].message was missing or invalid.")
    finish_reason = first.get("finish_reason")
    if finish_reason is not None and not isinstance(finish_reason, str):
        finish_reason = str(finish_reason)
    return message, finish_reason


def normalize_message_text(content: Any) -> Optional[str]:
    if content is None:
        return None
    if isinstance(content, str):
        stripped = content.strip()
        return stripped or None
    if isinstance(content, list):
        fragments: List[str] = []
        for item in content:
            if isinstance(item, str):
                if item.strip():
                    fragments.append(item.strip())
                continue
            if not isinstance(item, dict):
                continue
            text_value = item.get("text")
            if isinstance(text_value, str) and text_value.strip():
                fragments.append(text_value.strip())
        if fragments:
            return "\n".join(fragments)
        return json.dumps(content, ensure_ascii=False, indent=2)
    return json.dumps(content, ensure_ascii=False, indent=2)


def decode_audio_blob(audio_data: str) -> Tuple[bytes, Optional[str]]:
    if audio_data.startswith("data:") and ";base64," in audio_data:
        prefix, encoded = audio_data.split(";base64,", 1)
        mime_type = prefix[5:] if prefix.startswith("data:") else None
        return base64.b64decode(encoded), mime_type
    return base64.b64decode(audio_data), None


def extension_for_audio(mime_type: Optional[str], fallback: str) -> str:
    if mime_type and mime_type in MIME_EXTENSION_MAP:
        return MIME_EXTENSION_MAP[mime_type]
    return fallback.lstrip(".")


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_request_has_content(args)
    validate_args(args)

    if args.list_voices:
        api_key = resolve_api_key()
        voices = get_json(list_voices_url(args.api_base_url, args.voice_limit), api_key)
        if args.print_json:
            print(json.dumps(voices, ensure_ascii=False, indent=2))
        else:
            print("Custom/cloned StepFun voices for this account:")
            for item in voices.get("data", []):
                if not isinstance(item, dict):
                    continue
                voice_id = item.get("id", "")
                file_id = item.get("file_id", "")
                created_at = item.get("created_at", "")
                print(f"- {voice_id}  file_id={file_id}  created_at={created_at}")
            print("\nOfficial voice hints from StepFun docs:")
            for voice_id in OFFICIAL_VOICE_HINTS:
                print(f"- {voice_id}")
        return 0

    output_dir = create_output_dir(args.output_dir)
    payload = build_payload(args)

    if args.dry_run:
        request_path = output_dir / "request.json"
        write_json(request_path, payload)
        print(f"Dry run complete. Request saved to: {request_path}")
        if args.print_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    api_key = resolve_api_key()
    response = post_json(api_url(args.api_base_url), api_key, payload)
    response_path = output_dir / "response.json"
    write_json(response_path, response)

    message, finish_reason = extract_first_message(response)
    text_content = normalize_message_text(message.get("content"))

    audio_block = message.get("audio")
    audio_path: Optional[Path] = None
    transcript_path: Optional[Path] = None
    transcript_text: Optional[str] = None

    if isinstance(audio_block, dict):
        transcript = audio_block.get("transcript")
        if isinstance(transcript, str) and transcript.strip():
            transcript_text = transcript.strip()
            transcript_path = output_dir / "transcript.txt"
            transcript_path.write_text(transcript_text + "\n", encoding="utf-8")

        audio_data = audio_block.get("data")
        if isinstance(audio_data, str) and audio_data.strip():
            audio_bytes, mime_type = decode_audio_blob(audio_data)
            extension = extension_for_audio(mime_type, args.format)
            audio_path = output_dir / f"response.{extension}"
            audio_path.write_bytes(audio_bytes)

    content_path: Optional[Path] = None
    if text_content:
        content_path = output_dir / "content.txt"
        content_path.write_text(text_content + "\n", encoding="utf-8")

    print(f"Response saved to: {response_path}")
    if audio_path:
        print(f"Audio saved to: {audio_path}")
    else:
        print("Audio saved to: none")
    if transcript_path:
        print(f"Transcript saved to: {transcript_path}")
    else:
        print("Transcript saved to: none")
    if content_path:
        print(f"Text content saved to: {content_path}")
    else:
        print("Text content saved to: none")
    if finish_reason:
        print(f"Finish reason: {finish_reason}")
    if transcript_text:
        print("\nTranscript:\n")
        print(transcript_text)
    elif text_content:
        print("\nAssistant text:\n")
        print(text_content)

    if args.print_json:
        print("\nFull response JSON:\n")
        print(json.dumps(response, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
