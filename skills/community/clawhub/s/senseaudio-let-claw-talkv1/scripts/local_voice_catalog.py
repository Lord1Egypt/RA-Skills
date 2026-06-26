#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, List, Optional


OFFICIAL_VOICES = [
    {"voice_id": "male_0004_a", "family": "male_0004", "name": "儒雅道长", "tier": "free", "emotion": "平稳", "tags": ["assistant", "serious", "neutral"]},
    {"voice_id": "male_0018_a", "family": "male_0018", "name": "沙哑青年", "tier": "free", "emotion": "深情", "tags": ["warm", "story"]},
    {"voice_id": "child_0001_a", "family": "child_0001", "name": "可爱萌娃", "tier": "free", "emotion": "开心", "tags": ["cheerful", "playful"]},
    {"voice_id": "child_0001_b", "family": "child_0001", "name": "可爱萌娃", "tier": "free", "emotion": "平稳", "tags": ["gentle", "neutral"]},
    {"voice_id": "male_0027_a", "family": "male_0027", "name": "亢奋主播", "tier": "trial", "emotion": "热情介绍", "tags": ["promo", "marketing"]},
    {"voice_id": "male_0027_b", "family": "male_0027", "name": "亢奋主播", "tier": "trial", "emotion": "卖点解读", "tags": ["promo", "sales"]},
    {"voice_id": "male_0027_c", "family": "male_0027", "name": "亢奋主播", "tier": "trial", "emotion": "促销逼单", "tags": ["sales", "conversion"]},
    {"voice_id": "male_0023_a", "family": "male_0023", "name": "撒娇青年", "tier": "trial", "emotion": "平稳", "tags": ["light", "playful"]},
    {"voice_id": "male_0019_a", "family": "male_0019", "name": "孔武青年", "tier": "paid", "emotion": "平稳", "tags": ["heroic", "strong"]},
    {"voice_id": "female_0006_a", "family": "female_0006", "name": "温柔御姐", "tier": "paid", "emotion": "深情", "tags": ["warm", "narration"]},
    {"voice_id": "female_0033_a", "family": "female_0033", "name": "嗲嗲台妹", "tier": "paid", "emotion": "平稳", "tags": ["lively", "neutral"]},
    {"voice_id": "female_0033_b", "family": "female_0033", "name": "嗲嗲台妹", "tier": "paid", "emotion": "开心", "tags": ["cheerful", "promo"]},
    {"voice_id": "female_0033_c", "family": "female_0033", "name": "嗲嗲台妹", "tier": "paid", "emotion": "撒娇", "tags": ["playful"]},
    {"voice_id": "female_0033_f", "family": "female_0033", "name": "嗲嗲台妹", "tier": "paid", "emotion": "生气", "tags": ["angry"]},
    {"voice_id": "male_0026_a", "family": "male_0026", "name": "乐观少年", "tier": "paid", "emotion": "平稳", "tags": ["neutral"]},
    {"voice_id": "male_0026_b", "family": "male_0026", "name": "乐观少年", "tier": "paid", "emotion": "开心", "tags": ["cheerful"]},
    {"voice_id": "male_0028_a", "family": "male_0028", "name": "可靠青叔", "tier": "paid", "emotion": "内容剖析", "tags": ["analytical", "briefing"]},
    {"voice_id": "male_0028_d", "family": "male_0028", "name": "可靠青叔", "tier": "paid", "emotion": "轻松铺陈", "tags": ["warm", "narration"]},
]


def load_clone_voices(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"voices": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"voices": {}}
    if not isinstance(data, dict):
        return {"voices": {}}
    voices = data.get("voices")
    if not isinstance(voices, dict):
        data["voices"] = {}
    return data


def save_clone_voices(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_custom_voice_entry(voice_id: str, *, name: str = "", source: str = "custom") -> Dict[str, object]:
    family = voice_id.split("_", 1)[0] if "_" in voice_id else voice_id.split("-", 1)[0]
    if voice_id.startswith("vc-"):
        family = "clone_voice"
    return {
        "voice_id": voice_id,
        "family": family or "custom",
        "name": name or ("Cloned Voice" if voice_id.startswith("vc-") else "Custom Voice"),
        "tier": "clone" if voice_id.startswith("vc-") else "custom",
        "emotion": "自定义",
        "tags": ["custom", "clone"] if voice_id.startswith("vc-") else ["custom"],
        "source": source,
    }


def upsert_clone_voice(clone_data: Dict[str, object], *, voice_id: str, name: str = "", source: str = "registered_clone") -> Dict[str, object]:
    voices = clone_data.setdefault("voices", {})
    if not isinstance(voices, dict):
        clone_data["voices"] = {}
        voices = clone_data["voices"]
    entry = voices.get(voice_id)
    if not isinstance(entry, dict):
        entry = {}
    entry["voice_id"] = voice_id
    entry["name"] = name or entry.get("name") or ("Cloned Voice" if voice_id.startswith("vc-") else "Custom Voice")
    entry["source"] = source
    voices[voice_id] = entry
    return entry


def all_voices(clone_data: Dict[str, object]) -> List[Dict[str, object]]:
    voices: List[Dict[str, object]] = list(OFFICIAL_VOICES)
    raw = clone_data.get("voices")
    if isinstance(raw, dict):
        for voice_id, payload in raw.items():
            if any(item["voice_id"] == voice_id for item in voices):
                continue
            if not isinstance(payload, dict):
                payload = {}
            voices.append(build_custom_voice_entry(voice_id, name=str(payload.get("name") or ""), source=str(payload.get("source") or "registered_clone")))
    return voices


def find_voice(query: str, clone_data: Dict[str, object]) -> Optional[Dict[str, object]]:
    query = str(query or "").strip().lower()
    if not query:
        return None
    for voice in all_voices(clone_data):
        haystack = " ".join(
            [
                str(voice.get("voice_id") or ""),
                str(voice.get("name") or ""),
                str(voice.get("family") or ""),
                str(voice.get("emotion") or ""),
                " ".join(str(item) for item in voice.get("tags", [])),
            ]
        ).lower()
        if query == str(voice.get("voice_id") or "").lower() or query in haystack:
            return voice
    return None
