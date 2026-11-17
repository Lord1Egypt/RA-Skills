#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
order_cli.py — 示例系统 CLI 骨架（配合全局守卫单例）。

这个文件演示「一个系统的 CLI 长什么样」：
  - 读命令直接执行
  - 写命令：--dry-run 预演 → 守卫审批 → 执行 → 结果回写（卡片刷新归守护进程）
  - 外部 API 全部收口在 api() 一个函数里（stub，替换成真实实现即可）

真实部署时放 <工作区>/cli/order-system/order_cli.py，
_guard_client 从 <工作区>/cli/_guard/ 引入（全机共享一份）。

用法示例：
  python3 order_cli.py list --status open
  python3 order_cli.py apply 27127 --status done --note 复核通过 --dry-run
  python3 order_cli.py apply 27127 --status done --note 复核通过
"""

import argparse
import json
import sys
from pathlib import Path

# 真实部署：from _guard.guard_client import ...（全局共享客户端）
sys.path.insert(0, str(Path(__file__).parent))
from _guard_client import (NotApproved, canonical_params, param_hash,  # noqa: E402
                           report_result, request_approval)

TOOL = "order-system"

# exit code 语义（全 CLI 统一）：0 成功 1 参数错 2 认证失败 3 限流/未获授权 4 API 错 5 网络 6 未找到
EXIT_OK, EXIT_USAGE, EXIT_AUTH, EXIT_NOT_APPROVED, EXIT_API, EXIT_NET, EXIT_NOT_FOUND = range(7)


# ─── 传输层（stub：替换成真实系统 API + 认证逻辑） ────────────

def api(method: str, path: str, payload: dict | None = None) -> dict:
    """所有远端调用唯一出口。stub 直接返回演示数据——真实实现要点：
    - token：环境变量 > 本地缓存 > 浏览器登录态，全失败 exit 2 打印手动获取方法
    - 有签名算法的在此复现（逐字节验证过再上线）
    - 401 自动作废缓存重取；429 退避；错误走 stderr JSON 信封
    """
    stub = {
        ("GET", "/orders"): {"data": [
            {"id": 27127, "status": "open", "title": "示例订单A"},
            {"id": 27128, "status": "open", "title": "示例订单B"},
        ], "count": 2},
        ("GET", "/orders/27127"): {"id": 27127, "status": "open", "title": "示例订单A",
                                   "process": [], "logs": []},
    }
    if method == "GET":
        return stub.get(("GET", path), {"error": "not_found"})
    return {"ok": True, "echo": payload}  # POST 等写请求：真实实现在这里发远端


def out_json(obj):
    print(json.dumps(obj, ensure_ascii=False))


def fail(code: int, type_: str, hint: str):
    print(json.dumps({"type": type_, "hint": hint}, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


# ─── 读命令（不拦） ───────────────────────────────────────────

def cmd_list(args):
    out_json(api("GET", "/orders"))


def cmd_detail(args):
    d = api("GET", f"/orders/{args.id}")
    if d.get("error"):
        fail(EXIT_NOT_FOUND, "not_found", f"订单 {args.id} 不存在")
    out_json(d)


# ─── 写命令（必走守卫） ───────────────────────────────────────

def cmd_apply(args):
    params = {"tool": TOOL, "op": "apply", "order_id": args.id,
              "status": args.status, "note": args.note}
    payload = {"order_id": args.id, "status": args.status, "note": args.note}

    # ① dry-run：只打印 payload 和参数哈希，不提交、不审批（守卫不拦 dry-run）
    if args.dry_run:
        out_json({"dry_run": True, "payload": payload,
                  "param_hash": param_hash(params),
                  "result_label": f"订单 {args.id} 状态将置为 {args.status}",
                  "warning": "正式执行需飞书审批（全局守卫单例）"})
        return

    # ② 守卫审批：未获批 → exit 3 + stdout 末行 approved:false（fail-closed）
    try:
        hash8 = request_approval(TOOL, "apply", f"订单 {args.id}", params)
    except NotApproved as e:
        print(str(e), flush=True)  # {"approved": false, "reason": "..."}
        sys.exit(EXIT_NOT_APPROVED)

    # ③ 执行（行为与 exit code 完全不变——审批对成功路径零侵入）
    try:
        result = api("POST", f"/orders/{args.id}/status", payload)
        ok = result.get("ok", False)
        code = EXIT_OK if ok else EXIT_API
    except Exception as e:
        ok, code, result = False, EXIT_NET, {"error": str(e)}

    # ④ 结果回写：写 spool 由守护进程统一刷卡片（预算 1 次，见规范 §3）
    report_result(TOOL, hash8, "apply", ok, code,
                  output_tail=json.dumps(result, ensure_ascii=False))
    out_json({"applied": ok, "verified_status": args.status if ok else None})
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(prog="order_cli")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="订单列表")
    p.add_argument("--status")
    p.add_argument("--format", default="json", choices=["json", "table"])
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("detail", help="订单详情")
    p.add_argument("id")
    p.set_defaults(fn=cmd_detail)

    p = sub.add_parser("apply", help="变更订单状态（写操作，必走守卫）")
    p.add_argument("id")
    p.add_argument("--status", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    if not hasattr(args, "fn"):
        fail(EXIT_USAGE, "usage", "缺少子命令")
    args.fn(args)


if __name__ == "__main__":
    main()
