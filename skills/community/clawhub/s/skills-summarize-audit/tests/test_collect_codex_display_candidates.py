#!/usr/bin/env python3
"""Fixture tests for the read-only Codex display candidate collector."""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_SOURCE = ROOT / "tests" / "fixture-data" / "codex-display"
FIXTURE = Path(tempfile.mkdtemp(prefix="codex-display-")) / "codex-display"
shutil.copytree(FIXTURE_SOURCE, FIXTURE)
for source in FIXTURE.rglob("SKILL.fixture.md"):
    source.rename(source.with_name("SKILL.md"))
assert any(part.startswith("codex-display-") for part in FIXTURE.parts), "fixture 必须覆盖随机数字路径"
SCRIPT = ROOT / "scripts" / "collect_codex_display_candidates.py"

spec = importlib.util.spec_from_file_location("collector", SCRIPT)
collector = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(collector)


def hashes():
    return {str(p.relative_to(FIXTURE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FIXTURE.rglob("*") if p.is_file()}


def main():
    before = hashes()
    items, watched = collector.collect(FIXTURE, FIXTURE / "remote_plugin_catalog", FIXTURE / "missing-runtime")
    after = hashes()
    assert before == after, "只读采集器修改了 fixture"
    assert watched, "未记录扫描源"
    by_type = {item["source_type"]: item for item in items if item["fact_status"] == "observed"}
    for source in ("codex_global_skill", "codex_plugin_cache", "codex_plugin_manifest", "remote_plugin_catalog"):
        assert source in by_type, f"缺少来源 {source}"
        item = by_type[source]
        assert item["only_list"] is True
        if source != "codex_global_skill":
            assert item["editable"] is False
        assert item["command_palette"]["original"] and item["sidebar"]["original"]
        assert item["command_palette"]["display_name"] == item["command_palette"]["original"]
        assert any("\u4e00" <= char <= "\u9fff" for char in item["sidebar"]["short_description"])
        assert len(item["command_palette"]["display_name"]) <= collector.DISPLAY_MAX
        assert len(item["sidebar"]["short_description"]) <= collector.SHORT_MAX
        assert len(item["sidebar"]["long_description"]) <= collector.LONG_MAX
    assert by_type["codex_global_skill"]["sidebar"]["short_description"] == "基于审核证据生成业务决策报告"
    assert by_type["codex_plugin_cache"]["sidebar"]["short_description"] == "分析或发布前评估表格与数据集"
    assert by_type["remote_plugin_catalog"]["sidebar"]["short_description"] == "创建有依据的产品指标仪表板"
    assert by_type["remote_plugin_catalog"]["translation_quality"] == "ready"
    assert by_type["remote_plugin_catalog"]["long_description_quality"] == "ready"
    assert by_type["remote_plugin_catalog"]["sidebar"]["long_original"] == "Build dashboards for product metrics."
    mixed_candidate, mixed_method = collector.chinese_candidate("Build 中 dashboard", collector.SHORT_MAX, "fixture")
    assert mixed_method == "glossary_partial_needs_refinement"
    assert mixed_candidate != "Build 中 dashboard"
    summary = collector.inventory_summary(items)
    installed_plugin = next(item for item in items if item["source_type"] == "codex_plugin_cache")
    assert installed_plugin["plugin_ref"] == "fixture-plugin@fixture-market"
    assert installed_plugin["installation_status"] == "installed_enabled"
    assert installed_plugin["installation_evidence"]
    assert by_type["codex_plugin_manifest"]["command_palette"]["display_name"] == by_type["codex_plugin_manifest"]["command_palette"]["original"]
    assert by_type["codex_plugin_manifest"]["sidebar"]["short_description"] == "创建可复用工件模板"
    assert summary["installed_unique_items"] == 3
    assert summary["catalog_only_source_records"] == 1
    assert len(collector.logical_items(items, "installed")) == 3
    assert len(collector.logical_items(items, "catalog")) == 1
    cached_only = dict(installed_plugin)
    cached_only.update({"id": "cached-only", "installation_status": "cached_only", "installation_evidence": []})
    assert "cached-only" not in {item["id"] for item in collector.logical_items([*items, cached_only], "installed")}
    assert "cached-only" in {item["id"] for item in collector.logical_items([*items, cached_only], "all")}
    visible = collector.logical_items(items, "visible", ["fixture-global", "fixture-plugin"])
    assert [item["id"] for item in visible] == ["fixture-global", "fixture-plugin"]
    assert all(item["inventory_scope"] == "visible" for item in visible)
    assert collector.untranslated_visible_items(visible) == []
    assert collector.unresolved_visible_items(visible) == ["fixture-plugin"]
    namespaced = collector.logical_items(items, "visible", ["$fixture:fixture-global"])
    assert namespaced[0]["input_id"] == "$fixture:fixture-global"
    assert namespaced[0]["normalized_id"] == "fixture-global"
    assert collector.substantial_chinese("使用 CONTEXT、ADR 和 frontmatter 生成报告")
    assert any(item["source_conflict"] for item in collector.logical_items(items, "installed") if item["id"] == "fixture-plugin")
    try:
        collector.logical_items(items, "visible", [])
    except ValueError as exc:
        assert "--visible-id" in str(exc)
    else:
        raise AssertionError("visible 范围未拒绝空清单")
    selected_plugin = next(item for item in collector.logical_items(items, "installed") if item["id"] == "fixture-plugin")
    assert "1.0.0" in selected_plugin["source_paths"][0]
    assert selected_plugin["selection_reason"] == "highest_non_temporary_cache_version"
    assert selected_plugin["source_resolution_status"] == "requires_ui_confirmation"
    assert "暂停写入" in selected_plugin["source_resolution_plan"]
    catalog_item = next(item for item in items if item["source_type"] == "remote_plugin_catalog")
    assert catalog_item["source_resolution_status"] == "single_source"
    installed_markdown = collector.markdown(collector.logical_items(items, "installed"), "installed")
    assert "fixture-catalog" not in installed_markdown
    assert "（installed，3 项）" in installed_markdown
    assert collector.GLOSSARY["skill_overrides"]["imagegen"]["display_name"] == "图像生成"

    # 用户声明数量与 ID 数量不一致时，必须在写入前失败。
    command = [
        sys.executable, str(SCRIPT), "--root", str(FIXTURE), "--catalog-dir", str(FIXTURE / "remote_plugin_catalog"),
        "--runtime-dir", str(FIXTURE / "missing-runtime"), "--user-skill-dir", str(FIXTURE / "missing-user-skills"),
        "--scope", "visible", "--provided-visible-count", "1",
        "--visible-id", "fixture-global", "--visible-id", "fixture-plugin",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode != 0
    assert "数量不一致" in (result.stderr + result.stdout)

    ready_command = [
        sys.executable, str(SCRIPT), "--root", str(FIXTURE), "--catalog-dir", str(FIXTURE / "remote_plugin_catalog"),
        "--runtime-dir", str(FIXTURE / "missing-runtime"), "--user-skill-dir", str(FIXTURE / "missing-user-skills"),
        "--scope", "visible", "--visible-id", "fixture-plugin", "--require-ready",
    ]
    ready_result = subprocess.run(ready_command, capture_output=True, text=True)
    assert ready_result.returncode != 0
    assert "ready" in (ready_result.stderr + ready_result.stdout)

    # 可选的 Junction/符号链接目录不可阻断扫描；无法创建时跳过该平台专属部分。
    link_root = Path(tempfile.mkdtemp(prefix="codex-links-"))
    try:
        link = link_root / "broken-junction"
        try:
            link.symlink_to(link_root / "missing-target", target_is_directory=True)
        except (OSError, NotImplementedError):
            pass
        else:
            assert collector.skill_files(link_root) == []
    finally:
        shutil.rmtree(link_root, ignore_errors=True)
    print(json.dumps({"result": "passed", "candidate_count": len(items)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
