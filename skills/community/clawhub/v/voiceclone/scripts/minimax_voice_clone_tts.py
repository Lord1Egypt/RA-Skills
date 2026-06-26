#!/usr/bin/env python3
"""
MiniMax voice clone + text to speech utility.

Flow:
1) Upload clone audio
2) Create cloned voice
3) (Optional) Synthesize text with cloned or existing voice
4) Write back cloned voice info to SKILL.md for future reuse
"""

from __future__ import annotations

import argparse
import binascii
import datetime as dt
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests

UPLOAD_URL = "https://api.minimax.io/v1/files/upload"
CLONE_URL = "https://api.minimax.io/v1/voice_clone"
TTS_URL = "https://api.minimax.io/v1/t2a_v2"

ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav"}
MAX_AUDIO_SIZE_BYTES = 20 * 1024 * 1024

VOICES_START = "<!-- CLONED_VOICES:START -->"
VOICES_END = "<!-- CLONED_VOICES:END -->"


class MiniMaxVoiceError(RuntimeError):
    """Domain-specific error for voice clone/tts operations."""


def _read_api_key() -> str:
    key = (
        os.getenv("MINIMAX_API_KEY")
        or os.getenv("MINIMAX_KEY")
        or os.getenv("MINIMAX_GROUP_API_KEY")
    )
    if not key:
        raise MiniMaxVoiceError(
            "Missing API key. Set MINIMAX_API_KEY (or MINIMAX_KEY / MINIMAX_GROUP_API_KEY)."
        )
    return key


def _auth_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


def _ensure_ok_base_resp(payload: Dict[str, Any], action: str) -> None:
    base_resp = payload.get("base_resp") or {}
    code = base_resp.get("status_code", 0)
    if code != 0:
        raise MiniMaxVoiceError(
            f"{action} failed: status_code={code}, status_msg={base_resp.get('status_msg', 'unknown')}"
        )


def _validate_audio_file(audio_path: Path) -> None:
    if not audio_path.is_file():
        raise MiniMaxVoiceError(f"Audio file not found: {audio_path}")

    if audio_path.suffix.lower() not in ALLOWED_AUDIO_EXTENSIONS:
        raise MiniMaxVoiceError(
            f"Unsupported audio format: {audio_path.suffix}. Allowed: {sorted(ALLOWED_AUDIO_EXTENSIONS)}"
        )

    size = audio_path.stat().st_size
    if size > MAX_AUDIO_SIZE_BYTES:
        raise MiniMaxVoiceError(
            f"Audio too large ({size} bytes). Max allowed is {MAX_AUDIO_SIZE_BYTES} bytes."
        )


def upload_clone_audio(api_key: str, audio_path: Path) -> int:
    _validate_audio_file(audio_path)

    with audio_path.open("rb") as f:
        files = {"file": (audio_path.name, f, "application/octet-stream")}
        data = {"purpose": "voice_clone"}
        resp = requests.post(
            UPLOAD_URL,
            headers=_auth_headers(api_key),
            data=data,
            files=files,
            timeout=120,
        )

    resp.raise_for_status()
    payload = resp.json()
    _ensure_ok_base_resp(payload, "upload clone audio")

    file_obj = payload.get("file") or {}
    file_id = file_obj.get("file_id")
    if file_id is None:
        raise MiniMaxVoiceError("Upload response missing file.file_id")
    return int(file_id)


def create_cloned_voice(
    api_key: str,
    file_id: int,
    voice_name: str,
    preview_text: Optional[str] = None,
) -> str:
    body: Dict[str, Any] = {"file_id": file_id, "voice_id": voice_name}
    if preview_text:
        body["text"] = preview_text

    headers = {"Content-Type": "application/json", **_auth_headers(api_key)}
    resp = requests.post(CLONE_URL, headers=headers, json=body, timeout=120)
    resp.raise_for_status()
    payload = resp.json()
    _ensure_ok_base_resp(payload, "create cloned voice")

    voice_id = payload.get("voice_id") or payload.get("data", {}).get("voice_id")
    if not voice_id:
        # Some APIs only return success in base_resp; fallback to user-provided id.
        voice_id = voice_name
    return str(voice_id)


def synthesize_speech(
    api_key: str,
    voice_id: str,
    text: str,
    output_path: Path,
    model: str = "speech-2.8-turbo",
    audio_format: str = "mp3",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    emotion: Optional[str] = None,
) -> Path:
    voice_setting: Dict[str, Any] = {
        "voice_id": voice_id,
        "speed": speed,
        "vol": vol,
        "pitch": pitch,
    }
    if emotion:
        voice_setting["emotion"] = emotion

    body: Dict[str, Any] = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": voice_setting,
        "audio_setting": {"format": audio_format},
        "output_format": "hex",
    }

    headers = {"Content-Type": "application/json", **_auth_headers(api_key)}
    resp = requests.post(TTS_URL, headers=headers, json=body, timeout=180)
    resp.raise_for_status()
    payload = resp.json()
    _ensure_ok_base_resp(payload, "text to speech")

    audio_hex = payload.get("data", {}).get("audio")
    if not audio_hex:
        raise MiniMaxVoiceError("TTS response missing data.audio")

    try:
        audio_bytes = binascii.unhexlify(audio_hex)
    except binascii.Error as exc:
        raise MiniMaxVoiceError(f"Failed to decode hex audio: {exc}") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_bytes)
    return output_path


def update_skill_registry(
    skill_md_path: Path, display_name: str, voice_id: str
) -> None:
    """Write or update one mapping: display_name (e.g. 中文名) -> voice_id."""
    if not skill_md_path.exists():
        return

    content = skill_md_path.read_text(encoding="utf-8")
    if VOICES_START not in content or VOICES_END not in content:
        return

    before, rest = content.split(VOICES_START, 1)
    middle, after = rest.split(VOICES_END, 1)

    def is_mapping_line(ln: str) -> bool:
        s = ln.strip()
        return s.startswith("- `") and "`: `" in s

    def parse_line(ln: str) -> tuple[str, str] | None:
        s = ln.strip()
        if not is_mapping_line(s):
            return None
        try:
            # "- `key`: `voice_id` (updated: ...)"
            after_dash = s[2:].strip()  # "`key`: `voice_id` ..."
            if not after_dash.startswith("`"):
                return None
            idx = after_dash.index("`: `")
            key = after_dash[1:idx].strip()
            rest = after_dash[idx + 4 :]
            end = rest.index("`")
            voice_id_val = rest[:end].strip()
            return (key, voice_id_val)
        except (ValueError, IndexError):
            return None

    rows = [ln for ln in middle.strip("\n").splitlines() if is_mapping_line(ln)]
    row_prefix = f"- `{display_name}`:"
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = f"- `{display_name}`: `{voice_id}` (updated: {now})"

    replaced = False
    for i, row in enumerate(rows):
        if row.strip().startswith(row_prefix):
            rows[i] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)

    # Sort by display name (case-insensitive for ASCII, natural for Chinese)
    rows_sorted = sorted(rows, key=lambda x: (parse_line(x) or ("", ""))[0].lower())
    rebuilt_middle = "\n".join(rows_sorted)
    rebuilt = (
        f"{before}{VOICES_START}\n"
        f"{rebuilt_middle}\n"
        f"{VOICES_END}{after}"
    )
    skill_md_path.write_text(rebuilt, encoding="utf-8")


def parse_skill_voices(skill_md_path: Path) -> Dict[str, str]:
    """Parse SKILL.md CLONED_VOICES block: return { display_name: voice_id }."""
    result: Dict[str, str] = {}
    if not skill_md_path.exists():
        return result
    content = skill_md_path.read_text(encoding="utf-8")
    if VOICES_START not in content or VOICES_END not in content:
        return result
    _, rest = content.split(VOICES_START, 1)
    middle, _ = rest.split(VOICES_END, 1)
    for ln in middle.strip("\n").splitlines():
        s = ln.strip()
        if not s.startswith("- `") or "`: `" not in s:
            continue
        try:
            after_dash = s[2:].strip()
            if not after_dash.startswith("`"):
                continue
            idx = after_dash.index("`: `")
            key = after_dash[1:idx].strip()
            rest_part = after_dash[idx + 4 :]
            end = rest_part.index("`")
            voice_id_val = rest_part[:end].strip()
            result[key] = voice_id_val
        except (ValueError, IndexError):
            continue
    return result


def resolve_voice_id(skill_md_path: Path, voice_key: str) -> str:
    """Resolve display name or voice_id to API voice_id. Prefer mapping key, then value, else pass through."""
    mapping = parse_skill_voices(skill_md_path)
    if voice_key in mapping:
        return mapping[voice_key]
    if voice_key in mapping.values():
        return voice_key
    return voice_key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload clone audio, create voice clone, optional TTS, and write voice mapping to SKILL.md."
        )
    )
    parser.add_argument("--audio", type=str, help="Path to clone audio file (mp3/m4a/wav)")
    parser.add_argument(
        "--voice-name",
        type=str,
        help="Required when cloning. API voice_id (e.g. yangtuo_demo_v1, letters/numbers/_-).",
    )
    parser.add_argument(
        "--display-name",
        type=str,
        help="Optional when cloning. Display name for SKILL mapping (e.g. 羊驼试听). Defaults to --voice-name.",
    )
    parser.add_argument(
        "--voice-id",
        type=str,
        help="TTS: use this API voice_id directly (skip clone and skip display-name lookup).",
    )
    parser.add_argument(
        "--voice",
        type=str,
        help="TTS: display name or voice_id; resolved from SKILL.md mapping (e.g. 羊驼试听 or yangtuo_demo_v1).",
    )
    parser.add_argument("--text", type=str, help="Text to synthesize. If omitted, only clone.")
    parser.add_argument(
        "--output",
        type=str,
        default="./output/minimax_tts.mp3",
        help="Output audio path for synthesis.",
    )
    parser.add_argument("--model", type=str, default="speech-2.8-turbo")
    parser.add_argument("--format", type=str, default="mp3", choices=["mp3", "pcm", "flac", "wav"])
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--vol", type=float, default=1.0)
    parser.add_argument("--pitch", type=int, default=0)
    parser.add_argument("--emotion", type=str, default=None)
    parser.add_argument(
        "--preview-text",
        type=str,
        default=None,
        help="Optional preview text used during clone creation.",
    )
    parser.add_argument(
        "--skill-md",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "SKILL.md"),
        help="Path to SKILL.md for writing back cloned voice mapping.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = _read_api_key()
    skill_md = Path(args.skill_md).expanduser().resolve()

    voice_id = args.voice_id
    if not voice_id and args.voice:
        voice_id = resolve_voice_id(skill_md, args.voice)

    if not voice_id:
        if not args.voice_name:
            raise MiniMaxVoiceError(
                "Cloning requires --voice-name. Please provide a user-defined voice name (API id)."
            )
        if not args.audio:
            raise MiniMaxVoiceError("Cloning requires --audio.")

        audio_path = Path(args.audio).expanduser().resolve()
        print(f"[1/3] Uploading clone audio: {audio_path}")
        file_id = upload_clone_audio(api_key, audio_path)
        print(f"Uploaded file_id: {file_id}")

        print(f"[2/3] Creating cloned voice: {args.voice_name}")
        voice_id = create_cloned_voice(api_key, file_id, args.voice_name, args.preview_text)
        print(f"Cloned voice_id: {voice_id}")

        registry_key = args.display_name if args.display_name else args.voice_name
        update_skill_registry(skill_md, registry_key, voice_id)
        print(f"Voice mapping written to: {skill_md} ({registry_key} -> {voice_id})")
    else:
        print(f"Using voice_id: {voice_id}")

    if args.text:
        if not voice_id:
            raise MiniMaxVoiceError(
                "TTS requires --voice-id or --voice (display name / voice_id from SKILL mapping)."
            )
        print("[3/3] Synthesizing speech...")
        output_path = Path(args.output).expanduser().resolve()
        out = synthesize_speech(
            api_key=api_key,
            voice_id=voice_id,
            text=args.text,
            output_path=output_path,
            model=args.model,
            audio_format=args.format,
            speed=args.speed,
            vol=args.vol,
            pitch=args.pitch,
            emotion=args.emotion,
        )
        print(f"TTS saved to: {out}")
    else:
        print("No --text provided; clone step completed.")


if __name__ == "__main__":
    main()
