#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""红线底座 · 可移植检查器（写作专家团技能附带）

对应 references/redlines.md 的「红线 1 中文引号」与「红线 2 HTML 实体」两道关。
扫描时自动跳过 ``` 代码围栏与行内 `code`，避免误报代码示例。
红线 3（字体字形覆盖）依赖具体字体文件，需在各渲染仓库内单独实现，本脚本不覆盖。

用法：
  python redline_check.py <文件或目录> [--fix] [--ext .md .txt]
  --fix   自动把英文直引号替换成中文弯引号（跳过代码围栏与行内 code）
不传参数则扫描当前目录下的 .md / .txt。

退出码：0 = 全通过；1 = 发现违规且未修复；2 = 用法错误。
"""
import os
import re
import sys
import html

CJK = r"\u3400-\u9fff\u3000-\u303f\uff00-\uffef"  # 中日韩 + 中文标点 + 全角
# 英文直引号紧邻 CJK 或落在两段 CJK 之间 → 视为违规
QUOTE_RE = re.compile(r'([' + CJK + r'])"([' + CJK + r'])|([' + CJK + r'])"|"([' + CJK + r'])')
SQUOTE_RE = re.compile(r"([" + CJK + r"])'|'([" + CJK + r"])")
ENTITY_RE = re.compile(r"&(?:#\d+;|#x[0-9a-fA-F]+;|[a-zA-Z]+;)")
INLINE_CODE_RE = re.compile(r"(`[^`]*`)")


def _pairwise_replace(text):
    """把成对英文直引号替换为中文弯引号，单引号同理。"""
    out = []
    d_open, s_open = True, True
    for ch in text:
        if ch == '"':
            out.append("\u201c" if d_open else "\u201d")
            d_open = not d_open
        elif ch == "'":
            out.append("\u2018" if s_open else "\u2019")
            s_open = not s_open
        else:
            out.append(ch)
    return "".join(out)


def _scan_line(text):
    """Scan one line of non-code text, return (double_quote, single_quote, entity) booleans."""
    return (
        bool(QUOTE_RE.search(text)),
        bool(SQUOTE_RE.search(text)),
        bool(ENTITY_RE.search(text)),
    )


def scan_text(text):
    issues = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # 跳过行内 code 区间后扫描剩余文本
        segments = INLINE_CODE_RE.split(line)
        has_dq, has_sq, has_ent = False, False, False
        for idx, seg in enumerate(segments):
            if idx % 2 == 1:
                continue  # 行内 code，跳过
            dq, sq, ent = _scan_line(seg)
            has_dq |= dq
            has_sq |= sq
            has_ent |= ent
        if has_dq:
            issues.append((i, "英文直双引号", line.strip()[:90]))
        if has_sq:
            issues.append((i, "英文直单引号", line.strip()[:90]))
        if has_ent:
            issues.append((i, "HTML 实体", line.strip()[:90]))
    return issues


def fix_text(text):
    out, in_fence = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        # 保护行内 code
        parts = INLINE_CODE_RE.split(line)
        for j, p in enumerate(parts):
            if j % 2 == 1:
                continue
            p = _pairwise_replace(p)
            p = ENTITY_RE.sub(lambda m: html.unescape(m.group(0)), p)
            parts[j] = p
        out.append("".join(parts))
    return "\n".join(out)


def iter_files(paths, exts):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in files:
                    if any(f.endswith(e) for e in exts):
                        yield os.path.join(root, f)
        else:
            yield p


def main():
    args = sys.argv[1:]
    do_fix = False
    paths, exts = [], [".md", ".txt"]
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--fix":
            do_fix = True
        elif a == "--ext":
            i += 1
            exts = args[i].split()
        elif a.startswith("-"):
            print("未知参数:", a)
            return 2
        else:
            paths.append(a)
        i += 1
    if not paths:
        paths = ["."]
    files = list(iter_files(paths, exts))
    if not files:
        print("未找到可扫描文件。")
        return 0

    total, fixed = 0, 0
    for fp in files:
        with open(fp, encoding="utf-8") as fh:
            text = fh.read()
        issues = scan_text(text)
        if not issues:
            continue
        total += len(issues)
        print(f"\n🔴 {fp} 发现 {len(issues)} 处：")
        for ln, kind, snippet in issues:
            print(f"   L{ln} [{kind}] {snippet}")
        if do_fix:
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(fix_text(text))
            fixed += len(issues)
            print(f"   ✅ 已自动修复 {len(issues)} 处")

    if total == 0:
        print("🟢 全部通过：无英文直引号、无 HTML 实体。")
        return 0
    if do_fix:
        print(f"\n🟢 已修复 {fixed} 处，请重新运行不带 --fix 的检查确认归零。")
        return 0
    print(f"\n🔴 共 {total} 处违规，未修复。加 --fix 可自动修复。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
