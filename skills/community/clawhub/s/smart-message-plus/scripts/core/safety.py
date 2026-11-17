#!/usr/bin/env python3
"""smart-message-plus: safety gate (headcount tiers) + approval codes.

Tiering (configurable):
  <= warn_threshold          : send directly
  warn < n <= review         : warn, requires --force-send
  > review_threshold         : requires admin approval code (--approve-code)

Approval codes: secrets-generated, TTL-bound, single-use, bound to
(recipients set + message content) hash — changing either invalidates the code.
Admin notification goes through a configured provider (dingtalk/feishu DM).
"""
from __future__ import annotations

import hashlib
import secrets
import time

from . import config as C


class GateWarn(Exception):
    """51-100: needs --force-send."""


class GateReview(Exception):
    """>100: needs approval code."""


def _content_hash(recipients: list[str], msg: str) -> str:
    payload = "|".join(sorted(recipients)) + "\x00" + msg
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def check(
    recipients: list[str],
    msg: str,
    cfg: dict,
    force_send: bool = False,
    approve_code: str = "",
) -> str:
    """Returns tier passed: 'ok' | 'warned' | 'approved'. Raises GateWarn/GateReview."""
    gate = cfg.get("safety_gate", {})
    if not gate.get("enabled", True):
        return "ok"
    n = len(recipients)
    warn_t = int(gate.get("warn_threshold", 50))
    review_t = int(gate.get("review_threshold", 100))
    if n <= warn_t:
        return "ok"
    if n <= review_t:
        if force_send:
            return "warned"
        raise GateWarn(
            f"⚠️ 接收人数 {n} 超过警告线 {warn_t}。确认无误请加 --force-send 重新执行。"
        )
    # review tier
    if approve_code:
        ok, why = _verify_code(approve_code, recipients, msg)
        if ok:
            return "approved"
        raise GateReview(f"🔐 审核码无效: {why}")
    code = _issue_code(recipients, msg, ttl_minutes=int(gate.get("code_ttl_minutes", 30)))
    raise GateReview(
        f"🔐 接收人数 {n} 超过审核线 {review_t}，已生成审核码并通知管理员。\n"
        f"   请从管理员处获取审核码后，附加 --approve-code <码> 重新执行。\n"
        f"   （审核码 {int(cfg.get('safety_gate', {}).get('code_ttl_minutes', 30))} 分钟内有效、"
        f"一次性、绑定本次内容，修改内容后作废）\n"
        f"__PENDING_CODE__:{code}"  # caller strips this & sends to admin
    )


def _issue_code(recipients: list[str], msg: str, ttl_minutes: int = 30) -> str:
    code = f"{secrets.randbelow(900000) + 100000}"
    approvals = C.load_json("approvals.json", {})
    now = time.time()
    # GC expired
    approvals = {
        k: v for k, v in approvals.items() if v.get("expires_at", 0) > now
    }
    approvals[code] = {
        "hash": _content_hash(recipients, msg),
        "expires_at": now + ttl_minutes * 60,
        "count": len(recipients),
    }
    C.save_json("approvals.json", approvals, secret=True)
    return code


def _verify_code(code: str, recipients: list[str], msg: str) -> tuple[bool, str]:
    approvals = C.load_json("approvals.json", {})
    ent = approvals.get(code)
    if not ent:
        return False, "审核码不存在或已使用"
    if ent.get("expires_at", 0) < time.time():
        del approvals[code]
        C.save_json("approvals.json", approvals, secret=True)
        return False, "审核码已过期"
    if ent.get("hash") != _content_hash(recipients, msg):
        return False, "内容或收件人与申请时不一致（审核码绑定内容）"
    del approvals[code]  # single-use
    C.save_json("approvals.json", approvals, secret=True)
    return True, ""
