#!/usr/bin/env python3
"""Create a hash-aligned, deliberately pending Image2 audit manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def images(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        rels = {
            node.attrib["Id"]: node.attrib.get("Target", "")
            for node in relationships.findall("pr:Relationship", NS)
        }
        result = []
        for node in document.findall(".//a:blip", NS):
            rid = node.attrib.get(f"{{{NS['r']}}}embed")
            target = rels.get(rid, "")
            if target.startswith("media/"):
                payload = archive.read("word/" + target)
                result.append({"path": f"{path.name}!/word/{target}", "sha256": hashlib.sha256(payload).hexdigest()})
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chinese_docx", type=Path)
    parser.add_argument("bilingual_docx", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    chinese = images(args.chinese_docx)
    bilingual = images(args.bilingual_docx)
    if not chinese or len(bilingual) != 2 * len(chinese):
        raise SystemExit("expected bilingual images to alternate original+Chinese and total exactly twice the Chinese count")

    figures = []
    for index, translated in enumerate(chinese):
        original = bilingual[index * 2]
        paired = bilingual[index * 2 + 1]
        if paired["sha256"] != translated["sha256"]:
            raise SystemExit(f"figure {index + 1}: bilingual Chinese image differs from Chinese-only image")
        figures.append({
            "figure": index + 1,
            "generator": "Image2",
            "status": "pending_visual_audit",
            "original_path": original["path"],
            "translated_path": translated["path"],
            "original_sha256": original["sha256"],
            "translated_sha256": translated["sha256"],
            "label_audit": {"result": "pending", "items": []},
            "residual_semantic_english": True,
            "clipped": True,
        })
    args.output_json.write_text(json.dumps({"figures": figures}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "pending_visual_audit", "figures": len(figures), "manifest": str(args.output_json)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

