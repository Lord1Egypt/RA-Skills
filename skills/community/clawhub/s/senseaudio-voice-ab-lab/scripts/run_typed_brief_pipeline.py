#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


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

from audioclaw_paths import get_workspace_root


def run_step(args: list[str], env: dict) -> None:
    completed = subprocess.run(args, env=env, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or f"Step failed: {' '.join(args)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full typed-brief -> A/B -> TTS pipeline, with optional Feishu audio sending.")
    parser.add_argument("--campaign-name", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--key-message", required=True)
    parser.add_argument("--cta", required=True)
    parser.add_argument("--offer", default="")
    parser.add_argument("--proof", default="")
    parser.add_argument("--voice-id", default="")
    parser.add_argument("--clone-voice-id", default="")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--tones", default="trust,warm,urgent,direct")
    parser.add_argument("--regional-styles", default="neutral")
    parser.add_argument("--send-feishu-audio", action="store_true")
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--chat-id", default="")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--send-labels", action="store_true")
    parser.add_argument("--send-limit", type=int, default=0)
    parser.add_argument("--send-variant-ids", default="")
    parser.add_argument("--send-delay-ms", type=int, default=0)
    parser.add_argument("--ffmpeg-exe", default="")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    args = parser.parse_args()

    selected_voice_id = args.clone_voice_id or args.voice_id
    if not selected_voice_id:
        raise SystemExit("Provide either --voice-id or --clone-voice-id.")
    voice_source = "clone" if args.clone_voice_id else "system"

    skill_dir = Path(__file__).resolve().parent
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()

    manifest_json = outdir / "typed_brief_manifest.json"
    audio_dir = outdir / "audio"

    run_step(
        [
            sys.executable,
            str(skill_dir / "build_voice_ab_variants.py"),
            "--campaign-name",
            args.campaign_name,
            "--product",
            args.product,
            "--audience",
            args.audience,
            "--key-message",
            args.key_message,
            "--cta",
            args.cta,
            *(["--offer", args.offer] if args.offer else []),
            *(["--proof", args.proof] if args.proof else []),
            "--tones",
            args.tones,
            "--regional-styles",
            args.regional_styles,
            "--out-json",
            str(manifest_json),
        ],
        env,
    )
    run_step(
        [
            sys.executable,
            str(skill_dir / "batch_tts_variants.py"),
            "--manifest",
            str(manifest_json),
            "--voice-id",
            selected_voice_id,
            "--outdir",
            str(audio_dir),
            "--voice-source",
            voice_source,
            "--api-key-env",
            args.api_key_env,
        ],
        env,
    )

    result = {
        "campaign_name": args.campaign_name,
        "voice_id": selected_voice_id,
        "voice_source": voice_source,
        "manifest_json": str(manifest_json),
        "audio_dir": str(audio_dir),
    }
    if args.send_feishu_audio:
        feishu_send_json = audio_dir / "feishu_send_results.json"
        run_step(
            [
                sys.executable,
                str(skill_dir / "send_ab_variants_to_feishu.py"),
                "--tts-results",
                str(audio_dir / "tts_results.json"),
                "--out-json",
                str(feishu_send_json),
                "--workspace-root",
                args.workspace_root or str(get_workspace_root()),
                *(["--chat-id", args.chat_id] if args.chat_id else []),
                *(["--session-file", args.session_file] if args.session_file else []),
                *(["--send-labels"] if args.send_labels else []),
                *(["--limit", str(args.send_limit)] if args.send_limit > 0 else []),
                *(["--variant-ids", args.send_variant_ids] if args.send_variant_ids else []),
                *(["--delay-ms", str(args.send_delay_ms)] if args.send_delay_ms > 0 else []),
                *(["--ffmpeg-exe", args.ffmpeg_exe] if args.ffmpeg_exe else []),
            ],
            env,
        )
        result["feishu_send_json"] = str(feishu_send_json)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
