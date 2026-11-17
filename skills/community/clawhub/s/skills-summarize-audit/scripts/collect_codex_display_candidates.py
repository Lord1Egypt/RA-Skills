#!/usr/bin/env python3
"""Collect read-only Simplified Chinese candidates for Codex skill UI text."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tomllib
from pathlib import Path

try:
    import yaml
except ImportError:  # The parser still supports the small UI metadata subset below.
    yaml = None

DISPLAY_MAX = 24
SHORT_MAX = 40
LONG_MAX = 80
GLOSSARY_PATH = Path(__file__).resolve().parent.parent / "references" / "codex-ui-zh-glossary.json"
INSTALLED_SOURCE_TYPES = {"codex_global_skill", "codex_system_skill", "codex_plugin_cache", "codex_runtime_plugin", "codex_plugin_manifest"}
CONFLICT_SOURCE_TYPES = INSTALLED_SOURCE_TYPES | {"codex_plugin_staging"}


def plugin_installations(root: Path) -> dict[str, dict]:
    """Read plugin installation evidence without invoking or mutating Codex."""
    installations: dict[str, dict] = {}
    config_path = root / "config.toml"
    if config_path.exists():
        try:
            data = tomllib.loads(read_text(config_path))
            plugins = data.get("plugins", {})
            if isinstance(plugins, dict):
                for plugin_ref, settings in plugins.items():
                    enabled = settings.get("enabled", True) if isinstance(settings, dict) else True
                    installations[str(plugin_ref)] = {
                        "status": "installed_enabled" if enabled else "installed_disabled",
                        "evidence": [str(config_path.resolve())],
                    }
        except (OSError, tomllib.TOMLDecodeError):
            pass

    cache_root = root / "plugins" / "cache"
    for marker in walk_files(cache_root, ".codex-remote-plugin-install.json"):
        try:
            relative = marker.relative_to(cache_root)
        except ValueError:
            continue
        if len(relative.parts) < 3:
            continue
        marketplace, plugin_id = relative.parts[0], relative.parts[1]
        plugin_ref = f"{plugin_id}@{marketplace}"
        current = installations.setdefault(plugin_ref, {"status": "installed_remote", "evidence": []})
        current["evidence"] = sorted(set([*current.get("evidence", []), str(marker.resolve())]))
    return installations


def plugin_identity(path: Path, cache_root: Path) -> tuple[str | None, str | None]:
    try:
        relative = path.resolve().relative_to(cache_root.resolve())
    except (OSError, ValueError):
        return None, None
    if len(relative.parts) < 3:
        return None, None
    marketplace, plugin_id = relative.parts[0], relative.parts[1]
    return plugin_id, f"{plugin_id}@{marketplace}"


def annotate_plugin_installation(item: dict, path: Path, root: Path, installations: dict[str, dict]) -> None:
    plugin_id, plugin_ref = plugin_identity(path, root / "plugins" / "cache")
    if not plugin_ref:
        return
    state = installations.get(plugin_ref, {"status": "cached_only", "evidence": []})
    item["plugin"] = plugin_id
    item["plugin_ref"] = plugin_ref
    item["installation_status"] = state["status"]
    item["installation_evidence"] = list(state.get("evidence", []))


def is_installed_item(item: dict) -> bool:
    source_type = item.get("source_type")
    if source_type not in INSTALLED_SOURCE_TYPES:
        return False
    if source_type in {"codex_plugin_cache", "codex_plugin_manifest"}:
        return item.get("installation_status") in {"installed_enabled", "installed_disabled", "installed_remote"}
    return True


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def glossary() -> dict:
    data = json.loads(read_text(GLOSSARY_PATH))
    if not isinstance(data.get("phrases"), dict) or not isinstance(data.get("words"), dict) or not isinstance(data.get("skill_overrides"), dict):
        raise ValueError("术语库缺少 phrases、words 或 skill_overrides")
    return data


GLOSSARY = glossary()


def yaml_subset(path: Path) -> dict:
    """Load UI metadata without requiring PyYAML at runtime."""
    text = read_text(path)
    if yaml:
        try:
            value = yaml.safe_load(text)
            return value if isinstance(value, dict) else {}
        except yaml.YAMLError:
            pass
    result: dict[str, object] = {}
    interface: dict[str, str] = {}
    for key in ("display_name", "short_description", "long_description"):
        match = re.search(rf"^\s*{key}:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
        if match:
            interface[key] = match.group(1).strip()
    if interface:
        result["interface"] = interface
    return result


def frontmatter(path: Path) -> dict:
    text = read_text(path)
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    if yaml:
        try:
            value = yaml.safe_load(match.group(1))
            return value if isinstance(value, dict) else {}
        except yaml.YAMLError:
            pass
    value = {}
    for key in ("name", "description"):
        item = re.search(rf"^{key}:\s*[\"']?(.+?)[\"']?\s*$", match.group(1), re.M)
        if item:
            value[key] = item.group(1).strip()
    return value


def compact(value: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", value).strip(" .")
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def substantial_chinese(value: str) -> bool:
    """Accept Chinese prose while allowing protected technical terms."""
    han_count = len(re.findall(r"[\u4e00-\u9fff]", value))
    latin_words = re.findall(r"[A-Za-z]{3,}", value)
    protected = set(GLOSSARY.get("protected_terms", []))
    unprotected = [word for word in latin_words if word not in protected and word.lower() not in {p.lower() for p in protected}]
    return han_count >= 3 and len(unprotected) <= 2


def chinese_candidate(value: str, limit: int, fallback: str) -> tuple[str, str]:
    """Create a conservative candidate; unrecognized prose is flagged for agent refinement."""
    value = re.sub(r"\bUse when\b.*", "", value, flags=re.I).strip()
    if substantial_chinese(value):
        return compact(value, limit), "source_chinese"
    normalized = re.sub(r"[.?!]+$", "", value).lower().strip()
    phrase = GLOSSARY["phrases"].get(normalized)
    if phrase:
        return compact(str(phrase), limit), "glossary_exact"
    words = re.findall(r"[A-Za-z0-9+.#]+", value)
    word_map = GLOSSARY["words"]
    translated = [word_map[word.lower()] for word in words if word.lower() in word_map]
    result = "".join(translated)
    if not re.search(r"[\u4e00-\u9fff]", result):
        result = "通用技能"
    return compact(result, limit), "glossary_partial_needs_refinement"


def translated_fields(command: str, sidebar: str, long: str, fallback: str, skill_id: str) -> dict:
    override = GLOSSARY["skill_overrides"].get(skill_id, {})
    if override:
        display_name = compact(command, DISPLAY_MAX)
        short_description = compact(str(override["short_description"]), SHORT_MAX)
        display_method = "preserve_original"; short_method = "skill_override"
    else:
        display_name, display_method = compact(command, DISPLAY_MAX), "preserve_original"
        short_description, short_method = chinese_candidate(sidebar, SHORT_MAX, fallback)
    long_description, long_method = chinese_candidate(long, LONG_MAX, fallback)
    core_methods = {display_method, short_method}
    quality = "ready" if core_methods <= {"source_chinese", "glossary_exact", "skill_override", "preserve_original"} else "needs_agent_refinement"
    return {
        "translation_quality": quality,
        "translation_methods": sorted({display_method, short_method, long_method}),
        "long_description_quality": "ready" if long_method in {"source_chinese", "glossary_exact"} else "needs_agent_refinement",
        "command_palette": {"original": command, "display_name": display_name},
        "sidebar": {"original": sidebar, "short_description": short_description, "long_original": long, "long_description": long_description},
    }


def source_hashes(paths: list[Path]) -> dict[str, str]:
    return {str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def source_fingerprint(item: dict) -> str:
    """Hash metadata contents, independent of cache/staging directory prefixes."""
    parts: list[str] = []
    for raw_path in sorted(item.get("source_paths", [])):
        path = Path(raw_path)
        if not path.is_file():
            continue
        parts.append(f"{path.name}:{hashlib.sha256(path.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def is_link_or_junction(path: Path) -> bool:
    """Treat symlinks, Junctions and unreadable entries as traversal boundaries."""
    try:
        if path.is_symlink() or os.path.islink(path):
            return True
        isjunction = getattr(os.path, "isjunction", None)
        return bool(isjunction and isjunction(path))
    except OSError:
        return True


def walk_files(root: Path, filename: str | None = None) -> list[Path]:
    """Walk without following reparse points; broken Junctions must not abort a scan."""
    if not root.exists() or is_link_or_junction(root):
        return []
    found: list[Path] = []
    def onerror(_: OSError) -> None:
        return None
    for current, directories, files in os.walk(root, topdown=True, followlinks=False, onerror=onerror):
        base = Path(current)
        directories[:] = [name for name in directories
                       if not is_link_or_junction(base / name)
                       and name.lower() not in ("archived", ".archived")]  # [local-patch] 排除备份目录（大小写不敏感）
        for name in files:
            if filename is None or name == filename:
                found.append(base / name)
    return sorted(found)


def skill_files(root: Path) -> list[Path]:
    return [p for p in walk_files(root, "SKILL.md") if ".archived" not in p.parts and ".archived" not in str(p).lower()]


def candidate_from_skill(path: Path, source_type: str, editable: bool, editable_reason: str | None = None) -> tuple[dict, list[Path]]:
    meta = frontmatter(path)
    skill_id = str(meta.get("name") or path.parent.name)
    description = str(meta.get("description") or "")
    ui_path = path.parent / "agents" / "openai.yaml"
    ui = yaml_subset(ui_path).get("interface", {}) if ui_path.exists() else {}
    ui = ui if isinstance(ui, dict) else {}
    command_original = str(ui.get("display_name") or skill_id)
    sidebar_original = str(ui.get("short_description") or description or command_original)
    long_original = str(ui.get("long_description") or description or sidebar_original)
    paths = [path] + ([ui_path] if ui_path.exists() else [])
    translated = translated_fields(command_original, sidebar_original, long_original, description or skill_id, skill_id)
    return ({
        "id": skill_id, "source_paths": [str(p.resolve()) for p in paths],
        "source_type": source_type, "inventory_scope": "installed", "editable": editable,
        "editable_reason": editable_reason or ("user_skill" if editable else "read_only_source"), "only_list": True,
        "fact_status": "observed", **translated,
    }, paths)


def catalog_candidates(catalog: Path) -> tuple[list[dict], list[Path]]:
    try:
        data = json.loads(read_text(catalog))
    except (OSError, json.JSONDecodeError) as exc:
        return ([{"id": catalog.name, "source_paths": [str(catalog.resolve())], "source_type": "remote_plugin_catalog",
                  "editable": False, "only_list": True, "fact_status": "unavailable", "error": str(exc)}], [catalog])
    items = []
    for plugin in data.get("plugins", []):
        release = plugin.get("release", {}) if isinstance(plugin, dict) else {}
        for skill in release.get("skills", []) or []:
            if not isinstance(skill, dict):
                continue
            interface = skill.get("interface", {}) if isinstance(skill.get("interface"), dict) else {}
            skill_id = str(skill.get("name") or "unknown-skill")
            command = str(interface.get("display_name") or skill_id)
            sidebar = str(interface.get("short_description") or skill.get("description") or command)
            long = str(skill.get("description") or sidebar)
            translated = translated_fields(command, sidebar, long, skill_id, skill_id)
            items.append({
                "id": skill_id, "plugin": plugin.get("name"), "source_paths": [str(catalog.resolve())],
                "source_type": "remote_plugin_catalog", "inventory_scope": "catalog_only", "editable": False, "only_list": True,
                "fact_status": "observed", **translated,
            })
    return items, [catalog]


def manifest_candidates(root: Path, codex_root: Path, installations: dict[str, dict]) -> tuple[list[dict], list[Path]]:
    """Collect installed Codex plugin-card UI metadata from plugin.json interfaces."""
    items: list[dict] = []
    manifests = [p for p in walk_files(root, "plugin.json") if p.parent.name == ".codex-plugin"]
    for manifest in manifests:
        try:
            data = json.loads(read_text(manifest))
        except (OSError, json.JSONDecodeError) as exc:
            item = {
                "id": manifest.parent.parent.name, "source_paths": [str(manifest.resolve())],
                "source_type": "codex_plugin_manifest", "inventory_scope": "installed", "editable": False,
                "only_list": True, "fact_status": "unavailable", "error": str(exc),
            }
            annotate_plugin_installation(item, manifest, codex_root, installations)
            items.append(item)
            continue
        interface = data.get("interface", {}) if isinstance(data.get("interface"), dict) else {}
        plugin_id = str(data.get("name") or manifest.parent.parent.name)
        command = str(interface.get("displayName") or plugin_id)
        sidebar = str(interface.get("shortDescription") or data.get("description") or command)
        long = str(interface.get("longDescription") or data.get("description") or sidebar)
        translated = translated_fields(command, sidebar, long, plugin_id, f"plugin:{plugin_id}")
        item = {
            "id": f"plugin:{plugin_id}", "plugin": plugin_id, "source_paths": [str(manifest.resolve())],
            "source_type": "codex_plugin_manifest", "inventory_scope": "installed", "editable": False,
            "editable_reason": "plugin_manifest_read_only",
            "only_list": True, "fact_status": "observed", **translated,
        }
        annotate_plugin_installation(item, manifest, codex_root, installations)
        items.append(item)
    return items, manifests


def watched_source_files(root: Path, catalog_dir: Path, runtime_dir: Path, staging_dir: Path | None = None, user_skill_dir: Path | None = None) -> list[Path]:
    """Discover every file the collector may read before parsing any metadata."""
    files: list[Path] = []
    locations = [root / "skills", root / "plugins" / "cache", runtime_dir]
    if user_skill_dir is not None:
        locations.append(user_skill_dir)
    if staging_dir is not None:
        locations.append(staging_dir)
    for location in locations:
        for skill in skill_files(location):
            files.append(skill)
            ui_path = skill.parent / "agents" / "openai.yaml"
            if ui_path.exists():
                files.append(ui_path)
            manifest = next(
                (parent / ".codex-plugin" / "plugin.json" for parent in [skill.parent, *skill.parents]
                 if (parent / ".codex-plugin" / "plugin.json").exists()),
                None,
            )
            if manifest:
                files.append(manifest)
    files.extend(p for p in walk_files(catalog_dir, None) if p.suffix.lower() == ".json")
    files.extend([p for p in walk_files(root / "plugins" / "cache", "plugin.json") if p.parent.name == ".codex-plugin"])
    return sorted(set(files))


def enrich_source_conflicts(candidates: list[dict]) -> None:
    """Keep every source candidate visible and provide a deterministic handling plan."""
    by_id: dict[str, list[dict]] = {}
    for item in candidates:
        by_id.setdefault(item["id"], []).append(item)
    for item in candidates:
        peers = by_id[item["id"]]
        actionable = [peer for peer in peers if peer.get("source_type") in CONFLICT_SOURCE_TYPES
                      and peer.get("installation_status") != "cached_only"
                      and not any(part.startswith("plugin-install-") for raw in peer.get("source_paths", []) for part in Path(raw).parts)]
        catalog_peers = [peer for peer in peers if peer.get("source_type") == "remote_plugin_catalog"]
        item["source_candidates"] = [
            {"source_type": peer.get("source_type"), "source_paths": peer.get("source_paths", []),
             "editable": peer.get("editable", False), "fingerprint": source_fingerprint(peer)}
            for peer in peers
        ]
        fingerprints = {source_fingerprint(peer) for peer in actionable}
        has_duplicate = len(actionable) > 1
        divergent = has_duplicate and len(fingerprints) > 1
        display_values = {
            (
                str(peer.get("sidebar", {}).get("original", "")).strip(),
                str(peer.get("command_palette", {}).get("display_name", "")).strip(),
            )
            for peer in actionable
        }
        display_equivalent = has_duplicate and len(display_values) == 1
        item["catalog_candidates"] = [{"source_type": peer.get("source_type"), "source_paths": peer.get("source_paths", [])} for peer in catalog_peers]
        item["source_conflict"] = divergent
        if divergent and display_equivalent:
            item["source_conflict"] = False
            item["source_resolution_status"] = "display_equivalent_sources"
            item["source_resolution_plan"] = "行为文件存在版本差异，但命令栏展示字段一致；按活动 cache 展示并保留 staging 更新风险。"
            item["source_conflict_reason"] = "行为文件不同但展示字段一致"
        elif divergent:
            item["source_resolution_status"] = "requires_ui_confirmation"
            item["source_resolution_plan"] = "暂停写入；以 UI 证据确认 cache 或 staging 后只修改确认来源。"
            item["source_conflict_reason"] = "同一 ID 的安装来源内容不同"
        elif has_duplicate:
            item["source_resolution_status"] = "equivalent_sources"
            source_types = {peer.get("source_type") for peer in actionable}
            if {"codex_plugin_cache", "codex_plugin_staging"} <= source_types:
                item["source_resolution_plan"] = "内容一致；以 codex_plugin_cache 作为当前来源，staging 仅作待刷新来源。"
            else:
                item["source_resolution_plan"] = "内容一致；按已安装来源优先级选择当前来源，其余记录为等价副本，不阻断使用。"
            item["source_conflict_reason"] = None
        else:
            item["source_resolution_status"] = "single_source"
            item["source_resolution_plan"] = "使用唯一安装来源；市场目录记录不参与写入。"
            item["source_conflict_reason"] = None


def collect(root: Path, catalog_dir: Path, runtime_dir: Path, staging_dir: Path | None = None, user_skill_dir: Path | None = None) -> tuple[list[dict], list[Path]]:
    candidates: list[dict] = []
    watched: list[Path] = []
    installations = plugin_installations(root)
    groups = [
        (root / "skills", "codex_global_skill", True, "user_skill"),
        (root / "plugins" / "cache", "codex_plugin_cache", False, "plugin_cache_read_only"),
        (runtime_dir, "codex_runtime_plugin", False, "runtime_read_only"),
    ]
    if staging_dir is not None:
        groups.append((staging_dir, "codex_plugin_staging", False, "staging_read_only"))
    if user_skill_dir is not None:
        groups.append((user_skill_dir, "codex_global_skill", True, "user_skill"))
    seen: set[Path] = set()
    for location, source_type, editable, editable_reason in groups:
        for path in skill_files(location):
            if path in seen:
                continue
            seen.add(path)
            item_editable = editable and ".system" not in path.parts
            item_reason = editable_reason if item_editable else ("system_skill_read_only" if source_type == "codex_global_skill" and ".system" in path.parts else editable_reason)
            item, paths = candidate_from_skill(path, source_type, item_editable, item_reason)
            if source_type == "codex_global_skill" and not item_editable:
                item["source_type"] = "codex_system_skill"
            if source_type == "codex_plugin_cache":
                annotate_plugin_installation(item, path, root, installations)
            candidates.append(item)
            watched.extend(paths)
            manifest = next((parent / ".codex-plugin" / "plugin.json" for parent in [path.parent, *path.parents] if (parent / ".codex-plugin" / "plugin.json").exists()), None)
            if manifest:
                watched.append(manifest)
                item["plugin_manifest"] = str(manifest.resolve())
    if catalog_dir.exists():
        for catalog in sorted(catalog_dir.glob("*.json")):
            items, paths = catalog_candidates(catalog)
            candidates.extend(items)
            watched.extend(paths)
    manifest_items, manifests = manifest_candidates(root / "plugins" / "cache", root, installations)
    candidates.extend(manifest_items)
    watched.extend(manifests)
    enrich_source_conflicts(candidates)
    return candidates, sorted(set(watched))


def resolve_visible_ids(items: list[dict], visible_ids: list[str]) -> list[dict]:
    """Resolve bare IDs and `$namespace:id` aliases, rejecting ambiguous aliases."""
    installed = logical_items(items, "installed")
    exact = {item["id"]: item for item in installed}
    aliases: dict[str, list[dict]] = {}
    for item in installed:
        aliases.setdefault(item["id"], []).append(item)
        if ":" in item["id"]:
            aliases.setdefault(item["id"].split(":", 1)[1], []).append(item)
    selected: list[dict] = []
    for raw_value in visible_ids:
        raw = raw_value.strip()
        if raw.startswith("$"):
            raw = raw[1:]
        suffix = raw.split(":", 1)[1] if ":" in raw else raw
        # A namespace-qualified UI command normally points at the bare skill ID;
        # prefer that exact suffix before falling back to plugin:* aliases.
        matches = [exact[raw]] if raw in exact else ([exact[suffix]] if suffix in exact else aliases.get(suffix, []))
        unique = {id(item): item for item in matches}
        if not unique:
            raise ValueError(f"未在本地来源中找到可见技能 ID: {raw_value}")
        if len(unique) > 1:
            raise ValueError(f"可见技能 ID 映射不唯一: {raw_value} -> {', '.join(item['id'] for item in unique.values())}")
        item = next(iter(unique.values()))
        item["input_id"] = raw_value
        item["normalized_id"] = item["id"]
        selected.append(item)
    return selected


def logical_items(items: list[dict], scope: str, visible_ids: list[str] | None = None) -> list[dict]:
    """Filter the requested inventory scope and de-duplicate installed UI entries."""
    if scope == "visible":
        requested = list(dict.fromkeys(item.strip() for item in visible_ids or [] if item.strip()))
        if not requested:
            raise ValueError("visible 范围要求至少一个 --visible-id；请根据当前侧栏或命令栏截图提供技能 ID")
        selected = resolve_visible_ids(items, requested)
        for item in selected:
            item["inventory_scope"] = "visible"
            item["selection_reason"] = "user_provided_visible_ui_evidence"
        return selected
    if scope == "installed":
        selected = [item for item in items if is_installed_item(item)]
    elif scope == "catalog":
        selected = [item for item in items if item["source_type"] == "remote_plugin_catalog"]
    else:
        return items
    unique: dict[str, dict] = {}
    for item in selected:
        # Prefer a normal cache directory, then the highest discovered version, then newest metadata.
        existing = unique.get(item["id"])
        if existing is None or candidate_rank(item) > candidate_rank(existing):
            unique[item["id"]] = item
    for item in unique.values():
        item["selection_reason"] = "highest_non_temporary_cache_version"
    return list(unique.values())


def candidate_rank(item: dict) -> tuple:
    paths = [Path(value) for value in item.get("source_paths", [])]
    temporary = any(part.startswith("plugin-install-") for path in paths for part in path.parts)
    versions: list[tuple[int, ...]] = []
    newest_mtime = 0.0
    for path in paths:
        for part in path.parts:
            match = re.fullmatch(r"(\d+(?:\.\d+)+)(?:-[A-Za-z0-9]+)?", part)
            if match:
                versions.append(tuple(int(number) for number in match.group(1).split(".")))
        try:
            newest_mtime = max(newest_mtime, path.stat().st_mtime)
        except OSError:
            pass
    return (not temporary, max(versions, default=()), newest_mtime)


def inventory_summary(items: list[dict]) -> dict:
    installed = [item for item in items if is_installed_item(item)]
    cached_only = [item for item in items if item.get("source_type") in {"codex_plugin_cache", "codex_plugin_manifest"} and not is_installed_item(item)]
    catalog = [item for item in items if item["source_type"] == "remote_plugin_catalog"]
    installed_unique = logical_items(items, "installed")
    installed_ids = {item["id"] for item in installed_unique}
    for item in catalog:
        item["matches_installed_id"] = item["id"] in installed_ids
    return {
        "installed_source_records": len(installed),
        "installed_unique_items": len(installed_unique),
        "installed_ready": sum(item["translation_quality"] == "ready" for item in installed_unique),
        "installed_needs_agent_refinement": sum(item["translation_quality"] == "needs_agent_refinement" for item in installed_unique),
        "cached_only_source_records": len(cached_only),
        "catalog_only_source_records": len(catalog),
        "catalog_matches_installed_id": sum(item["matches_installed_id"] for item in catalog),
        "note": "remote_plugin_catalog 是可发现市场项；不计入已安装健康度或 P1 翻译积压。",
    }


def markdown(items: list[dict], scope: str) -> str:
    lines = [f"## Codex 命令栏与侧边栏中文翻译清单（{scope}，{len(items)} 项）", "", "仅清单，不写入 Codex UI、插件缓存或技能触发逻辑。", "",
             "| 标识 | 命令栏原文 | 中文候选 | 侧边栏原文 | 中文候选 | 来源 | 来源处理 | 状态 |", "|---|---|---|---|---|---|---|---|"]
    for item in items:
        if item.get("fact_status") != "observed":
            continue
        lines.append("| {id} | {co} | {cc} | {so} | {sc} | {source} | {resolution} | observed / {quality} / 只读 |".format(
            id=item["id"], co=item["command_palette"]["original"], cc=item["command_palette"]["display_name"],
            so=item["sidebar"]["original"], sc=item["sidebar"]["short_description"], source=item["source_type"],
            resolution=item.get("source_resolution_status", "unavailable"), quality=item["translation_quality"]))
    return "\n".join(lines)


def untranslated_visible_items(items: list[dict]) -> list[str]:
    """Return visible IDs whose generated candidate has no Chinese text."""
    return [
        item["id"] for item in items
        if not re.search(r"[\u4e00-\u9fff]", item["sidebar"]["short_description"])
    ]


def unresolved_visible_items(items: list[dict]) -> list[str]:
    """Return candidates requiring agent refinement or source confirmation."""
    return [item["id"] for item in items if item.get("translation_quality") != "ready" or item.get("source_conflict")]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Collect read-only Codex Chinese UI candidates.")
    parser.add_argument("--root", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--catalog-dir", type=Path)
    parser.add_argument("--runtime-dir", type=Path, default=Path.home() / ".cache" / "codex-runtimes")
    parser.add_argument("--user-skill-dir", type=Path, default=Path.home() / ".agents" / "skills", help="用户可编辑 skill 根目录；与 CODEX_HOME 下系统/缓存来源分开记录。")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--check-unchanged", action="store_true")
    parser.add_argument("--scope", choices=("visible", "installed", "catalog", "all"), default="visible")
    parser.add_argument("--visible-id", action="append", default=[], help="A skill ID currently visible in the Codex sidebar or command palette; repeat for each visible skill.")
    parser.add_argument("--expect-visible-count", type=int, help="Require this many resolved visible IDs; use with --scope visible.")
    parser.add_argument("--provided-visible-count", type=int, help="Count stated by the user; rejects a mismatch before any write.")
    parser.add_argument("--fail-on-source-conflict", action="store_true", help="Fail when a visible ID has multiple source candidates.")
    parser.add_argument("--require-chinese", action="store_true", help="Fail when a visible item's sidebar short description has no Chinese text; command names remain original by design.")
    parser.add_argument("--require-ready", action="store_true", help="Fail when a visible item still needs agent translation refinement or source confirmation.")
    parser.add_argument("--batch-size", type=int, default=0, help="Limit the emitted scope items for P1 refinement batches.")
    parser.add_argument("--offset", type=int, default=0, help="Zero-based offset used with --batch-size.")
    args = parser.parse_args()
    catalog_dir = args.catalog_dir or args.root / "cache" / "remote_plugin_catalog"
    staging_dir = args.root / ".tmp" / "bundled-marketplaces"
    watched = watched_source_files(args.root, catalog_dir, args.runtime_dir, staging_dir if staging_dir.exists() else None, args.user_skill_dir)
    before = source_hashes(watched) if args.check_unchanged else {}
    items, _ = collect(args.root, catalog_dir, args.runtime_dir, staging_dir if staging_dir.exists() else None, args.user_skill_dir)
    # Formatting happens after collection; this script intentionally has no write path.
    summary = inventory_summary(items)
    try:
        scoped_items = logical_items(items, args.scope, args.visible_id)
    except ValueError as exc:
        parser.error(str(exc))
    if args.expect_visible_count is not None:
        if args.scope != "visible" or args.expect_visible_count < 0:
            parser.error("--expect-visible-count 只能与 visible 范围及非负数一起使用")
        if len(scoped_items) != args.expect_visible_count:
            parser.error(f"可见项数量不完整：期望 {args.expect_visible_count}，实际 {len(scoped_items)}")
    if args.provided_visible_count is not None:
        if args.provided_visible_count < 0:
            parser.error("--provided-visible-count 必须为非负数")
        if args.scope != "visible":
            parser.error("--provided-visible-count 只能与 visible 范围一起使用")
        if args.provided_visible_count != len(args.visible_id):
            parser.error(f"用户声明数量与提供 ID 数量不一致：声明 {args.provided_visible_count}，提供 {len(args.visible_id)}")
    conflicts = [item["id"] for item in scoped_items if item.get("source_conflict")]
    if args.fail_on_source_conflict and conflicts:
        parser.error("可见项存在来源冲突，需先确认实际 UI 来源: " + ", ".join(conflicts))
    unresolved = unresolved_visible_items(scoped_items) if args.scope == "visible" else []
    if args.require_ready and unresolved:
        parser.error("可见项尚未达到 ready 或来源未确认: " + ", ".join(unresolved))
    untranslated = untranslated_visible_items(scoped_items) if args.require_chinese else []
    if args.batch_size < 0 or args.offset < 0:
        parser.error("--batch-size and --offset must be non-negative")
    if args.batch_size:
        scoped_items = scoped_items[args.offset: args.offset + args.batch_size]
    output = {
        "mode": "read_only", "only_list": True, "scope": args.scope,
        "inventory_summary": (
            {"visible_items": len(scoped_items), "note": "仅输出用户提供证据表明当前 UI 可见的技能。"}
            if args.scope == "visible" else summary
        ), "items": scoped_items,
        "batch": {"offset": args.offset, "size": args.batch_size or None},
        "user_provided_visible_count": args.provided_visible_count,
        "source_conflicts": conflicts,
        "unresolved_visible_items": unresolved,
        "watched_source_count": len(watched),
    }
    after = source_hashes(watched) if args.check_unchanged else {}
    if args.check_unchanged and before != after:
        print("扫描源 SHA256 在运行期间变化", file=sys.stderr)
        return 2
    if untranslated:
        print("可见项仍含英文展示字段: " + ", ".join(untranslated), file=sys.stderr)
        return 3
    if args.as_json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(markdown(scoped_items, args.scope))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
