#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""safety-guardrails: 自主智能体的预执行安全护栏。

能力：
  - 策略引擎：基于 deny/confirm 规则的意图风险分级（low/medium/high/critical）
  - 决策门：ALLOW / CONFIRM / DENY，对 destructive、不可逆、越权、外发动作强制拦截
  - 审计日志：记录每一次决策（action / decision / reason / ts）
  - 置信自检：selftest 覆盖 危险动作拦截 / 中危需确认 / 安全放行 / 审计落盘

用法：
  python guardrails.py --selftest
  python guardrails.py --action "rm -rf /data" --context '{"user_approved":false}'
  python guardrails.py --audit   # 打印当前审计日志
"""
import argparse
import json
import re
import sys
import datetime
import os

# ---------------------------------------------------------------------------
# 风险分级策略
# ---------------------------------------------------------------------------
# DENY：破坏性强、不可逆、越权、外发隐私 —— 默认拒绝，除非显式授权且high_risk_allowed
DENY_PATTERNS = [
    (r"\brm\s+-rf\b", "递归强制删除，不可逆"),
    (r"\brm\s+-r\b\s+/", "删除根/绝对路径目录"),
    (r"\bformat\s+(?:/dev|hkcu|hklm)\b", "格式化存储/注册表"),
    (r"\bdd\s+if=.*of=/dev/", "整盘写入，破坏性强"),
    (r"\bshutdown\b|\breboot\b", "关机/重启影响可用性"),
    (r"\bmkfs\b", "创建文件系统，擦除数据"),
    (r"\bdel\s+/[sqf]\b|\bdel\s+/[sqf]\b", "强制静默删除"),
    (r"\bDELETE\s+FROM\b.*\bWHERE\b", "无 WHERE 的整表删除由 confirm 兜底"),
    (r"\bdrop\s+table\b|\bdrop\s+database\b", "删表/库，数据不可逆"),
    (r"\btruncate\b", "清空表，不可逆"),
    (r"\bgit\s+push\s+--force\b", "强推，可覆盖远端历史"),
    (r"\bgit\s+reset\s+--hard\b", "丢弃工作区改动"),
    (r"\b:\(\)\s*\{.*\}\s*;\s*:\b", "fork 炸弹，耗尽资源"),
    (r"\bcurl\b.*\|\s*(?:bash|sh|python)\b", "下载即执行，供应链风险"),
    (r"\bwget\b.*\|\s*(?:bash|sh|python)\b", "下载即执行，供应链风险"),
]
# CONFIRM：高影响但未必恶意 —— 需用户确认
CONFIRM_PATTERNS = [
    (r"\brm\s+-", "删除文件/目录"),
    (r"\bdelete\b|\bremove\b", "删除操作"),
    (r"\bupdate\b.*\bset\b|\binsert\b|\balter\b", "写库操作"),
    (r"\bsend\b|\bemail\b|\bpost\b.*\bhttp", "对外发送/外发数据"),
    (r"\bchmod\s+777\b", "放宽权限，扩大攻击面"),
    (r"\bsudo\b|\brunas\b", "提权执行"),
    (r"\binstall\b|\bpip\s+install\b|\bnpm\s+install\b", "安装依赖，可能引入恶意包"),
    (r"\bgit\s+checkout\b.*--\s", "丢弃未提交改动"),
    (r"\bkill\b|\bstop\b|\bterminate\b", "终止进程/服务"),
    (r"\bdeploy\b|\bpublish\b|\brelease\b", "上线/发布，影响生产"),
    (r"\btransfer\b|\bpay\b|\bwithdraw\b", "资金转移/支付"),
]
# 外发/隐私红线（即便 confirm 也要求高可见）
EXTERNAL_SEND = [
    (r"\bsend.*(?:email|sms|message)\b", "对外发邮件/短信/消息"),
    (r"\bpost\b.*\bhttp", "向外部 HTTP 端点发布"),
    (r"\bupload\b", "上传数据到外部"),
    (r"\btransfer\b.*\bwallet\b", "钱包转账"),
    (r"\bshare\b.*\bpublic\b", "公开分享"),
]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _match(patterns, text):
    hits = []
    for pat, reason in patterns:
        if re.search(pat, text, re.IGNORECASE):
            hits.append((pat, reason))
    return hits


def classify(action):
    """返回 (level, reasons) — level ∈ low/medium/high/critical"""
    deny = _match(DENY_PATTERNS, action)
    if deny:
        return "critical", [r for _, r in deny]
    confirm = _match(CONFIRM_PATTERNS, action)
    ext = _match(EXTERNAL_SEND, action)
    if ext:
        return "high", [r for _, r in ext] + [r for _, r in confirm]
    if confirm:
        return "medium", [r for _, r in confirm]
    return "low", ["无匹配危险模式"]


def gate(action, context=None):
    """决策门。context 可含 user_approved(bool) / high_risk_allowed(bool)。"""
    context = context or {}
    level, reasons = classify(action)
    ts = now()
    if level == "critical":
        if context.get("high_risk_allowed") and context.get("user_approved"):
            decision = "ALLOW"
            note = "已显式授权的高危操作，放行（仍记录）"
        else:
            decision = "DENY"
            note = "破坏性/不可逆动作，默认拒绝：" + "; ".join(reasons)
    elif level == "medium":
        if context.get("user_approved"):
            decision = "ALLOW"
            note = "已确认，放行"
        else:
            decision = "CONFIRM"
            note = "需要用户确认：" + "; ".join(reasons)
    elif level == "high":
        if context.get("user_approved") and context.get("high_risk_allowed"):
            decision = "ALLOW"
            note = "已确认的外发/越权操作，放行"
        else:
            decision = "CONFIRM"
            note = "高影响外发/敏感操作需显式确认：" + "; ".join(reasons)
    else:
        decision = "ALLOW"
        note = "低风险动作，放行"
    record = {"ts": ts, "action": action, "level": level,
              "decision": decision, "reason": note}
    _audit_append(record)
    return decision, note, record


_AUDIT = []


def _audit_append(rec):
    _AUDIT.append(rec)


def get_audit():
    return list(_AUDIT)


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
def selftest():
    ok = True

    # 1) 危险动作被拦截
    d, n, _ = gate("rm -rf /data/important", {})
    assert d == "DENY", f"期望 DENY，实际 {d}: {n}"
    print("[1] 危险递归删除 -> DENY ✓")

    # 2) 中危需确认（未授权）
    d, n, _ = gate("delete /tmp/cache", {})
    assert d == "CONFIRM", f"期望 CONFIRM，实际 {d}: {n}"
    print("[2] 删除操作未授权 -> CONFIRM ✓")

    # 3) 中危已授权放行
    d, n, _ = gate("delete /tmp/cache", {"user_approved": True})
    assert d == "ALLOW", f"期望 ALLOW，实际 {d}: {n}"
    print("[3] 删除操作已授权 -> ALLOW ✓")

    # 4) 安全动作直接放行
    d, n, _ = gate("read file /etc/hosts", {})
    assert d == "ALLOW", f"期望 ALLOW，实际 {d}: {n}"
    print("[4] 只读动作 -> ALLOW ✓")

    # 5) 强推未经授权必须拦截（绝不无条件 ALLOW）
    d, n, _ = gate("git push --force origin main", {})
    assert d == "DENY", f"force push 无授权应 DENY，实际 {d}: {n}"
    print(f"[5] 强推无授权 -> DENY ✓")

    # 6) 外发高级别
    d, n, _ = gate("upload report to public s3", {})
    assert d in ("CONFIRM", "DENY"), f"外发应至少 CONFIRM，实际 {d}"
    print(f"[6] 外发动作 -> {d} ✓")

    # 7) 审计落盘
    assert len(get_audit()) >= 6, f"审计条目不足：{len(get_audit())}"
    print(f"[7] 审计条目数={len(get_audit())} ✓")

    print("\n✅ safety-guardrails selftest 全部通过")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--action", default=None)
    ap.add_argument("--context", default="{}")
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1
    if args.audit:
        print(json.dumps(get_audit(), ensure_ascii=False, indent=2))
        return 0
    if args.action:
        ctx = json.loads(args.context)
        d, n, _ = gate(args.action, ctx)
        print(json.dumps({"decision": d, "note": n}, ensure_ascii=False))
        return 0
    print("用法: --selftest | --action '...' [--context '{}'] | --audit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
