#!/usr/bin/env python3

import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://tushare.pro"
INDEX_URL = f"{BASE_URL}/document/2?doc_id=14"
CATEGORY_ORDER = [
    "基础数据",
    "行情数据",
    "财务数据",
    "参考数据",
    "特色数据",
    "两融及转融通",
    "资金流向数据",
    "打板专题数据",
]
CATEGORY_TITLES = set(CATEGORY_ORDER)
STOP_TITLE = "ETF专题"


def normalize_title(text: str) -> str:
    return " ".join(text.split())


def strip_title_variants(title: str) -> list[str]:
    variants = {title}
    variants.add(re.sub(r"[（(].*?[）)]", "", title).strip())
    variants.add(title.replace("（", "").replace("）", "").replace("(", "").replace(")", "").strip())
    return sorted(v for v in variants if v)


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_between(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return None
    value = match.group(1).strip()
    return re.sub(r"\s+", " ", value)


def parse_access(access_note: str | None) -> dict:
    info = {
        "mode": "unknown",
        "formal_min_points": None,
        "trial_points": None,
        "unlimited_points": None,
        "requires_extra_permission": False,
    }
    if not access_note:
        return info

    note = access_note
    if any(word in note for word in ["单独开权限", "在线开通", "联系管理员", "权限说明", "正式权限请参阅"]):
        info["requires_extra_permission"] = True

    trial_match = re.search(r"(\d+)\s*积分.*?试用", note)
    if trial_match:
        info["trial_points"] = int(trial_match.group(1))

    formal_patterns = [
        r"至少(\d+)\s*积分",
        r"达到(\d+)\s*积分",
        r"(\d+)\s*积分起",
        r"正式权限需(\d+)\s*积分",
        r"需(\d+)\s*积分",
        r"(\d+)\s*积分可提取数据",
        r"(\d+)\s*积分可以调用",
    ]
    for pattern in formal_patterns:
        match = re.search(pattern, note)
        if match:
            info["formal_min_points"] = int(match.group(1))
            break

    all_points = [int(value) for value in re.findall(r"(\d+)\s*积分", note)]
    if info["trial_points"] is not None and info["formal_min_points"] is None and len(all_points) >= 2:
        info["formal_min_points"] = all_points[1]
    if info["formal_min_points"] is None and all_points and "0积分完全开放" not in note:
        info["formal_min_points"] = all_points[0]

    unlimited_match = re.search(r"(\d+)\s*积分.*?无总量限制", note)
    if unlimited_match:
        info["unlimited_points"] = int(unlimited_match.group(1))

    if info["requires_extra_permission"]:
        info["mode"] = "extra_permission"
    elif info["formal_min_points"] is not None:
        info["mode"] = "points"
    elif info["trial_points"] is not None:
        info["mode"] = "trial_only"

    return info


def table_rows(table) -> list[list[str]]:
    rows = []
    for tr in table.find_all("tr"):
        row = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if row:
            rows.append(row)
    return rows


def parse_input_rows(rows: list[list[str]]) -> list[dict]:
    result = []
    if not rows:
        return result
    for row in rows[1:]:
        if len(row) < 4:
            continue
        result.append(
            {
                "name": row[0],
                "type": row[1],
                "required": row[2] == "Y",
                "desc": row[3],
            }
        )
    return result


def parse_output_rows(rows: list[list[str]]) -> list[dict]:
    result = []
    if not rows:
        return result
    for row in rows[1:]:
        if len(row) < 3:
            continue
        entry = {"name": row[0], "type": row[1], "desc": row[-1]}
        if len(row) >= 4:
            entry["default"] = row[2]
        result.append(entry)
    return result


def crawl_index() -> list[dict]:
    html = requests.get(INDEX_URL, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    raw_links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "document/2?doc_id=" not in href:
            continue
        title = normalize_title(anchor.get_text(" ", strip=True))
        raw_links.append((title, urljoin(BASE_URL, href)))

    seen = set()
    ordered = []
    for title, href in raw_links:
        key = (title, href)
        if key in seen:
            continue
        seen.add(key)
        ordered.append((title, href))

    current_category = None
    selected = []
    for title, href in ordered:
        if title == STOP_TITLE:
            break
        if title in CATEGORY_TITLES:
            current_category = title
            continue
        if not current_category or title == "股票数据":
            continue
        selected.append(
            {
                "category": current_category,
                "title": title,
                "url": href,
                "doc_id": int(re.search(r"doc_id=(\d+)", href).group(1)),
            }
        )
    return selected


def parse_endpoint(entry: dict) -> dict:
    html = requests.get(entry["url"], timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(soup.get_text("\n"))

    api_name = extract_between(text, r"(?:接口：|接口名称\s*：)([^\n，,(（]+)")
    description = extract_between(text, r"(?:描述：|接口说明\s*：)(.+?)(?:\n(?:积分|权限|限量|提示|注：|输入参数|复权说明)|$)")
    access_note = extract_between(text, r"(?:积分|权限)：(.+?)(?:\n(?:提示|注：|输入参数)|$)")
    limit_note = extract_between(text, r"限量：(.+?)(?:\n(?:积分|权限|提示|注：|输入参数)|$)")
    prompt_note = extract_between(text, r"(?:提示|注：)(.+?)(?:\n输入参数|$)")

    tables = [table_rows(table) for table in soup.find_all("table")]
    input_rows = []
    output_rows = []
    if tables:
        for rows in tables:
            if rows and rows[0][:4] == ["名称", "类型", "必选", "描述"]:
                input_rows = rows
                break
    if tables:
        for rows in tables:
            if rows and rows[0][:2] == ["名称", "类型"] and rows[0][-1] == "描述" and rows is not input_rows:
                output_rows = rows
                break

    access = parse_access(access_note)
    aliases = strip_title_variants(entry["title"])
    if api_name:
        aliases.append(api_name)
    inactive = "（停" in entry["title"] or "(停" in entry["title"] or (prompt_note and "暂无新增数据" in prompt_note)

    return {
        "category": entry["category"],
        "title": entry["title"],
        "doc_id": entry["doc_id"],
        "url": entry["url"],
        "api_name": api_name,
        "description": description,
        "access_note": access_note,
        "limit_note": limit_note,
        "access": access,
        "inactive": inactive,
        "aliases": sorted({alias for alias in aliases if alias}),
        "input_params": parse_input_rows(input_rows),
        "output_fields": parse_output_rows(output_rows),
    }


def render_markdown(catalog: list[dict]) -> str:
    lines = [
        "# Tushare Stock Endpoint Catalog",
        "",
        "Generated from the official Tushare stock-data docs.",
        "",
    ]
    current_category = None
    for item in catalog:
        if item["category"] != current_category:
            current_category = item["category"]
            lines.extend([f"## {current_category}", ""])
        access = item["access_note"] or "未写明"
        lines.append(
            f"- `{item['api_name']}` - {item['title']} - {access}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    ref_dir = base_dir / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    index_entries = crawl_index()
    catalog = [parse_endpoint(entry) for entry in index_entries]
    catalog.sort(key=lambda item: (CATEGORY_ORDER.index(item["category"]) if item["category"] in CATEGORY_TITLES else 999, item["doc_id"]))

    json_path = ref_dir / "stock_endpoints.json"
    md_path = ref_dir / "stock_endpoints.md"

    payload = {
        "source_index": INDEX_URL,
        "generated_count": len(catalog),
        "catalog": catalog,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(catalog), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
