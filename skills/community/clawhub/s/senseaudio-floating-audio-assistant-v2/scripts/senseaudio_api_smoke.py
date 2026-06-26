#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"
ASR_WS_URL = "wss://api.senseaudio.cn/ws/v1/audio/transcriptions"
MUSIC_CREATE_URL = "https://api.senseaudio.cn/v1/music/song/create"
DEFAULT_TTS_MODEL = "SenseAudio-TTS-1.0"
DEFAULT_ASR_MODEL = "senseaudio-asr-deepthink-1.5-260319"
DEFAULT_MUSIC_MODEL = "senseaudio-music-1.0-260319"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnostic smoke test for SenseAudio integration used by this skill.")
    parser.add_argument("--env-file", default="", help="Optional .env file. Defaults to workspace/.env discovered from this skill.")
    parser.add_argument("--live-tts", action="store_true", help="Make a tiny real SenseAudio TTS request and report chunk metadata.")
    parser.add_argument("--voice-id", default="female_0006_a")
    parser.add_argument("--text", default="SenseAudio floating audio assistant smoke test.")
    return parser.parse_args()


def workspace_dir() -> Path:
    return Path(__file__).resolve().parents[3]


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api_key_available() -> bool:
    return bool(os.environ.get("SENSEAUDIO_API_KEY", "").strip() or os.environ.get("AUDIOCLAW_ASR_API_KEY", "").strip())


def resolve_api_key() -> str:
    for name in ("SENSEAUDIO_API_KEY", "AUDIOCLAW_ASR_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise SystemExit("Missing SENSEAUDIO_API_KEY or AUDIOCLAW_ASR_API_KEY.")


def parse_sse_tts(response) -> tuple[int, int, str]:
    chunk_count = 0
    audio_bytes = 0
    trace_id = ""
    for raw_line in response:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line.startswith("data: "):
            continue
        chunk_count += 1
        payload = json.loads(line[6:])
        trace_id = payload.get("trace_id") or trace_id
        base_resp = payload.get("base_resp") or {}
        if base_resp.get("status_code") not in (None, 0):
            raise RuntimeError(base_resp.get("status_msg") or "SenseAudio returned an error.")
        data = payload.get("data") or {}
        audio_hex = data.get("audio") or ""
        audio_bytes += len(audio_hex) // 2
    return chunk_count, audio_bytes, trace_id


def live_tts_probe(api_key: str, text: str, voice_id: str) -> dict:
    payload = {
        "model": DEFAULT_TTS_MODEL,
        "text": text,
        "stream": True,
        "voice_setting": {"voice_id": voice_id},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    request = urllib.request.Request(
        TTS_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "SenseAudio-FloatingAudioAssistant/1.0",
        },
        method="POST",
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            chunk_count, audio_bytes, trace_id = parse_sse_tts(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"SenseAudio TTS HTTP {exc.code}: {body}") from exc
    return {
        "ok": audio_bytes > 0,
        "endpoint": TTS_URL,
        "model": DEFAULT_TTS_MODEL,
        "voice_id": voice_id,
        "chunk_count": chunk_count,
        "audio_bytes": audio_bytes,
        "trace_id": trace_id,
        "elapsed_ms": int((time.time() - started) * 1000),
    }


def main() -> int:
    args = parse_args()
    env_file = Path(args.env_file).expanduser().resolve() if args.env_file else workspace_dir() / ".env"
    load_dotenv(env_file)
    diagnostics = {
        "skill": "senseaudio-floating-audio-assistant",
        "integration_status": "api-backed",
        "api_key_configured": api_key_available(),
        "api_endpoints": {
            "asr_websocket": ASR_WS_URL,
            "tts_http_sse": TTS_URL,
            "music_create": MUSIC_CREATE_URL,
        },
        "models": {
            "asr": DEFAULT_ASR_MODEL,
            "tts": DEFAULT_TTS_MODEL,
            "music": DEFAULT_MUSIC_MODEL,
        },
        "live_probe": None,
    }
    if args.live_tts:
        diagnostics["live_probe"] = live_tts_probe(resolve_api_key(), args.text, args.voice_id)
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
