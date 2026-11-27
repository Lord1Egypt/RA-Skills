# -*- coding: utf-8 -*-
"""一致性扫描：跨篇一致性问题的机器检查（第零道的跨篇扩展）。

用法：
    python consistency_check.py <目录或单篇.md>

覆盖（围栏代码块与行内代码内白名单豁免）：
  A. 文件名 ≠ 文内 H1（"序号_"前缀保留，其余应与 H1 一致）
  B. 跨篇指代词表（上一篇/上一章/前文/后面某章……）
  C. 术语大小写（token→Token；凭证义需人工豁免，报告时带上下文）
  D. 直角引号「」『』正文残留
  E. 提示词引出句后既非围栏块也非行内代码
  F. 中英文之间缺空格

判据来源：《风格手册》与全书一致性修订口径。命中是信号，逐条人工定夺。
"""
import re
import sys
from pathlib import Path

# ---------- 配置 ----------

# B 类：跨篇指代词（命中即报告；同篇内引用如"本章/这篇"不在表内）
CROSS_REF_PATTERNS = [
    r"上一篇", r"上篇", r"之前我们", r"在某一篇", r"某一篇",
    r"上一章", r"下一章", r"前一章", r"后一章", r"前面讲过",
    r"后面.{0,8}章", r"专门的章节", r"单独.{0,4}篇", r"另一篇",
    r"前文(提到|说过)", r"后文(会|将)",
]

# C 类：术语统一（小写→大写；凭证义等例外人工豁免）
TERM_RULES = [
    (r"\btoken\b", "token→Token（若为凭证/口令义则豁免）"),
    (r"\bsubagent\b", "subagent→Subagent"),
    (r"\bmcps?\b(?!erver)", "mcp→MCP"),
]

# E 类：提示词引出句（其后应跟 ```text 围栏块或行内代码）
PROMPT_LEADINS = [
    r"提示词[是为：:]", r"[这支]段提示词", r"直接和 AI 说[：:]", r"对 Agent 说[：:]",
    r"可以对 AI 说[：:]", r"直接对 Agent 说[：:]", r"扔给 AI 一[个条].{0,6}提示词",
]

FENCE_RE = re.compile(r"^(\s*)```")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
CJK = r"\u4e00-\u9fff"
SPACING_RE = re.compile(rf"[{CJK}][A-Za-z]|[A-Za-z][{CJK}]")


def iter_prose_lines(text):
    """产出 (行号, 行文本)，跳过围栏代码块内部；返回 fences 供白名单。"""
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield i, line


def strip_inline_code(line):
    return INLINE_CODE_RE.sub("", line)


def check_file(path: Path, is_dir_mode: bool):
    issues = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # A. H1 与文件名（H1 检测跳过围栏块；前缀形如 03_ / 04_ / 06.1_ / 06.5_）
    h1s = []
    in_fence = False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if not in_fence and ln.startswith("# "):
            h1s.append(ln[2:].strip())
    stem = path.stem
    if len(h1s) == 1:
        m = re.match(r"^\d{2}(\.\d+)?_", stem)
        rest = stem[m.end():] if m else stem
        # H1 以“.md”结尾时文件名会少一个后缀（避免 xxx.md.md），视为一致
        if rest != h1s[0] and not (h1s[0].endswith(".md") and rest + ".md" == h1s[0]):
            issues.append(("A", 1, f"文件名“{rest}”≠ H1“{h1s[0]}”"))
    elif not h1s:
        issues.append(("A", 0, "未找到 H1"))
    else:
        issues.append(("A", 0, f"存在 {len(h1s)} 个 H1"))

    # 逐行正文检查
    for ln, raw in iter_prose_lines(text):
        line = strip_inline_code(raw)
        if not line.strip():
            continue
        for pat in CROSS_REF_PATTERNS:
            for m in re.finditer(pat, line):
                ctx = line.strip()
                issues.append(("B", ln, f"跨篇指代“{m.group(0)}”：{ctx[:60]}"))
                break  # 每行每类报一次
        for pat, label in TERM_RULES:
            if re.search(pat, line):
                issues.append(("C", ln, f"{label}：{line.strip()[:60]}"))
        for ch in "「」『』":
            if ch in line:
                issues.append(("D", ln, f"直角引号 {ch}：{line.strip()[:60]}"))
                break
        for pat in PROMPT_LEADINS:
            m = re.search(pat, line)
            if not m:
                continue
            after = raw[m.end():].strip()
            if INLINE_CODE_RE.search(after):
                break  # 行内代码紧随，合规
            if m.end() >= len(line.rstrip()) - 2:
                # 引出句在行尾 → 下一非空行应是围栏块或行内代码
                nxt = next((lines[k] for k in range(ln, len(lines)) if lines[k].strip()), "")
                if not (FENCE_RE.match(nxt) or nxt.lstrip().startswith("`")):
                    issues.append(("E", ln, f"提示词引出句后非代码块：{line.strip()[:60]}"))
            break
        for m in SPACING_RE.finditer(line):
            issues.append(("F", ln, f"中英文缺空格“{m.group(0)}”：{line.strip()[:60]}"))
            break
    return issues


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/正文")
    files = sorted(target.glob("*.md")) if target.is_dir() else [target]
    total = 0
    for f in files:
        issues = check_file(f, target.is_dir())
        if issues:
            print(f"\n== {f.name} ==")
            for cat, ln, msg in issues:
                print(f"  [{cat}] L{ln} {msg}")
            total += len(issues)
    print(f"\n共 {len(files)} 篇，命中 {total} 条（命中是信号，逐条人工定夺）。")


if __name__ == "__main__":
    main()
