#!/usr/bin/env python3
"""Fetch one HTML page and print deterministic on-page SEO evidence as JSON."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


MAX_BYTES = 5 * 1024 * 1024


def attributes(values: list[tuple[str, str | None]]) -> dict[str, str]:
    return {name.lower(): value or "" for name, value in values}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.title_parts: list[str] = []
        self.in_title = False
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str | bool]] = []
        self.headings: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.current_heading: dict[str, object] | None = None
        self.current_anchor: dict[str, object] | None = None
        self.current_jsonld: list[str] | None = None
        self.jsonld_blocks: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        attrs_map = attributes(attrs)
        if tag == "html":
            self.html_lang = attrs_map.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(attrs_map)
        elif tag == "link":
            self.links.append(attrs_map)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.current_heading = {"level": tag, "parts": []}
        elif tag == "img":
            self.images.append(
                {
                    "src": attrs_map.get("src", ""),
                    "alt_present": "alt" in attrs_map,
                    "alt": attrs_map.get("alt", ""),
                    "width": attrs_map.get("width", ""),
                    "height": attrs_map.get("height", ""),
                    "loading": attrs_map.get("loading", ""),
                }
            )
        elif tag == "a":
            self.current_anchor = {
                "href": attrs_map.get("href", ""),
                "rel": attrs_map.get("rel", ""),
                "parts": [],
            }
        elif tag == "script" and attrs_map.get("type", "").lower() == "application/ld+json":
            self.current_jsonld = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.current_heading is not None:
            parts = self.current_heading["parts"]
            assert isinstance(parts, list)
            parts.append(data)
        if self.current_anchor is not None:
            parts = self.current_anchor["parts"]
            assert isinstance(parts, list)
            parts.append(data)
        if self.current_jsonld is not None:
            self.current_jsonld.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif self.current_heading is not None and tag == self.current_heading["level"]:
            parts = self.current_heading["parts"]
            assert isinstance(parts, list)
            self.headings.append(
                {
                    "level": tag,
                    "text": " ".join("".join(parts).split()),
                }
            )
            self.current_heading = None
        elif tag == "a" and self.current_anchor is not None:
            parts = self.current_anchor.pop("parts")
            assert isinstance(parts, list)
            self.current_anchor["text"] = " ".join("".join(parts).split())
            self.anchors.append(
                {key: str(value) for key, value in self.current_anchor.items()}
            )
            self.current_anchor = None
        elif tag == "script" and self.current_jsonld is not None:
            self.jsonld_blocks.append("".join(self.current_jsonld).strip())
            self.current_jsonld = None


def first_meta(parser: PageParser, key: str, value: str) -> str:
    value = value.lower()
    for meta in parser.metas:
        if meta.get(key, "").lower() == value:
            return meta.get("content", "").strip()
    return ""


def link_values(parser: PageParser, relation: str) -> list[dict[str, str]]:
    relation = relation.lower()
    return [
        link
        for link in parser.links
        if relation in link.get("rel", "").lower().split()
    ]


def schema_types(blocks: list[str]) -> tuple[list[str], int]:
    found: list[str] = []
    invalid = 0

    def visit(value: object) -> None:
        if isinstance(value, dict):
            kind = value.get("@type")
            if isinstance(kind, str):
                found.append(kind)
            elif isinstance(kind, list):
                found.extend(item for item in kind if isinstance(item, str))
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for block in blocks:
        if not block:
            continue
        try:
            visit(json.loads(block))
        except json.JSONDecodeError:
            invalid += 1
    return sorted(set(found)), invalid


def warning(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def inspect(url: str, timeout: float) -> dict[str, object]:
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("URL must be an absolute http or https URL")

    request = Request(
        url,
        headers={"User-Agent": "RankizzOnPageInspector/1.0 (+https://www.rankizz.com/docs/skills)"},
    )
    response = None
    try:
        response = urlopen(request, timeout=timeout)
    except HTTPError as error:
        response = error
    except URLError as error:
        raise RuntimeError(f"Request failed: {error.reason}") from error

    assert response is not None
    body = response.read(MAX_BYTES + 1)
    truncated = len(body) > MAX_BYTES
    body = body[:MAX_BYTES]
    charset = response.headers.get_content_charset() or "utf-8"
    html = body.decode(charset, errors="replace")
    parser = PageParser()
    parser.feed(html)

    title = " ".join("".join(parser.title_parts).split())
    description = first_meta(parser, "name", "description")
    robots = first_meta(parser, "name", "robots")
    viewport = first_meta(parser, "name", "viewport")
    canonicals = link_values(parser, "canonical")
    alternates = link_values(parser, "alternate")
    hreflang = [
        {"language": link.get("hreflang", ""), "href": link.get("href", "")}
        for link in alternates
        if link.get("hreflang")
    ]
    h1s = [heading for heading in parser.headings if heading["level"] == "h1"]
    schemas, invalid_schemas = schema_types(parser.jsonld_blocks)
    warnings: list[dict[str, str]] = []

    status = getattr(response, "status", response.getcode())
    final_url = response.geturl()
    content_type = response.headers.get("Content-Type", "")
    if status != 200:
        warnings.append(warning("http_status", f"Final response status is {status}, not 200"))
    if "text/html" not in content_type.lower():
        warnings.append(warning("content_type", f"Response content type is {content_type or 'missing'}"))
    if not title:
        warnings.append(warning("missing_title", "No non-empty title element was found"))
    if not description:
        warnings.append(warning("missing_description", "No non-empty meta description was found"))
    if len(h1s) != 1:
        warnings.append(warning("h1_count", f"Found {len(h1s)} H1 elements; review the main heading"))
    if len(canonicals) != 1:
        warnings.append(warning("canonical_count", f"Found {len(canonicals)} canonical links"))
    if "noindex" in robots.lower() or "noindex" in response.headers.get("X-Robots-Tag", "").lower():
        warnings.append(warning("noindex", "A noindex directive is present"))
    if not viewport:
        warnings.append(warning("missing_viewport", "No viewport meta tag was found"))
    if truncated:
        warnings.append(warning("response_truncated", f"Only the first {MAX_BYTES} response bytes were inspected"))
    if invalid_schemas:
        warnings.append(warning("invalid_jsonld", f"Found {invalid_schemas} JSON-LD blocks that did not parse"))

    images_without_alt = sum(not bool(image["alt_present"]) for image in parser.images)
    images_without_dimensions = sum(
        not image["width"] or not image["height"] for image in parser.images
    )
    if images_without_alt:
        warnings.append(warning("missing_image_alt", f"{images_without_alt} images have no alt attribute"))
    if images_without_dimensions:
        warnings.append(warning("missing_image_dimensions", f"{images_without_dimensions} images lack width or height"))

    open_graph = {
        meta.get("property", ""): meta.get("content", "")
        for meta in parser.metas
        if meta.get("property", "").lower().startswith("og:")
    }
    twitter = {
        meta.get("name", ""): meta.get("content", "")
        for meta in parser.metas
        if meta.get("name", "").lower().startswith("twitter:")
    }

    return {
        "requested_url": url,
        "final_url": final_url,
        "redirected": final_url != url,
        "status": status,
        "content_type": content_type,
        "response_headers": {"x_robots_tag": response.headers.get("X-Robots-Tag", "")},
        "document": {
            "lang": parser.html_lang,
            "title": title,
            "title_characters": len(title),
            "meta_description": description,
            "description_characters": len(description),
            "robots": robots,
            "viewport": viewport,
            "canonicals": canonicals,
            "hreflang": hreflang,
            "headings": parser.headings,
            "images": {
                "count": len(parser.images),
                "without_alt_attribute": images_without_alt,
                "with_empty_alt": sum(image["alt_present"] and not image["alt"] for image in parser.images),
                "without_width_or_height": images_without_dimensions,
                "items": parser.images,
            },
            "open_graph": open_graph,
            "twitter": twitter,
            "jsonld": {"blocks": len(parser.jsonld_blocks), "types": schemas, "invalid_blocks": invalid_schemas},
            "links": {"count": len(parser.anchors), "items": parser.anchors},
        },
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Absolute public or local http(s) URL")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()
    try:
        result = inspect(args.url, args.timeout)
    except (ValueError, RuntimeError) as error:
        raise SystemExit(str(error)) from error
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
