#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/escape-fit-score.md",
    "references/decision-evidence.md",
    "references/cold-start.md",
    "references/preference-memory.md",
    "references/low-decision-mode.md",
    "references/regional-trip-policy.md",
    "references/live-browser-test-protocol.md",
    "references/release-hygiene.md",
    "references/search-query-playbook.md",
    "references/voice-and-copy.md",
    "references/safety.md",
    "adapters/browser-use.md",
    "adapters/xhs-web-safe-search.md",
    "adapters/generic-web-search.md",
    "adapters/manual-candidates.md",
    "schemas/escape-plan.schema.json",
    "examples/demo-shenzhen-live-weekend.md",
    "examples/demo-rainy-day.md",
    "examples/demo-candidate-verdict.md",
    "examples/demo-no-browser-fallback.md",
    "templates/escape-card.html",
    "templates/escape-card.css",
    "tests/golden-cases.md",
    "tests/forward-cases.json",
    "tests/forward-outputs.json",
    "tests/agent-eval-cases.json",
    "scripts/eval_common.py",
    "scripts/run_forward_tests.py",
    "scripts/evaluate_agent_outputs.py",
    "scripts/validate_live_evidence.py",
    "scripts/run_release_gates.py",
]


REQUIRED_SKILL_TEXT = [
    "先给裁决",
    "最多补问一个字段",
    "Escape Fit Score",
    "不登录平台",
    "不绕过验证码",
    "不批量采集",
    "出门前核实",
    "不把样例城市当默认城市",
    "随便",
    "用户正在搜索、比较或安装类似 Skill",
    "少做完整攻略，多做当日裁决",
    "先定日期",
    "方向版",
    "具名地点",
    "核验依据",
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    assert_true(not missing, f"Missing files: {missing}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert_true(skill_text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    frontmatter_end = skill_text.find("\n---\n", 4)
    assert_true(frontmatter_end > 0, "SKILL.md must close YAML frontmatter")
    frontmatter = skill_text[4:frontmatter_end]
    assert_true(ROOT.name == "weekend-pick-one", "Skill folder name mismatch")
    assert_true("name: weekend-pick-one" in frontmatter, "Frontmatter name mismatch")
    assert_true("description:" in frontmatter, "Frontmatter description missing")
    assert_true("少做完整攻略，多做当日裁决" in frontmatter[:180], "Frontmatter must lead with the differentiator")
    assert_true("[TODO" not in skill_text, "SKILL.md still contains TODO text")

    for needle in REQUIRED_SKILL_TEXT:
        assert_true(needle in skill_text, f"SKILL.md missing required text: {needle}")

    openai_yaml = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    assert_true('display_name: "周末去哪玩｜只推一个"' in openai_yaml, "Public display name mismatch")
    assert_true("$weekend-pick-one" in openai_yaml, "Default prompt must mention the skill")
    marker = 'short_description: "'
    start = openai_yaml.find(marker)
    assert_true(start >= 0, "agents/openai.yaml missing short_description")
    start += len(marker)
    end = openai_yaml.find('"', start)
    short_description = openai_yaml[start:end]
    assert_true(25 <= len(short_description) <= 64, "short_description length must be 25-64 characters")

    schema = json.loads((ROOT / "schemas/escape-plan.schema.json").read_text(encoding="utf-8"))
    assert_true(schema["title"] == "WeekendPickOnePlan", "Unexpected schema title")
    assert_true(schema["required"] == ["mode"], "Schema top-level required should only contain mode")
    assert_true("oneOf" in schema, "Schema must separate cold start, skill selection, and outing decisions")
    assert_true(schema["properties"]["backup_plans"]["maxItems"] == 2, "Keep backups capped at 2")
    modes = schema["properties"]["mode"]["enum"]
    assert_true("skill_selection" in modes, "Schema mode enum must include skill_selection")
    branch_titles = {branch.get("title") for branch in schema["oneOf"]}
    assert_true({"ColdStart", "SkillSelection", "OutingDecision"} <= branch_titles, "Schema branches are incomplete")
    for field in ["decision_context", "evidence", "profile_snapshot", "candidate_pool_summary", "source_status", "memory_status"]:
        assert_true(field in schema["properties"], f"Schema must define {field}")
    assert_true("startup_question" in schema["properties"], "Schema must define startup_question")
    assert_true("skill_selection" in schema["properties"], "Schema must define skill_selection output")
    schema_text = json.dumps(schema, ensure_ascii=False)
    assert_true('"const": "cold_start"' in schema_text, "Schema must special-case cold_start")
    assert_true('"const": "skill_selection"' in schema_text, "Schema must special-case skill_selection")
    outing_branch = next(branch for branch in schema["oneOf"] if branch.get("title") == "OutingDecision")
    for field in ["recommendation_level", "decision_context", "evidence", "memory_status"]:
        assert_true(field in outing_branch["required"], f"OutingDecision must require {field}")
    assert_true("share_card" not in outing_branch["required"], "Share card should remain optional")
    name_rule = schema["properties"]["main_plan"]["properties"]["name"]
    assert_true("not" in name_rule and "pattern" in name_rule["not"], "Named main plan must reject option strings")

    safety = (ROOT / "references/safety.md").read_text(encoding="utf-8")
    blocked_actions = ["自动登录", "绕过验证码", "批量采集", "下载图片", "保存博主"]
    for action in blocked_actions:
        assert_true(action in safety, f"Safety file missing blocked action: {action}")

    cold_start = (ROOT / "references/cold-start.md").read_text(encoding="utf-8")
    assert_true("不得从示例" in cold_start, "Cold start must block sample-city inference")
    assert_true("首次启动问题" in cold_start, "Cold start needs first-launch question")
    assert_true("你一般从哪儿出发" in cold_start, "Cold start must ask departure city")
    assert_true("单程最多愿意折腾多久" in cold_start, "Cold start must ask distance tolerance")

    preference_memory = (ROOT / "references/preference-memory.md").read_text(encoding="utf-8")
    assert_true("记住 / 只这次 / 别记" in preference_memory, "Preference memory needs explicit consent choices")
    assert_true("home_base" in preference_memory, "Preference memory needs home_base")

    low_decision = (ROOT / "references/low-decision-mode.md").read_text(encoding="utf-8")
    assert_true("近场" in low_decision and "城市内" in low_decision and "周边" in low_decision, "Low decision mode must cover three distance bands")
    assert_true("不表示距离短" in low_decision, "Low decision mode must not infer short distance")
    assert_true("Top5 只用于内部打分" in low_decision, "Top5 must stay internal")
    assert_true("travel_scope" in low_decision, "Low decision mode must split travel_scope from decision_load")

    regional = (ROOT / "references/regional-trip-policy.md").read_text(encoding="utf-8")
    for gate in ["返程", "天气", "交通", "同行人", "退路"]:
        assert_true(gate in regional, f"Regional policy missing gate: {gate}")

    live_browser = (ROOT / "references/live-browser-test-protocol.md").read_text(encoding="utf-8")
    assert_true("小红书受限" in live_browser, "Live browser protocol must cover xhs fallback")
    assert_true("候选池摘要" in live_browser, "Live browser protocol must require candidate pool summary")

    release_hygiene = (ROOT / "references/release-hygiene.md").read_text(encoding="utf-8")
    assert_true("latest.zip" in release_hygiene, "Release hygiene must cover latest zip")
    assert_true("不得清理其他 Skill" in release_hygiene, "Release hygiene must scope cleanup")

    examples_dir = ROOT / "examples"
    for example in examples_dir.glob("*.md"):
        text = example.read_text(encoding="utf-8")
        assert_true("判了" in text or "方向版" in text, f"{example.name} needs a verdict or directional label")
        assert_true("出门前检查" in text or "要更准" in text, f"{example.name} needs a next-step or check")
        assert_true("主逃跑" not in text, f"{example.name} still uses the retired user-facing term")

    forward_cases = json.loads((ROOT / "tests/forward-cases.json").read_text(encoding="utf-8"))
    assert_true(len(forward_cases) >= 16, "Need at least 16 fixture cases")
    case_ids = [case["id"] for case in forward_cases]
    assert_true(len(case_ids) == len(set(case_ids)), "Forward case IDs must be unique")
    assert_true(any(case.get("browser_state") == "login_required" for case in forward_cases), "Need browser-limited case")
    assert_true(any(case["mode"] == "anti_filter" for case in forward_cases), "Need anti-filter case")
    assert_true(any(case["mode"] == "cold_start" for case in forward_cases), "Need cold-start case")
    assert_true(any(case["mode"] == "low_decision" for case in forward_cases), "Need low-decision case")
    assert_true(any(case["mode"] == "skill_selection" for case in forward_cases), "Need skill-selection case")
    assert_true(any(case["id"] == "relative-weekend-exact-date-directional" for case in forward_cases), "Need relative-date case")
    assert_true(any(case["id"] == "memory-unavailable-session-only" for case in forward_cases), "Need memory capability case")
    assert_true(any("required_any" in case for case in forward_cases), "Need at least one flexible assertion group")

    agent_cases = json.loads((ROOT / "tests/agent-eval-cases.json").read_text(encoding="utf-8"))
    assert_true(len(agent_cases) >= 4, "Need at least 4 independent agent cases")
    agent_ids = [case["id"] for case in agent_cases]
    assert_true(len(agent_ids) == len(set(agent_ids)), "Agent case IDs must be unique")
    assert_true(any(case.get("require_specific_main_line") for case in agent_cases), "Agent eval needs a named-main-plan case")
    assert_true(any(case.get("must_start_with") == "方向版" for case in agent_cases), "Agent eval needs a directional case")

    user_facing_files = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")), *sorted((ROOT / "examples").glob("*.md"))]
    retired = [str(path.relative_to(ROOT)) for path in user_facing_files if "主逃跑" in path.read_text(encoding="utf-8")]
    assert_true(not retired, f"Retired user-facing term remains in: {retired}")

    print("weekend-pick-one validation passed")


if __name__ == "__main__":
    main()
