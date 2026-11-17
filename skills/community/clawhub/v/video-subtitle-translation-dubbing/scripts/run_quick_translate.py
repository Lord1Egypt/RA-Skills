#!/usr/bin/env python3
"""Quick translation and dubbing utility script for developers.

Loads local configuration from `.env`, constructs the appropriate
ManifestParams, and runs the OpenClaw translation_dubbing_skill directly.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add project src to sys.path so it runs without installing
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    from translation_dubbing_skill import ManifestParams, run
    from translation_dubbing_skill.models import ProcessingMode
except ImportError:
    print("❌ Error: Cannot import translation_dubbing_skill. Make sure to run inside project directory.", file=sys.stderr)
    sys.exit(1)


def load_env() -> None:
    """Simple parser to load variables from a local .env file."""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        print("💡 Hint: No .env file found in project root. Reading from system environments.")
        return

    print("🔑 Loading configurations from local .env...")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Quick translation and dubbing CLI utility for OpenClaw Video Subtitle Skill."
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Path to the input English video file."
    )
    parser.add_argument(
        "--subtitle",
        help="Optional path to external subtitle (.srt/.vtt); auto-extracts if not specified."
    )
    parser.add_argument(
        "--mode",
        choices=["subtitle_only", "subtitle_and_dubbing"],
        default="subtitle_and_dubbing",
        help="Execution mode (default: subtitle_and_dubbing)."
    )
    parser.add_argument(
        "--voice",
        help="TTS Voice ID character override."
    )

    args = parser.parse_args()

    # Load local variables
    load_env()

    # Read essential configs from env variables
    trans_provider = os.getenv("TRANSLATION_PROVIDER", "llm")
    trans_endpoint = os.getenv("TRANSLATION_ENDPOINT")
    trans_credential = os.getenv("TRANSLATION_CREDENTIAL")
    trans_model = os.getenv("TRANSLATION_MODEL_NAME", "deepseek-chat")

    tts_provider = os.getenv("TTS_PROVIDER", "web")
    tts_endpoint = os.getenv("TTS_ENDPOINT")
    tts_credential = os.getenv("TTS_CREDENTIAL")
    tts_voice = args.voice or os.getenv("TTS_VOICE_ID", "zh-CN-YunxiNeural")

    if not trans_endpoint or not trans_credential:
        print("❌ Error: TRANSLATION_ENDPOINT and TRANSLATION_CREDENTIAL must be configured in .env", file=sys.stderr)
        return 1

    mode = ProcessingMode.SUBTITLE_AND_DUBBING if args.mode == "subtitle_and_dubbing" else ProcessingMode.SUBTITLE_ONLY

    # If dubbing mode, ensure TTS endpoints are present
    if mode == ProcessingMode.SUBTITLE_AND_DUBBING:
        if not tts_endpoint:
            print("❌ Error: TTS_ENDPOINT must be configured in .env for dubbing mode.", file=sys.stderr)
            return 1

    # Wire manifest params matching the manifest schema defaults
    params = ManifestParams(
        video_path=Path(args.video).resolve(),
        subtitle_path=Path(args.subtitle).resolve() if args.subtitle else None,
        target_language="zh-CN",
        processing_mode=mode,
        voice_id=tts_voice,
        translation_provider=trans_provider,
        translation_endpoint=trans_endpoint,
        translation_credential=trans_credential,
        translation_extra={"model_name": trans_model},
        translation_rate_limit={
            "batch_size_initial": 20,
            "batch_size_min": 1,
            "batch_size_max": 50,
            "payload_size_initial": 4000,
            "payload_size_min": 500,
            "payload_size_max": 32000,
            "payload_unit": "tokens",
            "concurrency_initial": 2,
            "concurrency_min": 1,
            "concurrency_max": 8,
            "max_retries": 5,
            "backoff_base_ms": 500,
            "backoff_jitter_ms": 300,
            "probe_up_every_n_success": 10,
            "supports_batch": True
        },
        tts_provider=tts_provider,
        tts_endpoint=tts_endpoint,
        tts_credential=tts_credential if tts_credential else "none",
        tts_extra={"default_voice": tts_voice},
        tts_rate_limit={
            "batch_size_initial": 1,
            "batch_size_min": 1,
            "batch_size_max": 16,
            "payload_size_initial": 1000,
            "payload_size_min": 200,
            "payload_size_max": 5000,
            "payload_unit": "chars",
            "concurrency_initial": 4,
            "concurrency_min": 1,
            "concurrency_max": 16,
            "max_retries": 5,
            "backoff_base_ms": 500,
            "backoff_jitter_ms": 300,
            "probe_up_every_n_success": 10,
            "supports_batch": False
        }
    )

    # Light logging progress listener
    class SimpleProgressReporter:
        def report(self, event):
            print(f"🔄 [{event.stage.upper()}] {event.message} "
                  f"({event.completed}/{event.total} entries)" if event.total else f"🔄 [{event.stage.upper()}] {event.message}")

    print("🚀 Starting translation & dubbing execution pipeline...")
    try:
        result = await run(params, reporter=SimpleProgressReporter())
        print("\n✨ Finished successfully!")
        print(f"🎥 Output video: {result.output_video_path}")
        print(f"📝 Output subtitle: {result.output_subtitle_path}")
    except Exception as exc:
        print(f"\n❌ Pipeline failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
