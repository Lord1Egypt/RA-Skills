# -*- coding: utf-8 -*-
"""
把 novels/书名/ 下的章节 MD 导出为番茄作家后台可粘贴的纯文本。

源自 AI小说/tools/export_fanqie.py，适配本 skill 落盘结构。

用法：
  python scripts/export_fanqie.py --src novels/我的书名
  python scripts/export_fanqie.py --src novels/我的书名 --out novels/我的书名/番茄导出 --as-chapter

输出：
  …/番茄导出/
    001_第1章_xxx.txt
    目录.txt
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SKIP_NAME_PREFIXES = ("00-", "01-", "02-", "03-", "000-")
SKIP_EXACT = {"readme.md"}
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
MIN_CHARS = 1000


def strip_md(text: str) -> tuple[str, str]:
    title = ""
    m = TITLE_RE.search(text)
    if m:
        title = m.group(1).strip()
        text = text[: m.start()] + text[m.end() :]

    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.M)
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^---+\s*$", "", text, flags=re.M)
    text = re.sub(r"^\*\*\*+\s*$", "", text, flags=re.M)
    text = re.sub(r"^>\s?", "", text, flags=re.M)
    # HTML 注释（skill 章末提示）
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = text.replace("「", "“").replace("」", "”")
    text = text.replace("『", "“").replace("』", "”")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return title, text.strip() + "\n"


def platform_title(raw: str, as_chapter: bool) -> str:
    t = raw
    if as_chapter:
        t = re.sub(r"第(\d+)张", r"第\1章", t)
        if t.startswith("第") and "张" in t[:8]:
            t = t.replace("张 ", "章 ", 1)
    return t.strip()


def safe_filename(seq: int, title: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", title)
    name = re.sub(r"\s+", "_", name)
    return f"{seq:03d}_{name}.txt"


def collect_chapters(src: Path) -> list[Path]:
    files: list[Path] = []
    for p in sorted(src.glob("*.md")):
        low = p.name.lower()
        if low in SKIP_EXACT:
            continue
        if p.name.startswith(SKIP_NAME_PREFIXES):
            continue
        # 兼容 第01章 / 001章
        if p.name.startswith("第") or re.match(r"^\d{3}章", p.name):
            files.append(p)
    return files


def main() -> None:
    here = Path(__file__).resolve().parent
    skill_root = here.parent
    ap = argparse.ArgumentParser(description="导出番茄可粘贴纯文本（skill 版）")
    ap.add_argument(
        "--src",
        type=Path,
        required=True,
        help="章节目录，如 novels/书名",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="输出目录，默认 src/番茄导出",
    )
    ap.add_argument(
        "--as-chapter",
        action="store_true",
        help="「第N张」改为「第N章」",
    )
    ap.add_argument(
        "--min-chars",
        type=int,
        default=MIN_CHARS,
        help=f"字数预警阈值，默认 {MIN_CHARS}",
    )
    args = ap.parse_args()

    src = args.src if args.src.is_absolute() else (Path.cwd() / args.src)
    if not src.is_dir():
        # 再试相对 skill 根
        alt = skill_root / args.src
        src = alt if alt.is_dir() else src
    if not src.is_dir():
        raise SystemExit(f"找不到目录: {args.src}")

    out = args.out or (src / "番茄导出")
    if not out.is_absolute():
        out = Path.cwd() / out

    chapters = collect_chapters(src)
    if not chapters:
        raise SystemExit(f"未找到章节 md（第*.md 或 001章*.md）: {src}")

    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.txt"):
        if old.name != "目录.txt":
            old.unlink()

    index_lines = ["# 番茄上传目录（章节名复制到后台「章节标题」）", ""]
    short: list[str] = []
    for i, path in enumerate(chapters, start=1):
        raw = path.read_text(encoding="utf-8")
        title, body = strip_md(raw)
        if not title:
            title = path.stem
        char_count = len(re.sub(r"\s+", "", body))
        if char_count < args.min_chars:
            short.append(f"{path.name}: {char_count}字（不足{args.min_chars}）")
        plat = platform_title(title, args.as_chapter)
        fname = safe_filename(i, plat)
        (out / fname).write_text(body, encoding="utf-8")
        index_lines.append(f"{i:03d}\t{plat}\t← 文件 {fname}\t{char_count}字")

    (out / "目录.txt").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"已导出 {len(chapters)} 章 → {out}")
    if short:
        print(f"\n[!] 以下章节不足 {args.min_chars} 字，建议补完再上传：")
        for line in short:
            print(f"  - {line}")
    print("用法：打开 .txt 全选复制 → 番茄作家「章节正文」；标题用 目录.txt。")


if __name__ == "__main__":
    main()
