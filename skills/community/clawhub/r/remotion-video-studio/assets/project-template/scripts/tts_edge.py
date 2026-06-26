#!/usr/bin/env python3
"""
Edge TTS batch generator — generates audio for each slide using Microsoft Edge TTS.

Features:
  - Incremental build: skips slides whose text hasn't changed (hash-based)
  - Multi-speaker support: maps speaker names to voice IDs via config.speakers
  - Retry with exponential backoff (3 attempts)
  - Optional SRT subtitle generation for time-aligned captions

Usage:
    python scripts/tts_edge.py [--config config/project.json] [--content content/subtitles.json]

Prerequisites:
    pip install edge-tts
"""

import hashlib
import json
import os
import subprocess
import sys
import time

from tts_utils import resolve_project_root, parse_tts_args, load_config_and_content, resolve_audio_dir


MAX_RETRIES = 3
RETRY_BASE_DELAY = 2  # seconds


def compute_text_hash(text: str, voice: str, rate: str) -> str:
    """Compute a deterministic hash for TTS input parameters."""
    content = f"{text}|{voice}|{rate}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def load_hash_manifest(manifest_path: str) -> dict:
    """Load the hash manifest file for incremental builds."""
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_hash_manifest(manifest_path: str, manifest: dict) -> None:
    """Save the hash manifest file."""
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def resolve_voice_for_speaker(
    speaker: str,
    speakers_config: dict,
    default_voice: str,
) -> str:
    """Resolve the TTS voice ID for a given speaker name."""
    if not speakers_config:
        return default_voice
    return speakers_config.get(speaker, speakers_config.get("default", default_voice))


def run_edge_tts_with_retry(cmd: list, slide_id: str) -> bool:
    """Run edge-tts command with retry and exponential backoff."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            if attempt < MAX_RETRIES:
                delay = RETRY_BASE_DELAY ** attempt
                print(f"         ⚠️  Attempt {attempt}/{MAX_RETRIES} failed for {slide_id}, retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"         ❌ Failed after {MAX_RETRIES} attempts: {e.stderr or e}")
                return False
        except FileNotFoundError:
            print("         ❌ edge-tts not found. Install with: pip install edge-tts")
            sys.exit(1)
    return False


def main():
    args = parse_tts_args("Edge TTS audio generator")
    root = resolve_project_root()
    config, content, _, _ = load_config_and_content(args, root)
    output_dir = resolve_audio_dir(config, root)

    tts_config = config["tts"]
    edge_config = tts_config["edge"]
    speakers_config = config.get("speakers", {})

    # Compute effective rate: merge global speedRate with per-engine rate
    speed_rate = tts_config.get("speedRate", 1.0)
    rate_percent = round((speed_rate - 1.0) * 100)
    effective_rate = f"{rate_percent:+d}%" if rate_percent != 0 else "+0%"
    engine_rate = edge_config.get("rate", "+0%")
    if engine_rate != "+0%":
        effective_rate = engine_rate

    os.makedirs(output_dir, exist_ok=True)

    # Load hash manifest for incremental builds
    manifest_path = os.path.join(output_dir, ".tts_manifest.json")
    manifest = load_hash_manifest(manifest_path)

    slides = content.get("slides", [])
    if not slides:
        print("[ERROR] No slides found in content file")
        sys.exit(1)

    default_voice = edge_config["voice"]

    print("=" * 50)
    print("  Edge TTS Audio Generation")
    print("=" * 50)
    print(f"  Default Voice : {default_voice}")
    print(f"  SpeedRate     : {speed_rate}x → edge rate: {effective_rate}")
    print(f"  Slides        : {len(slides)}")
    print(f"  Speakers      : {len(speakers_config)} configured")
    print(f"  Incremental   : {'enabled' if manifest else 'first run'}")
    print("=" * 50)

    generated = 0
    skipped = 0
    failed = 0

    for slide in slides:
        slide_id = slide["id"]
        text = slide["text"]
        speaker = slide.get("speaker", "default")
        voice = resolve_voice_for_speaker(speaker, speakers_config, default_voice)
        out_file = os.path.join(output_dir, f"{slide_id}.mp3")
        srt_file = os.path.join(output_dir, f"{slide_id}.srt")

        # Incremental build: check if text/voice/rate changed
        current_hash = compute_text_hash(text, voice, effective_rate)
        prev_hash = manifest.get(slide_id, {}).get("hash", "")

        if os.path.exists(out_file) and current_hash == prev_hash:
            print(f"  [SKIP] {slide_id} — unchanged (hash: {current_hash})")
            skipped += 1
            continue

        print(f'  [GEN]  {slide_id} — voice={voice}, speaker={speaker}')
        print(f'         "{text[:50]}..."')

        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", effective_rate,
            "--volume", edge_config["volume"],
            "--text", text,
            "--write-media", out_file,
            "--write-subtitles", srt_file,
        ]

        if run_edge_tts_with_retry(cmd, slide_id):
            print(f"         ✅ {out_file}")
            manifest[slide_id] = {"hash": current_hash, "voice": voice}
            generated += 1
        else:
            failed += 1

    # Save updated manifest
    save_hash_manifest(manifest_path, manifest)

    print(f"\n{'=' * 50}")
    print(f"  Edge TTS generation complete!")
    print(f"  Generated: {generated}, Skipped: {skipped}, Failed: {failed}")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
