#!/usr/bin/env python3
"""Validate native WPS internal hyperlinks, bookmarks, and DOI links in DOCX."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from zipfile import ZipFile

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS, "r": R_NS, "pr": PKG_REL_NS}


def validate(path: Path) -> bool:
    with ZipFile(path) as archive:
        document = etree.fromstring(archive.read("word/document.xml"))
        relationships = etree.fromstring(archive.read("word/_rels/document.xml.rels"))

    bookmarks = set(document.xpath(".//w:bookmarkStart/@w:name", namespaces=NS))
    field_targets = document.xpath('.//w:hyperlink/@w:anchor', namespaces=NS)
    field_targets = [x for x in field_targets if re.fullmatch(r"ref_\d+", x)]
    malformed = []

    missing = sorted(set(field_targets) - bookmarks)
    reference_bookmarks = sorted(x for x in bookmarks if re.fullmatch(r"ref_\d+", x))
    doi_targets = [
        rel.get("Target", "")
        for rel in relationships.xpath(".//pr:Relationship", namespaces=NS)
        if rel.get("Type", "").endswith("/hyperlink")
        and rel.get("Target", "").lower().startswith("https://doi.org/")
    ]

    print(f"Reference bookmarks: {len(reference_bookmarks)}")
    print(f"WPS internal hyperlink targets: {len(field_targets)}")
    print(f"DOI hyperlinks: {len(doi_targets)}")
    if malformed:
        print("ERROR: malformed local HYPERLINK fields:", file=sys.stderr)
        for item in malformed:
            print(f"  {item}", file=sys.stderr)
    if missing:
        print("ERROR: missing bookmark targets: " + ", ".join(missing), file=sys.stderr)
    if not reference_bookmarks:
        print("ERROR: no reference bookmarks found", file=sys.stderr)
    if not field_targets:
        print("ERROR: no native WPS internal hyperlinks found", file=sys.stderr)
    return bool(reference_bookmarks and field_targets and not malformed and not missing)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    raise SystemExit(0 if validate(args.docx) else 1)


if __name__ == "__main__":
    main()

