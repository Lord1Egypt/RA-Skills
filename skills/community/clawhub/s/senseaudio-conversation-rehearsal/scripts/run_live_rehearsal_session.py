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
from senseaudio_api_guard import ensure_runtime_api_key
from analyze_rehearsal_transcript import analyze_text
from build_counterpart_turn import build_turn
from senseaudio_asr import transcribe as transcribe_audio, validate_input as validate_audio
from senseaudio_counterpart_tts import synthesize as synthesize_counterpart


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def gather_user_audio(dir_path: Path) -> list[Path]:
    files = [p for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() in {".mp3", ".wav", ".mp4"}]
    return sorted(files)


def aggregate_user_text(history: dict) -> str:
    lines = []
    for turn in history.get("turns", []):
        if turn.get("kind") == "user" and turn.get("text"):
            lines.append(turn["text"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a multi-turn live rehearsal session with ASR user turns and TTS counterpart turns.")
    parser.add_argument("--blueprint-json", required=True)
    parser.add_argument("--user-audio-dir", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--asr-model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--counterpart-voice-id", default="")
    parser.add_argument("--stream-asr", action="store_true")
    parser.add_argument("--max-user-turns", type=int, default=3)
    parser.add_argument("--send-feishu-audio", action="store_true")
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--chat-id", default="")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--send-labels", action="store_true")
    parser.add_argument("--send-limit", type=int, default=0)
    parser.add_argument("--send-turn-indexes", default="")
    parser.add_argument("--send-delay-ms", type=int, default=0)
    parser.add_argument("--ffmpeg-exe", default="")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    args = parser.parse_args()

    api_key = ensure_runtime_api_key(os.getenv(args.api_key_env), args.api_key_env, purpose="tts")

    blueprint = load_json(Path(args.blueprint_json))
    user_audio_dir = Path(args.user_audio_dir)
    if not user_audio_dir.exists():
        raise SystemExit(f"user audio dir not found: {user_audio_dir}")
    user_audio_files = gather_user_audio(user_audio_dir)[: args.max_user_turns]
    if not user_audio_files:
        raise SystemExit("No user audio files found.")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    history = {"turns": []}

    opening_turn = build_turn(blueprint, history, user_reply="")
    opening_turn_path = outdir / "turn_00_counterpart.json"
    save_json(opening_turn_path, opening_turn)
    opening_audio_path = outdir / "turn_00_counterpart.mp3"
    voice_id = args.counterpart_voice_id or blueprint.get("voice_policy", {}).get("authorized_voice_id", "")
    if not voice_id:
        voice_id = "male_0004_a"
        role = blueprint.get("counterpart", {}).get("role", "")
        if role in {"senior_executive", "mentor_reviewer"}:
            voice_id = "male_0018_a"
    audio_bytes, trace_id, extra_info, chunk_count, model_used = synthesize_counterpart(opening_turn["counterpart_text"], voice_id, api_key)
    opening_audio_path.write_bytes(audio_bytes)
    history["turns"].append(
        {
            "kind": "counterpart",
            "turn_index": 0,
            "phase": opening_turn["phase"],
            "text": opening_turn["counterpart_text"],
            "audio_path": str(opening_audio_path),
            "trace_id": trace_id,
            "voice_id": voice_id,
            "extra_info": extra_info,
            "model_used": model_used,
            "tts_stream": True,
            "tts_stream_chunk_count": chunk_count,
        }
    )

    for idx, audio_path in enumerate(user_audio_files, start=1):
        validate_audio(audio_path)
        transcript_response = transcribe_audio(
            audio_path,
            api_key,
            args.asr_model,
            response_format="json",
            language="",
            stream=args.stream_asr,
        )
        transcript_text = transcript_response.get("text", "")
        transcript_json_path = outdir / f"turn_{idx:02d}_user_transcript.json"
        save_json(
            transcript_json_path,
            {
                "input_audio": str(audio_path),
                "model": args.asr_model,
                "stream": args.stream_asr,
                "stream_chunk_count": transcript_response.get("chunk_count", 0),
                "transcript": transcript_text,
                "raw_response": transcript_response,
            },
        )
        history["turns"].append(
            {
                "kind": "user",
                "turn_index": idx,
                "text": transcript_text,
                "audio_path": str(audio_path),
                "transcript_json": str(transcript_json_path),
            }
        )

        counterpart_turn = build_turn(blueprint, history, user_reply=transcript_text)
        counterpart_turn_path = outdir / f"turn_{idx:02d}_counterpart.json"
        save_json(counterpart_turn_path, counterpart_turn)
        counterpart_audio_path = outdir / f"turn_{idx:02d}_counterpart.mp3"
        audio_bytes, trace_id, extra_info, chunk_count, model_used = synthesize_counterpart(counterpart_turn["counterpart_text"], voice_id, api_key)
        counterpart_audio_path.write_bytes(audio_bytes)
        history["turns"].append(
            {
                "kind": "counterpart",
                "turn_index": idx,
                "phase": counterpart_turn["phase"],
                "text": counterpart_turn["counterpart_text"],
                "audio_path": str(counterpart_audio_path),
                "trace_id": trace_id,
                "voice_id": voice_id,
                "assessment_notes": counterpart_turn.get("assessment_notes", []),
                "extra_info": extra_info,
                "model_used": model_used,
                "tts_stream": True,
                "tts_stream_chunk_count": chunk_count,
            }
        )

    user_transcript_path = outdir / "all_user_replies.txt"
    user_transcript_path.write_text(aggregate_user_text(history), encoding="utf-8")
    debrief = analyze_text(user_transcript_path.read_text(encoding="utf-8"))
    debrief_path = outdir / "debrief.json"
    save_json(debrief_path, debrief)
    history_path = outdir / "history.json"
    save_json(history_path, history)

    result = {
        "blueprint_json": str(Path(args.blueprint_json)),
        "user_audio_dir": str(user_audio_dir),
        "history_json": str(history_path),
        "all_user_replies": str(user_transcript_path),
        "debrief_json": str(debrief_path),
        "turn_count": len(history["turns"]),
        "voice_id": voice_id,
        "stream_asr": args.stream_asr,
        "output_dir": str(outdir),
    }
    if args.send_feishu_audio:
        send_results_path = outdir / "feishu_send_results.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve().parent / "send_rehearsal_counterparts_to_feishu.py"),
                "--history-json",
                str(history_path),
                "--out-json",
                str(send_results_path),
                "--workspace-root",
                args.workspace_root or str(get_workspace_root()),
                *(["--chat-id", args.chat_id] if args.chat_id else []),
                *(["--session-file", args.session_file] if args.session_file else []),
                *(["--send-labels"] if args.send_labels else []),
                *(["--limit", str(args.send_limit)] if args.send_limit > 0 else []),
                *(["--turn-indexes", args.send_turn_indexes] if args.send_turn_indexes else []),
                *(["--delay-ms", str(args.send_delay_ms)] if args.send_delay_ms > 0 else []),
                *(["--ffmpeg-exe", args.ffmpeg_exe] if args.ffmpeg_exe else []),
            ],
            capture_output=True,
            text=True,
            check=False,
            env=os.environ.copy(),
        )
        if completed.returncode != 0:
            raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "send_rehearsal_counterparts_to_feishu.py failed")
        result["feishu_send_json"] = str(send_results_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
