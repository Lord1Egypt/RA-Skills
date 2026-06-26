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


def write_text_transcript(path: Path, text: str) -> None:
    cleaned = str(text or "").strip()
    if not cleaned:
        raise SystemExit("input text is empty")
    payload = {
        "request": {
            "input_text": cleaned,
            "channel": "",
            "user_id": "",
        },
        "routing": {
            "mode": "direct_text",
            "selected_model": "",
            "model_reason": "text_input_bypasses_asr",
        },
        "audio": {
            "size_bytes": 0,
            "duration_seconds": 0,
        },
        "transcript": {
            "raw_text": cleaned,
            "normalized_text": cleaned,
            "empty": False,
        },
        "understanding": {
            "clarification_needed": False,
            "clarification_prompt": "",
            "segment_count": 1,
            "input_type": "text",
        },
        "openclaw": {
            "turn_payload": {
                "role": "user",
                "content": cleaned,
                "metadata": {
                    "input_type": "text",
                    "channel": "",
                    "user_id": "",
                    "clarification_needed": False,
                },
            }
        },
        "raw_response": {
            "text": cleaned,
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full player-input -> NPC reply -> TTS pipeline.")
    parser.add_argument("--input-audio", default="")
    parser.add_argument("--input-text", default="")
    parser.add_argument("--profile-json", required=True)
    parser.add_argument("--relationship", default="neutral")
    parser.add_argument("--location", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--voice-id", default="")
    parser.add_argument("--clone-voice-id", default="")
    parser.add_argument("--model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--stream-asr", action="store_true")
    parser.add_argument("--send-feishu-audio", action="store_true")
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--chat-id", default="")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--send-labels", action="store_true")
    parser.add_argument("--send-limit", type=int, default=0)
    parser.add_argument("--send-line-ids", default="")
    parser.add_argument("--send-delay-ms", type=int, default=0)
    parser.add_argument("--ffmpeg-exe", default="")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    args = parser.parse_args()

    selected_voice_id = args.clone_voice_id or args.voice_id
    voice_source = "clone" if args.clone_voice_id else "system"

    skill_dir = Path(__file__).resolve().parent
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()

    if bool(args.input_audio.strip()) == bool(args.input_text.strip()):
        raise SystemExit("Provide exactly one of --input-audio or --input-text.")

    transcript_json = outdir / "player_transcript.json"
    manifest_json = outdir / "npc_reply_manifest.json"
    audio_dir = outdir / "audio"

    if args.input_audio.strip():
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
    else:
        write_text_transcript(transcript_json, args.input_text)
    run_step(
        [
            sys.executable,
            str(skill_dir / "build_npc_reply_from_player.py"),
            "--profile-json",
            args.profile_json,
            "--player-transcript-json",
            str(transcript_json),
            "--relationship",
            args.relationship,
            "--location",
            args.location,
            "--objective",
            args.objective,
            "--out-json",
            str(manifest_json),
        ],
        env,
    )
    run_step(
        [
            sys.executable,
            str(skill_dir / "batch_tts_scene.py"),
            "--manifest",
            str(manifest_json),
            "--outdir",
            str(audio_dir),
            *(["--voice-id", selected_voice_id] if selected_voice_id else []),
            "--voice-source",
            voice_source,
            "--api-key-env",
            args.api_key_env,
        ],
        env,
    )

    result = {
        "input_audio": args.input_audio,
        "input_text": args.input_text,
        "profile_json": args.profile_json,
        "relationship": args.relationship,
        "location": args.location,
        "objective": args.objective,
        "voice_id": selected_voice_id,
        "voice_source": voice_source,
        "stream_asr": args.stream_asr,
        "transcript_json": str(transcript_json),
        "manifest_json": str(manifest_json),
        "audio_dir": str(audio_dir),
    }
    if args.send_feishu_audio:
        feishu_send_json = audio_dir / "feishu_send_results.json"
        run_step(
            [
                sys.executable,
                str(skill_dir / "send_npc_scene_to_feishu.py"),
                "--scene-tts-results",
                str(audio_dir / "scene_tts_results.json"),
                "--out-json",
                str(feishu_send_json),
                "--workspace-root",
                args.workspace_root or str(get_workspace_root()),
                *(["--chat-id", args.chat_id] if args.chat_id else []),
                *(["--session-file", args.session_file] if args.session_file else []),
                *(["--send-labels"] if args.send_labels else []),
                *(["--limit", str(args.send_limit)] if args.send_limit > 0 else []),
                *(["--line-ids", args.send_line_ids] if args.send_line_ids else []),
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
