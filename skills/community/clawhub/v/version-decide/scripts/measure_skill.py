#!/usr/bin/env python3
"""measure_skill.py -- DEV / MAINTENANCE-ONLY tool (not part of the runtime decision flow).

Measures SKILL.md compliance metrics: description length, token estimate, per-section
token budget. Use it before/after editing SKILL.md to confirm the description stays under
the 1536-char cap and the body keeps enough compression headroom.

This script is a documentation-maintenance helper. It is NEVER invoked to answer a
release-decision question; the decision engine is semver_check.py.

Usage:
    python measure_skill.py <path-to-SKILL.md>            # English output (default)
    python measure_skill.py <path-to-SKILL.md> --zh        # Chinese output

Language: English by default (matches the skill's English-default policy); pass --zh for
Chinese output.

（中文：本脚本是开发/维护工具，仅用于量测 SKILL.md 的合规指标，不属于运行期判定流程。
默认英文输出，加 --zh 输出中文。）
"""
import io
import re
import sys

# --------------------------------------------------------------------------
# 双语文案：默认英文（SQP-3），--zh 切中文
# --------------------------------------------------------------------------

_LABELS = {
    "en": {
        "file": "file",
        "desc_len": "description chars",
        "desc_cap": "/ 1536 cap",
        "ok": "OK",
        "over": "!! OVER",
        "when_len": "when_to_use chars",
        "combined": "combined (desc+when)",
        "body_tok": "body token estimate",
        "body_cap": "/ 8000 cap",
        "headroom": "compression headroom (8000 - body)",
        "tok_unit": "tokens",
        "body_lines": "body total lines",
        "budget_head": "sections fitting within the 3000-token budget:",
        "trunc_note": "... (rest truncated; check 'core rules' front-load)",
        "all_head": "all top-level sections:",
    },
    "zh": {
        "file": "文件",
        "desc_len": "description 字符数",
        "desc_cap": "/ 1536 上限",
        "ok": "OK",
        "over": "!! 超限",
        "when_len": "when_to_use 字符数",
        "combined": "两者拼接估算",
        "body_tok": "正文 token 估算",
        "body_cap": "/ 8000 上限",
        "headroom": "压缩余量（8000 - 正文）",
        "tok_unit": "token",
        "body_lines": "正文总行数",
        "budget_head": "3000 token 预算内可容纳的一级小节",
        "trunc_note": "...（其余被截断，见下方'核心规则'是否已前置）",
        "all_head": "全部一级小节",
    },
}


def cjk_ratio(text):
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    return cjk, len(text) - cjk


def est_tokens(text):
    """粗估 token：中文约 1.5 字符/token，ASCII 约 4 字符/token。"""
    cjk, other = cjk_ratio(text)
    return int(cjk / 1.5 + other / 4)


def main():
    args = sys.argv[1:]
    zh = "--zh" in args
    args = [a for a in args if a != "--zh"]
    if not args:
        sys.stderr.write("usage: measure_skill.py <path-to-SKILL.md> [--zh]\n")
        return 2
    path = args[0]
    t = _LABELS["zh" if zh else "en"]
    text = io.open(path, encoding="utf-8").read()
    front = text.split("---", 2)[1] if text.startswith("---") else ""

    def field(name):
        """取标量或块标量字段。块标量（| / >）按缩进收集到下一个非缩进行。"""
        m = re.search(r"^%s:\s*(\|.*|>.*)$" % re.escape(name), front, re.M)
        if m:
            block = re.search(r"^%s:\s*[|>][-+]?\d*$" % re.escape(name), front, re.M)
            if block:
                start = block.end()
                lines, pos = [], start
                rows = front[start:].splitlines()
                for row in rows:
                    if row.strip() and not row.startswith((" ", "\t")):
                        break
                    lines.append(row.strip())
                    pos += len(row) + 1
                return " ".join(x for x in lines if x).strip()
        m2 = re.search(r"^%s:\s*(.+)$" % re.escape(name), front, re.M)
        return m2.group(1).strip() if m2 else ""

    desc = field("description")
    when = field("when_to_use")

    body = text.split("---", 2)[2] if text.startswith("---") else text

    print("%s: %s" % (t["file"], path))
    print("%s: %d %s  %s" % (
        t["desc_len"], len(desc), t["desc_cap"],
        t["ok"] if len(desc) <= 1536 else t["over"]))
    print("%s: %d" % (t["when_len"], len(when)))
    print("%s: %d / 1536  %s" % (
        t["combined"], len(desc) + len(when) + 1,
        t["ok"] if len(desc) + len(when) + 1 <= 1536 else t["over"]))
    print("%s: ~%d %s  %s" % (
        t["body_tok"], est_tokens(body), t["body_cap"],
        t["ok"] if est_tokens(body) <= 8000 else t["over"]))
    print("%s: ~%d %s" % (t["headroom"], 8000 - est_tokens(body), t["tok_unit"]))
    print("%s: %d" % (t["body_lines"], len(body.splitlines())))

    # 前 3000 token 预算内包含哪些一级小节
    lines = body.splitlines()
    acc, heads, cur = 0, [], None
    for ln in lines:
        if ln.startswith("## "):
            cur = ln.strip()
        acc += est_tokens(ln)
        if cur and cur not in heads and acc > 3000:
            break
        if cur and cur not in heads:
            heads.append(cur)
    print("\n--- %s ---" % t["budget_head"])
    for h in heads:
        print("  ", h)
    if heads and len(heads) < len([l for l in lines if l.startswith("## ")]):
        print("   %s" % t["trunc_note"])
    all_h = [l.strip() for l in lines if l.startswith("## ")]
    print("\n%s:" % t["all_head"])
    for h in all_h:
        print("  ", h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
