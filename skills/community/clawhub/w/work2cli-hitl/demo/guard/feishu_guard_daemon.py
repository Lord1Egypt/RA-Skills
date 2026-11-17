#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu_guard_daemon.py — 全局飞书写守卫单例守护进程（参考实现骨架）。

设计规范：../../references/write-guard-hitl.md §2.5
部署形态：全机一个实例，服务所有系统的所有 CLI。

职责（也只做这三件事，不懂任何业务）：
  1. 独占持有 lark-cli 的 card.action.trigger 事件总线（常驻循环），
     把按钮回调解析成决定，写到 spool/decisions/<tool>/<hash8>.json
  2. 监听 spool/results/<tool>/<hash8>.json（CLI 写回的执行结果），
     用回调 token 把卡片原位刷新成「执行结果」终态（预算按成功 1 次设计）
  3. 单例保障：pid 文件 + flock，双开互斥

约定（与守卫客户端 _guard_client.py 严格对应）：
  SPOOL_ROOT = ~/.config/work-cli-hitl-guard
  ├── daemon.pid / daemon.lock
  ├── inflight/<tool>/<hash8>.json     # 审批发起时由客户端登记（卡片 message_id/chat_id）
  ├── decisions/<tool>/<hash8>.json    # 本进程写：{"decision","operator_open_id","message_id","time"}
  ├── results/<tool>/<hash8>.json      # 客户端写：{"ok","exit_code","output_tail","card_message_id","chat_id"}
  └── audit.jsonl                      # 所有工具共用，按 tool 字段区分

运行：python3 feishu_guard_daemon.py [--once]   # --once 供测试跑一轮即退
依赖：lark-cli 已登录（全局守卫默认 profile，或环境变量 GUARD_LARK_PROFILE）
"""

import argparse
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SPOOL_ROOT = Path.home() / ".config" / "work-cli-hitl-guard"
PID_FILE = SPOOL_ROOT / "daemon.pid"
LOCK_FILE = SPOOL_ROOT / "daemon.lock"
INFLIGHT_DIR = SPOOL_ROOT / "inflight"
DECISIONS_DIR = SPOOL_ROOT / "decisions"
RESULTS_DIR = SPOOL_ROOT / "results"
AUDIT_FILE = SPOOL_ROOT / "audit.jsonl"

CONSUME_INTERVAL = 30      # event consume 单次阻塞时长（秒），循环无缝衔接
RESULT_POLL_INTERVAL = 5   # results 目录扫描间隔（秒）
CARD_REFRESH_BUDGET = 1    # ⭐ 实测回调 token 只能成功刷一次卡片（第二次报 300040）


def ensure_dirs():
    for d in (INFLIGHT_DIR, DECISIONS_DIR, RESULTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def acquire_single_instance() -> int:
    """文件锁保证全局单例。返回锁 fd（保持持有直到进程退出）。"""
    SPOOL_ROOT.mkdir(parents=True, exist_ok=True)
    fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another guard daemon is already running", file=sys.stderr)
        raise SystemExit(0)
    os.write(fd, str(os.getpid()).encode())
    return fd


def lark(*args: str, timeout: int = 35) -> dict:
    """lark-cli 唯一出口之一（守护进程侧）。返回解析后的 JSON，失败抛异常。"""
    profile = os.environ.get("GUARD_LARK_PROFILE", "").strip()
    argv = ["lark-cli"]
    if profile:
        argv += ["--profile", profile]
    argv += list(args)
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"lark-cli failed: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout)


def audit(tool: str, op: str, hash8: str, result: str, **extra):
    row = {"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "tool": tool,
           "op": op, "hash": hash8, "result": result, **extra}
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_decision(tool: str, hash8: str, decision: str, operator: str, message_id: str):
    """决定落 spool（领取即 consumed 的语义由客户端负责：读后删除/标记）。"""
    out = DECISIONS_DIR / tool / f"{hash8}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "hash": hash8, "decision": decision, "operator_open_id": operator,
        "message_id": message_id, "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }, ensure_ascii=False), encoding="utf-8")


def consume_events_once() -> int:
    """消费一轮按钮回调。返回处理条数。任何 lark-cli 失败不退出循环（fail-closed 由客户端侧兜底）。"""
    data = lark("event", "consume", "card.action.trigger", "--as", "bot",
                "--timeout", f"{CONSUME_INTERVAL}s", "--quiet")
    events = data if isinstance(data, list) else [data]
    handled = 0
    for ev in events:
        hash8 = ((ev.get("action_value") or {}).get("hash") or "").strip()
        operator = (ev.get("operator_id") or "").strip()
        message_id = (ev.get("message_id") or "").strip()
        action = ((ev.get("action_value") or {}).get("action") or "approve").strip()
        if not (hash8 and operator and message_id):
            continue  # 三要素不全，无法归属，忽略
        decision = "rejected" if action == "reject" else "approved"
        owner_tool = find_inflight_owner(hash8)
        if owner_tool is None:
            continue  # 不在 inflight 登记里（过期/别应用的卡片），忽略
        # ⭐ 幂等：同一卡片同哈希的重复回调（用户手抖点两次）以第一点击为准
        dec_file = DECISIONS_DIR / owner_tool / f"{hash8}.json"
        if dec_file.exists():
            continue
        write_decision(owner_tool, hash8, decision, operator, message_id)
        audit(owner_tool, "-", hash8, f"button_{decision}")
        handled += 1
    return handled


def find_inflight_owner(hash8: str):
    """在 inflight/ 里反查哈希归属的工具。"""
    if not INFLIGHT_DIR.exists():
        return None
    for tool_dir in INFLIGHT_DIR.iterdir():
        if (tool_dir / f"{hash8}.json").exists():
            return tool_dir.name
    return None


def pump_results_once() -> int:
    """扫描 results/，把执行结果原位刷到卡片上。预算按成功 1 次设计。"""
    handled = 0
    for result_file in sorted(RESULTS_DIR.glob("*/*.json")):
        try:
            payload = json.loads(result_file.read_text(encoding="utf-8"))
        except Exception:
            continue  # 半写文件（客户端原子写用 tmp+rename，这里容忍脏读）
        tool, hash8 = result_file.parent.name, result_file.stem
        inflight = json.loads((INFLIGHT_DIR / tool / f"{hash8}.json").read_text())
        text = ("✅ 执行成功" if payload.get("ok") else "❌ 执行失败") + \
               f"\nexit={payload.get('exit_code')}\n{payload.get('output_tail', '')[:600]}"
        try:
            lark("im", "+card-update", "--as", "bot",
                 "--message-id", inflight["card_message_id"],
                 "--open-ids", inflight["operator_open_id"],
                 "--content", json.dumps({"text": text}, ensure_ascii=False))
            channel = "card"
        except Exception as e:
            # 300040 / 频控 / 网关失败：静默回退文本，不重试
            channel = "text_fallback"
            try:
                lark("im", "+messages-send", "--as", "bot",
                     "--chat-id", inflight["chat_id"], "--text", text)
            except Exception:
                pass
        audit(tool, payload.get("op", "-"), hash8, "result_delivered",
              result_channel=channel, error=str(e) if channel == "text_fallback" else "")
        # 清理：决定、在途、结果三份记录同清（审计已留痕）
        for f in (result_file, DECISIONS_DIR / tool / f"{hash8}.json",
                  INFLIGHT_DIR / tool / f"{hash8}.json"):
            f.unlink(missing_ok=True)
        handled += 1
    return handled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="各跑一轮即退出（测试用）")
    args = ap.parse_args()

    lock_fd = acquire_single_instance()
    ensure_dirs()
    PID_FILE.write_text(str(os.getpid()))
    print(f"guard daemon started, pid={os.getpid()}, spool={SPOOL_ROOT}", flush=True)

    try:
        while True:
            # 两个循环合在一个主循环里：consume 阻塞 ≤30s，天然给 results 留出节奏
            try:
                consume_events_once()
            except Exception as e:
                print(f"consume error (will retry): {e}", file=sys.stderr)
            try:
                pump_results_once()
            except Exception as e:
                print(f"result pump error (will retry): {e}", file=sys.stderr)
            if args.once:
                break
    except KeyboardInterrupt:
        pass
    finally:
        PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
