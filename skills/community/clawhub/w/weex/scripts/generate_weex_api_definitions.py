#!/usr/bin/env python3
"""Regenerate local WEEX REST API definitions from the live V3 docs."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
SITEMAP_URL = "https://www.weex.com/api-doc/sitemap.xml"
DOC_TIMEOUT = 20
MAX_WORKERS = 12

CONTRACT_GROUP_MAP = {
    "Market_API": "market",
    "Account_API": "account",
    "Transaction_API": "transaction",
}

SPOT_GROUP_MAP = {
    "ConfigAPI": "config",
    "MarketDataAPI": "market",
    "AccountAPI": "account",
    "orderApi": "order",
    "rebate-endpoints": "rebate",
}


@dataclass
class ParsedDoc:
    product: str
    key: str
    title: str
    category: str
    method: str
    path: str
    doc_url: str
    requires_auth: bool
    weight_ip: Optional[int]
    weight_uid: Optional[int]
    request_params: List[Dict[str, str]]
    response_params: List[Dict[str, str]]


def fetch_text(url: str) -> str:
    response = requests.get(url, timeout=DOC_TIMEOUT)
    response.raise_for_status()
    return response.text


def load_sitemap_urls() -> List[str]:
    xml_text = fetch_text(SITEMAP_URL)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in root.findall("sm:url/sm:loc", ns) if node.text]
    return urls


def slugify(text: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text.strip())
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return text or "unnamed"


def clean_text(text: str) -> str:
    text = " ".join(text.split())
    text = text.replace("â", "->")
    text = text.replace("→", "->")
    return text


def parse_weight(text: str) -> tuple[Optional[int], Optional[int]]:
    ip = None
    uid = None
    ip_match = re.search(r"Weight\(IP\):\s*(\d+)", text)
    uid_match = re.search(r"Weight\(UID\):\s*(\d+)", text)
    if ip_match:
        ip = int(ip_match.group(1))
    if uid_match:
        uid = int(uid_match.group(1))
    return ip, uid


def get_group(product: str, path_parts: List[str]) -> Optional[str]:
    group_segment = path_parts[2] if len(path_parts) > 2 else ""
    if product == "contract":
        return CONTRACT_GROUP_MAP.get(group_segment)
    return SPOT_GROUP_MAP.get(group_segment)


def extract_table_rows(container: Tag) -> List[Dict[str, str]]:
    table = container.find("table")
    if table is None:
        return []
    rows = table.find_all("tr")
    if not rows:
        return []
    headers = [
        clean_text(cell.get_text(" ", strip=True))
        for cell in rows[0].find_all(["th", "td"])
    ]
    results: List[Dict[str, str]] = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        values = [clean_text(cell.get_text(" ", strip=True)) for cell in cells]
        item: Dict[str, str] = {}
        for idx, header in enumerate(headers):
            key = header.lower().replace("?", "")
            value = values[idx] if idx < len(values) else ""
            if key.startswith("parameter") or key.startswith("name") or key.startswith("field"):
                item["name"] = value
            elif key.startswith("type"):
                item["type"] = value
            elif key.startswith("required"):
                item["required"] = value
            elif key.startswith("description"):
                item["description"] = value
        if item:
            results.append(item)
    return results


def parse_doc(url: str) -> Optional[ParsedDoc]:
    html = fetch_text(url)
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")
    markdown = soup.select_one("article .theme-doc-markdown.markdown")
    if article is None or markdown is None:
        return None

    lines = [line for line in article.get_text("\n", strip=True).splitlines() if line.strip()]
    method = None
    path = None
    for idx, line in enumerate(lines):
        if line in {"GET", "POST", "PUT", "DELETE"} and idx + 1 < len(lines):
            candidate = lines[idx + 1].strip()
            if candidate.startswith("/"):
                method = line
                path = candidate
                break
    if method is None or path is None:
        return None

    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) < 4 or path_parts[0] != "api-doc":
        return None
    product = path_parts[1]
    if product not in {"contract", "spot"}:
        return None
    if "V2" in path_parts or path_parts[1] == "zh-CN":
        return None

    category = get_group(product, path_parts)
    if category is None:
        return None

    title_node = markdown.find("header")
    title = clean_text(title_node.get_text(" ", strip=True)) if title_node else path_parts[-1]

    key = f"{category}.{slugify(path_parts[-1])}"
    if product == "spot":
        key = f"spot.{key}"

    weight_text = clean_text(markdown.get_text(" ", strip=True))
    weight_ip, weight_uid = parse_weight(weight_text)
    requires_auth = "ACCESS-KEY" in clean_text(article.get_text(" ", strip=True))

    wraps = markdown.select(":scope > .api-content-wrap")
    request_params = extract_table_rows(wraps[0]) if len(wraps) >= 1 else []
    response_params = extract_table_rows(wraps[1]) if len(wraps) >= 2 else []

    return ParsedDoc(
        product=product,
        key=key,
        title=title,
        category=category,
        method=method,
        path=path,
        doc_url=url,
        requires_auth=requires_auth,
        weight_ip=weight_ip,
        weight_uid=weight_uid,
        request_params=request_params,
        response_params=response_params,
    )


def iter_doc_urls(product: str, sitemap_urls: Iterable[str]) -> List[str]:
    prefix = f"https://www.weex.com/api-doc/{product}/"
    urls = []
    for url in sitemap_urls:
        if not url.startswith(prefix):
            continue
        if "/V2/" in url or "/zh-CN/" in url:
            continue
        urls.append(url)
    return sorted(set(urls))


def collect_docs(product: str, urls: List[str]) -> List[ParsedDoc]:
    docs: List[ParsedDoc] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {executor.submit(parse_doc, url): url for url in urls}
        for future in as_completed(future_map):
            doc = future.result()
            if doc is not None:
                docs.append(doc)
    docs.sort(key=lambda item: (item.category, item.key))
    return docs


def docs_to_json(product: str, docs: List[ParsedDoc]) -> Dict[str, Any]:
    generated_at = datetime.now(timezone.utc).astimezone().date().isoformat()
    definitions = []
    for doc in docs:
        row: Dict[str, Any] = {
            "key": doc.key,
            "title": doc.title,
            "category": doc.category,
            "method": doc.method,
            "path": doc.path,
            "doc_url": doc.doc_url,
            "requires_auth": doc.requires_auth,
            "request_params": doc.request_params,
            "response_params": doc.response_params,
        }
        if doc.weight_ip is not None:
            row["weight_ip"] = doc.weight_ip
        if doc.weight_uid is not None:
            row["weight_uid"] = doc.weight_uid
        definitions.append(row)
    return {
        "generated_at": generated_at,
        "source": SITEMAP_URL,
        "product": product,
        "definitions": definitions,
    }


def render_md(product: str, docs: List[ParsedDoc], generated_at: str) -> str:
    lines = [
        f"# WEEX {product.capitalize()} API Definitions",
        "",
        f"Generated from live V3 docs on {generated_at}.",
        "",
        f"Total endpoints: **{len(docs)}**",
        "",
        "| Key | Method | Path | Auth |",
        "|---|---|---|---|",
    ]
    for doc in docs:
        lines.append(f"| `{doc.key}` | `{doc.method}` | `{doc.path}` | `{doc.requires_auth}` |")

    for doc in docs:
        lines.extend(
            [
                "",
                f"## {doc.key} — {doc.title}",
                "",
                f"- Method: `{doc.method}`",
                f"- Path: `{doc.path}`",
                f"- Category: `{doc.category}`",
                f"- Requires Auth: `{doc.requires_auth}`",
            ]
        )
        if doc.weight_ip is not None or doc.weight_uid is not None:
            lines.append(f"- Weight(IP/UID): `{doc.weight_ip or '-'} / {doc.weight_uid or '-'}`")
        lines.append(f"- Source: {doc.doc_url}")
        lines.append("")
        lines.append("### Request Parameters")
        lines.append("")
        if doc.request_params:
            lines.extend(
                [
                    "| Name | Type | Required | Description |",
                    "|---|---|---|---|",
                ]
            )
            for row in doc.request_params:
                lines.append(
                    f"| `{row.get('name', '')}` | `{row.get('type', '')}` | `{row.get('required', '')}` | {row.get('description', '')} |"
                )
        else:
            lines.append("NONE")
        lines.append("")
        lines.append("### Response Parameters")
        lines.append("")
        if doc.response_params:
            lines.extend(
                [
                    "| Name | Type | Description |",
                    "|---|---|---|",
                ]
            )
            for row in doc.response_params:
                lines.append(
                    f"| `{row.get('name', '')}` | `{row.get('type', '')}` | {row.get('description', '')} |"
                )
        else:
            lines.append("NONE")
    lines.append("")
    return "\n".join(lines)


def write_outputs(product: str, docs: List[ParsedDoc]) -> None:
    payload = docs_to_json(product, docs)
    json_path = REFS / f"{product}-api-definitions.json"
    md_path = REFS / f"{product}-api-definitions.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_md(product, docs, payload["generated_at"]) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate WEEX REST API definitions from live docs")
    parser.add_argument("--product", choices=["contract", "spot", "all"], default="all")
    args = parser.parse_args()

    sitemap_urls = load_sitemap_urls()
    products = ["contract", "spot"] if args.product == "all" else [args.product]
    for product in products:
        urls = iter_doc_urls(product, sitemap_urls)
        docs = collect_docs(product, urls)
        write_outputs(product, docs)
        print(f"{product}: generated {len(docs)} endpoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
