"""Budget enforcement: max_sources, max_runtime_min, soft/hard limit, depth presets."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run


def test_budget_source_hard_limit(root: Path) -> None:
    budget_root = root / "budget-root"
    budget_root.mkdir(parents=True, exist_ok=True)
    json_out(run("create", "--root", str(budget_root), "--id", "budget-src", "--goal", "Max sources budget test", "--max-sources", "3", "--depth", "S", "--skip-preflight"))
    lease1 = json_out(run("begin", "--root", str(budget_root), "--id", "budget-src"))
    res1 = Path(lease1["paths"]["result_file"])
    res1.write_text(
        json.dumps({"summary": "Iteration 1 with source.", "phase": "search", "meaningful_progress": True, "sources": [{"url": "https://b1.example.com/1", "title": "Source 1"}, {"url": "https://b1.example.com/2", "title": "Source 2"}], "findings": [{"text": "Finding 1"}], "notify_recommendation": "silent"}),
        encoding="utf-8",
    )
    fin1 = json_out(run("finish", "--root", str(budget_root), "--id", "budget-src", "--run-id", lease1["run_id"], "--result-file", str(res1)))
    assert_eq(fin1["status"], "idle", "should stay idle after 2/3 sources")
    assert_eq(fin1["budget_phase"], "normal", "phase normal at 67% source utilization")
    assert_eq(fin1["total_sources"], 2, "should have 2 sources")

    lease2 = json_out(run("begin", "--root", str(budget_root), "--id", "budget-src"))
    res2 = Path(lease2["paths"]["result_file"])
    res2.write_text(
        json.dumps({"summary": "Iteration 2 adds source 3, hits max.", "phase": "search", "meaningful_progress": True, "sources": [{"url": "https://b2.example.com/3", "title": "Source 3"}], "findings": [{"text": "Finding 2"}], "notify_recommendation": "silent"}),
        encoding="utf-8",
    )
    fin2 = json_out(run("finish", "--root", str(budget_root), "--id", "budget-src", "--run-id", lease2["run_id"], "--result-file", str(res2)))
    assert_eq(fin2["status"], "idle", "budget auto-completion should route to adequacy before review")
    assert_eq(fin2["normalized_reason"], "continued:iteration-complete", "budget precheck should continue through adequacy")
    assert_true(not fin2["review_gated"], "budget auto-completion should not be review-gated before adequacy")
    assert_eq(fin2["budget_phase"], "hard_limit", "phase should be hard_limit at 100%")
    assert_eq(fin2["total_sources"], 3, "should have 3 sources total")
    state = json.loads((budget_root / "budget-src" / "state.json").read_text(encoding="utf-8"))
    assert_eq(state["phase"], "verify", "budget auto-completion should require adequacy verification")
    assert_eq(state["delivery"]["review_ready"], False, "budget auto-completion should not mark report review-ready before adequacy")
    assert_eq(state["delivery"]["ready"], False, "budget auto-completion must not mark report delivery-ready")

    summary = json_out(run("summary", "--root", str(budget_root), "--id", "budget-src", "--format", "json"))
    assert_in("budget_phase", summary, "summary json should expose budget_phase")
    bp = summary["budget_phase"]
    assert_eq(bp["phase"], "hard_limit", "summary budget_phase phase should be hard_limit")
    assert_eq(bp["max_sources"], 3, "summary should show max_sources")
    assert_true(bp["source_pct"] is not None, "summary budget_phase should include source_pct")

    summary_text = run("summary", "--root", str(budget_root), "--id", "budget-src", "--format", "text").stdout
    assert_in("Budget:", summary_text, "summary text should expose budget info")
    assert_in("hard_limit", summary_text, "summary text should show budget phase")

    draft_md = run("draft-report", "--root", str(budget_root), "--id", "budget-src", "--format", "markdown").stdout
    assert_in("Budget phase:", draft_md, "draft report should expose budget phase")

    playbook = (budget_root / "budget-src" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("## Budget", playbook, "playbook should have ## Budget section")
    assert_in("hard_limit", playbook, "playbook budget section should show phase")


def test_budget_no_constraint(root: Path) -> None:
    budget_root = root / "budget-none-root"
    budget_root.mkdir(parents=True, exist_ok=True)
    json_out(run("create", "--root", str(budget_root), "--id", "budget-none", "--goal", "No budget constraint test", "--depth", "S"))
    summary = json_out(run("summary", "--root", str(budget_root), "--id", "budget-none", "--format", "json"))
    bp = summary["budget_phase"]
    assert_eq(bp["phase"], "normal", "phase normal when no sources collected")
    assert_eq(bp["max_sources"], 15, "should inherit default max_sources from S preset")


def test_budget_soft_limit(root: Path) -> None:
    budget_root = root / "budget-soft-root"
    budget_root.mkdir(parents=True, exist_ok=True)
    json_out(run("create", "--root", str(budget_root), "--id", "budget-soft", "--goal", "Soft limit test", "--max-sources", "10", "--skip-preflight"))
    lease = json_out(run("begin", "--root", str(budget_root), "--id", "budget-soft"))
    res = Path(lease["paths"]["result_file"])
    res.write_text(
        json.dumps({"summary": "At 80% source utilization.", "phase": "search", "meaningful_progress": True, "sources": [{"url": f"https://soft.example.com/{i}", "title": f"S{i}"} for i in range(8)], "findings": [], "notify_recommendation": "silent"}),
        encoding="utf-8",
    )
    fin = json_out(run("finish", "--root", str(budget_root), "--id", "budget-soft", "--run-id", lease["run_id"], "--result-file", str(res)))
    assert_eq(fin["status"], "idle", "soft limit should not stop iteration")
    assert_eq(fin["budget_phase"], "soft_limit", "phase should be soft_limit at 80%")
    assert_eq(fin["normalized_reason"], "continued:iteration-complete", "soft limit should allow iteration to continue")
    assert_eq(fin["budget_phase_detail"]["dominant_limit"], "sources", "dominant limit should stay on the highest-utilization budget dimension")
    assert_in("budget_phase_detail", fin, "finish response should expose budget_phase_detail")
    detail = fin["budget_phase_detail"]
    assert_eq(detail["soft_pct"], 0.80, "soft_pct should be 0.80")
    assert_eq(detail["max_sources"], 10, "detail should show max_sources")

    lease_check = json_out(run("begin", "--root", str(budget_root), "--id", "budget-soft"))
    assert_in("budget_phase", lease_check, "work order should expose budget_phase")
    assert_in("budget_phase_detail", lease_check, "work order should expose budget_phase_detail")
    assert_eq(lease_check["budget_phase"], "soft_limit", "work order budget_phase should be soft_limit")
    assert_true(any("synthesis" in item.lower() or "prioritize synthesis" in item.lower() for item in lease_check["execution_guidance"]), "work order guidance should mention synthesis at soft_limit")
    assert_in("max_runtime_min", lease_check["budget_phase_detail"], "work order budget_phase_detail should include max_runtime_min")
    run("fail", "--root", str(budget_root), "--id", "budget-soft", "--run-id", lease_check["run_id"], "--error", "cleanup")


def test_budget_runtime_hard_limit(root: Path) -> None:
    budget_root = root / "budget-rt-root"
    budget_root.mkdir(parents=True, exist_ok=True)
    json_out(run("create", "--root", str(budget_root), "--id", "budget-rt", "--goal", "Runtime budget test", "--max-runtime-min", "60", "--skip-preflight"))
    state_path = budget_root / "budget-rt" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    old_ts = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=65)
    state["created_at"] = old_ts.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lease = json_out(run("begin", "--root", str(budget_root), "--id", "budget-rt"))
    res = Path(lease["paths"]["result_file"])
    res.write_text(
        json.dumps({"summary": "First iteration before runtime budget expires.", "phase": "search", "meaningful_progress": True, "sources": [{"url": "https://rt.example.com/1", "title": "RT Source"}], "findings": [{"text": "RT Finding"}], "notify_recommendation": "silent"}),
        encoding="utf-8",
    )
    fin = json_out(run("finish", "--root", str(budget_root), "--id", "budget-rt", "--run-id", lease["run_id"], "--result-file", str(res)))
    assert_eq(fin["status"], "idle", "runtime budget auto-completion should route to adequacy before review")
    assert_eq(fin["normalized_reason"], "continued:iteration-complete", "runtime budget precheck should continue through adequacy")
    assert_true(not fin["review_gated"], "runtime budget auto-completion should not be review-gated before adequacy")
    assert_eq(fin["budget_phase"], "hard_limit", "phase should be hard_limit when runtime exceeded")
    assert_true(fin.get("reached_max_runtime"), "finish response should signal reached_max_runtime")
    assert_true(fin.get("total_runtime_min") is not None, "finish response should include total_runtime_min")
    assert_true(fin["budget_phase_detail"].get("runtime_pct") is not None, "budget_phase_detail should include runtime_pct")
    assert_eq(fin["budget_phase_detail"]["dominant_limit"], "runtime", "runtime should be dominant limit when max_runtime_min exceeded")
    state_rt = json.loads((budget_root / "budget-rt" / "state.json").read_text(encoding="utf-8"))
    assert_eq(state_rt["phase"], "verify", "runtime budget should require adequacy verification")
    assert_eq(state_rt["delivery"]["review_ready"], False, "runtime budget should not mark review_ready before adequacy")

    summary_rt = json_out(run("summary", "--root", str(budget_root), "--id", "budget-rt", "--format", "json"))
    bp_rt = summary_rt["budget_phase"]
    assert_eq(bp_rt["phase"], "hard_limit", "summary budget_phase should be hard_limit")
    assert_eq(bp_rt["max_runtime_min"], 60, "summary should expose max_runtime_min")
    assert_true(bp_rt["total_runtime_min"] is not None, "summary budget_phase should include total_runtime_min")
    assert_true(bp_rt["runtime_pct"] is not None, "summary budget_phase should include runtime_pct")

    summary_rt_text = run("summary", "--root", str(budget_root), "--id", "budget-rt", "--format", "text").stdout
    assert_in("rt_pct=", summary_rt_text, "summary text should expose runtime percentage in budget line")
    draft_rt_md = run("draft-report", "--root", str(budget_root), "--id", "budget-rt", "--format", "markdown").stdout
    assert_in("rt 100%", draft_rt_md, "draft report should expose runtime percentage in budget line")
    playbook_rt = (budget_root / "budget-rt" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("Runtime budget:", playbook_rt, "task playbook should include runtime budget details")
