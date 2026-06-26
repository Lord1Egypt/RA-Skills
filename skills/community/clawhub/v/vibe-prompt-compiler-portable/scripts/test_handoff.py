#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "create_handoff.py"

CASES = [
    {
        "request": "修复登录接口 500",
        "expected_task": "bugfix",
        "expected_mode": "bugfix",
        "required_deliverables": ["Root-cause analysis", "Minimal fix plan"],
        "required_non_goals": ["Do not modify unrelated files or modules."],
    },
    {
        "request": "我们有一套 React + FastAPI + SQLite 的测试系统，想支持两个产品，数据完全隔离但功能一致，怎么设计架构？",
        "expected_task": "architecture-review",
        "expected_mode": "architecture",
        "required_deliverables": ["Recommended architecture", "Phased rollout plan"],
        "required_non_goals": ["Do not recommend a rewrite unless the current system clearly cannot support the requirement."],
    },
    {
        "request": "把我们的系统和企业微信审批打通，审批通过后自动回写状态",
        "expected_task": "integration",
        "expected_mode": "integration",
        "required_deliverables": ["Integration design", "Retry/idempotency rules"],
        "required_non_goals": ["Do not assume third-party reliability without explicit retries and verification."],
    },
    {
        "request": "做一个自动化流程，定时扫描目录里的文件，解析后入库，失败就提醒我",
        "expected_task": "automation-workflow",
        "expected_mode": "workflow",
        "required_deliverables": ["Workflow design", "Execution states"],
        "required_non_goals": ["Do not hide failure handling behind vague automation abstractions."],
    },
]


def handoff(request: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--request", request, "--output", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def contains_all(items: list[str], required: list[str]) -> bool:
    return all(item in items for item in required)


def main():
    failed = 0
    for case in CASES:
        result = handoff(case["request"])
        ok_task = result["task_type"] == case["expected_task"]
        ok_mode = result["execution_mode"] == case["expected_mode"]
        ok_deliverables = contains_all(result.get("deliverables", []), case["required_deliverables"])
        ok_non_goals = contains_all(result.get("non_goals", []), case["required_non_goals"])
        ok_text = all(section in result.get("handoff_text", "") for section in ["Assumptions:", "Non-goals:", "Expected deliverables:", "Execution rules:"])

        ok = ok_task and ok_mode and ok_deliverables and ok_non_goals and ok_text
        print(
            f"{'OK' if ok else 'FAIL'} | "
            f"task={result['task_type']} mode={result['execution_mode']} | {case['request']}"
        )
        if not ok:
            failed += 1
            if not ok_task:
                print(f"  expected task: {case['expected_task']}")
            if not ok_mode:
                print(f"  expected mode: {case['expected_mode']}")
            if not ok_deliverables:
                print(f"  missing deliverables: {case['required_deliverables']}")
            if not ok_non_goals:
                print(f"  missing non-goals: {case['required_non_goals']}")
            if not ok_text:
                print("  handoff_text missing required sections")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
