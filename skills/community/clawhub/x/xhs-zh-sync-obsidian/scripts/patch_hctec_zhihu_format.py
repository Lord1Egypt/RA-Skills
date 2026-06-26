#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import DEFAULT_CONFIG_PATH, expand_path, load_config, skill_dir


START = "class _TextExtractor(HTMLParser):"
END = "\n\ndef html_to_text(html: str) -> str:"
MARKER = "# Patched by social-favorites-to-obsidian v2: preserve Zhihu block formatting."

PATCHED_CLASS = rf'''class _TextExtractor(HTMLParser):
    {MARKER}
    BLOCK_TAGS = {{"address", "blockquote", "div", "figure", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "li", "ol", "p", "pre", "section", "table", "tr", "ul"}}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._last_was_space = False

    def _append(self, text: str) -> None:
        if text:
            self.parts.append(text)
            self._last_was_space = text[-1].isspace()

    def _newline(self, count: int = 1) -> None:
        raw = "".join(self.parts).rstrip(" \t")
        raw = re.sub(r"\n{{3,}}$", "\n\n", raw)
        need = "\n" * count
        if not raw.endswith(need):
            raw = raw.rstrip("\n") + need
        self.parts = [raw]
        self._last_was_space = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "br":
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            self._append("- ")
        elif tag in self.BLOCK_TAGS:
            self._newline(2)
        elif tag == "img":
            attrs_map = {{k.lower(): v for k, v in attrs if v}}
            if attrs_map.get("src") or attrs_map.get("data-actualsrc") or attrs_map.get("data-original"):
                if "".join(self.parts).rstrip().endswith("[图片]"):
                    return
                self._newline(1)
                self._append("[图片]")
                self._newline(1)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.BLOCK_TAGS:
            self._newline(2)

    def handle_data(self, data: str) -> None:
        text = re.sub(r"\s+", " ", data or "")
        if not text.strip():
            return
        if self.parts and not self._last_was_space and not text.startswith((" ", "，", "。", "、", "；", "：", "！", "？", ")", "）", "]", "】")):
            self._append(" ")
        self._append(text.strip())

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n{{3,}}", "\n\n", raw)
        return raw.strip()
'''


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    start = text.find(START)
    end = text.find(END)
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError(f"Cannot find _TextExtractor block in {path}")
    updated = text[:start] + PATCHED_CLASS + text[end:]
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch hctec Zhihu formatter to preserve paragraphs and line breaks.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--skills-root", help="Override hctec skills root.")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.skills_root:
        config.setdefault("hctec", {})["skills_root"] = args.skills_root
    target = skill_dir(config, "zhihu_skill") / "scripts" / "zhihu_item_content.py"
    if not target.exists():
        raise SystemExit(f"Missing target file: {target}")
    changed = patch_file(target)
    print(("patched: " if changed else "already patched: ") + str(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
