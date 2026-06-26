#!/usr/bin/env python3
"""Shared client helpers for the report-search skill."""

from __future__ import annotations

import html
import json
import os
import re
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from html.parser import HTMLParser
from typing import Any

try:
    import certifi
except ImportError:  # pragma: no cover - optional dependency
    certifi = None


BASE_URL = os.getenv("FXBAOGAO_BASE_URL", "https://api.fxbaogao.com")
DETAIL_BASE_URL = os.getenv("FXBAOGAO_DETAIL_BASE_URL", "https://www.fxbaogao.com")
HTTP_TIMEOUT = float(os.getenv("FXBAOGAO_HTTP_TIMEOUT", "30"))
USER_AGENT = os.getenv(
    "FXBAOGAO_USER_AGENT",
    "report-search-skill/1.0 (+https://www.fxbaogao.com)",
)
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
SSL_NO_VERIFY = os.getenv("FXBAOGAO_SSL_NO_VERIFY", "").lower() in {"1", "true", "yes"}

RELATIVE_TIME_VALUES = {
    "last3day",
    "last7day",
    "last1mon",
    "last3mon",
    "last1year",
}


class FxbaogaoError(RuntimeError):
    """Raised when the remote API or detail page cannot be parsed."""


class _HTMLTextExtractor(HTMLParser):
    """Convert small HTML fragments into readable plain text."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"br", "p", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def get_text(self) -> str:
        text = "".join(self.parts)
        text = html.unescape(text)
        text = re.sub(r"[ \t\f\v]+", " ", text)
        text = re.sub(r"\s*\n\s*", "\n", text)
        return text.strip()


class _SummaryHTMLParser(HTMLParser):
    """Parse the summaryHtml payload into titled bullet sections."""

    def __init__(self) -> None:
        super().__init__()
        self.sections: list[dict[str, Any]] = []
        self._heading_parts: list[str] = []
        self._item_parts: list[str] = []
        self._in_heading = False
        self._in_item = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in HEADING_TAGS:
            self._flush_heading()
            self._in_heading = True
            self._heading_parts = []
            return
        if tag == "li":
            self._flush_item()
            self._in_item = True
            self._item_parts = []
            return
        if tag == "br":
            if self._in_heading:
                self._heading_parts.append("\n")
            if self._in_item:
                self._item_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in HEADING_TAGS and self._in_heading:
            self._flush_heading()
        if tag == "li" and self._in_item:
            self._flush_item()

    def handle_data(self, data: str) -> None:
        if self._in_heading:
            self._heading_parts.append(data)
        if self._in_item:
            self._item_parts.append(data)

    def _flush_heading(self) -> None:
        if not self._in_heading:
            return
        title = _normalize_text("".join(self._heading_parts))
        if title:
            self.sections.append({"title": title, "items": []})
        self._heading_parts = []
        self._in_heading = False

    def _flush_item(self) -> None:
        if not self._in_item:
            return
        item = _normalize_text("".join(self._item_parts))
        if item:
            if not self.sections:
                self.sections.append({"title": "摘要", "items": []})
            self.sections[-1]["items"].append(item)
        self._item_parts = []
        self._in_item = False

    def get_sections(self) -> list[dict[str, Any]]:
        self._flush_heading()
        self._flush_item()
        return [section for section in self.sections if section["items"]]


def _normalize_text(value: str) -> str:
    text = html.unescape(value)
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    return text.strip()


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    parser = _HTMLTextExtractor()
    parser.feed(value)
    parser.close()
    return parser.get_text()


def parse_summary_html(summary_html: str | None) -> list[dict[str, Any]]:
    if not summary_html:
        return []
    parser = _SummaryHTMLParser()
    parser.feed(summary_html)
    parser.close()
    return parser.get_sections()


def parse_relative_time(time_str: str, now: datetime | None = None) -> int:
    """Convert supported relative time aliases into a start timestamp in ms."""
    current = now or datetime.now()
    deltas = {
        "last3day": timedelta(days=3),
        "last7day": timedelta(days=7),
        "last1mon": timedelta(days=30),
        "last3mon": timedelta(days=90),
        "last1year": timedelta(days=365),
    }
    if time_str not in deltas:
        raise ValueError(
            f"未知的时间格式: {time_str}。支持的格式: {sorted(deltas)}"
        )
    return int((current - deltas[time_str]).timestamp() * 1000)


def parse_date_to_timestamp(date_str: str, *, end_of_day: bool = False) -> int:
    date_str = date_str.strip()
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"日期格式错误: {date_str}，应为 YYYY-MM-DD") from exc
    if end_of_day:
        parsed = parsed.replace(hour=23, minute=59, second=59, microsecond=999000)
    return int(parsed.timestamp() * 1000)


def _request(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> str:
    body = None
    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/html;q=0.9,*/*;q=0.8",
    }
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        url,
        data=body,
        headers=request_headers,
        method=method,
    )
    ssl_context = _build_ssl_context()

    try:
        with urllib.request.urlopen(
            request,
            timeout=HTTP_TIMEOUT,
            context=ssl_context,
        ) as response:
            return response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        detail = _normalize_text(detail)[:200]
        raise FxbaogaoError(f"HTTP {exc.code}: {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise FxbaogaoError(f"网络请求失败: {exc.reason}") from exc


def _request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    raw = _request(url, method=method, payload=payload, headers=headers)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FxbaogaoError("接口返回了无法解析的 JSON") from exc


def _build_ssl_context() -> ssl.SSLContext:
    if SSL_NO_VERIFY:
        return ssl._create_unverified_context()
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def _format_publish_date(pub_time: Any, pub_time_str: str | None) -> str:
    if isinstance(pub_time, (int, float)) and pub_time > 0:
        return datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d")
    if pub_time_str:
        cleaned = pub_time_str.strip().rstrip("/")
        return cleaned.replace("/", "-")
    return ""


def _clean_snippet(value: str | None) -> str:
    cleaned = strip_html(value)
    return re.sub(r"^[•·]+\s*", "", cleaned)


def _clean_name_list(values: list[str] | None) -> list[str]:
    cleaned_values: list[str] = []
    for value in values or []:
        cleaned = strip_html(value)
        if cleaned and cleaned != "-":
            cleaned_values.append(cleaned)
    return cleaned_values


def normalize_search_result(
    raw_result: dict[str, Any],
    *,
    keywords: str | None,
    authors: list[str] | None,
    org_names: list[str] | None,
    start_time: int | None,
    end_time: int | str | None,
    page_size: int,
) -> dict[str, Any]:
    if raw_result.get("code") != 0:
        raise FxbaogaoError(raw_result.get("msg") or "搜索接口返回失败")

    data = raw_result.get("data") or {}
    reports: list[dict[str, Any]] = []

    for item in data.get("dataList") or []:
        doc_id = item.get("docId")
        reports.append(
            {
                "doc_id": doc_id,
                "title": strip_html(item.get("title")) or "无标题",
                "org_name": strip_html(item.get("orgName")) or "",
                "authors": _clean_name_list(item.get("authors")),
                "publish_date": _format_publish_date(
                    item.get("pubTime"),
                    item.get("pubTimeStr"),
                ),
                "publish_timestamp": item.get("pubTime"),
                "industry_name": strip_html(item.get("industryName")) or "",
                "page_count": item.get("pageNum"),
                "report_url": f"{DETAIL_BASE_URL}/view?id={doc_id}" if doc_id else "",
                "detail_url": f"{DETAIL_BASE_URL}/detail/{doc_id}" if doc_id else "",
                "snippets": [
                    _clean_snippet(paragraph.get("content"))
                    for paragraph in item.get("paragraphObjs") or []
                    if _clean_snippet(paragraph.get("content"))
                ],
            }
        )

    return {
        "query": {
            "keywords": keywords,
            "authors": authors or [],
            "org_names": org_names or [],
            "start_time": start_time,
            "end_time": end_time,
        },
        "total": data.get("count") or data.get("total") or 0,
        "page_size": data.get("limit") or page_size,
        "current_page": data.get("currPage") or 1,
        "reports": reports,
    }


def search_reports(
    *,
    keywords: str | None = None,
    authors: list[str] | None = None,
    org_names: list[str] | None = None,
    start_time: int | None = None,
    end_time: int | str | None = None,
    page_size: int = 10,
) -> dict[str, Any]:
    if not keywords and not authors and not org_names:
        raise ValueError("请至少指定一个搜索条件（关键词、作者或机构）")

    if isinstance(end_time, str) and end_time not in RELATIVE_TIME_VALUES:
        raise ValueError(
            f"未知的时间格式: {end_time}。支持的格式: {sorted(RELATIVE_TIME_VALUES)}"
        )

    clamped_page_size = max(1, min(page_size, 100))
    payload = {
        "keywords": keywords,
        "authors": authors or [],
        "orgNames": org_names or [],
        "paragraphSize": 3,
        "startTime": start_time,
        "endTime": end_time,
        "pageSize": clamped_page_size,
        "pageNum": 1,
    }

    raw_result = _request_json(
        f"{BASE_URL}/mofoun/report/searchReport/searchNoAuth",
        method="POST",
        payload=payload,
    )

    return normalize_search_result(
        raw_result,
        keywords=keywords,
        authors=authors,
        org_names=org_names,
        start_time=start_time,
        end_time=end_time,
        page_size=clamped_page_size,
    )


def _extract_next_data(document: str) -> dict[str, Any]:
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        document,
        re.DOTALL,
    )
    if not match:
        raise FxbaogaoError("详情页中未找到 __NEXT_DATA__ 数据")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise FxbaogaoError("详情页中的 __NEXT_DATA__ 无法解析") from exc


def _split_content_lines(raw_content: str | None) -> list[str]:
    if not raw_content:
        return []
    lines: list[str] = []
    for chunk in re.split(r"[\r\n]+", raw_content):
        cleaned = _normalize_text(chunk)
        cleaned = re.sub(r"^[•·]+\s*", "", cleaned)
        if cleaned:
            lines.append(cleaned)
    return lines


def get_report_content(doc_id: int) -> dict[str, Any]:
    document = _request(
        f"{DETAIL_BASE_URL}/detail/{doc_id}",
        headers={"AUTH-KEY": ""},
    )
    next_data = _extract_next_data(document)
    page_props = next_data.get("props", {}).get("pageProps", {})
    detail_data = page_props.get("dtlData") or {}
    report = detail_data.get("report") or {}

    summary_sections = parse_summary_html(detail_data.get("summaryHtml"))
    summary = [
        item
        for section in summary_sections
        for item in section.get("items", [])
    ]
    raw_content = detail_data.get("content") or ""

    return {
        "doc_id": doc_id,
        "title": strip_html(report.get("title")) or "",
        "org_name": strip_html(report.get("orgName")) or "",
        "authors": _clean_name_list(report.get("authors")),
        "industry_name": strip_html(report.get("industryName")) or "",
        "publish_date": _format_publish_date(
            report.get("pubTime"),
            report.get("pubTimeStr"),
        ),
        "page_count": report.get("pageNum"),
        "report_url": f"{DETAIL_BASE_URL}/view?id={doc_id}",
        "detail_url": f"{DETAIL_BASE_URL}/detail/{doc_id}",
        "summary_sections": summary_sections,
        "summary": summary,
        "content": _split_content_lines(raw_content),
        "raw_content": raw_content,
    }


def format_search_output(result: dict[str, Any]) -> str:
    reports = result.get("reports") or []
    total = result.get("total", 0)
    lines = [
        f"找到 {total} 条相关研报，展示前 {len(reports)} 条。",
        "-" * 60,
    ]

    for index, report in enumerate(reports, start=1):
        authors = "、".join(report.get("authors") or []) or "未知作者"
        lines.extend(
            [
                f"{index}. {report.get('title') or '无标题'}",
                f"   机构: {report.get('org_name') or '未知机构'}",
                f"   作者: {authors}",
                f"   日期: {report.get('publish_date') or '未知日期'}",
                f"   文档ID: {report.get('doc_id') or 'N/A'}",
                f"   链接: {report.get('report_url') or ''}",
            ]
        )

        snippets = report.get("snippets") or []
        if snippets:
            lines.append(f"   摘要片段: {snippets[0]}")

        lines.append("")

    return "\n".join(lines).rstrip()


def format_detail_output(result: dict[str, Any], *, max_content_lines: int = 20) -> str:
    authors = "、".join(result.get("authors") or []) or "未知作者"
    lines = [
        "=" * 60,
        result.get("title") or f"研报详情 (ID: {result.get('doc_id')})",
        f"机构: {result.get('org_name') or '未知机构'}",
        f"作者: {authors}",
        f"日期: {result.get('publish_date') or '未知日期'}",
        f"详情页: {result.get('detail_url') or ''}",
        "=" * 60,
    ]

    for section in result.get("summary_sections") or []:
        lines.append("")
        lines.append(f"## {section.get('title') or '摘要'}")
        lines.append("")
        for item in section.get("items") or []:
            lines.append(f"- {item}")

    content_lines = result.get("content") or []
    if content_lines:
        lines.append("")
        lines.append("## 正文摘录")
        lines.append("")
        for line in content_lines[:max_content_lines]:
            if len(line) > 220:
                line = f"{line[:220]}..."
            lines.append(line)
        if len(content_lines) > max_content_lines:
            lines.append("")
            lines.append(
                f"... (共 {len(content_lines)} 段，仅显示前 {max_content_lines} 段)"
            )

    return "\n".join(lines)
