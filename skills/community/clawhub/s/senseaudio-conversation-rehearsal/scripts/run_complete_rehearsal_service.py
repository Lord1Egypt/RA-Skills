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

from senseaudio_clone_workspace import (
    create_clone,
    create_clone_via_browser,
    extract_voice_id,
    list_available_voices,
    list_available_voices_via_browser,
    pick_latest_clone_voice,
)
from senseaudio_platform_token import resolve_platform_token


SCRIPT_DIR = Path(__file__).resolve().parent
BUILD_BLUEPRINT = SCRIPT_DIR / "build_rehearsal_blueprint.py"
RUN_SESSION = SCRIPT_DIR / "run_live_rehearsal_session.py"


def run_python(script: Path, args: list[str], env: dict) -> dict:
    command = [sys.executable, str(script), *args]
    result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"{script.name} failed"
        raise RuntimeError(message)
    stdout = result.stdout.strip()
    if not stdout:
        return {}
    return json.loads(stdout)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_clone_voice(
    platform_token: str,
    voice_sample_path: Path,
    voice_name: str,
    slot_id: str,
) -> tuple[str, dict]:
    clone_result = create_clone(
        platform_token,
        voice_sample_path,
        slot_id=slot_id or None,
        voice_name=voice_name,
    )
    voice_id = extract_voice_id(clone_result)
    available = list_available_voices(platform_token)
    picked = pick_latest_clone_voice(available, preferred_name=voice_name or voice_sample_path.stem)
    if not voice_id and picked:
        voice_id = str(picked.get("id") or picked.get("voice_id") or "")
    return voice_id, {
        "clone_result": clone_result,
        "available_voices": available,
        "picked_voice": picked,
    }


def resolve_clone_voice_via_browser(
    voice_sample_path: Path,
    voice_name: str,
    slot_id: str,
) -> tuple[str, dict]:
    clone_result = create_clone_via_browser(
        voice_sample_path,
        slot_id=slot_id or None,
        voice_name=voice_name,
    )
    voice_id = extract_voice_id(clone_result)
    available = list_available_voices_via_browser()
    picked = pick_latest_clone_voice(available, preferred_name=voice_name or voice_sample_path.stem)
    if not voice_id and picked:
        voice_id = str(picked.get("id") or picked.get("voice_id") or "")
    return voice_id, {
        "clone_result": clone_result,
        "available_voices": available,
        "picked_voice": picked,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="One entry point for blueprint generation, optional authorized clone resolution, live rehearsal, and debrief.")
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--counterpart-role", required=True)
    parser.add_argument("--relationship", default="manager")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--desired-outcome", required=True)
    parser.add_argument("--fear-triggers", default="")
    parser.add_argument("--difficulty", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--voice-mode", choices=["proxy_voice", "authorized_clone"], default="proxy_voice")
    parser.add_argument("--voice-sample-path", default="")
    parser.add_argument("--authorized-voice-id", default="")
    parser.add_argument("--prepared-clone-voice-id", default="")
    parser.add_argument("--clone-consent", action="store_true")
    parser.add_argument("--create-clone", action="store_true")
    parser.add_argument("--clone-voice-name", default="")
    parser.add_argument("--clone-slot-id", default="")
    parser.add_argument("--user-audio-dir", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--asr-model", default=os.getenv("SENSEAUDIO_ASR_MODEL", "sense-asr-deepthink"))
    parser.add_argument("--stream-asr", action="store_true")
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
    parser.add_argument("--platform-token-env", default="SENSEAUDIO_PLATFORM_TOKEN")
    parser.add_argument("--max-user-turns", type=int, default=3)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    notes: list[str] = []
    clone_artifacts: dict = {}

    blueprint_path = outdir / "service_blueprint.json"
    build_args = [
        "--scenario", args.scenario,
        "--counterpart-role", args.counterpart_role,
        "--relationship", args.relationship,
        "--topic", args.topic,
        "--desired-outcome", args.desired_outcome,
        "--fear-triggers", args.fear_triggers,
        "--difficulty", args.difficulty,
        "--voice-mode", args.voice_mode,
        "--out-json", str(blueprint_path),
    ]
    if args.voice_sample_path:
        build_args.extend(["--voice-sample-path", args.voice_sample_path])
    prepared_clone_voice_id = args.prepared_clone_voice_id or args.authorized_voice_id
    if prepared_clone_voice_id:
        build_args.extend(["--authorized-voice-id", prepared_clone_voice_id])
    if args.clone_consent:
        build_args.append("--clone-consent")
    run_python(BUILD_BLUEPRINT, build_args, env)

    blueprint = load_json(blueprint_path)
    voice_policy = blueprint.setdefault("voice_policy", {})
    effective_voice_id = prepared_clone_voice_id or voice_policy.get("authorized_voice_id", "")
    if prepared_clone_voice_id:
        notes.append("Using a platform-prepared clone voice_id from the official clone flow.")

    if args.voice_mode == "authorized_clone" and not effective_voice_id:
        if args.create_clone and args.voice_sample_path and args.clone_consent:
            platform_token, token_source = resolve_platform_token(
                token_env=args.platform_token_env,
                allow_chrome=True,
            )
            if platform_token:
                try:
                    effective_voice_id, clone_artifacts = resolve_clone_voice(
                        platform_token,
                        Path(args.voice_sample_path),
                        args.clone_voice_name,
                        args.clone_slot_id,
                    )
                    if effective_voice_id:
                        notes.append(
                            f"Authorized clone resolved from SenseAudio workspace via {token_source}. "
                            "This workspace automation path is best-effort and not the public documented clone API flow."
                        )
                        voice_policy["authorized_voice_id"] = effective_voice_id
                    else:
                        notes.append("Clone request returned no usable voice id. Falling back to proxy voice.")
                        voice_policy["mode"] = "proxy_voice"
                except Exception as exc:
                    notes.append(f"Clone creation failed, falling back to proxy voice: {exc}")
                    voice_policy["mode"] = "proxy_voice"
            else:
                try:
                    effective_voice_id, clone_artifacts = resolve_clone_voice_via_browser(
                        Path(args.voice_sample_path),
                        args.clone_voice_name,
                        args.clone_slot_id,
                    )
                    if effective_voice_id:
                        notes.append(
                            "Authorized clone resolved through the logged-in Chrome browser session. "
                            "This browser-session path is best-effort and not the public documented clone API flow."
                        )
                        voice_policy["authorized_voice_id"] = effective_voice_id
                    else:
                        notes.append("Browser-session clone request returned no usable voice id. Falling back to proxy voice.")
                        voice_policy["mode"] = "proxy_voice"
                except Exception as exc:
                    notes.append(
                        "No platform token found and browser-session clone did not succeed. "
                        f"Falling back to proxy voice: {exc}"
                    )
                    voice_policy["mode"] = "proxy_voice"
        else:
            notes.append("No authorized voice id or clone creation input provided. Falling back to proxy voice.")
            voice_policy["mode"] = "proxy_voice"

    save_json(blueprint_path, blueprint)

    session_outdir = outdir / "session"
    session_args = [
        "--blueprint-json", str(blueprint_path),
        "--user-audio-dir", args.user_audio_dir,
        "--outdir", str(session_outdir),
        "--asr-model", args.asr_model,
        "--api-key-env", args.api_key_env,
        "--max-user-turns", str(args.max_user_turns),
        *(["--stream-asr"] if args.stream_asr else []),
        *(["--send-feishu-audio"] if args.send_feishu_audio else []),
        *(["--workspace-root", args.workspace_root] if args.workspace_root else []),
        *(["--chat-id", args.chat_id] if args.chat_id else []),
        *(["--session-file", args.session_file] if args.session_file else []),
        *(["--send-labels"] if args.send_labels else []),
        *(["--send-limit", str(args.send_limit)] if args.send_limit > 0 else []),
        *(["--send-turn-indexes", args.send_turn_indexes] if args.send_turn_indexes else []),
        *(["--delay-ms", str(args.send_delay_ms)] if args.send_delay_ms > 0 else []),
        *(["--ffmpeg-exe", args.ffmpeg_exe] if args.ffmpeg_exe else []),
    ]
    if effective_voice_id:
        session_args.extend(["--counterpart-voice-id", effective_voice_id])
    session_result = run_python(RUN_SESSION, session_args, env)

    summary = {
        "service": "senseaudio-conversation-rehearsal",
        "blueprint_json": str(blueprint_path),
        "session_output_dir": str(session_outdir),
        "session_result": session_result,
        "effective_voice_mode": blueprint.get("voice_policy", {}).get("mode"),
        "effective_voice_id": effective_voice_id,
        "stream_asr": args.stream_asr,
        "notes": notes,
        "clone_artifacts": clone_artifacts,
    }
    summary_path = outdir / "service_summary.json"
    save_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
