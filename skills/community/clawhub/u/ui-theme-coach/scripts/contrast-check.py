#!/usr/bin/env python3
"""WCAG 2.1 AA 对比度检查：验证两个 hex 颜色的对比度是否达标"""

import re

HEX_RE = re.compile(r"^[0-9a-fA-F]{6}$")


def hex_error(c: str):
    """校验颜色格式，返回中文错误原因；合法返回 None。"""
    if not isinstance(c, str) or not c.startswith("#"):
        return '缺少 "#" 前缀（如 #f0e8d8）'
    body = c[1:]
    if len(body) == 3 and re.fullmatch(r"[0-9a-fA-F]{3}", body):
        return "3 位简写不支持，请写成 6 位完整形式（如 #a8c → #aa88cc）"
    if not HEX_RE.fullmatch(body):
        return '不是 "# + 6 位十六进制" 格式（如 #f0e8d8）'
    return None


def parse_hex(c: str):
    return int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)


def relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c: int) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(hex1: str, hex2: str) -> float:
    r1, g1, b1 = parse_hex(hex1)
    r2, g2, b2 = parse_hex(hex2)
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check(hex1: str, hex2: str, label: str = "text vs bg") -> str:
    ratio = contrast_ratio(hex1, hex2)
    aa_normal = ratio >= 4.5
    aa_large = ratio >= 3.0
    status = "✅" if aa_normal else ("⚠️" if aa_large else "❌")
    return f"{status} {label}: {ratio:.2f}:1 (AA normal: {'pass' if aa_normal else 'FAIL'}, AA large: {'pass' if aa_large else 'FAIL'})"


def usage():
    print("Usage: python3 contrast-check.py <hex1> <hex2> [label]")
    print("  hex 格式：# + 6 位十六进制（3 位简写请展开成 6 位，如 #a8c → #aa88cc）")
    print("Example: python3 contrast-check.py '#f0e8d8' '#17120d' 'chat-text vs bg'")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("错误：需要两个颜色参数（文字色 背景色）。", file=sys.stderr)
        usage()
        sys.exit(2)
    for arg in sys.argv[1:3]:
        err = hex_error(arg)
        if err:
            print(f"非法颜色值 {arg!r}：{err}", file=sys.stderr)
            usage()
            sys.exit(2)
    label = sys.argv[3] if len(sys.argv) > 3 else "text vs bg"
    print(check(sys.argv[1], sys.argv[2], label))
