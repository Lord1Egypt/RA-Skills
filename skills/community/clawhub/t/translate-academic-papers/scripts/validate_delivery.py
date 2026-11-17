#!/usr/bin/env python3
"""Hard-gate validator for the two final academic-paper DOCX deliverables."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect_docx(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        doc_root = ET.fromstring(z.read("word/document.xml"))
        rel_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        rels = {
            el.attrib["Id"]: el.attrib.get("Target", "")
            for el in rel_root.findall("pr:Relationship", NS)
        }
        image_order = []
        for blip in doc_root.findall(".//a:blip", NS):
            rid = blip.attrib.get(f"{{{NS['r']}}}embed")
            target = rels.get(rid, "")
            if target.startswith("media/"):
                data = z.read("word/" + target)
                image_order.append({"target": target, "sha256": sha256(data), "bytes": len(data)})

        anchors = [
            el.attrib.get(f"{{{NS['w']}}}anchor", "")
            for el in doc_root.findall(".//w:hyperlink", NS)
            if el.attrib.get(f"{{{NS['w']}}}anchor")
        ]
        bookmarks = {
            el.attrib.get(f"{{{NS['w']}}}name", "")
            for el in doc_root.findall(".//w:bookmarkStart", NS)
        }
        externals = [
            el.attrib.get("Target", "")
            for el in rel_root.findall("pr:Relationship", NS)
            if el.attrib.get("TargetMode") == "External"
        ]
        text = "".join(doc_root.itertext())
        return {
            "images": image_order,
            "anchors": anchors,
            "bookmarks": bookmarks,
            "externals": externals,
            "text": text,
        }


def fail(errors: list[str], message: str):
    errors.append(message)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chinese_docx", type=Path)
    ap.add_argument("bilingual_docx", type=Path)
    ap.add_argument("image2_manifest", type=Path)
    ap.add_argument("--translation-cache", type=Path)
    args = ap.parse_args()

    errors: list[str] = []
    for path in (args.chinese_docx, args.bilingual_docx, args.image2_manifest):
        if not path.exists() or path.stat().st_size == 0:
            fail(errors, f"missing or empty artifact: {path}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if "_Image2全文中文版" not in args.chinese_docx.stem:
        fail(errors, "Chinese filename must contain _Image2全文中文版")
    if "_Image2逐段中英对照版" not in args.bilingual_docx.stem:
        fail(errors, "Bilingual filename must contain _Image2逐段中英对照版")

    cn = inspect_docx(args.chinese_docx)
    bi = inspect_docx(args.bilingual_docx)
    manifest = json.loads(args.image2_manifest.read_text(encoding="utf-8"))
    pairs = manifest.get("figures", [])

    if not cn["images"]:
        fail(errors, "Chinese document contains no translated figures")
    if len(bi["images"]) != 2 * len(cn["images"]):
        fail(errors, "Bilingual document must contain exactly original+Chinese image pairs")
    if len(pairs) != len(cn["images"]):
        fail(errors, "Image2 manifest count does not match Chinese document image count")

    cn_hashes = [x["sha256"] for x in cn["images"]]
    bi_hashes = [x["sha256"] for x in bi["images"]]
    if len(bi_hashes) == 2 * len(cn_hashes):
        if bi_hashes[1::2] != cn_hashes:
            fail(errors, "Bilingual image order must be original then the exact embedded Chinese Image2 output")
        if any(a == b for a, b in zip(bi_hashes[0::2], bi_hashes[1::2])):
            fail(errors, "At least one English/Chinese image pair is pixel-identical")

    for index, item in enumerate(pairs, 1):
        if item.get("generator", "").lower() not in {"image2", "gpt image 2", "gpt-image-2"}:
            fail(errors, f"figure {index} does not record Image2 as generator")
        if item.get("status") != "accepted":
            fail(errors, f"figure {index} is not accepted")
        audit = item.get("label_audit")
        if not isinstance(audit, dict):
            fail(errors, f"figure {index} has no label-by-label audit")
        elif audit.get("result") != "pass":
            fail(errors, f"figure {index} label audit is not pass")
        for field in ("original_path", "translated_path", "original_sha256", "translated_sha256"):
            if not item.get(field):
                fail(errors, f"figure {index} manifest is missing {field}")
        if item.get("original_sha256") == item.get("translated_sha256"):
            fail(errors, f"figure {index} manifest records identical original/translated hashes")
        if index <= len(cn_hashes) and item.get("translated_sha256") != cn_hashes[index - 1]:
            fail(errors, f"figure {index} translated manifest hash does not match the Chinese DOCX image")
        if 2 * index - 1 <= len(bi_hashes) and item.get("original_sha256") != bi_hashes[2 * index - 2]:
            fail(errors, f"figure {index} original manifest hash does not match the bilingual DOCX image")
        if item.get("residual_semantic_english", True):
            fail(errors, f"figure {index} reports residual semantic English")
        if item.get("clipped", True):
            fail(errors, f"figure {index} reports clipping")

    for label, info in (("Chinese", cn), ("bilingual", bi)):
        missing = sorted(set(info["anchors"]) - info["bookmarks"])
        if missing:
            fail(errors, f"{label} document has missing bookmark targets: {missing[:8]}")
        if not info["anchors"]:
            fail(errors, f"{label} document contains no internal citation hyperlinks")
        if not any(url.lower().startswith("https://doi.org/") for url in info["externals"]):
            fail(errors, f"{label} document contains no external https://doi.org link")

    if args.translation_cache:
        if not args.translation_cache.exists():
            fail(errors, "translation cache is missing")
        else:
            rows = [json.loads(line) for line in args.translation_cache.read_text(encoding="utf-8").splitlines() if line.strip()]
            unverified = [row.get("id", "?") for row in rows if row.get("status") != "ai_verified"]
            if unverified:
                fail(errors, f"translation cache contains non-ai_verified records: {unverified[:12]}")

    if re.search(r"\b(?:TODO|PLACEHOLDER|机器初译|待校订)\b", cn["text"], re.I):
        fail(errors, "Chinese document contains draft/placeholder markers")

    if errors:
        print("DELIVERY VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print(json.dumps({
        "status": "pass",
        "chinese_images": len(cn["images"]),
        "bilingual_images": len(bi["images"]),
        "chinese_internal_links": len(cn["anchors"]),
        "bilingual_internal_links": len(bi["anchors"]),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

