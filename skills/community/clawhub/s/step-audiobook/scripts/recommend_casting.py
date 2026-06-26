#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_LIBRARY_PATH,
    ensure_dir,
    get_story_base_name,
    load_yaml,
    load_yaml_if_exists,
    normalize_string_array,
    resolve_api_key,
    resolve_artifact_dir,
    resolve_story_workspace_dir,
    resolve_path,
    save_json,
    save_yaml,
    trim_string,
)
from llm_json import call_openai_compatible_json
from llm_tasks import (
    build_casting_role_profile_messages,
    build_casting_selection_messages,
    resolve_llm_task_config,
)
from story_artifacts import refresh_story_artifact_manifest


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def read_structured_input(file_path: Path) -> Any:
    ext = file_path.suffix.lower()
    if ext == ".json":
        return json.loads(file_path.read_text(encoding="utf-8"))
    if ext in {".yaml", ".yml"}:
        return load_yaml(file_path)
    return None


def load_input_source(input_path: Path) -> dict[str, Any]:
    ext = input_path.suffix.lower()
    raw_text = input_path.read_text(encoding="utf-8")
    if ext in {".yaml", ".yml", ".json"}:
        return {
            "kind": "structured",
            "data": read_structured_input(input_path),
            "raw_text": raw_text,
        }
    return {
        "kind": "text",
        "data": None,
        "raw_text": raw_text,
    }


def is_structured_input_path(input_path: Path) -> bool:
    return input_path.suffix.lower() in {".yaml", ".yml", ".json"}


def is_role_profile_document(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("roles"), list)


def is_dialogue_script_document(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("characters"), list) and isinstance(value.get("dialogues"), list)


def is_segment_script_document(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("characters"), list) and isinstance(value.get("segments"), list)


def take_sample_lines(values: Any, limit: int = 5) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values or []:
        text = trim_string(value)
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
        if len(result) >= limit:
            break
    return result


def resolve_role_type_hint(role_id: str, role_name: str, explicit_type: Any = None) -> str:
    normalized_type = trim_string(explicit_type)
    if normalized_type in {"narrator", "character"}:
        return normalized_type
    if role_id == "narrator":
        return "narrator"
    if trim_string(role_name).lower() in {"旁白", "narrator"}:
        return "narrator"
    return "character"


def build_role_evidence_from_dialogue_script(document: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = {}
    for dialogue in document.get("dialogues") or []:
        role_id = trim_string(str(dialogue.get("speaker") or ""))
        if not role_id:
            continue
        grouped.setdefault(role_id, []).append(trim_string(dialogue.get("text")))

    roles = []
    for character in document.get("characters") or []:
        role_id = trim_string(str(character.get("id") or ""))
        if not role_id:
            continue
        samples = grouped.get(role_id, [])
        roles.append(
            {
                "role_id": role_id,
                "role_name": trim_string(character.get("name")) or role_id,
                "role_type_hint": resolve_role_type_hint(
                    role_id,
                    trim_string(character.get("name")),
                    character.get("role_type"),
                ),
                "dialogue_count": len(samples),
                "character_instruction": trim_string(character.get("instruction")),
                "aliases": normalize_string_array(character.get("aliases")),
                "delivery_modes": ["narration"] if role_id == "narrator" else ["dialogue"],
                "sample_lines": take_sample_lines(samples),
            }
        )
    return roles


def build_role_evidence_from_segment_script(document: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = {}
    delivery_modes_by_role: dict[str, list[str]] = {}
    inline_cues_by_role: dict[str, list[str]] = {}
    scene_cues_by_role: dict[str, list[str]] = {}
    for segment in document.get("segments") or []:
        role_id = trim_string(str(segment.get("speaker") or ""))
        if not role_id:
            continue
        grouped.setdefault(role_id, []).append(
            trim_string(segment.get("clean_text") or segment.get("tts_input_text") or segment.get("raw_text"))
        )
        delivery_mode = trim_string(segment.get("delivery_mode"))
        if delivery_mode:
            delivery_modes_by_role.setdefault(role_id, []).append(delivery_mode)
        inline_instruction = trim_string(segment.get("inline_instruction"))
        if inline_instruction:
            inline_cues_by_role.setdefault(role_id, []).append(inline_instruction)
        scene_instruction = trim_string(segment.get("scene_instruction"))
        if scene_instruction:
            scene_cues_by_role.setdefault(role_id, []).append(scene_instruction)

    roles = []
    for character in document.get("characters") or []:
        role_id = trim_string(str(character.get("id") or ""))
        if not role_id:
            continue
        samples = grouped.get(role_id, [])
        roles.append(
            {
                "role_id": role_id,
                "role_name": trim_string(character.get("name")) or role_id,
                "role_type_hint": resolve_role_type_hint(
                    role_id,
                    trim_string(character.get("name")),
                    character.get("role_type"),
                ),
                "dialogue_count": len(samples),
                "character_instruction": trim_string(character.get("instruction")),
                "aliases": normalize_string_array(character.get("aliases")),
                "delivery_modes": take_sample_lines(delivery_modes_by_role.get(role_id), 3),
                "inline_cues": take_sample_lines(inline_cues_by_role.get(role_id), 4),
                "scene_cues": take_sample_lines(scene_cues_by_role.get(role_id), 4),
                "sample_lines": take_sample_lines(samples),
            }
        )
    return roles


def compact_candidate_for_prompt(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "asset_id": candidate.get("asset_id"),
        "source": candidate.get("source"),
        "availability": compute_candidate_availability(candidate),
        "information_quality": trim_string(candidate.get("information_quality")) or "unknown",
        "official_description": trim_string(candidate.get("official_description")),
        "official_recommended_scenes": normalize_string_array(
            candidate.get("recommended_scenes") or candidate.get("official_recommended_scenes")
        ),
        "selection_summary": trim_string(candidate.get("selection_summary")),
        "display_name": candidate.get("display_name"),
        "name_is_identifier_only": candidate.get("source") == "official",
        "review_status": candidate.get("review_status") or "unknown",
        "selected_for_clone": candidate.get("selected_for_clone") is True,
        "description": trim_string(candidate.get("description")),
        "tags": normalize_string_array(candidate.get("tags")),
        "suitable_scenes": normalize_string_array(candidate.get("suitable_scenes")),
        "avoid_scenes": normalize_string_array(candidate.get("avoid_scenes")),
        "stable_instruction": trim_string(candidate.get("stable_instruction")),
    }


def normalize_role_profile(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "role_id": trim_string(raw.get("role_id") or raw.get("id")),
        "role_name": trim_string(raw.get("role_name") or raw.get("name")),
        "role_type": trim_string(raw.get("role_type")) or "character",
        "dialogue_count": int(raw.get("dialogue_count") or 0),
        "role_summary": trim_string(raw.get("role_summary")),
        "desired_tags": normalize_string_array(raw.get("desired_tags")),
        "suitable_scenes": normalize_string_array(raw.get("suitable_scenes") or raw.get("frequent_scenes")),
        "avoid_scenes": normalize_string_array(raw.get("avoid_scenes")),
        "current_instruction": trim_string(
            raw.get("current_instruction") or raw.get("stable_instruction_hint") or raw.get("instruction")
        ),
        "sample_lines": take_sample_lines(raw.get("sample_lines") or raw.get("evidence_lines")),
    }


def normalize_lookup_key(value: Any) -> str:
    return trim_string(value).casefold()


def build_role_anchor_maps(source_role_evidence: list[dict[str, Any]]) -> dict[str, Any]:
    by_role_id: dict[str, dict[str, Any]] = {}
    by_name_or_alias: dict[str, list[dict[str, Any]]] = {}
    ordered: list[dict[str, Any]] = []
    for item in source_role_evidence or []:
        role_id = trim_string(item.get("role_id"))
        if not role_id:
            continue
        role_name = trim_string(item.get("role_name")) or role_id
        normalized = {
            "role_id": role_id,
            "role_name": role_name,
            "role_type": resolve_role_type_hint(role_id, role_name, item.get("role_type_hint") or item.get("role_type")),
            "dialogue_count": int(item.get("dialogue_count") or 0),
            "current_instruction": trim_string(item.get("character_instruction") or item.get("current_instruction")),
            "aliases": normalize_string_array(item.get("aliases")),
            "sample_lines": take_sample_lines(item.get("sample_lines")),
        }
        by_role_id[normalize_lookup_key(role_id)] = normalized
        ordered.append(normalized)
        for token in [role_id, role_name, *(normalized.get("aliases") or [])]:
            key = normalize_lookup_key(token)
            if not key:
                continue
            by_name_or_alias.setdefault(key, []).append(normalized)
    return {"ordered": ordered, "by_role_id": by_role_id, "by_name_or_alias": by_name_or_alias}


def resolve_role_anchor(profile: dict[str, Any], anchor_maps: dict[str, Any]) -> dict[str, Any] | None:
    for token in [profile.get("role_id"), profile.get("role_name")]:
        key = normalize_lookup_key(token)
        if not key:
            continue
        if key in anchor_maps["by_role_id"]:
            return anchor_maps["by_role_id"][key]
        candidates = anchor_maps["by_name_or_alias"].get(key) or []
        if len(candidates) == 1:
            return candidates[0]
    return None


def merge_role_profiles(primary: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
    merged = dict(primary)
    merged["role_name"] = trim_string(primary.get("role_name")) or trim_string(secondary.get("role_name")) or merged.get("role_id")
    merged["role_type"] = trim_string(primary.get("role_type")) or trim_string(secondary.get("role_type")) or "character"
    merged["dialogue_count"] = max(int(primary.get("dialogue_count") or 0), int(secondary.get("dialogue_count") or 0))
    merged["role_summary"] = trim_string(primary.get("role_summary")) or trim_string(secondary.get("role_summary"))
    merged["current_instruction"] = trim_string(primary.get("current_instruction")) or trim_string(secondary.get("current_instruction"))
    merged["desired_tags"] = normalize_string_array((primary.get("desired_tags") or []) + (secondary.get("desired_tags") or []))
    merged["suitable_scenes"] = normalize_string_array((primary.get("suitable_scenes") or []) + (secondary.get("suitable_scenes") or []))
    merged["avoid_scenes"] = normalize_string_array((primary.get("avoid_scenes") or []) + (secondary.get("avoid_scenes") or []))
    merged["sample_lines"] = take_sample_lines((primary.get("sample_lines") or []) + (secondary.get("sample_lines") or []))
    return merged


def build_fallback_role_profile(anchor: dict[str, Any]) -> dict[str, Any]:
    role_name = trim_string(anchor.get("role_name")) or trim_string(anchor.get("role_id"))
    current_instruction = trim_string(anchor.get("current_instruction"))
    summary = f"{role_name} 的声音画像待人工补充。"
    if current_instruction:
        summary = current_instruction
    return {
        "role_id": trim_string(anchor.get("role_id")),
        "role_name": role_name,
        "role_type": trim_string(anchor.get("role_type")) or "character",
        "dialogue_count": int(anchor.get("dialogue_count") or 0),
        "role_summary": summary,
        "desired_tags": [],
        "suitable_scenes": [],
        "avoid_scenes": [],
        "current_instruction": current_instruction,
        "sample_lines": take_sample_lines(anchor.get("sample_lines")),
    }


def anchor_role_profiles_to_source(role_profiles: list[dict[str, Any]], source_role_evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not source_role_evidence:
        return role_profiles

    anchor_maps = build_role_anchor_maps(source_role_evidence)
    merged_by_role_id: dict[str, dict[str, Any]] = {}
    unmatched_profiles: list[dict[str, Any]] = []

    for profile in role_profiles:
        anchor = resolve_role_anchor(profile, anchor_maps)
        if not anchor:
            unmatched_profiles.append(profile)
            continue
        anchored_profile = {
            **profile,
            "role_id": anchor["role_id"],
            "role_name": anchor["role_name"],
            "role_type": resolve_role_type_hint(anchor["role_id"], anchor["role_name"], profile.get("role_type") or anchor.get("role_type")),
            "dialogue_count": max(int(profile.get("dialogue_count") or 0), int(anchor.get("dialogue_count") or 0)),
            "current_instruction": trim_string(profile.get("current_instruction")) or trim_string(anchor.get("current_instruction")),
            "sample_lines": take_sample_lines((profile.get("sample_lines") or []) + (anchor.get("sample_lines") or [])),
        }
        existing = merged_by_role_id.get(anchor["role_id"])
        merged_by_role_id[anchor["role_id"]] = merge_role_profiles(anchored_profile, existing or {})

    ordered_profiles: list[dict[str, Any]] = []
    for anchor in anchor_maps["ordered"]:
        role_id = anchor["role_id"]
        ordered_profiles.append(merged_by_role_id.pop(role_id, build_fallback_role_profile(anchor)))

    ordered_profiles.extend(unmatched_profiles)
    ordered_profiles.extend(merged_by_role_id.values())
    return ordered_profiles


def build_artifacts_base_dir(output_path: Path) -> Path:
    return resolve_artifact_dir(output_path)


def get_casting_base_name(output_path: Path) -> str:
    base = output_path.stem
    return base[: -len(".casting-plan")] if base.endswith(".casting-plan") else base


def get_role_profiles_artifact_path(output_path: Path) -> Path:
    return build_artifacts_base_dir(output_path) / f"{output_path.stem}.role-profiles.json"


def get_casting_response_artifact_path(output_path: Path) -> Path:
    return build_artifacts_base_dir(output_path) / f"{output_path.stem}.casting-selection.json"


def get_casting_review_path(output_path: Path) -> Path:
    return output_path.parent / f"{get_casting_base_name(output_path)}.casting-review.yaml"


def get_clone_review_path(output_path: Path) -> Path:
    return output_path.parent / f"{get_casting_base_name(output_path)}.clone-review.yaml"


def resolve_default_casting_plan_path(input_path: Path) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.casting-plan.yaml"


def build_casting_config(args: argparse.Namespace, library: dict[str, Any]) -> dict[str, Any]:
    config = library.get("casting") or {}
    llm = config.get("llm") or {}
    output = config.get("output") or {}
    role_llm = resolve_llm_task_config(
        library,
        "casting_role_extraction",
        cli_overrides={
            "api_key_env": args.api_key_env,
            "base_url": args.base_url,
            "model": args.role_model or args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        },
        legacy_config={
            **llm,
            "model": args.role_model or llm.get("role_model") or args.model or llm.get("model"),
        },
    )
    selection_llm = resolve_llm_task_config(
        library,
        "casting_selection",
        cli_overrides={
            "api_key_env": args.api_key_env,
            "base_url": args.base_url,
            "model": args.selection_model or args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        },
        legacy_config={
            **llm,
            "model": args.selection_model or llm.get("selection_model") or args.model or llm.get("model"),
        },
    )
    return {
        "source_of_truth": config.get("source_of_truth") or "candidate_pool_only",
        "role_extraction_mode": config.get("role_extraction_mode") or "llm",
        "selection_mode": config.get("selection_mode") or "llm",
        "output": {
            "top_candidates_per_role": int(args.top_candidates or output.get("top_candidates_per_role") or 5),
            "save_intermediate_json": output.get("save_intermediate_json") is not False,
        },
        "role_llm": role_llm,
        "selection_llm": selection_llm,
    }
def extract_role_profiles_from_source(source: dict[str, Any], llm_config: dict[str, Any]) -> dict[str, Any]:
    source_role_evidence: list[dict[str, Any]] = []
    if source["kind"] == "structured" and is_role_profile_document(source["data"]):
        return {
            "mode": "provided_role_profiles",
            "raw_response": None,
            "repaired": False,
            "role_profiles": [normalize_role_profile(item) for item in (source["data"].get("roles") or []) if trim_string(item.get("role_id") or item.get("id"))],
        }

    if source["kind"] == "structured" and is_dialogue_script_document(source["data"]):
        source_role_evidence = build_role_evidence_from_dialogue_script(source["data"])
        user_payload = json.dumps(
            {
                "source_type": "dialogue_script",
                "title": trim_string(source["data"].get("title")),
                "global_instruction": trim_string(source["data"].get("global_instruction")),
                "role_evidence": source_role_evidence,
            },
            ensure_ascii=False,
            indent=2,
        )
    elif source["kind"] == "structured" and is_segment_script_document(source["data"]):
        source_role_evidence = build_role_evidence_from_segment_script(source["data"])
        user_payload = json.dumps(
            {
                "source_type": "parsed_segment_script",
                "title": trim_string(source["data"].get("title")),
                "global_instruction": trim_string(source["data"].get("global_instruction")),
                "role_evidence": source_role_evidence,
            },
            ensure_ascii=False,
            indent=2,
        )
    elif source["kind"] == "structured":
        user_payload = json.dumps({"source_type": "generic_structured_document", "document": source["data"]}, ensure_ascii=False, indent=2)
    else:
        user_payload = source["raw_text"]

    response = call_openai_compatible_json(
        llm_config,
        llm_config["model"],
        build_casting_role_profile_messages(user_payload),
    )

    roles = [normalize_role_profile(item) for item in (response["parsed"].get("roles") or []) if trim_string(item.get("role_id") or item.get("id"))]
    roles = anchor_role_profiles_to_source(roles, source_role_evidence)
    if not roles:
        raise RuntimeError("角色画像提取结果为空")
    return {
        "mode": "llm_extracted",
        "raw_response": response,
        "repaired": response.get("repaired") is True,
        "title": trim_string(response["parsed"].get("title")),
        "role_profiles": roles,
    }


def build_candidate_maps(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    by_asset_id: dict[str, dict[str, Any]] = {}
    by_display_name: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        by_key[f"{candidate.get('source')}:{candidate.get('asset_id')}"] = candidate
        by_asset_id.setdefault(candidate.get("asset_id"), candidate)
        by_display_name.setdefault(candidate.get("display_name"), candidate)
    return {
        "by_key": by_key,
        "by_asset_id": by_asset_id,
        "by_display_name": by_display_name,
    }


def resolve_candidate_reference(item: Any, candidate_maps: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    source = trim_string(item.get("source") or item.get("selected_source"))
    asset_id = trim_string(item.get("asset_id") or item.get("selected_asset_id"))
    display_name = trim_string(item.get("display_name") or item.get("selected_display_name"))
    if source and asset_id and f"{source}:{asset_id}" in candidate_maps["by_key"]:
        return candidate_maps["by_key"][f"{source}:{asset_id}"]
    if asset_id and asset_id in candidate_maps["by_asset_id"]:
        return candidate_maps["by_asset_id"][asset_id]
    if display_name and display_name in candidate_maps["by_display_name"]:
        return candidate_maps["by_display_name"][display_name]
    return None


def compute_candidate_availability(candidate: dict[str, Any]) -> str:
    if candidate.get("source") == "official":
        return "ready"
    return "ready" if candidate.get("voice_id") and trim_string(candidate.get("status")) == "ready" else "requires_paid_clone"


def build_recommended_candidate_entry(candidate: dict[str, Any], reason: Any) -> dict[str, Any]:
    return {
        "asset_id": candidate.get("asset_id"),
        "source": candidate.get("source"),
        "display_name": candidate.get("display_name"),
        "availability": compute_candidate_availability(candidate),
        "information_quality": trim_string(candidate.get("information_quality")) or "unknown",
        "status": candidate.get("status") or "unknown",
        "voice_id": candidate.get("voice_id") or "",
        "selected_for_clone": candidate.get("selected_for_clone") is True,
        "reason": trim_string(reason),
        "description": trim_string(candidate.get("description")),
        "official_description": trim_string(candidate.get("official_description")),
        "tags": normalize_string_array(candidate.get("tags")),
        "suitable_scenes": normalize_string_array(candidate.get("suitable_scenes")),
        "recommended_scenes": normalize_string_array(
            candidate.get("recommended_scenes") or candidate.get("official_recommended_scenes")
        ),
        "avoid_scenes": normalize_string_array(candidate.get("avoid_scenes")),
        "stable_instruction": trim_string(candidate.get("stable_instruction")),
        "selection_summary": trim_string(candidate.get("selection_summary")),
    }


def create_empty_casting_manual() -> dict[str, Any]:
    return {
        "selected_asset_id": "",
        "selected_source": "",
        "stable_instruction": "",
        "notes": "",
    }


def normalize_casting_manual(value: Any) -> dict[str, Any]:
    manual = value or {}
    return {
        "selected_asset_id": trim_string(manual.get("selected_asset_id")),
        "selected_source": trim_string(manual.get("selected_source")),
        "stable_instruction": trim_string(manual.get("stable_instruction")),
        "notes": trim_string(manual.get("notes")),
    }


def has_manual_casting_candidate(manual: dict[str, Any]) -> bool:
    return bool(trim_string(manual.get("selected_asset_id")) and trim_string(manual.get("selected_source")))


def has_manual_casting_content(manual: dict[str, Any]) -> bool:
    return bool(has_manual_casting_candidate(manual) or trim_string(manual.get("stable_instruction")) or trim_string(manual.get("notes")))


def build_casting_review_state(manual: dict[str, Any], generated_at: str) -> dict[str, Any]:
    return {
        "status": "manual_override_present" if has_manual_casting_content(manual) else "pending_manual_review",
        "edit_target": "manual",
        "compare_against": "recommended",
        "last_recommended_at": generated_at,
    }


def create_empty_clone_review_manual() -> dict[str, Any]:
    return {"decision": "pending", "notes": ""}


def normalize_clone_review_manual(value: Any) -> dict[str, Any]:
    manual = value or {}
    decision = trim_string(manual.get("decision")) or "pending"
    return {
        "decision": decision if decision in {"pending", "confirm_clone", "skip"} else "pending",
        "notes": trim_string(manual.get("notes")),
    }


def build_clone_review_state(manual: dict[str, Any]) -> dict[str, Any]:
    if manual["decision"] == "confirm_clone":
        return {"status": "confirm_clone_requested", "next_step": "set_library_selected_for_clone_true"}
    if manual["decision"] == "skip":
        return {"status": "skipped_by_user", "next_step": "no_action"}
    return {"status": "pending_clone_confirmation", "next_step": "await_user_confirmation"}


def sync_clone_review_decisions_to_library(library: dict[str, Any], clone_review_store: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(library, dict):
        return {"changed": False, "applied": [], "missing": []}
    library.setdefault("clones", {})
    applied = []
    missing = []
    changed = False
    for asset_id, entry in (clone_review_store.get("items") or {}).items():
        manual = normalize_clone_review_manual((entry or {}).get("manual") or create_empty_clone_review_manual())
        if manual["decision"] == "pending":
            continue
        target_value = manual["decision"] == "confirm_clone"
        clone_entry = library["clones"].get(asset_id)
        if not isinstance(clone_entry, dict):
            missing.append({"asset_id": asset_id, "decision": manual["decision"]})
            continue
        had_explicit_value = "selected_for_clone" in clone_entry
        previous_value = clone_entry.get("selected_for_clone") is True
        clone_entry["selected_for_clone"] = target_value
        did_change = (not had_explicit_value) or previous_value != target_value
        if did_change:
            changed = True
        applied.append(
            {
                "asset_id": asset_id,
                "decision": manual["decision"],
                "selected_for_clone": target_value,
                "changed": did_change,
            }
        )
    return {"changed": changed, "applied": applied, "missing": missing}


def select_casting_with_llm(role_profiles: list[dict[str, Any]], candidates: list[dict[str, Any]], llm_config: dict[str, Any]) -> dict[str, Any]:
    candidate_payload = [compact_candidate_for_prompt(candidate) for candidate in candidates]
    return call_openai_compatible_json(
        llm_config,
        llm_config["model"],
        build_casting_selection_messages(role_profiles, candidate_payload),
    )


def collect_unresolved_role_profiles(selection_response: dict[str, Any], role_profiles: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_maps = build_candidate_maps(candidates)
    response_roles = selection_response.get("parsed", {}).get("roles") or []
    selection_by_role_id = {trim_string(item.get("role_id")): item for item in response_roles if trim_string(item.get("role_id"))}
    selection_by_role_name = {trim_string(item.get("role_name")): item for item in response_roles if trim_string(item.get("role_name"))}

    unresolved = []
    for profile in role_profiles:
        raw_selection = selection_by_role_id.get(profile["role_id"]) or selection_by_role_name.get(profile["role_name"]) or {}
        selected_candidate = resolve_candidate_reference(raw_selection, candidate_maps)
        raw_recommended = raw_selection.get("recommended_candidates") if isinstance(raw_selection.get("recommended_candidates"), list) else []
        has_recommended = any(resolve_candidate_reference(item, candidate_maps) for item in raw_recommended)
        if not selected_candidate or not has_recommended:
            unresolved.append(profile)
    return unresolved


def merge_selection_responses(base_response: dict[str, Any], patch_response: dict[str, Any]) -> dict[str, Any]:
    merged_map: dict[str, dict[str, Any]] = {}
    for item in (base_response.get("parsed", {}).get("roles") or []):
        key = trim_string(item.get("role_id") or item.get("role_name"))
        if key:
            merged_map[key] = item
    for item in (patch_response.get("parsed", {}).get("roles") or []):
        key = trim_string(item.get("role_id") or item.get("role_name"))
        if key:
            merged_map[key] = item
    summary = trim_string(base_response.get("parsed", {}).get("summary")) or trim_string(patch_response.get("parsed", {}).get("summary"))
    roles = list(merged_map.values())
    return {
        "raw": {"primary": base_response.get("raw"), "patch": patch_response.get("raw")},
        "content": json.dumps({"summary": summary, "roles": roles}, ensure_ascii=False),
        "channel": "merged",
        "parsed": {"summary": summary, "roles": roles},
        "repaired": base_response.get("repaired") is True or patch_response.get("repaired") is True,
        "repaired_raw": {"primary": base_response.get("repaired_raw"), "patch": patch_response.get("repaired_raw")},
        "repaired_content": json.dumps(
            {"primary": base_response.get("repaired_content") or "", "patch": patch_response.get("repaired_content") or ""},
            ensure_ascii=False,
        ),
    }


def normalize_casting_selection(selection_response: dict[str, Any], role_profiles: list[dict[str, Any]], candidates: list[dict[str, Any]], top_n: int) -> dict[str, Any]:
    candidate_maps = build_candidate_maps(candidates)
    response_roles = selection_response.get("parsed", {}).get("roles") or []
    selection_by_role_id = {trim_string(item.get("role_id")): item for item in response_roles if trim_string(item.get("role_id"))}
    selection_by_role_name = {trim_string(item.get("role_name")): item for item in response_roles if trim_string(item.get("role_name"))}

    roles = []
    for profile in role_profiles:
        raw_selection = selection_by_role_id.get(profile["role_id"]) or selection_by_role_name.get(profile["role_name"]) or {}
        selected_candidate = resolve_candidate_reference(raw_selection, candidate_maps)
        raw_recommended = raw_selection.get("recommended_candidates") if isinstance(raw_selection.get("recommended_candidates"), list) else []
        recommended = []
        seen: set[str] = set()
        for item in raw_recommended:
            candidate = resolve_candidate_reference(item, candidate_maps)
            if not candidate:
                continue
            key = f"{candidate.get('source')}:{candidate.get('asset_id')}"
            if key in seen:
                continue
            seen.add(key)
            recommended.append(build_recommended_candidate_entry(candidate, item.get("reason")))
            if len(recommended) >= top_n:
                break
        final_selected = selected_candidate or (
            candidate_maps["by_key"].get(f"{recommended[0]['source']}:{recommended[0]['asset_id']}") if recommended else None
        )
        if not final_selected:
            raise RuntimeError(f"角色 {profile['role_id']} 缺少可用选角结果")
        final_selected_key = f"{final_selected.get('source')}:{final_selected.get('asset_id')}"
        if final_selected_key not in seen:
            recommended.insert(0, build_recommended_candidate_entry(final_selected, raw_selection.get("selected_reason")))
        selected_reason = trim_string(raw_selection.get("selected_reason")) if selected_candidate else (recommended[0].get("reason") or "LLM 选择的主候选无效，已回退到首个有效备选。")
        roles.append(
            {
                **profile,
                "selected_asset_id": final_selected.get("asset_id"),
                "selected_source": final_selected.get("source"),
                "selected_display_name": final_selected.get("display_name"),
                "selected_status": compute_candidate_availability(final_selected),
                "selected_voice_id": final_selected.get("voice_id") or "",
                "selected_reason": selected_reason or "LLM 未提供说明，使用首个有效候选兜底。",
                "stable_instruction": trim_string(raw_selection.get("stable_instruction")) or trim_string(final_selected.get("stable_instruction")) or profile.get("current_instruction"),
                "candidates": recommended[:top_n],
            }
        )
    return {"summary": trim_string(selection_response.get("parsed", {}).get("summary")), "roles": roles}


def build_normalized_summary(normalized_roles: list[dict[str, Any]]) -> str:
    parts = []
    for role in normalized_roles:
        status_suffix = "可直接用" if role.get("selected_status") == "ready" else "需先付费 clone"
        parts.append(f"{role.get('role_name')} -> {role.get('selected_display_name')}（{role.get('selected_source')}，{status_suffix}）")
    return "；".join(parts)


def build_clone_actions(normalized_roles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clone_map: dict[str, dict[str, Any]] = {}
    for role in normalized_roles:
        asset_id = trim_string(role.get("pending_clone_asset_id"))
        display_name = trim_string(role.get("pending_clone_display_name"))
        current_status = trim_string(role.get("pending_clone_status"))
        recommendation_reason = trim_string(role.get("pending_clone_reason"))
        if not asset_id:
            if role.get("selected_source") != "clone" or role.get("selected_status") == "ready":
                continue
            asset_id = role.get("selected_asset_id")
            display_name = role.get("selected_display_name")
            current_status = role.get("selected_status")
            recommendation_reason = trim_string(role.get("selected_reason"))
        clone_map.setdefault(
            asset_id,
            {
                "asset_id": asset_id,
                "display_name": display_name,
                "current_status": current_status or "requires_paid_clone",
                "linked_roles": [],
                "recommendation_reason": [],
            },
        )
        clone_map[asset_id]["linked_roles"].append(role.get("role_name"))
        if recommendation_reason:
            clone_map[asset_id]["recommendation_reason"].append(recommendation_reason)
    return [
        {
            "asset_id": item["asset_id"],
            "display_name": item["display_name"],
            "current_status": item["current_status"],
            "linked_roles": item["linked_roles"],
            "recommendation_reason": item["recommendation_reason"][0] if item["recommendation_reason"] else "",
        }
        for item in clone_map.values()
    ]


def build_casting_review_store(params: dict[str, Any]) -> dict[str, Any]:
    generated_at = now_iso()
    existing_roles = (params.get("existingStore") or {}).get("roles") or {}
    roles = {}
    for role in params["normalizedSelection"]["roles"]:
        existing_entry = existing_roles.get(role["role_id"], {})
        manual = normalize_casting_manual(existing_entry.get("manual") or create_empty_casting_manual())
        roles[role["role_id"]] = {
            "role_name": role.get("role_name"),
            "role_type": role.get("role_type"),
            "dialogue_count": role.get("dialogue_count"),
            "role_summary": role.get("role_summary"),
            "desired_tags": normalize_string_array(role.get("desired_tags")),
            "suitable_scenes": normalize_string_array(role.get("suitable_scenes")),
            "avoid_scenes": normalize_string_array(role.get("avoid_scenes")),
            "current_instruction": trim_string(role.get("current_instruction")),
            "sample_lines": take_sample_lines(role.get("sample_lines"), 8),
            "recommended": {
                "selected_asset_id": role.get("selected_asset_id"),
                "selected_source": role.get("selected_source"),
                "selected_display_name": role.get("selected_display_name"),
                "selected_status": role.get("selected_status"),
                "selected_voice_id": role.get("selected_voice_id") or "",
                "selected_reason": trim_string(role.get("selected_reason")),
                "stable_instruction": trim_string(role.get("stable_instruction")),
                "candidates": role.get("candidates") or [],
            },
            "manual": manual,
            "review": build_casting_review_state(manual, generated_at),
        }
    return {
        "version": "1",
        "generated_at": generated_at,
        "source_input_path": str(params["inputPath"]),
        "candidate_pool_path": str(params["candidatePoolPath"]),
        "role_profiles_path": str(params["roleProfilesPath"]),
        "casting_response_path": str(params["castingResponsePath"]),
        "effective_plan_path": str(params["effectivePlanPath"]),
        "clone_review_path": str(params["cloneReviewPath"]),
        "llm": params["llmMeta"],
        "roles": roles,
    }


def resolve_effective_candidate_from_review(role_id: str, entry: dict[str, Any], candidate_maps: dict[str, dict[str, Any]]) -> dict[str, Any]:
    manual = normalize_casting_manual(entry.get("manual"))
    if has_manual_casting_candidate(manual):
        manual_candidate = resolve_candidate_reference(
            {"selected_source": manual["selected_source"], "selected_asset_id": manual["selected_asset_id"]},
            candidate_maps,
        )
        if not manual_candidate:
            raise RuntimeError(f"角色 {role_id} 的 manual 选角无效: {manual['selected_source']}:{manual['selected_asset_id']}")
        return {"candidate": manual_candidate, "source": "manual", "manual": manual}

    recommended = entry.get("recommended") or {}
    recommended_candidate = resolve_candidate_reference(
        {
            "selected_source": recommended.get("selected_source"),
            "selected_asset_id": recommended.get("selected_asset_id"),
            "selected_display_name": recommended.get("selected_display_name"),
        },
        candidate_maps,
    )
    if not recommended_candidate:
        raise RuntimeError(f"角色 {role_id} 的 recommended 选角已无法在候选池中找到，请重新执行 recommend-casting")
    return {"candidate": recommended_candidate, "source": "recommended", "manual": manual}


def resolve_ready_recommended_fallback(entry: dict[str, Any], candidate_maps: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    recommended = entry.get("recommended") or {}
    for item in recommended.get("candidates") or []:
        candidate = resolve_candidate_reference(item, candidate_maps)
        if not candidate:
            continue
        if compute_candidate_availability(candidate) == "ready":
            return candidate
    return None


def build_effective_plan_from_review(review_store: dict[str, Any], candidates: list[dict[str, Any]], output_path: Path, clone_review_path: Path) -> dict[str, Any]:
    candidate_maps = build_candidate_maps(candidates)
    roles = []
    for role_id, entry in (review_store.get("roles") or {}).items():
        effective_candidate = resolve_effective_candidate_from_review(role_id, entry, candidate_maps)
        recommended = entry.get("recommended") or {}
        candidate = effective_candidate["candidate"]
        selected_candidate_source = effective_candidate["source"]
        pending_clone_candidate: dict[str, Any] | None = None

        # If the LLM recommends a paid clone but the user has not manually forced it,
        # keep the clone as a review target while falling back to a ready candidate so
        # the downstream TTS chain can continue.
        if (
            effective_candidate["source"] != "manual"
            and compute_candidate_availability(candidate) != "ready"
        ):
            fallback_candidate = resolve_ready_recommended_fallback(entry, candidate_maps)
            if fallback_candidate:
                pending_clone_candidate = candidate
                candidate = fallback_candidate
                selected_candidate_source = "recommended_ready_fallback"

        stable_instruction = trim_string(effective_candidate["manual"].get("stable_instruction")) or trim_string(recommended.get("stable_instruction")) or trim_string(entry.get("current_instruction"))
        stable_instruction_source = (
            "manual"
            if trim_string(effective_candidate["manual"].get("stable_instruction"))
            else "recommended"
            if trim_string(recommended.get("stable_instruction"))
            else "role_profile"
        )
        fallback_reason = ""
        if pending_clone_candidate:
            fallback_reason = (
                f"推荐 clone {pending_clone_candidate.get('display_name') or pending_clone_candidate.get('asset_id')} 仍需付费复刻，"
                f"当前先回退到可直接使用的 {candidate.get('display_name') or candidate.get('asset_id')}。"
            )
        roles.append(
            {
                "role_id": role_id,
                "role_name": trim_string(entry.get("role_name")),
                "role_type": trim_string(entry.get("role_type")) or "character",
                "dialogue_count": int(entry.get("dialogue_count") or 0),
                "role_summary": trim_string(entry.get("role_summary")),
                "desired_tags": normalize_string_array(entry.get("desired_tags")),
                "suitable_scenes": normalize_string_array(entry.get("suitable_scenes")),
                "avoid_scenes": normalize_string_array(entry.get("avoid_scenes")),
                "current_instruction": trim_string(entry.get("current_instruction")),
                "sample_lines": take_sample_lines(entry.get("sample_lines"), 8),
                "selected_asset_id": candidate.get("asset_id"),
                "selected_source": candidate.get("source"),
                "selected_display_name": candidate.get("display_name"),
                "selected_status": compute_candidate_availability(candidate),
                "selected_voice_id": candidate.get("voice_id") or "",
                "selected_reason": (
                    trim_string(effective_candidate["manual"].get("notes")) or "来自 casting-review.yaml 的人工改选。"
                    if effective_candidate["source"] == "manual"
                    else fallback_reason or trim_string(recommended.get("selected_reason"))
                ),
                "stable_instruction": stable_instruction,
                "notes": trim_string(effective_candidate["manual"].get("notes")),
                "sources": {
                    "selected_candidate": selected_candidate_source,
                    "stable_instruction": stable_instruction_source,
                    "notes": "manual" if trim_string(effective_candidate["manual"].get("notes")) else "empty",
                },
                "review_status": ((entry.get("review") or {}).get("status")) or "pending_manual_review",
                "candidates": recommended.get("candidates") if isinstance(recommended.get("candidates"), list) else [],
                "pending_clone_asset_id": pending_clone_candidate.get("asset_id") if pending_clone_candidate else "",
                "pending_clone_source": pending_clone_candidate.get("source") if pending_clone_candidate else "",
                "pending_clone_display_name": pending_clone_candidate.get("display_name") if pending_clone_candidate else "",
                "pending_clone_status": compute_candidate_availability(pending_clone_candidate) if pending_clone_candidate else "",
                "pending_clone_reason": trim_string(recommended.get("selected_reason")) if pending_clone_candidate else "",
            }
        )
    return {
        "version": "2",
        "generated_at": now_iso(),
        "source_input_path": review_store.get("source_input_path") or "",
        "candidate_pool_path": review_store.get("candidate_pool_path") or "",
        "casting_review_path": str(get_casting_review_path(output_path)),
        "clone_review_path": str(clone_review_path),
        "llm": review_store.get("llm") or {},
        "summary": build_normalized_summary(roles),
        "roles": roles,
    }


def build_clone_review_store(effective_plan: dict[str, Any], existing_clone_review: dict[str, Any], library_clones: dict[str, Any] | None = None) -> dict[str, Any]:
    existing_items = (existing_clone_review or {}).get("items") or {}
    library_clones = library_clones or {}
    grouped: dict[str, dict[str, Any]] = {}
    for role in effective_plan.get("roles") or []:
        asset_id = trim_string(role.get("pending_clone_asset_id"))
        display_name = trim_string(role.get("pending_clone_display_name"))
        current_status = trim_string(role.get("pending_clone_status"))
        recommendation_reason = trim_string(role.get("pending_clone_reason"))
        if not asset_id:
            if role.get("selected_source") != "clone" or role.get("selected_status") == "ready":
                continue
            asset_id = role.get("selected_asset_id")
            display_name = role.get("selected_display_name")
            current_status = role.get("selected_status")
            recommendation_reason = trim_string(role.get("selected_reason"))
        grouped.setdefault(
            asset_id,
            {
                "asset_id": asset_id,
                "display_name": display_name,
                "linked_roles": [],
                "recommendation_reason": [],
                "current_status": current_status or "requires_paid_clone",
            },
        )
        grouped[asset_id]["linked_roles"].append(role.get("role_name"))
        if recommendation_reason:
            grouped[asset_id]["recommendation_reason"].append(recommendation_reason)
    items = {}
    for asset_id, item in grouped.items():
        existing = existing_items.get(asset_id) or {}
        manual = normalize_clone_review_manual(existing.get("manual") or create_empty_clone_review_manual())
        items[asset_id] = {
            "display_name": item.get("display_name"),
            "current_status": item.get("current_status") or "requires_paid_clone",
            "library_selected_for_clone": ((library_clones.get(asset_id) or {}).get("selected_for_clone")) is True,
            "linked_roles": item.get("linked_roles") or [],
            "recommendation_reason": (item.get("recommendation_reason") or [""])[0],
            "action_target": f"voice-library.yaml -> clones.{asset_id}.selected_for_clone",
            "manual": manual,
            "review": build_clone_review_state(manual),
        }
    return {
        "version": "1",
        "generated_at": now_iso(),
        "source_effective_plan_summary": effective_plan.get("summary") or "",
        "items": items,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend audiobook voice casting from unified candidate pool.")
    parser.add_argument("--input", required=True, help="Input story/script path")
    parser.add_argument("--output", help="Output casting-plan.yaml path")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--model")
    parser.add_argument("--role-model", dest="role_model")
    parser.add_argument("--selection-model", dest="selection_model")
    parser.add_argument("--base-url", dest="base_url")
    parser.add_argument("--api-key-env", dest="api_key_env")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--max-tokens", dest="max_tokens")
    parser.add_argument("--top-candidates", dest="top_candidates")
    parser.add_argument("--refresh-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    library_path = Path(args.library).resolve()
    library_dir = library_path.parent
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise RuntimeError(f"输入文件不存在: {input_path}")

    library = load_yaml_if_exists(library_path, {}) or {}
    candidate_pool_path = resolve_path(library_dir, ((library.get("paths") or {}).get("candidate_pool_file")) or ".audiobook/voice-candidate-pool.yaml")
    if not candidate_pool_path.exists():
        raise RuntimeError(f"缺少统一候选池，请先执行 sync_voice_library.py: {candidate_pool_path}")
    candidate_pool = load_yaml(candidate_pool_path)
    candidates = candidate_pool.get("voices") or []
    if not candidates:
        raise RuntimeError(f"统一候选池为空: {candidate_pool_path}")

    casting_config = build_casting_config(args, library)
    if casting_config["source_of_truth"] != "candidate_pool_only":
        raise RuntimeError(f"当前 recommend-casting 只支持 candidate_pool_only，实际为 {casting_config['source_of_truth']}")

    output_path = Path(args.output).resolve() if args.output else resolve_default_casting_plan_path(input_path)
    role_profiles_path = get_role_profiles_artifact_path(output_path)
    casting_response_path = get_casting_response_artifact_path(output_path)
    casting_review_path = get_casting_review_path(output_path)
    clone_review_path = get_clone_review_path(output_path)
    ensure_dir(output_path.parent)
    ensure_dir(role_profiles_path.parent)

    if args.refresh_only:
        review_store = load_yaml_if_exists(casting_review_path, None)
        if review_store is None:
            raise RuntimeError(f"缺少 casting review 文件，无法 refresh-only: {casting_review_path}")
        existing_clone_review = load_yaml_if_exists(clone_review_path, {}) or {}
        clone_decision_sync = sync_clone_review_decisions_to_library(library, existing_clone_review)
        effective_plan = build_effective_plan_from_review(review_store, candidates, output_path, clone_review_path)
        effective_plan["voice_library_path"] = str(library_path)
        effective_plan["role_profiles_path"] = str(role_profiles_path)
        effective_plan["casting_response_path"] = str(casting_response_path)
        effective_plan["clone_actions"] = build_clone_actions(effective_plan.get("roles") or [])
        clone_review_store = build_clone_review_store(effective_plan, existing_clone_review, library.get("clones") or {})
        if clone_decision_sync["changed"]:
            save_yaml(library_path, library)
        save_yaml(output_path, effective_plan)
        save_yaml(clone_review_path, clone_review_store)
        manifest_kwargs = {
            "casting_output_path": output_path,
            "casting_review_path": casting_review_path,
            "clone_review_path": clone_review_path,
            "role_profiles_path": role_profiles_path,
            "casting_selection_path": casting_response_path,
            "library_path": library_path,
        }
        if is_structured_input_path(input_path):
            manifest_kwargs["effective_story_input_path"] = input_path
        else:
            manifest_kwargs["story_input_path"] = input_path
        refresh_story_artifact_manifest(**manifest_kwargs)
        print(
            json.dumps(
                {
                    "mode": "refresh-only",
                    "input_path": str(input_path),
                    "output_path": str(output_path),
                    "casting_review_path": str(casting_review_path),
                    "clone_review_path": str(clone_review_path),
                    "role_count": len(effective_plan.get("roles") or []),
                    "pending_clone_count": len(clone_review_store.get("items") or {}),
                    "clone_review_sync": {
                        "applied_count": len(clone_decision_sync["applied"]),
                        "changed_count": len([item for item in clone_decision_sync["applied"] if item.get("changed")]),
                        "missing_library_assets": [item.get("asset_id") for item in clone_decision_sync["missing"]],
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    role_llm = dict(casting_config["role_llm"])
    selection_llm = dict(casting_config["selection_llm"])

    role_api_key_info = resolve_api_key([Path.cwd(), library_dir, Path(__file__).resolve().parent], role_llm["api_key_env"])
    if not role_api_key_info.get("value"):
        raise RuntimeError(f"缺少 {role_llm['api_key_env']}，无法调用角色画像提取 LLM")
    role_llm["api_key"] = role_api_key_info["value"]

    selection_api_key_info = resolve_api_key(
        [Path.cwd(), library_dir, Path(__file__).resolve().parent],
        selection_llm["api_key_env"],
    )
    if not selection_api_key_info.get("value"):
        raise RuntimeError(f"缺少 {selection_llm['api_key_env']}，无法调用音色选角 LLM")
    selection_llm["api_key"] = selection_api_key_info["value"]

    source = load_input_source(input_path)
    extracted = extract_role_profiles_from_source(source, role_llm)
    role_profiles = extracted["role_profiles"]
    selection_response = select_casting_with_llm(role_profiles, candidates, selection_llm)
    unresolved_roles = collect_unresolved_role_profiles(selection_response, role_profiles, candidates)
    final_selection_response = (
        merge_selection_responses(selection_response, select_casting_with_llm(unresolved_roles, candidates, selection_llm))
        if unresolved_roles
        else selection_response
    )

    if casting_config["output"]["save_intermediate_json"]:
        save_json(
            role_profiles_path,
            {
                "generated_at": now_iso(),
                "mode": extracted["mode"],
                "title": extracted.get("title") or "",
                "roles": role_profiles,
                "raw_response": (extracted.get("raw_response") or {}).get("raw") if extracted.get("raw_response") else None,
                "raw_text": (extracted.get("raw_response") or {}).get("content") if extracted.get("raw_response") else "",
                "raw_channel": (extracted.get("raw_response") or {}).get("channel") if extracted.get("raw_response") else "",
                "repaired": extracted.get("repaired") is True,
                "repaired_raw": (extracted.get("raw_response") or {}).get("repaired_raw") if extracted.get("raw_response") else None,
                "repaired_text": (extracted.get("raw_response") or {}).get("repaired_content") if extracted.get("raw_response") else "",
            },
        )
        save_json(
            casting_response_path,
            {
                "generated_at": now_iso(),
                "unresolved_roles": [{"role_id": item.get("role_id"), "role_name": item.get("role_name")} for item in unresolved_roles],
                "raw_response": final_selection_response.get("raw"),
                "raw_text": final_selection_response.get("content") or "",
                "raw_channel": final_selection_response.get("channel") or "",
                "repaired": final_selection_response.get("repaired") is True,
                "repaired_raw": final_selection_response.get("repaired_raw"),
                "repaired_text": final_selection_response.get("repaired_content") or "",
            },
        )

    normalized_selection = normalize_casting_selection(
        final_selection_response,
        role_profiles,
        candidates,
        casting_config["output"]["top_candidates_per_role"],
    )
    review_store = build_casting_review_store(
        {
            "inputPath": input_path,
            "candidatePoolPath": candidate_pool_path,
            "roleProfilesPath": role_profiles_path,
            "castingResponsePath": casting_response_path,
            "effectivePlanPath": output_path,
            "cloneReviewPath": clone_review_path,
            "llmMeta": {
                "provider": "openai_compatible_shared_prompt_layer",
                "role_extraction": {
                    "provider": role_llm["provider"],
                    "api_key_env": role_llm["api_key_env"],
                    "api_key_source": role_api_key_info.get("source"),
                    "base_url": role_llm["base_url"],
                    "model": role_llm["model"],
                },
                "selection": {
                    "provider": selection_llm["provider"],
                    "api_key_env": selection_llm["api_key_env"],
                    "api_key_source": selection_api_key_info.get("source"),
                    "base_url": selection_llm["base_url"],
                    "model": selection_llm["model"],
                },
                "response_mode": "text",
            },
            "normalizedSelection": normalized_selection,
            "existingStore": load_yaml_if_exists(casting_review_path, {}) or {},
        }
    )
    effective_plan = build_effective_plan_from_review(review_store, candidates, output_path, clone_review_path)
    effective_plan["voice_library_path"] = str(library_path)
    effective_plan["role_profiles_path"] = str(role_profiles_path)
    effective_plan["casting_response_path"] = str(casting_response_path)
    effective_plan["clone_actions"] = build_clone_actions(effective_plan.get("roles") or [])
    existing_clone_review = load_yaml_if_exists(clone_review_path, {}) or {}
    clone_decision_sync = sync_clone_review_decisions_to_library(library, existing_clone_review)
    clone_review_store = build_clone_review_store(effective_plan, existing_clone_review, library.get("clones") or {})

    if casting_config["output"]["save_intermediate_json"]:
        save_json(
            casting_response_path,
            {
                "generated_at": now_iso(),
                "unresolved_roles": [{"role_id": item.get("role_id"), "role_name": item.get("role_name")} for item in unresolved_roles],
                "raw_response": final_selection_response.get("raw"),
                "raw_text": final_selection_response.get("content") or "",
                "raw_channel": final_selection_response.get("channel") or "",
                "repaired": final_selection_response.get("repaired") is True,
                "repaired_raw": final_selection_response.get("repaired_raw"),
                "repaired_text": final_selection_response.get("repaired_content") or "",
                "normalized_selection": {**effective_plan, "summary": effective_plan.get("summary")},
            },
        )

    if clone_decision_sync["changed"]:
        save_yaml(library_path, library)
    save_yaml(casting_review_path, review_store)
    save_yaml(output_path, effective_plan)
    save_yaml(clone_review_path, clone_review_store)
    manifest_kwargs = {
        "casting_output_path": output_path,
        "casting_review_path": casting_review_path,
        "clone_review_path": clone_review_path,
        "role_profiles_path": role_profiles_path,
        "casting_selection_path": casting_response_path,
        "library_path": library_path,
    }
    if is_structured_input_path(input_path):
        manifest_kwargs["effective_story_input_path"] = input_path
    else:
        manifest_kwargs["story_input_path"] = input_path
    refresh_story_artifact_manifest(**manifest_kwargs)
    print(
        json.dumps(
            {
                "mode": "full",
                "input_path": str(input_path),
                "output_path": str(output_path),
                "library_path": str(library_path),
                "candidate_pool_path": str(candidate_pool_path),
                "casting_review_path": str(casting_review_path),
                "clone_review_path": str(clone_review_path),
                "role_profiles_path": str(role_profiles_path),
                "casting_response_path": str(casting_response_path),
                "role_count": len(effective_plan.get("roles") or []),
                "clone_actions_count": len(effective_plan.get("clone_actions") or []),
                "pending_clone_count": len(clone_review_store.get("items") or {}),
                "role_llm": {
                    "provider": role_llm["provider"],
                    "model": role_llm["model"],
                    "api_key_env": role_llm["api_key_env"],
                    "api_key_source": role_api_key_info.get("source"),
                    "base_url": role_llm["base_url"],
                },
                "selection_llm": {
                    "provider": selection_llm["provider"],
                    "model": selection_llm["model"],
                    "api_key_env": selection_llm["api_key_env"],
                    "api_key_source": selection_api_key_info.get("source"),
                    "base_url": selection_llm["base_url"],
                },
                "clone_review_sync": {
                    "applied_count": len(clone_decision_sync["applied"]),
                    "changed_count": len([item for item in clone_decision_sync["applied"] if item.get("changed")]),
                    "missing_library_assets": [item.get("asset_id") for item in clone_decision_sync["missing"]],
                },
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
