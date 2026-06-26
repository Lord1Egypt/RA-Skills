#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    load_json_if_exists,
    load_yaml_if_exists,
    resolve_artifact_dir,
    resolve_path,
    resolve_story_workspace_dir,
    save_json,
    trim_string,
)


LEVEL_RANK = {
    "essential": 1,
    "review": 2,
    "debug": 3,
}

STRUCTURED_STORY_EXTENSIONS = {".yaml", ".yml", ".json"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def strip_story_suffix(base_name: str) -> str:
    value = str(base_name or "")
    for suffix in (".tts-requests", ".casting-plan", ".structured-script"):
        if value.endswith(suffix):
            return value[: -len(suffix)]
    return value


def normalize_path(value: str | Path | None) -> Path | None:
    if not value:
        return None
    if isinstance(value, Path):
        return value.resolve()
    text = trim_string(value)
    if not text:
        return None
    return Path(text).resolve()


def resolve_story_base_name(*, story_input_path: Path | None, effective_story_input_path: Path | None, casting_output_path: Path | None, tts_requests_path: Path | None) -> str:
    for candidate in (tts_requests_path, casting_output_path, effective_story_input_path, story_input_path):
        if candidate is None:
            continue
        base_name = strip_story_suffix(candidate.stem)
        if base_name:
            return base_name
    return "audiobook"


def resolve_artifact_base_dir(*, story_input_path: Path | None, effective_story_input_path: Path | None, casting_output_path: Path | None, tts_requests_path: Path | None) -> Path:
    if tts_requests_path is not None:
        return tts_requests_path.parent.resolve()

    if effective_story_input_path is not None:
        return resolve_story_workspace_dir(effective_story_input_path).resolve()

    if casting_output_path is not None:
        return resolve_story_workspace_dir(casting_output_path).resolve()

    if story_input_path is not None:
        return resolve_story_workspace_dir(story_input_path).resolve()

    return resolve_story_workspace_dir(Path.cwd()).resolve()


def resolve_manifest_path(*, artifact_base_dir: Path, base_name: str) -> Path:
    return artifact_base_dir / f"{base_name}.artifacts.json"


def get_generation_artifact_path(structured_script_path: Path) -> Path:
    return structured_script_path.parent / f"{structured_script_path.stem}.generation.json"


def get_casting_base_name(casting_output_path: Path) -> str:
    base = casting_output_path.stem
    return base[: -len(".casting-plan")] if base.endswith(".casting-plan") else base


def get_casting_review_path(casting_output_path: Path) -> Path:
    return casting_output_path.parent / f"{get_casting_base_name(casting_output_path)}.casting-review.yaml"


def get_clone_review_path(casting_output_path: Path) -> Path:
    return casting_output_path.parent / f"{get_casting_base_name(casting_output_path)}.clone-review.yaml"


def get_role_profiles_path(casting_output_path: Path) -> Path:
    return (resolve_artifact_dir(casting_output_path) / f"{casting_output_path.stem}.role-profiles.json").resolve()


def get_casting_selection_path(casting_output_path: Path) -> Path:
    return (resolve_artifact_dir(casting_output_path) / f"{casting_output_path.stem}.casting-selection.json").resolve()


def get_tts_requests_base_name(tts_requests_path: Path) -> str:
    base = tts_requests_path.stem
    return base[: -len(".tts-requests")] if base.endswith(".tts-requests") else base


def get_script_runtime_path(tts_requests_path: Path) -> Path:
    return tts_requests_path.parent / f"{get_tts_requests_base_name(tts_requests_path)}.script-runtime.json"


def get_segments_dir(tts_requests_path: Path) -> Path:
    return tts_requests_path.parent / f"{get_tts_requests_base_name(tts_requests_path)}.segments"


def load_library_related_paths(library_path: Path | None) -> dict[str, Path]:
    if library_path is None:
        return {}

    library = load_yaml_if_exists(library_path, {}) or {}
    paths = library.get("paths") or {}
    library_dir = library_path.parent
    return {
        "voice_reviews": resolve_path(library_dir, paths.get("review_file", "voice-reviews.yaml")).resolve(),
        "effective_voice_library": resolve_path(
            library_dir,
            paths.get("effective_library_file", ".audiobook/effective-voice-library.yaml"),
        ).resolve(),
        "official_cache": resolve_path(
            library_dir,
            paths.get("official_cache_file", ".audiobook/official-voices-cache.json"),
        ).resolve(),
        "voice_candidate_pool": resolve_path(
            library_dir,
            paths.get("candidate_pool_file", ".audiobook/voice-candidate-pool.yaml"),
        ).resolve(),
    }


def add_item(items: list[dict[str, Any]], *, item_id: str, label: str, path: Path | None, stage: str, visibility: str, description: str, scope: str = "story", meta: dict[str, Any] | None = None) -> None:
    if path is None:
        return

    resolved = path.resolve()
    items.append(
        {
            "id": item_id,
            "scope": scope,
            "stage": stage,
            "visibility": visibility,
            "label": label,
            "path": str(resolved),
            "exists": resolved.exists(),
            "description": description,
            "meta": meta or {},
        }
    )


def sort_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            LEVEL_RANK.get(trim_string(item.get("visibility")) or "debug", 99),
            trim_string(item.get("scope")) or "story",
            trim_string(item.get("stage")) or "zzz",
            trim_string(item.get("label")) or "",
        ),
    )


def select_manifest_items(manifest: dict[str, Any], level: str = "essential") -> list[dict[str, Any]]:
    requested_rank = LEVEL_RANK.get(level, LEVEL_RANK["essential"])
    selected = []
    for item in manifest.get("items") or []:
        visibility = trim_string(item.get("visibility")) or "debug"
        if LEVEL_RANK.get(visibility, 99) <= requested_rank:
            selected.append(item)
    return selected


def format_manifest_pretty(manifest: dict[str, Any], level: str = "essential") -> str:
    items = select_manifest_items(manifest, level)
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(str(item.get("stage") or "other"), []).append(item)

    lines = [
        f"level: {level}",
        f"manifest: {manifest.get('manifest_path')}",
        f"artifact_base_dir: {manifest.get('artifact_base_dir')}",
        "",
    ]

    stage_order = ["source", "script", "voice_library", "casting", "synthesis", "export", "other"]
    ordered_stages = [stage for stage in stage_order if stage in groups] + [
        stage for stage in groups if stage not in stage_order
    ]
    for stage in ordered_stages:
        lines.append(f"[{stage}]")
        for item in groups[stage]:
            exists_text = "yes" if item.get("exists") else "no"
            lines.append(f"- {item.get('label')} ({item.get('visibility')}, exists={exists_text})")
            lines.append(f"  path: {item.get('path')}")
            lines.append(f"  desc: {item.get('description')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def manifest_item_path(manifest: dict[str, Any], item_id: str) -> str:
    for item in manifest.get("items") or []:
        if trim_string(item.get("id")) == item_id:
            return str(item.get("path") or "")
    return ""


def is_structured_story_input(path: Path | None) -> bool:
    return bool(path and path.suffix.lower() in STRUCTURED_STORY_EXTENSIONS)


def build_story_artifact_manifest(
    *,
    story_input_path: str | Path | None = None,
    effective_story_input_path: str | Path | None = None,
    structured_script_artifact_path: str | Path | None = None,
    casting_output_path: str | Path | None = None,
    casting_review_path: str | Path | None = None,
    clone_review_path: str | Path | None = None,
    role_profiles_path: str | Path | None = None,
    casting_selection_path: str | Path | None = None,
    tts_requests_path: str | Path | None = None,
    library_path: str | Path | None = None,
) -> dict[str, Any]:
    story_input = normalize_path(story_input_path)
    effective_story_input = normalize_path(effective_story_input_path)
    structured_script_artifact = normalize_path(structured_script_artifact_path)
    casting_output = normalize_path(casting_output_path)
    casting_review = normalize_path(casting_review_path)
    clone_review = normalize_path(clone_review_path)
    role_profiles = normalize_path(role_profiles_path)
    casting_selection = normalize_path(casting_selection_path)
    tts_requests = normalize_path(tts_requests_path)
    library = normalize_path(library_path)

    base_name = resolve_story_base_name(
        story_input_path=story_input,
        effective_story_input_path=effective_story_input,
        casting_output_path=casting_output,
        tts_requests_path=tts_requests,
    )
    artifact_base_dir = resolve_artifact_base_dir(
        story_input_path=story_input,
        effective_story_input_path=effective_story_input,
        casting_output_path=casting_output,
        tts_requests_path=tts_requests,
    )
    manifest_path = resolve_manifest_path(artifact_base_dir=artifact_base_dir, base_name=base_name)

    if effective_story_input is not None and structured_script_artifact is None:
        candidate = get_generation_artifact_path(effective_story_input)
        if candidate.exists() or ".structured-script" in effective_story_input.stem:
            structured_script_artifact = candidate

    if casting_output is not None:
        if casting_review is None:
            casting_review = get_casting_review_path(casting_output)
        if clone_review is None:
            clone_review = get_clone_review_path(casting_output)
        if role_profiles is None:
            role_profiles = get_role_profiles_path(casting_output)
        if casting_selection is None:
            casting_selection = get_casting_selection_path(casting_output)

    runtime_script_path: Path | None = None
    segment_dir: Path | None = None
    latest_export_path: Path | None = None
    final_output_path: Path | None = None
    suggested_final_output_path: Path | None = None
    if tts_requests is not None:
        runtime_script_path = get_script_runtime_path(tts_requests)
        segment_dir = get_segments_dir(tts_requests)
        request_artifact = load_json_if_exists(tts_requests, {}) or {}
        source = request_artifact.get("source") or {}
        latest_export = request_artifact.get("latest_export") or {}
        final_output = request_artifact.get("final_output") or {}
        suggested_final_output_path = normalize_path(source.get("output_path"))
        latest_export_path = normalize_path(latest_export.get("output_path"))
        final_output_path = normalize_path(final_output.get("output_path"))

    items: list[dict[str, Any]] = []

    if story_input is not None and story_input != effective_story_input:
        add_item(
            items,
            item_id="source_text",
            label="原始文本",
            path=story_input,
            stage="source",
            visibility="debug",
            description="原始 txt 输入；结构化脚本通常由它生成。",
        )

    if effective_story_input is not None:
        label = "结构化剧本"
        description = "角色、段落、speaker 的统一入口；后续 casting 与 TTS 都从这里继续。"
        if story_input is not None and story_input == effective_story_input:
            label = "结构化剧本输入"
            description = "用户直接提供的结构化 yaml/json。"
        add_item(
            items,
            item_id="structured_script",
            label=label,
            path=effective_story_input,
            stage="script",
            visibility="essential",
            description=description,
        )

    add_item(
        items,
        item_id="script_generation_trace",
        label="结构化剧本生成轨迹",
        path=structured_script_artifact,
        stage="script",
        visibility="review",
        description="txt -> structured-script 的 overview/chunks/finalize 调用归档。",
    )

    add_item(
        items,
        item_id="casting_review",
        label="角色选角审核",
        path=casting_review,
        stage="casting",
        visibility="essential",
        description="人工修正角色最终音色入口。",
    )
    add_item(
        items,
        item_id="casting_plan",
        label="生效选角计划",
        path=casting_output,
        stage="casting",
        visibility="essential",
        description="真正供下游使用的角色 -> 音色映射结果。",
    )
    add_item(
        items,
        item_id="clone_review",
        label="待付费 clone 审核",
        path=clone_review,
        stage="casting",
        visibility="review",
        description="人工决定哪些 clone 值得进入真正付费复刻。",
    )
    add_item(
        items,
        item_id="role_profiles",
        label="角色画像",
        path=role_profiles,
        stage="casting",
        visibility="review",
        description="LLM 为每个角色提炼出的音色需求与证据。",
    )
    add_item(
        items,
        item_id="casting_selection_trace",
        label="选角模型原始结果",
        path=casting_selection,
        stage="casting",
        visibility="review",
        description="LLM 选角返回与归一化结果归档，适合排查。",
    )

    add_item(
        items,
        item_id="script_runtime",
        label="标准化剧本 runtime",
        path=runtime_script_path,
        stage="synthesis",
        visibility="review",
        description="进入 build_tts_requests 前整理好的统一 runtime 结构。",
    )
    add_item(
        items,
        item_id="tts_requests",
        label="TTS 请求清单",
        path=tts_requests,
        stage="synthesis",
        visibility="essential",
        description="真正可编辑、可 replay、可部分重跑的请求清单。",
    )
    add_item(
        items,
        item_id="segment_audio_dir",
        label="分段音频目录",
        path=segment_dir,
        stage="synthesis",
        visibility="review",
        description="每段实际合成出来的音频产物；局部重放主要看这里。",
    )
    add_item(
        items,
        item_id="suggested_final_output",
        label="建议整本导出路径",
        path=suggested_final_output_path,
        stage="export",
        visibility="debug",
        description="build_tts_requests 预先写入的默认整本导出位置。",
    )
    add_item(
        items,
        item_id="latest_export",
        label="最近一次导出",
        path=latest_export_path,
        stage="export",
        visibility="review",
        description="最近一次 full export 或 preview 导出结果。",
    )
    add_item(
        items,
        item_id="final_output",
        label="最终整本音频",
        path=final_output_path,
        stage="export",
        visibility="essential",
        description="完整 audiobook 成品；只有 full export 成功后才存在。",
    )

    if library is not None:
        add_item(
            items,
            item_id="voice_library",
            label="音色库源文件",
            path=library,
            stage="voice_library",
            visibility="debug",
            description="官方音色、用户 clone 元信息、selected_for_clone 都在这里。",
            scope="library",
        )
        related_paths = load_library_related_paths(library)
        add_item(
            items,
            item_id="voice_reviews",
            label="音色审核文件",
            path=related_paths.get("voice_reviews"),
            stage="voice_library",
            visibility="review",
            description="用户手改 clone 音色真实描述的人工入口。",
            scope="library",
        )
        add_item(
            items,
            item_id="effective_voice_library",
            label="生效音色库",
            path=related_paths.get("effective_voice_library"),
            stage="voice_library",
            visibility="review",
            description="后续选角真正读取的统一音色库快照。",
            scope="library",
        )
        add_item(
            items,
            item_id="official_voice_cache",
            label="官方音色缓存",
            path=related_paths.get("official_cache"),
            stage="voice_library",
            visibility="review",
            description="最近一次 Step 官方音色接口同步结果，含官方描述与推荐场景。",
            scope="library",
        )
        add_item(
            items,
            item_id="voice_candidate_pool",
            label="统一音色候选池",
            path=related_paths.get("voice_candidate_pool"),
            stage="voice_library",
            visibility="review",
            description="官方音色 + clone 生效结果合并后的统一选角入口。",
            scope="library",
        )

    manifest = {
        "version": "1",
        "generated_at": now_iso(),
        "base_name": base_name,
        "artifact_base_dir": str(artifact_base_dir),
        "manifest_path": str(manifest_path),
        "story_input_path": str(story_input) if story_input is not None else "",
        "effective_story_input_path": str(effective_story_input) if effective_story_input is not None else "",
        "casting_output_path": str(casting_output) if casting_output is not None else "",
        "tts_requests_path": str(tts_requests) if tts_requests is not None else "",
        "library_path": str(library) if library is not None else "",
        "items": sort_items(items),
    }
    manifest["counts"] = {
        "essential": len(select_manifest_items(manifest, "essential")),
        "review": len(select_manifest_items(manifest, "review")),
        "debug": len(select_manifest_items(manifest, "debug")),
    }
    return manifest


def save_story_artifact_manifest(manifest: dict[str, Any]) -> Path:
    manifest_path = Path(str(manifest.get("manifest_path") or "")).resolve()
    save_json(manifest_path, manifest)
    return manifest_path


def refresh_story_artifact_manifest(
    *,
    story_input_path: str | Path | None = None,
    effective_story_input_path: str | Path | None = None,
    structured_script_artifact_path: str | Path | None = None,
    casting_output_path: str | Path | None = None,
    casting_review_path: str | Path | None = None,
    clone_review_path: str | Path | None = None,
    role_profiles_path: str | Path | None = None,
    casting_selection_path: str | Path | None = None,
    tts_requests_path: str | Path | None = None,
    library_path: str | Path | None = None,
) -> dict[str, Any]:
    explicit_story_input = normalize_path(story_input_path)
    explicit_effective_story_input = normalize_path(effective_story_input_path)
    explicit_structured_script_artifact = normalize_path(structured_script_artifact_path)
    explicit_casting_output = normalize_path(casting_output_path)
    explicit_casting_review = normalize_path(casting_review_path)
    explicit_clone_review = normalize_path(clone_review_path)
    explicit_role_profiles = normalize_path(role_profiles_path)
    explicit_casting_selection = normalize_path(casting_selection_path)
    explicit_tts_requests = normalize_path(tts_requests_path)
    explicit_library = normalize_path(library_path)

    base_name = resolve_story_base_name(
        story_input_path=explicit_story_input,
        effective_story_input_path=explicit_effective_story_input,
        casting_output_path=explicit_casting_output,
        tts_requests_path=explicit_tts_requests,
    )
    artifact_base_dir = resolve_artifact_base_dir(
        story_input_path=explicit_story_input,
        effective_story_input_path=explicit_effective_story_input,
        casting_output_path=explicit_casting_output,
        tts_requests_path=explicit_tts_requests,
    )
    manifest_path = resolve_manifest_path(artifact_base_dir=artifact_base_dir, base_name=base_name)
    existing_manifest = load_json_if_exists(manifest_path, {}) if manifest_path.exists() else {}

    manifest = build_story_artifact_manifest(
        story_input_path=explicit_story_input or existing_manifest.get("story_input_path") or "",
        effective_story_input_path=explicit_effective_story_input or existing_manifest.get("effective_story_input_path") or "",
        structured_script_artifact_path=explicit_structured_script_artifact or manifest_item_path(existing_manifest, "script_generation_trace"),
        casting_output_path=explicit_casting_output or existing_manifest.get("casting_output_path") or "",
        casting_review_path=explicit_casting_review or manifest_item_path(existing_manifest, "casting_review"),
        clone_review_path=explicit_clone_review or manifest_item_path(existing_manifest, "clone_review"),
        role_profiles_path=explicit_role_profiles or manifest_item_path(existing_manifest, "role_profiles"),
        casting_selection_path=explicit_casting_selection or manifest_item_path(existing_manifest, "casting_selection_trace"),
        tts_requests_path=explicit_tts_requests or existing_manifest.get("tts_requests_path") or "",
        library_path=explicit_library or existing_manifest.get("library_path") or "",
    )

    if explicit_story_input and is_structured_story_input(explicit_story_input) and not explicit_effective_story_input:
        manifest["effective_story_input_path"] = str(explicit_story_input)

    save_story_artifact_manifest(manifest)
    return manifest
