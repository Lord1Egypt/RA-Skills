#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def default_credentials_path() -> Path:
    return (Path.home() / ".audioclaw" / "workspace" / "state" / "senseaudio_credentials.json").resolve()


def load_payload(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Write SenseAudio API keys into the user-level AudioClaw credentials file.")
    parser.add_argument("--api-key", default="", help="Shared key used for both ASR and TTS.")
    parser.add_argument("--asr-api-key", default="", help="Optional ASR-only key.")
    parser.add_argument("--tts-api-key", default="", help="Optional TTS-only key.")
    parser.add_argument("--path", default=str(default_credentials_path()))
    args = parser.parse_args()

    target = Path(str(args.path)).expanduser().resolve()
    payload = load_payload(target)

    if args.api_key:
        payload["SENSEAUDIO_API_KEY"] = args.api_key.strip()
    if args.asr_api_key:
        payload["AUDIOCLAW_ASR_API_KEY"] = args.asr_api_key.strip()
    if args.tts_api_key:
        payload["AUDIOCLAW_TTS_API_KEY"] = args.tts_api_key.strip()

    if not payload:
        raise SystemExit("No credentials were provided.")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
