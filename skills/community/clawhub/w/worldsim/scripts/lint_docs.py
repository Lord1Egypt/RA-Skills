#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_docs.py — 规则文档机检（维护期·非运行期）

检查项：
  ① 裸编号    —— `Dn` 跨文件引用未带文件名限定（`Dn` 被 4 个文件共用·裸编号不可判定空间）
  ② 悬空引用  —— `X.md「Y」` 的目标文件不存在，或锚点文本不在目标文件中
  ③ 命令名    —— 解释器写法不一致（`python <脚本>` 应为 `python3`）

只报告、不修改。修复需人工裁定（AGENTS.md §4.5 先审后改）。

用法：
  python3 scripts/lint_docs.py [--skill-dir <目录>] [--json]

退出码：0=无问题；1=有问题；2=用法错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ① `Dn` 的定义文件——在这些文件内部裸 `Dn` 指向自身决策空间，不构成歧义
D_DEFINING_FILES = {
    "phase_dramatist.md",
    "phase_storyliner.md",
    "phase_director.md",
    "actor_decision.md",
}

# 扫描范围与排除
SCAN_DIRS = ("references",)
SCAN_FILES = ("SKILL.md", "README.md")
SKIP_DIR_NAMES = {".git", ".venv", "node_modules", "vendor", "worlds", "tmp", "snaps", "archive"}
# ② 锚点解析的候选目录（引用可能指向 skill 根 / references/ / templates/）
ANCHOR_SEARCH_DIRS = (".", "references", "templates")

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)([^`]*?)\1")
BARE_D_RE = re.compile(r"(?<![A-Za-z0-9_.])(D\d+)(?![0-9])")
REF_RE = re.compile(r"`?([A-Za-z_]+\.md)`?\s*「([^」]+)」")
PY_CMD_RE = re.compile(r"`python\s+(?=[{/\-.])|^python\s+(?=[{/\-.])")
# 定义位豁免：索引表行（| D1 | … |）与节标题（#### D3 …）
INDEX_ROW_RE = re.compile(r"^\s*\|[^|]*\|\s*D\d+\s*\|")
HEADING_RE = re.compile(r"^\s*#{1,6}\s*D\d+\b")


def iter_lines(path: Path):
    """逐行产出 (行号, 原文, 掩码文本, 是否在代码块内)。掩码 = 行内代码内容替换为 x。"""
    text = path.read_text(encoding="utf-8")
    in_fence = False
    fence_char = ""
    for no, raw in enumerate(text.splitlines(), start=1):
        fence = FENCE_RE.match(raw)
        if fence:
            ch = fence.group(1)[0]
            if in_fence and ch == fence_char:
                in_fence = False
                fence_char = ""
            elif not in_fence:
                in_fence = True
                fence_char = ch
            yield no, raw, "", True
            continue
        masked = INLINE_CODE_RE.sub(lambda m: "`" + "x" * len(m.group(2)) + "`", raw)
        yield no, raw, masked, in_fence


def collect_targets(skill_dir: Path) -> list[Path]:
    targets: list[Path] = []
    for name in SCAN_FILES:
        p = skill_dir / name
        if p.exists():
            targets.append(p)
    for d in SCAN_DIRS:
        base = skill_dir / d
        if base.is_dir():
            for md in sorted(base.rglob("*.md")):
                if any(part in SKIP_DIR_NAMES for part in md.parts):
                    continue
                targets.append(md)
    return sorted({t.resolve(): t for t in targets}.values(), key=str)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def resolve_ref(skill_dir: Path, name: str) -> Path | None:
    """把 `X.md` 解析为实际文件路径（依次在 skill 根 / references / templates 下找）。"""
    if any(ch in name for ch in "*?["):
        return None  # 通配路径不检查
    for sub in ANCHOR_SEARCH_DIRS:
        cand = (skill_dir / sub / name) if sub != "." else (skill_dir / name)
        if cand.is_file():
            return cand
    return None


QUALIFIER_TOKEN = r"(?:[A-Za-z_]+\.md|[a-z_]{4,}|[①-⑥](?:戏剧家|编剧|导演|角色|场记|作家)?)"
QUALIFIER_RE = re.compile(QUALIFIER_TOKEN + r"$")
# 邻近窗口只认明确形态（`*.md` 与阶段标记）——裸词在窗口内误命中率太高
QUALIFIER_NEAR_RE = re.compile(r"(?:[A-Za-z_]+\.md|[①-⑥](?:戏剧家|编剧|导演|角色|场记|作家)?)")
SKIP_CHARS = "` \t（(*·"
NEAR_WINDOW = 25


def has_qualifier(raw: str, pos: int) -> bool:
    """判断 pos 处的 Dn 之前是否有定位符。

    接受形式：`phase_director.md D2` / `phase_dramatist D6` / `actor_decision.md D1/D2/D5`
    / `①戏剧家 D7` / `④（D8·…）`——复合组（`D1/D2/D5`）只要组首有定位，整组视为已定位。
    另接受邻近窗口内的 `*.md` 或阶段标记（限定符与编号之间夹中文词的情形）。
    """
    j = pos
    for _ in range(8):  # 最多回退 8 段同组编号
        while j > 0 and raw[j - 1] in SKIP_CHARS:
            j -= 1
        m = re.search(r"[DP]\d+\s*[/–—-]\s*$", raw[:j])
        if not m:
            break
        j = m.start()
    while j > 0 and raw[j - 1] in SKIP_CHARS:
        j -= 1
    if QUALIFIER_RE.search(raw[:j]):
        return True
    return bool(QUALIFIER_NEAR_RE.search(raw[max(0, pos - NEAR_WINDOW):pos]))


def check_bare_number(skill_dir: Path, path: Path) -> list[dict]:
    findings: list[dict] = []
    if path.name in D_DEFINING_FILES:
        return findings
    for no, raw, masked, in_fence in iter_lines(path):
        if in_fence or not masked:
            continue
        if INDEX_ROW_RE.match(raw) or HEADING_RE.match(raw):
            continue
        # 表格行：归属文件常写在相邻单元格——整行出现 `*.md` 即视为已限定（宁缺勿滥）
        table_row = raw.lstrip().startswith("|")
        if table_row and re.search(r"[A-Za-z_]+\.md", raw):
            continue
        for m in BARE_D_RE.finditer(masked):
            if has_qualifier(raw, m.start()):
                continue
            findings.append({
                "kind": "bare-number",
                "file": str(path.relative_to(skill_dir)),
                "line": no,
                "hit": m.group(1),
                "text": raw.strip()[:120],
            })
    return findings


def check_dangling_ref(skill_dir: Path, path: Path) -> list[dict]:
    findings: list[dict] = []
    cache: dict[Path, str] = {}
    for no, raw, masked, in_fence in iter_lines(path):
        if in_fence or not masked:
            continue
        for m in REF_RE.finditer(masked):
            target_name, anchor = m.group(1), m.group(2)
            target = resolve_ref(skill_dir, target_name)
            if target is None:
                findings.append({
                    "kind": "dangling-file",
                    "file": str(path.relative_to(skill_dir)),
                    "line": no,
                    "hit": f"{target_name}「{anchor}」",
                    "text": raw.strip()[:120],
                })
                continue
            if target not in cache:
                cache[target] = read_text(target)
            body = cache[target]
            parts = [p for p in anchor.split("·") if p]
            if all(p in body for p in parts):
                continue
            findings.append({
                "kind": "dangling-anchor",
                "file": str(path.relative_to(skill_dir)),
                "line": no,
                "hit": f"{target_name}「{anchor}」",
                "text": raw.strip()[:120],
            })
    return findings


def check_interpreter(path: Path) -> list[dict]:
    findings: list[dict] = []
    for no, raw, masked, in_fence in iter_lines(path):
        source = raw if in_fence else masked
        if PY_CMD_RE.search(source):
            findings.append({
                "kind": "interpreter",
                "file": str(path),
                "line": no,
                "hit": "python",
                "text": raw.strip()[:120],
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="规则文档机检（维护期）")
    parser.add_argument("--skill-dir", default=None, help="skill 根目录（缺省＝本脚本上一级）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve() if args.skill_dir else Path(__file__).resolve().parent.parent
    if not skill_dir.is_dir():
        print(f"[ERR] skill 根目录不存在: {skill_dir}", file=sys.stderr)
        return 2

    targets = collect_targets(skill_dir)
    if not targets:
        print(f"[ERR] 未找到可检查的 Markdown 文件: {skill_dir}", file=sys.stderr)
        return 2

    findings: list[dict] = []
    for path in targets:
        findings.extend(check_bare_number(skill_dir, path))
        findings.extend(check_dangling_ref(skill_dir, path))
        findings.extend(check_interpreter(path))

    if args.json:
        print(json.dumps({"skill_dir": str(skill_dir), "files": len(targets), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"PASS: 共检查 {len(targets)} 个文件，未发现问题。")
            return 0
        by_kind: dict[str, int] = {}
        for f in findings:
            by_kind[f["kind"]] = by_kind.get(f["kind"], 0) + 1
        for f in findings:
            print(f"- [{f['kind']}] {f['file']}:{f['line']} «{f['hit']}»\n    {f['text']}")
        summary = " ".join(f"{k}={v}" for k, v in sorted(by_kind.items()))
        print(f"\nFAIL: 共检查 {len(targets)} 个文件；{summary}")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
