#!/usr/bin/env python3
import json
import mimetypes
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union


API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
SUPPORTED_SUFFIXES = {".wav", ".mp3", ".ogg", ".opus", ".flac", ".aac", ".m4a", ".mp4"}
VALID_MODELS = {"sense-asr-lite", "sense-asr", "sense-asr-pro", "sense-asr-deepthink"}


class SenseAudioASRError(RuntimeError):
    pass


@dataclass
class ASRRequest:
    audio_path: Path
    model: str
    response_format: str = "json"
    enable_speaker_diarization: Optional[bool] = None
    max_speakers: Optional[int] = None


@dataclass
class ASRResult:
    raw_response: Union[dict, str]
    transcript: str
    request_fields: Dict[str, object]


def detect_duration_seconds(path: Path) -> float:
    try:
        output = subprocess.check_output(["/usr/bin/afinfo", str(path)], stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0.0
    for raw_line in output.decode("utf-8", "ignore").splitlines():
        if "estimated duration:" in raw_line:
            try:
                return float(raw_line.split("estimated duration:", 1)[1].strip().split()[0])
            except ValueError:
                return 0.0
    return 0.0


def validate_input(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise SenseAudioASRError(f"Input file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise SenseAudioASRError("Unsupported file type.")
    return {"size_bytes": path.stat().st_size, "duration_seconds": detect_duration_seconds(path)}


def validate_model_support(request: ASRRequest) -> None:
    if request.model not in VALID_MODELS:
        raise SenseAudioASRError(f"Unsupported model: {request.model}")
    if request.model == "sense-asr-deepthink" and request.enable_speaker_diarization:
        raise SenseAudioASRError("sense-asr-deepthink does not support diarization.")


def _iter_field_items(fields: Dict[str, object]) -> Sequence[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for key, value in fields.items():
        if value is None or value == "" or value == []:
            continue
        if isinstance(value, list):
            for entry in value:
                items.append((key, str(entry)))
        elif isinstance(value, bool):
            items.append((key, "true" if value else "false"))
        else:
            items.append((key, str(value)))
    return items


def build_multipart(fields: Dict[str, object], file_field: str, path: Path) -> Tuple[bytes, str]:
    boundary = f"----AudioClawContinuous{uuid.uuid4().hex}"
    chunks = []
    for key, value in _iter_field_items(fields):
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
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


def extract_transcript(response: Union[dict, str]) -> str:
    if isinstance(response, str):
        return response.strip()
    if "text" in response and isinstance(response["text"], str):
        return response["text"].strip()
    if "result" in response and isinstance(response["result"], str):
        return response["result"].strip()
    return ""


def transcribe(request: ASRRequest, api_key: str) -> ASRResult:
    validate_input(request.audio_path)
    validate_model_support(request)
    fields: Dict[str, object] = {
        "model": request.model,
        "response_format": request.response_format,
        "enable_speaker_diarization": request.enable_speaker_diarization,
        "max_speakers": request.max_speakers,
    }
    body, boundary = build_multipart(fields, "file", request.audio_path)
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "AudioClaw-Continuous-Voice/1.0",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                text = response.read().decode("utf-8", "replace")
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    parsed = {"text": text}
                return ASRResult(raw_response=parsed, transcript=extract_transcript(parsed), request_fields=fields)
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", "replace")
            if exc.code == 429 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = SenseAudioASRError(f"HTTP {exc.code}: {body_text}")
            break
        except urllib.error.URLError as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = SenseAudioASRError(f"Network error: {exc}")
            break
    raise last_error or SenseAudioASRError("Unknown ASR failure.")
