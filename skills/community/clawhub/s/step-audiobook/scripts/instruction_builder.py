#!/usr/bin/env python3

from __future__ import annotations

import re
from typing import Any

from common import trim_string


BASE_DELIVERY_INSTRUCTIONS = {
    "narration": "旁白叙述，语气中立清晰",
    "inner_monologue": "内心独白，声音更轻、更近，语气克制，贴近呼吸感，略慢",
}


def sanitize_spoken_text(text: Any) -> str:
    value = str(text or "")
    value = re.sub(r"\r", " ", value)
    value = re.sub(r"\\+[nrt]", " ", value)
    value = re.sub(r"\\+", " ", value)
    value = re.sub(r"[`*_#~^]+", " ", value)
    value = re.sub(r"[<>\[\]{}]", " ", value)
    value = re.sub(r"[|]", " ", value)
    value = re.sub(r"[•●▪◦◆◇□■▲▼※★☆☞☛→←↑↓]", " ", value)
    value = re.sub(r"-{3,}", "，", value)
    value = re.sub(r"[—–]{2,}", "，", value)
    value = re.sub(r"\.{3,}", "……", value)
    value = re.sub(r"…{3,}", "……", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s*([，。！？；：、])", r"\1", value)
    value = re.sub(r"([（【《“「『])\s+", r"\1", value)
    value = re.sub(r"\s+([）】》”」』])", r"\1", value)
    return value.strip()


def sanitize_instruction_text(text: Any) -> str:
    value = sanitize_spoken_text(text)
    value = re.sub(r"^[，。！？；：、\-\s]+", "", value)
    value = re.sub(r"[，。！？；：、\-\s]+$", "", value)
    return value.strip()


def split_instruction_value(value: Any) -> list[str]:
    text = sanitize_instruction_text(value)
    if not text:
        return []
    parts = [segment.strip() for segment in re.split(r"[，,、；;]", text) if segment.strip()]
    return parts


class InstructionBuilder:
    def __init__(
        self,
        *,
        max_length: int = 200,
        separator: str = "，",
        truncation_suffix: str = "...",
    ) -> None:
        self.max_length = max_length
        self.separator = separator
        self.truncation_suffix = truncation_suffix

    def contains_instruction(self, parts: list[str], instruction: str) -> bool:
        target = sanitize_instruction_text(instruction).lower()
        if not target:
            return False
        return any(
            existing.lower() == target or existing.lower() in target or target in existing.lower()
            for existing in parts
        )

    def dedupe_parts(self, parts: list[str]) -> list[str]:
        merged: list[str] = []
        for part in parts:
            clean_part = sanitize_instruction_text(part)
            if not clean_part:
                continue
            if not self.contains_instruction(merged, clean_part):
                merged.append(clean_part)
        return merged

    def merge_instruction_parts(self, *parts: str | None) -> str:
        flattened: list[str] = []
        for value in parts:
            if not trim_string(value):
                continue
            flattened.extend(split_instruction_value(value))
        return self.separator.join(self.dedupe_parts(flattened))

    def parse_structured_global_instruction(self, global_instruction: str) -> dict[str, list[str]] | None:
        if not re.search(r"[｜|]", global_instruction) or not re.search(r"[:=：]", global_instruction):
            return None

        parsed = {
            "scene": [],
            "narration": [],
            "dialogue": [],
            "shared": [],
        }

        matched = False
        chunks = [part.strip() for part in re.split(r"[｜|]", global_instruction) if part.strip()]
        for chunk in chunks:
            match = re.match(r"^(场景|旁白|对白|共享|通用)\s*[:=：]\s*(.+)$", chunk)
            if not match:
                parsed["shared"].extend(split_instruction_value(chunk))
                continue

            matched = True
            key, raw_value = match.group(1), match.group(2)
            values = split_instruction_value(raw_value)
            if key == "场景":
                parsed["scene"].extend(values)
            elif key == "旁白":
                parsed["narration"].extend(values)
            elif key == "对白":
                parsed["dialogue"].extend(values)
            else:
                parsed["shared"].extend(values)

        return parsed if matched else None

    def parse_legacy_global_instruction(self, global_instruction: str) -> dict[str, list[str]]:
        normalized = sanitize_spoken_text(global_instruction)
        scene_match = re.search(r"整体保持([^，。]+)", normalized)
        narration_match = re.search(r"旁白([^，。]+)", normalized)
        dialogue_match = re.search(r"(?:人物对白|角色对白|对白)([^，。]+)", normalized)

        scene = split_instruction_value(f"保持{scene_match.group(1)}") if scene_match else []
        narration = split_instruction_value(narration_match.group(1)) if narration_match else []
        dialogue = split_instruction_value(dialogue_match.group(1)) if dialogue_match else []

        residual = []
        for part in re.split(r"[，。]", normalized):
            clean_part = part.strip()
            if not clean_part:
                continue
            if clean_part.startswith("整体保持") or clean_part.startswith("旁白") or re.match(r"^(人物对白|角色对白|对白)", clean_part):
                continue
            residual.append(clean_part)

        return {
            "scene": scene,
            "narration": narration,
            "dialogue": dialogue,
            "shared": self.dedupe_parts(residual),
        }

    def resolve_applicable_global_instructions(
        self,
        *,
        speaker: str,
        delivery_mode: str,
        global_instruction: str,
    ) -> list[str]:
        effective = sanitize_instruction_text(global_instruction)
        if not effective:
            return []

        structured = self.parse_structured_global_instruction(effective)
        if structured:
            role_specific = structured["narration"] if speaker == "narrator" or delivery_mode == "narration" else structured["dialogue"]
            return self.dedupe_parts(structured["shared"] + structured["scene"] + role_specific)

        legacy = self.parse_legacy_global_instruction(effective)
        role_specific = legacy["narration"] if speaker == "narrator" or delivery_mode == "narration" else legacy["dialogue"]
        return self.dedupe_parts(legacy["shared"] + legacy["scene"] + role_specific)

    def build_tts_input_text(self, *, clean_text: str, inline_instruction: str, raw_text: str) -> str:
        safe_clean_text = sanitize_spoken_text(clean_text)
        safe_inline_instruction = sanitize_instruction_text(inline_instruction)
        normalized_raw = sanitize_spoken_text(raw_text)
        if not safe_inline_instruction:
            return safe_clean_text

        if re.match(r"^[（(][^）)]+[）)]", normalized_raw):
            return re.sub(r"^[（(][^）)]+[）)]", f"（{safe_inline_instruction}）", normalized_raw, count=1)

        return f"（{safe_inline_instruction}）{safe_clean_text}"

    def smart_truncate(self, text: str) -> str:
        if len(text) <= self.max_length:
            return text

        punct_matches = list(re.finditer(r"[，。！？,\.!?；;]", text))
        for match in reversed(punct_matches):
            if match.start() < self.max_length - len(self.truncation_suffix):
                return text[: match.start() + 1] + self.truncation_suffix

        safe_zone_start = max(0, self.max_length - 30)
        safe_zone_end = max(0, self.max_length - len(self.truncation_suffix))
        for index in range(safe_zone_end, safe_zone_start - 1, -1):
            if text[index : index + 1] in {" ", "，", "。", "、"}:
                return text[: index + 1] + self.truncation_suffix

        return text[: safe_zone_end] + self.truncation_suffix

    def build_for_segment(
        self,
        segment: dict[str, Any],
        *,
        role_stable_instruction: str = "",
        global_instruction: str = "",
    ) -> dict[str, str | int]:
        clean_text = sanitize_spoken_text(
            segment.get("clean_text")
            or segment.get("tts_input_text")
            or segment.get("raw_text")
        )
        inline_instruction = sanitize_instruction_text(segment.get("inline_instruction"))
        scene_instruction = sanitize_instruction_text(segment.get("scene_instruction"))
        role_stable = sanitize_instruction_text(role_stable_instruction)
        segment_character_instruction = sanitize_instruction_text(segment.get("character_instruction"))
        delivery_mode = trim_string(segment.get("delivery_mode")) or "dialogue"

        tts_input_text = self.build_tts_input_text(
            clean_text=clean_text,
            inline_instruction=inline_instruction,
            raw_text=trim_string(segment.get("raw_text")) or clean_text,
        )
        effective_character_instruction = self.merge_instruction_parts(
            role_stable,
            segment_character_instruction,
        )

        parts: list[str] = []
        base_instruction = BASE_DELIVERY_INSTRUCTIONS.get(delivery_mode, "")
        if base_instruction:
            parts.append(base_instruction)
        if scene_instruction and not self.contains_instruction(parts, scene_instruction):
            parts.append(scene_instruction)
        if role_stable and not self.contains_instruction(parts, role_stable):
            parts.append(role_stable)
        if segment_character_instruction and not self.contains_instruction(parts, segment_character_instruction):
            parts.append(segment_character_instruction)

        for global_part in self.resolve_applicable_global_instructions(
            speaker=trim_string(segment.get("speaker")),
            delivery_mode=delivery_mode,
            global_instruction=global_instruction,
        ):
            if not self.contains_instruction(parts, global_part):
                parts.append(global_part)

        combined_instruction = self.separator.join(self.dedupe_parts(parts))
        if len(combined_instruction) > self.max_length:
            combined_instruction = self.smart_truncate(combined_instruction)

        return {
            "clean_text": clean_text,
            "tts_input_text": tts_input_text,
            "inline_instruction": inline_instruction,
            "scene_instruction": scene_instruction,
            "role_stable_instruction": role_stable,
            "character_instruction": effective_character_instruction,
            "instruction": combined_instruction,
            "instruction_length": len(combined_instruction),
        }
