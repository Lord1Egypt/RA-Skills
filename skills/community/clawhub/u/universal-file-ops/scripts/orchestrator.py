#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrator.py — 统一调度器
支持：单操作调用、批量操作（串行/并行）、dry-run、失败回滚

调用方式：
  1) 列出所有可用操作：
      python orchestrator.py --list

  2) 单操作（直接传递 JSON 到对应脚本）：
      echo '{"action":"create","file":"a.txt","content":"Hello"}' |
        python orchestrator.py --op text_crud

  3) 批量操作（JSON 配置文件）：
      python orchestrator.py --batch batch.json [--parallel] [--stop-on-error]

批量配置 JSON 格式：
  {
    "tasks": [
      {"op": "text_crud", "args": {"action":"create","file":"a.txt","content":"Hello"}},
      {"op": "file_ops",  "args": {"action":"copy", "src":"a.txt","dst":"b.txt"}}
    ],
    "parallel": false,
    "stop_on_error": true
  }

输出（JSON 数组，每项对应该任务结果）：
  [{"success":true,...}, {"success":false,...}]
"""

import argparse
import json
import os
import sys
import subprocess
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 常量 ───────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
OP_MAP = {
    "text_crud":  SCRIPTS_DIR / "text_crud.py",
    "office_crud": SCRIPTS_DIR / "office_crud.py",
    "file_ops":    SCRIPTS_DIR / "file_ops.py",
}
# ── 核心逻辑 ───────────────────────────────────────────────────────────

def run_single_op(op: str, args: Dict[str, Any],
                    timeout: int = 30) -> Dict[str, Any]:
    """调用单个操作脚本，返回标准化结果 dict"""
    script = OP_MAP.get(op)
    if not script or not script.exists():
        return {
            "success": False,
            "op": op,
            "error": f"未知或不支持的操作: {op}",
        }

    # 构造子进程命令
    cmd = [sys.executable, str(script)]
    try:
        proc = subprocess.run(
            cmd,
            input=json.dumps(args, ensure_ascii=False),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = proc.stdout.strip()
        if not output:
            return {
                "success": False,
                "op": op,
                "error": f"脚本无输出（stderr: {proc.stderr[:200]}）",
                "stderr": proc.stderr[:500],
            }
        result = json.loads(output)
        result["_op"] = op   # 注入操作名便于追踪
        return result
    except subprocess.TimeoutExpired:
        return {"success": False, "op": op, "error": f"操作超时（>{timeout}s）"}
    except json.JSONDecodeError as e:
        return {"success": False, "op": op, "error": f"输出 JSON 解析失败: {e}"}
    except Exception as e:
        return {"success": False, "op": op, "error": str(e)}


def run_batch(config: Dict[str, Any],
               parallel: bool = False,
               stop_on_error: bool = True,
               dry_run: bool = False) -> List[Dict[str, Any]]:
    """
    执行批量任务。
    返回结果列表（与 tasks 顺序一致）。
    失败时如 stop_on_error=true 则立即中止并返回已执行结果。
    """
    tasks = config.get("tasks", [])
    if not tasks:
        return [{"success": False, "error": "tasks 为空"}]

    results = []
    rollback_ids = []   # 收集 rollback_id 以便失败时回滚

    if parallel:
        # 并行模式：使用 threading（因脚本是 IO 密集）
        lock = threading.Lock()

        def _worker(task, idx):
            op   = task.get("op")
            args = task.get("args", {})
            if dry_run:
                res = {"success": True, "_dry_run": True, "op": op}
            else:
                res = run_single_op(op, args)
            with lock:
                results.append((idx, res))
                if res.get("success") and res.get("rollback_id"):
                    rollback_ids.append(res["rollback_id"])

        threads = []
        for idx, task in enumerate(tasks):
            t = threading.Thread(target=_worker, args=(task, idx))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        # 按原始顺序排序
        results = [r for _, r in sorted(results, key=lambda x: x[0])]
    else:
        # 串行模式
        for idx, task in enumerate(tasks):
            op   = task.get("op")
            args = task.get("args", {})
            if dry_run:
                res = {"success": True, "_dry_run": True, "op": op}
            else:
                res = run_single_op(op, args)

            results.append(res)
            if res.get("success") and res.get("rollback_id"):
                rollback_ids.append(res["rollback_id"])

            if not res.get("success") and stop_on_error:
                # 失败：追加剩余任务为 skipped
                for skipped_task in tasks[idx+1:]:
                    results.append({
                        "success": False,
                        "op": skipped_task.get("op"),
                        "skipped": True,
                        "reason": "前置任务失败（stop_on_error=true）",
                    })
                break

    # 检查是否有失败需要提示回滚
    failed = [r for r in results if not r.get("success") and not r.get("skipped")]
    if failed and rollback_ids:
        print(
            f"[WARN] 有 {len(failed)} 个任务失败，"
            f"可回滚 {len(rollback_ids)} 个操作："
            f" python rollback.py --ids {','.join(rollback_ids)}",
            file=sys.stderr,
        )

    return results


# ── CLI ────────────────────────────────────────────────────────────────

def list_operations():
    """列出所有可用操作"""
    print("可用操作（op 名称 → 对应脚本）：")
    for op, script in OP_MAP.items():
        exists = "✅" if script.exists() else "❌ (缺失)"
        print(f"  {op:15s} → {script.name}  {exists}")


def parse_args():
    p = argparse.ArgumentParser(
        description="统一调度器：串行/并行执行多文件操作"
    )
    p.add_argument("--list",         action="store_true",
                    help="列出所有可用操作")
    p.add_argument("--op",           choices=list(OP_MAP.keys()),
                    help="单操作名称（配合 stdin JSON 使用）")
    p.add_argument("--batch",        help="批量配置文件路径（JSON）")
    p.add_argument("--parallel",     action="store_true",
                    help="并行执行（默认串行）")
    p.add_argument("--no-stop",      action="store_true",
                    help="失败不中止（继续后续任务）")
    p.add_argument("--dry-run",      action="store_true",
                    help="仅打印计划，不实际执行")
    p.add_argument("--timeout",      type=int, default=30,
                    help="单操作超时秒数（默认 30）")
    return p.parse_args()


def main():
    args = parse_args()

    if args.list:
        list_operations()
        sys.exit(0)

    if args.op:
        # 单操作模式：从 stdin 读取 JSON，直接转发到对应脚本
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print(json.dumps(
                {"success": False, "error": "单操作模式需要从 stdin 传入 JSON"},
                ensure_ascii=False,
            ))
            sys.exit(1)
        script = OP_MAP.get(args.op)
        if not script or not script.exists():
            print(json.dumps(
                {"success": False, "error": f"脚本不存在: {script}"},
                ensure_ascii=False,
            ))
            sys.exit(1)
        cmd = [sys.executable, str(script)]
        proc = subprocess.run(cmd, input=stdin_data, capture_output=True, text=True)
        # 透传脚本输出
        if proc.stdout:
            print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, file=sys.stderr, end="")
        sys.exit(proc.returncode)

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            config = json.load(f)
        results = run_batch(
            config,
            parallel=args.parallel,
            stop_on_error=not args.no_stop,
            dry_run=args.dry_run,
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
        has_failure = any(
            not r.get("success") and not r.get("skipped") for r in results
        )
        sys.exit(1 if has_failure else 0)

    print("错误：需要 --list / --op / --batch 之一。用 -h 查看帮助。")
    sys.exit(1)


if __name__ == "__main__":
    main()
