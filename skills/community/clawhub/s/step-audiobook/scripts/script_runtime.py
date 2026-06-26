#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from common import load_yaml, trim_string


VALID_DELIVERY_MODES = {"narration", "dialogue", "inner_monologue"}


def read_structured_input(input_path: str | Path) -> Any:
    path = Path(input_path)
    ext = path.suffix.lower()
    if ext == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if ext in {".yaml", ".yml"}:
        return load_yaml(path)
    raise RuntimeError(f"当前下游链路只支持结构化 yaml/json 输入，暂不支持: {path}")


def is_dialogue_script_document(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("characters"), list) and isinstance(value.get("dialogues"), list)


def is_segment_script_document(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("characters"), list) and isinstance(value.get("segments"), list)


def normalize_metadata(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def coerce_index(value: Any, fallback: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return fallback


def normalize_character(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError("characters[] 每一项都必须是对象")
    item = value or {}
    character_id = trim_string(item.get("id") or item.get("role_id"))
    if not character_id:
        raise RuntimeError("characters[].id 不能为空")
    return {
        "id": character_id,
        "name": trim_string(item.get("name")) or character_id,
        "instruction": trim_string(item.get("instruction")),
        "voice_id": trim_string(item.get("voice_id")),
        "voice_preset": trim_string(item.get("voice_preset")),
        "metadata": normalize_metadata(item.get("metadata")),
    }


def build_character_map(characters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in characters}


def dedupe_instruction_parts(parts: list[str]) -> list[str]:
    merged: list[str] = []
    for part in parts:
        text = trim_string(part)
        if not text:
            continue
        existing_index = next(
            (
                index
                for index, existing in enumerate(merged)
                if existing in text or text in existing
            ),
            -1,
        )
        if existing_index == -1:
            merged.append(text)
        elif len(text) > len(merged[existing_index]):
            merged[existing_index] = text
    return merged


def extract_prefix_inline_instruction(text: Any) -> tuple[str, str]:
    current = trim_string(text)
    if not current:
        return "", ""

    instructions: list[str] = []
    pattern = re.compile(r"^[（(]\s*([^（）()]{1,80}?)\s*[）)]\s*")

    while current:
        match = pattern.match(current)
        if not match:
            break
        instruction = trim_string(match.group(1))
        if instruction:
            instructions.append(instruction)
        current = current[match.end() :].lstrip()

    merged = "，".join(dedupe_instruction_parts(instructions))
    return merged, current or trim_string(text)


def resolve_delivery_mode(raw_mode: Any, speaker: str) -> str:
    mode = trim_string(raw_mode)
    if mode in VALID_DELIVERY_MODES:
        return mode
    return "narration" if speaker == "narrator" else "dialogue"


def normalize_dialogue_segment(
    dialogue: dict[str, Any],
    index: int,
    character_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(dialogue, dict):
        raise RuntimeError(f"dialogues[{index}] 必须是对象")
    speaker = trim_string(dialogue.get("speaker"))
    if not speaker:
        raise RuntimeError(f"dialogues[{index}].speaker 不能为空")

    character = character_map.get(speaker) or {
        "id": speaker,
        "name": speaker,
        "instruction": "",
    }
    raw_text = trim_string(dialogue.get("text"))
    if not raw_text:
        raise RuntimeError(f"dialogues[{index}].text 不能为空")
    inline_instruction, clean_text = extract_prefix_inline_instruction(raw_text)

    return {
        "index": index,
        "speaker": speaker,
        "character_name": character.get("name") or speaker,
        "character_instruction": trim_string(character.get("instruction")),
        "delivery_mode": resolve_delivery_mode(dialogue.get("delivery_mode"), speaker),
        "raw_text": raw_text,
        "clean_text": clean_text,
        "tts_input_text": clean_text,
        "inline_instruction": inline_instruction,
        "scene_instruction": trim_string(dialogue.get("scene_instruction")),
        "metadata": normalize_metadata(dialogue.get("metadata")),
    }


def normalize_explicit_segment(
    segment: dict[str, Any],
    index: int,
    character_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(segment, dict):
        raise RuntimeError(f"segments[{index}] 必须是对象")
    speaker = trim_string(segment.get("speaker"))
    if not speaker:
        raise RuntimeError(f"segments[{index}].speaker 不能为空")

    character = character_map.get(speaker) or {
        "id": speaker,
        "name": speaker,
        "instruction": "",
    }
    raw_text = trim_string(
        segment.get("raw_text")
        or segment.get("text")
        or segment.get("tts_input_text")
        or segment.get("clean_text")
    )
    if not raw_text:
        raise RuntimeError(f"segments[{index}] 缺少可用文本，请至少提供 raw_text / text / tts_input_text / clean_text 之一")
    candidate_text = trim_string(segment.get("tts_input_text") or segment.get("clean_text") or raw_text)
    extracted_inline, extracted_clean = extract_prefix_inline_instruction(candidate_text)
    inline_instruction = trim_string(segment.get("inline_instruction")) or extracted_inline
    clean_text = trim_string(segment.get("clean_text")) or extracted_clean or raw_text
    tts_input_text = trim_string(segment.get("tts_input_text")) or clean_text

    return {
        "index": coerce_index(segment.get("index"), index),
        "speaker": speaker,
        "character_name": trim_string(segment.get("character_name")) or character.get("name") or speaker,
        "character_instruction": trim_string(segment.get("character_instruction")) or trim_string(character.get("instruction")),
        "delivery_mode": resolve_delivery_mode(segment.get("delivery_mode"), speaker),
        "raw_text": raw_text,
        "clean_text": clean_text,
        "tts_input_text": tts_input_text,
        "inline_instruction": inline_instruction,
        "scene_instruction": trim_string(segment.get("scene_instruction")),
        "metadata": normalize_metadata(segment.get("metadata")),
    }


def normalize_script_document(value: Any, input_path: str | Path) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError(f"脚本输入必须是对象: {input_path}")

    raw_characters = value.get("characters") or []
    characters = [normalize_character(item) for item in raw_characters]
    character_map = build_character_map(characters)

    if is_segment_script_document(value):
        segments = [
            normalize_explicit_segment(item or {}, index, character_map)
            for index, item in enumerate(value.get("segments") or [])
        ]
    elif is_dialogue_script_document(value):
        segments = [
            normalize_dialogue_segment(item or {}, index, character_map)
            for index, item in enumerate(value.get("dialogues") or [])
        ]
    else:
        raise RuntimeError(
            "当前下游链路只支持两种结构化输入：characters+dialogues 或 characters+segments"
        )

    if not segments:
        raise RuntimeError("结构化剧本里没有可用段落，无法进入后续 audiobook 下游链路")

    for segment in segments:
        speaker = segment["speaker"]
        if speaker not in character_map:
            inferred = {
                "id": speaker,
                "name": segment.get("character_name") or speaker,
                "instruction": trim_string(segment.get("character_instruction")),
                "voice_id": "",
                "voice_preset": "",
                "metadata": {},
            }
            characters.append(inferred)
            character_map[speaker] = inferred

    return {
        "version": "1",
        "title": trim_string(value.get("title")) or Path(input_path).stem,
        "global_instruction": trim_string(value.get("global_instruction")),
        "source_input_path": str(Path(input_path).resolve()),
        "characters": characters,
        "segments": segments,
    }


def load_normalized_script(input_path: str | Path) -> dict[str, Any]:
    path = Path(input_path).resolve()
    parsed = read_structured_input(path)
    return normalize_script_document(parsed, path)
