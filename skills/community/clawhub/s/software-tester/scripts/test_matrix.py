#!/usr/bin/env python3
"""Generate a REST/GraphQL API test matrix (normal / boundary / negative / security).

Usage:
    python3 scripts/test_matrix.py --method POST --path /api/login --params username,password
    python3 scripts/test_matrix.py --method GET --path /api/orders/{id} --auth
"""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser(description="Generate an API test matrix Markdown.")
    ap.add_argument("--method", default="GET", help="HTTP method")
    ap.add_argument("--path", required=True, help="endpoint path")
    ap.add_argument("--params", help="comma-separated param names")
    ap.add_argument("--auth", action="store_true", help="endpoint requires auth")
    args = ap.parse_args()

    params = [p.strip() for p in (args.params or "").split(",") if p.strip()]
    plist = ", ".join(params) if params else "(none)"

    rows = []
    # Normal
    rows.append(("正常", "合法参数，期望成功", "200 + 正确结构"))
    # Boundary
    if params:
        rows.append(("边界", f"{params[0]} 为空 / 超长(10k) / 特殊字符", "400 或正确截断"))
        rows.append(("边界", "类型错误（字符串当数字）", "400"))
    else:
        rows.append(("边界", "极限分页 / 大量返回", "200 或 429"))
    # Negative
    rows.append(("异常", "缺必填参数", "400 + 规范错误体"))
    rows.append(("异常", "资源不存在", "404"))
    if args.auth:
        rows.append(("异常", "无 Token", "401"))
        rows.append(("异常", "过期 Token", "401"))
        rows.append(("安全", "越权访问他人资源 (BOLA)", "403"))
        rows.append(("安全", "越权功能 (BFLA)", "403"))
        rows.append(("安全", "高频请求（速率限制）", "429"))
    rows.append(("安全", "注入 payload 作入参", "拦截/转义，不执行"))

    lines = [
        f"# API 测试矩阵：{args.method} {args.path}",
        "",
        f"- 参数：{plist}",
        f"- 需鉴权：{'是' if args.auth else '否'}",
        "",
        "| 类别 | 用例 | 期望结果 |",
        "|------|------|----------|",
    ]
    for cat, case, expect in rows:
        lines.append(f"| {cat} | {case} | {expect} |")
    lines.append("")
    lines.append("> 执行参考 references/api-testing.md 与 references/security-testing.md。")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
