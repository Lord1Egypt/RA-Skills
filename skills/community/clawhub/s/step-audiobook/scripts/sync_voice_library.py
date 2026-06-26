#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_LIBRARY_PATH,
    ensure_dir,
    is_relative_to,
    load_json,
    load_json_if_exists,
    load_yaml,
    resolve_path,
    resolve_step_api_key,
    save_json,
    save_yaml,
    sha256_file,
    trim_string,
)


CHAT_COMPLETIONS_URL = "https://api.stepfun.com/v1/chat/completions"
SYSTEM_VOICES_URL = "https://api.stepfun.com/v1/audio/system_voices"


def create_voice_registry() -> dict[str, Any]:
    return {
        "version": "1",
        "updated_at": datetime.fromtimestamp(0).isoformat() + "Z",
        "assets": {},
    }


def load_voice_registry(registry_path: str | Path) -> dict[str, Any]:
    parsed = load_json_if_exists(registry_path, create_voice_registry())
    if not isinstance(parsed, dict) or not isinstance(parsed.get("assets"), dict):
        return create_voice_registry()
    return {
        "version": str(parsed.get("version") or "1"),
        "updated_at": parsed.get("updated_at") or datetime.fromtimestamp(0).isoformat() + "Z",
        "assets": parsed.get("assets") or {},
    }


def save_voice_registry(registry_path: str | Path, registry: dict[str, Any]) -> None:
    payload = {
        **registry,
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    save_json(registry_path, payload)


def create_review_store() -> dict[str, Any]:
    return {
        "version": "1",
        "generated_at": "",
        "clones": {},
    }


def load_review_store(review_path: str | Path) -> dict[str, Any]:
    data = load_yaml(review_path) if Path(review_path).exists() else create_review_store()
    return {
        "version": str(data.get("version") or "1"),
        "generated_at": data.get("generated_at") or "",
        "clones": data.get("clones") or {},
    }


def decode_sample_audio(sample_audio: str | None) -> bytes | None:
    if not isinstance(sample_audio, str):
        return None
    normalized = sample_audio.strip()
    if not normalized:
        return None
    if normalized.startswith("data:"):
        parts = normalized.split(",", 1)
        if len(parts) != 2 or not parts[1]:
            return None
        return base64.b64decode(parts[1])
    try:
        data = base64.b64decode(normalized)
        return data or None
    except Exception:
        return None


def write_sample_preview(preview_dir: str | Path, asset_id: str, sample_audio: str | None) -> str:
    decoded = decode_sample_audio(sample_audio)
    if not decoded:
        return ""
    preview_dir_path = Path(preview_dir)
    ensure_dir(preview_dir_path)
    preview_path = preview_dir_path / f"{asset_id}.preview.wav"
    preview_path.write_bytes(decoded)
    return str(preview_path)


def split_scenes(text: Any) -> list[str]:
    input_text = str(text or "").strip()
    if not input_text:
        return []

    parts: list[str] = []
    buffer: list[str] = []
    depth = 0

    for char in input_text:
        if re.search(r"[\(\[（【]", char):
            depth += 1
            buffer.append(char)
            continue
        if re.search(r"[\)\]）】]", char):
            depth = max(0, depth - 1)
            buffer.append(char)
            continue
        if depth == 0 and re.search(r"[、，,；;]", char):
            item = "".join(buffer).strip()
            if item:
                parts.append(item)
            buffer = []
            continue
        buffer.append(char)

    last = "".join(buffer).strip()
    if last:
        parts.append(last)

    deduped: list[str] = []
    seen: set[str] = set()
    for item in parts:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def normalize_string_array(value: Any) -> list[str]:
    if isinstance(value, list):
        result: list[str] = []
        seen: set[str] = set()
        for item in value:
            text = str(item).strip()
            if text and text not in seen:
                seen.add(text)
                result.append(text)
        return result
    if isinstance(value, str):
        values = [part.strip() for part in re.split(r"[、，,；;/|]+", value) if part.strip()]
        result = []
        seen: set[str] = set()
        for item in values:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    return []


def clean_short_labels(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = re.sub(r"[。！？!?,，；;：:]+$", "", str(item).strip())
        if not text:
            continue
        if len(text) > 12:
            continue
        if re.search(r"^(这个声音|比如|不过|在录制时|适合出现在|请保持)", text):
            continue
        if text not in seen:
            seen.add(text)
            result.append(text)
    return result


def normalize_tag_text(text: Any) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[。！？!?,，；;：:]", " ", str(text or ""))).strip()


def normalize_emotion_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if re.search(r"温和", text) and re.search(r"愉悦|愉快|轻松", text):
        return "温和愉悦"
    if re.search(r"平静", text) and re.search(r"愉悦|愉快", text):
        return "平静愉悦"
    if re.search(r"温柔", text) and re.search(r"亲切", text):
        return "温柔亲切"
    return re.sub(r"[。！？!]+$", "", text)


def derive_tags_from_official(detail: dict[str, Any]) -> list[str]:
    bag = f"{detail.get('voice-name', '')} {detail.get('voice-description', '')} {detail.get('recommended_scene', '')}"
    text = normalize_tag_text(bag)
    tags: list[str] = []
    rules = [
        (r"男", ["男声", "男性"]),
        (r"女", ["女声", "女性"]),
        (r"旁白|有声书", ["旁白", "有声书"]),
        (r"温柔", ["温柔"]),
        (r"沉稳|厚重", ["沉稳"]),
        (r"活力|元气", ["活力"]),
        (r"甜|萌|少女", ["甜美"]),
        (r"成熟|熟女|御姐|姐姐", ["成熟"]),
        (r"冷静|冷艳", ["冷感"]),
        (r"专业|播音|解说|新闻", ["播音感"]),
        (r"情感陪伴", ["陪伴感"]),
    ]
    seen: set[str] = set()
    for pattern, values in rules:
        if re.search(pattern, text):
            for value in values:
                if value not in seen:
                    seen.add(value)
                    tags.append(value)
    return tags


def compute_information_quality(*, description: str, suitable_scenes: list[str]) -> str:
    if description and suitable_scenes:
        return "rich"
    if description or suitable_scenes:
        return "partial"
    return "missing"


def build_official_selection_summary(*, description: str, recommended_scenes: list[str]) -> str:
    parts: list[str] = []
    if description:
        parts.append(f"官方描述：{description}")
    if recommended_scenes:
        parts.append(f"官方推荐场景：{'、'.join(recommended_scenes)}")
    if not parts:
        return "官方接口未提供描述或推荐场景，请只把这个音色当作低信息备选。"
    return "；".join(parts)


def build_clone_selection_summary(*, description: str, suitable_scenes: list[str], avoid_scenes: list[str], notes: str) -> str:
    parts: list[str] = []
    if description:
        parts.append(f"音色描述：{description}")
    if suitable_scenes:
        parts.append(f"适合场景：{'、'.join(suitable_scenes)}")
    if avoid_scenes:
        parts.append(f"避免场景：{'、'.join(avoid_scenes)}")
    if notes:
        parts.append(f"备注：{notes}")
    if not parts:
        return "当前缺少可用音色描述，请先补充 manual 或重新分析。"
    return "；".join(parts)


def official_lookup_keys(voice: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    for raw_value in [voice.get("asset_id"), voice.get("voice_id")]:
        value = trim_string(raw_value)
        if value and value not in keys:
            keys.append(value)
    return keys


def normalize_official_voice_entry(voice: dict[str, Any], fallback_voice: dict[str, Any] | None = None) -> dict[str, Any]:
    primary = voice if isinstance(voice, dict) else {}
    fallback = fallback_voice if isinstance(fallback_voice, dict) else {}

    raw_detail: dict[str, Any] = {}
    for source in [fallback.get("raw"), primary.get("raw")]:
        if not isinstance(source, dict):
            continue
        for key, value in source.items():
            if value in (None, "", [], {}):
                continue
            raw_detail[key] = value

    voice_id = (
        trim_string(primary.get("voice_id"))
        or trim_string(fallback.get("voice_id"))
        or trim_string(primary.get("asset_id"))
        or trim_string(fallback.get("asset_id"))
    )
    asset_id = trim_string(primary.get("asset_id")) or trim_string(fallback.get("asset_id")) or voice_id
    display_name = (
        trim_string(primary.get("display_name"))
        or trim_string(raw_detail.get("voice-name"))
        or trim_string(fallback.get("display_name"))
        or voice_id
        or asset_id
    )
    description = (
        trim_string(primary.get("description"))
        or trim_string(raw_detail.get("voice-description"))
        or trim_string(fallback.get("description"))
    )
    suitable_scenes = normalize_string_array(primary.get("recommended_scenes") or primary.get("suitable_scenes"))
    if not suitable_scenes:
        suitable_scenes = split_scenes(raw_detail.get("recommended_scene"))
    if not suitable_scenes:
        suitable_scenes = normalize_string_array(fallback.get("recommended_scenes") or fallback.get("suitable_scenes"))
    tags = normalize_string_array(primary.get("tags"))
    if not tags:
        tags = derive_tags_from_official(raw_detail) if raw_detail else []
    if not tags:
        tags = normalize_string_array(fallback.get("tags"))
    avoid_scenes = normalize_string_array(primary.get("avoid_scenes") or fallback.get("avoid_scenes"))
    stable_instruction = trim_string(primary.get("stable_instruction"))
    official_name = trim_string(raw_detail.get("voice-name")) or display_name
    information_quality = compute_information_quality(
        description=description,
        suitable_scenes=suitable_scenes,
    )

    normalized_raw = dict(raw_detail)
    normalized_raw.setdefault("voice-name", official_name)
    normalized_raw.setdefault("voice-description", description)
    normalized_raw.setdefault("recommended_scene", "、".join(suitable_scenes))

    return {
        "asset_id": asset_id or voice_id,
        "voice_id": voice_id,
        "display_name": display_name,
        "description": description,
        "official_description": description,
        "recommended_scenes": suitable_scenes,
        "suitable_scenes": suitable_scenes,
        "avoid_scenes": avoid_scenes,
        "tags": tags,
        "stable_instruction": stable_instruction,
        "selection_summary": build_official_selection_summary(
            description=description,
            recommended_scenes=suitable_scenes,
        ),
        "information_quality": information_quality,
        "raw": normalized_raw,
    }


def merge_official_voice_catalog(primary: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    fallback_lookup: dict[str, dict[str, Any]] = {}
    for voice in fallback.get("voices") or []:
        for key in official_lookup_keys(voice):
            fallback_lookup[key] = voice

    merged_voices: list[dict[str, Any]] = []
    seen: set[str] = set()
    for voice in primary.get("voices") or []:
        fallback_voice = None
        for key in official_lookup_keys(voice):
            if key in fallback_lookup:
                fallback_voice = fallback_lookup[key]
                break
        normalized = normalize_official_voice_entry(voice, fallback_voice)
        primary_key = trim_string(normalized.get("asset_id")) or trim_string(normalized.get("voice_id"))
        if primary_key and primary_key not in seen:
            seen.add(primary_key)
            merged_voices.append(normalized)

    for voice in fallback.get("voices") or []:
        normalized = normalize_official_voice_entry(voice)
        primary_key = trim_string(normalized.get("asset_id")) or trim_string(normalized.get("voice_id"))
        if primary_key and primary_key in seen:
            continue
        if primary_key:
            seen.add(primary_key)
        merged_voices.append(normalized)

    merged_source = trim_string(primary.get("source")) or trim_string(fallback.get("source")) or "unknown"
    if trim_string(primary.get("source")) == "api" and (fallback.get("voices") or []):
        merged_source = "api+bundled-backfill"

    return {
        "version": str(primary.get("version") or fallback.get("version") or "1"),
        "source": merged_source,
        "synced_at": primary.get("synced_at") or fallback.get("synced_at") or datetime.utcnow().isoformat() + "Z",
        "model": primary.get("model") or fallback.get("model") or "step-tts-2",
        "voices": merged_voices,
    }


def get_message_text(message_content: Any) -> str:
    if isinstance(message_content, str):
        return message_content
    if isinstance(message_content, list):
        chunks: list[str] = []
        for item in message_content:
            if isinstance(item, str):
                chunks.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                chunks.append(item["text"])
        return "\n".join(chunks)
    if isinstance(message_content, dict) and isinstance(message_content.get("text"), str):
        return message_content["text"]
    return ""


def parse_json_from_text(raw_text: Any) -> dict[str, Any]:
    trimmed = str(raw_text or "").strip()
    fenced = re.sub(r"^```(?:json)?\s*", "", trimmed, flags=re.IGNORECASE)
    fenced = re.sub(r"\s*```$", "", fenced)
    start = fenced.find("{")
    end = fenced.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"模型返回中未找到 JSON 对象: {trimmed[:200]}")
    return json.loads(fenced[start : end + 1])


def parse_loose_structured_fields(raw_text: Any) -> dict[str, Any]:
    known_fields = {
        "generated_description",
        "derived_tags",
        "derived_suitable_scenes",
        "derived_avoid_scenes",
        "derived_stable_instruction",
        "accent",
        "gender_guess",
        "age_band_guess",
        "speech_rate",
        "emotion_baseline",
        "confidence",
    }
    result: dict[str, Any] = {}
    pattern = re.compile(
        r'"([^"]+)":\s*("(?:\\.|[^"\\])*"|\[[\s\S]*?\]|true|false|null|-?\d+(?:\.\d+)?)'
    )
    text = str(raw_text or "")
    for match in pattern.finditer(text):
        key = match.group(1)
        if key not in known_fields:
            continue
        token = match.group(2)
        try:
            result[key] = json.loads(token)
        except Exception:
            result[key] = token.strip('"')
    if not result:
        raise ValueError(f"模型返回中未识别到可恢复字段: {text[:200]}")
    return result


def canonicalize_gender_guess(value: Any) -> str:
    text = normalize_tag_text(value).lower()
    if not text:
        return ""
    if re.search(r"female|women?|女性|女声|女生|女孩|少女|偏女", text):
        return "female"
    if re.search(r"male|men?|男性|男声|男生|男孩|少年|偏男", text):
        return "male"
    if re.search(r"unknown|未知|不确定|难判断|无法判断", text):
        return "unknown"
    return ""


def infer_gender_guess(text: str) -> str:
    normalized = normalize_tag_text(text).lower()
    has_female = bool(re.search(r"female|女性|女声|女生|女孩|少女|偏女", normalized))
    has_male = bool(re.search(r"male|男性|男声|男生|男孩|少年|偏男", normalized))
    if has_female and not has_male:
        return "female"
    if has_male and not has_female:
        return "male"
    return "unknown"


def canonicalize_age_band_guess(value: Any) -> str:
    text = normalize_tag_text(value).lower()
    if not text:
        return ""
    if re.search(r"child|儿童|小孩|幼童", text):
        return "child"
    if re.search(r"teen|青少年|少年|少女|未成年", text):
        return "teen"
    if re.search(r"young[_ ]?adult|青年|年轻成人|二十多|二十来岁|偏年轻", text):
        return "young_adult"
    if re.search(r"middle[_ ]?aged|中年", text):
        return "middle_aged"
    if re.search(r"elder|老年|老人", text):
        return "elder"
    if re.search(r"adult|成人|成年", text):
        return "adult"
    if re.search(r"unknown|未知|不确定|难判断|无法判断", text):
        return "unknown"
    return ""


def infer_age_band_guess(text: str) -> str:
    normalized = normalize_tag_text(text).lower()
    if re.search(r"child|儿童|小孩|幼童", normalized):
        return "child"
    if re.search(r"teen|青少年|少年|少女|未成年", normalized):
        return "teen"
    if re.search(r"young[_ ]?adult|青年|年轻成人|二十多|二十来岁", normalized):
        return "young_adult"
    if re.search(r"middle[_ ]?aged|中年", normalized):
        return "middle_aged"
    if re.search(r"elder|老年|老人", normalized):
        return "elder"
    if re.search(r"adult|成人|成年", normalized):
        return "adult"
    return "unknown"


def canonicalize_speech_rate(value: Any) -> str:
    text = normalize_tag_text(value).lower()
    if not text:
        return ""
    if re.search(r"medium[_ ]?slow|偏慢|稍慢|舒缓", text):
        return "medium_slow"
    if re.search(r"medium[_ ]?fast|偏快|稍快", text):
        return "medium_fast"
    if re.search(r"fast|很快|快速", text):
        return "fast"
    if re.search(r"slow|慢速|缓慢", text):
        return "slow"
    if re.search(r"medium|适中|中速|平稳", text):
        return "medium"
    if re.search(r"unknown|未知|不确定|难判断|无法判断", text):
        return "unknown"
    return ""


def infer_speech_rate(text: str) -> str:
    normalized = normalize_tag_text(text).lower()
    if re.search(r"medium[_ ]?slow|偏慢|稍慢|舒缓", normalized):
        return "medium_slow"
    if re.search(r"medium[_ ]?fast|偏快|稍快", normalized):
        return "medium_fast"
    if re.search(r"fast|很快|快速", normalized):
        return "fast"
    if re.search(r"slow|慢速|缓慢", normalized):
        return "slow"
    if re.search(r"medium|适中|中速|平稳", normalized):
        return "medium"
    return "unknown"


def normalize_analysis_result(raw_result: dict[str, Any], source_text: Any) -> dict[str, Any]:
    combined = " ".join(
        str(part or "")
        for part in [
            source_text or "",
            raw_result.get("generated_description") or "",
            raw_result.get("derived_tags") or "",
            raw_result.get("derived_suitable_scenes") or "",
            raw_result.get("derived_avoid_scenes") or "",
            raw_result.get("derived_stable_instruction") or "",
            raw_result.get("accent") or "",
            raw_result.get("gender_guess") or "",
            raw_result.get("age_band_guess") or "",
            raw_result.get("speech_rate") or "",
            raw_result.get("emotion_baseline") or "",
            str(raw_result.get("confidence") or ""),
        ]
    )

    tags = set(clean_short_labels(normalize_string_array(raw_result.get("derived_tags"))))
    suitable = set(clean_short_labels(normalize_string_array(raw_result.get("derived_suitable_scenes"))))
    avoid = set(clean_short_labels(normalize_string_array(raw_result.get("derived_avoid_scenes"))))

    def add_if(pattern: str, values: list[str], bag: set[str]) -> None:
        if re.search(pattern, combined):
            for value in values:
                bag.add(value)

    accent = "普通话" if re.search(r"普通话", combined) else (str(raw_result.get("accent") or "").strip() or "unknown")
    gender_guess = canonicalize_gender_guess(raw_result.get("gender_guess")) or infer_gender_guess(combined)
    age_band_guess = canonicalize_age_band_guess(raw_result.get("age_band_guess")) or infer_age_band_guess(combined)
    speech_rate = canonicalize_speech_rate(raw_result.get("speech_rate")) or infer_speech_rate(combined)

    if gender_guess == "female":
        tags.update(["女性", "女声"])
    elif gender_guess == "male":
        tags.update(["男性", "男声"])

    age_band_tag_map = {
        "child": "儿童",
        "teen": "青少年",
        "young_adult": "青年",
        "adult": "成年",
        "middle_aged": "中年",
        "elder": "老年",
    }
    if age_band_guess in age_band_tag_map:
        tags.add(age_band_tag_map[age_band_guess])

    if accent == "普通话":
        tags.add("标准普通话")

    add_if(r"清亮|清澈", ["清亮"], tags)
    add_if(r"甜美|甜", ["甜美"], tags)
    add_if(r"温和|温柔|亲切|亲和|友好|贴心", ["亲和"], tags)
    add_if(r"活力|阳光|积极|元气", ["活力"], tags)
    add_if(r"低沉|厚重|沉稳", ["沉稳"], tags)
    add_if(r"冷静|冷淡|克制", ["克制"], tags)
    add_if(r"校园", ["校园生活"], suitable)
    add_if(r"家庭聚会", ["家庭聚会"], suitable)
    add_if(r"家庭场景|温馨", ["温馨家庭"], suitable)
    add_if(r"邻家女孩", ["邻家女孩"], suitable)
    add_if(r"浪漫|约会", ["浪漫对白"], suitable)
    add_if(r"轻松愉快|闲聊|聊天", ["轻松对白"], suitable)
    add_if(r"朋友|交流|闲聊", ["日常交流"], suitable)
    add_if(r"温柔|体贴|亲切", ["温柔角色"], suitable)
    add_if(r"严肃", ["严肃角色"], avoid)
    add_if(r"强势", ["强势角色"], avoid)
    add_if(r"法庭", ["法庭辩论"], avoid)
    add_if(r"动作|战斗|紧张刺激", ["动作场面"], avoid)
    add_if(r"沉重|悲伤", ["沉重剧情"], avoid)
    add_if(r"战争", ["战争场面"], avoid)

    normalized_emotion = normalize_emotion_text(raw_result.get("emotion_baseline"))
    emotion_baseline = normalized_emotion or (
        "积极明快"
        if re.search(r"活力|阳光|积极", combined)
        else "温和亲切"
        if re.search(r"温柔|亲切|温暖", combined)
        else "unknown"
    )

    confidence_raw = raw_result.get("confidence")
    try:
        confidence = float(confidence_raw)
    except Exception:
        confidence = 0.85 if re.search(r"很有信心|非常有信心", combined) else 0.7
    if confidence > 1 and confidence <= 100:
        confidence /= 100
    confidence = max(0.0, min(1.0, confidence))

    description = str(raw_result.get("generated_description") or "").strip()
    stable_instruction_raw = str(raw_result.get("derived_stable_instruction") or "")
    stable_instruction = stable_instruction_raw.strip()
    if stable_instruction and re.search(r"^(请|在录制时)", stable_instruction):
        stable_instruction = ""

    return {
        "generated_description": description,
        "derived_tags": list(tags),
        "derived_suitable_scenes": list(suitable),
        "derived_avoid_scenes": list(avoid),
        "derived_stable_instruction": stable_instruction,
        "accent": accent,
        "gender_guess": gender_guess,
        "age_band_guess": age_band_guess,
        "speech_rate": speech_rate,
        "emotion_baseline": emotion_baseline,
        "confidence": confidence,
    }


def has_non_empty_array(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def has_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def create_empty_manual_profile() -> dict[str, Any]:
    return {
        "description": "",
        "tags": [],
        "suitable_scenes": [],
        "avoid_scenes": [],
        "stable_instruction": "",
        "notes": "",
    }


def normalize_manual_profile(profile: Any) -> dict[str, Any]:
    value = profile or {}
    base = create_empty_manual_profile()
    return {
        "description": value.get("description", base["description"]).strip() if has_non_empty_string(value.get("description")) else base["description"],
        "tags": normalize_string_array(value.get("tags")),
        "suitable_scenes": normalize_string_array(value.get("suitable_scenes")),
        "avoid_scenes": normalize_string_array(value.get("avoid_scenes")),
        "stable_instruction": value.get("stable_instruction", base["stable_instruction"]).strip() if has_non_empty_string(value.get("stable_instruction")) else base["stable_instruction"],
        "notes": value.get("notes", base["notes"]).strip() if has_non_empty_string(value.get("notes")) else base["notes"],
    }


def extract_manual_profile(existing_review_entry: dict[str, Any], existing_clone: dict[str, Any]) -> dict[str, Any]:
    if isinstance(existing_review_entry.get("manual"), dict):
        return normalize_manual_profile(existing_review_entry.get("manual"))
    if isinstance(((existing_clone.get("profiles") or {}).get("manual")), dict):
        return normalize_manual_profile((existing_clone.get("profiles") or {}).get("manual"))
    return normalize_manual_profile(
        {
            "description": existing_clone.get("description"),
            "tags": existing_clone.get("tags"),
            "suitable_scenes": existing_clone.get("suitable_scenes"),
            "avoid_scenes": existing_clone.get("avoid_scenes"),
            "stable_instruction": existing_clone.get("stable_instruction"),
            "notes": existing_clone.get("notes"),
        }
    )


def build_archived_analysis_profile(normalized_result: dict[str, Any], clone_analysis: dict[str, Any], relative_analysis_path: str) -> dict[str, Any]:
    return {
        "description": normalized_result.get("generated_description") or "",
        "tags": normalize_string_array(normalized_result.get("derived_tags")),
        "suitable_scenes": normalize_string_array(normalized_result.get("derived_suitable_scenes")),
        "avoid_scenes": normalize_string_array(normalized_result.get("derived_avoid_scenes")),
        "stable_instruction": normalized_result.get("derived_stable_instruction") or "",
        "voice_traits": {
            "accent": normalized_result.get("accent") or "unknown",
            "gender_guess": normalized_result.get("gender_guess") or "unknown",
            "age_band_guess": normalized_result.get("age_band_guess") or "unknown",
            "speech_rate": normalized_result.get("speech_rate") or "unknown",
            "emotion_baseline": normalized_result.get("emotion_baseline") or "unknown",
            "confidence": normalized_result.get("confidence"),
        },
        "generated_at": clone_analysis.get("generated_at"),
        "generated_by": clone_analysis.get("generated_by"),
        "analysis_pipeline": clone_analysis.get("analysis_pipeline"),
        "analysis_file": relative_analysis_path,
    }


def build_model_analysis_record(clone_analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": clone_analysis.get("generated_at"),
        "generated_by": clone_analysis.get("generated_by"),
        "response_mode": clone_analysis.get("response_mode"),
        "response_type": clone_analysis.get("response_type"),
        "analysis_pipeline": clone_analysis.get("analysis_pipeline"),
        "analysis_file": clone_analysis.get("analysis_file"),
        "raw_text": clone_analysis.get("raw_text"),
        "raw_model_result": clone_analysis.get("raw_model_result"),
        "structured_result": clone_analysis.get("structured_result"),
        "structured_raw": clone_analysis.get("structured_raw"),
        "normalization_note": clone_analysis.get("normalization_note") or "",
        "normalized_result": clone_analysis.get("normalized_result"),
    }


def build_review_state(manual_profile: dict[str, Any], generated_at: str) -> dict[str, Any]:
    has_manual = any(
        [
            has_non_empty_string(manual_profile.get("description")),
            has_non_empty_array(manual_profile.get("tags")),
            has_non_empty_array(manual_profile.get("suitable_scenes")),
            has_non_empty_array(manual_profile.get("avoid_scenes")),
            has_non_empty_string(manual_profile.get("stable_instruction")),
            has_non_empty_string(manual_profile.get("notes")),
        ]
    )
    return {
        "status": "manual_override_present" if has_manual else "pending_manual_confirmation",
        "edit_target": "manual",
        "compare_against": "archived_analysis",
        "last_analysis_at": generated_at,
    }


def build_review_entry(display_name: str, manual_profile: dict[str, Any], model_analysis: dict[str, Any], archived_analysis_profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "display_name": display_name,
        "manual": manual_profile,
        "model_analysis": model_analysis,
        "archived_analysis": archived_analysis_profile,
        "review": build_review_state(manual_profile, model_analysis.get("generated_at") or ""),
    }


def pick_effective_string(manual_value: Any, archived_value: Any) -> dict[str, Any]:
    if has_non_empty_string(manual_value):
        return {"value": str(manual_value).strip(), "source": "manual"}
    if has_non_empty_string(archived_value):
        return {"value": str(archived_value).strip(), "source": "archived_analysis"}
    return {"value": "", "source": "empty"}


def pick_effective_array(manual_value: Any, archived_value: Any) -> dict[str, Any]:
    if has_non_empty_array(manual_value):
        return {"value": normalize_string_array(manual_value), "source": "manual"}
    if has_non_empty_array(archived_value):
        return {"value": normalize_string_array(archived_value), "source": "archived_analysis"}
    return {"value": [], "source": "empty"}


def build_effective_profile(manual_profile: dict[str, Any], archived_analysis_profile: dict[str, Any]) -> dict[str, Any]:
    description = pick_effective_string(manual_profile.get("description"), archived_analysis_profile.get("description"))
    tags = pick_effective_array(manual_profile.get("tags"), archived_analysis_profile.get("tags"))
    suitable = pick_effective_array(manual_profile.get("suitable_scenes"), archived_analysis_profile.get("suitable_scenes"))
    avoid = pick_effective_array(manual_profile.get("avoid_scenes"), archived_analysis_profile.get("avoid_scenes"))
    stable_instruction = pick_effective_string(
        manual_profile.get("stable_instruction"), archived_analysis_profile.get("stable_instruction")
    )
    return {
        "description": description["value"],
        "tags": tags["value"],
        "suitable_scenes": suitable["value"],
        "avoid_scenes": avoid["value"],
        "stable_instruction": stable_instruction["value"],
        "notes": manual_profile.get("notes") or "",
        "sources": {
            "description": description["source"],
            "tags": tags["source"],
            "suitable_scenes": suitable["source"],
            "avoid_scenes": avoid["source"],
            "stable_instruction": stable_instruction["source"],
            "notes": "manual" if has_non_empty_string(manual_profile.get("notes")) else "empty",
        },
    }


def build_effective_library(
    library: dict[str, Any], review_store: dict[str, Any], effective_library_relative_path: str, registry: dict[str, Any] | None = None
) -> dict[str, Any]:
    registry = registry or create_voice_registry()
    clones: dict[str, Any] = {}
    for asset_id, clone_meta in (library.get("clones") or {}).items():
        review_entry = ((review_store.get("clones") or {}).get(asset_id)) or {}
        registry_entry = ((registry.get("assets") or {}).get(asset_id)) or {}
        manual_profile = extract_manual_profile(review_entry, clone_meta)
        archived_analysis_profile = review_entry.get("archived_analysis") or create_empty_manual_profile()
        effective_profile = build_effective_profile(manual_profile, archived_analysis_profile)
        clones[asset_id] = {
            "enabled": clone_meta.get("enabled", True) is not False,
            "status": clone_meta.get("status") or "draft",
            "selected_for_clone": clone_meta.get("selected_for_clone") is True,
            "display_name": clone_meta.get("display_name") or asset_id,
            "voice_id": registry_entry.get("voice_id") or "",
            "file_id": registry_entry.get("file_id") or "",
            "source_file": clone_meta.get("source_file") or "",
            "raw_file": clone_meta.get("raw_file") or "",
            "clone_model": clone_meta.get("clone_model") or "step-tts-2",
            "transcript": clone_meta.get("transcript") or "",
            "sample_text": clone_meta.get("sample_text") or "",
            "description": effective_profile["description"],
            "tags": effective_profile["tags"],
            "suitable_scenes": effective_profile["suitable_scenes"],
            "avoid_scenes": effective_profile["avoid_scenes"],
            "stable_instruction": effective_profile["stable_instruction"],
            "notes": effective_profile["notes"],
            "sources": effective_profile["sources"],
            "review_status": ((review_entry.get("review") or {}).get("status")) or "pending_manual_confirmation",
            "review_file": ((library.get("paths") or {}).get("review_file")) or "voice-reviews.yaml",
            "effective_library_file": effective_library_relative_path,
            "preview_wav": registry_entry.get("preview_wav") or "",
            "prepared_at": registry_entry.get("prepared_at") or "",
            "reference_audio_sha256": registry_entry.get("reference_audio_sha256") or "",
            "registry_file": ((library.get("paths") or {}).get("registry_file")) or ".audiobook/voice-registry.json",
        }
    return {
        "version": "1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_review_file": ((library.get("paths") or {}).get("review_file")) or "voice-reviews.yaml",
        "official_cache_file": ((library.get("paths") or {}).get("official_cache_file")) or ".audiobook/official-voices-cache.json",
        "clones": clones,
    }


def build_voice_candidate_pool(official_cache: dict[str, Any], effective_library: dict[str, Any], source_files: dict[str, str]) -> dict[str, Any]:
    voices: list[dict[str, Any]] = []
    for official_voice in official_cache.get("voices") or []:
        normalized_official = normalize_official_voice_entry(official_voice)
        voices.append(
            {
                "asset_id": normalized_official.get("asset_id") or normalized_official.get("voice_id"),
                "source": "official",
                "status": "ready",
                "review_status": "not_required",
                "voice_id": normalized_official.get("voice_id") or "",
                "display_name": normalized_official.get("display_name") or normalized_official.get("voice_id") or "",
                "description": normalized_official.get("description") or "",
                "official_description": normalized_official.get("official_description") or "",
                "recommended_scenes": normalize_string_array(normalized_official.get("recommended_scenes")),
                "tags": normalize_string_array(normalized_official.get("tags")),
                "suitable_scenes": normalize_string_array(normalized_official.get("suitable_scenes")),
                "avoid_scenes": normalize_string_array(normalized_official.get("avoid_scenes")),
                "stable_instruction": normalized_official.get("stable_instruction") or "",
                "selection_summary": normalized_official.get("selection_summary") or "",
                "information_quality": normalized_official.get("information_quality") or "missing",
                "raw": normalized_official.get("raw") or {},
            }
        )
    for asset_id, clone_voice in (effective_library.get("clones") or {}).items():
        description = trim_string(clone_voice.get("description"))
        suitable_scenes = normalize_string_array(clone_voice.get("suitable_scenes"))
        avoid_scenes = normalize_string_array(clone_voice.get("avoid_scenes"))
        notes = trim_string(clone_voice.get("notes"))
        voices.append(
            {
                "asset_id": asset_id,
                "source": "clone",
                "status": clone_voice.get("status") or "draft",
                "review_status": clone_voice.get("review_status") or "pending_manual_confirmation",
                "voice_id": clone_voice.get("voice_id") or "",
                "display_name": clone_voice.get("display_name") or asset_id,
                "description": description,
                "tags": normalize_string_array(clone_voice.get("tags")),
                "suitable_scenes": suitable_scenes,
                "avoid_scenes": avoid_scenes,
                "stable_instruction": clone_voice.get("stable_instruction") or "",
                "notes": notes,
                "selected_for_clone": clone_voice.get("selected_for_clone") is True,
                "clone_model": clone_voice.get("clone_model") or "step-tts-2",
                "source_file": clone_voice.get("source_file") or "",
                "raw_file": clone_voice.get("raw_file") or "",
                "sources": clone_voice.get("sources") or {},
                "selection_summary": build_clone_selection_summary(
                    description=description,
                    suitable_scenes=suitable_scenes,
                    avoid_scenes=avoid_scenes,
                    notes=notes,
                ),
                "information_quality": compute_information_quality(
                    description=description,
                    suitable_scenes=suitable_scenes,
                ),
            }
        )
    return {
        "version": "1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_effective_library_file": source_files["effectiveLibraryFile"],
        "source_official_cache_file": source_files["officialCacheFile"],
        "voices": voices,
    }


def request_json(url: str, headers: dict[str, str] | None = None, body: dict[str, Any] | None = None, method: str | None = None) -> dict[str, Any]:
    data = None
    final_headers = dict(headers or {})
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=data, headers=final_headers, method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")
            return json.loads(text)
    except urllib.error.HTTPError as error:
        error_text = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{error.status} {error_text}") from error


def structure_analysis_text(api_key: str, analysis_text: str) -> dict[str, Any]:
    body = {
        "model": "step-3.5-flash",
        "messages": [
            {
                "role": "system",
                "content": "\n".join(
                    [
                        "你是结构化整理助手。只根据给定音色分析文本整理 JSON，不要补充音频中不存在的信息。",
                        "必须只输出一个合法 JSON 对象，不要 markdown，不要解释。",
                        "字段固定为：generated_description, derived_tags, derived_suitable_scenes, derived_avoid_scenes, derived_stable_instruction, accent, gender_guess, age_band_guess, speech_rate, emotion_baseline, confidence。",
                        "其中 derived_tags / derived_suitable_scenes / derived_avoid_scenes 必须是短标签数组。",
                        "如果原文证据不足，gender_guess / age_band_guess / speech_rate 要写 unknown，不要从“年轻、温柔、甜美”这类形容词硬推性别。",
                        "generated_description 只描述长期声线特征，不要脑补人物设定。",
                        "derived_stable_instruction 只写稳定可复用的 TTS 指导语；如果不确定就写空字符串，不要写“请继续保持”这类对话式措辞。",
                        "gender_guess 只能是 male/female/unknown。",
                        "age_band_guess 只能是 child/teen/young_adult/adult/middle_aged/elder/unknown。",
                        "speech_rate 只能是 slow/medium_slow/medium/medium_fast/fast/unknown。",
                        "confidence 必须是 0 到 1 的数字。",
                        "如果信息不足，用空字符串、空数组或 unknown 兜底。",
                    ]
                ),
            },
            {
                "role": "user",
                "content": "\n".join([
                    "请把下面这段音色分析整理成严格 JSON。",
                    "generated_description 和 derived_stable_instruction 请写成简洁中文。",
                    "",
                    analysis_text,
                ]),
            },
        ],
        "temperature": 0.1,
        "max_tokens": 1200,
        "response_format": {"type": "text"},
    }
    raw = request_json(
        CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        body=body,
    )
    content = get_message_text((((raw.get("choices") or [{}])[0]).get("message") or {}).get("content"))
    if content:
        try:
            parsed = parse_json_from_text(content)
        except Exception:
            parsed = parse_loose_structured_fields(content)
        return {"raw": raw, "content": content, "parsed": parsed}
    reasoning = get_message_text((((raw.get("choices") or [{}])[0]).get("message") or {}).get("reasoning") or "")
    if reasoning:
        return {"raw": raw, "content": reasoning, "parsed": parse_loose_structured_fields(reasoning)}
    raise RuntimeError("step-3.5-flash 结构化返回为空")


def looks_like_transcript_response(text: str) -> bool:
    normalized = trim_string(text)
    if not normalized or len(normalized) > 120:
        return False
    if "{" in normalized or "}" in normalized:
        return False
    if re.search(r"generated_description|derived_tags|gender_guess|age_band_guess|speech_rate", normalized):
        return False
    if re.search(r"声音|音色|声线|语速|语调|口音|情绪|年龄|适合|不适合|男|女|普通话|清亮|厚重|甜美|沉稳", normalized):
        return False
    return True


def build_voice_analysis_messages(asset_id: str, audio_base64: str, *, strict_no_transcript: bool = False) -> list[dict[str, Any]]:
    system_lines = [
        "你是有声书选角导演。",
        "你的目标是为后续有声书角色选角和是否值得付费 clone 提供一份稳定、保守、可复用的声音画像。",
        "请只根据音频里能稳定听出来的长期声线特征作答，不要根据台词内容、角色语义、说话者身份或刻板印象脑补人物设定。",
        "重点分析：感知性别、年龄层、声线冷暖厚薄、明亮度、语速、情绪底色、口音、适合/不适合的戏路。",
        "如果某项证据不足，请写 unknown，不要硬猜；尤其不要因为“年轻、温柔、甜美”就直接推成女性。",
        "必须只输出 JSON 文本，不要 markdown，不要解释，不要返回多余字段。",
        "generated_description 只描述稳定声线特征，不描述台词内容。",
        "derived_tags / derived_suitable_scenes / derived_avoid_scenes 必须是 JSON 数组，每项是 2-8 字短标签，不要整句。",
        "derived_stable_instruction 只写适合 TTS 长期复用的稳定指导语；如果不确定请写空字符串，不要写“请继续保持”之类的对话式措辞。",
        "gender_guess 只能是 male/female/unknown；age_band_guess 只能是 child/teen/young_adult/adult/middle_aged/elder/unknown；speech_rate 只能是 slow/medium_slow/medium/medium_fast/fast/unknown。",
        "confidence 必须是 0 到 1 的数字。",
    ]
    if strict_no_transcript:
        system_lines.append("禁止输出音频转写，禁止复述音频中的说话文本；如果听不出稳定特征，就把相关字段写 unknown 或空数组。")
    user_lines = [
        "请基于这段参考音频输出声音画像 JSON。",
        f"当前资产 ID: {asset_id}",
    ]
    if strict_no_transcript:
        user_lines.insert(1, "再次强调：不要返回台词转写，不要复述音频原句。")
    return [
        {"role": "system", "content": "\n".join(system_lines)},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "\n".join(user_lines)},
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": f"data:audio/wav;base64,{audio_base64}",
                        "format": "wav",
                    },
                },
            ],
        },
    ]


def fetch_official_voices(api_key: str, model: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"model": model})
    raw = request_json(
        f"{SYSTEM_VOICES_URL}?{query}",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    voice_ids = raw.get("voices") or []
    details = raw.get("voices-details") or {}
    voices = []
    for voice_id in voice_ids:
        detail = details.get(voice_id) or {}
        voices.append(
            normalize_official_voice_entry(
                {
                    "asset_id": voice_id,
                    "voice_id": voice_id,
                    "display_name": detail.get("voice-name") or voice_id,
                    "description": detail.get("voice-description") or "",
                    "tags": derive_tags_from_official(detail),
                    "recommended_scenes": split_scenes(detail.get("recommended_scene")),
                    "suitable_scenes": split_scenes(detail.get("recommended_scene")),
                    "avoid_scenes": [],
                    "stable_instruction": "",
                    "raw": detail,
                }
            )
        )
    return {
        "version": "1",
        "source": "api",
        "synced_at": datetime.utcnow().isoformat() + "Z",
        "model": model,
        "voices": voices,
    }


def load_bundled_official_voices(seed_path: str | Path) -> dict[str, Any]:
    raw = load_json(seed_path)
    voices = []
    for voice in raw.get("voices") or []:
        recommended_scenes = normalize_string_array(
            voice.get("recommended_scenes") or voice.get("recommended_scene") or voice.get("suitable_scenes")
        )
        raw_detail = {
            "voice-name": trim_string(voice.get("display_name") or voice.get("voice-name")),
            "voice-description": trim_string(voice.get("description") or voice.get("voice-description")),
            "recommended_scene": "、".join(recommended_scenes),
        }
        voices.append(
            normalize_official_voice_entry(
                {
                    "asset_id": voice.get("voice_id") or voice.get("asset_id"),
                    "voice_id": voice.get("voice_id") or voice.get("asset_id"),
                    "display_name": voice.get("display_name") or voice.get("voice-name") or voice.get("voice_id"),
                    "description": voice.get("description") or voice.get("voice-description") or "",
                    "tags": normalize_string_array(voice.get("tags")),
                    "recommended_scenes": recommended_scenes,
                    "suitable_scenes": recommended_scenes,
                    "avoid_scenes": normalize_string_array(voice.get("avoid_scenes")),
                    "stable_instruction": voice.get("stable_instruction") or "",
                    "raw": raw_detail,
                }
            )
        )
    return {
        "version": str(raw.get("version") or "1"),
        "source": "bundled-seed",
        "synced_at": datetime.utcnow().isoformat() + "Z",
        "model": raw.get("model") or "step-tts-2",
        "voices": voices,
    }


def refresh_official_cache_only(
    library: dict[str, Any],
    library_path: Path,
    library_dir: Path,
    review_store: dict[str, Any],
    registry: dict[str, Any],
    review_path: Path,
    effective_library_path: Path,
    candidate_pool_path: Path,
    registry_path: Path,
) -> None:
    api_key_info = resolve_step_api_key([Path.cwd(), library_dir, Path(__file__).resolve().parent])
    api_key = str(api_key_info.get("value") or "")
    if not api_key:
        raise RuntimeError("缺少 STEP_API_KEY，无法访问 Step API")

    official_cache_path = resolve_path(
        library_dir,
        library["paths"].get("official_cache_file", ".audiobook/official-voices-cache.json"),
    )
    bundled_official_voices_path = (
        Path(__file__).resolve().parent / "../assets/official-voices.seed.json"
    ).resolve()

    ensure_dir(review_path.parent)
    ensure_dir(effective_library_path.parent)
    ensure_dir(candidate_pool_path.parent)
    ensure_dir(registry_path.parent)
    ensure_dir(official_cache_path.parent)

    bundled_official = load_bundled_official_voices(bundled_official_voices_path)
    official_sync_error = ""
    try:
        official = merge_official_voice_catalog(
            fetch_official_voices(
                api_key,
                (library.get("official") or {}).get("api_model") or "step-tts-2",
            ),
            bundled_official,
        )
    except Exception as error:
        official = bundled_official
        official_sync_error = str(error)
    save_json(official_cache_path, official)

    library.setdefault("official", {})
    library["official"]["last_synced_at"] = official.get("synced_at")
    library["official"]["last_sync_source"] = official.get("source") or "unknown"
    library["official"]["last_sync_error"] = official_sync_error
    library["official"].pop("catalog", None)

    effective_library = build_effective_library(
        library,
        review_store,
        str(effective_library_path.relative_to(library_dir)),
        registry,
    )
    save_yaml(effective_library_path, effective_library)
    save_yaml(
        candidate_pool_path,
        build_voice_candidate_pool(
            official,
            effective_library,
            {
                "effectiveLibraryFile": str(effective_library_path.relative_to(library_dir)),
                "officialCacheFile": str(official_cache_path.relative_to(library_dir)),
            },
        ),
    )
    save_yaml(library_path, library)

    print(
        json.dumps(
            {
                "library_path": str(library_path),
                "review_path": str(review_path),
                "effective_library_path": str(effective_library_path),
                "candidate_pool_path": str(candidate_pool_path),
                "official_cache_path": str(official_cache_path),
                "official_sync_source": library["official"].get("last_sync_source"),
                "official_sync_error": official_sync_error,
                "official_voice_count": len(official.get("voices") or []),
                "step_api_key_source": api_key_info.get("source"),
                "mode": "refresh-official-only",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def analyze_voice(api_key: str, wav_path: str | Path, asset_id: str) -> dict[str, Any]:
    audio_base64 = base64.b64encode(Path(wav_path).read_bytes()).decode("ascii")
    raw = {}
    content = ""
    retried_without_transcript = False

    def request_analysis(*, strict_no_transcript: bool) -> tuple[dict[str, Any], str]:
        body = {
            "model": "step-audio-r1.1",
            "modalities": ["text"],
            "messages": build_voice_analysis_messages(
                asset_id,
                audio_base64,
                strict_no_transcript=strict_no_transcript,
            ),
            "temperature": 0.2,
            "max_tokens": 800,
            "response_format": {"type": "text"},
        }
        response = request_json(
            CHAT_COMPLETIONS_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            body=body,
        )
        message_text = get_message_text((((response.get("choices") or [{}])[0]).get("message") or {}).get("content"))
        return response, message_text

    raw, content = request_analysis(strict_no_transcript=False)
    if looks_like_transcript_response(content):
        retried_without_transcript = True
        raw, content = request_analysis(strict_no_transcript=True)

    pipeline_suffix = ":text+retry-no-transcript" if retried_without_transcript else ":text"
    try:
        json_result = parse_json_from_text(content)
        return {
            "raw": raw,
            "content": content,
            "parsed": json_result,
            "raw_model_result": json_result,
            "structured_result": None,
            "structured_raw": None,
            "response_type": "text",
            "pipeline": f"step-audio-r1.1{pipeline_suffix}",
        }
    except Exception:
        try:
            recovered = parse_loose_structured_fields(content)
            return {
                "raw": raw,
                "content": content,
                "parsed": recovered,
                "raw_model_result": recovered,
                "structured_result": None,
                "structured_raw": None,
                "response_type": "text",
                "pipeline": f"step-audio-r1.1{pipeline_suffix}+loose-json-recovery",
            }
        except Exception:
            pass

    structured = structure_analysis_text(api_key, content)
    return {
        "raw": raw,
        "content": content,
        "parsed": structured["parsed"],
        "raw_model_result": None,
        "structured_result": structured["parsed"],
        "structured_raw": structured["raw"],
        "response_type": "text",
        "pipeline": f"step-audio-r1.1{pipeline_suffix} -> step-3.5-flash:text",
    }


def refresh_clone_profiles_from_stored_analysis(
    library: dict[str, Any], library_dir: Path, review_store: dict[str, Any], asset_id: str
) -> dict[str, Any]:
    existing_clone = ((library.get("clones") or {}).get(asset_id))
    if not existing_clone:
        raise RuntimeError(f"未找到 clone 资产: {asset_id}")
    existing_analysis = existing_clone.get("analysis") or {}
    analysis_file_relative = existing_analysis.get("analysis_file") or str(
        Path((library.get("paths") or {}).get("analysis_dir") or ".audiobook/voice-analysis") / f"{asset_id}.json"
    )
    analysis_path = resolve_path(library_dir, analysis_file_relative)
    if not analysis_path.exists():
        raise RuntimeError(f"缺少分析文件，无法重建 profiles: {analysis_path}")
    stored_analysis = load_json(analysis_path)
    existing_review_entry = ((review_store.get("clones") or {}).get(asset_id)) or {}
    manual_profile = extract_manual_profile(existing_review_entry, existing_clone)
    relative_analysis_path = str(analysis_path.relative_to(library_dir))
    archived_analysis_profile = build_archived_analysis_profile(
        stored_analysis.get("normalized_result") or {}, stored_analysis, relative_analysis_path
    )
    model_analysis = build_model_analysis_record({**stored_analysis, "analysis_file": relative_analysis_path})
    review_entry = build_review_entry(
        existing_clone.get("display_name") or asset_id,
        manual_profile,
        model_analysis,
        archived_analysis_profile,
    )
    review_store.setdefault("clones", {})[asset_id] = review_entry
    library.setdefault("clones", {})[asset_id] = {
        "enabled": existing_clone.get("enabled", True) is not False,
        "status": existing_clone.get("status") or "ready_for_clone_decision",
        "selected_for_clone": existing_clone.get("selected_for_clone") is True,
        "display_name": existing_clone.get("display_name") or asset_id,
        "source_file": existing_clone.get("source_file") or "",
        "raw_file": existing_clone.get("raw_file") or "",
        "clone_model": existing_clone.get("clone_model") or "step-tts-2",
        "transcript": existing_clone.get("transcript") or "",
        "sample_text": existing_clone.get("sample_text") or "",
        "review_ref": {
            "review_file": ((library.get("paths") or {}).get("review_file")) or "voice-reviews.yaml",
            "key": asset_id,
            "last_status": (review_entry.get("review") or {}).get("status"),
            "last_updated_at": (review_entry.get("review") or {}).get("last_analysis_at"),
        },
        "analysis": {
            "enabled": existing_analysis.get("enabled", True) is not False,
            "model": existing_analysis.get("model") or "step-audio-r1.1",
            "response_mode": existing_analysis.get("response_mode") or "text",
            "analysis_file": relative_analysis_path,
            "last_generated_at": stored_analysis.get("generated_at") or existing_analysis.get("last_generated_at") or "",
            "normalized_result_note": "normalized_result 是本地归一化建议，不是模型原话。",
        },
    }
    return {
        "asset_id": asset_id,
        "analysis_path": str(analysis_path),
        "review_status": (review_entry.get("review") or {}).get("status"),
    }


def choose_asset_id(input_path: str | Path) -> str:
    stamp = datetime.now().strftime("%Y%m%d")
    base = Path(input_path).stem
    ascii_base = (
        unicodedata.normalize("NFKD", base)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    ascii_base = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_base).strip("_").lower()
    return f"{ascii_base}_{stamp}" if ascii_base else f"voice_{stamp}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync audiobook voice library and clone analysis.")
    parser.add_argument("--input", help="Input audio file path")
    parser.add_argument("--asset-id", dest="asset_id", help="Explicit asset id")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--refresh-profiles-only", action="store_true", help="Rebuild effective/review files only")
    parser.add_argument("--refresh-official-only", action="store_true", help="Refresh official voices and rebuild candidate pool only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    library_path = Path(args.library).resolve()
    library_dir = library_path.parent
    library = load_yaml(library_path)
    library.setdefault("paths", {})

    review_path = resolve_path(library_dir, library["paths"].get("review_file", "voice-reviews.yaml"))
    effective_library_path = resolve_path(
        library_dir, library["paths"].get("effective_library_file", ".audiobook/effective-voice-library.yaml")
    )
    candidate_pool_path = resolve_path(
        library_dir, library["paths"].get("candidate_pool_file", ".audiobook/voice-candidate-pool.yaml")
    )
    registry_path = resolve_path(library_dir, library["paths"].get("registry_file", ".audiobook/voice-registry.json"))
    review_store = load_review_store(review_path)
    registry = load_voice_registry(registry_path)

    if args.refresh_profiles_only and args.refresh_official_only:
        raise RuntimeError("--refresh-profiles-only 和 --refresh-official-only 不能同时使用")

    if args.refresh_profiles_only:
        target_asset_ids = [args.asset_id] if args.asset_id else list((library.get("clones") or {}).keys())
        if not target_asset_ids:
            raise RuntimeError("没有可重建的 clone 条目")
        refreshed = [refresh_clone_profiles_from_stored_analysis(library, library_dir, review_store, asset_id) for asset_id in target_asset_ids]
        review_store["generated_at"] = datetime.utcnow().isoformat() + "Z"
        ensure_dir(review_path.parent)
        ensure_dir(effective_library_path.parent)
        ensure_dir(candidate_pool_path.parent)
        ensure_dir(registry_path.parent)
        save_yaml(review_path, review_store)
        effective_library = build_effective_library(
            library,
            review_store,
            str(effective_library_path.relative_to(library_dir)),
            registry,
        )
        save_yaml(effective_library_path, effective_library)
        official_cache_path = resolve_path(library_dir, library["paths"].get("official_cache_file", ".audiobook/official-voices-cache.json"))
        official_cache = load_json(official_cache_path)
        save_yaml(
            candidate_pool_path,
            build_voice_candidate_pool(
                official_cache,
                effective_library,
                {
                    "effectiveLibraryFile": str(effective_library_path.relative_to(library_dir)),
                    "officialCacheFile": str(official_cache_path.relative_to(library_dir)),
                },
            ),
        )
        save_yaml(library_path, library)
        print(
            json.dumps(
                {
                    "library_path": str(library_path),
                    "review_path": str(review_path),
                    "effective_library_path": str(effective_library_path),
                    "candidate_pool_path": str(candidate_pool_path),
                    "refreshed_assets": refreshed,
                    "refreshed_count": len(refreshed),
                    "mode": "refresh-profiles-only",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.refresh_official_only:
        refresh_official_cache_only(
            library,
            library_path,
            library_dir,
            review_store,
            registry,
            review_path,
            effective_library_path,
            candidate_pool_path,
            registry_path,
        )
        return

    api_key_info = resolve_step_api_key([Path.cwd(), library_dir, Path(__file__).resolve().parent])
    api_key = str(api_key_info.get("value") or "")
    if not api_key:
        raise RuntimeError("缺少 STEP_API_KEY，无法访问 Step API")

    inbox_dir = resolve_path(library_dir, library["paths"].get("inbox_dir", "voices/inbox"))
    source_path = Path(args.input).resolve() if args.input else None
    if source_path is None or not source_path.exists():
        files = sorted([item for item in inbox_dir.iterdir() if item.is_file()])
        if not files:
            raise RuntimeError(f"inbox 中没有待处理音频: {inbox_dir}")
        source_path = files[0]

    asset_id = args.asset_id or choose_asset_id(source_path)
    references_dir = resolve_path(library_dir, library["paths"].get("references_dir", "voices/references"))
    analysis_dir = resolve_path(library_dir, library["paths"].get("analysis_dir", ".audiobook/voice-analysis"))
    official_cache_path = resolve_path(library_dir, library["paths"].get("official_cache_file", ".audiobook/official-voices-cache.json"))
    bundled_official_voices_path = (Path(__file__).resolve().parent / "../assets/official-voices.seed.json").resolve()

    ensure_dir(references_dir)
    ensure_dir(analysis_dir)
    ensure_dir(official_cache_path.parent)
    ensure_dir(review_path.parent)
    ensure_dir(effective_library_path.parent)
    ensure_dir(candidate_pool_path.parent)
    ensure_dir(registry_path.parent)

    asset_dir = references_dir / asset_id
    ensure_dir(asset_dir)
    raw_ext = source_path.suffix or ".bin"
    raw_path = asset_dir / f"raw{raw_ext}"
    reference_path = asset_dir / "reference.wav"

    source_origin = "external_input"
    inbox_consumed = False
    resolved_source_path = source_path.resolve()
    resolved_raw_path = raw_path.resolve()
    if resolved_source_path == resolved_raw_path:
        source_origin = "library_reference"
    elif is_relative_to(resolved_source_path, inbox_dir):
        if raw_path.exists():
            raw_path.unlink()
        shutil.move(str(resolved_source_path), str(raw_path))
        source_origin = "inbox"
        inbox_consumed = True
    else:
        shutil.copyfile(resolved_source_path, raw_path)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "24000",
            str(reference_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    bundled_official = load_bundled_official_voices(bundled_official_voices_path)
    official_sync_error = ""
    try:
        official = merge_official_voice_catalog(
            fetch_official_voices(api_key, (library.get("official") or {}).get("api_model") or "step-tts-2"),
            bundled_official,
        )
    except Exception as error:
        official = bundled_official
        official_sync_error = str(error)
    save_json(official_cache_path, official)

    library.setdefault("official", {})
    library["official"]["last_synced_at"] = official.get("synced_at")
    library["official"]["last_sync_source"] = official.get("source") or "unknown"
    library["official"]["last_sync_error"] = official_sync_error
    library["official"].pop("catalog", None)

    analyzed = analyze_voice(api_key, reference_path, asset_id)
    normalized_result = normalize_analysis_result(analyzed["parsed"], analyzed["content"])
    analysis_path = analysis_dir / f"{asset_id}.json"
    clone_analysis = {
        "asset_id": asset_id,
        "source_audio": str(raw_path),
        "reference_audio": str(reference_path),
        "source_audio_sha256": sha256_file(raw_path),
        "reference_audio_sha256": sha256_file(reference_path),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "generated_by": "step-audio-r1.1",
        "response_mode": "text",
        "response_type": analyzed["response_type"],
        "analysis_pipeline": analyzed["pipeline"],
        "raw_text": analyzed["content"],
        "raw_model_result": analyzed["raw_model_result"],
        "structured_result": analyzed["structured_result"],
        "normalization_note": "normalized_result 为本地归一化建议字段，仅用于检索和选角，不代表 step-audio-r1.1 的逐字原话。",
        "normalized_result": normalized_result,
    }
    if analyzed.get("structured_raw") is not None:
        clone_analysis["structured_raw"] = analyzed["structured_raw"]
    save_json(analysis_path, clone_analysis)

    library.setdefault("clones", {})
    existing_clone = (library.get("clones") or {}).get(asset_id) or {}
    existing_analysis = existing_clone.get("analysis") or {}
    existing_review_entry = (review_store.get("clones") or {}).get(asset_id) or {}
    manual_profile = extract_manual_profile(existing_review_entry, existing_clone)
    relative_raw_path = str(raw_path.relative_to(references_dir))
    relative_reference_path = str(reference_path.relative_to(references_dir))
    relative_analysis_path = str(analysis_path.relative_to(library_dir))
    archived_analysis_profile = build_archived_analysis_profile(normalized_result, clone_analysis, relative_analysis_path)
    clone_analysis["analysis_file"] = relative_analysis_path
    model_analysis = build_model_analysis_record(clone_analysis)
    review_entry = build_review_entry(existing_clone.get("display_name") or asset_id, manual_profile, model_analysis, archived_analysis_profile)
    review_store.setdefault("clones", {})[asset_id] = review_entry
    review_store["generated_at"] = datetime.utcnow().isoformat() + "Z"
    library["clones"][asset_id] = {
        "enabled": existing_clone.get("enabled", True) is not False,
        "status": "ready_for_clone_decision",
        "selected_for_clone": existing_clone.get("selected_for_clone") is True,
        "display_name": existing_clone.get("display_name") or asset_id,
        "source_file": existing_clone.get("source_file") or relative_reference_path,
        "raw_file": existing_clone.get("raw_file") or relative_raw_path,
        "clone_model": existing_clone.get("clone_model") or "step-tts-2",
        "transcript": existing_clone.get("transcript") or "",
        "sample_text": existing_clone.get("sample_text") or "",
        "review_ref": {
            "review_file": str(review_path.relative_to(library_dir)),
            "key": asset_id,
            "last_status": (review_entry.get("review") or {}).get("status"),
            "last_updated_at": (review_entry.get("review") or {}).get("last_analysis_at"),
        },
        "analysis": {
            "enabled": existing_analysis.get("enabled", True) is not False,
            "model": "step-audio-r1.1",
            "response_mode": "text",
            "analysis_file": relative_analysis_path,
            "last_generated_at": clone_analysis["generated_at"],
            "normalized_result_note": "normalized_result 是本地归一化建议，不是模型原话。",
        },
    }
    library["clones"][asset_id].pop("profiles", None)
    library["clones"][asset_id].pop("review", None)
    if isinstance(library["clones"][asset_id].get("analysis"), dict):
        library["clones"][asset_id]["analysis"].pop("auto_apply_fields", None)

    save_yaml(review_path, review_store)
    effective_library = build_effective_library(
        library,
        review_store,
        str(effective_library_path.relative_to(library_dir)),
        registry,
    )
    save_yaml(effective_library_path, effective_library)
    save_yaml(
        candidate_pool_path,
        build_voice_candidate_pool(
            official,
            effective_library,
            {
                "effectiveLibraryFile": str(effective_library_path.relative_to(library_dir)),
                "officialCacheFile": str(official_cache_path.relative_to(library_dir)),
            },
        ),
    )
    save_yaml(library_path, library)

    print(
        json.dumps(
            {
                "library_path": str(library_path),
                "review_path": str(review_path),
                "effective_library_path": str(effective_library_path),
                "candidate_pool_path": str(candidate_pool_path),
                "official_cache_path": str(official_cache_path),
                "official_sync_source": library["official"].get("last_sync_source"),
                "asset_id": asset_id,
                "raw_path": str(raw_path),
                "reference_path": str(reference_path),
                "analysis_path": str(analysis_path),
                "official_voice_count": len(official.get("voices") or []),
                "clone_status": library["clones"][asset_id].get("status"),
                "review_status": (review_entry.get("review") or {}).get("status"),
                "analysis_pipeline": analyzed["pipeline"],
                "input_audio_path": str(source_path),
                "source_origin": source_origin,
                "inbox_consumed": inbox_consumed,
                "step_api_key_source": api_key_info.get("source"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # pragma: no cover - CLI error path
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
