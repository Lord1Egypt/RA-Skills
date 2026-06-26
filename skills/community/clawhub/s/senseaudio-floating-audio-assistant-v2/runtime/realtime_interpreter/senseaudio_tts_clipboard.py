#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthesize clipboard text with SenseAudio TTS.")
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--voice-id", default="female_0006_a")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--output-audio", default="")
    return parser.parse_args()


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def resolve_api_keys() -> list[str]:
    keys: list[str] = []
    for key_name in ["SENSEAUDIO_API_KEY", "AUDIOCLAW_ASR_API_KEY"]:
        value = os.environ.get(key_name, "").strip()
        if value and value not in keys:
            keys.append(value)
    if not keys:
        raise SystemExit("Missing SenseAudio API key.")
    return keys


def is_auth_error(error: str) -> bool:
    lowered = error.lower()
    return "http 401" in lowered or "authentication_error" in lowered or "incorrect api key" in lowered


def parse_sse_audio(response) -> Tuple[bytes, Optional[str], Optional[dict], int]:
    audio_parts = []
    trace_id = None
    extra_info = None
    chunk_count = 0
    for raw_line in response:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line or not line.startswith("data: "):
            continue
        chunk_count += 1
        payload = json.loads(line[6:])
        base_resp = payload.get("base_resp") or {}
        if base_resp.get("status_code") not in (None, 0):
            raise RuntimeError(base_resp.get("status_msg") or "SenseAudio returned an error.")
        trace_id = payload.get("trace_id") or trace_id
        if payload.get("extra_info"):
            extra_info = payload["extra_info"]
        data = payload.get("data") or {}
        audio_hex = data.get("audio")
        if audio_hex:
            audio_parts.append(bytes.fromhex(audio_hex))
    return b"".join(audio_parts), trace_id, extra_info, chunk_count


def candidate_models(voice_id: str) -> list[str]:
    if voice_id.startswith("vc-"):
        return ["SenseAudio-TTS-1.5", "SenseAudio-TTS-1.0"]
    return ["SenseAudio-TTS-1.0"]


def synthesize(text: str, voice_id: str, api_key: str) -> Tuple[bytes, Optional[str], Optional[dict], int, str]:
    last_error = ""
    for model in candidate_models(voice_id):
        payload = {
            "model": model,
            "text": text,
            "stream": True,
            "voice_setting": {"voice_id": voice_id},
            "audio_setting": {"format": "mp3", "sample_rate": 32000},
        }
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "AudioClaw-RealtimeInterpreter/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                audio_bytes, trace_id, extra_info, chunk_count = parse_sse_audio(response)
                return audio_bytes, trace_id, extra_info, chunk_count, model
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            last_error = f"HTTP {exc.code}: {body}"
            if voice_id.startswith("vc-") and "model does not support this capability" in last_error.lower():
                continue
            raise RuntimeError(last_error) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network error: {exc}") from exc
    raise RuntimeError(last_error or "No compatible TTS model found.")


def main() -> int:
    args = parse_args()
    if args.env_file.strip():
        load_dotenv(Path(args.env_file).expanduser().resolve())
    text_path = Path(args.text_file).expanduser().resolve()
    text = text_path.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("Clipboard text is empty.")
    output_audio = Path(args.output_audio).expanduser().resolve() if args.output_audio else text_path.with_suffix(".mp3")
    output_audio.parent.mkdir(parents=True, exist_ok=True)

    last_error = ""
    for api_key in resolve_api_keys():
        try:
            audio_bytes, trace_id, extra_info, chunk_count, model_used = synthesize(text, args.voice_id, api_key)
            break
        except RuntimeError as exc:
            last_error = str(exc)
            if is_auth_error(last_error):
                continue
            raise
    else:
        raise RuntimeError(last_error or "SenseAudio TTS authentication failed.")

    output_audio.write_bytes(audio_bytes)
    manifest = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "text_file": str(text_path),
        "output_audio": str(output_audio),
        "voice_id": args.voice_id,
        "model_used": model_used,
        "trace_id": trace_id,
        "extra_info": extra_info,
        "chunk_count": chunk_count,
    }
    output_audio.with_suffix(".meta.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
