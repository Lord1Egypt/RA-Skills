#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from zipfile import ZipFile

BASE_CN = "https://dashscope.aliyuncs.com/api/v1"
BASE_INTL = "https://dashscope-intl.aliyuncs.com/api/v1"
DEFAULT_OUTPUT_SUBDIR = "output"
DEFAULT_STATE_SUBDIR = ".state"
DEFAULT_USER_DATA_DIRNAME = "qwen-audio-lab"
VOICE_DB_NAME = "voices.json"
MAX_CLONE_AUDIO_BYTES = 20 * 1024 * 1024


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def skill_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def default_user_data_root() -> pathlib.Path:
    home = pathlib.Path.home()
    return home / ".openclaw" / "data" / DEFAULT_USER_DATA_DIRNAME


def output_dir() -> pathlib.Path:
    configured = os.getenv("QWEN_AUDIO_OUTPUT_DIR")
    root = pathlib.Path(configured).expanduser() if configured else default_user_data_root() / "output"
    root.mkdir(parents=True, exist_ok=True)
    return root


def state_dir() -> pathlib.Path:
    configured = os.getenv("QWEN_AUDIO_STATE_DIR")
    root = pathlib.Path(configured).expanduser() if configured else default_user_data_root() / "state"
    root.mkdir(parents=True, exist_ok=True)
    return root


def voice_db_path() -> pathlib.Path:
    return state_dir() / VOICE_DB_NAME


def load_voice_db() -> dict:
    path = voice_db_path()
    if not path.exists():
        legacy = skill_root() / VOICE_DB_NAME
        if legacy.exists():
            return json.loads(legacy.read_text(encoding="utf-8"))
        return {"voices": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_voice_db(data: dict) -> None:
    voice_db_path().write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remember_voice(entry: dict) -> None:
    data = load_voice_db()
    voices = [v for v in data.get("voices", []) if v.get("voice") != entry.get("voice")]
    voices.append(entry)
    data["voices"] = voices
    save_voice_db(data)


def remove_voice(voice: str) -> None:
    data = load_voice_db()
    data["voices"] = [v for v in data.get("voices", []) if v.get("voice") != voice]
    save_voice_db(data)


def base_url(region: str | None) -> str:
    resolved = (region or os.getenv("QWEN_AUDIO_REGION") or "cn").strip().lower()
    return BASE_INTL if resolved == "intl" else BASE_CN


def require_api_key() -> str:
    key = os.getenv("DASHSCOPE_API_KEY")
    if not key:
        fail("Missing DASHSCOPE_API_KEY. Use mac-say for local TTS or export a DashScope API key for Qwen features.")
    return key


def post_json(url: str, payload: dict, api_key: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"HTTP {exc.code} calling {url}: {body}")
    except urllib.error.URLError as exc:
        fail(f"Network error calling {url}: {exc}")


def validate_clone_audio(path: pathlib.Path) -> None:
    if not path.exists():
        fail(f"Audio file not found: {path}")
    size = path.stat().st_size
    if size > MAX_CLONE_AUDIO_BYTES:
        fail(f"Reference audio is too large ({size} bytes). Trim it to a shorter clean sample before cloning.")


def file_to_data_uri(path: pathlib.Path) -> str:
    validate_clone_audio(path)
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "audio/mpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def download_file(url: str, out_path: pathlib.Path) -> pathlib.Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    return out_path


def trim_audio_prefix(path: pathlib.Path, seconds: float) -> None:
    if seconds <= 0:
        return
    if not shutil.which("ffmpeg"):
        fail("ffmpeg is required for prefix trimming but was not found in PATH.")
    tmp_path = path.with_name(path.stem + '.trimmed' + path.suffix)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(path),
            "-af", f"atrim=start={seconds},afade=t=in:st=0:d=0.03",
            str(tmp_path),
        ],
        check=True,
    )
    tmp_path.replace(path)


def sanitize_name(value: str) -> str:
    out = []
    for ch in value:
        out.append(ch if ch.isalnum() or ch in ("-", "_", ".") else "-")
    cleaned = "".join(out).strip("-")
    return cleaned or f"audio-{int(time.time())}"


def load_text_from_args(args: argparse.Namespace) -> str:
    sources = [
        bool(getattr(args, "text", None)),
        bool(getattr(args, "text_file", None)),
        bool(getattr(args, "stdin", False)),
    ]
    if sum(sources) != 1:
        fail("Provide exactly one of --text, --text-file, or --stdin.")
    if getattr(args, "text", None):
        text = args.text
    elif getattr(args, "text_file", None):
        text = pathlib.Path(args.text_file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        fail("Input text is empty.")
    return text


def cmd_mac_say(args: argparse.Namespace) -> None:
    text = load_text_from_args(args)
    cmd = ["say"]
    if args.voice:
        cmd.extend(["-v", args.voice])
    if args.rate:
        cmd.extend(["-r", str(args.rate)])
    cmd.append(text)
    subprocess.run(cmd, check=True)
    print("Played with macOS say")


def extract_audio_url(resp: dict) -> str:
    output = resp.get("output", {})
    audio = output.get("audio", {}) if isinstance(output, dict) else {}
    url = audio.get("url")
    if not url:
        fail(f"No audio URL returned: {json.dumps(resp, ensure_ascii=False)}")
    return url


def cmd_qwen_tts(args: argparse.Namespace) -> None:
    api_key = require_api_key()
    text = load_text_from_args(args)
    payload = {
        "model": args.model,
        "input": {
            "text": text,
            "voice": args.voice,
            "language_type": args.language_type,
        },
    }
    url = base_url(args.region) + "/services/aigc/multimodal-generation/generation"
    resp = post_json(url, payload, api_key)
    audio_url = extract_audio_url(resp)
    result = {"audio_url": audio_url}
    if args.download:
        ext = args.format or "wav"
        filename = args.output or f"{sanitize_name(args.voice)}-{int(time.time())}.{ext}"
        path = output_dir() / filename
        download_file(audio_url, path)
        result["file"] = str(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_clone_voice(args: argparse.Namespace) -> None:
    api_key = require_api_key()
    audio_path = pathlib.Path(args.audio).expanduser()
    payload = {
        "model": "qwen-voice-enrollment",
        "input": {
            "action": "create",
            "target_model": args.target_model,
            "preferred_name": args.name,
            "audio": {"data": file_to_data_uri(audio_path)},
        },
    }
    url = base_url(args.region) + "/services/audio/tts/customization"
    resp = post_json(url, payload, api_key)
    voice = resp.get("output", {}).get("voice")
    if not voice:
        fail(f"No voice returned: {json.dumps(resp, ensure_ascii=False)}")
    entry = {
        "voice": voice,
        "kind": "cloned",
        "source_audio": str(audio_path),
        "target_model": args.target_model,
        "preferred_name": args.name,
        "created_at": int(time.time()),
        "region": args.region or os.getenv("QWEN_AUDIO_REGION") or "cn",
    }
    remember_voice(entry)
    print(json.dumps(entry, ensure_ascii=False, indent=2))


def cmd_design_voice(args: argparse.Namespace) -> None:
    api_key = require_api_key()
    payload = {
        "model": "qwen-voice-design",
        "input": {
            "action": "create",
            "target_model": args.target_model,
            "preferred_name": args.name,
            "voice_prompt": args.prompt,
            "response_format": args.preview_format,
        },
    }
    url = base_url(args.region) + "/services/audio/tts/customization"
    resp = post_json(url, payload, api_key)
    output = resp.get("output", {})
    voice = output.get("voice")
    if not voice:
        fail(f"No voice returned: {json.dumps(resp, ensure_ascii=False)}")
    entry = {
        "voice": voice,
        "kind": "designed",
        "target_model": args.target_model,
        "preferred_name": args.name,
        "prompt": args.prompt,
        "created_at": int(time.time()),
        "region": args.region or os.getenv("QWEN_AUDIO_REGION") or "cn",
    }
    preview_url = output.get("audio", {}).get("url") if isinstance(output, dict) else None
    if preview_url:
        filename = f"{sanitize_name(voice)}-preview.{args.preview_format}"
        path = output_dir() / filename
        download_file(preview_url, path)
        entry["preview_file"] = str(path)
        entry["preview_url"] = preview_url
    remember_voice(entry)
    print(json.dumps(entry, ensure_ascii=False, indent=2))


def cmd_delete_voice(args: argparse.Namespace) -> None:
    api_key = require_api_key()
    payload = {
        "model": "qwen-voice-enrollment",
        "input": {
            "action": "delete",
            "voice": args.voice,
        },
    }
    url = base_url(args.region) + "/services/audio/tts/customization"
    resp = post_json(url, payload, api_key)
    remove_voice(args.voice)
    print(json.dumps({"deleted": args.voice, "response": resp}, ensure_ascii=False, indent=2))


def cmd_list_voices(args: argparse.Namespace) -> None:
    print(json.dumps(load_voice_db(), ensure_ascii=False, indent=2))


def latest_voice(kind: str | None = None) -> dict:
    voices = load_voice_db().get("voices", [])
    if kind:
        voices = [v for v in voices if v.get("kind") == kind]
    if not voices:
        fail("No remembered voices found. Clone or design a voice first.")
    voices.sort(key=lambda v: v.get("created_at", 0), reverse=True)
    return voices[0]


def resolve_voice_config(selection: str, explicit_voice: str | None, explicit_model: str | None) -> tuple[str, str | None]:
    if explicit_voice:
        return explicit_voice, explicit_model
    normalized = (selection or "last-cloned").strip().lower()
    if normalized == "last-cloned":
        voice = latest_voice("cloned")
        return voice["voice"], explicit_model or voice["target_model"]
    if normalized == "last-designed":
        voice = latest_voice("designed")
        return voice["voice"], explicit_model or voice["target_model"]
    return selection, explicit_model


def cmd_speak_last_cloned(args: argparse.Namespace) -> None:
    voice = latest_voice("cloned")
    payload = argparse.Namespace(
        text=args.text,
        text_file=args.text_file,
        stdin=args.stdin,
        voice=voice["voice"],
        model=voice["target_model"],
        language_type=args.language_type,
        region=args.region or voice.get("region"),
        download=args.download,
        output=args.output,
        format=args.format,
    )
    cmd_qwen_tts(payload)


def cmd_narrate_text(args: argparse.Namespace) -> None:
    voice_name, model_name = resolve_voice_config(args.voice_source, args.voice, args.model)
    payload = argparse.Namespace(
        text=args.text,
        text_file=args.text_file,
        stdin=args.stdin,
        voice=voice_name,
        model=model_name or "qwen3-tts-flash",
        language_type=args.language_type,
        region=args.region,
        download=True,
        output=args.output,
        format=args.format,
    )
    cmd_qwen_tts(payload)


def cmd_narrate_file(args: argparse.Namespace) -> None:
    if args.text or args.stdin:
        fail("narrate-file only accepts --text-file.")
    if not args.text_file:
        fail("Provide --text-file for narrate-file.")
    voice_name, model_name = resolve_voice_config(args.voice_source, args.voice, args.model)
    output_name = args.output
    if not output_name:
        stem = sanitize_name(pathlib.Path(args.text_file).expanduser().stem)
        output_name = f"{stem}.{args.format}"
    payload = argparse.Namespace(
        text=None,
        text_file=args.text_file,
        stdin=False,
        voice=voice_name,
        model=model_name or "qwen3-tts-flash",
        language_type=args.language_type,
        region=args.region,
        download=True,
        output=output_name,
        format=args.format,
    )
    cmd_qwen_tts(payload)


def cmd_show_last_voice(args: argparse.Namespace) -> None:
    voice = latest_voice(args.kind)
    print(json.dumps(voice, ensure_ascii=False, indent=2))


def split_text_by_utf8_bytes(text: str, max_bytes: int = 500) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    units = [u.strip() for u in re.split(r"(?<=[。！？；.!?;])", cleaned) if u.strip()]
    chunks = []
    cur = ""

    def size(s: str) -> int:
        return len(s.encode("utf-8"))

    for u in units:
        if size(u) > max_bytes:
            piece = ""
            for ch in u:
                if size(piece + ch) <= max_bytes:
                    piece += ch
                else:
                    if cur:
                        chunks.append(cur)
                        cur = ""
                    if piece:
                        chunks.append(piece)
                    piece = ch
            if piece:
                if cur:
                    chunks.append(cur)
                    cur = ""
                chunks.append(piece)
            continue
        candidate = u if not cur else cur + " " + u
        if size(candidate) <= max_bytes:
            cur = candidate
        else:
            if cur:
                chunks.append(cur)
            cur = u
    if cur:
        chunks.append(cur)
    return chunks


def extract_ppt_notes(ppt_path: str) -> list[tuple[int, str]]:
    path = pathlib.Path(ppt_path).expanduser()
    if not path.exists():
        fail(f"PPT file not found: {path}")
    slides = []
    with ZipFile(path) as z:
        note_files = sorted(
            [name for name in z.namelist() if name.startswith("ppt/notesSlides/notesSlide") and name.endswith(".xml")]
        )
        for name in note_files:
            match = re.search(r"notesSlide(\d+)\.xml$", name)
            if not match:
                continue
            slide_no = int(match.group(1))
            data = z.read(name).decode("utf-8", "ignore")
            parts = re.findall(r"<a:t>(.*?)</a:t>", data)
            cleaned_parts = []
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if part in {"‹#›", "[#]"}:
                    continue
                if re.fullmatch(r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}", part):
                    continue
                cleaned_parts.append(part)
            if not cleaned_parts:
                continue
            text = "\n".join(cleaned_parts)
            text = text.replace("‹#›", " ").replace("“", '"').replace("”", '"')
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                slides.append((slide_no, text))
    return sorted(slides, key=lambda item: item[0])


def narrate_ppt_with_voice(args: argparse.Namespace, voice_name: str, model_name: str, region: str | None) -> None:
    slides = extract_ppt_notes(args.ppt)
    if not slides:
        fail("No PPT notes found.")
    base = output_dir()
    deck_name = sanitize_name(pathlib.Path(args.ppt).stem)
    per_slide_dir = base / f"{deck_name}-slides"
    per_slide_dir.mkdir(parents=True, exist_ok=True)
    created = []
    for slide_no, text in slides:
        chunks = split_text_by_utf8_bytes(text, max_bytes=args.max_bytes)
        if not chunks:
            continue
        chunk_files = []
        for idx, chunk in enumerate(chunks, 1):
            name = f"slide-{slide_no:02d}-chunk-{idx:02d}.wav"
            payload = argparse.Namespace(
                text=chunk,
                text_file=None,
                stdin=False,
                voice=voice_name,
                model=model_name,
                language_type=args.language_type,
                region=region,
                download=True,
                output=name,
                format="wav",
            )
            cmd_qwen_tts(payload)
            src = output_dir() / name
            dst = per_slide_dir / name
            if src.exists():
                src.replace(dst)
            if args.trim_leading_seconds > 0:
                trim_audio_prefix(dst, args.trim_leading_seconds)
            chunk_files.append(dst)
        final = per_slide_dir / f"slide-{slide_no:02d}.wav"
        if len(chunk_files) == 1:
            if final.exists():
                final.unlink()
            chunk_files[0].replace(final)
        else:
            concat = per_slide_dir / f"slide-{slide_no:02d}-concat.txt"
            concat.write_text("".join([f"file '{f.as_posix()}'\n" for f in chunk_files]), encoding="utf-8")
            subprocess.run(
                ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(final)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not args.keep_fragments:
                concat.unlink(missing_ok=True)
        if not args.keep_fragments:
            for chunk_file in chunk_files:
                chunk_file.unlink(missing_ok=True)
        created.append(str(final))
    print(json.dumps({"voice": voice_name, "files": created}, ensure_ascii=False, indent=2))


def cmd_ppt_own_voice(args: argparse.Namespace) -> None:
    voice = latest_voice("cloned")
    narrate_ppt_with_voice(args, voice["voice"], voice["target_model"], args.region or voice.get("region"))


def cmd_narrate_ppt(args: argparse.Namespace) -> None:
    voice_name, model_name = resolve_voice_config(args.voice_source, args.voice, args.model)
    narrate_ppt_with_voice(args, voice_name, model_name or "qwen3-tts-flash", args.region)

def add_text_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text")
    parser.add_argument("--text-file")
    parser.add_argument("--stdin", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid macOS + Qwen audio helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("mac-say", help="Use macOS say for local playback")
    add_text_source_args(p)
    p.add_argument("--voice")
    p.add_argument("--rate", type=int)
    p.set_defaults(func=cmd_mac_say)

    p = sub.add_parser("qwen-tts", help="Use Qwen TTS and optionally download audio")
    add_text_source_args(p)
    p.add_argument("--voice", required=True)
    p.add_argument("--model", default="qwen3-tts-flash")
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--download", action="store_true")
    p.add_argument("--output")
    p.add_argument("--format", choices=["wav", "mp3"], default="wav")
    p.set_defaults(func=cmd_qwen_tts)

    p = sub.add_parser("clone-voice", help="Clone a voice from a reference audio file")
    p.add_argument("--audio", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--target-model", default="qwen3-tts-vc-2026-01-22")
    p.add_argument("--region", choices=["cn", "intl"])
    p.set_defaults(func=cmd_clone_voice)

    p = sub.add_parser("design-voice", help="Create a custom voice from a text prompt")
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--target-model", default="qwen3-tts-vd-2026-01-26")
    p.add_argument("--preview-format", choices=["wav", "mp3"], default="wav")
    p.add_argument("--region", choices=["cn", "intl"])
    p.set_defaults(func=cmd_design_voice)

    p = sub.add_parser("delete-voice", help="Delete a custom Qwen voice")
    p.add_argument("--voice", required=True)
    p.add_argument("--region", choices=["cn", "intl"])
    p.set_defaults(func=cmd_delete_voice)

    p = sub.add_parser("list-voices", help="List locally remembered custom voices")
    p.set_defaults(func=cmd_list_voices)

    p = sub.add_parser("speak-last-cloned", help="Speak with the most recently cloned voice")
    add_text_source_args(p)
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--download", action="store_true")
    p.add_argument("--output")
    p.add_argument("--format", choices=["wav", "mp3"], default="wav")
    p.set_defaults(func=cmd_speak_last_cloned)

    p = sub.add_parser("narrate-text", help="High-level narration from inline text, file text, or stdin")
    add_text_source_args(p)
    p.add_argument("--voice-source", default="last-cloned", help="last-cloned, last-designed, or a literal voice id")
    p.add_argument("--voice", help="Explicit voice id overrides --voice-source")
    p.add_argument("--model", help="Explicit synthesis model")
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--output")
    p.add_argument("--format", choices=["wav", "mp3"], default="wav")
    p.set_defaults(func=cmd_narrate_text)

    p = sub.add_parser("narrate-file", help="High-level narration from a text file")
    add_text_source_args(p)
    p.add_argument("--voice-source", default="last-cloned", help="last-cloned, last-designed, or a literal voice id")
    p.add_argument("--voice", help="Explicit voice id overrides --voice-source")
    p.add_argument("--model", help="Explicit synthesis model")
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--output")
    p.add_argument("--format", choices=["wav", "mp3"], default="wav")
    p.set_defaults(func=cmd_narrate_file)

    p = sub.add_parser("show-last-voice", help="Show the most recently remembered voice")
    p.add_argument("--kind", choices=["cloned", "designed"])
    p.set_defaults(func=cmd_show_last_voice)

    p = sub.add_parser("ppt-own-voice", help="Extract PPT notes and narrate them with the most recent cloned voice")
    p.add_argument("--ppt", required=True)
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--max-bytes", type=int, default=900)
    p.add_argument("--trim-leading-seconds", type=float, default=0.0)
    p.add_argument("--keep-fragments", action="store_true")
    p.set_defaults(func=cmd_ppt_own_voice)

    p = sub.add_parser("narrate-ppt", help="High-level PPT speaker-note narration")
    p.add_argument("--ppt", required=True)
    p.add_argument("--voice-source", default="last-cloned", help="last-cloned, last-designed, or a literal voice id")
    p.add_argument("--voice", help="Explicit voice id overrides --voice-source")
    p.add_argument("--model", help="Explicit synthesis model")
    p.add_argument("--language-type", default="Chinese")
    p.add_argument("--region", choices=["cn", "intl"])
    p.add_argument("--max-bytes", type=int, default=900)
    p.add_argument("--trim-leading-seconds", type=float, default=0.0)
    p.add_argument("--keep-fragments", action="store_true")
    p.set_defaults(func=cmd_narrate_ppt)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
