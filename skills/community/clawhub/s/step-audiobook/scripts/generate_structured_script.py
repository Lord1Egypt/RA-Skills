#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_LIBRARY_PATH,
    ensure_dir,
    load_json_if_exists,
    get_story_base_name,
    load_yaml_if_exists,
    resolve_story_workspace_dir,
    resolve_api_key,
    save_json,
    save_yaml,
    sha256_file,
    trim_string,
)
from llm_json import call_openai_compatible_json
from llm_json import is_reasoning_model, is_step_plan_base_url
from llm_tasks import (
    build_script_chunk_messages,
    build_script_finalize_messages,
    build_script_overview_messages,
    resolve_llm_task_config,
)
from story_artifacts import refresh_story_artifact_manifest

VALID_DELIVERY_MODES = {"narration", "dialogue", "inner_monologue"}
CHECKPOINT_SCHEMA_VERSION = "2"
DEFAULT_TIMEOUT_SECONDS = 180
DEFAULT_CHAPTER_HEADING_MAX_CHARS = 60

CHAPTER_HEADING_PATTERNS = [
    re.compile(r"^第[0-9零一二三四五六七八九十百千万两〇○ＯoOIVXLCDMivxlcdm]+[章节卷回部集篇](?:\s*[：:.-]?\s*.*)?$"),
    re.compile(r"^(chapter|chap\.?)\s*[0-9ivxlcdm]+(?:\s*[:.-]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^【\s*第?[0-9零一二三四五六七八九十百千万两〇○ＯoOIVXLCDMivxlcdm]+[章节卷回部集篇].*】$"),
]
SHORT_SECTION_TITLES = {
    "序章",
    "楔子",
    "引子",
    "尾声",
    "后记",
    "番外",
    "终章",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a structured audiobook script from raw txt with an LLM-first Step 3.5 workflow."
    )
    parser.add_argument("--input", required=True, help="Raw story text path")
    parser.add_argument("--output", help="Output structured yaml path")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--model", help="Optional script generation model override")
    parser.add_argument("--base-url", dest="base_url")
    parser.add_argument("--api-key-env", dest="api_key_env")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--max-tokens", dest="max_tokens")
    parser.add_argument("--timeout-seconds", dest="timeout_seconds", type=int)
    parser.add_argument("--chunk-chars", dest="chunk_chars", type=int)
    parser.add_argument("--overview-chars", dest="overview_chars", type=int)
    parser.add_argument("--resume", dest="resume", action="store_true", help="Resume from an existing compatible checkpoint")
    parser.add_argument("--no-resume", dest="resume", action="store_false", help="Ignore existing checkpoints and start fresh")
    parser.add_argument("--chapter-split", dest="chapter_split", action="store_true", help="Enable chapter-aware pre-splitting before chunking")
    parser.add_argument("--no-chapter-split", dest="chapter_split", action="store_false", help="Disable chapter-aware pre-splitting before chunking")
    parser.set_defaults(resume=True, chapter_split=None)
    return parser.parse_args()


def resolve_default_output_path(input_path: Path) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.structured-script.yaml"


def get_artifact_path(output_path: Path) -> Path:
    return output_path.parent / f"{output_path.stem}.generation.json"


def build_script_generation_config(args: argparse.Namespace, library: dict[str, Any]) -> dict[str, Any]:
    script_generation = library.get("script_generation") or {}
    legacy_llm = (script_generation.get("llm") or {}) or ((library.get("casting") or {}).get("llm") or {})
    config = resolve_llm_task_config(
        library,
        "script_generation",
        cli_overrides={
            "api_key_env": args.api_key_env,
            "base_url": args.base_url,
            "model": args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "timeout_seconds": args.timeout_seconds,
        },
        legacy_config=legacy_llm,
    )
    config["chunk_chars"] = max(
        600,
        int(args.chunk_chars or config.get("chunk_chars") or script_generation.get("chunk_chars") or 2600),
    )
    config["overview_chars"] = max(
        1200,
        int(args.overview_chars or config.get("overview_chars") or script_generation.get("overview_chars") or 12000),
    )
    config["finalize_max_input_chars"] = max(
        4000,
        int(config.get("finalize_max_input_chars") or script_generation.get("finalize_max_input_chars") or 50000),
    )
    config["adaptive_chunking"] = bool(script_generation.get("adaptive_chunking", True))
    config["reasoning_target_chunk_chars"] = max(
        900,
        int(script_generation.get("reasoning_target_chunk_chars") or 1800),
    )
    config["reasoning_min_chunk_chars"] = max(
        600,
        int(script_generation.get("reasoning_min_chunk_chars") or 900),
    )
    config["chapter_split_enabled"] = (
        args.chapter_split
        if args.chapter_split is not None
        else bool(config.get("chapter_split_enabled", script_generation.get("chapter_split_enabled", True)))
    )
    config["chapter_heading_max_chars"] = max(
        20,
        int(config.get("chapter_heading_max_chars") or script_generation.get("chapter_heading_max_chars") or DEFAULT_CHAPTER_HEADING_MAX_CHARS),
    )
    config["timeout_seconds"] = max(
        10,
        int(config.get("timeout_seconds") or script_generation.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
    )
    return config


def clean_text_input(text: str) -> str:
    value = text.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_probable_chapter_heading(line: str, *, max_chars: int) -> bool:
    text = trim_string(line)
    if not text or len(text) > max_chars:
        return False
    if text in SHORT_SECTION_TITLES:
        return True
    return any(pattern.match(text) for pattern in CHAPTER_HEADING_PATTERNS)


def build_story_sections(
    text: str,
    *,
    chapter_split_enabled: bool,
    chapter_heading_max_chars: int,
) -> list[dict[str, Any]]:
    cleaned = clean_text_input(text)
    if not cleaned:
        return []
    if not chapter_split_enabled:
        return [{"section_index": 0, "section_title": "", "text": cleaned}]

    sections: list[dict[str, Any]] = []
    current_title = ""
    current_lines: list[str] = []
    saw_heading = False

    def flush_current() -> None:
        nonlocal current_title, current_lines
        body = trim_string("\n".join(current_lines))
        if not body:
            current_title = ""
            current_lines = []
            return
        sections.append(
            {
                "section_index": len(sections),
                "section_title": current_title,
                "text": body,
            }
        )
        current_title = ""
        current_lines = []

    for line in cleaned.split("\n"):
        stripped = trim_string(line)
        if is_probable_chapter_heading(stripped, max_chars=chapter_heading_max_chars):
            saw_heading = True
            flush_current()
            current_title = stripped
            current_lines = [stripped]
            continue
        current_lines.append(line)

    flush_current()
    if not saw_heading or not sections:
        return [{"section_index": 0, "section_title": "", "text": cleaned}]
    return sections


def build_chunk_plan(sections: list[dict[str, Any]], max_chars: int) -> list[dict[str, Any]]:
    chunk_plan: list[dict[str, Any]] = []
    for section in sections:
        section_text = trim_string(section.get("text"))
        if not section_text:
            continue
        paragraphs = split_into_paragraphs(section_text, max_chars)
        section_chunks = chunk_paragraphs(paragraphs, max_chars)
        if not section_chunks:
            section_chunks = [section_text]
        for chunk_text in section_chunks:
            chunk_plan.append(
                {
                    "chunk_index": len(chunk_plan),
                    "section_index": int(section.get("section_index") or 0),
                    "section_title": trim_string(section.get("section_title")),
                    "chunk_length": len(chunk_text),
                    "raw_text": chunk_text,
                }
            )
    return chunk_plan


def build_resume_signature(
    *,
    input_path: Path,
    output_path: Path,
    cleaned_text: str,
    llm_config: dict[str, Any],
    effective_chunk_chars: int,
    sections: list[dict[str, Any]],
    chunk_plan: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "checkpoint_schema_version": CHECKPOINT_SCHEMA_VERSION,
        "input_path": str(input_path),
        "output_path": str(output_path),
        "input_sha256": sha256_file(input_path),
        "cleaned_text_sha256": sha256_text(cleaned_text),
        "text_length": len(cleaned_text),
        "model": llm_config["model"],
        "base_url": llm_config["base_url"],
        "temperature": llm_config["temperature"],
        "max_tokens": llm_config["max_tokens"],
        "timeout_seconds": llm_config["timeout_seconds"],
        "requested_chunk_chars": llm_config["chunk_chars"],
        "effective_chunk_chars": effective_chunk_chars,
        "overview_chars": llm_config["overview_chars"],
        "chapter_split_enabled": llm_config["chapter_split_enabled"],
        "section_count": len(sections),
        "chunk_count": len(chunk_plan),
        "chunk_plan_sha256": sha256_text(
            json.dumps(
                [
                    {
                        "chunk_index": item["chunk_index"],
                        "section_index": item["section_index"],
                        "section_title": item["section_title"],
                        "raw_text": item["raw_text"],
                    }
                    for item in chunk_plan
                ],
                ensure_ascii=False,
            )
        ),
    }


def is_reusable_checkpoint(checkpoint: dict[str, Any], signature: dict[str, Any]) -> bool:
    if not isinstance(checkpoint, dict):
        return False
    if str(checkpoint.get("checkpoint_schema_version") or "") != CHECKPOINT_SCHEMA_VERSION:
        return False
    if checkpoint.get("status") not in {"running", "failed"}:
        return False
    return (checkpoint.get("resume_signature") or {}) == signature


def split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    text = trim_string(paragraph)
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    pieces: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[。！？!?；;])", text):
        chunk = trim_string(sentence)
        if not chunk:
            continue
        if current and len(current) + len(chunk) > max_chars:
            pieces.append(current)
            current = chunk
            continue
        if not current and len(chunk) > max_chars:
            for start in range(0, len(chunk), max_chars):
                pieces.append(chunk[start : start + max_chars])
            current = ""
            continue
        current = f"{current}{chunk}"
    if current:
        pieces.append(current)
    return pieces


def split_into_paragraphs(text: str, chunk_chars: int) -> list[str]:
    raw_parts = [part.strip() for part in re.split(r"\n\s*\n|\n", clean_text_input(text)) if part.strip()]
    paragraphs: list[str] = []
    for part in raw_parts:
        paragraphs.extend(split_long_paragraph(part, chunk_chars))
    return paragraphs


def chunk_paragraphs(paragraphs: list[str], max_chars: int) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0
    for paragraph in paragraphs:
        candidate_length = current_length + len(paragraph) + (2 if current else 0)
        if current and candidate_length > max_chars:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_length = len(paragraph)
            continue
        current.append(paragraph)
        current_length = candidate_length
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def should_use_reasoning_adaptive_chunking(config: dict[str, Any]) -> bool:
    return bool(config.get("adaptive_chunking")) and is_reasoning_model(str(config.get("model") or "")) and is_step_plan_base_url(
        str(config.get("base_url") or "")
    )


def derive_effective_chunk_chars(text_length: int, config: dict[str, Any]) -> int:
    requested_chunk_chars = max(600, int(config.get("chunk_chars") or 2600))
    if text_length <= 0 or not should_use_reasoning_adaptive_chunking(config):
        return requested_chunk_chars

    target_chunk_chars = min(
        requested_chunk_chars,
        max(900, int(config.get("reasoning_target_chunk_chars") or 1800)),
    )
    min_chunk_chars = min(
        requested_chunk_chars,
        max(600, int(config.get("reasoning_min_chunk_chars") or 900)),
    )
    if text_length <= target_chunk_chars:
        return requested_chunk_chars

    target_chunk_count = max(2, math.ceil(text_length / target_chunk_chars))
    adaptive_chunk_chars = math.ceil(text_length / target_chunk_count)
    return max(min_chunk_chars, min(requested_chunk_chars, adaptive_chunk_chars))


def create_default_narrator() -> dict[str, Any]:
    return {
        "id": "narrator",
        "name": "旁白",
        "instruction": "中立清晰的旁白叙述",
        "voice_trait": "narrator",
        "aliases": ["旁白", "narrator"],
    }


def create_placeholder_character(character_id: str) -> dict[str, Any] | None:
    normalized_id = trim_string(character_id)
    if not normalized_id or normalized_id == "narrator":
        return None
    return {
        "id": normalized_id,
        "name": normalized_id,
        "instruction": "成年人，声线自然，表达克制",
        "voice_trait": "default",
        "aliases": [],
    }


def normalize_character(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    character_id = trim_string(value.get("id"))
    if not character_id or character_id == "narrator":
        return None
    aliases = []
    for item in value.get("aliases") or []:
        text = trim_string(item)
        if text and text not in aliases:
            aliases.append(text)
    return {
        "id": character_id,
        "name": trim_string(value.get("name")) or character_id,
        "instruction": trim_string(value.get("instruction") or value.get("context")) or "成年人，声线自然，表达克制",
        "voice_trait": trim_string(value.get("voice_trait")) or "default",
        "aliases": aliases,
    }


def normalize_segment(value: Any, index: int, known_character_ids: set[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    speaker = trim_string(value.get("speaker")) or "narrator"
    delivery_mode = trim_string(value.get("delivery_mode"))
    if delivery_mode not in VALID_DELIVERY_MODES:
        delivery_mode = "narration" if speaker == "narrator" else "dialogue"
    raw_text = trim_string(value.get("raw_text") or value.get("text"))
    if not raw_text:
        return None
    if speaker != "narrator" and speaker not in known_character_ids:
        return None

    metadata = value.get("metadata") if isinstance(value.get("metadata"), dict) else {}
    return {
        "index": index,
        "speaker": speaker,
        "raw_text": raw_text,
        "delivery_mode": delivery_mode,
        "inline_instruction": trim_string(value.get("inline_instruction")),
        "scene_instruction": trim_string(value.get("scene_instruction")),
        "metadata": metadata,
    }


def register_missing_speakers(registry: dict[str, dict[str, Any]], raw_segments: Any) -> None:
    placeholders: list[dict[str, Any]] = []
    known_ids = set(registry.keys()) | {"narrator"}
    for item in raw_segments or []:
        if not isinstance(item, dict):
            continue
        speaker = trim_string(item.get("speaker"))
        if not speaker or speaker in known_ids:
            continue
        placeholder = create_placeholder_character(speaker)
        if not placeholder:
            continue
        placeholders.append(placeholder)
        known_ids.add(speaker)
    if placeholders:
        merge_character_registry(registry, placeholders)


def merge_character_registry(
    registry: dict[str, dict[str, Any]],
    incoming: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    for item in incoming:
        character_id = item["id"]
        existing = registry.get(character_id)
        if not existing:
            registry[character_id] = item
            continue

        if len(item.get("name", "")) > len(existing.get("name", "")):
            existing["name"] = item["name"]
        if len(item.get("instruction", "")) > len(existing.get("instruction", "")):
            existing["instruction"] = item["instruction"]
        if item.get("voice_trait") and existing.get("voice_trait") in {"", "default"}:
            existing["voice_trait"] = item["voice_trait"]
        alias_set = {trim_string(alias) for alias in existing.get("aliases") or [] if trim_string(alias)}
        alias_set.update(trim_string(alias) for alias in item.get("aliases") or [] if trim_string(alias))
        existing["aliases"] = sorted(alias_set)
    return registry


def normalize_overview_response(parsed: dict[str, Any], file_stem: str) -> dict[str, Any]:
    characters = [
        normalized
        for normalized in [normalize_character(item) for item in (parsed.get("characters") or [])]
        if normalized
    ]
    registry: dict[str, dict[str, Any]] = {}
    merge_character_registry(registry, characters)
    narrator = create_default_narrator()
    return {
        "title": trim_string(parsed.get("title")) or file_stem,
        "global_instruction": trim_string(parsed.get("global_instruction")),
        "characters": [narrator, *sorted(registry.values(), key=lambda item: item["id"])],
    }


def normalize_chunk_response(
    parsed: dict[str, Any],
    *,
    current_registry: dict[str, dict[str, Any]],
    chunk_index: int,
    section_index: int = 0,
    section_title: str = "",
) -> dict[str, Any]:
    new_characters = [
        normalized
        for normalized in [normalize_character(item) for item in (parsed.get("characters") or [])]
        if normalized
    ]
    merge_character_registry(current_registry, new_characters)
    register_missing_speakers(current_registry, parsed.get("segments") or [])
    known_ids = set(current_registry.keys()) | {"narrator"}

    segments: list[dict[str, Any]] = []
    raw_segments = parsed.get("segments") or []
    for index, item in enumerate(raw_segments):
        normalized_segment = normalize_segment(item, index, known_ids)
        if not normalized_segment:
            continue
        metadata = normalized_segment.get("metadata") or {}
        metadata = {
            **metadata,
            "source_chunk_index": chunk_index,
            "source_section_index": section_index,
        }
        if section_title:
            metadata["source_section_title"] = section_title
        normalized_segment["metadata"] = metadata
        segments.append(normalized_segment)

    return {
        "characters": sorted(current_registry.values(), key=lambda item: item["id"]),
        "segments": segments,
    }


def normalize_final_script_response(parsed: dict[str, Any], file_stem: str) -> dict[str, Any]:
    overview = normalize_overview_response(parsed, file_stem)
    registry: dict[str, dict[str, Any]] = {
        item["id"]: item
        for item in overview["characters"]
        if item["id"] != "narrator"
    }
    register_missing_speakers(registry, parsed.get("segments") or [])
    known_ids = set(registry.keys()) | {"narrator"}
    narrator = create_default_narrator()

    segments: list[dict[str, Any]] = []
    for index, item in enumerate(parsed.get("segments") or []):
        normalized_segment = normalize_segment(item, index, known_ids)
        if not normalized_segment:
            continue
        segments.append(normalized_segment)

    return {
        "title": overview["title"],
        "global_instruction": overview["global_instruction"],
        "characters": [narrator, *sorted(registry.values(), key=lambda item: item["id"])],
        "segments": reindex_segments(segments),
    }


def reindex_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reindexed = []
    for index, item in enumerate(segments):
        reindexed.append(
            {
                **item,
                "index": index,
            }
        )
    return reindexed


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise RuntimeError(f"输入文本不存在: {input_path}")

    output_path = Path(args.output).resolve() if args.output else resolve_default_output_path(input_path)
    artifact_path = get_artifact_path(output_path)
    ensure_dir(output_path.parent)

    library_path = Path(args.library).resolve()
    library = load_yaml_if_exists(library_path, {}) or {}
    llm_config = build_script_generation_config(args, library)
    api_key_info = resolve_api_key([Path.cwd(), library_path.parent, Path(__file__).resolve().parent], llm_config["api_key_env"])
    if not api_key_info.get("value"):
        raise RuntimeError(f"缺少 {llm_config['api_key_env']}，无法调用脚本生成 LLM")
    llm_config["api_key"] = api_key_info["value"]

    raw_text = input_path.read_text(encoding="utf-8")
    cleaned_text = clean_text_input(raw_text)
    if not cleaned_text:
        raise RuntimeError(f"输入文本为空: {input_path}")

    effective_chunk_chars = derive_effective_chunk_chars(len(cleaned_text), llm_config)
    sections = build_story_sections(
        cleaned_text,
        chapter_split_enabled=llm_config["chapter_split_enabled"],
        chapter_heading_max_chars=llm_config["chapter_heading_max_chars"],
    )
    chunk_plan = build_chunk_plan(sections, effective_chunk_chars)
    if not chunk_plan:
        raise RuntimeError("文本切块结果为空，无法生成结构化 script")

    overview_input = cleaned_text[: llm_config["overview_chars"]]
    resume_signature = build_resume_signature(
        input_path=input_path,
        output_path=output_path,
        cleaned_text=cleaned_text,
        llm_config=llm_config,
        effective_chunk_chars=effective_chunk_chars,
        sections=sections,
        chunk_plan=chunk_plan,
    )
    narrator = create_default_narrator()
    artifact_payload: dict[str, Any] = {}
    overview: dict[str, Any] | None = None
    finalization_result: dict[str, Any] | None = None
    final_script_document: dict[str, Any] | None = None
    finalization_skipped_reason = ""
    resumed_from_checkpoint = False

    def persist() -> None:
        artifact_payload["updated_at"] = now_iso()
        save_json(artifact_path, artifact_payload)

    try:
        existing_checkpoint = load_json_if_exists(artifact_path, None) if args.resume else None
        if existing_checkpoint and is_reusable_checkpoint(existing_checkpoint, resume_signature):
            artifact_payload = existing_checkpoint
            resumed_from_checkpoint = True
            resume_info = artifact_payload.get("resume_info") or {}
            artifact_payload["status"] = "running"
            artifact_payload["resume_info"] = {
                **resume_info,
                "resumed_from_checkpoint": True,
                "resume_count": int(resume_info.get("resume_count") or 0) + 1,
                "last_resumed_at": now_iso(),
            }
            artifact_payload["resume_signature"] = resume_signature
            persist()
        else:
            artifact_payload = {
                "checkpoint_schema_version": CHECKPOINT_SCHEMA_VERSION,
                "generated_at": now_iso(),
                "updated_at": now_iso(),
                "status": "running",
                "phase": "overview",
                "input_path": str(input_path),
                "output_path": str(output_path),
                "artifact_path": str(artifact_path),
                "resume_enabled": args.resume,
                "resume_signature": resume_signature,
                "resume_info": {
                    "resumed_from_checkpoint": False,
                    "resume_count": 0,
                    "last_resumed_at": "",
                },
                "input": {
                    "file_sha256": sha256_file(input_path),
                    "cleaned_text_sha256": sha256_text(cleaned_text),
                    "text_length": len(cleaned_text),
                },
                "chunk_count": len(chunk_plan),
                "requested_chunk_chars": llm_config["chunk_chars"],
                "effective_chunk_chars": effective_chunk_chars,
                "adaptive_chunking_enabled": should_use_reasoning_adaptive_chunking(llm_config),
                "chunk_lengths": [item["chunk_length"] for item in chunk_plan],
                "chapter_split": {
                    "enabled": llm_config["chapter_split_enabled"],
                    "section_count": len(sections),
                    "sections": [
                        {
                            "section_index": item["section_index"],
                            "section_title": item["section_title"],
                            "text_length": len(item["text"]),
                        }
                        for item in sections
                    ],
                },
                "chunk_plan": [
                    {
                        "chunk_index": item["chunk_index"],
                        "section_index": item["section_index"],
                        "section_title": item["section_title"],
                        "chunk_length": item["chunk_length"],
                    }
                    for item in chunk_plan
                ],
                "llm": {
                    "provider": llm_config["provider"],
                    "model": llm_config["model"],
                    "api_key_env": llm_config["api_key_env"],
                    "api_key_source": api_key_info.get("source"),
                    "base_url": llm_config["base_url"],
                    "temperature": llm_config["temperature"],
                    "max_tokens": llm_config["max_tokens"],
                    "timeout_seconds": llm_config["timeout_seconds"],
                },
                "overview": {
                    "status": "pending",
                    "input_length": len(overview_input),
                    "raw_response": None,
                    "raw_text_response": "",
                    "repaired": False,
                    "normalized": None,
                },
                "chunks": [],
                "provisional_script": {},
                "finalization": {
                    "status": "pending",
                    "enabled": False,
                    "input_length": 0,
                    "skipped_reason": "",
                    "raw_response": None,
                    "raw_text_response": "",
                    "repaired": False,
                    "normalized": None,
                },
                "final_script": None,
            }
            persist()

        overview_meta = artifact_payload.get("overview") or {}
        overview_candidate = overview_meta.get("normalized")
        if isinstance(overview_candidate, dict) and overview_candidate.get("title"):
            overview = overview_candidate
        else:
            artifact_payload["phase"] = "overview"
            artifact_payload["overview"] = {
                **overview_meta,
                "status": "running",
                "input_length": len(overview_input),
            }
            persist()
            overview_response = call_openai_compatible_json(
                llm_config,
                llm_config["model"],
                build_script_overview_messages(overview_input, input_path.stem),
            )
            overview = normalize_overview_response(overview_response["parsed"], input_path.stem)
            artifact_payload["overview"] = {
                "status": "completed",
                "input_length": len(overview_input),
                "raw_response": overview_response.get("raw"),
                "raw_text_response": overview_response.get("content"),
                "repaired": overview_response.get("repaired") is True,
                "normalized": overview,
            }
            artifact_payload["provisional_script"] = {
                "title": overview["title"],
                "global_instruction": overview["global_instruction"],
                "characters": overview["characters"],
                "segments": [],
            }
            persist()

        provisional_script = artifact_payload.get("provisional_script")
        if not isinstance(provisional_script, dict) or not provisional_script.get("title"):
            provisional_script = {
                "title": overview["title"],
                "global_instruction": overview["global_instruction"],
                "characters": overview["characters"],
                "segments": [],
            }
            artifact_payload["provisional_script"] = provisional_script
            persist()

        character_registry: dict[str, dict[str, Any]] = {
            item["id"]: item
            for item in (provisional_script.get("characters") or [])
            if isinstance(item, dict) and item.get("id") not in {None, "", "narrator"}
        }
        all_segments: list[dict[str, Any]] = [
            item for item in (provisional_script.get("segments") or []) if isinstance(item, dict)
        ]

        chunk_artifacts = sorted(
            [
                item
                for item in (artifact_payload.get("chunks") or [])
                if isinstance(item, dict) and isinstance(item.get("chunk_index"), int)
            ],
            key=lambda item: int(item["chunk_index"]),
        )
        completed_chunk_indices = {int(item["chunk_index"]) for item in chunk_artifacts}

        for chunk_entry in chunk_plan:
            chunk_index = int(chunk_entry["chunk_index"])
            if chunk_index in completed_chunk_indices:
                continue

            artifact_payload["phase"] = "chunks"
            artifact_payload["phase_details"] = {
                "current_chunk_index": chunk_index,
                "current_section_index": chunk_entry["section_index"],
                "current_section_title": chunk_entry["section_title"],
                "completed_chunks": len(completed_chunk_indices),
                "total_chunks": len(chunk_plan),
            }
            persist()

            known_characters = [narrator, *sorted(character_registry.values(), key=lambda item: item["id"])]
            chunk_response = call_openai_compatible_json(
                llm_config,
                llm_config["model"],
                build_script_chunk_messages(
                    chunk_text=chunk_entry["raw_text"],
                    chunk_index=chunk_index,
                    total_chunks=len(chunk_plan),
                    title=overview["title"],
                    global_instruction=overview["global_instruction"],
                    known_characters=known_characters,
                    section_title=chunk_entry["section_title"],
                ),
            )
            normalized_chunk = normalize_chunk_response(
                chunk_response["parsed"],
                current_registry=character_registry,
                chunk_index=chunk_index,
                section_index=int(chunk_entry["section_index"]),
                section_title=chunk_entry["section_title"],
            )
            all_segments.extend(normalized_chunk["segments"])
            provisional_script = {
                "title": overview["title"],
                "global_instruction": overview["global_instruction"],
                "characters": [narrator, *sorted(character_registry.values(), key=lambda item: item["id"])],
                "segments": reindex_segments(all_segments),
            }
            chunk_record = {
                "chunk_index": chunk_index,
                "section_index": int(chunk_entry["section_index"]),
                "section_title": chunk_entry["section_title"],
                "chunk_length": chunk_entry["chunk_length"],
                "raw_text": chunk_entry["raw_text"],
                "response_channel": chunk_response.get("channel"),
                "repaired": chunk_response.get("repaired") is True,
                "raw_response": chunk_response.get("raw"),
                "raw_text_response": chunk_response.get("content"),
                "normalized_segment_count": len(normalized_chunk["segments"]),
                "normalized_segments": normalized_chunk["segments"],
                "characters_snapshot": normalized_chunk["characters"],
                "completed_at": now_iso(),
            }
            chunk_artifacts = [item for item in chunk_artifacts if int(item["chunk_index"]) != chunk_index]
            chunk_artifacts.append(chunk_record)
            chunk_artifacts.sort(key=lambda item: int(item["chunk_index"]))
            completed_chunk_indices.add(chunk_index)

            artifact_payload["chunks"] = chunk_artifacts
            artifact_payload["provisional_script"] = provisional_script
            artifact_payload["phase_details"] = {
                "current_chunk_index": chunk_index,
                "current_section_index": chunk_entry["section_index"],
                "current_section_title": chunk_entry["section_title"],
                "completed_chunks": len(completed_chunk_indices),
                "total_chunks": len(chunk_plan),
            }
            persist()

        script_document = artifact_payload.get("provisional_script") or {
            "title": overview["title"],
            "global_instruction": overview["global_instruction"],
            "characters": [narrator, *sorted(character_registry.values(), key=lambda item: item["id"])],
            "segments": reindex_segments(all_segments),
        }

        existing_finalization = artifact_payload.get("finalization") or {}
        final_script_candidate = artifact_payload.get("final_script")
        if (
            isinstance(final_script_candidate, dict)
            and final_script_candidate.get("segments")
            and existing_finalization.get("status") in {"completed", "skipped"}
        ):
            final_script_document = final_script_candidate
            finalization_skipped_reason = trim_string(existing_finalization.get("skipped_reason"))
        else:
            finalization_payload = json.dumps(script_document, ensure_ascii=False, indent=2)
            artifact_payload["phase"] = "finalization"
            artifact_payload["provisional_script"] = script_document
            artifact_payload["finalization"] = {
                **existing_finalization,
                "status": "running",
                "enabled": len(finalization_payload) <= int(llm_config["finalize_max_input_chars"]),
                "input_length": len(finalization_payload),
            }
            persist()

            final_script_document = script_document
            if len(finalization_payload) <= int(llm_config["finalize_max_input_chars"]):
                finalization_result = call_openai_compatible_json(
                    llm_config,
                    llm_config["model"],
                    build_script_finalize_messages(
                        provisional_script=script_document,
                        chunk_count=len(chunk_plan),
                    ),
                )
                final_script_document = normalize_final_script_response(finalization_result["parsed"], input_path.stem)
                artifact_payload["finalization"] = {
                    "status": "completed",
                    "enabled": True,
                    "input_length": len(finalization_payload),
                    "skipped_reason": "",
                    "raw_response": finalization_result.get("raw"),
                    "raw_text_response": finalization_result.get("content"),
                    "repaired": finalization_result.get("repaired") is True,
                    "normalized": final_script_document,
                }
            else:
                finalization_skipped_reason = (
                    f"provisional script 过长（{len(finalization_payload)} 字符），超过 finalize_max_input_chars="
                    f"{llm_config['finalize_max_input_chars']}，本次跳过 final LLM reconciliation。"
                )
                artifact_payload["finalization"] = {
                    "status": "skipped",
                    "enabled": False,
                    "input_length": len(finalization_payload),
                    "skipped_reason": finalization_skipped_reason,
                    "raw_response": None,
                    "raw_text_response": "",
                    "repaired": False,
                    "normalized": final_script_document,
                }
            persist()

        save_yaml(output_path, final_script_document)
        artifact_payload["status"] = "completed"
        artifact_payload["phase"] = "completed"
        artifact_payload["final_script"] = final_script_document
        persist()

    except Exception as error:
        if artifact_payload:
            artifact_payload["status"] = "failed"
            artifact_payload["phase"] = artifact_payload.get("phase") or "failed"
            artifact_payload["last_error"] = str(error)
            artifact_payload["failed_at"] = now_iso()
            save_json(artifact_path, artifact_payload)
        raise

    refresh_story_artifact_manifest(
        story_input_path=input_path,
        effective_story_input_path=output_path,
        structured_script_artifact_path=artifact_path,
        library_path=library_path,
    )

    print(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "artifact_path": str(artifact_path),
                "chunk_count": len(chunk_plan),
                "requested_chunk_chars": llm_config["chunk_chars"],
                "effective_chunk_chars": effective_chunk_chars,
                "chapter_split_enabled": llm_config["chapter_split_enabled"],
                "section_count": len(sections),
                "character_count": len(final_script_document["characters"]),
                "segment_count": len(final_script_document["segments"]),
                "finalization_enabled": ((artifact_payload.get("finalization") or {}).get("enabled")) is True,
                "resumed_from_checkpoint": resumed_from_checkpoint,
                "model": llm_config["model"],
                "api_key_env": llm_config["api_key_env"],
                "api_key_source": api_key_info.get("source"),
                "base_url": llm_config["base_url"],
                "timeout_seconds": llm_config["timeout_seconds"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
