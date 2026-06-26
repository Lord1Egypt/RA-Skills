#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bench.py
--------
创建 isolated session 对指定 skill 进行性能测试，
无需 Cron，任意时刻可运行。

用法:
    # 基本用法：让 Agent 在新 session 里执行一段任务，测量 token 消耗
    python3 bench.py --label "html-extractor 文章提取" \
        --task "帮我提取这篇文章的内容：https://example.com/article/123" \
        --timeout 120

    # 多次运行求均值
    python3 bench.py --label "enterprise-doc 查接口" \
        --task "查询 live_core 服务的 startLive 接口文档" \
        --runs 3

    # 查看历史基准结果
    python3 bench.py --history
"""

import argparse
import json
import time
import uuid
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────

API_BASE      = "http://localhost:3459"
OPENCLAW_DIR  = Path.home() / ".openclaw"
RESULTS_DIR   = OPENCLAW_DIR / "skills" / "skill-perf" / "results" / "bench"
SESSIONS_PATH = OPENCLAW_DIR / "agents" / "main" / "sessions" / "sessions.json"


# ─────────────────────────────────────────────
# API helpers
# ─────────────────────────────────────────────

def api_call(method: str, path: str, body: dict = None) -> dict:
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def create_session(name: str) -> str:
    """创建新 session，返回 sessionId"""
    session_id = str(uuid.uuid4())
    api_call("POST", "/api/sessions", {
        "sessionId":   session_id,
        "sessionName": name,
        "isComposer":  True,
        "agentMode":   "agent",
    })
    return session_id


def send_task(session_id: str, task: str) -> dict:
    return api_call("POST", f"/api/sessions/{session_id}/tasks", {
        "taskContent": task,
        "agentMode":   "agent",
        "isAskMode":   False,
    })


def get_status(session_id: str) -> dict:
    return api_call("GET", f"/api/sessions/{session_id}/status")


def delete_session(session_id: str):
    try:
        api_call("DELETE", f"/api/sessions/{session_id}")
    except Exception:
        pass


def wait_for_completion(session_id: str, timeout: int = 180, poll: float = 2.0) -> dict:
    """轮询直到任务完成，返回最终 status"""
    start = time.time()
    dots = 0
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            print(f"\n  ⏰ 超时 ({timeout}s)")
            return {"success": False, "error": "timeout"}

        status = get_status(session_id)
        data   = status.get("data", {})
        is_running = data.get("isRunning", True)
        last_say   = data.get("lastMessageSay", "")

        if last_say in ("text", "thinking"):
            print("s", end="", flush=True)
        else:
            print(".", end="", flush=True)
        dots += 1
        if dots % 30 == 0:
            print(f" {int(elapsed)}s", flush=True)

        if not is_running:
            print()
            return status

        time.sleep(poll)


# ─────────────────────────────────────────────
# Token 读取
# ─────────────────────────────────────────────

def read_session_tokens(session_key: str) -> Optional[dict]:
    """从 sessions.json 读取指定 session 的 token 数据"""
    if not SESSIONS_PATH.exists():
        return None
    with open(SESSIONS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    val = data.get(session_key)
    if not val:
        return None
    return {
        "total":  val.get("totalTokens", 0),
        "input":  val.get("inputTokens", 0),
        "output": val.get("outputTokens", 0),
        "model":  val.get("model", ""),
    }


def find_session_key(session_id: str) -> Optional[str]:
    """在 sessions.json 里找包含 session_id 的 key"""
    if not SESSIONS_PATH.exists():
        return None
    with open(SESSIONS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    # 可能是 agent:main:session_id 或其他格式
    for key in data:
        if session_id in key:
            return key
    return None


# ─────────────────────────────────────────────
# 单次 bench run
# ─────────────────────────────────────────────

def run_once(label: str, task: str, timeout: int, keep_session: bool = False) -> dict:
    """
    创建 isolated session → 发送任务 → 等待完成 → 收集 token → 返回结果
    """
    session_name = f"skill-perf: {label[:40]}"
    print(f"\n  创建 isolated session: {session_name}")
    session_id = create_session(session_name)
    print(f"  session_id: {session_id}")

    # 发送任务
    t_start = time.time()
    print(f"  发送任务... ", end="", flush=True)
    send_task(session_id, task)
    # 等待任务真正启动（API 有短暂延迟）
    time.sleep(3)
    print("done")

    # 等待完成
    print(f"  等待完成 (timeout={timeout}s): ", end="", flush=True)
    final_status = wait_for_completion(session_id, timeout=timeout)
    duration = round(time.time() - t_start, 1)

    # 读 token（等一秒让 sessions.json 刷新）
    time.sleep(2)
    session_key = find_session_key(session_id)
    tokens = read_session_tokens(session_key) if session_key else None

    result = {
        "session_id":  session_id,
        "session_key": session_key,
        "duration_sec": duration,
        "completed":   not final_status.get("error"),
        "tokens":      tokens,
    }

    if tokens:
        print(f"  ✅ 完成: {duration}s | tokens: total={tokens['total']:,} input={tokens['input']:,} output={tokens['output']:,}")
    else:
        print(f"  ✅ 完成: {duration}s | tokens: 未找到 (session_key={session_key})")

    if not keep_session:
        delete_session(session_id)

    return result


# ─────────────────────────────────────────────
# 主命令
# ─────────────────────────────────────────────

def cmd_bench(label: str, task: str, runs: int, timeout: int, keep: bool):
    print(f"\n🔬 skill-perf bench")
    print(f"   Label:   {label}")
    print(f"   Task:    {task[:80]}{'...' if len(task) > 80 else ''}")
    print(f"   Runs:    {runs}")

    results = []
    for i in range(runs):
        print(f"\n── Run {i+1}/{runs} ──")
        r = run_once(label, task, timeout, keep_session=keep)
        results.append(r)

    # 汇总
    completed = [r for r in results if r["completed"] and r["tokens"]]
    summary = {
        "label":      label,
        "task":       task,
        "runs":       runs,
        "completed":  len(completed),
        "timestamp":  datetime.now().isoformat(),
        "runs_detail": results,
    }

    if completed:
        totals    = [r["tokens"]["total"]  for r in completed]
        inputs    = [r["tokens"]["input"]  for r in completed]
        outputs   = [r["tokens"]["output"] for r in completed]
        durations = [r["duration_sec"]     for r in completed]

        summary["stats"] = {
            "duration_sec": {"avg": round(sum(durations)/len(durations), 1), "min": min(durations), "max": max(durations)},
            "total_tokens": {"avg": round(sum(totals)/len(totals)),   "min": min(totals),   "max": max(totals)},
            "input_tokens": {"avg": round(sum(inputs)/len(inputs)),   "min": min(inputs),   "max": max(inputs)},
            "output_tokens":{"avg": round(sum(outputs)/len(outputs)), "min": min(outputs),  "max": max(outputs)},
        }

        print(f"\n{'─'*50}")
        print(f"📊 结果汇总: {label}")
        print(f"{'─'*50}")
        s = summary["stats"]
        print(f"  完成率:       {len(completed)}/{runs}")
        print(f"  耗时 (avg):   {s['duration_sec']['avg']}s  [{s['duration_sec']['min']}–{s['duration_sec']['max']}s]")
        print(f"  Total tokens: {s['total_tokens']['avg']:,}  [{s['total_tokens']['min']:,}–{s['total_tokens']['max']:,}]")
        print(f"  Input tokens: {s['input_tokens']['avg']:,}")
        print(f"  Output tokens:{s['output_tokens']['avg']:,}")

    # 保存
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fname = RESULTS_DIR / f"bench_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label[:20].replace(' ', '_')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n  结果已保存: {fname.name}")
    return summary


def cmd_history(limit: int):
    if not RESULTS_DIR.exists():
        print("暂无历史记录")
        return
    files = sorted(RESULTS_DIR.glob("bench_*.json"), reverse=True)[:limit]
    print(f"\n{'Label':<30} {'Runs':>5} {'Avg Total':>12} {'Avg Dur':>10} {'Time'}")
    print("─" * 75)
    for f in files:
        with open(f, encoding="utf-8") as fp:
            d = json.load(fp)
        s = d.get("stats", {})
        avg_tok = s.get("total_tokens", {}).get("avg", "?")
        avg_dur = s.get("duration_sec", {}).get("avg", "?")
        ts = d.get("timestamp", "")[:16]
        print(f"{d.get('label',''):<30} {d.get('runs',0):>5} {str(avg_tok):>12} {str(avg_dur)+'s':>10} {ts}")


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Skill 性能基准测试（isolated session）")
    sub = parser.add_subparsers(dest="cmd")

    # run（默认）
    p_run = sub.add_parser("run", help="运行 bench 测试")
    p_run.add_argument("--label",   "-l", required=True, help="测试标签")
    p_run.add_argument("--task",    "-t", required=True, help="发送给 Agent 的任务内容")
    p_run.add_argument("--runs",    "-n", type=int, default=1, help="运行次数（默认 1）")
    p_run.add_argument("--timeout", type=int, default=180, help="单次超时秒数（默认 180）")
    p_run.add_argument("--keep",    action="store_true", help="保留 session（默认完成后删除）")

    # history
    p_hist = sub.add_parser("history", help="查看历史测试结果")
    p_hist.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.cmd == "history":
        cmd_history(args.limit)
    else:
        # 默认 run
        if args.cmd != "run":
            parser.print_help()
            return
        cmd_bench(args.label, args.task, args.runs, args.timeout, args.keep)


if __name__ == "__main__":
    main()
