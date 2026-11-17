#!/usr/bin/env python3
"""
epub_parser.py — EPUB 解析器
提取書籍 Metadata、章節結構、段落文字
"""

import sys
import json
import argparse
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

# ── EPUB 命名空間 ─────────────────────────────────────────────────────────────
NS = {
    "opf":    "http://www.idpf.org/2007/opf",
    "dc":     "http://purl.org/dc/elements/1.1/",
    "content": "http://www.idpf.org/206/xinc",
    "ncx":    "http://www.daisy.org/z3986/2005/ncx/",
}

def _q(ns: str, tag: str) -> str:
    """快速構造帶命名空間的標籤"""
    return f"{{{NS[ns]}}}{tag}"

def _tag(ns: str, tag: str) -> str:
    return f"{{{NS[ns]}}}{tag}" if ns else tag

# ── 解析 EPUB ────────────────────────────────────────────────────────────────

class EPUBBook:
    def __init__(self, path: str):
        self.path = Path(path)
        self.zip_path = zipfile.Path(self.zip_open(), at="")
        self.metadata: dict = {}
        self.chapters: list[dict] = []  # [{title, content, order}]
        self.cover_image: Optional[bytes] = None

    def zip_open(self) -> zipfile.ZipFile:
        return zipfile.ZipFile(self.path)

    # ── Metadata ─────────────────────────────────────────────────────────────
    def parse_metadata(self) -> dict:
        """從 OPF 檔案解析 Metadata"""
        try:
            # 找 opf 檔案
            opf_path = self._find_opf()
            with self.zip_path.joinpath(opf_path).open() as f:
                tree = ET.parse(f)
            root = tree.getroot()

            meta: dict = {}
            for elem in root.iter():
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                if tag == "metadata":
                    for child in elem:
                        ctag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                        val = (child.text or "").strip()
                        key = f"dc:{ctag}" if ":" in ctag else ctag
                        if val:
                            meta[key] = val
                # 封面
                if tag in ("meta", "opf:meta") and elem.get("name") == "cover":
                    meta["cover_id"] = elem.get("content")
            self.metadata = meta

            # 標題
            if not self.metadata.get("title"):
                self.metadata["title"] = self.path.stem

            return self.metadata

        except Exception as e:
            self.metadata = {"title": self.path.stem, "error": str(e)}
            return self.metadata

    def _find_opf(self) -> str:
        """找 META-INF/container.xml 裏的 OPF 路徑"""
        try:
            with self.zip_path.joinpath("META-INF/container.xml").open() as f:
                tree = ET.parse(f)
            root = tree.getroot()
            # 遍歷所有命名空間
            for elem in root.iter():
                if elem.tag.endswith("}rootfile"):
                    full_path = elem.get("full-path")
                    if full_path:
                        return full_path
        except Exception:
            pass
        # fallback: 找第一個 .opf
        for name in self.zip_path.iterdir():
            if name.suffix == ".opf":
                return name.name
        return "OEBPS/content.opf"

    # ── 章節內容 ──────────────────────────────────────────────────────────────
    def parse_chapters(self) -> list[dict]:
        """解析所有章節"""
        try:
            opf_path_str = self._find_opf()
            opf_dir = str(Path(opf_path_str).parent)
            if opf_dir == ".":
                opf_dir = ""

            with self.zip_path.joinpath(opf_path_str).open() as f:
                tree = ET.parse(f)
            root = tree.getroot()

            # 建立 manifest map: id -> href
            manifest: dict = {}
            for elem in root.iter():
                if elem.tag.endswith("}manifest"):
                    for item in elem:
                        item_id = item.get("id", "")
                        href = item.get("href", "")
                        media_type = item.get("media-type", "")
                        if item_id and href:
                            manifest[item_id] = {"href": href, "type": media_type}

            # spine 順序
            spine_ids: list[str] = []
            for elem in root.iter():
                if elem.tag.endswith("}spine"):
                    for itemref in elem:
                        idref = itemref.get("idref", "")
                        if idref:
                            spine_ids.append(idref)

            # 依 spine 順序解析每個章節
            chapters: list[dict] = []
            for idx, item_id in enumerate(spine_ids):
                item = manifest.get(item_id)
                if not item:
                    continue
                href = item["href"]
                # 處理相對路徑
                if opf_dir:
                    full_href = opf_dir + "/" + href
                else:
                    full_href = href
                full_href = full_href.replace("//", "/")

                try:
                    with self.zip_path.joinpath(full_href).open() as f:
                        content = self._extract_text_from_xhtml(f.read())
                except Exception:
                    continue

                title = self._extract_title_from_xhtml(
                    self.zip_path.joinpath(full_href).read_bytes()
                ) or f"第 {idx + 1} 章"

                if content.strip():
                    chapters.append({
                        "index": idx + 1,
                        "title": title,
                        "content": content,
                        "source": full_href,
                    })

            self.chapters = chapters
            return chapters

        except Exception as e:
            self.chapters = []
            return self.chapters

    def _extract_text_from_xhtml(self, raw: bytes) -> str:
        """從 XHTML 內容萃取純文字"""
        try:
            root = ET.fromstring(raw)
            return self._strip_tags(root)
        except Exception:
            # fallback: 當純文字
            try:
                return raw.decode("utf-8", errors="replace")
            except Exception:
                return ""

    def _strip_tags(self, elem: ET.Element) -> str:
        """遞迴去除所有標籤，保留純文字"""
        parts: list[str] = []
        if elem.text and elem.text.strip():
            parts.append(elem.text.strip())
        for child in elem:
            parts.append(self._strip_tags(child))
            if child.tail and child.tail.strip():
                parts.append(child.tail.strip())
        return "\n".join(p for p in parts if p)

    def _extract_title_from_xhtml(self, raw: bytes) -> Optional[str]:
        """從 XHTML 萃取章節標題"""
        try:
            root = ET.fromstring(raw)
            # 優先找 title 標籤
            for elem in root.iter():
                tag = elem.tag.split("}")[-1]
                if tag in ("title", "h1", "h2"):
                    text = (elem.text or "").strip()
                    if text:
                        return text
            # fallback: body 第一行文字
            for elem in root.iter("body"):
                for child in list(elem)[:3]:
                    tag = child.tag.split("}")[-1]
                    if tag in ("h1", "h2", "p"):
                        text = (child.text or "").strip()
                        if text:
                            return text
        except Exception:
            pass
        return None

    # ── 封面圖 ────────────────────────────────────────────────────────────────
    def extract_cover(self) -> Optional[bytes]:
        """萃取封面圖片"""
        cover_id = self.metadata.get("cover_id")
        if not cover_id:
            return None
        try:
            opf_path_str = self._find_opf()
            opf_dir = str(Path(opf_path_str).parent)
            with self.zip_path.joinpath(opf_path_str).open() as f:
                tree = ET.parse(f)
            root = tree.getroot()
            for elem in root.iter():
                if elem.tag.endswith("}manifest"):
                    for item in elem:
                        if item.get("id") == cover_id:
                            href = item.get("href", "")
                            if opf_dir:
                                full = opf_dir + "/" + href
                            else:
                                full = href
                            full = full.replace("//", "/")
                            return self.zip_path.joinpath(full).read_bytes()
        except Exception:
            pass
        return None

    # ── 完整解析 ──────────────────────────────────────────────────────────────
    def parse(self) -> dict:
        """執行完整解析並回傳結構"""
        self.parse_metadata()
        self.parse_chapters()
        self.cover_image = self.extract_cover()
        return self.to_dict()

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "chapters": self.chapters,
            "has_cover": self.cover_image is not None,
        }

    def summary(self) -> str:
        """產生可讀摘要"""
        lines = [
            f"📖 {self.metadata.get('dc:title', self.metadata.get('title', '未知書名'))}",
            f"👤 作者：{self.metadata.get('dc:creator', self.metadata.get('creator', '未知'))}",
            f"📚 章節：{len(self.chapters)} 章",
        ]
        total_chars = sum(len(c["content"]) for c in self.chapters)
        lines.append(f"📝 總字數：約 {total_chars:,} 字")
        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="EPUB 解析器 — 萃取書籍結構與文字")
    parser.add_argument("file", help="EPUB 檔案路徑")
    parser.add_argument("--output", "-o", help="JSON 輸出路徑（預設印到標準輸出）")
    parser.add_argument("--chapters", action="store_true", help="同時輸出各章節內容")
    args = parser.parse_args()

    book = EPUBBook(args.file)
    result = book.parse()

    # 摘要輸出
    print(book.summary())

    # 決定輸出範圍
    if not args.chapters:
        result["chapters"] = [
            {"index": c["index"], "title": c["title"],
             "source": c["source"], "chars": len(c["content"])}
            for c in result["chapters"]
        ]

    # 輸出
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✅ 已寫入：{args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
