#!/usr/bin/env python3
"""Fixture tests for read-only skill/plugin issue discovery."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_SOURCE = ROOT / "tests" / "fixture-data" / "codex-display"
FIXTURE = Path(tempfile.mkdtemp(prefix="codex-issue-audit-")) / "codex-display"
shutil.copytree(FIXTURE_SOURCE, FIXTURE)
for source in FIXTURE.rglob("SKILL.fixture.md"):
    source.rename(source.with_name("SKILL.md"))
SCRIPT = ROOT / "scripts" / "audit_skill_plugin_issues.py"
spec = importlib.util.spec_from_file_location("issue_audit", SCRIPT)
audit_module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(audit_module)


def main() -> None:
    report, watched = audit_module.audit(
        FIXTURE,
        FIXTURE / "remote_plugin_catalog",
        FIXTURE / "missing-runtime",
        None,
        FIXTURE / "missing-user-skills",
        "installed",
        [],
    )
    assert watched
    assert report["mode"] == "read_only"
    assert report["summary"]["items_scanned"] == 3
    assert len(report["skill_scores"]) == 3
    assert set(report["relationship_counts"]) == {"conflict", "complementary", "unrelated"}
    assert report["recommendations"]
    assert report["external_candidate_status"].startswith("unavailable")
    assert report["profile"]["status"] == "unavailable"
    codes = {entry["code"] for entry in report["issues"]}
    assert "SOURCE_DIVERGENCE" in codes
    assert "DESCRIPTION_NEEDS_REFINEMENT" not in codes
    divergent = next(entry for entry in report["issues"] if entry["code"] == "SOURCE_DIVERGENCE")
    assert "确认" in divergent["remediation"]
    human_report = audit_module.render_human_report(report)
    assert "结论:" in human_report
    assert "需处理" in human_report
    assert "SOURCE_DIVERGENCE" in human_report
    assert "附注: 已折叠" not in human_report
    assert "安装全景" in human_report
    assert "使用频率" in human_report
    assert "优化建议" in human_report
    assert report["inventory_analysis"]["usage_evidence"].startswith("unavailable")
    compact_report = {"summary": {"items_scanned": 1, "by_severity": {"critical": 0, "warning": 0, "info": 2}}, "scope": "installed", "mode": "read_only", "issues": [], "relationships": [], "profile": {"status": "observed"}, "external_candidate_status": "observed", "inventory_analysis": {"profile_status": "observed", "usage_evidence": "unavailable: fixture", "bundles": [], "action_candidates": [], "context_pressure_note": "fixture"}}
    assert "附注: 已折叠 2 条非阻断提示" in audit_module.render_human_report(compact_report)

    visible_item = {
        "id": "visible-needs-refinement",
        "source_type": "codex_global_skill",
        "source_paths": [],
        "fact_status": "observed",
        "inventory_scope": "visible",
        "translation_quality": "needs_agent_refinement",
        "editable": True,
        "command_palette": {"original": "Visible fixture"},
        "sidebar": {"original": "English description", "short_description": "通用技能"},
    }
    visible_issues = audit_module.audit_item(visible_item)
    assert any(entry["code"] == "DESCRIPTION_NEEDS_REFINEMENT" for entry in visible_issues)
    visible_score = audit_module.score_items([visible_item], visible_issues, "", "unavailable")[0]
    assert visible_score["dimensions"]["description"] == 6

    def fake(skill_id, display, description):
        return {"id": skill_id, "command_palette": {"original": display}, "sidebar": {"original": description, "short_description": description}}

    conflict_items = [fake("research-a", "调研", "调研 → 多平台搜索"), fake("research-b", "调研", "调研 → 网页资料搜索")]
    conflict_scores = [{"id": item["id"], "profile_alignment": {"matched_terms": ["调研"]}} for item in conflict_items]
    relations, _ = audit_module.relationships(conflict_items, conflict_scores)
    assert any(entry["relationship"] == "conflict" for entry in relations)

    identifier_items = [
        fake("summarize", "summarize", "总结 → 当前任务交接"),
        fake("skills-summarize-audit", "skills-summarize-audit", "技能审查 → 已安装技能审计"),
    ]
    identifier_scores = [{"id": item["id"], "profile_alignment": {"matched_terms": []}} for item in identifier_items]
    relations, _ = audit_module.relationships(identifier_items, identifier_scores)
    assert not any(entry["relationship"] == "conflict" for entry in relations)

    complement_items = [fake("research", "调研", "调研 → 多平台检索"), fake("summarize", "总结", "总结 → 文本压缩")]
    complement_scores = [{"id": item["id"], "profile_alignment": {"matched_terms": ["知识"]}} for item in complement_items]
    relations, _ = audit_module.relationships(complement_items, complement_scores)
    assert any(entry["relationship"] == "complementary" for entry in relations)
    print(json.dumps({"result": "passed", "issue_count": report["summary"]["issues"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
