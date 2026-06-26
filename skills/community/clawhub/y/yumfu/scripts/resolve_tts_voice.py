#!/usr/bin/env python3
"""
Resolve YumFu per-save TTS settings and stable voice selection.

Goals:
- Default TTS to enabled for gameplay turns unless explicitly disabled
- Keep one stable voice per language within the same save
- Allow explicit user-requested voice override
- Pick language/world-appropriate Edge/Azure-compatible voice ids

Usage:
  python3 resolve_tts_voice.py --user-id 1309815719 --universe game-of-thrones --language en
  python3 resolve_tts_voice.py --user-id 1309815719 --universe xiaoao --language zh --force-voice zh-CN-XiaoxiaoNeural
  python3 resolve_tts_voice.py --user-id 1309815719 --universe lotr --language en --tts off
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Any


SAVE_ROOT = Path.home() / "clawd" / "memory" / "yumfu" / "saves"


EN_WORLD_DEFAULTS = {
    "game-of-thrones": "en-GB-SoniaNeural",   # political / dark fantasy
    "lotr": "en-GB-RyanNeural",               # epic fantasy male narrator
    "harry-potter": "en-GB-SoniaNeural",      # British school fantasy
    "warrior-cats": "en-US-AriaNeural",       # expressive adventure
    "f15-down": "en-US-GuyNeural",            # crisp tactical briefings
}

ZH_WORLD_DEFAULTS = {
    "xiaoao": "zh-CN-XiaoxiaoNeural",         # wuxia narration
    "yitian": "zh-CN-XiaoxiaoNeural",         # wuxia / romance tension
    "sengoku": "zh-CN-XiaoyiNeural",          # dramatic, slightly lively alt-history
    "journey-to-west": "zh-CN-XiaoyiNeural",  # playful mythic energy
    "lobster-sanguo": "zh-TW-HsiaoChenNeural",# humorous / strategic
    "captain-underpants": "zh-CN-XiaoyiNeural"# chaotic comedy
}

GENERIC_DEFAULTS = {
    "en": "en-US-AriaNeural",
    "zh": "zh-TW-HsiaoChenNeural",
}


def normalize_lang(value: str | None) -> str:
    if not value:
        return "en"
    v = value.lower().strip()
    if v.startswith("zh") or "chinese" in v or value in {"中文", "汉语", "國語"}:
        return "zh"
    return "en"


def save_path(user_id: str, universe: str) -> Path:
    return SAVE_ROOT / universe / f"user-{user_id}.json"


def load_save(user_id: str, universe: str) -> Dict[str, Any]:
    path = save_path(user_id, universe)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def default_voice(universe: str, language: str) -> str:
    language = normalize_lang(language)
    if language == "zh":
        return ZH_WORLD_DEFAULTS.get(universe, GENERIC_DEFAULTS[language])
    return EN_WORLD_DEFAULTS.get(universe, GENERIC_DEFAULTS[language])


def resolve(user_id: str, universe: str, language: str, force_voice: str | None = None, tts: str | None = None) -> Dict[str, Any]:
    save = load_save(user_id, universe)
    lang = normalize_lang(language or save.get("language"))

    existing = save.get("tts") or {}
    language_voices = dict(existing.get("language_voices") or {})
    last_language = normalize_lang(existing.get("last_language") or lang)

    if force_voice:
        chosen = force_voice
        reason = "user_override"
        language_voices[lang] = chosen
    elif language_voices.get(lang):
        chosen = language_voices[lang]
        reason = "locked_for_language"
    else:
        chosen = default_voice(universe, lang)
        reason = "world_language_default"
        language_voices[lang] = chosen

    if tts == "on":
        enabled = True
    elif tts == "off":
        enabled = False
    elif isinstance(existing.get("enabled"), bool):
        enabled = existing["enabled"]
    else:
        enabled = True  # new default required by user

    style_hint = (
        "voice bubble, warm/dramatic Chinese narration" if lang == "zh"
        else "voice bubble, immersive English narration"
    )

    payload = {
        "enabled": enabled,
        "provider": existing.get("provider") or "edge-tts",
        "delivery": "voice-bubble",
        "language_voices": language_voices,
        "current_voice": chosen,
        "last_language": lang,
        "style_hint": style_hint,
        "switch_policy": "keep same voice for same language within one save unless user explicitly asks to change",
        "reason": reason,
    }

    return {
        "user_id": user_id,
        "universe": universe,
        "language": lang,
        "save_exists": bool(save),
        "tts": payload,
        "save_patch": {
            "tts": payload,
        },
        "voice_changed": chosen != existing.get("current_voice"),
        "language_changed": lang != last_language,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve YumFu TTS voice settings")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--universe", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--force-voice")
    parser.add_argument("--tts", choices=["on", "off"])
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    result = resolve(
        user_id=args.user_id,
        universe=args.universe,
        language=args.language,
        force_voice=args.force_voice,
        tts=args.tts,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
