"""Behavior regressions for missing evidence, provenance, baseline reuse and exports."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_skill_plugin_issues import audit, audit_ecosystem, assess_mcp_health, inventory_analysis, render_ecosystem_report
from compute_value_scores import assess_skills_optimization, assess_mcp_optimization, value_score, market_score
from extract_usage_signals import aggregate_signals, merge_with_mcp_config, _parse_codex_session_file
from scan_state import digest_paths, plan_scan, finish_scan
from collect_codex_display_candidates import enrich_source_conflicts


def market(**overrides):
    return {"status": "market_observed", "source_url": "https://example.org/fixture", "license": "MIT",
            "checked_at": datetime.now(timezone.utc).isoformat(), "scoring_basis": "fixture only", "score": 8, **overrides}


@pytest.mark.parametrize("usage", [{}, {"other": {"invocations": 10}}])
def test_no_usage_cannot_decommission(usage):
    rec = assess_skills_optimization([{"id": "a", "health_score": 0,
                                     "profile_alignment": {"status": "observed", "score": 0}}], usage)[0]
    assert rec["value_score"] is None
    assert rec["layer"] == "pending_evidence"
    assert rec["breakdown"]["usage"] is None
    assert rec["breakdown"]["market"] is None


def test_complete_inputs_and_stale_market():
    item = {"id": "a", "health_score": 8, "profile_alignment": {"status": "observed", "score": 8}}
    usage = {"a": {"invocations": 10, "status": "observed"}}
    assert assess_skills_optimization([item], usage, {"skill:a": market()})[0]["value_score"] == 8.8
    old = market(checked_at=(datetime.now(timezone.utc) - timedelta(days=31)).isoformat())
    assert assess_skills_optimization([item], usage, {"skill:a": old})[0]["layer"] == "pending_evidence"
    assert market_score(market(license=None)) is None


@pytest.mark.parametrize("missing", [None, float("nan"), -1, 11, True])
def test_invalid_score_never_ranks(missing):
    assert value_score(8, 8, 8, missing) is None


def test_low_score_requires_coverage_and_dependencies():
    scores = [{"id": "a", "health_score": 0, "profile_alignment": {"status": "observed", "score": 0}}]
    usage = {"a": {"invocations": 0, "status": "observed", "coverage_complete": True}}
    evidence = {"skill:a": market(score=0)}
    assert assess_skills_optimization(scores, usage, evidence)[0]["layer"] == "watch"
    usage["a"]["dependency_review_complete"] = True
    assert assess_skills_optimization(scores, usage, evidence)[0]["layer"] == "uninstall_candidate"


def test_mcp_health_is_not_project_alignment_or_startup():
    health = assess_mcp_health({"fixture": {"command": "unavailable-fixture", "args": [],
                                           "env": {"API_TOKEN": "private-test-token"}}}, {})
    assert health[0]["dimensions"]["startup"]["status"] == "unavailable"
    assert health[0]["grade"] == "partial"
    assert "private-test-token" not in json.dumps(health)
    assert health[0]["dimensions"]["permissions"]["status"] == "unavailable"
    rec = assess_mcp_optimization(health, [{"mcp_server": "fixture", "tool_calls": 20}], {"mcp:fixture": market()})[0]
    assert rec["breakdown"]["alignment"] is None
    assert rec["layer"] == "pending_evidence"


def record(client, server):
    return {"agent_id": client + "_fixture", "profile_id": client, "profile_name": client,
            "total_duration_ms": 0, "total_tokens": 0, "created_at": None, "tool_distribution": {},
            "mcp_calls": [{"tool": f"mcp__{server}__search", "ts": None}], "skill_invocations": [],
            "python_packages": []}


def test_mcp_client_attribution_is_not_scan_scope():
    result = aggregate_signals([record("codex", "alpha"), record("claude", "beta")], clients_scanned=["zcode", "codex", "claude"])
    result = merge_with_mcp_config(result, None, ["zcode", "codex", "claude"])
    by_server = {m["mcp_server"]: m for m in result["mcp_usage_evidence"]}
    assert by_server["alpha"]["observed_in_clients"] == ["codex"]
    assert by_server["beta"]["observed_in_clients"] == ["claude"]
    assert merge_with_mcp_config({}, None)["mcp_usage_evidence"] == []


def test_codex_function_calls_use_event_window_and_string_inputs(tmp_path):
    log = tmp_path / "rollout-fixture.jsonl"
    old = {"timestamp": "2025-01-01T00:00:00Z", "type": "session_meta", "payload": {}}
    recent = {"timestamp": "2026-09-01T00:00:00Z", "type": "response_item",
              "payload": {"type": "function_call", "name": "mcp__firecrawl__search", "arguments": "{}"}}
    custom = {"timestamp": "2026-09-01T01:00:00Z", "type": "response_item",
              "payload": {"type": "custom_tool_call", "name": "Bash", "input": "plain script"}}
    log.write_text("\n".join(json.dumps(row) for row in [old, recent, custom]), encoding="utf-8")
    result = _parse_codex_session_file(log, datetime(2026, 8, 20, tzinfo=timezone.utc))
    assert result["total_tool_use_count"] == 2
    assert result["mcp_calls"] == [{"tool": "mcp__firecrawl__search", "ts": recent["timestamp"]}]
    assert result["created_at"] == recent["timestamp"]
    log.write_text(json.dumps(old), encoding="utf-8")
    assert _parse_codex_session_file(log, datetime(2026, 8, 20, tzinfo=timezone.utc)) is None


@pytest.fixture
def local_tree(tmp_path):
    root = tmp_path / "codex"
    skill = root / "skills" / "example"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: example\ndescription: 示例技能 → 文件分析\n---\n# Example\n", encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text('interface:\n  display_name: "Example"\n  short_description: "示例技能 → 文件分析"\n', encoding="utf-8")
    return root


def run_audit(root, **kwargs):
    return audit(root, root / "catalog", root / "runtime", None, root / "users", "installed", [], **kwargs)[0]


def test_real_baseline_readonly_and_reference_change(local_tree):
    files = list(local_tree.rglob("*"))
    before = digest_paths(p for p in files if p.is_file())
    first = run_audit(local_tree)
    assert first["scan"]["mode"] == "full"
    second = run_audit(local_tree, baseline=first["baseline"])
    assert second["scan"]["mode"] == "incremental"
    assert second["scan"]["reused"] == 1
    assert second["issues"] == first["issues"]
    assert digest_paths(p for p in files if p.is_file()) == before
    ref = local_tree / "skills/example/reference.md"
    ref.write_text("new reference", encoding="utf-8")
    third = run_audit(local_tree, baseline=second["baseline"])
    assert third["scan"]["checked"] == 1
    assert third["scan"]["suggest_full_scan"]
    assert run_audit(local_tree, baseline=third["baseline"], scan_mode="full")["scan"]["mode"] == "full"


def test_stale_baseline_and_scope_changes(local_tree):
    first = run_audit(local_tree)
    first["baseline"]["created_at"] = (datetime.now(timezone.utc) - timedelta(days=31)).isoformat()
    assert run_audit(local_tree, baseline=first["baseline"])["scan"]["mode"] == "full"
    first = run_audit(local_tree)
    first["baseline"]["context"]["scope"] = "visible"
    assert run_audit(local_tree, baseline=first["baseline"])["scan"]["mode"] == "full"


def test_malformed_baseline_falls_back(local_tree):
    assert run_audit(local_tree, baseline=["wrong schema"])["scan"]["mode"] == "full"
    baseline = run_audit(local_tree)["baseline"]
    baseline["fingerprints"] = []
    assert run_audit(local_tree, baseline=baseline)["scan"]["mode"] == "full"


def test_external_reference_change_invalidates_reuse(local_tree):
    skill = local_tree / "skills/example/SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\nSee references/shared.md\n", encoding="utf-8")
    ref = local_tree / "references/shared.md"
    ref.parent.mkdir()
    ref.write_text("fixture", encoding="utf-8")
    first = run_audit(local_tree)
    assert not first["issues"]
    assert run_audit(local_tree, baseline=first["baseline"])["scan"]["reused"] == 1
    ref.unlink()
    next_report = run_audit(local_tree, baseline=first["baseline"])
    assert next_report["scan"]["reused"] == 0
    assert any(i["code"] == "REFERENCE_MISSING" for i in next_report["issues"])


@pytest.mark.parametrize("payload", [["invalid"], {"mcp_usage_evidence": ["wrong"]}, {"skill_invocation_evidence": {"wrong": 1}},
    {"mcp_usage_evidence": [{"mcp_server": "a", "tool_calls": "many"}]},
    {"mcp_usage_evidence": [{"mcp_server": "a", "tool_calls": -1}]},
    {"skill_invocation_evidence": [{"skill_id": "a", "invocations": True}]},
    {"scan_summary": {"coverage_complete": "yes"}},
    {"agent_dispatch_stats": [{"profile_id": "a", "dispatch_count": -1}]}])
def test_invalid_signals_remain_unavailable(local_tree, payload):
    path = local_tree / "signals.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    report = audit_ecosystem(local_tree / "skills", local_tree / "missing-config.json", None, path, root=local_tree, runtime_dir=local_tree / "runtime")
    assert report["signals_status"].startswith("unavailable")
    assert report["ecosystem_assessment"]["optimization"]["summary"]["hide"] == 0


def test_incremental_escalation_rules():
    scan = {"mode": "incremental", "reasons": []}
    snapshot = {"fingerprints": {}, "findings": {}}
    finish_scan(scan, snapshot, [{"id": "a", "severity": "critical"}], {"available": 1, "total": 4})
    assert scan["suggest_full_scan"] and len(scan["reasons"]) == 2


def test_ecosystem_missing_signals_has_actionable_gap(local_tree):
    cfg = local_tree / "mcp.json"
    cfg.write_text(json.dumps({"mcpServers": {"a": {"command": "fixture", "args": []}}}), encoding="utf-8")
    result = audit_ecosystem(local_tree / "skills", cfg, None, root=local_tree, runtime_dir=local_tree / "runtime")
    summary = result["ecosystem_assessment"]["optimization"]["summary"]
    assert summary["hide"] == summary["uninstall_candidates"] == 0
    assert summary["pending_evidence"] > 0
    text = render_ecosystem_report(result)
    assert "高价值工具（Top 5）" not in text
    assert "证据不足" in text and "建议执行" in text
    for action in result["actions"]:
        assert all(key in action for key in ("target", "problem", "evidence", "judgment", "steps", "execution_agent", "verification", "rollback", "status", "market", "exposure"))


def test_shared_gaps_are_grouped_but_target_plans_remain(local_tree):
    result = audit_ecosystem(local_tree / "skills", local_tree / "missing.json", None, root=local_tree, runtime_dir=local_tree / "runtime")
    recs = result["ecosystem_assessment"]["optimization"]["skill_recommendations"]
    assert len(result["actions"]) == 1
    assert result["actions"][0]["evidence"]["targets"] == [r["target"] for r in recs]
    assert all(r["action_plan"]["target"] == r["target"] for r in recs)
    text = render_ecosystem_report(result)
    assert "处理 0 个" not in text and "明确 0 个" not in text
    assert "Agent 层: unavailable" in text
    assert "Agent 层: 0 个" not in text
    assert "评估状态: partial" in text
    assert "{'available'" not in text
    result["ecosystem_assessment"]["agent_dispatch"]["status"] = "inferred"
    rendered = render_ecosystem_report(result)
    assert "Agent 层: 0 个" not in rendered
    assert "不代表已验证正常" in rendered


def test_partial_mcp_with_unknown_calls_renders(local_tree):
    result = audit_ecosystem(local_tree / "skills", local_tree / "missing.json", None, root=local_tree, runtime_dir=local_tree / "runtime")
    result["ecosystem_assessment"]["mcp_health"] = assess_mcp_health(
        {"fixture": {"command": "fixture", "args": []}},
        {"mcp_usage_evidence": [{"mcp_server": "fixture", "status": "configured_never_observed"}]})
    text = render_ecosystem_report(result)
    assert "（2/6 维）" in text and "fixture" in text


def test_invalid_usage_counts_are_unavailable_and_proxy_is_not_zero_usage():
    config = {"fixture": {"command": "fixture", "args": []}}
    malformed = {"mcp_usage_evidence": [{"mcp_server": "fixture", "tool_calls": "many", "status": "observed"}]}
    health = assess_mcp_health(config, malformed)
    usage = health[0]["dimensions"]["usage"]
    assert usage["status"] == "unavailable" and usage["calls"] is None

    proxy = {"mcp_usage_evidence": [{"mcp_server": "fixture", "tool_calls": 0,
                                      "status": "observed", "working_mode": "proxy_active"}]}
    proxy_health = assess_mcp_health(config, proxy)[0]
    assert proxy_health["dimensions"]["usage"]["status"] == "unavailable"
    assert proxy_health["dimensions"]["usage"]["calls"] is None
    assert proxy_health["dimensions"]["usage"]["proxy_active"] is True


def test_inferred_profile_alignment_counts_low_fit():
    items = [{"id": "skill:a", "source_type": "global", "source_paths": []}]
    scores = [{"id": "skill:a", "profile_alignment": {"status": "inferred", "score": 0}, "health_score": 8}]
    result = inventory_analysis(items, scores, [], "observed")
    assert result["bundles"][0]["low_suitability_items"] == 1


def test_explicit_in_memory_signals_preserve_coverage(local_tree):
    data = {"scan_summary": {"clients_scanned": ["codex"], "agents_scanned": 2, "coverage_complete": False}}
    result = audit_ecosystem(local_tree / "skills", local_tree / "missing.json", None, root=local_tree,
                             runtime_dir=local_tree / "runtime", signals_data=data)
    assert result["usage_coverage"] == data["scan_summary"]
    assert result["signals_status"] == "observed"
    assert "覆盖完整=False" in render_ecosystem_report(result)


def test_temporary_plugin_cache_does_not_create_active_conflict(tmp_path):
    items = []
    for relative, description in [("browser/1.0/.codex-plugin/plugin.json", "Current browser"),
                                  ("plugin-install-old/browser/0.9/.codex-plugin/plugin.json", "Old browser")]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"description": description}), encoding="utf-8")
        items.append({"id": "plugin:browser", "source_type": "codex_plugin_manifest", "source_paths": [str(path)],
                      "sidebar": {"original": description}, "command_palette": {"display_name": "Browser"},
                      "installation_status": "installed_enabled"})
    enrich_source_conflicts(items)
    assert not items[0]["source_conflict"]
    assert len(items[0]["source_candidates"]) == 2
    # Two normal installed sources still need explicit resolution.
    other = tmp_path / "browser/2.0/.codex-plugin/plugin.json"
    other.parent.mkdir(parents=True)
    other.write_text('{"description":"Different"}', encoding="utf-8")
    items[1]["source_paths"] = [str(other)]
    enrich_source_conflicts(items)
    assert items[0]["source_conflict"]


def test_explicit_export_does_not_overwrite(local_tree, tmp_path):
    output = tmp_path / "report.json"
    args = [sys.executable, str(ROOT / "scripts/audit_skill_plugin_issues.py"), "--root", str(local_tree),
            "--runtime-dir", str(local_tree / "runtime"), "--user-skill-dir", str(local_tree / "users"), "--json", "--output", str(output)]
    result = subprocess.run(args, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    content = output.read_bytes()
    assert json.loads(content)["baseline"]["schema_version"] == 1
    assert subprocess.run(args, capture_output=True).returncode == 2
    assert output.read_bytes() == content


def test_ecosystem_cli_baseline_reuses_unchanged_skills(local_tree, tmp_path):
    output = tmp_path / "ecosystem-baseline.json"
    args = [sys.executable, str(ROOT / "scripts/audit_skill_plugin_issues.py"),
            "--scope", "ecosystem", "--root", str(local_tree),
            "--runtime-dir", str(local_tree / "runtime"),
            "--user-skill-dir", str(local_tree / "users"),
            "--zcode-config", str(local_tree / "missing-config.json"),
            "--agents-dir", str(local_tree / "missing-agents"),
            "--reasonix-dir", str(local_tree / "missing-reasonix"), "--json"]
    first = subprocess.run(args + ["--output", str(output)], capture_output=True, text=True, encoding="utf-8")
    assert first.returncode == 0, first.stderr
    initial = json.loads(output.read_text(encoding="utf-8"))
    assert initial["scope"] == "ecosystem"
    assert initial["scan"]["mode"] == "full"
    second = subprocess.run(args + ["--baseline", str(output)], capture_output=True, text=True, encoding="utf-8")
    assert second.returncode == 0, second.stderr
    reused = json.loads(second.stdout)
    assert reused["scan"]["mode"] == "incremental"
    assert reused["scan"]["reused"] == 1
    assert reused["ecosystem_assessment"]["optimization"]["summary"]["hide"] == 0


@pytest.mark.parametrize("script", ["test_collect_codex_display_candidates.py", "test_audit_skill_plugin_issues.py", "test_analyze_project_profile.py"])
def test_legacy_fixture_entrypoints(script):
    result = subprocess.run([sys.executable, str(ROOT / "tests" / script)], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr


def test_version_gate_covers_all_public_sources():
    spec = importlib.util.spec_from_file_location("audit_validation", ROOT / "tests/validate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    versions = module.version_consistency()
    assert "MISSING" not in versions.values()
    assert set(versions.values()) == {"9.2.2"}
    assert "package.json" in versions and "report-template.md" in versions
