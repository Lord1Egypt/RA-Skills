#!/usr/bin/env python3
"""
Prepare YumFu daily evolution delivery assets.

This bridges the current gap where daily evolution cron jobs deliver image+text
but forget to consistently generate/send TTS.

What it does:
- loads a generated daily evolution JSON payload
- derives stable language
- prepares delivery state
- reuses an existing generated image if one is already present
- otherwise tries local image generation from image_prompt
- generates TTS using the same per-save TTS workflow as regular YumFu turns
- returns a structured delivery plan for the caller (agent / cron task)

What it does NOT do:
- no direct OpenClaw tool calls
- no direct message sending
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from turn_delivery_state import load as load_state
from turn_delivery_state import save as save_state

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATE_IMAGE = SCRIPT_DIR / "generate_image.py"
GENERATE_TTS = SCRIPT_DIR / "generate_turn_tts.py"
OUTBOUND_YUMFU = Path.home() / ".openclaw" / "media" / "outbound" / "yumfu"
SAVE_DIR = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'saves'


def load_save_language(user_id: str, universe: str) -> str | None:
    path = SAVE_DIR / universe / f'user-{user_id}.json'
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None
    lang = str(data.get('language') or '').strip().lower()
    if lang.startswith('zh') or lang in {'cn', 'chinese', '中文'}:
        return 'zh'
    if lang.startswith('en') or lang == 'english':
        return 'en'
    return None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "turn"


def run_json(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {
            "success": False,
            "error": proc.stderr.strip() or proc.stdout.strip() or f"command failed ({proc.returncode})",
            "command": cmd,
        }
    stdout = proc.stdout.strip()
    if not stdout:
        return {"success": False, "error": "empty stdout", "command": cmd}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "stdout was not valid JSON",
            "stdout": stdout,
            "command": cmd,
        }


def run_proc(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "command": cmd,
    }


def detect_language(payload: dict[str, Any], explicit: str | None, save_language: str | None) -> str:
    if explicit:
        return explicit
    if save_language:
        return save_language
    delivered = (payload.get("delivered_text") or "").strip()
    text = delivered or (payload.get("story_text") or "")
    if any("\u4e00" <= ch <= "\u9fff" for ch in text):
        return "zh"
    return "en"


def compose_delivery_text(payload: dict[str, Any], language: str) -> str:
    recap = (payload.get("recap_text") or "").strip()
    story = (payload.get("delivered_text") or payload.get("story_text") or "").strip()
    if recap:
        if language == "zh":
            return f"前情：{recap}\n\n今日推进：{story}".strip()
        return f"Previously: {recap}\n\nToday: {story}".strip()
    return story


def plan_caption(story_text: str) -> tuple[str, str | None, str]:
    clean = " ".join(story_text.split())
    if len(clean) <= 900:
        return clean, None, "caption-only"
    short = clean[:220]
    if " " in short:
        short = short.rsplit(" ", 1)[0]
    short = short.rstrip(".,;:!?") + "…"
    return short, story_text.strip(), "caption+followup"


def existing_image(payload: dict[str, Any]) -> str | None:
    p = payload.get("generated_image_path")
    if p and Path(p).exists():
        return str(Path(p))
    return None


def prepare_image(user_id: str, universe: str, turn_id: str, image_prompt: str | None, state: dict[str, Any], reuse_path: str | None) -> dict[str, Any]:
    if state.get("image_sent"):
        return {
            "generated": False,
            "skipped": True,
            "reason": "image_already_sent",
            "needs_fallback": False,
        }
    if reuse_path:
        return {
            "generated": True,
            "reused": True,
            "path": reuse_path,
            "provider": "pre-generated",
            "needs_fallback": False,
        }
    if not image_prompt:
        return {
            "generated": False,
            "skipped": True,
            "reason": "no_image_prompt",
            "needs_fallback": False,
        }

    OUTBOUND_YUMFU.mkdir(parents=True, exist_ok=True)
    filename = OUTBOUND_YUMFU / f"{universe}-user-{user_id}-{slugify(turn_id)}.png"
    result = run_proc([
        "uv",
        "run",
        str(GENERATE_IMAGE),
        "--prompt",
        image_prompt,
        "--filename",
        str(filename),
        "--resolution",
        "1K",
        "--aspect-ratio",
        "4:5",
    ])
    if result["success"] and filename.exists():
        return {
            "generated": True,
            "reused": False,
            "path": str(filename),
            "provider": "local-yumfu",
            "needs_fallback": False,
            "stdout": result["stdout"],
        }
    return {
        "generated": False,
        "path": str(filename),
        "provider": "local-yumfu",
        "needs_fallback": True,
        "error": result["stderr"] or result["stdout"] or "local image generation failed",
    }


def prepare_tts(user_id: str, universe: str, language: str, story_text: str, state: dict[str, Any]) -> dict[str, Any]:
    if state.get("tts_sent"):
        return {
            "generated": False,
            "skipped": True,
            "reason": "tts_already_sent",
        }
    if not story_text.strip():
        return {
            "generated": False,
            "skipped": True,
            "reason": "no_story_text",
        }
    return run_json([
        "uv",
        "run",
        str(GENERATE_TTS),
        "--user-id",
        user_id,
        "--universe",
        universe,
        "--language",
        language,
        "--text",
        story_text,
    ])


def extract_turn_stamp(payload: dict[str, Any], json_path: Path) -> str:
    for key in ("generated_at", "timestamp"):
        value = str(payload.get(key) or "").strip()
        if not value:
            continue
        try:
            normalized = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalized)
            return dt.strftime("%Y%m%d")
        except ValueError:
            pass

    value = str(payload.get("date") or "").strip()
    if value:
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", value)
        if match:
            return "".join(match.groups())
        match = re.search(r"(\d{8})", value)
        if match:
            return match.group(1)

    try:
        return datetime.fromtimestamp(json_path.stat().st_mtime).strftime("%Y%m%d")
    except OSError:
        return datetime.now().strftime("%Y%m%d")



def derive_turn_id(payload: dict[str, Any], json_path: Path, explicit_turn_id: str | None, universe: str) -> str:
    if explicit_turn_id:
        return explicit_turn_id
    world_id = payload.get("world_id", universe)
    stamp = extract_turn_stamp(payload, json_path)
    return f"daily-evolution-{world_id}-{json_path.stem}-{stamp}"



def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare YumFu daily evolution delivery assets")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--universe", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--json", dest="json_path", required=True, help="Path to generated daily evolution json")
    parser.add_argument("--turn-id")
    parser.add_argument("--language")
    args = parser.parse_args()

    json_path = Path(args.json_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    save_language = load_save_language(args.user_id, args.universe)
    language = detect_language(payload, args.language, save_language)
    story_text = compose_delivery_text(payload, language)
    turn_id = derive_turn_id(payload, json_path, args.turn_id, args.universe)

    state = load_state(args.user_id, args.universe, turn_id)
    state["chat_id"] = args.target
    save_state(state)

    caption, followup_text, text_mode = plan_caption(story_text)
    image = prepare_image(
        user_id=args.user_id,
        universe=args.universe,
        turn_id=turn_id,
        image_prompt=payload.get("image_prompt"),
        state=state,
        reuse_path=existing_image(payload),
    )
    tts = prepare_tts(
        user_id=args.user_id,
        universe=args.universe,
        language=language,
        story_text=story_text,
        state=state,
    )

    result = {
        "success": True,
        "kind": "daily-evolution-delivery",
        "turn_id": turn_id,
        "user_id": args.user_id,
        "universe": args.universe,
        "target": args.target,
        "language": language,
        "save_language": save_language,
        "delivery_state": state,
        "source_payload": payload,
        "story": {
            "caption": caption,
            "followup_text": followup_text,
            "mode": text_mode,
            "full_text": story_text,
            "summary": payload.get("summary"),
            "recap_text": payload.get("recap_text"),
            "hooks": payload.get("hooks") or [],
        },
        "image": image,
        "tts": tts,
        "next_actions": {
            "send_image_with_caption": bool(image.get("generated")),
            "fallback_to_openclaw_image_generate": bool(image.get("needs_fallback")),
            "send_text_followup": bool(followup_text),
            "send_tts_voice": bool(tts.get("success") and tts.get("generated")),
            "mark_main_text_sent_after_success": True,
            "mark_image_sent_after_success": bool(image.get("generated")),
            "mark_tts_sent_after_success": bool(tts.get("success") and tts.get("generated")),
        },
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
