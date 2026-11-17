#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_guard_client.py — 全局守卫客户端（参考实现骨架）。

设计规范：../../../references/write-guard-hitl.md
部署位置：真实部署时放 <工作区>/cli/_guard/guard_client.py，全机共享一份。
         所有系统的 CLI import 它，绝不各自复制——升级只改这一处。

职责（CLI 侧视角）：
  request_approval(tool, op, target, params)  写命令执行前调用；返回是否获批
  report_result(tool, hash8, op, ok, exit_code, output_tail)
                                              执行完写 results/，卡片刷新交给守护进程
  ensure_daemon()                             按需拉起全局守卫单例（pid + flock）

不做的事（设计红线）：
  - 绝不直接 lark-cli event consume（事件总线归守护进程独占）
  - 绝不自己刷新卡片（token 预算只有 1 次，归守护进程统一花）
  - 任何失败都不放行（fail-closed）
"""

import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SPOOL_ROOT = Path.home() / ".config" / "work-cli-hitl-guard"
INFLIGHT_DIR = SPOOL_ROOT / "inflight"
DECISIONS_DIR = SPOOL_ROOT / "decisions"
RESULTS_DIR = SPOOL_ROOT / "results"
DAEMON_PID = SPOOL_ROOT / "daemon.pid"
DAEMON_LOCK = SPOOL_ROOT / "daemon.lock"
DAEMON_SCRIPT = os.environ.get("GUARD_DAEMON_SCRIPT", "")  # 守护进程脚本绝对路径

APPROVAL_TIMEOUT = 600
POLL_INTERVAL = 5
INFLIGHT_TTL = 1200  # 在途记录寿命（等待上限的 2 倍），过期作废重发


class NotApproved(Exception):
    """未获授权（拒绝/超时/哈希不一致/通道故障）。消息体可 json.dumps 给 stdout 末行。"""


# ─── 哈希与规范化 ─────────────────────────────────────────────

def canonical_params(params: dict) -> str:
    return json.dumps(params, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def param_hash(params: dict) -> str:
    return hashlib.sha256(canonical_params(params).encode("utf-8")).hexdigest()[:8]


# ─── 守护进程单例（按需拉起） ─────────────────────────────────

def daemon_alive() -> bool:
    if not DAEMON_PID.exists():
        return False
    pid = DAEMON_PID.read_text().strip()
    try:
        os.kill(int(pid), 0)
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        return False


def ensure_daemon():
    if daemon_alive():
        return
    if not DAEMON_SCRIPT or not Path(DAEMON_SCRIPT).exists():
        raise NotApproved(json.dumps({"approved": False,
                                      "reason": f"guard daemon not running and GUARD_DAEMON_SCRIPT unset ({DAEMON_PID})"}))
    SPOOL_ROOT.mkdir(parents=True, exist_ok=True)
    subprocess.Popen([sys.executable, DAEMON_SCRIPT],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    deadline = time.time() + 10
    while time.time() < deadline and not daemon_alive():
        time.sleep(0.3)
    if not daemon_alive():
        raise NotApproved(json.dumps({"approved": False, "reason": "guard daemon failed to start"}))


# ─── lark-cli（客户端侧仅用于发卡片/兜底轮询，不碰事件总线与卡片更新） ──

def lark(*args: str, timeout: int = 35) -> dict:
    profile = os.environ.get("GUARD_LARK_PROFILE", "").strip()
    argv = ["lark-cli"]
    if profile:
        argv += ["--profile", profile]
    argv += list(args)
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"lark-cli failed: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout)


def whoami_open_id() -> str:
    return (lark("whoami").get("onBehalfOf") or {}).get("openId", "")


# ─── 审批主流程 ───────────────────────────────────────────────

def request_approval(tool: str, op: str, target: str, params: dict,
                     timeout: int = APPROVAL_TIMEOUT) -> str:
    """阻塞直到批准/拒绝/超时。返回 hash8。未获批抛 NotApproved（调用方 exit 3）。"""
    hash8 = param_hash(params)
    dec_file = DECISIONS_DIR / tool / f"{hash8}.json"
    inflight_file = INFLIGHT_DIR / tool / f"{hash8}.json"

    # ① 在途复用：同参数未决定的老卡片继续用，不重发（坑 B）
    reused = inflight_file.exists() and \
        time.time() - inflight_file.stat().st_mtime < INFLIGHT_TTL and \
        not dec_file.exists()

    # ② 决定已存在且未消费（例如守护进程先收到文本兜底）→ 直接领取
    if dec_file.exists():
        return _consume_decision(tool, hash8, params)

    ensure_daemon()

    if not reused:
        try:
            open_id = whoami_open_id()
            card = lark("im", "+messages-send", "--as", "bot", "--user-id", open_id,
                        "--msg-type", "interactive", "--content", _card_content(
                            tool, op, target, params, hash8))
            d = card.get("data") or {}
            inflight_file.parent.mkdir(parents=True, exist_ok=True)
            inflight_file.write_text(json.dumps({
                "tool": tool, "op": op, "target": target,
                "card_message_id": d.get("message_id", ""),
                "chat_id": d.get("chat_id", ""),
                "operator_open_id": open_id, "created": time.time(),
            }, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            raise NotApproved(json.dumps({"approved": False,
                                          "reason": f"card send failed (fail-closed): {e}"}))

    # ③ 等待：主通道守护进程落盘的决定；兜底通道文本回复轮询。stdout 倒计时不静默。
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            if dec_file.exists():
                return _consume_decision(tool, hash8, params)
            _try_text_fallback(tool, hash8)  # 兜底：轮询会话里的 ok <hash8> / no
            if dec_file.exists():
                return _consume_decision(tool, hash8, params)
            remain = int(deadline - time.time())
            print(f"[write-guard] waiting approval {hash8} ... {remain}s left", flush=True)
            time.sleep(POLL_INTERVAL)
        raise NotApproved(json.dumps({"approved": False, "reason": "timeout"}))
    finally:
        pass  # inflight 清理由守护进程在结果回写后统一做


def _consume_decision(tool: str, hash8: str, params: dict) -> str:
    """领取决定（一次性消费）并校验参数哈希。"""
    dec_file = DECISIONS_DIR / tool / f"{hash8}.json"
    decision = json.loads(dec_file.read_text(encoding="utf-8"))
    dec_file.unlink(missing_ok=True)  # ⭐ 领取即消费：同 hash 第二个等待者拿不到
    if decision.get("decision") != "approved":
        raise NotApproved(json.dumps({"approved": False,
                                      "reason": f"rejected ({decision.get('decision')})"}))
    if param_hash(params) != hash8:  # 批准后重算比对（防批准后参数被改）
        raise NotApproved(json.dumps({"approved": False, "reason": "hash_mismatch"}))
    return hash8


def _try_text_fallback(tool: str, hash8: str):
    """兜底通道：轮询审批卡片所在会话，找请求之后的 ok <hash8> / no 文本回复。"""
    inflight_file = INFLIGHT_DIR / tool / f"{hash8}.json"
    if not inflight_file.exists():
        return
    inflight = json.loads(inflight_file.read_text(encoding="utf-8"))
    chat_id = inflight.get("chat_id")
    if not chat_id:
        return
    try:
        data = lark("im", "+chat-messages-list", "--as", "bot", "--chat-id", chat_id)
        msgs = (data.get("data") or {}).get("items") or []
        req_pos = next((m.get("position") for m in msgs
                        if m.get("message_id") == inflight.get("card_message_id")), None)
        if req_pos is None:
            return
        for m in sorted(msgs, key=lambda x: x.get("position") or 0):
            if (m.get("position") or 0) <= req_pos or m.get("sender_type") != "user" or m.get("deleted"):
                continue
            t = (m.get("text") or "").strip().strip("`'\"").lower()
            if re.fullmatch(r"no", t):
                write_decision_file(tool, hash8, "rejected")
                return
            m_ok = re.fullmatch(r"ok\s+([0-9a-f]{8})", t)
            if m_ok:
                # 哈希不符的 ok 视为无关消息忽略
                if m_ok.group(1) == hash8:
                    write_decision_file(tool, hash8, "approved")
                return
    except Exception:
        pass  # 兜底通道失败不影响主通道


def write_decision_file(tool: str, hash8: str, decision: str):
    out = DECISIONS_DIR / tool / f"{hash8}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"hash": hash8, "decision": decision,
                               "channel": "text_fallback",
                               "time": time.strftime("%Y-%m-%dT%H:%M:%S%z")}),
                   encoding="utf-8")


# ─── 执行结果回写（卡片刷新归守护进程） ───────────────────────

def report_result(tool: str, hash8: str, op: str, ok: bool, exit_code: int,
                  output_tail: str = ""):
    """执行完调用。写 results/，由守护进程统一刷卡片（预算 1 次，见规范 §3）。"""
    inflight_file = INFLIGHT_DIR / tool / f"{hash8}.json"
    if not inflight_file.exists():
        return  # 无在途（如文本兜底路径已清理），结果只进审计
    inflight = json.loads(inflight_file.read_text(encoding="utf-8"))
    out = RESULTS_DIR / tool / f"{hash8}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")  # 原子写，防守护进程读到半文件
    tmp.write_text(json.dumps({
        "tool": tool, "op": op, "hash": hash8, "ok": ok, "exit_code": exit_code,
        "output_tail": output_tail[-600:],
        "card_message_id": inflight.get("card_message_id", ""),
        "chat_id": inflight.get("chat_id", ""),
        "operator_open_id": inflight.get("operator_open_id", ""),
    }, ensure_ascii=False), encoding="utf-8")
    tmp.rename(out)


# ─── 卡片内容 ─────────────────────────────────────────────────

def _card_content(tool: str, op: str, target: str, params: dict, hash8: str) -> str:
    pretty = json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True)[:800]
    return json.dumps({
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": "🔐 [write-guard] 写操作审批"},
                   "template": "orange"},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content":
                f"**工具:** {tool}\n**操作:** {op}\n**目标:** {target}\n"
                f"**参数:**\n{pretty}\n**参数哈希:** {hash8}\n\n"
                f"回复「ok {hash8}」批准；回复「no」拒绝。10 分钟内未回复视为拒绝。"}},
            {"tag": "action", "actions": [
                {"tag": "button", "text": {"tag": "plain_text", "content": "✅ 批准执行"},
                 "type": "primary", "value": {"hash": hash8, "action": "approve"}},
                {"tag": "button", "text": {"tag": "plain_text", "content": "❌ 拒绝"},
                 "type": "danger", "value": {"hash": hash8, "action": "reject"}},
            ]},
        ],
    }, ensure_ascii=False)
