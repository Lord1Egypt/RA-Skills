#!/usr/bin/env python3
"""Check an HTML deck for non-portable or missing local assets."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


CSS_URL_RE = re.compile(r"""url\((?:["']?)([^"')]+)(?:["']?)\)""", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(
    r"""@import\s+(?:url\()?(?:["']?)([^"')\s;]+)""",
    re.IGNORECASE,
)


def parse_srcset(value: str) -> set[str]:
    if value.strip().startswith("data:"):
        return set()
    refs: set[str] = set()
    for candidate in value.split(","):
        ref = candidate.strip().split(maxsplit=1)[0]
        if ref:
            refs.add(ref)
    return refs


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: set[str] = set()
        self.resource_refs: set[str] = set()
        self.css_fragments: list[str] = []
        self._style_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        for attribute, value in attrs:
            if not value:
                continue
            attribute = attribute.lower()
            if attribute in {"src", "poster", "data-source"}:
                self.refs.add(value)
                self.resource_refs.add(value)
            elif attribute == "href":
                self.refs.add(value)
                if tag in {"base", "link"}:
                    self.resource_refs.add(value)
            elif attribute == "srcset":
                candidates = parse_srcset(value)
                self.refs.update(candidates)
                self.resource_refs.update(candidates)
            elif attribute == "style":
                self.css_fragments.append(value)

        if tag == "style":
            self._style_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style" and self._style_depth:
            self._style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self.css_fragments.append(data)

    handle_startendtag = handle_starttag


def is_remote(value: str) -> bool:
    parsed = urlparse(value)
    return value.startswith(("//", "#")) or parsed.scheme.lower() in {
        "blob",
        "data",
        "http",
        "https",
        "javascript",
        "mailto",
        "tel",
    }


def is_absolute_local(value: str) -> bool:
    parsed = urlparse(value)
    if parsed.scheme == "file":
        return True
    return bool(re.match(r"^[a-zA-Z]:[\\/]", value) or value.startswith(("/", "\\")))


def extract_refs(text: str) -> set[str]:
    parser = ReferenceParser()
    parser.feed(text)
    css = "\n".join(parser.css_fragments)
    refs = parser.refs | set(CSS_URL_RE.findall(css)) | set(CSS_IMPORT_RE.findall(css))
    return refs


def extract_resource_refs(text: str) -> set[str]:
    parser = ReferenceParser()
    parser.feed(text)
    css = "\n".join(parser.css_fragments)
    refs = parser.resource_refs | set(CSS_URL_RE.findall(css)) | set(CSS_IMPORT_RE.findall(css))
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Check asset paths in an HTML deck.")
    parser.add_argument("html", type=Path, help="HTML file to inspect.")
    parser.add_argument(
        "--strict-offline",
        action="store_true",
        help="Fail when HTTP or HTTPS assets are present.",
    )
    args = parser.parse_args()

    text = args.html.read_text(encoding="utf-8")
    base = args.html.parent
    refs = extract_refs(text)
    resource_refs = extract_resource_refs(text)
    missing: list[str] = []
    absolute: list[str] = []
    remote: list[str] = []
    remote_links: list[str] = []

    for raw in sorted(refs):
        value = raw.strip()
        if not value or value.startswith("--"):
            continue
        if is_remote(value):
            if value.startswith(("//", "http://", "https://")):
                if raw in resource_refs:
                    remote.append(value)
                else:
                    remote_links.append(value)
            continue
        if is_absolute_local(value):
            absolute.append(value)
            continue
        clean = unquote(value.split("#", 1)[0].split("?", 1)[0])
        if clean and not (base / clean).exists():
            missing.append(value)

    if absolute:
        print("ABSOLUTE_LOCAL_PATHS")
        for item in absolute:
            print(f"  {item}")
    if missing:
        print("MISSING_ASSETS")
        for item in missing:
            print(f"  {item}")
    if remote:
        print("REMOTE_ASSETS")
        for item in remote:
            print(f"  {item}")
    if remote_links:
        print("REMOTE_LINKS")
        for item in remote_links:
            print(f"  {item}")

    if absolute or missing or (args.strict_offline and remote):
        return 1
    print("ASSET_CHECK_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
