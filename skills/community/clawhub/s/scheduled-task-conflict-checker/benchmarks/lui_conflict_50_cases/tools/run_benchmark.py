#!/usr/bin/env python3
"""运行 50 组定时任务冲突检测 benchmark。

清理原则：
- 每个 case 执行前删除 runtime/task_pool.json。
- 只把当前 case 的 initial_tasks 写入 runtime/task_pool.json。
- 调用 checker 时从这个临时任务池读取 existing_tasks。
- 每个 case 执行后再次删除 runtime/task_pool.json。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "fixtures"
RUNTIME_DIR = ROOT / "runtime"
RESULTS_DIR = ROOT / "results"
TASK_POOL = RUNTIME_DIR / "task_pool.json"
TEMP_INPUT = RUNTIME_DIR / "current_input.json"
CHECKER = Path("/Users/wangzhilelelelele/.agents/skills/scheduled-task-conflict-checker/scripts/check_scheduled_task_conflicts.py")


def clear_task_pool() -> None:
    TASK_POOL.unlink(missing_ok=True)
    TEMP_INPUT.unlink(missing_ok=True)


def primary_reason(result: Dict[str, Any]) -> str:
    findings = result.get("findings") or []
    if not findings:
        return "none"
    decision = result.get("decision")
    for item in findings:
        if item.get("decision") == decision:
            return item.get("code") or "none"
    return findings[0].get("code") or "none"


def load_cases() -> List[Path]:
    return sorted(FIXTURES_DIR.glob("case_*/input.json"))


def run_case(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    clear_task_pool()
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    TASK_POOL.write_text(json.dumps(payload.get("initial_tasks", []), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    existing_tasks = json.loads(TASK_POOL.read_text(encoding="utf-8"))
    checker_payload = {
        "proposed_task": payload["proposed_task"],
        "existing_tasks": existing_tasks,
        "user_context": payload["user_context"],
    }
    TEMP_INPUT.write_text(json.dumps(checker_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        completed = subprocess.run(
            [sys.executable, str(CHECKER), str(TEMP_INPUT), "--format", "json"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            return {
                "case_id": payload["case_id"],
                "status": "error",
                "error": completed.stderr,
                "cleanup_after_case": False,
            }
        result = json.loads(completed.stdout)
        reason = primary_reason(result)
        decision_ok = result.get("decision") == payload["expected_decision"]
        reason_ok = reason == payload["expected_reason_code"]
        prompt_ok = bool(result.get("prompt_required")) == bool(payload["expected_prompt_required"])
        return {
            "case_id": payload["case_id"],
            "category": payload["category"],
            "title": payload["title"],
            "status": "pass" if decision_ok and reason_ok and prompt_ok else "fail",
            "expected_decision": payload["expected_decision"],
            "actual_decision": result.get("decision"),
            "expected_reason_code": payload["expected_reason_code"],
            "actual_reason_code": reason,
            "expected_prompt_required": payload["expected_prompt_required"],
            "actual_prompt_required": bool(result.get("prompt_required")),
            "decision_ok": decision_ok,
            "reason_ok": reason_ok,
            "prompt_ok": prompt_ok,
            "findings": result.get("findings", []),
            "user_prompt": result.get("user_prompt", ""),
            "cleanup_after_case": True,
        }
    finally:
        clear_task_pool()


def write_outputs(results: List[Dict[str, Any]]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "total": len(results),
        "passed": sum(1 for item in results if item["status"] == "pass"),
        "failed": sum(1 for item in results if item["status"] == "fail"),
        "errors": sum(1 for item in results if item["status"] == "error"),
        "task_pool_exists_after_run": TASK_POOL.exists(),
        "results": results,
    }
    (RESULTS_DIR / "benchmark_results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 定时任务冲突检测 Benchmark 结果",
        "",
        f"- 总数：{summary['total']}",
        f"- 通过：{summary['passed']}",
        f"- 失败：{summary['failed']}",
        f"- 错误：{summary['errors']}",
        f"- 运行结束后临时任务池是否仍存在：{'是' if summary['task_pool_exists_after_run'] else '否'}",
        "",
        "| Case | 类别 | 结果 | 预期 | 实际 | 原因码 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in results:
        lines.append(
            f"| {item['case_id']} | {item.get('category', '')} | {item['status']} | "
            f"{item.get('expected_decision', '')} | {item.get('actual_decision', '')} | "
            f"{item.get('actual_reason_code', item.get('error', ''))} |"
        )
    (RESULTS_DIR / "benchmark_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 scheduled-task-conflict-checker benchmark")
    parser.add_argument("--case", dest="case_id", help="只运行单个 case，例如 case_001")
    args = parser.parse_args()

    case_paths = load_cases()
    if args.case_id:
        case_paths = [path for path in case_paths if path.parent.name == args.case_id]
        if not case_paths:
            raise SystemExit(f"case not found: {args.case_id}")
    if not case_paths:
        raise SystemExit("no fixtures found; run generate_benchmark.py first")

    results = [run_case(path) for path in case_paths]
    write_outputs(results)
    failed = [item for item in results if item["status"] != "pass"]
    print(json.dumps({
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed_or_error": len(failed),
        "task_pool_exists_after_run": TASK_POOL.exists(),
        "results_json": str(RESULTS_DIR / "benchmark_results.json"),
    }, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
