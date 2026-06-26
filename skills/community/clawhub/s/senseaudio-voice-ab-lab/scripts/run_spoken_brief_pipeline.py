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
    parser = argparse.ArgumentParser(description="Run the full spoken-brief -> ASR -> A/B -> TTS pipeline.")
    parser.add_argument("--input-audio", required=True)
    parser.add_argument("--voice-id", default="")
    parser.add_argument("--clone-voice-id", default="")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--tones", default="trust,warm,urgent,direct")
    parser.add_argument("--regional-styles", default="neutral")
    parser.add_argument("--stream-asr", action="store_true")
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

    transcript_json = outdir / "spoken_brief_transcript.json"
    brief_json = outdir / "spoken_brief_brief.json"
    manifest_json = outdir / "spoken_brief_manifest.json"
    audio_dir = outdir / "audio"

    run_step(
        [
            sys.executable,
            str(skill_dir / "senseaudio_asr.py"),
            "--input",
            args.input_audio,
            "--out-json",
            str(transcript_json),
            "--model",
            args.model,
            *(["--stream"] if args.stream_asr else []),
        ],
        env,
    )
    run_step(
        [
            sys.executable,
            str(skill_dir / "extract_spoken_brief.py"),
            "--transcript-json",
            str(transcript_json),
            "--out-json",
            str(brief_json),
        ],
        env,
    )
    brief = json.loads(brief_json.read_text(encoding="utf-8"))
    if brief.get("missing_fields"):
        raise SystemExit(f"Missing fields in spoken brief: {', '.join(brief['missing_fields'])}")
    run_step(
        [
            sys.executable,
            str(skill_dir / "build_voice_ab_variants.py"),
            "--brief-json",
            str(brief_json),
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
        "input_audio": args.input_audio,
        "voice_id": selected_voice_id,
        "voice_source": voice_source,
        "stream_asr": args.stream_asr,
        "transcript_json": str(transcript_json),
        "brief_json": str(brief_json),
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
