#!/usr/bin/env python3
"""Generate Server-Mate markdown and PDF reports from SQLite rollups."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import shutil
import socket
import sqlite3
import ssl
import subprocess
import sys
import textwrap
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import font_manager, pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import FancyBboxPatch
    from matplotlib.ticker import FuncFormatter, MaxNLocator
except ImportError:  # pragma: no cover
    matplotlib = None
    font_manager = None
    plt = None
    PdfPages = None
    FancyBboxPatch = None
    FuncFormatter = None
    MaxNLocator = None

from server_agent import (
    HOST_METRIC_SITE,
    build_site_runtime_config,
    find_site,
    get_timezone,
    load_config,
    resolve_sites,
)
from webhook_center import send_markdown_message


PDF_COLORS = {
    "bg": "#ffffff",
    "panel": "#ffffff",
    "panel_alt": "#fafafa",
    "border": "#e5e7eb",
    "divider": "#e5e7eb",
    "grid": "#eeeeee",
    "text": "#000000",
    "muted": "#666666",
    "subtle": "#888888",
    "blue": "#2563eb",
    "green": "#16a34a",
    "teal": "#0891b2",
    "orange": "#ea580c",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "yellow": "#ca8a04",
    "sky": "#0ea5e9",
    "gray": "#94a3b8",
}

MORANDI_PALETTE = [
    "#7C8A9B",
    "#9AA690",
    "#B79E8C",
    "#AFA1BF",
    "#9FA7A6",
    "#C2B59B",
    "#8E9AA8",
    "#B7A39A",
]

CARD_COLORS = {
    "face": "#FFFFFF",
    "edge": "#ECECEC",
    "muted": "#000000",
    "subtle": "#000000",
    "header": "#FAFAFA",
    "zebra": "#F9F9F9",
}

ENTERPRISE_DONUT_COLORS = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
]

PDF_FONT_PATHS = [
    Path(__file__).resolve().parents[1] / "assets" / "NotoSansSC-VF.ttf",
]
GEOIP_MIRROR_URL = "https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-City.mmdb"
DEFAULT_GEOIP_UPDATE_CONFIG = Path("./data/GeoIP.conf")
SSL_WARNING_DAYS = 15

TRANSLATIONS = {
    "zh": {
        "daily_title": "Server-Mate 日报",
        "weekly_title": "Server-Mate 周报",
        "monthly_title": "Server-Mate 月报",
        "monitoring_report": "Server-Mate 监控报表",
        "dashboard_page": "核心大盘",
        "details_page": "详情明细",
        "generated_at": "生成时间",
        "page_indicator": "第 {current} 页 / 共 {total} 页",
        "site": "站点",
        "host": "主机",
        "window": "统计窗口",
        "date": "统计日期",
        "bucket": "统计粒度",
        "core_metrics": "核心指标",
        "status_mix": "状态码分布",
        "top_errors": "高频错误 Top 10",
        "top_uris": "热门 URI Top 10",
        "spiders": "蜘蛛抓取概览",
        "system_health": "服务器健康",
        "pv": "PV",
        "uv": "UV",
        "ips": "独立 IP",
        "requests": "总请求数",
        "bandwidth_out": "下行流量",
        "bandwidth_in": "上行流量",
        "peak_qps": "峰值 QPS",
        "avg_response": "平均响应",
        "slow_requests": "慢请求数",
        "daily_hourly_trend": "24 小时流量热力折线图",
        "slow_routes": "最慢响应路由 Top 10",
        "abnormal_ips": "高频异常 IP Top 10",
        "traffic_trend": "流量趋势",
        "spider_distribution": "蜘蛛抓取分布",
        "http_status_mix": "HTTP 状态码占比",
        "wow_summary": "周环比摘要",
        "security_summary": "安全防御与拦截汇总",
        "cpu_disk_trend": "CPU 与磁盘消耗趋势",
        "daily_breakdown": "日维度明细",
        "summary": "摘要",
        "ai_summary_title": "AI 智能分析",
        "ai_summary_badge": "智能诊断",
        "compare_day": "昨日",
        "compare_week": "上周",
        "compare_month": "上月",
        "total_traffic": "总流量",
        "spider_total": "蜘蛛爬虫",
        "kpi_compare_na": "暂无可比数据",
        "download_url": "下载链接",
        "report_path": "PDF 路径",
        "no_data": "暂无数据",
        "local_only": "未配置 public_base_url，当前仅提供本地文件路径。",
        "report_ready": "PDF 已生成",
        "trend_pv_uv": "近 7 天流量趋势图",
        "trend_30d": "30 天平滑流量趋势",
        "period_delta": "环比变化",
        "security_404": "404 扫描量",
        "security_5xx": "5xx 错误量",
        "security_bad_ips": "异常 IP 数",
        "report_note": "说明: 纯 webhook 通道通常不支持直接上传 PDF，当前采用“生成文件 + 推送路径或下载链接”的轻量方案。",
        "hour": "时段",
        "count": "次数",
        "value": "数值",
        "item": "项目",
        "rank": "排名",
        "cpu": "CPU",
        "memory": "内存",
        "disk": "磁盘",
        "avg_short": "平均",
        "current": "本期",
        "previous": "上期",
        "delta": "变化",
        "ratio": "环比",
        "rpm": "RPM",
        "other": "其他",
        "system_overview": "系统健康摘要",
        "security_overview": "安全态势摘要",
        "kpi_pv_subtitle": "周期总浏览量",
        "kpi_uv_subtitle": "独立访客",
        "kpi_requests_subtitle": "全部请求数",
        "kpi_qps_subtitle": "峰值请求吞吐",
        "kpi_response_subtitle": "平均响应耗时",
        "kpi_slow_subtitle": "慢请求累计次数",
        "kpi_cpu_subtitle": "周期 CPU 最高值",
        "kpi_memory_subtitle": "周期内存最高值",
        "kpi_disk_subtitle": "磁盘最低剩余空间",
        "resource_cpu": "CPU 峰值 (%)",
        "resource_disk": "磁盘剩余 (GB)",
        "warning_estimate": "说明: UV/IP 若无明细表则退化为闭合桶估算值。",
    },
    "en": {
        "daily_title": "Server-Mate Daily Report",
        "weekly_title": "Server-Mate Weekly Report",
        "monthly_title": "Server-Mate Monthly Report",
        "monitoring_report": "Server-Mate Monitoring Report",
        "dashboard_page": "Core Dashboard",
        "details_page": "Details",
        "generated_at": "Generated At",
        "page_indicator": "Page {current} / {total}",
        "site": "Site",
        "host": "Host",
        "window": "Window",
        "date": "Date",
        "bucket": "Bucket",
        "core_metrics": "Core Metrics",
        "status_mix": "HTTP Status Mix",
        "top_errors": "Top Errors Top 10",
        "top_uris": "Top URIs Top 10",
        "spiders": "Spider Overview",
        "system_health": "System Health",
        "pv": "PV",
        "uv": "UV",
        "ips": "IPs",
        "requests": "Requests",
        "bandwidth_out": "Outbound",
        "bandwidth_in": "Inbound",
        "peak_qps": "Peak QPS",
        "avg_response": "Avg Response",
        "slow_requests": "Slow Requests",
        "daily_hourly_trend": "24h Traffic Heat Line",
        "slow_routes": "Slowest Routes Top 10",
        "abnormal_ips": "Abnormal IPs Top 10",
        "traffic_trend": "Traffic Trend",
        "spider_distribution": "Spider Distribution",
        "http_status_mix": "HTTP Status Ratio",
        "wow_summary": "Week-over-Week Summary",
        "security_summary": "Security Summary",
        "cpu_disk_trend": "CPU and Disk Trend",
        "daily_breakdown": "Daily Breakdown",
        "summary": "Summary",
        "ai_summary_title": "AI Analysis",
        "ai_summary_badge": "Smart Insights",
        "compare_day": "Yesterday",
        "compare_week": "Last Week",
        "compare_month": "Last Month",
        "total_traffic": "Total Traffic",
        "spider_total": "Spiders",
        "kpi_compare_na": "No prior period data",
        "download_url": "Download URL",
        "report_path": "PDF Path",
        "no_data": "No data",
        "local_only": "No public_base_url configured; only local file path is available.",
        "report_ready": "PDF generated",
        "trend_pv_uv": "7-day PV vs UV Trend",
        "trend_30d": "30-day Smoothed Traffic Trend",
        "period_delta": "Period Delta",
        "security_404": "404 Volume",
        "security_5xx": "5xx Volume",
        "security_bad_ips": "Abnormal IPs",
        "report_note": "Note: generic incoming webhooks usually cannot upload PDF files directly, so Server-Mate delivers a local path or public URL instead.",
        "hour": "Hour",
        "count": "Count",
        "value": "Value",
        "item": "Item",
        "rank": "Rank",
        "cpu": "CPU",
        "memory": "Memory",
        "disk": "Disk",
        "avg_short": "Avg",
        "current": "Current",
        "previous": "Previous",
        "delta": "Delta",
        "ratio": "WoW",
        "rpm": "RPM",
        "other": "Other",
        "system_overview": "System Summary",
        "security_overview": "Security Summary",
        "kpi_pv_subtitle": "Total page views",
        "kpi_uv_subtitle": "Unique visitors",
        "kpi_requests_subtitle": "All processed requests",
        "kpi_qps_subtitle": "Peak query throughput",
        "kpi_response_subtitle": "Average response latency",
        "kpi_slow_subtitle": "Slow request volume",
        "kpi_cpu_subtitle": "Period CPU peak",
        "kpi_memory_subtitle": "Period memory peak",
        "kpi_disk_subtitle": "Lowest free disk",
        "resource_cpu": "CPU Peak (%)",
        "resource_disk": "Disk Free (GB)",
        "warning_estimate": "Note: UV/IP falls back to rollup approximation when detail tables are missing.",
    },
}

TRANSLATIONS["zh"].update(
    {
        "daily_title": "Server-Mate 日报",
        "weekly_title": "Server-Mate 周报",
        "monthly_title": "Server-Mate 月报",
        "monitoring_report": "Server-Mate 监控报告",
        "dashboard_page": "核心看板",
        "details_page": "明细页",
        "generated_at": "生成时间",
        "page_indicator": "第 {current} 页 / 共 {total} 页",
        "site": "站点",
        "host": "主机",
        "window": "统计窗口",
        "date": "统计日期",
        "bucket": "统计粒度",
        "core_metrics": "核心指标",
        "status_mix": "状态码分布",
        "top_errors": "高频错误 Top 10",
        "top_uris": "热门 URI Top 10",
        "spiders": "蜘蛛爬虫概览",
        "system_health": "系统健康度",
        "pv": "浏览量(PV)",
        "uv": "访客数(UV)",
        "ips": "IP 数",
        "requests": "总请求数",
        "bandwidth_out": "出站流量",
        "bandwidth_in": "入站流量",
        "peak_qps": "峰值 QPS",
        "avg_response": "平均响应",
        "slow_requests": "慢请求",
        "daily_hourly_trend": "24 小时流量热力折线",
        "slow_routes": "慢响应路由 Top 10",
        "abnormal_ips": "高频异常 IP Top 10",
        "traffic_trend": "流量趋势",
        "spider_distribution": "蜘蛛抓取分布",
        "http_status_mix": "HTTP 状态码占比",
        "wow_summary": "环比摘要",
        "security_summary": "安全防御与拦截汇总",
        "cpu_disk_trend": "CPU 与磁盘趋势",
        "daily_breakdown": "日报明细",
        "summary": "摘要",
        "ai_summary_title": "AI 智能分析摘要",
        "ai_summary_badge": "智能分析",
        "compare_day": "昨日",
        "compare_week": "上周",
        "compare_month": "上月",
        "total_traffic": "总流量",
        "spider_total": "蜘蛛爬虫",
        "kpi_compare_na": "暂无可比数据",
        "download_url": "下载链接",
        "report_path": "PDF 路径",
        "no_data": "暂无数据",
        "local_only": "未配置 public_base_url，仅提供本地文件路径。",
        "report_ready": "PDF 已生成",
        "trend_pv_uv": "近 7 天流量趋势",
        "trend_30d": "30 天平滑流量趋势",
        "period_delta": "周期变化",
        "security_404": "404 扫描量",
        "security_5xx": "5xx 错误量",
        "security_bad_ips": "异常 IP 数",
        "report_note": "说明：通用 Webhook 通常无法直接上传 PDF，Server-Mate 会推送本地路径或公网下载链接。",
        "hour": "小时",
        "count": "次数",
        "value": "数值",
        "item": "项目",
        "rank": "排名",
        "cpu": "CPU",
        "memory": "内存",
        "disk": "磁盘",
        "avg_short": "平均",
        "current": "本期",
        "previous": "上期",
        "delta": "变化",
        "ratio": "环比",
        "rpm": "RPM",
        "other": "其他",
        "system_overview": "系统健康摘要",
        "security_overview": "安全态势摘要",
        "kpi_pv_subtitle": "总浏览量",
        "kpi_uv_subtitle": "独立访客",
        "kpi_requests_subtitle": "总请求量",
        "kpi_qps_subtitle": "请求峰值",
        "kpi_response_subtitle": "平均响应延迟",
        "kpi_slow_subtitle": "慢请求数",
        "kpi_cpu_subtitle": "周期 CPU 峰值",
        "kpi_memory_subtitle": "周期内存峰值",
        "kpi_disk_subtitle": "最低剩余磁盘",
        "resource_cpu": "CPU 峰值 (%)",
        "resource_disk": "磁盘剩余 (GB)",
        "warning_estimate": "说明：当明细表缺失时，UV/IP 将回退为 rollup 近似值。",
        "performance_load": "性能/负载",
        "website_traffic": "网站流量",
        "spider_stats": "蜘蛛统计",
        "status_code_stats": "状态码统计",
        "hot_pages": "热门页面",
        "hot_ips": "热门 IP",
        "hot_referers": "热门来源",
        "url_path": "URL路径",
        "ip_address": "IP地址",
        "referer_source": "Referer来源",
        "spider_crawl_stats": "蜘蛛爬取统计",
        "status_code": "状态码",
        "request_volume": "请求量",
        "share": "占比",
        "province_access_distribution": "省份访问分布",
        "province": "省份",
        "visits": "访问量",
        "client_distribution": "客户端分布",
        "client": "客户端",
        "google": "谷歌",
        "baidu": "百度",
        "bing": "必应",
        "sogou": "搜狗",
        "yandex": "Yandex",
        "spider_360": "360",
        "total": "汇总",
        "crawler_top10": "蜘蛛爬虫 Top 10",
        "status_detail_top10": "状态码详情 Top 10",
        "province_top10": "省份 Top 10",
        "client_top10": "客户端 Top 10",
        "traffic_volume": "流量",
        "info": "信息",
        "visit_volume": "访问量",
        "largest": "最大",
        "smallest": "最小",
    }
)

TRANSLATIONS["en"].update(
    {
        "top_errors": "Top Errors Top 10",
        "top_uris": "Top URIs Top 10",
        "slow_routes": "Slowest Routes Top 10",
        "abnormal_ips": "Abnormal IPs Top 10",
        "performance_load": "Performance / Load",
        "website_traffic": "Website Traffic",
        "spider_stats": "Spider Stats",
        "status_code_stats": "HTTP Status Stats",
        "hot_pages": "Top Pages",
        "hot_ips": "Top IPs",
        "hot_referers": "Top Referers",
        "url_path": "URL Path",
        "ip_address": "IP Address",
        "referer_source": "Referer Source",
        "spider_crawl_stats": "Crawler Activity",
        "status_code": "Status Code",
        "request_volume": "Requests",
        "share": "Share",
        "province_access_distribution": "Province Traffic",
        "province": "Province",
        "visits": "Visits",
        "client_distribution": "Client Distribution",
        "client": "Client",
        "google": "Google",
        "baidu": "Baidu",
        "bing": "Bing",
        "sogou": "Sogou",
        "yandex": "Yandex",
        "spider_360": "360",
        "total": "Total",
        "crawler_top10": "Crawler Top 10",
        "status_detail_top10": "Status Detail Top 10",
        "province_top10": "Province Top 10",
        "client_top10": "Client Top 10",
        "traffic_volume": "Traffic",
        "info": "Info",
        "visit_volume": "Visits",
        "largest": "Max",
        "smallest": "Min",
    }
)

TRANSLATIONS["zh"].update(
    {
        "ssl_remaining": "SSL 证书剩余",
        "http_status_distribution": "HTTP 状态码分布",
        "top_pages_short": "热门页面 Top 3",
        "top_ips_short": "访问 IP Top 3",
    }
)

TRANSLATIONS["en"].update(
    {
        "ssl_remaining": "SSL Remaining",
        "http_status_distribution": "HTTP Status Mix",
        "top_pages_short": "Top Pages",
        "top_ips_short": "Top IPs",
    }
)

TRANSLATIONS["zh"].update(
    {
        "pageviews_pv": "浏览量(PV)",
        "visitors_uv": "访问数(UV)",
        "region": "地区",
    }
)

TRANSLATIONS["en"].update(
    {
        "pageviews_pv": "Pageviews (PV)",
        "visitors_uv": "Visitors (UV)",
        "region": "Region",
    }
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Server-Mate daily Markdown or PDF reports."
    )
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))

    subparsers = parser.add_subparsers(dest="command")

    daily_parser = subparsers.add_parser("daily", help="Generate a daily markdown report.")
    daily_parser.add_argument("--date", help="Local date in YYYY-MM-DD.")
    daily_parser.add_argument("--site", help="Generate report for a specific site domain.")
    daily_parser.add_argument("--output", type=Path, help="Optional markdown output path.")
    daily_parser.add_argument("--send", action="store_true")
    daily_parser.add_argument("--channels", nargs="+")
    daily_parser.add_argument("--json", action="store_true")

    pdf_parser = subparsers.add_parser("pdf", help="Generate a visual PDF report.")
    pdf_parser.add_argument(
        "--range",
        choices=("daily", "weekly", "monthly"),
        default="weekly",
    )
    pdf_parser.add_argument("--end-date", help="Local end date in YYYY-MM-DD.")
    pdf_parser.add_argument("--site", help="Generate report for a specific site domain.")
    pdf_parser.add_argument("--output", type=Path, help="Optional PDF output path.")
    pdf_parser.add_argument("--send", action="store_true")
    pdf_parser.add_argument("--channels", nargs="+")
    pdf_parser.add_argument("--json", action="store_true")

    return parser.parse_args()


def emit_text(text: str) -> None:
    data = text.encode("utf-8", errors="replace")
    sys.stdout.buffer.write(data)
    if not text.endswith("\n"):
        sys.stdout.buffer.write(b"\n")


def parse_local_date(raw: str | None, timezone: dt.tzinfo, default_offset_days: int) -> dt.date:
    if raw:
        return dt.date.fromisoformat(raw)
    return (dt.datetime.now(timezone) + dt.timedelta(days=default_offset_days)).date()


def t(config: dict[str, Any], key: str) -> str:
    reports = config.get("notifications", {}).get("reports", {})
    language = str(reports.get("report_language") or "zh").lower()
    if language not in TRANSLATIONS:
        language = "zh"
    return TRANSLATIONS[language].get(key, key)


def report_language(config: dict[str, Any]) -> str:
    reports = config.get("notifications", {}).get("reports", {})
    language = str(reports.get("report_language") or "zh").lower()
    return language if language in TRANSLATIONS else "zh"


def format_bytes(num_bytes: int | float | None) -> str:
    if num_bytes is None:
        return "N/A"
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < 1024.0 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} TB"


def format_number(value: int | float | None, digits: int = 2) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return f"{value:,}"
    return f"{value:,.{digits}f}"


def format_percent(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}%"


def format_signed_number(value: int | float | None, digits: int = 2) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, int) or float(value).is_integer():
        return f"{int(value):+,}"
    return f"{float(value):+,.{digits}f}"


def safe_ratio(part: int | float, total: int | float) -> float:
    if not total:
        return 0.0
    return float(part) / float(total)


def truncate_text(value: str, limit: int = 40) -> str:
    return value if len(value) <= limit else value[: max(limit - 3, 1)] + "..."


def sanitize_long_table_text(
    value: Any,
    limit: int = 45,
    *,
    strip_query: bool = True,
) -> str:
    text = str(value or "").strip()
    if strip_query:
        text = text.split("?", 1)[0]
    text = re.sub(r"\s+", " ", text)
    if len(text) > limit:
        text = text[: max(limit - 3, 1)] + "..."
    return text or "-"


def wrap_dashboard_text(value: Any, width: int = 40) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return "-"

    wrapped_lines: list[str] = []
    limit = max(int(width), 1)
    for raw_line in text.split("\n"):
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line:
            wrapped_lines.append("")
            continue
        if re.search(r"[\u3400-\u9FFF]", line):
            current = ""
            current_width = 0
            for char in line:
                char_width = 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
                if current and current_width + char_width > limit:
                    wrapped_lines.append(current)
                    current = char
                    current_width = char_width
                else:
                    current += char
                    current_width += char_width
            if current:
                wrapped_lines.append(current)
            continue
        wrapped_lines.append(
            textwrap.fill(
                line,
                width=limit,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return "\n".join(wrapped_lines).strip() or "-"


def moving_average(values: list[float], window: int) -> list[float]:
    if not values:
        return []
    result = []
    for index in range(len(values)):
        start = max(0, index - window + 1)
        chunk = values[start : index + 1]
        result.append(sum(chunk) / len(chunk))
    return result


def report_span_days(report_kind: str) -> int:
    return {"daily": 1, "weekly": 7, "monthly": 30}.get(report_kind, 1)


def compare_label(config: dict[str, Any], report_kind: str) -> str:
    key = {
        "daily": "compare_day",
        "weekly": "compare_week",
        "monthly": "compare_month",
    }.get(report_kind, "compare_day")
    return t(config, key)


def total_spider_count(report: dict[str, Any]) -> int:
    return sum(int(item["count"]) for item in report.get("spiders", []))


def total_traffic_bytes(report: dict[str, Any]) -> int | None:
    traffic = report.get("traffic", {})
    outbound = traffic.get("bandwidth_out_bytes")
    inbound = traffic.get("bandwidth_in_bytes")
    if outbound is None and inbound is None:
        return None
    return int(outbound or 0) + int(inbound or 0)


def kpi_metric_value(report: dict[str, Any], metric_key: str) -> int | float | None:
    traffic = report.get("traffic", {})
    if metric_key == "pv":
        return traffic.get("pv")
    if metric_key == "uv":
        return traffic.get("uv")
    if metric_key == "unique_ips":
        return traffic.get("unique_ips")
    if metric_key == "request_count":
        return traffic.get("request_count")
    if metric_key == "total_traffic_bytes":
        return total_traffic_bytes(report)
    if metric_key == "spider_total":
        return total_spider_count(report)
    return None


def format_kpi_value(metric_key: str, value: int | float | None) -> str:
    if metric_key == "total_traffic_bytes":
        return format_bytes(value)
    return format_number(value)


def build_kpi_comparisons(report: dict[str, Any], previous_summary: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    previous = previous_summary or {}
    comparisons = {}
    for metric_key in ("pv", "uv", "unique_ips", "request_count", "total_traffic_bytes", "spider_total"):
        comparisons[metric_key] = compare_period(
            kpi_metric_value(report, metric_key),
            kpi_metric_value(previous, metric_key),
        )
    return comparisons


def format_compare_subtitle(
    config: dict[str, Any],
    report_kind: str,
    metric_key: str,
    comparison: dict[str, Any] | None,
) -> str:
    if not comparison:
        return t(config, "kpi_compare_na")
    previous = comparison.get("previous")
    ratio = comparison.get("ratio")
    label = compare_label(config, report_kind)
    if previous in (None, 0) and ratio is None:
        return f"{label}: {format_kpi_value(metric_key, previous)}"
    ratio_text = format_percent(ratio) if ratio is not None else "N/A"
    return f"{label}: {format_kpi_value(metric_key, previous)} ({ratio_text})"


def open_database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def resolve_primary_bucket_minutes(config: dict[str, Any]) -> int:
    rollups = config.get("storage", {}).get("rollup_minutes", [10, 60])
    return min(int(value) for value in rollups)


def local_day_window(report_date: dt.date, timezone: dt.tzinfo) -> tuple[dt.datetime, dt.datetime]:
    start_local = dt.datetime(
        report_date.year,
        report_date.month,
        report_date.day,
        tzinfo=timezone,
    )
    return start_local, start_local + dt.timedelta(days=1)


def query_metric_rows(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    start_local: dt.datetime,
    end_local: dt.datetime,
    bucket_minutes: int | None = None,
) -> list[sqlite3.Row]:
    minutes = bucket_minutes if bucket_minutes is not None else resolve_primary_bucket_minutes(config)
    return connection.execute(
        """
        SELECT *
        FROM metric_rollups
        WHERE host_id = ?
          AND site = ?
          AND bucket_minutes = ?
          AND bucket_start >= ?
          AND bucket_start < ?
        ORDER BY bucket_start
        """,
        (
            config["agent"]["host_id"],
            config["agent"]["site"],
            minutes,
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchall()


def query_host_metric_rows(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    start_local: dt.datetime,
    end_local: dt.datetime,
    bucket_minutes: int | None = None,
) -> list[sqlite3.Row]:
    minutes = bucket_minutes if bucket_minutes is not None else resolve_primary_bucket_minutes(config)
    return connection.execute(
        """
        SELECT *
        FROM metric_rollups
        WHERE host_id = ?
          AND site = ?
          AND bucket_minutes = ?
          AND bucket_start >= ?
          AND bucket_start < ?
        ORDER BY bucket_start
        """,
        (
            config["agent"]["host_id"],
            HOST_METRIC_SITE,
            minutes,
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchall()


def query_grouped_counts(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    detail_table: str,
    group_column: str,
    value_column: str,
    start_local: dt.datetime,
    end_local: dt.datetime,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    if not table_exists(connection, detail_table):
        return []
    limit_sql = f" LIMIT {int(limit)}" if limit is not None else ""
    rows = connection.execute(
        f"""
        SELECT d.{group_column} AS item, SUM(d.{value_column}) AS total
        FROM {detail_table} AS d
        INNER JOIN metric_rollups AS m ON m.id = d.rollup_id
        WHERE m.host_id = ?
          AND m.site = ?
          AND m.bucket_minutes = ?
          AND m.bucket_start >= ?
          AND m.bucket_start < ?
        GROUP BY d.{group_column}
        ORDER BY total DESC, item ASC
        {limit_sql}
        """,
        (
            config["agent"]["host_id"],
            config["agent"]["site"],
            resolve_primary_bucket_minutes(config),
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchall()
    return [{"item": str(row["item"]), "count": int(row["total"] or 0)} for row in rows]


def query_grouped_metrics(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    detail_table: str,
    group_column: str,
    metric_columns: dict[str, str],
    start_local: dt.datetime,
    end_local: dt.datetime,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    if not table_exists(connection, detail_table):
        return []
    limit_sql = f" LIMIT {int(limit)}" if limit is not None else ""
    metric_select = ", ".join(
        f"SUM(COALESCE(d.{column_name}, 0)) AS {alias}"
        for alias, column_name in metric_columns.items()
    )
    order_alias = next(iter(metric_columns.keys()))
    rows = connection.execute(
        f"""
        SELECT d.{group_column} AS item, {metric_select}
        FROM {detail_table} AS d
        INNER JOIN metric_rollups AS m ON m.id = d.rollup_id
        WHERE m.host_id = ?
          AND m.site = ?
          AND m.bucket_minutes = ?
          AND m.bucket_start >= ?
          AND m.bucket_start < ?
        GROUP BY d.{group_column}
        ORDER BY {order_alias} DESC, item ASC
        {limit_sql}
        """,
        (
            config["agent"]["host_id"],
            config["agent"]["site"],
            resolve_primary_bucket_minutes(config),
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchall()
    results: list[dict[str, Any]] = []
    for row in rows:
        item = {"item": str(row["item"])}
        for alias in metric_columns:
            item[alias] = int(row[alias] or 0)
        results.append(item)
    return results


def query_distinct_count(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    detail_table: str,
    value_column: str,
    start_local: dt.datetime,
    end_local: dt.datetime,
) -> int | None:
    if not table_exists(connection, detail_table):
        return None
    row = connection.execute(
        f"""
        SELECT COUNT(DISTINCT d.{value_column}) AS total
        FROM {detail_table} AS d
        INNER JOIN metric_rollups AS m ON m.id = d.rollup_id
        WHERE m.host_id = ?
          AND m.site = ?
          AND m.bucket_minutes = ?
          AND m.bucket_start >= ?
          AND m.bucket_start < ?
        """,
        (
            config["agent"]["host_id"],
            config["agent"]["site"],
            resolve_primary_bucket_minutes(config),
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchone()
    return int(row["total"] or 0)


def localized_unknown_region(config: dict[str, Any]) -> str:
    return "未知地区" if report_language(config) == "zh" else "Unknown Region"


def localized_unknown_info(config: dict[str, Any]) -> str:
    return "GeoIP 未配置" if report_language(config) == "zh" else "GeoIP Not Configured"


def resolve_geoip_update_config(config: dict[str, Any]) -> Path | None:
    reports = config.get("notifications", {}).get("reports", {})
    raw_path = str(reports.get("geoip_update_config") or "").strip()
    if raw_path:
        return Path(raw_path).expanduser()
    if DEFAULT_GEOIP_UPDATE_CONFIG.exists():
        return DEFAULT_GEOIP_UPDATE_CONFIG
    return None


def try_geoipupdate_download(path: Path, config: dict[str, Any]) -> bool:
    geoip_conf = resolve_geoip_update_config(config)
    if not geoip_conf or not geoip_conf.exists():
        return False

    binary = shutil.which("geoipupdate")
    if not binary:
        print(
            "[geoip] GeoIP.conf found but geoipupdate is not installed; falling back to public mirror.",
            file=sys.stderr,
            flush=True,
        )
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    print(
        f"[geoip] updating {path.name} with geoipupdate using {geoip_conf}...",
        file=sys.stderr,
        flush=True,
    )
    try:
        result = subprocess.run(
            [binary, "-f", str(geoip_conf), "-d", str(path.parent)],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        print(f"[geoip] geoipupdate execution failed: {exc}", file=sys.stderr, flush=True)
        return False

    if result.returncode != 0:
        stderr_output = (result.stderr or "").strip()
        detail = f" {stderr_output}" if stderr_output else ""
        print(
            f"[geoip] geoipupdate failed with exit code {result.returncode}; falling back to public mirror.{detail}",
            file=sys.stderr,
            flush=True,
        )
        return False

    if path.exists():
        print(f"[geoip] saved to {path}", file=sys.stderr, flush=True)
        return True

    print(
        f"[geoip] geoipupdate completed but {path.name} was not found in {path.parent}; falling back to public mirror.",
        file=sys.stderr,
        flush=True,
    )
    return False


def ensure_geoip_city_db(config: dict[str, Any]) -> Path | None:
    reports = config.get("notifications", {}).get("reports", {})
    raw_path = str(reports.get("geoip_city_db") or "").strip()
    if not raw_path:
        return None

    path = Path(raw_path).expanduser()
    if path.exists():
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    if try_geoipupdate_download(path, config):
        return path

    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        print(f"[geoip] downloading {path.name} from public mirror...", file=sys.stderr, flush=True)
        with urllib.request.urlopen(GEOIP_MIRROR_URL, timeout=30) as response, temp_path.open("wb") as handle:
            total = int(response.headers.get("Content-Length") or 0)
            downloaded = 0
            while True:
                chunk = response.read(1024 * 128)
                if not chunk:
                    break
                handle.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    percent = downloaded / total * 100.0
                    print(
                        f"[geoip] {downloaded}/{total} bytes ({percent:.1f}%)",
                        file=sys.stderr,
                        flush=True,
                    )
                else:
                    print(f"[geoip] {downloaded} bytes downloaded", file=sys.stderr, flush=True)
        temp_path.replace(path)
        print(f"[geoip] saved to {path}", file=sys.stderr, flush=True)
        return path
    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        return None


def resolve_geoip_city_db(config: dict[str, Any]) -> Path | None:
    return ensure_geoip_city_db(config)


def open_geoip_reader(config: dict[str, Any]) -> Any | None:
    db_path = resolve_geoip_city_db(config)
    if not db_path:
        return None
    try:
        import geoip2.database  # type: ignore
    except ImportError:
        return None
    try:
        return geoip2.database.Reader(str(db_path))
    except Exception:
        return None


def geoip_describe_ip(config: dict[str, Any], ip_address: str, reader: Any | None = None) -> tuple[str, str]:
    unknown_region = localized_unknown_region(config)
    unknown_info = localized_unknown_info(config)
    if reader is None:
        return unknown_region, unknown_info
    try:
        record = reader.city(ip_address)
    except Exception:
        return unknown_region, unknown_info

    language = "zh-CN" if report_language(config) == "zh" else "en"
    country = record.country.names.get(language) or record.country.name or ""
    region = (
        record.subdivisions.most_specific.names.get(language)
        if record.subdivisions
        else ""
    ) or (
        record.city.names.get(language)
        if record.city
        else ""
    ) or country
    if not region:
        region = unknown_region
    info_parts = [part for part in (country, region) if part]
    info = " / ".join(dict.fromkeys(info_parts)) if info_parts else unknown_info
    return region, info


def enrich_ip_rows_with_geo(
    config: dict[str, Any],
    ip_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reader = open_geoip_reader(config)
    enriched_rows: list[dict[str, Any]] = []
    province_aggregate: dict[str, dict[str, Any]] = {}
    for row in ip_rows:
        ip_address = str(row.get("item") or "-")
        region, info = geoip_describe_ip(config, ip_address, reader)
        enriched_rows.append(
            {
                "item": ip_address,
                "request_count": int(row.get("request_count") or row.get("count") or 0),
                "bytes_out": int(row.get("bytes_out") or 0),
                "region": region,
                "info": info,
            }
        )
        entry = province_aggregate.setdefault(
            region,
            {"item": region, "request_count": 0, "ip_set": set()},
        )
        entry["request_count"] += int(row.get("request_count") or row.get("count") or 0)
        entry["ip_set"].add(ip_address)

    province_rows = [
        {
            "item": key,
            "request_count": value["request_count"],
            "unique_ips": len(value["ip_set"]),
        }
        for key, value in province_aggregate.items()
    ]
    if reader is not None:
        try:
            reader.close()
        except Exception:
            pass
    province_rows.sort(key=lambda item: (-int(item["request_count"]), str(item["item"])))
    return enriched_rows, province_rows


def resolve_ssl_target(config: dict[str, Any]) -> dict[str, Any]:
    agent = config.get("agent", {})
    raw_site = str(agent.get("site") or agent.get("site_host") or "").strip()
    if not raw_site:
        return {"source": "", "scheme": "https", "hostname": "", "port": 443}

    parsed = urlparse(raw_site if "://" in raw_site else f"https://{raw_site}")
    hostname = parsed.hostname or raw_site.split("/")[0]
    scheme = (parsed.scheme or "https").lower()
    if scheme == "http":
        port = parsed.port or 80
    else:
        scheme = "https"
        port = parsed.port or 443
    return {
        "source": raw_site,
        "scheme": scheme,
        "hostname": hostname,
        "port": port,
    }


def check_ssl_expiry(config: dict[str, Any], timeout_seconds: int = 5) -> dict[str, Any]:
    target = resolve_ssl_target(config)
    hostname = str(target.get("hostname") or "").strip()
    scheme = str(target.get("scheme") or "https").lower()
    port = int(target.get("port") or (443 if scheme == "https" else 80))
    if not hostname or scheme != "https":
        return {
            "hostname": hostname,
            "port": port,
            "scheme": scheme,
            "days_remaining": None,
            "status": "na",
            "error": None,
        }

    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=timeout_seconds) as tcp_socket:
            with context.wrap_socket(tcp_socket, server_hostname=hostname) as tls_socket:
                certificate = tls_socket.getpeercert()
        expires_raw = str(certificate.get("notAfter") or "").strip()
        if not expires_raw:
            raise ValueError("certificate missing notAfter")
        expires_at = dt.datetime.strptime(expires_raw, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
        seconds_remaining = (expires_at - dt.datetime.now(dt.timezone.utc)).total_seconds()
        days_remaining = math.floor(seconds_remaining / 86400)
        status = "expired" if days_remaining < 0 else "warning" if days_remaining < SSL_WARNING_DAYS else "ok"
        return {
            "hostname": hostname,
            "port": port,
            "scheme": scheme,
            "days_remaining": days_remaining,
            "status": status,
            "expires_at": expires_at.isoformat(),
            "error": None,
        }
    except Exception as exc:
        return {
            "hostname": hostname,
            "port": port,
            "scheme": scheme,
            "days_remaining": None,
            "status": "na",
            "error": str(exc),
        }


def format_ssl_summary_text(config: dict[str, Any], ssl_info: dict[str, Any]) -> str:
    language = report_language(config)
    days_remaining = ssl_info.get("days_remaining")
    status = str(ssl_info.get("status") or "na")
    if days_remaining is None or status == "na":
        return "N/A"
    if status == "expired":
        return f"已过期 {abs(int(days_remaining))} 天" if language == "zh" else f"Expired {abs(int(days_remaining))} days"
    return f"{int(days_remaining)} 天" if language == "zh" else f"{int(days_remaining)} days"


def format_ssl_markdown_line(config: dict[str, Any], ssl_info: dict[str, Any]) -> str:
    label = t(config, "ssl_remaining")
    status = str(ssl_info.get("status") or "na")
    summary = format_ssl_summary_text(config, ssl_info)
    if status in {"warning", "expired"}:
        return f"⚠️ {label}: {summary}"
    return f"�� {label}: {summary}"


def aggregate_status_families(status_codes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for entry in status_codes:
        code = str(entry["item"])
        family = f"{code[0]}xx" if code and code[0].isdigit() else "other"
        counts[family] = counts.get(family, 0) + int(entry["count"])
    return [
        {"item": key, "count": value}
        for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def build_status_chart_data(status_codes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = {"200": 0, "404": 0, "5xx": 0, "other": 0}
    for entry in status_codes:
        code = str(entry["item"])
        count = int(entry["count"])
        if code == "200":
            counts["200"] += count
        elif code == "404":
            counts["404"] += count
        elif code.startswith("5"):
            counts["5xx"] += count
        else:
            counts["other"] += count
    return [{"item": key, "count": value} for key, value in counts.items() if value > 0]


def build_spider_chart_data(spiders: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    if not spiders:
        return []
    result = [{"item": row["item"], "count": int(row["count"])} for row in spiders[:limit]]
    other = sum(int(row["count"]) for row in spiders[limit:])
    if other:
        result.append({"item": "other", "count": other})
    return result


def sum_metric_rows(rows: list[sqlite3.Row], column: str) -> int:
    return sum(int(row[column] or 0) for row in rows)


def mean_metric_rows(rows: list[sqlite3.Row], column: str) -> float | None:
    values = [float(row[column]) for row in rows if row[column] is not None]
    return round(sum(values) / len(values), 2) if values else None


def max_metric_rows(rows: list[sqlite3.Row], column: str) -> float | None:
    values = [float(row[column]) for row in rows if row[column] is not None]
    return round(max(values), 2) if values else None


def min_metric_rows(rows: list[sqlite3.Row], column: str) -> int | None:
    values = [int(row[column]) for row in rows if row[column] is not None]
    return min(values) if values else None


def query_hourly_series(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    report_date: dt.date,
) -> list[dict[str, Any]]:
    timezone = get_timezone(config)
    start_local, end_local = local_day_window(report_date, timezone)
    rows = connection.execute(
        """
        SELECT
            substr(bucket_start, 12, 2) AS hour_slot,
            SUM(pv) AS pv,
            SUM(uv) AS uv,
            SUM(unique_ips) AS unique_ips,
            SUM(request_count) AS request_count,
            MAX(qps) AS peak_qps,
            AVG(avg_response_ms) AS avg_response_ms,
            SUM(slow_request_count) AS slow_request_count,
            SUM(COALESCE(bandwidth_out_bytes, 0)) AS bandwidth_out_bytes,
            SUM(COALESCE(bandwidth_in_bytes, 0)) AS bandwidth_in_bytes
        FROM metric_rollups
        WHERE host_id = ?
          AND site = ?
          AND bucket_minutes = ?
          AND bucket_start >= ?
          AND bucket_start < ?
        GROUP BY substr(bucket_start, 12, 2)
        ORDER BY hour_slot
        """,
        (
            config["agent"]["host_id"],
            config["agent"]["site"],
            resolve_primary_bucket_minutes(config),
            start_local.isoformat(),
            end_local.isoformat(),
        ),
    ).fetchall()
    mapped = {int(row["hour_slot"]): row for row in rows if row["hour_slot"] is not None}
    series = []
    for hour in range(24):
        row = mapped.get(hour)
        series.append(
            {
                "hour": hour,
                "pv": int(row["pv"] or 0) if row else 0,
                "uv": int(row["uv"] or 0) if row else 0,
                "unique_ips": int(row["unique_ips"] or 0) if row else 0,
                "request_count": int(row["request_count"] or 0) if row else 0,
                "peak_qps": float(row["peak_qps"] or 0.0) if row else 0.0,
                "avg_response_ms": round(float(row["avg_response_ms"]), 2)
                if row and row["avg_response_ms"] is not None
                else None,
                "slow_request_count": int(row["slow_request_count"] or 0) if row else 0,
                "bandwidth_out_bytes": int(row["bandwidth_out_bytes"] or 0) if row else 0,
                "bandwidth_in_bytes": int(row["bandwidth_in_bytes"] or 0) if row else 0,
            }
        )
    return series


def daily_summary(connection: sqlite3.Connection, config: dict[str, Any], report_date: dt.date) -> dict[str, Any]:
    timezone = get_timezone(config)
    start_local, end_local = local_day_window(report_date, timezone)
    rows = query_metric_rows(connection, config, start_local, end_local)
    host_rows = query_host_metric_rows(connection, config, start_local, end_local)
    fallback_rows = query_metric_rows(
        connection,
        config,
        start_local,
        end_local,
        max(config.get("storage", {}).get("rollup_minutes", [resolve_primary_bucket_minutes(config)])),
    )

    exact_uv = query_distinct_count(connection, config, "visitor_rollups", "visitor_hash", start_local, end_local)
    exact_ips = query_distinct_count(connection, config, "client_ip_rollups", "client_ip", start_local, end_local)
    status_codes = query_grouped_counts(
        connection,
        config,
        "status_code_rollups",
        "status_code",
        "request_count",
        start_local,
        end_local,
    )
    top_errors = query_grouped_counts(
        connection,
        config,
        "error_fingerprint_rollups",
        "fingerprint",
        "error_count",
        start_local,
        end_local,
        10,
    )
    if not top_errors:
        top_errors = query_grouped_counts(
            connection,
            config,
            "error_category_rollups",
            "category",
            "error_count",
            start_local,
            end_local,
            10,
        )
    top_uri_details = query_grouped_metrics(
        connection,
        config,
        "uri_detail_rollups",
        "uri",
        {"request_count": "request_count", "uv_count": "uv_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        10,
    )
    top_sources = query_grouped_metrics(
        connection,
        config,
        "source_rollups",
        "source_name",
        {"request_count": "request_count", "uv_count": "uv_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        10,
    )
    raw_top_client_ips = query_grouped_metrics(
        connection,
        config,
        "client_ip_request_rollups",
        "client_ip",
        {"request_count": "request_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        50,
    )
    top_client_ips, province_distribution = enrich_ip_rows_with_geo(config, raw_top_client_ips)
    client_families = query_grouped_metrics(
        connection,
        config,
        "client_family_rollups",
        "client_family",
        {"request_count": "request_count"},
        start_local,
        end_local,
        12,
    )

    return {
        "meta": {
            "report_kind": "daily",
            "report_date": report_date.isoformat(),
            "window_start": start_local.isoformat(),
            "window_end": end_local.isoformat(),
            "host_id": config["agent"]["host_id"],
            "site": config["agent"]["site"],
            "bucket_minutes": resolve_primary_bucket_minutes(config),
        },
        "traffic": {
            "pv": sum_metric_rows(rows, "pv"),
            "request_count": sum_metric_rows(rows, "request_count"),
            "uv": exact_uv if exact_uv is not None else sum_metric_rows(fallback_rows or rows, "uv"),
            "uv_is_estimate": exact_uv is None,
            "unique_ips": exact_ips if exact_ips is not None else sum_metric_rows(fallback_rows or rows, "unique_ips"),
            "unique_ips_is_estimate": exact_ips is None,
            "qps_peak": max((float(row["qps"] or 0.0) for row in rows), default=0.0),
            "avg_response_ms": mean_metric_rows(rows, "avg_response_ms"),
            "slow_request_count": sum_metric_rows(rows, "slow_request_count"),
            "bandwidth_out_bytes": sum_metric_rows(rows, "bandwidth_out_bytes"),
            "bandwidth_in_bytes": sum(
                int(row["bandwidth_in_bytes"]) for row in rows if row["bandwidth_in_bytes"] is not None
            )
            if any(row["bandwidth_in_bytes"] is not None for row in rows)
            else None,
        },
        "system": {
            "avg_cpu_pct": mean_metric_rows(host_rows, "avg_cpu_pct"),
            "max_cpu_pct": max_metric_rows(host_rows, "max_cpu_pct"),
            "avg_memory_pct": mean_metric_rows(host_rows, "avg_memory_pct"),
            "max_memory_pct": max_metric_rows(host_rows, "max_memory_pct"),
            "min_disk_free_bytes": min_metric_rows(host_rows, "min_disk_free_bytes"),
        },
        "status_codes": status_codes,
        "status_families": aggregate_status_families(status_codes),
        "top_errors": top_errors,
        "top_uris": query_grouped_counts(
            connection,
            config,
            "uri_rollups",
            "uri",
            "request_count",
            start_local,
            end_local,
            10,
        ),
        "top_uri_details": top_uri_details,
        "top_sources": top_sources,
        "top_client_ips": top_client_ips[:10],
        "province_distribution": province_distribution[:10],
        "client_families": client_families,
        "spiders": query_grouped_counts(
            connection,
            config,
            "spider_rollups",
            "spider_family",
            "request_count",
            start_local,
            end_local,
            8,
        ),
        "slow_routes": query_grouped_counts(
            connection,
            config,
            "slow_request_rollups",
            "uri",
            "slow_request_count",
            start_local,
            end_local,
            10,
        ),
        "abnormal_ips": query_grouped_counts(
            connection,
            config,
            "suspicious_ip_rollups",
            "client_ip",
            "max_requests_per_minute",
            start_local,
            end_local,
            10,
        ),
        "hourly_series": query_hourly_series(connection, config, report_date),
        "errors_total": sum_metric_rows(rows, "total_errors"),
        "security": {
            "suspicious_ip_count": len({item["item"] for item in raw_top_client_ips}),
            "http_404_count": next((int(item["count"]) for item in status_codes if item["item"] == "404"), 0),
            "http_5xx_count": sum(int(item["count"]) for item in status_codes if str(item["item"]).startswith("5")),
        },
    }


def compare_period(current: int | float | None, previous: int | float | None) -> dict[str, Any]:
    if current is None or previous is None:
        return {"current": current, "previous": previous, "delta": None, "ratio": None}
    delta = float(current) - float(previous)
    ratio = None if previous == 0 else (delta / float(previous)) * 100.0
    return {"current": current, "previous": previous, "delta": delta, "ratio": ratio}


def build_date_window(end_date: dt.date, days: int, timezone: dt.tzinfo) -> tuple[dt.datetime, dt.datetime, list[dt.date]]:
    start_date = end_date - dt.timedelta(days=days - 1)
    dates = [start_date + dt.timedelta(days=offset) for offset in range(days)]
    start_local = dt.datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone)
    end_local = dt.datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone) + dt.timedelta(days=1)
    return start_local, end_local, dates


def period_summary(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    report_kind: str,
    end_date: dt.date,
    include_compare: bool = True,
) -> dict[str, Any]:
    timezone = get_timezone(config)
    if report_kind == "daily":
        return daily_summary(connection, config, end_date)

    days = 7 if report_kind == "weekly" else 30
    start_local, end_local, dates = build_date_window(end_date, days, timezone)
    rows = query_metric_rows(connection, config, start_local, end_local)
    host_rows = query_host_metric_rows(connection, config, start_local, end_local)
    exact_uv = query_distinct_count(connection, config, "visitor_rollups", "visitor_hash", start_local, end_local)
    exact_ips = query_distinct_count(connection, config, "client_ip_rollups", "client_ip", start_local, end_local)

    daily_items = [daily_summary(connection, config, item) for item in dates]
    traffic_series = [
        {
            "date": item["meta"]["report_date"],
            "pv": int(item["traffic"]["pv"] or 0),
            "uv": int(item["traffic"]["uv"] or 0),
            "unique_ips": int(item["traffic"]["unique_ips"] or 0),
            "request_count": int(item["traffic"]["request_count"] or 0),
            "errors_total": int(item["errors_total"] or 0),
            "avg_response_ms": float(item["traffic"]["avg_response_ms"] or 0.0),
            "slow_request_count": int(item["traffic"]["slow_request_count"] or 0),
            "bandwidth_out_bytes": int(item["traffic"]["bandwidth_out_bytes"] or 0),
            "bandwidth_in_bytes": int(item["traffic"]["bandwidth_in_bytes"] or 0),
            "spider_total": total_spider_count(item),
            "http_404_count": int(item.get("security", {}).get("http_404_count") or 0),
            "http_5xx_count": int(item.get("security", {}).get("http_5xx_count") or 0),
            "cpu_peak": item["system"]["max_cpu_pct"],
            "memory_peak": item["system"]["max_memory_pct"],
            "disk_free_bytes": item["system"]["min_disk_free_bytes"],
        }
        for item in daily_items
    ]
    spider_daily_series = [
        {
            "date": item["meta"]["report_date"],
            "counts": {
                str(row["item"]): int(row["count"] or 0)
                for row in (item.get("spiders") or [])
            },
        }
        for item in daily_items
    ]
    status_family_series = [
        {
            "date": item["meta"]["report_date"],
            "counts": {
                str(row["item"]): int(row["count"] or 0)
                for row in aggregate_status_families(item.get("status_codes") or [])
            },
        }
        for item in daily_items
    ]

    status_codes = query_grouped_counts(
        connection,
        config,
        "status_code_rollups",
        "status_code",
        "request_count",
        start_local,
        end_local,
    )
    spiders = query_grouped_counts(
        connection,
        config,
        "spider_rollups",
        "spider_family",
        "request_count",
        start_local,
        end_local,
        8,
    )
    suspicious_ips = query_grouped_counts(
        connection,
        config,
        "suspicious_ip_rollups",
        "client_ip",
        "max_requests_per_minute",
        start_local,
        end_local,
        10,
    )
    top_errors = query_grouped_counts(
        connection,
        config,
        "error_fingerprint_rollups",
        "fingerprint",
        "error_count",
        start_local,
        end_local,
        10,
    )
    top_uris = query_grouped_counts(
        connection,
        config,
        "uri_rollups",
        "uri",
        "request_count",
        start_local,
        end_local,
        10,
    )
    slow_routes = query_grouped_counts(
        connection,
        config,
        "slow_request_rollups",
        "uri",
        "slow_request_count",
        start_local,
        end_local,
        10,
    )
    top_uri_details = query_grouped_metrics(
        connection,
        config,
        "uri_detail_rollups",
        "uri",
        {"request_count": "request_count", "uv_count": "uv_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        10,
    )
    top_sources = query_grouped_metrics(
        connection,
        config,
        "source_rollups",
        "source_name",
        {"request_count": "request_count", "uv_count": "uv_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        10,
    )
    raw_top_client_ips = query_grouped_metrics(
        connection,
        config,
        "client_ip_request_rollups",
        "client_ip",
        {"request_count": "request_count", "bytes_out": "bytes_out"},
        start_local,
        end_local,
        50,
    )
    top_client_ips, province_distribution = enrich_ip_rows_with_geo(config, raw_top_client_ips)
    client_families = query_grouped_metrics(
        connection,
        config,
        "client_family_rollups",
        "client_family",
        {"request_count": "request_count"},
        start_local,
        end_local,
        12,
    )

    previous_summary = None
    wow = {}
    if report_kind in {"weekly", "monthly"} and include_compare:
        previous_end = end_date - dt.timedelta(days=days)
        previous_summary = period_summary(
            connection,
            config,
            report_kind,
            previous_end,
            include_compare=False,
        )
        wow = {
            "pv": compare_period(sum_metric_rows(rows, "pv"), previous_summary["traffic"]["pv"]),
            "uv": compare_period(
                exact_uv if exact_uv is not None else sum(item["traffic"]["uv"] for item in daily_items),
                previous_summary["traffic"]["uv"],
            ),
            "request_count": compare_period(sum_metric_rows(rows, "request_count"), previous_summary["traffic"]["request_count"]),
            "errors_total": compare_period(sum_metric_rows(rows, "total_errors"), previous_summary["errors_total"]),
        }

    pv_total = sum_metric_rows(rows, "pv")
    request_total = sum_metric_rows(rows, "request_count")
    return {
        "meta": {
            "report_kind": report_kind,
            "report_date": end_date.isoformat(),
            "window_start": start_local.isoformat(),
            "window_end": end_local.isoformat(),
            "host_id": config["agent"]["host_id"],
            "site": config["agent"]["site"],
            "bucket_minutes": resolve_primary_bucket_minutes(config),
            "days": days,
        },
        "traffic": {
            "pv": pv_total,
            "request_count": request_total,
            "uv": exact_uv if exact_uv is not None else sum(item["traffic"]["uv"] for item in daily_items),
            "uv_is_estimate": exact_uv is None,
            "unique_ips": exact_ips if exact_ips is not None else sum(item["traffic"]["unique_ips"] for item in daily_items),
            "unique_ips_is_estimate": exact_ips is None,
            "qps_peak": max((float(row["qps"] or 0.0) for row in rows), default=0.0),
            "avg_response_ms": mean_metric_rows(rows, "avg_response_ms"),
            "slow_request_count": sum_metric_rows(rows, "slow_request_count"),
            "bandwidth_out_bytes": sum_metric_rows(rows, "bandwidth_out_bytes"),
            "bandwidth_in_bytes": sum(
                int(row["bandwidth_in_bytes"]) for row in rows if row["bandwidth_in_bytes"] is not None
            )
            if any(row["bandwidth_in_bytes"] is not None for row in rows)
            else None,
            "cpu_peak": max_metric_rows(host_rows, "max_cpu_pct"),
            "memory_peak": max_metric_rows(host_rows, "max_memory_pct"),
            "disk_free_min": min_metric_rows(host_rows, "min_disk_free_bytes"),
        },
        "status_codes": status_codes,
        "status_families": aggregate_status_families(status_codes),
        "spiders": spiders,
        "top_errors": top_errors,
        "top_uris": top_uris,
        "top_uri_details": top_uri_details,
        "top_sources": top_sources,
        "top_client_ips": top_client_ips[:10],
        "province_distribution": province_distribution[:10],
        "client_families": client_families,
        "slow_routes": slow_routes,
        "abnormal_ips": suspicious_ips,
        "traffic_series": traffic_series,
        "spider_daily_series": spider_daily_series,
        "status_family_series": status_family_series,
        "errors_total": sum_metric_rows(rows, "total_errors"),
        "wow": wow,
        "previous_summary": previous_summary,
        "security": {
            "suspicious_ip_count": len({item["item"] for item in suspicious_ips}),
            "http_404_count": next((int(item["count"]) for item in status_codes if item["item"] == "404"), 0),
            "http_5xx_count": sum(int(item["count"]) for item in status_codes if str(item["item"]).startswith("5")),
        },
    }


def resolve_ai_settings(config: dict[str, Any]) -> dict[str, Any]:
    reports = config.get("notifications", {}).get("reports", {})
    ai_settings = dict(reports.get("ai_analysis") or {})
    return {
        "enabled": bool(ai_settings.get("enabled", True)),
        "simulate": bool(ai_settings.get("simulate", False)),
        "endpoint": str(ai_settings.get("endpoint") or ai_settings.get("base_url") or "").strip(),
        "model": str(ai_settings.get("model") or "gpt-4o-mini").strip(),
        "api_key_env": str(ai_settings.get("api_key_env") or "OPENAI_API_KEY").strip(),
        "timeout_seconds": max(int(ai_settings.get("timeout_seconds", 20)), 3),
    }


def ai_analysis_payload(report: dict[str, Any]) -> dict[str, Any]:
    top_error = report.get("top_errors", [{}])[0] if report.get("top_errors") else {}
    traffic = report.get("traffic", {})
    return {
        "report_kind": report["meta"]["report_kind"],
        "site": report["meta"]["site"],
        "host_id": report["meta"]["host_id"],
        "window_start": report["meta"]["window_start"],
        "window_end": report["meta"]["window_end"],
        "pv": traffic.get("pv"),
        "uv": traffic.get("uv"),
        "unique_ips": traffic.get("unique_ips"),
        "request_count": traffic.get("request_count"),
        "total_traffic_gb": round((total_traffic_bytes(report) or 0) / (1024 ** 3), 2),
        "spider_total": total_spider_count(report),
        "qps_peak": traffic.get("qps_peak"),
        "avg_response_ms": traffic.get("avg_response_ms"),
        "slow_request_count": traffic.get("slow_request_count"),
        "cpu_peak_pct": traffic.get("cpu_peak", report.get("system", {}).get("max_cpu_pct")),
        "memory_peak_pct": traffic.get("memory_peak", report.get("system", {}).get("max_memory_pct")),
        "disk_free_gb": round((traffic.get("disk_free_min", report.get("system", {}).get("min_disk_free_bytes")) or 0) / (1024 ** 3), 2),
        "http_404_count": report.get("security", {}).get("http_404_count", 0),
        "http_5xx_count": report.get("security", {}).get("http_5xx_count", 0),
        "suspicious_ip_count": report.get("security", {}).get("suspicious_ip_count", 0),
        "top_error_fingerprint": top_error.get("item"),
        "top_error_count": top_error.get("count"),
    }


def ai_analysis_prompt(config: dict[str, Any], payload: dict[str, Any]) -> str:
    language = report_language(config)
    if language == "en":
        return (
            "You are a senior site reliability engineer. Based on the following aggregated server metrics, "
            "write a 100-150 word health summary and 1-2 actionable recommendations. Focus on risk, trend, "
            "and next actions. Avoid sensitive data.\n\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )
    return (
        "你是一名资深运维专家。请根据以下服务器周期汇总数据，用100-150字输出一段专业的健康度综合分析，"
        "并补充1-2条排查或优化建议。请聚焦风险、趋势和下一步动作，避免输出敏感信息。\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def request_ai_analysis(config: dict[str, Any], payload: dict[str, Any]) -> str | None:
    settings = resolve_ai_settings(config)
    if not settings["enabled"] or settings["simulate"] or not settings["endpoint"]:
        return None
    api_key = os.getenv(settings["api_key_env"])
    if not api_key:
        return None
    endpoint = settings["endpoint"].rstrip("/")
    if endpoint.endswith("/v1"):
        endpoint = endpoint + "/chat/completions"
    elif not endpoint.endswith("/chat/completions"):
        endpoint = endpoint + "/chat/completions"
    body = {
        "model": settings["model"],
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": "You are an expert SRE assistant."},
            {"role": "user", "content": ai_analysis_prompt(config, payload)},
        ],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=settings["timeout_seconds"]) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        return None


def simulated_ai_analysis(config: dict[str, Any], report: dict[str, Any], payload: dict[str, Any]) -> str:
    language = report_language(config)
    traffic = report["traffic"]
    signals = []
    recommendations = []
    if payload["http_5xx_count"] >= 20:
        signals.append("5xx 错误偏高" if language == "zh" else "5xx errors are elevated")
        recommendations.append("优先检查上游服务和 PHP-FPM/Nginx 连接池" if language == "zh" else "Inspect upstream services and PHP-FPM/Nginx pools first")
    if (traffic.get("avg_response_ms") or 0) > 1500 or (traffic.get("slow_request_count") or 0) > 200:
        signals.append("响应时延出现明显压力" if language == "zh" else "latency pressure is visible")
        recommendations.append("关注慢路由 Top10，定位数据库或外部依赖瓶颈" if language == "zh" else "Review slow-route Top 10 for database or upstream bottlenecks")
    if (payload["cpu_peak_pct"] or 0) > 85:
        signals.append("CPU 峰值接近阈值" if language == "zh" else "CPU peak is near the alert threshold")
        recommendations.append("建议复核定时任务与突发流量时段" if language == "zh" else "Recheck cron jobs and burst traffic windows")
    if (payload["http_404_count"] or 0) > 200:
        signals.append("404 扫描请求较多" if language == "zh" else "404 probing traffic is notable")
        recommendations.append("排查恶意扫描并完善黑名单或 WAF 规则" if language == "zh" else "Review scanner activity and tighten blacklist or WAF rules")
    if not signals:
        signals.append("整体运行平稳，核心吞吐与资源水位处于可控区间" if language == "zh" else "overall service health is stable and resource usage remains controlled")
        recommendations.append("继续观察高峰时段趋势并保留当前阈值策略" if language == "zh" else "Continue monitoring peak windows and keep current alert thresholds")
    top_error = payload.get("top_error_fingerprint") or ("暂无突出错误" if language == "zh" else "no dominant error")
    if language == "en":
        return (
            f"This period handled {format_number(payload['request_count'])} requests with {format_number(payload['pv'])} PV and "
            f"{format_number(payload['spider_total'])} crawler hits. The service shows {signals[0]}; peak QPS was "
            f"{format_number(payload['qps_peak'], 2)} and average latency stayed near {format_number(payload['avg_response_ms'])} ms. "
            f"The main error fingerprint was {top_error}. Recommendations: {recommendations[0]}."
        )
    return (
        f"本周期共处理 {format_number(payload['request_count'])} 次请求，浏览量 {format_number(payload['pv'])}，蜘蛛抓取 {format_number(payload['spider_total'])} 次。"
        f"整体来看，{signals[0]}；峰值 QPS 为 {format_number(payload['qps_peak'], 2)}，平均响应约 {format_number(payload['avg_response_ms'])} ms，"
        f"主要错误指纹为 {top_error}。建议：{recommendations[0]}。"
    )


def attach_ai_analysis(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    payload = ai_analysis_payload(report)
    ai_text = request_ai_analysis(config, payload)
    source = "llm"
    if not ai_text:
        ai_text = simulated_ai_analysis(config, report, payload)
        source = "simulated"
    report["ai_analysis"] = {
        "summary": ai_text,
        "payload": payload,
        "source": source,
    }
    return report


def prepare_report(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    report_kind: str,
    report_date: dt.date,
) -> dict[str, Any]:
    if report_kind == "daily":
        report = daily_summary(connection, config, report_date)
        previous_summary = daily_summary(connection, config, report_date - dt.timedelta(days=1))
    else:
        report = period_summary(connection, config, report_kind, report_date)
        previous_summary = report.get("previous_summary")
        if previous_summary is None:
            previous_summary = period_summary(
                connection,
                config,
                report_kind,
                report_date - dt.timedelta(days=report_span_days(report_kind)),
                include_compare=False,
            )
    report["previous_summary"] = previous_summary
    report["compare_label"] = compare_label(config, report_kind)
    report["kpi_comparisons"] = build_kpi_comparisons(report, previous_summary)
    report["ssl"] = check_ssl_expiry(config)
    return attach_ai_analysis(report, config)


def security_snapshot(report: dict[str, Any]) -> dict[str, int]:
    security = dict(report.get("security") or {})
    status_codes = report.get("status_codes", [])
    if "http_404_count" not in security:
        security["http_404_count"] = next(
            (int(item["count"]) for item in status_codes if str(item["item"]) == "404"),
            0,
        )
    if "http_5xx_count" not in security:
        security["http_5xx_count"] = sum(
            int(item["count"]) for item in status_codes if str(item["item"]).startswith("5")
        )
    if "suspicious_ip_count" not in security:
        security["suspicious_ip_count"] = len(report.get("abnormal_ips", []))
    return security


def ai_analysis_payload(report: dict[str, Any]) -> dict[str, Any]:
    security = security_snapshot(report)
    top_error = report.get("top_errors", [{}])[0] if report.get("top_errors") else {}
    traffic = report.get("traffic", {})
    system = report.get("system", {})
    return {
        "report_kind": report["meta"]["report_kind"],
        "site": report["meta"]["site"],
        "host_id": report["meta"]["host_id"],
        "window_start": report["meta"]["window_start"],
        "window_end": report["meta"]["window_end"],
        "pv": traffic.get("pv"),
        "uv": traffic.get("uv"),
        "unique_ips": traffic.get("unique_ips"),
        "request_count": traffic.get("request_count"),
        "total_traffic_gb": round((total_traffic_bytes(report) or 0) / (1024 ** 3), 2),
        "spider_total": total_spider_count(report),
        "qps_peak": traffic.get("qps_peak"),
        "avg_response_ms": traffic.get("avg_response_ms"),
        "slow_request_count": traffic.get("slow_request_count"),
        "cpu_peak_pct": traffic.get("cpu_peak", system.get("max_cpu_pct")),
        "memory_peak_pct": traffic.get("memory_peak", system.get("max_memory_pct")),
        "disk_free_gb": round(
            (
                traffic.get("disk_free_min", system.get("min_disk_free_bytes"))
                or 0
            )
            / (1024 ** 3),
            2,
        ),
        "http_404_count": security["http_404_count"],
        "http_5xx_count": security["http_5xx_count"],
        "suspicious_ip_count": security["suspicious_ip_count"],
        "top_error_fingerprint": top_error.get("item"),
        "top_error_count": top_error.get("count"),
        "ssl_days_remaining": (report.get("ssl") or {}).get("days_remaining"),
        "ssl_status": (report.get("ssl") or {}).get("status"),
    }


def ai_analysis_prompt(config: dict[str, Any], payload: dict[str, Any]) -> str:
    language = report_language(config)
    if language == "en":
        return (
            "You are a senior site reliability engineer. Based on the following aggregated "
            "server metrics, write a 100-150 word health summary and 1-2 actionable "
            "recommendations. Focus on risk, trend, and next actions. Avoid sensitive data.\n\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )
    return (
        "你是一名资深运维专家。请基于以下服务器周期汇总指标，输出 100-150 字的健康度综合分析，"
        "并给出 1-2 条具体的排查或优化建议。请重点关注风险、趋势和下一步动作，不要输出敏感信息。\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def simulated_ai_analysis(config: dict[str, Any], report: dict[str, Any], payload: dict[str, Any]) -> str:
    language = report_language(config)
    traffic = report["traffic"]
    signals: list[str] = []
    recommendations: list[str] = []

    if payload["http_5xx_count"] >= 20:
        signals.append("5xx 错误偏高" if language == "zh" else "5xx errors are elevated")
        recommendations.append(
            "优先检查上游服务、PHP-FPM 与 Nginx 连接池状态"
            if language == "zh"
            else "Inspect upstream services and PHP-FPM/Nginx pools first"
        )
    if (traffic.get("avg_response_ms") or 0) > 1500 or (traffic.get("slow_request_count") or 0) > 200:
        signals.append("存在明显的延迟压力" if language == "zh" else "latency pressure is visible")
        recommendations.append(
            "优先排查慢响应路由 Top 10，定位数据库或上游瓶颈"
            if language == "zh"
            else "Review the slow-route Top 10 for database or upstream bottlenecks"
        )
    if (payload["cpu_peak_pct"] or 0) > 85:
        signals.append("CPU 峰值逼近告警阈值" if language == "zh" else "CPU peak is near the alert threshold")
        recommendations.append(
            "复查定时任务与突发流量时间窗，确认是否存在短时资源抢占"
            if language == "zh"
            else "Recheck cron jobs and burst traffic windows for short spikes"
        )
    if (payload["http_404_count"] or 0) > 200:
        signals.append("404 扫描流量较为明显" if language == "zh" else "404 probing traffic is notable")
        recommendations.append(
            "检查扫描来源并收紧黑名单或 WAF 规则"
            if language == "zh"
            else "Review scanner activity and tighten blacklist or WAF rules"
        )
    if not signals:
        signals.append(
            "整体服务健康，资源占用处于可控范围"
            if language == "zh"
            else "overall service health is stable and resource usage remains controlled"
        )
        recommendations.append(
            "继续关注业务高峰窗口，并维持当前告警阈值策略"
            if language == "zh"
            else "Continue monitoring peak windows and keep the current alert thresholds"
        )

    top_error = payload.get("top_error_fingerprint") or (
        "暂无主导错误" if language == "zh" else "no dominant error"
    )
    if language == "en":
        return (
            f"This period handled {format_number(payload['request_count'])} requests with "
            f"{format_number(payload['pv'])} PV and {format_number(payload['spider_total'])} crawler hits. "
            f"The service shows {signals[0]}; peak QPS reached {format_number(payload['qps_peak'], 2)} and "
            f"average latency stayed near {format_number(payload['avg_response_ms'])} ms. "
            f"The main error fingerprint was {top_error}. Recommendation: {recommendations[0]}."
        )
    return (
        f"本周期共处理 {format_number(payload['request_count'])} 次请求，浏览量 {format_number(payload['pv'])}，"
        f"蜘蛛抓取 {format_number(payload['spider_total'])} 次。当前整体表现为{signals[0]}，峰值 QPS 达到 "
        f"{format_number(payload['qps_peak'], 2)}，平均响应约 {format_number(payload['avg_response_ms'])} ms。"
        f"主要错误指纹为 {top_error}。建议：{recommendations[0]}。"
    )


def attach_ai_analysis(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    payload = ai_analysis_payload(report)
    ai_text = request_ai_analysis(config, payload)
    source = "llm"
    if not ai_text:
        ai_text = simulated_ai_analysis(config, report, payload)
        source = "simulated"
    report["ai_analysis"] = {
        "summary": ai_text,
        "payload": payload,
        "source": source,
    }
    return report


def render_daily_markdown(report: dict[str, Any], config: dict[str, Any]) -> str:
    meta = report["meta"]
    traffic = report["traffic"]
    system = report["system"]
    ssl_info = report.get("ssl") or {}
    total_requests = max(int(traffic["request_count"] or 0), 1)
    lines = [
        f"# {t(config, 'daily_title')} | {meta['site']}",
        "",
        f"- {t(config, 'date')}: {meta['report_date']}",
        f"- {t(config, 'window')}: {meta['window_start']} -> {meta['window_end']}",
        f"- {t(config, 'host')}: `{meta['host_id']}`",
        f"- {t(config, 'bucket')}: {meta['bucket_minutes']} min",
        "",
        f"## {t(config, 'core_metrics')}",
        f"- {t(config, 'pv')}: {format_number(traffic['pv'])}",
        f"- {t(config, 'uv')}: {format_number(traffic['uv'])}",
        f"- {t(config, 'ips')}: {format_number(traffic['unique_ips'])}",
        f"- {t(config, 'requests')}: {format_number(traffic['request_count'])}",
        f"- {t(config, 'peak_qps')}: {format_number(traffic['qps_peak'], 4)}",
        f"- {t(config, 'avg_response')}: {format_number(traffic['avg_response_ms'])} ms",
        f"- {t(config, 'slow_requests')}: {format_number(traffic['slow_request_count'])}",
        f"- {t(config, 'ssl_remaining')}: {format_ssl_summary_text(config, ssl_info)}",
        f"- {t(config, 'bandwidth_out')}: {format_bytes(traffic['bandwidth_out_bytes'])}",
        f"- {t(config, 'bandwidth_in')}: {format_bytes(traffic['bandwidth_in_bytes'])}",
        "",
        f"## {t(config, 'status_mix')}",
    ]
    for item in report["status_families"] or []:
        lines.append(
            f"- {item['item']}: {format_number(item['count'])} ({safe_ratio(item['count'], total_requests) * 100:.2f}%)"
        )
    if not report["status_families"]:
        lines.append(f"- {t(config, 'no_data')}")

    for section_key, section_title in (
        ("top_errors", t(config, "top_errors")),
        ("top_uris", t(config, "top_uris")),
        ("spiders", t(config, "spiders")),
        ("slow_routes", t(config, "slow_routes")),
        ("abnormal_ips", t(config, "abnormal_ips")),
    ):
        lines.extend(["", f"## {section_title}"])
        if report.get(section_key):
            for row in report[section_key]:
                lines.append(f"- {row['item']}: {format_number(row['count'])}")
        else:
            lines.append(f"- {t(config, 'no_data')}")

    lines.extend(
        [
            "",
            f"## {t(config, 'system_health')}",
            f"- CPU avg/max: {format_number(system['avg_cpu_pct'])}% / {format_number(system['max_cpu_pct'])}%",
            f"- Memory avg/max: {format_number(system['avg_memory_pct'])}% / {format_number(system['max_memory_pct'])}%",
            f"- Disk free min: {format_bytes(system['min_disk_free_bytes'])}",
        ]
    )
    if traffic["uv_is_estimate"] or traffic["unique_ips_is_estimate"]:
        lines.extend(["", f"> {t(config, 'warning_estimate')}"])
    return "\n".join(lines).strip() + "\n"


def choose_font_family() -> str:
    if font_manager is None:
        return "DejaVu Sans"
    font_path = resolve_pdf_font_path()
    try:
        font_manager.fontManager.addfont(str(font_path))
    except RuntimeError:
        pass
    return font_manager.FontProperties(fname=str(font_path)).get_name()


def setup_pdf_style() -> None:
    if matplotlib is None or font_manager is None:
        return
    chosen = choose_font_family()
    matplotlib.rcParams["font.family"] = chosen
    matplotlib.rcParams["font.sans-serif"] = [chosen]
    matplotlib.rcParams["axes.unicode_minus"] = False
    matplotlib.rcParams["figure.facecolor"] = PDF_COLORS["bg"]
    matplotlib.rcParams["savefig.facecolor"] = PDF_COLORS["bg"]
    matplotlib.rcParams["axes.facecolor"] = PDF_COLORS["panel"]
    matplotlib.rcParams["axes.edgecolor"] = PDF_COLORS["border"]
    matplotlib.rcParams["grid.color"] = PDF_COLORS["grid"]
    matplotlib.rcParams["axes.grid"] = False
    matplotlib.rcParams["axes.spines.top"] = False
    matplotlib.rcParams["axes.spines.right"] = False
    matplotlib.rcParams["axes.spines.left"] = False
    matplotlib.rcParams["axes.spines.bottom"] = False
    matplotlib.rcParams["xtick.major.size"] = 0
    matplotlib.rcParams["ytick.major.size"] = 0
    matplotlib.rcParams["xtick.minor.size"] = 0
    matplotlib.rcParams["ytick.minor.size"] = 0
    matplotlib.rcParams["font.size"] = 8
    matplotlib.rcParams["axes.titlesize"] = 9
    matplotlib.rcParams["legend.fontsize"] = 8
    matplotlib.rcParams["xtick.labelsize"] = 8
    matplotlib.rcParams["ytick.labelsize"] = 8
    matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(color=MORANDI_PALETTE)


def add_card(fig: Any, left: float, bottom: float, width: float, height: float, title: str, value: str, subtitle: str) -> None:
    patch = FancyBboxPatch(
        (left, bottom),
        width,
        height,
        boxstyle="round,pad=0.006,rounding_size=0.018",
        facecolor=PDF_COLORS["panel"],
        edgecolor=PDF_COLORS["border"],
        linewidth=0.8,
        transform=fig.transFigure,
        zorder=1,
    )
    fig.patches.append(patch)
    fig.text(left + 0.015, bottom + height - 0.028, title, fontsize=9, color=PDF_COLORS["muted"])
    fig.text(left + 0.015, bottom + 0.032, value, fontsize=18, weight="bold", color=PDF_COLORS["text"])
    if subtitle:
        fig.text(left + 0.015, bottom + 0.01, subtitle, fontsize=8, color=PDF_COLORS["green"])


def style_axis(ax: Any, title: str) -> None:
    ax.set_title(title, loc="left", fontsize=11, weight="bold", pad=10)
    ax.grid(True, axis="y", color=PDF_COLORS["border"], linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(PDF_COLORS["border"])
    ax.spines["bottom"].set_color(PDF_COLORS["border"])
    ax.tick_params(length=0, pad=6, labelsize=9)


def draw_table(ax: Any, title: str, headers: list[str], rows: list[list[str]]) -> None:
    ax.set_title(title, loc="left", fontsize=11, weight="bold", pad=10)
    ax.axis("off")
    if not rows:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=PDF_COLORS["muted"])
        return
    table = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="left", colLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.35)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(PDF_COLORS["border"])
        cell.set_linewidth(0.5)
        if row == 0:
            cell.set_facecolor("#eaf5f0")
            cell.set_text_props(weight="bold", color=PDF_COLORS["text"])
        else:
            cell.set_facecolor(PDF_COLORS["panel"])
            cell.set_text_props(color=PDF_COLORS["text"])


def draw_pie(ax: Any, title: str, items: list[dict[str, Any]], colors: list[str]) -> None:
    ax.set_title(title, loc="left", fontsize=11, weight="bold", pad=10)
    if not items:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=PDF_COLORS["muted"])
        ax.axis("off")
        return
    wedges, texts, autotexts = ax.pie(
        [int(item["count"]) for item in items],
        labels=[str(item["item"]) for item in items],
        autopct="%1.1f%%",
        colors=colors[: len(items)],
        startangle=90,
        wedgeprops={"edgecolor": PDF_COLORS["panel"], "linewidth": 1},
        pctdistance=0.78,
    )
    ax.add_artist(plt.Circle((0, 0), 0.52, color=PDF_COLORS["panel"]))
    for text in texts:
        text.set_fontsize(8)
    for text in autotexts:
        text.set_fontsize(8)
    ax.axis("equal")


_PDF_FONT_CACHE: dict[tuple[str, float, str], Any] = {}


def resolve_pdf_font_path() -> Path:
    for path in PDF_FONT_PATHS:
        if path.exists():
            return path
    searched = ", ".join(str(path) for path in PDF_FONT_PATHS)
    raise FileNotFoundError(f"Server-Mate PDF font was not found. Searched: {searched}")


def pdf_font(size: float = 10.0, weight: str = "regular") -> Any:
    if font_manager is None:
        return None
    font_path = resolve_pdf_font_path()
    cache_key = (str(font_path), float(size), weight)
    if cache_key not in _PDF_FONT_CACHE:
        _PDF_FONT_CACHE[cache_key] = font_manager.FontProperties(
            fname=str(font_path),
            size=size,
            weight=weight,
        )
    return _PDF_FONT_CACHE[cache_key]


def create_pdf_figure() -> Any:
    fig = plt.figure(figsize=(18, 12), constrained_layout=True)
    fig.patch.set_facecolor(PDF_COLORS["bg"])
    try:
        fig.set_constrained_layout_pads(w_pad=0.04, h_pad=0.05, wspace=0.04, hspace=0.05)
    except AttributeError:
        pass
    return fig


def localize_chart_item(value: str, labels: dict[str, str]) -> str:
    mapped = {"other": labels["other"]}
    return mapped.get(str(value).lower(), str(value))


def apply_axis_tick_fonts(ax: Any, size: float = 9.5) -> None:
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(pdf_font(size))
        label.set_color(PDF_COLORS["muted"])


def style_report_axis(ax: Any, title: str) -> None:
    ax.set_facecolor(PDF_COLORS["panel"])
    ax.set_title(
        title,
        loc="left",
        pad=16,
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(14, "bold"),
    )
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.3, color=PDF_COLORS["grid"])
    for spine in ax.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(1.0)
    ax.tick_params(axis="both", length=0, pad=8, colors=PDF_COLORS["muted"])
    apply_axis_tick_fonts(ax)


def set_report_xticks(ax: Any, labels_text: list[str], max_labels: int, rotation: int = 30) -> None:
    if not labels_text:
        return
    step = max(1, math.ceil(len(labels_text) / max_labels))
    positions = list(range(0, len(labels_text), step))
    if positions[-1] != len(labels_text) - 1:
        positions.append(len(labels_text) - 1)
    ax.set_xticks(positions)
    ax.set_xticklabels([labels_text[index] for index in positions], rotation=rotation, ha="right")
    apply_axis_tick_fonts(ax)


def draw_report_header(
    ax: Any,
    report: dict[str, Any],
    labels: dict[str, str],
    title: str,
    generated_at: str,
    page_number: int,
    total_pages: int,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    meta_text = (
        f"{labels['site']}: {report['meta']['site']}  |  "
        f"{labels['host']}: {report['meta']['host_id']}  |  "
        f"{labels['window']}: {report['meta']['window_start']} -> {report['meta']['window_end']}"
    )
    ax.text(
        0.0,
        0.88,
        title,
        transform=ax.transAxes,
        va="top",
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(24, "bold"),
    )
    ax.text(
        0.0,
        0.42,
        meta_text,
        transform=ax.transAxes,
        va="top",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(10),
    )
    ax.text(
        1.0,
        0.88,
        labels["page_indicator"].format(current=page_number, total=total_pages),
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=PDF_COLORS["blue"],
        fontproperties=pdf_font(10, "bold"),
    )
    ax.text(
        1.0,
        0.42,
        f"{labels['generated_at']}: {generated_at}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(10),
    )
    ax.plot([0.0, 1.0], [0.05, 0.05], transform=ax.transAxes, color=PDF_COLORS["border"], linewidth=1.1)


def draw_metric_segments(
    ax: Any,
    cards: list[dict[str, str]],
    left: float = 0.0,
    right: float = 1.0,
    bottom: float = 0.08,
    top: float = 0.58,
    label_size: float = 12,
    value_size: float = 26,
    subtitle_size: float = 10,
) -> None:
    if not cards:
        return
    segment_width = (right - left) / len(cards)
    pad_x = segment_width * 0.08
    for index, card in enumerate(cards):
        segment_left = left + index * segment_width
        segment_right = segment_left + segment_width
        if index > 0:
            ax.plot(
                [segment_left, segment_left],
                [bottom + 0.02, top - 0.02],
                transform=ax.transAxes,
                color=PDF_COLORS["divider"],
                linewidth=0.9,
            )
        text_x = segment_left + pad_x
        ax.text(
            text_x,
            top - 0.01,
            card["label"],
            transform=ax.transAxes,
            ha="left",
            va="top",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(label_size),
        )
        ax.text(
            text_x,
            bottom + (top - bottom) * 0.48,
            card["value"],
            transform=ax.transAxes,
            ha="left",
            va="center",
            color=PDF_COLORS["text"],
            fontproperties=pdf_font(value_size, "bold"),
        )
        ax.text(
            text_x,
            bottom + 0.015,
            truncate_text(card["subtitle"], 26),
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            color=PDF_COLORS["subtle"],
            fontproperties=pdf_font(subtitle_size),
        )
        ax.plot(
            [text_x, min(segment_right - pad_x, text_x + segment_width * 0.32)],
            [top - 0.005, top - 0.005],
            transform=ax.transAxes,
            color=card.get("accent", PDF_COLORS["border"]),
            linewidth=1.6,
            solid_capstyle="round",
            alpha=0.9,
        )


def draw_stat_panel(ax: Any, title: str, cards: list[dict[str, str]], columns: int = 3) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if not cards:
        ax.text(
            0.5,
            0.5,
            title,
            transform=ax.transAxes,
            ha="center",
            va="center",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(10),
        )
        return
    ax.text(0.0, 0.97, title, transform=ax.transAxes, va="top", color=PDF_COLORS["text"], fontproperties=pdf_font(16, "bold"))
    ax.plot([0.0, 1.0], [0.86, 0.86], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.9)
    draw_metric_segments(
        ax,
        cards,
        left=0.0,
        right=1.0,
        bottom=0.10,
        top=0.72,
        label_size=11.5,
        value_size=24 if len(cards) >= 6 else 26,
        subtitle_size=10,
    )


def build_dashboard_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    traffic = report["traffic"]
    avg_response = traffic.get("avg_response_ms")
    http_5xx_count = sum(int(item["count"]) for item in report.get("status_codes", []) if str(item["item"]).startswith("5"))
    return [
        {"label": f"{labels['pv']}", "value": format_number(traffic["pv"]), "subtitle": f"{labels['uv']}: {format_number(traffic['uv'])}", "accent": PDF_COLORS["blue"]},
        {"label": f"{labels['uv']}", "value": format_number(traffic["uv"]), "subtitle": f"{labels['ips']}: {format_number(traffic['unique_ips'])}", "accent": PDF_COLORS["green"]},
        {"label": f"{labels['requests']}", "value": format_number(traffic["request_count"]), "subtitle": f"{labels['bandwidth_out']}: {format_bytes(traffic['bandwidth_out_bytes'])}", "accent": PDF_COLORS["sky"]},
        {"label": f"{labels['peak_qps']}", "value": format_number(traffic["qps_peak"], 4), "subtitle": f"{labels['bandwidth_in']}: {format_bytes(traffic.get('bandwidth_in_bytes'))}", "accent": PDF_COLORS["purple"]},
        {"label": f"{labels['avg_response']}", "value": "N/A" if avg_response is None else f"{format_number(avg_response)} ms", "subtitle": f"{labels['top_errors']}: {format_number(report.get('errors_total'))}", "accent": PDF_COLORS["orange"]},
        {"label": f"{labels['slow_requests']}", "value": format_number(traffic["slow_request_count"]), "subtitle": f"5xx: {format_number(http_5xx_count)}", "accent": PDF_COLORS["red"]},
    ]


def build_system_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    system = report["system"]
    return [
        {"label": labels["cpu"], "value": "N/A" if system["max_cpu_pct"] is None else f"{format_number(system['max_cpu_pct'])}%", "subtitle": f"{labels['avg_short']}: {format_number(system['avg_cpu_pct'])}%", "accent": PDF_COLORS["orange"]},
        {"label": labels["memory"], "value": "N/A" if system["max_memory_pct"] is None else f"{format_number(system['max_memory_pct'])}%", "subtitle": f"{labels['avg_short']}: {format_number(system['avg_memory_pct'])}%", "accent": PDF_COLORS["green"]},
        {"label": labels["disk"], "value": format_bytes(system["min_disk_free_bytes"]), "subtitle": labels["kpi_disk_subtitle"], "accent": PDF_COLORS["blue"]},
    ]


def build_weekly_compare_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    metrics = (
        ("pv", labels["pv"], PDF_COLORS["blue"]),
        ("uv", labels["uv"], PDF_COLORS["green"]),
        ("request_count", labels["requests"], PDF_COLORS["sky"]),
        ("errors_total", labels["top_errors"], PDF_COLORS["red"]),
    )
    cards = []
    for key, title, accent in metrics:
        item = report["wow"].get(key, {})
        cards.append(
            {
                "label": title,
                "value": format_number(item.get("current")),
                "subtitle": f"{labels['previous']}: {format_number(item.get('previous'))} | {labels['ratio']}: {format_percent(item.get('ratio'))}",
                "accent": accent,
            }
        )
    return cards


def build_security_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    return [
        {"label": labels["security_404"], "value": format_number(report["security"]["http_404_count"]), "subtitle": labels["security_overview"], "accent": PDF_COLORS["orange"]},
        {"label": labels["security_5xx"], "value": format_number(report["security"]["http_5xx_count"]), "subtitle": labels["security_overview"], "accent": PDF_COLORS["red"]},
        {"label": labels["security_bad_ips"], "value": format_number(report["security"]["suspicious_ip_count"]), "subtitle": labels["security_overview"], "accent": PDF_COLORS["purple"]},
    ]


def build_weekly_header_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    cards = []
    for key, title, accent in (
        ("pv", labels["pv"], PDF_COLORS["blue"]),
        ("uv", labels["uv"], PDF_COLORS["green"]),
        ("request_count", labels["requests"], PDF_COLORS["sky"]),
        ("errors_total", labels["top_errors"], PDF_COLORS["red"]),
    ):
        item = report["wow"].get(key, {})
        cards.append(
            {
                "label": title,
                "value": format_number(item.get("current")),
                "subtitle": f"{labels['ratio']}: {format_percent(item.get('ratio'))}",
                "accent": accent,
            }
        )
    cards.extend(
        [
            {
                "label": labels["security_404"],
                "value": format_number(report["security"]["http_404_count"]),
                "subtitle": f"5xx: {format_number(report['security']['http_5xx_count'])}",
                "accent": PDF_COLORS["orange"],
            },
            {
                "label": labels["security_bad_ips"],
                "value": format_number(report["security"]["suspicious_ip_count"]),
                "subtitle": labels["security_overview"],
                "accent": PDF_COLORS["purple"],
            },
        ]
    )
    return cards


def build_monthly_summary_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    traffic = report["traffic"]
    return [
        {
            "label": labels["cpu"],
            "value": "N/A" if traffic["cpu_peak"] is None else f"{format_number(traffic['cpu_peak'])}%",
            "subtitle": labels["resource_cpu"],
            "accent": PDF_COLORS["orange"],
        },
        {
            "label": labels["memory"],
            "value": "N/A" if traffic["memory_peak"] is None else f"{format_number(traffic['memory_peak'])}%",
            "subtitle": labels["avg_response"] + f": {format_number(traffic['avg_response_ms'])} ms",
            "accent": PDF_COLORS["green"],
        },
        {
            "label": labels["disk"],
            "value": format_bytes(traffic["disk_free_min"]),
            "subtitle": f"{labels['slow_requests']}: {format_number(traffic['slow_request_count'])}",
            "accent": PDF_COLORS["blue"],
        },
    ]


def draw_dashboard_header(
    ax: Any,
    report: dict[str, Any],
    labels: dict[str, str],
    title: str,
    generated_at: str,
    cards: list[dict[str, str]],
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    meta_text = (
        f"{labels['site']}: {report['meta']['site']}  |  "
        f"{labels['host']}: {report['meta']['host_id']}  |  "
        f"{labels['window']}: {report['meta']['window_start']} -> {report['meta']['window_end']}"
    )
    ax.text(0.0, 0.98, title, transform=ax.transAxes, va="top", color=PDF_COLORS["text"], fontproperties=pdf_font(22, "bold"))
    ax.text(0.0, 0.81, meta_text, transform=ax.transAxes, va="top", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
    ax.text(1.0, 0.98, labels["page_indicator"].format(current=1, total=2), transform=ax.transAxes, ha="right", va="top", color=PDF_COLORS["blue"], fontproperties=pdf_font(10, "bold"))
    ax.text(1.0, 0.81, f"{labels['generated_at']}: {generated_at}", transform=ax.transAxes, ha="right", va="top", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
    ax.plot([0.0, 1.0], [0.70, 0.70], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.9)
    draw_metric_segments(
        ax,
        cards,
        left=0.0,
        right=1.0,
        bottom=0.08,
        top=0.60,
        label_size=12,
        value_size=24 if len(cards) >= 6 else 26,
        subtitle_size=10,
    )


def draw_summary_header(
    ax: Any,
    report: dict[str, Any],
    labels: dict[str, str],
    title: str,
    generated_at: str,
    cards: list[dict[str, str]],
    page_number: int,
    total_pages: int,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    meta_text = (
        f"{labels['site']}: {report['meta']['site']}  |  "
        f"{labels['host']}: {report['meta']['host_id']}  |  "
        f"{labels['window']}: {report['meta']['window_start']} -> {report['meta']['window_end']}"
    )
    ax.text(0.0, 0.98, title, transform=ax.transAxes, va="top", color=PDF_COLORS["text"], fontproperties=pdf_font(21, "bold"))
    ax.text(0.0, 0.82, meta_text, transform=ax.transAxes, va="top", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
    ax.text(1.0, 0.98, labels["page_indicator"].format(current=page_number, total=total_pages), transform=ax.transAxes, ha="right", va="top", color=PDF_COLORS["blue"], fontproperties=pdf_font(10, "bold"))
    ax.text(1.0, 0.82, f"{labels['generated_at']}: {generated_at}", transform=ax.transAxes, ha="right", va="top", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
    ax.plot([0.0, 1.0], [0.68, 0.68], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.9)
    draw_metric_segments(
        ax,
        cards,
        left=0.0,
        right=1.0,
        bottom=0.08,
        top=0.58,
        label_size=11.5,
        value_size=23 if len(cards) >= 6 else 25,
        subtitle_size=10,
    )


def draw_report_table(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float] | None = None,
    empty_text: str = "No data",
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    shell = FancyBboxPatch(
        (0.0, 0.0),
        1.0,
        1.0,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PDF_COLORS["panel"],
        edgecolor=PDF_COLORS["border"],
        linewidth=0.9,
        transform=ax.transAxes,
        zorder=0,
    )
    ax.add_patch(shell)
    ax.text(0.03, 0.97, title, transform=ax.transAxes, va="top", color=PDF_COLORS["text"], fontproperties=pdf_font(14, "bold"))
    if not rows:
        ax.text(0.5, 0.46, empty_text, transform=ax.transAxes, ha="center", va="center", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
        return
    table = ax.table(
        cellText=rows,
        colLabels=headers,
        bbox=[0.03, 0.05, 0.94, 0.82],
        cellLoc="left",
        colLoc="left",
        colWidths=col_widths,
        zorder=2,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.0)
    table.scale(1.0, 1.42)
    for (row_index, column_index), cell in table.get_celld().items():
        cell.set_edgecolor(PDF_COLORS["border"])
        cell.set_linewidth(0.6)
        cell.get_text().set_wrap(False)
        if row_index == 0:
            cell.set_facecolor("#e8f0ff")
            cell.get_text().set_color(PDF_COLORS["text"])
            cell.get_text().set_fontproperties(pdf_font(9, "bold"))
        else:
            cell.set_facecolor(PDF_COLORS["panel_alt"] if row_index % 2 == 1 else PDF_COLORS["panel"])
            cell.get_text().set_color(PDF_COLORS["text"])
            cell.get_text().set_fontproperties(pdf_font(9))
        if column_index == 0:
            cell.get_text().set_ha("center")


def draw_report_pie(ax: Any, title: str, items: list[dict[str, Any]], colors: list[str], labels: dict[str, str]) -> None:
    ax.set_facecolor(PDF_COLORS["panel"])
    for spine in ax.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(1.0)
    ax.set_title(title, loc="left", pad=14, color=PDF_COLORS["text"], fontproperties=pdf_font(14, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    if not items:
        ax.text(0.5, 0.5, labels["no_data"], transform=ax.transAxes, ha="center", va="center", color=PDF_COLORS["muted"], fontproperties=pdf_font(10))
        return
    values = [int(item["count"]) for item in items]
    legends = [localize_chart_item(str(item["item"]), labels) for item in items]
    _wedges, texts, autotexts = ax.pie(
        values,
        labels=legends,
        colors=colors[: len(items)],
        startangle=90,
        autopct=lambda value: f"{value:.1f}%" if value >= 4 else "",
        pctdistance=0.78,
        labeldistance=1.06,
        wedgeprops={"width": 0.38, "edgecolor": PDF_COLORS["panel"], "linewidth": 1.6},
    )
    ax.text(0.0, 0.05, format_number(sum(values)), ha="center", va="center", color=PDF_COLORS["text"], fontproperties=pdf_font(16, "bold"))
    ax.text(0.0, -0.14, labels["count"], ha="center", va="center", color=PDF_COLORS["muted"], fontproperties=pdf_font(9))
    for text in texts:
        text.set_color(PDF_COLORS["muted"])
        text.set_fontproperties(pdf_font(9))
    for text in autotexts:
        text.set_color(PDF_COLORS["text"])
        text.set_fontproperties(pdf_font(8.5, "bold"))
    ax.axis("equal")


def draw_daily_trend_chart(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    style_report_axis(ax, labels["daily_hourly_trend"])
    hours = [item["hour"] for item in report["hourly_series"]]
    pv_values = [float(item["pv"]) for item in report["hourly_series"]]
    request_values = [float(item["request_count"]) for item in report["hourly_series"]]
    x_positions = list(range(len(hours)))
    point_sizes = [48 + math.sqrt(max(value, 0.0) + 1.0) * 16 for value in request_values]
    ax.plot(x_positions, pv_values, color=PDF_COLORS["blue"], linewidth=2.8, label=labels["pv"], zorder=3)
    ax.fill_between(x_positions, pv_values, color=PDF_COLORS["blue"], alpha=0.08, zorder=1)
    ax.scatter(x_positions, pv_values, s=point_sizes, color=PDF_COLORS["sky"], alpha=0.28, edgecolors=PDF_COLORS["blue"], linewidths=0.9, zorder=4)
    ax.plot(x_positions, request_values, color=PDF_COLORS["green"], linewidth=2.0, label=labels["requests"], alpha=0.95, zorder=2)
    set_report_xticks(ax, [f"{hour:02d}:00" for hour in hours], 12, rotation=30)
    ax.margins(x=0.02)
    ax.legend(frameon=False, loc="upper left", prop=pdf_font(10))


def draw_period_trend_chart(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    report_kind = report["meta"]["report_kind"]
    title = labels["trend_pv_uv"] if report_kind == "weekly" else labels["trend_30d"]
    style_report_axis(ax, title)
    series = report["traffic_series"]
    x_positions = list(range(len(series)))
    date_labels = [item["date"][5:] for item in series]
    pv_values = [float(item["pv"]) for item in series]
    uv_values = [float(item["uv"]) for item in series]
    if report_kind == "monthly":
        pv_values = moving_average(pv_values, 3)
        uv_values = moving_average(uv_values, 3)
    ax.plot(x_positions, pv_values, color=PDF_COLORS["blue"], linewidth=2.8, marker="o", markersize=5, label=labels["pv"])
    ax.fill_between(x_positions, pv_values, color=PDF_COLORS["blue"], alpha=0.08)
    ax.plot(x_positions, uv_values, color=PDF_COLORS["green"], linewidth=2.3, marker="o", markersize=4.2, label=labels["uv"])
    set_report_xticks(ax, date_labels, 8 if report_kind == "weekly" else 10, rotation=30)
    ax.margins(x=0.02)
    ax.legend(frameon=False, loc="upper left", prop=pdf_font(10))


def draw_monthly_resource_trend(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    style_report_axis(ax, labels["cpu_disk_trend"])
    series = report["traffic_series"]
    x_positions = list(range(len(series)))
    date_labels = [item["date"][5:] for item in series]
    cpu_values = [float(item["cpu_peak"] or 0.0) for item in series]
    disk_values = [float(item["disk_free_bytes"] or 0.0) / (1024 ** 3) for item in series]
    ax.plot(x_positions, cpu_values, color=PDF_COLORS["orange"], linewidth=2.5, marker="o", markersize=4.6, label=labels["resource_cpu"])
    ax.fill_between(x_positions, cpu_values, color=PDF_COLORS["orange"], alpha=0.08)
    ax.set_ylabel(labels["resource_cpu"], color=PDF_COLORS["orange"], fontproperties=pdf_font(10))
    ax_right = ax.twinx()
    ax_right.plot(x_positions, disk_values, color=PDF_COLORS["blue"], linewidth=2.3, marker="s", markersize=4.1, label=labels["resource_disk"])
    ax_right.set_ylabel(labels["resource_disk"], color=PDF_COLORS["blue"], fontproperties=pdf_font(10))
    ax_right.grid(False)
    ax_right.tick_params(axis="y", length=0, pad=8, colors=PDF_COLORS["muted"])
    for spine in ax_right.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(1.0)
    set_report_xticks(ax, date_labels, 10, rotation=30)
    apply_axis_tick_fonts(ax_right)
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    ax.legend(left_handles + right_handles, left_labels + right_labels, frameon=False, loc="upper left", prop=pdf_font(10))


def build_ranked_rows(items: list[dict[str, Any]], metric_formatter: Any, item_limit: int = 38) -> list[list[str]]:
    return [[str(index + 1), truncate_text(str(item["item"]), item_limit), metric_formatter(item["count"])] for index, item in enumerate(items)]


def render_detail_page(fig: Any, report: dict[str, Any], labels: dict[str, str], generated_at: str) -> None:
    report_kind = report["meta"]["report_kind"]
    if report_kind == "daily":
        grid = fig.add_gridspec(3, 12, height_ratios=[1.5, 4.25, 4.25])
        draw_summary_header(
            fig.add_subplot(grid[0, :]),
            report,
            labels,
            f"{labels['daily_title']} | {labels['details_page']}",
            generated_at,
            build_system_cards(report, labels),
            2,
            2,
        )
        top_row_index = 1
        bottom_row_index = 2
    elif report_kind == "weekly":
        grid = fig.add_gridspec(3, 12, height_ratios=[1.5, 4.25, 4.25])
        draw_summary_header(
            fig.add_subplot(grid[0, :]),
            report,
            labels,
            f"{labels['weekly_title']} | {labels['details_page']}",
            generated_at,
            build_weekly_header_cards(report, labels),
            2,
            2,
        )
        top_row_index = 1
        bottom_row_index = 2
    else:
        grid = fig.add_gridspec(4, 12, height_ratios=[1.5, 2.0, 3.25, 3.25])
        draw_summary_header(
            fig.add_subplot(grid[0, :]),
            report,
            labels,
            f"{labels['monthly_title']} | {labels['details_page']}",
            generated_at,
            build_monthly_summary_cards(report, labels),
            2,
            2,
        )
        draw_monthly_resource_trend(fig.add_subplot(grid[1, :]), report, labels)
        top_row_index = 2
        bottom_row_index = 3

    draw_report_table(fig.add_subplot(grid[top_row_index, 0:6]), labels["top_uris"], [labels["rank"], labels["item"], labels["count"]], build_ranked_rows(report["top_uris"], lambda value: format_number(value), 42), [0.10, 0.68, 0.22], labels["no_data"])
    draw_report_table(fig.add_subplot(grid[top_row_index, 6:12]), labels["slow_routes"], [labels["rank"], labels["item"], labels["count"]], build_ranked_rows(report["slow_routes"], lambda value: format_number(value), 38), [0.10, 0.68, 0.22], labels["no_data"])
    draw_report_table(fig.add_subplot(grid[bottom_row_index, 0:6]), labels["abnormal_ips"], [labels["rank"], labels["item"], labels["rpm"]], build_ranked_rows(report["abnormal_ips"], lambda value: format_number(value), 32), [0.10, 0.58, 0.32], labels["no_data"])
    draw_report_table(fig.add_subplot(grid[bottom_row_index, 6:12]), labels["top_errors"], [labels["rank"], labels["item"], labels["count"]], build_ranked_rows(report["top_errors"], lambda value: format_number(value), 44), [0.10, 0.70, 0.20], labels["no_data"])


def render_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    if plt is None or PdfPages is None or FancyBboxPatch is None or font_manager is None:
        raise RuntimeError("matplotlib is not installed; install it first to generate PDF reports.")

    setup_pdf_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_kind = report["meta"]["report_kind"]
    language = report_language(config)
    labels = TRANSLATIONS[language]
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        dashboard = create_pdf_figure()
        grid = dashboard.add_gridspec(3, 12, height_ratios=[1.5, 4.0, 4.5])
        draw_dashboard_header(
            dashboard.add_subplot(grid[0, :]),
            report,
            labels,
            f"{labels[f'{report_kind}_title']} | {labels['dashboard_page']}",
            generated_at,
            build_dashboard_cards(report, labels),
        )

        trend_axis = dashboard.add_subplot(grid[1, :])
        if report_kind == "daily":
            draw_daily_trend_chart(trend_axis, report, labels)
        else:
            draw_period_trend_chart(trend_axis, report, labels)

        draw_report_pie(
            dashboard.add_subplot(grid[2, 0:6]),
            labels["spider_distribution"],
            build_spider_chart_data(report["spiders"]),
            [PDF_COLORS["blue"], PDF_COLORS["green"], PDF_COLORS["purple"], PDF_COLORS["yellow"], PDF_COLORS["gray"]],
            labels,
        )
        draw_report_pie(
            dashboard.add_subplot(grid[2, 6:12]),
            labels["http_status_mix"],
            build_status_chart_data(report["status_codes"]),
            [PDF_COLORS["green"], PDF_COLORS["orange"], PDF_COLORS["red"], PDF_COLORS["gray"]],
            labels,
        )
        pdf.savefig(dashboard)
        plt.close(dashboard)

        details = create_pdf_figure()
        render_detail_page(details, report, labels, generated_at)
        pdf.savefig(details)
        plt.close(details)

    return output_path


def create_pdf_figure() -> Any:
    fig = plt.figure(figsize=(8.27, 11.69), constrained_layout=False)
    fig.patch.set_facecolor(PDF_COLORS["bg"])
    fig.subplots_adjust(left=0.055, right=0.97, top=0.985, bottom=0.045, wspace=0.32, hspace=0.42)
    return fig


def localize_chart_item(value: str, labels: dict[str, str]) -> str:
    mapped = {"other": labels["other"]}
    return mapped.get(str(value).lower(), str(value))


def wrap_report_text(value: str, width: int) -> str:
    return "\n".join(
        textwrap.wrap(
            str(value),
            width=max(width, 1),
            break_long_words=True,
            break_on_hyphens=False,
        )
    )


def apply_axis_tick_fonts(ax: Any, size: float = 8.4) -> None:
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(pdf_font(size))
        label.set_color("#000000")


def style_report_axis(ax: Any, title: str) -> None:
    ax.set_facecolor(PDF_COLORS["panel"])
    ax.set_title(
        title,
        loc="left",
        pad=12,
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(10.8, "bold"),
    )
    ax.grid(True, axis="y", linestyle="--", linewidth=0.7, alpha=0.3, color=PDF_COLORS["grid"])
    for spine in ax.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(0.8)
    ax.tick_params(axis="both", length=0, pad=6, colors=PDF_COLORS["muted"])
    apply_axis_tick_fonts(ax)


def set_report_xticks(ax: Any, labels_text: list[str], max_labels: int, rotation: int = 28) -> None:
    if not labels_text:
        return
    step = max(1, math.ceil(len(labels_text) / max_labels))
    positions = list(range(0, len(labels_text), step))
    if positions[-1] != len(labels_text) - 1:
        positions.append(len(labels_text) - 1)
    ax.set_xticks(positions)
    ax.set_xticklabels([labels_text[index] for index in positions], rotation=rotation, ha="right")
    apply_axis_tick_fonts(ax)


def draw_page_header(
    ax: Any,
    report: dict[str, Any],
    labels: dict[str, str],
    title: str,
    generated_at: str,
    page_number: int,
    total_pages: int,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(
        0.0,
        0.95,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(16.5, "bold"),
    )
    ax.text(
        0.0,
        0.57,
        f"{labels['site']}: {report['meta']['site']}    {labels['host']}: {report['meta']['host_id']}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(8.7),
    )
    ax.text(
        0.0,
        0.28,
        f"{labels['window']}: {report['meta']['window_start']} -> {report['meta']['window_end']}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(8.5),
    )
    ax.text(
        1.0,
        0.95,
        labels["page_indicator"].format(current=page_number, total=total_pages),
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=PDF_COLORS["blue"],
        fontproperties=pdf_font(8.8, "bold"),
    )
    ax.text(
        1.0,
        0.57,
        f"{labels['generated_at']}: {generated_at}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(8.5),
    )
    ax.plot([0.0, 1.0], [0.05, 0.05], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.9)


def draw_ai_summary_box(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel = FancyBboxPatch(
        (0.0, 0.04),
        1.0,
        0.90,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor="#eef6ff",
        edgecolor="#cbdcf8",
        linewidth=0.9,
        transform=ax.transAxes,
    )
    ax.add_patch(panel)
    badge = FancyBboxPatch(
        (0.84, 0.72),
        0.13,
        0.14,
        boxstyle="round,pad=0.01,rounding_size=0.04",
        facecolor="#dcecff",
        edgecolor="none",
        transform=ax.transAxes,
    )
    ax.add_patch(badge)
    ax.text(
        0.03,
        0.84,
        labels["ai_summary_title"],
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(11.2, "bold"),
    )
    ax.text(
        0.905,
        0.79,
        labels["ai_summary_badge"],
        transform=ax.transAxes,
        ha="center",
        va="center",
        color=PDF_COLORS["blue"],
        fontproperties=pdf_font(7.2, "bold"),
    )
    ai_block = report.get("ai_analysis") or {}
    summary_text = wrap_report_text(ai_block.get("summary") or labels["no_data"], 74)
    ax.text(
        0.03,
        0.66,
        summary_text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        linespacing=1.42,
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(8.8),
    )
    source_text = "LLM" if ai_block.get("source") == "llm" else "SIMULATED"
    ax.text(
        0.03,
        0.12,
        f"{labels['summary']}: {source_text}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color=PDF_COLORS["muted"],
        fontproperties=pdf_font(7.8),
    )


def draw_metric_segments(
    ax: Any,
    cards: list[dict[str, str]],
    left: float = 0.0,
    right: float = 1.0,
    bottom: float = 0.08,
    top: float = 0.88,
    label_size: float = 8.4,
    value_size: float = 17.0,
    subtitle_size: float = 7.6,
    item_wrap: int = 12,
    subtitle_wrap: int = 18,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if not cards:
        ax.text(
            0.5,
            0.5,
            "No data",
            transform=ax.transAxes,
            ha="center",
            va="center",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(8.5),
        )
        return
    segment_width = (right - left) / len(cards)
    pad_x = segment_width * 0.07
    for index, card in enumerate(cards):
        segment_left = left + index * segment_width
        segment_right = segment_left + segment_width
        if index > 0:
            ax.plot(
                [segment_left, segment_left],
                [bottom + 0.05, top - 0.05],
                transform=ax.transAxes,
                color=PDF_COLORS["divider"],
                linewidth=0.8,
            )
        text_x = segment_left + pad_x
        accent_width = min(segment_width * 0.24, 0.04)
        ax.plot(
            [text_x, text_x + accent_width],
            [top - 0.03, top - 0.03],
            transform=ax.transAxes,
            color=card.get("accent", PDF_COLORS["border"]),
            linewidth=1.7,
            solid_capstyle="round",
        )
        ax.text(
            text_x,
            top - 0.06,
            wrap_report_text(card["label"], item_wrap),
            transform=ax.transAxes,
            ha="left",
            va="top",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(label_size),
        )
        ax.text(
            text_x,
            bottom + (top - bottom) * 0.50,
            card["value"],
            transform=ax.transAxes,
            ha="left",
            va="center",
            color=PDF_COLORS["text"],
            fontproperties=pdf_font(value_size, "bold"),
        )
        ax.text(
            text_x,
            bottom + 0.12,
            wrap_report_text(card["subtitle"], subtitle_wrap),
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            linespacing=1.25,
            color=PDF_COLORS["subtle"],
            fontproperties=pdf_font(subtitle_size),
        )


def build_dashboard_cards(report: dict[str, Any], config: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    report_kind = report["meta"]["report_kind"]
    comparisons = report.get("kpi_comparisons", {})
    metrics = [
        ("pv", labels["pv"], PDF_COLORS["blue"]),
        ("uv", labels["uv"], PDF_COLORS["green"]),
        ("unique_ips", labels["ips"], PDF_COLORS["teal"]),
        ("request_count", labels["requests"], PDF_COLORS["sky"]),
        ("total_traffic_bytes", labels["total_traffic"], PDF_COLORS["orange"]),
        ("spider_total", labels["spider_total"], PDF_COLORS["purple"]),
    ]
    cards = []
    for key, title, accent in metrics:
        cards.append(
            {
                "label": title,
                "value": format_kpi_value(key, kpi_metric_value(report, key)),
                "subtitle": format_compare_subtitle(config, report_kind, key, comparisons.get(key)),
                "accent": accent,
            }
        )
    return cards


def build_system_summary_cards(report: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    system = report.get("system", {})
    traffic = report.get("traffic", {})
    security = security_snapshot(report)
    cpu_peak = traffic.get("cpu_peak", system.get("max_cpu_pct"))
    memory_peak = traffic.get("memory_peak", system.get("max_memory_pct"))
    disk_free = traffic.get("disk_free_min", system.get("min_disk_free_bytes"))
    report_kind = report["meta"]["report_kind"]

    cards = [
        {
            "label": labels["cpu"],
            "value": "N/A" if cpu_peak is None else f"{format_number(cpu_peak)}%",
            "subtitle": labels["kpi_cpu_subtitle"],
            "accent": PDF_COLORS["orange"],
        },
        {
            "label": labels["memory"],
            "value": "N/A" if memory_peak is None else f"{format_number(memory_peak)}%",
            "subtitle": labels["kpi_memory_subtitle"],
            "accent": PDF_COLORS["green"],
        },
        {
            "label": labels["disk"],
            "value": format_bytes(disk_free),
            "subtitle": labels["kpi_disk_subtitle"],
            "accent": PDF_COLORS["blue"],
        },
    ]
    if report_kind == "monthly":
        cards.extend(
            [
                {
                    "label": labels["avg_response"],
                    "value": "N/A"
                    if traffic.get("avg_response_ms") is None
                    else f"{format_number(traffic['avg_response_ms'])} ms",
                    "subtitle": labels["kpi_response_subtitle"],
                    "accent": PDF_COLORS["teal"],
                },
                {
                    "label": labels["slow_requests"],
                    "value": format_number(traffic.get("slow_request_count")),
                    "subtitle": labels["kpi_slow_subtitle"],
                    "accent": PDF_COLORS["red"],
                },
                {
                    "label": labels["security_5xx"],
                    "value": format_number(security["http_5xx_count"]),
                    "subtitle": labels["security_overview"],
                    "accent": PDF_COLORS["purple"],
                },
            ]
        )
    else:
        cards.extend(
            [
                {
                    "label": labels["security_404"],
                    "value": format_number(security["http_404_count"]),
                    "subtitle": labels["security_overview"],
                    "accent": PDF_COLORS["orange"],
                },
                {
                    "label": labels["security_5xx"],
                    "value": format_number(security["http_5xx_count"]),
                    "subtitle": labels["security_overview"],
                    "accent": PDF_COLORS["red"],
                },
                {
                    "label": labels["security_bad_ips"],
                    "value": format_number(security["suspicious_ip_count"]),
                    "subtitle": labels["security_overview"],
                    "accent": PDF_COLORS["purple"],
                },
            ]
        )
    return cards


def draw_summary_strip(ax: Any, title: str, cards: list[dict[str, str]]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(
        0.0,
        0.98,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(10.2, "bold"),
    )
    ax.plot([0.0, 1.0], [0.83, 0.83], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.8)
    draw_metric_segments(
        ax,
        cards,
        bottom=0.10,
        top=0.80,
        label_size=7.7,
        value_size=12.8,
        subtitle_size=7.0,
        item_wrap=10,
        subtitle_wrap=13,
    )


def draw_report_pie(ax: Any, title: str, items: list[dict[str, Any]], colors: list[str], labels: dict[str, str]) -> None:
    ax.set_facecolor(PDF_COLORS["panel"])
    for spine in ax.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(0.8)
    ax.set_title(title, loc="left", pad=10, color=PDF_COLORS["text"], fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    if not items:
        ax.text(
            0.5,
            0.5,
            labels["no_data"],
            transform=ax.transAxes,
            ha="center",
            va="center",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(8.5),
        )
        return
    values = [max(int(item["count"]), 0) for item in items]
    legend_labels = [
        f"{truncate_text(localize_chart_item(str(item['item']), labels), 16)}  {format_number(item['count'])}"
        for item in items
    ]
    wedges, _ = ax.pie(
        values,
        labels=None,
        colors=colors[: len(items)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.33, "edgecolor": PDF_COLORS["panel"], "linewidth": 1.2},
        radius=0.84,
    )
    total = sum(values)
    ax.text(0.0, 0.06, format_number(total), ha="center", va="center", color=PDF_COLORS["text"], fontproperties=pdf_font(12.2, "bold"))
    ax.text(0.0, -0.14, labels["count"], ha="center", va="center", color=PDF_COLORS["muted"], fontproperties=pdf_font(7.6))
    legend = ax.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(0.82, 0.5),
        frameon=False,
        prop=pdf_font(7.4),
        labelcolor=PDF_COLORS["muted"],
        handlelength=1.0,
    )
    for text in legend.get_texts():
        text.set_color(PDF_COLORS["muted"])
    ax.axis("equal")


def draw_daily_trend_chart(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    style_report_axis(ax, labels["daily_hourly_trend"])
    series = report["hourly_series"]
    hours = [item["hour"] for item in series]
    pv_values = [float(item["pv"]) for item in series]
    request_values = [float(item["request_count"]) for item in series]
    x_positions = list(range(len(hours)))
    ax.plot(x_positions, pv_values, color=PDF_COLORS["blue"], linewidth=1.9, marker="o", markersize=2.8, label=labels["pv"], zorder=3)
    ax.fill_between(x_positions, pv_values, color=PDF_COLORS["blue"], alpha=0.08, zorder=1)
    point_sizes = [12 + math.sqrt(max(value, 0.0) + 1.0) * 2.8 for value in request_values]
    ax.scatter(
        x_positions,
        pv_values,
        s=point_sizes,
        c=request_values,
        cmap="Blues",
        alpha=0.92,
        edgecolors=PDF_COLORS["panel"],
        linewidths=0.4,
        zorder=4,
    )
    ax.plot(x_positions, request_values, color=PDF_COLORS["green"], linewidth=1.4, alpha=0.55, label=labels["requests"], zorder=2)
    set_report_xticks(ax, [f"{hour:02d}:00" for hour in hours], 8, rotation=28)
    ax.margins(x=0.01)
    legend = ax.legend(frameon=False, loc="upper left", prop=pdf_font(7.8))
    for text in legend.get_texts():
        text.set_color(PDF_COLORS["muted"])


def draw_period_trend_chart(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    report_kind = report["meta"]["report_kind"]
    title = labels["trend_pv_uv"] if report_kind == "weekly" else labels["trend_30d"]
    style_report_axis(ax, title)
    series = report["traffic_series"]
    x_positions = list(range(len(series)))
    date_labels = [item["date"][5:] for item in series]
    pv_values = [float(item["pv"]) for item in series]
    uv_values = [float(item["uv"]) for item in series]
    if report_kind == "monthly":
        pv_values = moving_average(pv_values, 3)
        uv_values = moving_average(uv_values, 3)
    ax.plot(x_positions, pv_values, color=PDF_COLORS["blue"], linewidth=1.9, marker="o", markersize=3.0, label=labels["pv"])
    ax.fill_between(x_positions, pv_values, color=PDF_COLORS["blue"], alpha=0.08)
    ax.plot(x_positions, uv_values, color=PDF_COLORS["green"], linewidth=1.7, marker="o", markersize=2.7, label=labels["uv"])
    set_report_xticks(ax, date_labels, 7 if report_kind == "weekly" else 8, rotation=28)
    ax.margins(x=0.02)
    legend = ax.legend(frameon=False, loc="upper left", prop=pdf_font(7.8))
    for text in legend.get_texts():
        text.set_color(PDF_COLORS["muted"])


def draw_monthly_resource_trend(ax: Any, report: dict[str, Any], labels: dict[str, str]) -> None:
    style_report_axis(ax, labels["cpu_disk_trend"])
    series = report["traffic_series"]
    x_positions = list(range(len(series)))
    date_labels = [item["date"][5:] for item in series]
    cpu_values = [float(item["cpu_peak"] or 0.0) for item in series]
    disk_values = [float(item["disk_free_bytes"] or 0.0) / (1024 ** 3) for item in series]
    ax.plot(x_positions, cpu_values, color=PDF_COLORS["orange"], linewidth=1.8, marker="o", markersize=2.8, label=labels["resource_cpu"])
    ax.fill_between(x_positions, cpu_values, color=PDF_COLORS["orange"], alpha=0.08)
    ax.set_ylabel(labels["resource_cpu"], color=PDF_COLORS["orange"], fontproperties=pdf_font(7.8))
    ax_right = ax.twinx()
    ax_right.plot(x_positions, disk_values, color=PDF_COLORS["blue"], linewidth=1.7, marker="s", markersize=2.5, label=labels["resource_disk"])
    ax_right.set_ylabel(labels["resource_disk"], color=PDF_COLORS["blue"], fontproperties=pdf_font(7.8))
    ax_right.grid(False)
    ax_right.tick_params(axis="y", length=0, pad=6, colors=PDF_COLORS["muted"])
    for spine in ax_right.spines.values():
        spine.set_color(PDF_COLORS["border"])
        spine.set_linewidth(0.8)
    set_report_xticks(ax, date_labels, 8, rotation=28)
    apply_axis_tick_fonts(ax_right, 8.0)
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(left_handles + right_handles, left_labels + right_labels, frameon=False, loc="upper left", prop=pdf_font(7.5))
    for text in legend.get_texts():
        text.set_color(PDF_COLORS["muted"])


def build_ranked_rows(items: list[dict[str, Any]], metric_formatter: Any, item_limit: int = 24) -> list[list[str]]:
    rows = []
    for index, item in enumerate(items):
        rows.append(
            [
                str(index + 1),
                truncate_text(str(item["item"]), item_limit),
                metric_formatter(item["count"]),
            ]
        )
    return rows


def draw_report_table(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float] | None = None,
    empty_text: str = "No data",
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(
        0.0,
        0.98,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=PDF_COLORS["text"],
        fontproperties=pdf_font(10.0, "bold"),
    )
    ax.plot([0.0, 1.0], [0.90, 0.90], transform=ax.transAxes, color=PDF_COLORS["divider"], linewidth=0.8)
    if not rows:
        ax.text(
            0.5,
            0.48,
            empty_text,
            transform=ax.transAxes,
            ha="center",
            va="center",
            color=PDF_COLORS["muted"],
            fontproperties=pdf_font(8.4),
        )
        return
    table = ax.table(
        cellText=rows,
        colLabels=headers,
        bbox=[0.0, 0.02, 1.0, 0.83],
        cellLoc="left",
        colLoc="left",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.7)
    table.scale(1.0, 1.12 if len(rows) >= 9 else 1.18)
    for (row_index, column_index), cell in table.get_celld().items():
        cell.set_edgecolor(PDF_COLORS["border"])
        cell.set_linewidth(0.45)
        cell.get_text().set_wrap(False)
        if row_index == 0:
            cell.set_facecolor("#e8f0ff")
            cell.get_text().set_color(PDF_COLORS["text"])
            cell.get_text().set_fontproperties(pdf_font(7.8, "bold"))
        else:
            cell.set_facecolor(PDF_COLORS["panel_alt"] if row_index % 2 == 1 else PDF_COLORS["panel"])
            cell.get_text().set_color(PDF_COLORS["text"])
            cell.get_text().set_fontproperties(pdf_font(7.6))
        if column_index == 0:
            cell.get_text().set_ha("center")
        elif column_index == len(headers) - 1:
            cell.get_text().set_ha("right")


def render_detail_page(fig: Any, report: dict[str, Any], labels: dict[str, str], generated_at: str) -> None:
    report_kind = report["meta"]["report_kind"]
    total_pages = 2
    if report_kind == "monthly":
        grid = fig.add_gridspec(5, 12, height_ratios=[0.72, 0.95, 1.30, 3.05, 3.05])
        resource_row = 2
        top_row = 3
        bottom_row = 4
    else:
        grid = fig.add_gridspec(4, 12, height_ratios=[0.72, 0.95, 3.30, 3.30])
        resource_row = None
        top_row = 2
        bottom_row = 3

    draw_page_header(
        fig.add_subplot(grid[0, :]),
        report,
        labels,
        f"{labels[f'{report_kind}_title']} | {labels['details_page']}",
        generated_at,
        2,
        total_pages,
    )
    draw_summary_strip(fig.add_subplot(grid[1, :]), labels["system_overview"], build_system_summary_cards(report, labels))
    if resource_row is not None:
        draw_monthly_resource_trend(fig.add_subplot(grid[resource_row, :]), report, labels)

    draw_report_table(
        fig.add_subplot(grid[top_row, 0:6]),
        labels["top_uris"],
        [labels["rank"], labels["item"], labels["count"]],
        build_ranked_rows(report["top_uris"], lambda value: format_number(value), 24),
        [0.12, 0.63, 0.25],
        labels["no_data"],
    )
    draw_report_table(
        fig.add_subplot(grid[top_row, 6:12]),
        labels["slow_routes"],
        [labels["rank"], labels["item"], labels["count"]],
        build_ranked_rows(report["slow_routes"], lambda value: format_number(value), 24),
        [0.12, 0.63, 0.25],
        labels["no_data"],
    )
    draw_report_table(
        fig.add_subplot(grid[bottom_row, 0:6]),
        labels["abnormal_ips"],
        [labels["rank"], labels["item"], labels["rpm"]],
        build_ranked_rows(report["abnormal_ips"], lambda value: format_number(value), 18),
        [0.12, 0.50, 0.38],
        labels["no_data"],
    )
    draw_report_table(
        fig.add_subplot(grid[bottom_row, 6:12]),
        labels["top_errors"],
        [labels["rank"], labels["item"], labels["count"]],
        build_ranked_rows(report["top_errors"], lambda value: format_number(value), 28),
        [0.12, 0.63, 0.25],
        labels["no_data"],
    )


def build_baota_daily_demo(report: dict[str, Any]) -> dict[str, Any]:
    site = report.get("meta", {}).get("site") or "demo.server-mate.local"
    window_start = report.get("meta", {}).get("window_start") or "2026-03-25T00:00:00+08:00"
    window_end = report.get("meta", {}).get("window_end") or "2026-03-26T00:00:00+08:00"
    return {
        "title": "网站监控报表",
        "site": site,
        "window": f"{window_start} - {window_end}",
        "total_requests": "73,822",
        "total_traffic": "4.03 GB",
        "kpis": [
            {"label": "浏览量(PV)", "value": "17,421", "compare": "15,212"},
            {"label": "访客数(UV)", "value": "10,684", "compare": "9,832"},
            {"label": "IP数", "value": "7,956", "compare": "7,214"},
            {"label": "请求", "value": "73,822", "compare": "69,540"},
            {"label": "流量", "value": "4.03 GB", "compare": "3.81 GB"},
            {"label": "蜘蛛爬虫", "value": "8,917", "compare": "8,204"},
        ],
        "hour_labels": [f"{hour}:00" for hour in range(24)],
        "trend": {
            "pv": [480, 430, 390, 360, 320, 310, 420, 780, 1290, 1650, 1490, 1370, 1280, 1450, 1710, 1960, 2080, 1910, 1740, 1670, 1830, 1710, 1320, 860],
            "uv": [240, 212, 190, 170, 162, 155, 188, 362, 618, 790, 742, 701, 655, 690, 760, 835, 884, 826, 770, 733, 768, 742, 604, 428],
            "ip": [196, 182, 168, 150, 138, 132, 154, 294, 472, 598, 572, 546, 528, 551, 606, 653, 691, 664, 621, 598, 614, 603, 497, 352],
        },
        "performance": {
            "qps": [1.4, 1.2, 1.0, 0.9, 0.8, 0.7, 1.1, 2.2, 3.9, 4.8, 4.4, 4.0, 3.6, 4.1, 4.5, 5.2, 5.6, 5.1, 4.6, 4.2, 4.8, 4.5, 3.2, 2.1],
            "response_ms": [210, 205, 198, 192, 188, 186, 194, 228, 312, 428, 396, 372, 348, 360, 388, 446, 492, 460, 418, 402, 436, 410, 318, 264],
        },
        "network": {
            "upload_kb": [26, 24, 22, 20, 19, 18, 21, 35, 58, 92, 86, 82, 78, 84, 96, 118, 132, 125, 116, 110, 124, 118, 88, 54],
            "download_kb": [148, 136, 122, 116, 105, 101, 128, 236, 422, 618, 584, 560, 532, 574, 646, 732, 804, 760, 706, 684, 742, 711, 524, 338],
        },
        "spiders": {
            "Googlebot": 3620,
            "Baiduspider": 2310,
            "Bingbot": 1186,
            "Sogou": 904,
            "其他": 897,
        },
        "statuses": {
            "200": 66194,
            "301": 2842,
            "302": 1016,
            "403": 384,
            "404": 2451,
            "500": 516,
            "502": 419,
        },
        "uri_rows": [
            [1, "/api/orders/list", "2,846", "1,052", "4,918", "426.4 MB"],
            [2, "/api/orders/detail", "2,431", "988", "4,205", "388.1 MB"],
            [3, "/checkout/confirm", "1,952", "874", "3,742", "305.7 MB"],
            [4, "/product/sku/20260325", "1,846", "805", "3,514", "296.8 MB"],
            [5, "/search?q=server-mate", "1,575", "742", "3,008", "254.1 MB"],
            [6, "/campaign/spring-sale", "1,382", "654", "2,774", "231.6 MB"],
            [7, "/robots.txt", "1,164", "112", "2,468", "42.9 MB"],
            [8, "/wp-login.php", "954", "88", "2,241", "31.8 MB"],
            [9, "/assets/banner-hero.jpg", "882", "644", "1,962", "188.7 MB"],
            [10, "/favicon.ico", "774", "561", "1,734", "24.6 MB"],
        ],
        "ip_rows": [
            [1, "203.0.113.28", "CN/Shanghai", "1,264", "2,318", "186.2 MB"],
            [2, "198.51.100.42", "US/San Jose", "1,148", "2,106", "174.4 MB"],
            [3, "203.0.113.77", "CN/Beijing", "1,082", "1,984", "162.5 MB"],
            [4, "192.0.2.66", "JP/Tokyo", "1,036", "1,912", "154.1 MB"],
            [5, "203.0.113.101", "SG/Singapore", "996", "1,864", "149.3 MB"],
            [6, "198.51.100.18", "CN/Hangzhou", "942", "1,780", "142.6 MB"],
            [7, "203.0.113.125", "HK/Hong Kong", "904", "1,706", "136.9 MB"],
            [8, "192.0.2.140", "CN/Guangzhou", "882", "1,642", "132.4 MB"],
            [9, "198.51.100.205", "DE/Frankfurt", "846", "1,584", "128.7 MB"],
            [10, "203.0.113.211", "CN/Shenzhen", "812", "1,528", "124.1 MB"],
        ],
        "referer_rows": [
            [1, "https://www.baidu.com/", "3,912", "7,864", "418.6 MB"],
            [2, "https://www.google.com/", "3,264", "6,952", "392.2 MB"],
            [3, "https://cn.bing.com/", "1,826", "3,608", "188.4 MB"],
            [4, "https://m.weibo.cn/", "1,542", "3,204", "174.7 MB"],
            [5, "https://mp.weixin.qq.com/", "1,308", "2,846", "166.5 MB"],
            [6, "https://www.zhihu.com/", "1,126", "2,410", "152.2 MB"],
            [7, "https://news.qq.com/", "962", "2,136", "144.8 MB"],
            [8, "https://partner.example.com/", "884", "1,962", "139.7 MB"],
            [9, "直接访问", "806", "1,744", "126.3 MB"],
            [10, "其他来源", "742", "1,538", "112.6 MB"],
        ],
    }


def create_baota_daily_figure() -> Any:
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    fig.subplots_adjust(left=0.075, right=0.925, top=0.985, bottom=0.04, hspace=0.58, wspace=0.42)
    return fig


def apply_bt_axis_style(ax: Any, title: str) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#111111", fontproperties=pdf_font(10.5, "bold"))
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, color="#EEEEEE")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=4, colors="#666666", labelsize=7.6)
    apply_axis_tick_fonts(ax, 7.4)


def draw_baota_header(ax: Any, report: dict[str, Any], demo: dict[str, Any], generated_at: str, page_number: int, total_pages: int) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 0.90, demo["title"], ha="left", va="top", color="#111111", fontproperties=pdf_font(15.5, "bold"), transform=ax.transAxes)
    ax.text(0.0, 0.54, demo["site"], ha="left", va="top", color="#666666", fontproperties=pdf_font(8.6), transform=ax.transAxes)
    ax.text(0.0, 0.23, demo["window"], ha="left", va="top", color="#666666", fontproperties=pdf_font(7.8), transform=ax.transAxes)
    ax.text(1.0, 0.82, f"总请求: {demo['total_requests']}", ha="right", va="top", color="#111111", fontproperties=pdf_font(9.6, "bold"), transform=ax.transAxes)
    ax.text(1.0, 0.48, f"总流量: {demo['total_traffic']}", ha="right", va="top", color="#111111", fontproperties=pdf_font(9.6, "bold"), transform=ax.transAxes)
    ax.text(1.0, 0.18, f"第 {page_number} / {total_pages} 页  生成时间: {generated_at}", ha="right", va="top", color="#888888", fontproperties=pdf_font(7.2), transform=ax.transAxes)
    ax.plot([0.0, 1.0], [0.02, 0.02], transform=ax.transAxes, color="#EAEAEA", linewidth=0.9)


def draw_baota_kpis(ax: Any, cards: list[dict[str, str]]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    segment_width = 1.0 / len(cards)
    for index, card in enumerate(cards):
        left = index * segment_width
        text_x = left + segment_width * 0.08
        if index > 0:
            ax.plot([left, left], [0.18, 0.85], transform=ax.transAxes, color="#F0F0F0", linewidth=0.8)
        ax.text(text_x, 0.82, card["label"], ha="left", va="top", color="#666666", fontproperties=pdf_font(8.2), transform=ax.transAxes)
        ax.text(text_x, 0.48, card["value"], ha="left", va="center", color="#111111", fontproperties=pdf_font(15.6, "bold"), transform=ax.transAxes)
        ax.text(text_x, 0.18, card["compare"], ha="left", va="bottom", color="#888888", fontproperties=pdf_font(7.2), transform=ax.transAxes)


def draw_baota_three_line_chart(ax: Any, demo: dict[str, Any]) -> None:
    apply_bt_axis_style(ax, "24小时趋势主图")
    x_positions = list(range(24))
    ax.plot(x_positions, demo["trend"]["pv"], color="#2563EB", linewidth=1.8, marker="o", markersize=2.4, label="PV")
    ax.plot(x_positions, demo["trend"]["uv"], color="#10B981", linewidth=1.6, marker="o", markersize=2.2, label="UV")
    ax.plot(x_positions, demo["trend"]["ip"], color="#F59E0B", linewidth=1.5, marker="o", markersize=2.1, label="IP数")
    ax.set_xlim(-0.3, 23.3)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([demo["hour_labels"][index] for index in range(0, 24, 2)], rotation=0, ha="center")
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(7.6), ncol=3, handlelength=1.8)
    for text in legend.get_texts():
        text.set_color("#666666")


def draw_baota_dual_axis_chart(ax: Any, title: str, x_labels: list[str], left_series: list[float], right_series: list[float], left_label: str, right_label: str, left_color: str, right_color: str) -> None:
    apply_bt_axis_style(ax, title)
    x_positions = list(range(len(x_labels)))
    ax.plot(x_positions, left_series, color=left_color, linewidth=1.7, marker="o", markersize=2.2, label=left_label)
    ax.set_xlim(-0.2, len(x_labels) - 0.8)
    ax.set_xticks(range(0, len(x_labels), 3))
    ax.set_xticklabels([x_labels[index] for index in range(0, len(x_labels), 3)], rotation=0, ha="center")
    ax_right = ax.twinx()
    ax_right.set_facecolor("#FFFFFF")
    ax_right.plot(x_positions, right_series, color=right_color, linewidth=1.7, marker="o", markersize=2.2, label=right_label)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.grid(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#666666", labelsize=7.2)
    apply_axis_tick_fonts(ax_right, 7.2)
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(left_handles + right_handles, left_labels + right_labels, loc="upper left", frameon=False, prop=pdf_font(7.0))
    for text in legend.get_texts():
        text.set_color("#666666")


def draw_baota_donut(ax: Any, title: str, data: dict[str, int], colors: list[str]) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#111111", fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    labels = list(data.keys())
    values = list(data.values())
    wedges, _ = ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.34, "edgecolor": "#FFFFFF", "linewidth": 1.4},
        radius=0.90,
    )
    ax.text(0.0, 0.06, format_number(sum(values)), ha="center", va="center", color="#111111", fontproperties=pdf_font(11.2, "bold"))
    ax.text(0.0, -0.12, "总量", ha="center", va="center", color="#888888", fontproperties=pdf_font(7.2))
    legend_labels = [f"{label}  {format_number(value)}" for label, value in data.items()]
    legend = ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(0.78, 0.5), frameon=False, prop=pdf_font(7.0), handlelength=1.0)
    for text in legend.get_texts():
        text.set_color("#666666")
    ax.axis("equal")


def draw_baota_table(ax: Any, title: str, headers: list[str], rows: list[list[Any]], col_widths: list[float]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 1.02, title, ha="left", va="bottom", color="#111111", fontproperties=pdf_font(10.3, "bold"), transform=ax.transAxes)
    table = ax.table(
        cellText=[[str(value) for value in row] for row in rows],
        colLabels=headers,
        bbox=[0.0, 0.00, 1.0, 0.96],
        cellLoc="left",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.4)
    table.scale(1.0, 1.02)
    for (row_index, column_index), cell in table.get_celld().items():
        cell.set_linewidth(0.5)
        cell.set_edgecolor("#E5E7EB")
        if row_index == 0:
            cell.set_facecolor("#22C55E")
            cell.get_text().set_color("#FFFFFF")
            cell.get_text().set_fontproperties(pdf_font(6.6, "bold"))
            cell.get_text().set_ha("center")
        else:
            cell.set_facecolor("#FFFFFF" if row_index % 2 == 0 else "#FAFAFA")
            cell.get_text().set_color("#222222")
            cell.get_text().set_fontproperties(pdf_font(6.2))
            if column_index == 0:
                cell.get_text().set_ha("center")
            elif column_index == len(headers) - 1:
                cell.get_text().set_ha("right")
            else:
                cell.get_text().set_ha("left")


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    demo = build_baota_daily_demo(report)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(5, 12, height_ratios=[0.80, 0.90, 1.75, 1.62, 1.55])
        draw_baota_header(page_one.add_subplot(grid_one[0, :]), report, demo, generated_at, 1, 2)
        draw_baota_kpis(page_one.add_subplot(grid_one[1, :]), demo["kpis"])
        draw_baota_three_line_chart(page_one.add_subplot(grid_one[2, :]), demo)
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[3, 0:6]),
            "性能/负载",
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[3, 6:12]),
            "网站流量",
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB",
            "下行 KB",
            "#F59E0B",
            "#10B981",
        )
        draw_baota_donut(page_one.add_subplot(grid_one[4, 0:6]), "蜘蛛统计", demo["spiders"], ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"])
        draw_baota_donut(page_one.add_subplot(grid_one[4, 6:12]), "状态码统计", demo["statuses"], ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"])
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        grid_two = page_two.add_gridspec(4, 1, height_ratios=[0.72, 2.48, 2.48, 2.48])
        draw_baota_header(page_two.add_subplot(grid_two[0, :]), report, demo, generated_at, 2, 2)
        draw_baota_table(
            page_two.add_subplot(grid_two[1, :]),
            "热门 URI Top 10",
            ["#", "URI", "PV", "UV", "请求数", "流量"],
            demo["uri_rows"],
            [0.06, 0.45, 0.10, 0.10, 0.12, 0.17],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[2, :]),
            "热门 IP Top 10",
            ["#", "IP", "地区", "PV", "请求数", "流量"],
            demo["ip_rows"],
            [0.06, 0.20, 0.22, 0.12, 0.17, 0.23],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[3, :]),
            "热门来源 Referer Top 10",
            ["#", "Referer", "PV", "请求数", "流量"],
            demo["referer_rows"],
            [0.06, 0.50, 0.10, 0.14, 0.20],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)
    return output_path


def render_standard_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    labels = TRANSLATIONS[report_language(config)]
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")

    with PdfPages(output_path) as pdf:
        overview = create_pdf_figure()
        overview_grid = overview.add_gridspec(5, 12, height_ratios=[0.72, 1.22, 0.98, 1.72, 2.45])
        draw_page_header(
            overview.add_subplot(overview_grid[0, :]),
            report,
            labels,
            f"{labels[report['meta']['report_kind'] + '_title']} | {labels['dashboard_page']}",
            generated_at,
            1,
            2,
        )
        draw_ai_summary_box(overview.add_subplot(overview_grid[1, :]), report, labels)
        draw_metric_segments(
            overview.add_subplot(overview_grid[2, :]),
            build_dashboard_cards(report, config, labels),
            bottom=0.08,
            top=0.88,
            label_size=8.0,
            value_size=15.8,
            subtitle_size=7.0,
            item_wrap=8,
            subtitle_wrap=12,
        )

        trend_axis = overview.add_subplot(overview_grid[3, :])
        if report["meta"]["report_kind"] == "daily":
            draw_daily_trend_chart(trend_axis, report, labels)
        else:
            draw_period_trend_chart(trend_axis, report, labels)

        draw_report_pie(
            overview.add_subplot(overview_grid[4, 0:6]),
            labels["spider_distribution"],
            build_spider_chart_data(report["spiders"]),
            [PDF_COLORS["blue"], PDF_COLORS["green"], PDF_COLORS["purple"], PDF_COLORS["orange"], PDF_COLORS["gray"]],
            labels,
        )
        draw_report_pie(
            overview.add_subplot(overview_grid[4, 6:12]),
            labels["http_status_mix"],
            build_status_chart_data(report["status_codes"]),
            [PDF_COLORS["green"], PDF_COLORS["sky"], PDF_COLORS["orange"], PDF_COLORS["red"], PDF_COLORS["gray"]],
            labels,
        )
        pdf.savefig(overview, facecolor="#FFFFFF")
        plt.close(overview)

        detail_page = create_pdf_figure()
        render_detail_page(detail_page, report, labels, generated_at)
        pdf.savefig(detail_page, facecolor="#FFFFFF")
        plt.close(detail_page)

    return output_path


def render_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    if plt is None or PdfPages is None or FancyBboxPatch is None or font_manager is None:
        raise RuntimeError("matplotlib is not installed; install it first to generate PDF reports.")

    setup_pdf_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if report["meta"]["report_kind"] == "daily":
        return render_baota_daily_pdf(report, config, output_path)
    return render_standard_pdf(report, config, output_path)


def parse_demo_metric(value: str) -> float | None:
    cleaned = "".join(char for char in str(value) if char.isdigit() or char == ".")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def format_demo_compare(current: str, previous: str) -> str:
    current_value = parse_demo_metric(current)
    previous_value = parse_demo_metric(previous)
    if current_value is None or previous_value is None:
        return previous
    arrow = "↑" if current_value >= previous_value else "↓"
    return f"{arrow} {previous}"


def apply_bt_axis_style(ax: Any, title: str) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#111111", fontproperties=pdf_font(10.5, "bold"))
    ax.grid(True, axis="y", linestyle="--", linewidth=0.5, color="#E0E0E0")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=4, colors="#666666", labelsize=7.6)
    apply_axis_tick_fonts(ax, 7.4)


def draw_baota_kpis(ax: Any, cards: list[dict[str, str]]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    segment_width = 1.0 / len(cards)
    for index, card in enumerate(cards):
        left = index * segment_width
        text_x = left + segment_width * 0.08
        if index > 0:
            ax.plot([left, left], [0.16, 0.86], transform=ax.transAxes, color="#ECECEC", linewidth=0.9)
        ax.text(text_x, 0.82, card["label"], ha="left", va="top", color="#666666", fontproperties=pdf_font(8.2), transform=ax.transAxes)
        ax.text(text_x, 0.48, card["value"], ha="left", va="center", color="#111111", fontproperties=pdf_font(15.6, "bold"), transform=ax.transAxes)
        ax.text(
            text_x,
            0.18,
            format_demo_compare(card["value"], card["compare"]),
            ha="left",
            va="bottom",
            color="#888888",
            fontproperties=pdf_font(6.9),
            transform=ax.transAxes,
        )


def draw_baota_three_line_chart(ax: Any, demo: dict[str, Any]) -> None:
    apply_bt_axis_style(ax, "24小时趋势主图")
    x_positions = list(range(24))
    pv_values = demo["trend"]["pv"]
    uv_values = demo["trend"]["uv"]
    ip_values = demo["trend"]["ip"]
    ax.plot(x_positions, pv_values, color="#2563EB", linewidth=1.5, label="PV")
    ax.fill_between(x_positions, pv_values, color="#2563EB", alpha=0.12)
    ax.plot(x_positions, uv_values, color="#10B981", linewidth=1.5, label="UV")
    ax.fill_between(x_positions, uv_values, color="#10B981", alpha=0.10)
    ax.plot(x_positions, ip_values, color="#F59E0B", linewidth=1.4, label="IP数")
    ax.fill_between(x_positions, ip_values, color="#F59E0B", alpha=0.08)
    ax.set_xlim(-0.3, 23.3)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([demo["hour_labels"][index] for index in range(0, 24, 2)], rotation=0, ha="center")
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(7.6), ncol=3, handlelength=1.8)
    for text in legend.get_texts():
        text.set_color("#666666")


def draw_baota_dual_axis_chart(
    ax: Any,
    title: str,
    x_labels: list[str],
    left_series: list[float],
    right_series: list[float],
    left_label: str,
    right_label: str,
    left_color: str,
    right_color: str,
) -> None:
    apply_bt_axis_style(ax, title)
    x_positions = list(range(len(x_labels)))
    ax.plot(x_positions, left_series, color=left_color, linewidth=1.5, label=left_label)
    ax.fill_between(x_positions, left_series, color=left_color, alpha=0.12)
    ax.set_xlim(-0.2, len(x_labels) - 0.8)
    ax.set_xticks(range(0, len(x_labels), 3))
    ax.set_xticklabels([x_labels[index] for index in range(0, len(x_labels), 3)], rotation=0, ha="center")
    ax_right = ax.twinx()
    ax_right.set_facecolor("#FFFFFF")
    ax_right.plot(x_positions, right_series, color=right_color, linewidth=1.5, label=right_label)
    ax_right.fill_between(x_positions, right_series, color=right_color, alpha=0.10)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.grid(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#666666", labelsize=7.2)
    apply_axis_tick_fonts(ax_right, 7.2)
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(left_handles + right_handles, left_labels + right_labels, loc="upper left", frameon=False, prop=pdf_font(7.0))
    for text in legend.get_texts():
        text.set_color("#666666")


def draw_baota_donut(ax: Any, title: str, data: dict[str, int], colors: list[str]) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#111111", fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    values = list(data.values())
    wedges, _ = ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.22, "edgecolor": "#FFFFFF", "linewidth": 1.2},
        radius=0.88,
    )
    ax.text(0.0, 0.08, format_number(sum(values)), ha="center", va="center", color="#111111", fontproperties=pdf_font(11.4, "bold"))
    ax.text(0.0, -0.08, "总量", ha="center", va="center", color="#888888", fontproperties=pdf_font(7.0))
    legend_labels = [f"{label}  {format_number(value)}" for label, value in data.items()]
    legend = ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(0.76, 0.5), frameon=False, prop=pdf_font(7.0), handlelength=0.9)
    for text in legend.get_texts():
        text.set_color("#666666")
    ax.axis("equal")


def draw_baota_table(ax: Any, title: str, headers: list[str], rows: list[list[Any]], col_widths: list[float]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 1.02, title, ha="left", va="bottom", color="#111111", fontproperties=pdf_font(10.3, "bold"), transform=ax.transAxes)
    table = ax.table(
        cellText=[[str(value) for value in row] for row in rows],
        colLabels=headers,
        bbox=[0.0, 0.00, 1.0, 0.96],
        cellLoc="left",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.4)
    table.scale(1.0, 1.14)
    for (row_index, column_index), cell in table.get_celld().items():
        cell.set_linewidth(0.45)
        cell.set_edgecolor("#EEF1F5")
        if row_index == 0:
            cell.visible_edges = "B"
            cell.set_facecolor("#F5F7FA")
            cell.get_text().set_color("#222222")
            cell.get_text().set_fontproperties(pdf_font(6.6, "bold"))
            cell.get_text().set_ha("center")
        else:
            cell.visible_edges = "B"
            cell.set_facecolor("#FFFFFF" if row_index % 2 == 0 else "#FAFAFA")
            cell.get_text().set_color("#222222")
            cell.get_text().set_fontproperties(pdf_font(6.2))
            if column_index == 0:
                cell.get_text().set_ha("center")
            elif column_index == len(headers) - 1:
                cell.get_text().set_ha("right")
            else:
                cell.get_text().set_ha("left")


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    demo = build_baota_daily_demo(report)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(5, 12, height_ratios=[0.80, 0.90, 1.75, 1.62, 1.55])
        draw_baota_header(page_one.add_subplot(grid_one[0, :]), report, demo, generated_at, 1, 2)
        draw_baota_kpis(page_one.add_subplot(grid_one[1, :]), demo["kpis"])
        draw_baota_three_line_chart(page_one.add_subplot(grid_one[2, :]), demo)
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[3, 0:6]),
            "性能/负载",
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[3, 6:12]),
            "网站流量",
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB",
            "下行 KB",
            "#F59E0B",
            "#10B981",
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[4, 0:6]),
            "蜘蛛统计",
            demo["spiders"],
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"],
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[4, 6:12]),
            "状态码统计",
            demo["statuses"],
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"],
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        grid_two = page_two.add_gridspec(4, 1, height_ratios=[0.72, 2.48, 2.48, 2.48])
        draw_baota_header(page_two.add_subplot(grid_two[0, :]), report, demo, generated_at, 2, 2)
        draw_baota_table(
            page_two.add_subplot(grid_two[1, :]),
            "热门 URI Top 10",
            ["#", "URI", "PV", "UV", "请求数", "流量"],
            demo["uri_rows"],
            [0.06, 0.45, 0.10, 0.10, 0.12, 0.17],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[2, :]),
            "热门 IP Top 10",
            ["#", "IP", "地区", "PV", "请求数", "流量"],
            demo["ip_rows"],
            [0.06, 0.20, 0.22, 0.12, 0.17, 0.23],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[3, :]),
            "热门来源 Referer Top 10",
            ["#", "Referer", "PV", "请求数", "流量"],
            demo["referer_rows"],
            [0.06, 0.50, 0.10, 0.14, 0.20],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)
    return output_path


def report_kind_label(report_kind: str) -> str:
    return {"daily": "日报", "weekly": "周报", "monthly": "月报"}.get(report_kind, "报告")


def peak_qps_window(report: dict[str, Any]) -> str:
    hourly_series = report.get("hourly_series", [])
    if hourly_series:
        peak = max(hourly_series, key=lambda item: float(item.get("peak_qps") or 0.0))
        hour = int(peak.get("hour") or 0)
        next_hour = (hour + 1) % 24
        return f"{hour:02d}:00-{next_hour:02d}:00"
    return report.get("meta", {}).get("report_date") or "当前周期"


def build_ai_review_snapshot(report: dict[str, Any]) -> dict[str, Any]:
    traffic = report.get("traffic", {})
    system = report.get("system", {})
    security = security_snapshot(report)
    comparisons = report.get("kpi_comparisons", {})
    suspicious_top = report.get("abnormal_ips", [])
    slow_ratio = safe_ratio(
        int(traffic.get("slow_request_count") or 0),
        int(traffic.get("request_count") or 0),
    ) * 100.0
    suspicious = suspicious_top[0] if suspicious_top else None
    disk_free_bytes = traffic.get("disk_free_min", system.get("min_disk_free_bytes"))
    return {
        "report_kind": report_kind_label(report.get("meta", {}).get("report_kind", "daily")),
        "site": report.get("meta", {}).get("site"),
        "pv": int(traffic.get("pv") or 0),
        "uv": int(traffic.get("uv") or 0),
        "pv_change_pct": comparisons.get("pv", {}).get("ratio"),
        "uv_change_pct": comparisons.get("uv", {}).get("ratio"),
        "qps_peak": float(traffic.get("qps_peak") or 0.0),
        "qps_peak_time": peak_qps_window(report),
        "avg_response_ms": float(traffic.get("avg_response_ms") or 0.0),
        "slow_request_ratio_pct": round(slow_ratio, 2),
        "slow_request_count": int(traffic.get("slow_request_count") or 0),
        "http_5xx_count": int(security.get("http_5xx_count") or 0),
        "http_404_count": int(security.get("http_404_count") or 0),
        "suspicious_ip_top1": None
        if not suspicious
        else {
            "ip": suspicious.get("item"),
            "rpm": int(suspicious.get("count") or 0),
        },
        "cpu_peak_pct": float(traffic.get("cpu_peak", system.get("max_cpu_pct")) or 0.0),
        "memory_peak_pct": float(traffic.get("memory_peak", system.get("max_memory_pct")) or 0.0),
        "disk_free_gb": round((float(disk_free_bytes or 0.0)) / (1024 ** 3), 2),
    }


def build_ai_review_prompt(snapshot: dict[str, Any]) -> str:
    return (
        f"你是一个资深 Linux 运维专家。这是一份服务器的 {snapshot['report_kind']} 核心数据：\n"
        f"{json.dumps(snapshot, ensure_ascii=False, indent=2)}\n\n"
        "请你用专业、精炼的中文（约 150-200 字）总结当前的服务器健康状态、流量趋势，"
        "并针对异常指标（如有）给出 1-2 条具体的优化或排查建议。语气要客观、专业。"
    )


def request_ai_review(config: dict[str, Any], prompt: str) -> str | None:
    settings = resolve_ai_settings(config)
    if not settings["enabled"] or settings["simulate"] or not settings["endpoint"]:
        return None
    api_key = os.getenv(settings["api_key_env"])
    if not api_key:
        return None
    endpoint = settings["endpoint"].rstrip("/")
    if endpoint.endswith("/v1"):
        endpoint = endpoint + "/chat/completions"
    elif not endpoint.endswith("/chat/completions"):
        endpoint = endpoint + "/chat/completions"
    body = {
        "model": settings["model"],
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": "你是一名资深 Linux 运维专家和 SRE 助手。"},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=settings["timeout_seconds"]) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        return None


def simulated_ai_review(snapshot: dict[str, Any]) -> str:
    pv_change = snapshot.get("pv_change_pct")
    uv_change = snapshot.get("uv_change_pct")
    pv_trend = "小幅上升" if pv_change is not None and pv_change >= 0 else "有所回落"
    uv_trend = "稳中有升" if uv_change is not None and uv_change >= 0 else "略有波动"
    suspicious = snapshot.get("suspicious_ip_top1")
    suspicious_text = (
        f"当前未发现明显的高频异常 IP，整体访问分布较为均匀。"
        if not suspicious
        else f"可疑访问最高的来源 IP 为 {suspicious['ip']}，峰值约 {format_number(suspicious['rpm'])} RPM，建议结合黑名单或 WAF 策略持续观察。"
    )
    error_text = (
        f"5xx 错误累计 {format_number(snapshot['http_5xx_count'])} 次，404 累计 {format_number(snapshot['http_404_count'])} 次。"
        if snapshot["http_5xx_count"] or snapshot["http_404_count"]
        else "本周期未观察到明显的 4xx/5xx 异常峰值。"
    )
    return (
        f"本期整体流量表现为 {pv_trend}，PV/UV 分别为 {format_number(snapshot['pv'])} / {format_number(snapshot['uv'])}，"
        f"访客活跃度 {uv_trend}。峰值 QPS 出现在 {snapshot['qps_peak_time']}，达到 {format_number(snapshot['qps_peak'], 2)}；"
        f"平均响应约 {format_number(snapshot['avg_response_ms'], 2)} ms，慢请求占比 {format_number(snapshot['slow_request_ratio_pct'], 2)}%。"
        f"{error_text} 资源侧 CPU/内存峰值分别为 {format_number(snapshot['cpu_peak_pct'], 2)}% 和 {format_number(snapshot['memory_peak_pct'], 2)}%，"
        f"磁盘剩余约 {format_number(snapshot['disk_free_gb'], 2)} GB。建议优先关注 5xx 错误对应的上游链路与慢请求热点接口，"
        f"并结合高峰时段复查 Nginx/PHP-FPM 连接池配置。{suspicious_text}"
    )


def summarize_ai_review(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    snapshot = build_ai_review_snapshot(report)
    prompt = build_ai_review_prompt(snapshot)
    text = request_ai_review(config, prompt)
    source = "llm"
    if not text:
        text = simulated_ai_review(snapshot)
        source = "simulated"
    return {
        "title": "AI 智能运维点评",
        "summary": text,
        "snapshot": snapshot,
        "prompt": prompt,
        "source": source,
    }


def draw_ai_review_card(ax: Any, review: dict[str, Any]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel = FancyBboxPatch(
        (0.0, 0.02),
        1.0,
        0.94,
        boxstyle="round,pad=0.012,rounding_size=0.028",
        facecolor="#F4F8FB",
        edgecolor="none",
        transform=ax.transAxes,
    )
    ax.add_patch(panel)
    ax.text(
        0.03,
        0.82,
        review["title"],
        ha="left",
        va="top",
        color="#1D4ED8",
        fontproperties=pdf_font(10.2, "bold"),
        transform=ax.transAxes,
    )
    wrapped = "\n".join(
        textwrap.wrap(
            review["summary"],
            width=74,
            break_long_words=True,
            break_on_hyphens=False,
        )
    )
    ax.text(
        0.03,
        0.64,
        wrapped,
        ha="left",
        va="top",
        color="#334155",
        linespacing=1.42,
        fontproperties=pdf_font(7.9),
        transform=ax.transAxes,
    )


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    demo = build_baota_daily_demo(report)
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(6, 12, height_ratios=[0.76, 1.10, 0.82, 1.46, 1.34, 1.30])
        draw_baota_header(page_one.add_subplot(grid_one[0, :]), report, demo, generated_at, 1, 2)
        draw_ai_review_card(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis(page_one.add_subplot(grid_one[2, :]), demo["kpis"])
        draw_baota_three_line_chart(page_one.add_subplot(grid_one[3, :]), demo)
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[4, 0:6]),
            "性能/负载",
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[4, 6:12]),
            "网站流量",
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB",
            "下行 KB",
            "#F59E0B",
            "#10B981",
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[5, 0:6]),
            "蜘蛛统计",
            demo["spiders"],
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"],
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[5, 6:12]),
            "状态码统计",
            demo["statuses"],
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"],
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        grid_two = page_two.add_gridspec(4, 1, height_ratios=[0.72, 2.48, 2.48, 2.48])
        draw_baota_header(page_two.add_subplot(grid_two[0, :]), report, demo, generated_at, 2, 2)
        draw_baota_table(
            page_two.add_subplot(grid_two[1, :]),
            "热门 URI Top 10",
            ["#", "URI", "PV", "UV", "请求数", "流量"],
            demo["uri_rows"],
            [0.06, 0.45, 0.10, 0.10, 0.12, 0.17],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[2, :]),
            "热门 IP Top 10",
            ["#", "IP", "地区", "PV", "请求数", "流量"],
            demo["ip_rows"],
            [0.06, 0.20, 0.22, 0.12, 0.17, 0.23],
        )
        draw_baota_table(
            page_two.add_subplot(grid_two[3, :]),
            "热门来源 Referer Top 10",
            ["#", "Referer", "PV", "请求数", "流量"],
            demo["referer_rows"],
            [0.06, 0.50, 0.10, 0.14, 0.20],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)
    return output_path


def compact_table_text(value: Any, limit: int) -> str:
    return truncate_text(str(value), limit)


def build_compact_top_rows(rows: list[list[Any]], label_index: int, request_index: int, label_limit: int) -> list[list[str]]:
    compact_rows: list[list[str]] = []
    for row in rows[:10]:
        compact_rows.append(
            [
                str(row[0]),
                compact_table_text(row[label_index], label_limit),
                str(row[request_index]),
            ]
        )
    return compact_rows


def draw_baota_compact_table(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
) -> None:
    alignments = {0: "center"}
    if len(headers) >= 2:
        alignments[1] = "left"
    alignments[max(len(headers) - 1, 0)] = "center"
    draw_saas_table(
        ax,
        title,
        headers,
        rows,
        col_widths,
        title_align="left",
        font_size=7.2,
        header_font_size=7.8,
        title_font_size=10.3,
        row_height=0.084,
        bbox_height=0.96,
        alignments=alignments,
    )


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    demo = build_baota_daily_demo(report)
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(6, 12, height_ratios=[0.76, 1.10, 0.82, 1.46, 1.34, 1.30])
        draw_baota_header(page_one.add_subplot(grid_one[0, :]), report, demo, generated_at, 1, 2)
        draw_ai_review_card(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis(page_one.add_subplot(grid_one[2, :]), demo["kpis"])
        draw_baota_three_line_chart(page_one.add_subplot(grid_one[3, :]), demo)
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[4, 0:6]),
            "性能/负载",
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart(
            page_one.add_subplot(grid_one[4, 6:12]),
            "网站流量",
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB",
            "下行 KB",
            "#F59E0B",
            "#10B981",
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[5, 0:6]),
            "蜘蛛统计",
            demo["spiders"],
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"],
        )
        draw_baota_donut(
            page_one.add_subplot(grid_one[5, 6:12]),
            "状态码统计",
            demo["statuses"],
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"],
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        grid_two = page_two.add_gridspec(4, 1, height_ratios=[0.72, 2.42, 2.42, 2.42])
        draw_baota_header(page_two.add_subplot(grid_two[0, :]), report, demo, generated_at, 2, 2)
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[1, :]),
            "热门URL TOP 10",
            ["排名", "URL路径", "请求数"],
            build_compact_top_rows(demo["uri_rows"], 1, 4, 28),
            [0.16, 0.66, 0.18],
        )
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[2, :]),
            "热门IP TOP 10",
            ["排名", "IP地址", "请求数"],
            build_compact_top_rows(demo["ip_rows"], 1, 4, 24),
            [0.16, 0.66, 0.18],
        )
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[3, :]),
            "热门来源 TOP 10",
            ["排名", "Referer来源", "请求数"],
            build_compact_top_rows(demo["referer_rows"], 1, 3, 34),
            [0.16, 0.66, 0.18],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)
    return output_path


def compact_compare_text(
    config: dict[str, Any],
    report_kind: str,
    metric_key: str,
    comparison: dict[str, Any] | None,
) -> str:
    if not comparison:
        return t(config, "kpi_compare_na")
    previous = comparison.get("previous")
    label = compare_label(config, report_kind)
    previous_text = format_kpi_value(metric_key, previous)
    ratio = comparison.get("ratio")
    if ratio is None:
        return f"{label}: {previous_text}"
    arrow = "↑" if ratio >= 0 else "↓"
    return f"{arrow} {label} {previous_text} ({abs(float(ratio)):.1f}%)"


def build_baota_period_kpis(report: dict[str, Any], config: dict[str, Any]) -> list[dict[str, str]]:
    labels = TRANSLATIONS[report_language(config)]
    report_kind = report["meta"]["report_kind"]
    comparisons = report.get("kpi_comparisons", {})
    metrics = [
        ("pv", labels["pv"]),
        ("uv", labels["uv"]),
        ("unique_ips", labels["ips"]),
        ("request_count", labels["requests"]),
        ("total_traffic_bytes", labels["total_traffic"]),
        ("spider_total", labels["spider_total"]),
    ]
    cards: list[dict[str, str]] = []
    for metric_key, title in metrics:
        cards.append(
            {
                "label": title,
                "value": format_kpi_value(metric_key, kpi_metric_value(report, metric_key)),
                "compare": compact_compare_text(config, report_kind, metric_key, comparisons.get(metric_key)),
            }
        )
    return cards


def draw_baota_period_header(
    ax: Any,
    report: dict[str, Any],
    config: dict[str, Any],
    generated_at: str,
    page_number: int,
    total_pages: int,
) -> None:
    report_kind = report["meta"]["report_kind"]
    title = t(config, f"{report_kind}_title")
    window = f"{report['meta']['window_start']} - {report['meta']['window_end']}"
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 0.90, title, ha="left", va="top", color="#111111", fontproperties=pdf_font(15.5, "bold"), transform=ax.transAxes)
    ax.text(0.0, 0.54, str(report["meta"]["site"]), ha="left", va="top", color="#666666", fontproperties=pdf_font(8.6), transform=ax.transAxes)
    ax.text(0.0, 0.23, window, ha="left", va="top", color="#666666", fontproperties=pdf_font(7.8), transform=ax.transAxes)
    ax.text(
        1.0,
        0.82,
        f"{t(config, 'requests')}: {format_number(report['traffic']['request_count'])}",
        ha="right",
        va="top",
        color="#111111",
        fontproperties=pdf_font(9.6, "bold"),
        transform=ax.transAxes,
    )
    ax.text(
        1.0,
        0.48,
        f"{t(config, 'total_traffic')}: {format_bytes(total_traffic_bytes(report))}",
        ha="right",
        va="top",
        color="#111111",
        fontproperties=pdf_font(9.6, "bold"),
        transform=ax.transAxes,
    )
    ax.text(
        1.0,
        0.18,
        f"{t(config, 'page_indicator').format(current=page_number, total=total_pages)}  {t(config, 'generated_at')}: {generated_at}",
        ha="right",
        va="top",
        color="#888888",
        fontproperties=pdf_font(7.2),
        transform=ax.transAxes,
    )
    ax.plot([0.0, 1.0], [0.02, 0.02], transform=ax.transAxes, color="#EAEAEA", linewidth=0.9)


def draw_baota_period_trend(ax: Any, report: dict[str, Any], config: dict[str, Any]) -> None:
    labels = TRANSLATIONS[report_language(config)]
    report_kind = report["meta"]["report_kind"]
    title = labels["trend_pv_uv"] if report_kind == "weekly" else labels["trend_30d"]
    apply_bt_axis_style(ax, title)
    series = report.get("traffic_series", [])
    x_positions = list(range(len(series)))
    date_labels = [str(item.get("date", ""))[5:] for item in series]
    pv_values = [float(item.get("pv") or 0.0) for item in series]
    uv_values = [float(item.get("uv") or 0.0) for item in series]
    if report_kind == "monthly":
        pv_values = moving_average(pv_values, 3)
        uv_values = moving_average(uv_values, 3)
    ax.plot(x_positions, pv_values, color="#2563EB", linewidth=1.55, label=labels["pv"])
    ax.fill_between(x_positions, pv_values, color="#2563EB", alpha=0.12)
    ax.plot(x_positions, uv_values, color="#10B981", linewidth=1.55, label=labels["uv"])
    ax.fill_between(x_positions, uv_values, color="#10B981", alpha=0.10)
    if x_positions:
        ax.set_xlim(-0.2, len(x_positions) - 0.8)
        tick_step = max(1, math.ceil(len(date_labels) / (7 if report_kind == "weekly" else 8)))
        tick_positions = list(range(0, len(date_labels), tick_step))
        if tick_positions and tick_positions[-1] != len(date_labels) - 1:
            tick_positions.append(len(date_labels) - 1)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([date_labels[index] for index in tick_positions], rotation=28, ha="right")
        apply_axis_tick_fonts(ax, 7.2)
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(7.6), ncol=2, handlelength=1.8)
    for text in legend.get_texts():
        text.set_color("#666666")


def draw_baota_monthly_resource_trend(ax: Any, report: dict[str, Any], config: dict[str, Any]) -> None:
    labels = TRANSLATIONS[report_language(config)]
    apply_bt_axis_style(ax, labels["cpu_disk_trend"])
    series = report.get("traffic_series", [])
    x_positions = list(range(len(series)))
    date_labels = [str(item.get("date", ""))[5:] for item in series]
    cpu_values = [float(item.get("cpu_peak") or 0.0) for item in series]
    disk_values = [float(item.get("disk_free_bytes") or 0.0) / (1024 ** 3) for item in series]
    ax.plot(x_positions, cpu_values, color="#F59E0B", linewidth=1.55, label=labels["resource_cpu"])
    ax.fill_between(x_positions, cpu_values, color="#F59E0B", alpha=0.10)
    ax_right = ax.twinx()
    ax_right.set_facecolor("#FFFFFF")
    ax_right.plot(x_positions, disk_values, color="#2563EB", linewidth=1.45, label=labels["resource_disk"])
    ax_right.fill_between(x_positions, disk_values, color="#2563EB", alpha=0.08)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.grid(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#666666", labelsize=7.2)
    apply_axis_tick_fonts(ax_right, 7.2)
    if x_positions:
        ax.set_xlim(-0.2, len(x_positions) - 0.8)
        tick_step = max(1, math.ceil(len(date_labels) / 8))
        tick_positions = list(range(0, len(date_labels), tick_step))
        if tick_positions and tick_positions[-1] != len(date_labels) - 1:
            tick_positions.append(len(date_labels) - 1)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([date_labels[index] for index in tick_positions], rotation=28, ha="right")
        apply_axis_tick_fonts(ax, 7.2)
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(
        left_handles + right_handles,
        left_labels + right_labels,
        loc="upper left",
        frameon=False,
        prop=pdf_font(7.2),
        ncol=2,
        handlelength=1.6,
    )
    for text in legend.get_texts():
        text.set_color("#666666")


def build_baota_donut_data(items: list[dict[str, Any]], labels: dict[str, str]) -> dict[str, int]:
    donut: dict[str, int] = {}
    for item in items:
        key = truncate_text(localize_chart_item(str(item["item"]), labels), 14)
        donut[key] = int(item["count"])
    return donut


def draw_baota_period_donut(
    ax: Any,
    title: str,
    items: list[dict[str, Any]],
    labels: dict[str, str],
    colors: list[str],
) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#111111", fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    if not items:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#666666", fontproperties=pdf_font(8.2), transform=ax.transAxes)
        return
    draw_baota_donut(ax, title, build_baota_donut_data(items, labels), colors)


def safe_table_rows(rows: list[list[str]], empty_label: str) -> list[list[str]]:
    return rows if rows else [["-", empty_label, "-"]]


def render_standard_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    labels = TRANSLATIONS[report_language(config)]
    report_kind = report["meta"]["report_kind"]
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")

    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(5, 12, height_ratios=[0.76, 1.08, 0.84, 1.62, 1.44])
        draw_baota_period_header(page_one.add_subplot(grid_one[0, :]), report, config, generated_at, 1, 2)
        draw_ai_review_card(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis(page_one.add_subplot(grid_one[2, :]), build_baota_period_kpis(report, config))
        draw_baota_period_trend(page_one.add_subplot(grid_one[3, :]), report, config)
        draw_baota_period_donut(
            page_one.add_subplot(grid_one[4, 0:6]),
            labels["spider_distribution"],
            build_spider_chart_data(report.get("spiders", [])),
            labels,
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"],
        )
        draw_baota_period_donut(
            page_one.add_subplot(grid_one[4, 6:12]),
            labels["http_status_mix"],
            build_status_chart_data(report.get("status_codes", [])),
            labels,
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"],
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        if report_kind == "monthly":
            grid_two = page_two.add_gridspec(5, 12, height_ratios=[0.72, 0.95, 1.74, 2.50, 2.50])
            resource_row = 2
            top_row = 3
            bottom_row = 4
        else:
            grid_two = page_two.add_gridspec(4, 12, height_ratios=[0.72, 0.95, 3.10, 3.10])
            resource_row = None
            top_row = 2
            bottom_row = 3
        draw_baota_period_header(page_two.add_subplot(grid_two[0, :]), report, config, generated_at, 2, 2)
        draw_summary_strip(
            page_two.add_subplot(grid_two[1, :]),
            labels["system_overview"],
            build_system_summary_cards(report, labels),
        )
        if resource_row is not None:
            draw_baota_monthly_resource_trend(page_two.add_subplot(grid_two[resource_row, :]), report, config)
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[top_row, 0:6]),
            labels["top_uris"],
            [labels["rank"], labels["item"], labels["count"]],
            safe_table_rows(build_ranked_rows(report.get("top_uris", []), lambda value: format_number(value), 26), labels["no_data"]),
            [0.16, 0.64, 0.20],
        )
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[top_row, 6:12]),
            labels["slow_routes"],
            [labels["rank"], labels["item"], labels["count"]],
            safe_table_rows(build_ranked_rows(report.get("slow_routes", []), lambda value: format_number(value), 24), labels["no_data"]),
            [0.16, 0.64, 0.20],
        )
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[bottom_row, 0:6]),
            labels["abnormal_ips"],
            [labels["rank"], labels["item"], labels["rpm"]],
            safe_table_rows(build_ranked_rows(report.get("abnormal_ips", []), lambda value: format_number(value), 22), labels["no_data"]),
            [0.16, 0.60, 0.24],
        )
        draw_baota_compact_table(
            page_two.add_subplot(grid_two[bottom_row, 6:12]),
            labels["top_errors"],
            [labels["rank"], labels["item"], labels["count"]],
            safe_table_rows(build_ranked_rows(report.get("top_errors", []), lambda value: format_number(value), 28), labels["no_data"]),
            [0.16, 0.64, 0.20],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)

    return output_path


def build_baota_daily_demo(report: dict[str, Any]) -> dict[str, Any]:
    site = str(report.get("meta", {}).get("site") or "demo.server-mate.local")
    window_start = str(report.get("meta", {}).get("window_start") or "2026-03-25T00:00:00+08:00")
    window_end = str(report.get("meta", {}).get("window_end") or "2026-03-26T00:00:00+08:00")
    traffic = report.get("traffic", {})
    return {
        "title": "网站监控报表",
        "site": site,
        "window": f"{window_start} - {window_end}",
        "total_requests": format_number(traffic.get("request_count")),
        "total_traffic": format_bytes(total_traffic_bytes(report)),
        "hour_labels": [f"{hour}:00" for hour in range(24)],
        "trend": {
            "pv": [480, 430, 390, 360, 320, 310, 420, 780, 1290, 1650, 1490, 1370, 1280, 1450, 1710, 1960, 2080, 1910, 1740, 1670, 1830, 1710, 1320, 860],
            "uv": [240, 212, 190, 170, 162, 155, 188, 362, 618, 790, 742, 701, 655, 690, 760, 835, 884, 826, 770, 733, 768, 742, 604, 428],
            "ip": [196, 182, 168, 150, 138, 132, 154, 294, 472, 598, 572, 546, 528, 551, 606, 653, 691, 664, 621, 598, 614, 603, 497, 352],
        },
        "performance": {
            "qps": [1.4, 1.2, 1.0, 0.9, 0.8, 0.7, 1.1, 2.2, 3.9, 4.8, 4.4, 4.0, 3.6, 4.1, 4.5, 5.2, 5.6, 5.1, 4.6, 4.2, 4.8, 4.5, 3.2, 2.1],
            "response_ms": [210, 205, 198, 192, 188, 186, 194, 228, 312, 428, 396, 372, 348, 360, 388, 446, 492, 460, 418, 402, 436, 410, 318, 264],
        },
        "network": {
            "upload_kb": [26, 24, 22, 20, 19, 18, 21, 35, 58, 92, 86, 82, 78, 84, 96, 118, 132, 125, 116, 110, 124, 118, 88, 54],
            "download_kb": [148, 136, 122, 116, 105, 101, 128, 236, 422, 618, 584, 560, 532, 574, 646, 732, 804, 760, 706, 684, 742, 711, 524, 338],
        },
        "spiders": {
            "Googlebot": 3620,
            "Baiduspider": 2310,
            "Bingbot": 1186,
            "Sogou": 904,
            "Other": 897,
        },
        "statuses": {
            "200": 66194,
            "301": 2842,
            "302": 1016,
            "403": 384,
            "404": 2451,
            "500": 516,
            "502": 419,
        },
        "hot_page_rows": [
            ["/estimate/myestimate", "0", "0", "8791", "30.83 MB"],
            ["/carport/pinpoint", "0", "0", "2818", "10.26 MB"],
            ["/fence/pinpoint", "0", "0", "1518", "5.82 MB"],
            ["/", "643", "240", "1395", "310.19 MB"],
            ["/images/review_img/ss/45162.JPEG", "0", "0", "587", "1.83 MB"],
            ["/images/review_img/large/45162.JPEG", "0", "0", "482", "1.33 MB"],
            ["/images/review_img/large/47076.JPEG", "0", "0", "478", "1.24 MB"],
            ["/wooddeck/pinpoint", "0", "0", "382", "1.40 MB"],
            ["/terrace/pinpoint", "0", "0", "297", "1.13 MB"],
            ["/images/review_img/ss/47076.JPEG", "0", "0", "294", "923.90 KB"],
            ["/block/calendar", "0", "0", "256", "5.04 MB"],
            ["/robots.txt", "0", "0", "219", "811.33 KB"],
            ["/terrace-kakoi/case/2285", "218", "104", "218", "12.53 MB"],
            ["/carport/common_search_ajax", "0", "0", "192", "1.23 MB"],
            ["/apple-touch-icon.png", "0", "0", "188", "661.45 KB"],
            ["/apple-touch-icon-precomposed.png", "0", "0", "182", "628.70 KB"],
        ],
        "hot_ip_rows": [
            ["203.0.113.28", "上海", "1264", "2318", "186.2 MB"],
            ["198.51.100.42", "San Jose", "1148", "2106", "174.4 MB"],
            ["203.0.113.77", "北京", "1082", "1984", "162.5 MB"],
            ["192.0.2.66", "Tokyo", "1036", "1912", "154.1 MB"],
            ["203.0.113.101", "Singapore", "996", "1864", "149.3 MB"],
            ["198.51.100.18", "杭州", "942", "1780", "142.6 MB"],
        ],
        "hot_referer_rows": [
            ["https://www.baidu.com/", "3912", "7864", "418.6 MB"],
            ["https://www.google.com/", "3264", "6952", "392.2 MB"],
            ["https://cn.bing.com/", "1826", "3608", "188.4 MB"],
            ["https://m.weibo.cn/", "1542", "3204", "174.7 MB"],
            ["https://mp.weixin.qq.com/", "1308", "2846", "166.5 MB"],
            ["https://www.zhihu.com/", "1126", "2410", "152.2 MB"],
        ],
    }


def draw_ai_review_card_black(ax: Any, review: dict[str, Any]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    wrapped = wrap_dashboard_text(review["summary"], width=66)
    line_count = max(wrapped.count("\n") + 1, 1)
    body_font_size = 7.8 if line_count >= 6 else 8.1
    body_y = 0.72 if line_count >= 6 else 0.68
    # Use an invisible text block to let bbox auto-size with the wrapped content,
    # then draw the title/body separately so they never overlap each other.
    background_text = f"{review['title']}\n\n{wrapped}\n"
    ax.text(
        0.045,
        0.93,
        background_text,
        ha="left",
        va="top",
        color=(0, 0, 0, 0),
        linespacing=1.55,
        fontproperties=pdf_font(body_font_size),
        bbox=dict(facecolor="#F4F8FB", alpha=0.95, boxstyle="round,pad=1.0", edgecolor="none"),
        transform=ax.transAxes,
    )
    ax.text(
        0.045,
        0.88,
        review["title"],
        ha="left",
        va="top",
        color="#000000",
        fontproperties=pdf_font(10.2, "bold"),
        transform=ax.transAxes,
    )
    ax.text(
        0.045,
        body_y,
        wrapped,
        ha="left",
        va="top",
        color="#000000",
        linespacing=1.55,
        fontproperties=pdf_font(body_font_size),
        transform=ax.transAxes,
    )


def draw_baota_header_black(
    ax: Any,
    report: dict[str, Any],
    demo: dict[str, Any],
    labels: dict[str, str],
    generated_at: str,
    page_number: int,
    total_pages: int,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 0.90, demo["title"], ha="left", va="top", color="#000000", fontproperties=pdf_font(15.5, "bold"), transform=ax.transAxes)
    ax.text(0.0, 0.54, demo["site"], ha="left", va="top", color="#000000", fontproperties=pdf_font(8.6), transform=ax.transAxes)
    ax.text(0.0, 0.23, demo["window"], ha="left", va="top", color="#000000", fontproperties=pdf_font(7.8), transform=ax.transAxes)
    ax.text(1.0, 0.88, f"{labels['requests']}: {demo['total_requests']}", ha="right", va="top", color="#000000", fontproperties=pdf_font(8.5, "bold"), transform=ax.transAxes)
    ax.text(1.0, 0.64, f"{labels['total_traffic']}: {demo['total_traffic']}", ha="right", va="top", color="#000000", fontproperties=pdf_font(8.5, "bold"), transform=ax.transAxes)
    ax.text(1.0, 0.42, f"{labels['ssl_remaining']}: {demo.get('ssl_summary', 'N/A')}", ha="right", va="top", color="#000000", fontproperties=pdf_font(8.3, "bold"), transform=ax.transAxes)
    ax.text(
        1.0,
        0.20,
        f"{labels['page_indicator'].format(current=page_number, total=total_pages)}  {labels['generated_at']}: {generated_at}",
        ha="right",
        va="top",
        color="#000000",
        fontproperties=pdf_font(6.9),
        transform=ax.transAxes,
    )
    ax.plot([0.0, 1.0], [0.02, 0.02], transform=ax.transAxes, color="#EAEAEA", linewidth=0.9)


def draw_baota_kpis_black(ax: Any, cards: list[dict[str, str]]) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    segment_width = 1.0 / len(cards)
    for index, card in enumerate(cards):
        left = index * segment_width
        text_x = left + segment_width * 0.08
        if index > 0:
            ax.plot([left, left], [0.16, 0.86], transform=ax.transAxes, color="#ECECEC", linewidth=0.9)
        ax.text(text_x, 0.82, card["label"], ha="left", va="top", color="#000000", fontproperties=pdf_font(8.2), transform=ax.transAxes)
        ax.text(text_x, 0.48, card["value"], ha="left", va="center", color="#000000", fontproperties=pdf_font(15.6, "bold"), transform=ax.transAxes)
        ax.text(text_x, 0.18, card["compare"], ha="left", va="bottom", color="#000000", fontproperties=pdf_font(6.9), transform=ax.transAxes)


def apply_bt_axis_style_black(ax: Any, title: str) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#000000", fontproperties=pdf_font(9.2, "bold"))
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=4, colors="#000000", labelsize=7.6)
    apply_axis_tick_fonts(ax, 7.4)
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_color("#000000")


def draw_baota_three_line_chart_black(ax: Any, demo: dict[str, Any], labels: dict[str, str]) -> None:
    apply_bt_axis_style_black(ax, labels["daily_hourly_trend"])
    x_positions = list(range(24))
    pv_values = demo["trend"]["pv"]
    uv_values = demo["trend"]["uv"]
    ip_values = demo["trend"]["ip"]
    ax.plot(x_positions, pv_values, color="#2563EB", linewidth=1.5, label=labels["pv"])
    ax.fill_between(x_positions, pv_values, color="#2563EB", alpha=0.12)
    ax.plot(x_positions, uv_values, color="#10B981", linewidth=1.5, label=labels["uv"])
    ax.fill_between(x_positions, uv_values, color="#10B981", alpha=0.10)
    ax.plot(x_positions, ip_values, color="#F59E0B", linewidth=1.4, label=labels["ips"])
    ax.fill_between(x_positions, ip_values, color="#F59E0B", alpha=0.08)
    ax.set_xlim(-0.3, 23.3)
    tick_positions = [0, 4, 8, 12, 16, 20]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([demo["hour_labels"][index] for index in tick_positions], rotation=0, ha="center")
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(7.6), ncol=3, handlelength=1.8)
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_baota_dual_axis_chart_black(
    ax: Any,
    title: str,
    x_labels: list[str],
    left_series: list[float],
    right_series: list[float],
    left_label: str,
    right_label: str,
    left_color: str,
    right_color: str,
) -> None:
    apply_bt_axis_style_black(ax, title)
    x_positions = list(range(len(x_labels)))
    ax.plot(x_positions, left_series, color=left_color, linewidth=1.5, label=left_label)
    ax.fill_between(x_positions, left_series, color=left_color, alpha=0.12)
    ax.set_xlim(-0.2, len(x_labels) - 0.8)
    ax.margins(x=0.012, y=0.01)
    if MaxNLocator is not None:
        ax.yaxis.set_major_locator(MaxNLocator(4))
    left_max = max(left_series) if left_series else 1.0
    ax.set_ylim(0, left_max * 1.03 if left_max > 0 else 1.0)
    if MaxNLocator is not None and FuncFormatter is not None:
        ax.xaxis.set_major_locator(MaxNLocator(5, integer=True))
        ax.xaxis.set_major_formatter(
            FuncFormatter(
                lambda value, _pos: x_labels[int(round(value))]
                if 0 <= int(round(value)) < len(x_labels)
                else ""
            )
        )
    ax.tick_params(axis="x", labelrotation=0)
    ax.tick_params(axis="y", pad=2, labelsize=6.8)
    apply_axis_tick_fonts(ax, 6.8)
    ax_right = ax.twinx()
    ax_right.set_facecolor("#FFFFFF")
    ax_right.plot(x_positions, right_series, color=right_color, linewidth=1.5, label=right_label)
    ax_right.fill_between(x_positions, right_series, color=right_color, alpha=0.10)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.grid(False)
    right_max = max(right_series) if right_series else 1.0
    ax_right.set_ylim(0, right_max * 1.03 if right_max > 0 else 1.0)
    if MaxNLocator is not None:
        ax_right.yaxis.set_major_locator(MaxNLocator(4))
    ax_right.tick_params(axis="y", length=0, pad=2, colors="#000000", labelsize=6.6)
    apply_axis_tick_fonts(ax_right, 6.6)
    for label in list(ax_right.get_yticklabels()):
        label.set_color("#000000")
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(left_handles + right_handles, left_labels + right_labels, loc="upper left", frameon=False, prop=pdf_font(6.8))
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_baota_donut_black(ax: Any, title: str, data: dict[str, int], colors: list[str]) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#000000", fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    values = list(data.values())
    total = max(sum(values), 1)
    wedges, _ = ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        labels=None,
        wedgeprops={"width": 0.22, "edgecolor": "#FFFFFF", "linewidth": 1.2},
        radius=0.88,
    )
    ax.text(0.0, 0.08, format_number(sum(values)), ha="center", va="center", color="#000000", fontproperties=pdf_font(11.4, "bold"))
    ax.text(0.0, -0.08, "总量", ha="center", va="center", color="#000000", fontproperties=pdf_font(7.0))
    legend_labels = [f"{label} {value / total * 100:.1f}% ({format_number(value)})" for label, value in data.items()]
    legend = ax.legend(
        wedges,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        frameon=False,
        prop=pdf_font(6.8),
        handlelength=0.9,
        ncol=2 if len(values) <= 4 else 3,
    )
    for text in legend.get_texts():
        text.set_color("#000000")
    ax.axis("equal")


def draw_baota_hot_table(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    title_center: bool = False,
) -> None:
    ax.set_axis_off()
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(
        0.5 if title_center else 0.0,
        1.02,
        title,
        ha="center" if title_center else "left",
        va="bottom",
        color="#000000",
        fontproperties=pdf_font(11.2 if title_center else 10.3, "bold"),
        transform=ax.transAxes,
    )
    table = ax.table(
        cellText=rows,
        colLabels=headers,
        bbox=[0.0, 0.00, 1.0, 0.94],
        cellLoc="center",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.2)
    total_rows = len(rows) + 1
    row_height = min(0.085, 0.90 / max(total_rows, 1))
    for (row_index, column_index), cell in table.get_celld().items():
        if column_index < len(col_widths):
            cell.set_width(col_widths[column_index])
        cell.set_height(row_height)
        cell.set_edgecolor("#BDBDBD")
        cell.set_linewidth(0.55)
        cell.PAD = 0.045
        cell.get_text().set_color("#000000")
        cell.get_text().set_va("center")
        if row_index == 0:
            cell.set_facecolor("#48F65C")
            cell.get_text().set_fontproperties(pdf_font(7.5, "bold"))
            cell.get_text().set_ha("center")
        else:
            cell.set_facecolor("#DCDCDC" if row_index % 2 == 1 else "#FFFFFF")
            cell.get_text().set_fontproperties(pdf_font(7.0))
            if column_index == 0:
                cell.get_text().set_ha("center" if title_center else "left")
            else:
                cell.get_text().set_ha("center")


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    demo = build_baota_daily_demo(report)
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        grid_one = page_one.add_gridspec(6, 12, height_ratios=[0.76, 1.10, 0.82, 1.46, 1.34, 1.30])
        draw_baota_header_black(page_one.add_subplot(grid_one[0, :]), report, demo, generated_at, 1, 2)
        draw_ai_review_card_black(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis_black(page_one.add_subplot(grid_one[2, :]), build_baota_period_kpis(report, config))
        draw_baota_three_line_chart_black(page_one.add_subplot(grid_one[3, :]), demo)
        draw_baota_dual_axis_chart_black(
            page_one.add_subplot(grid_one[4, 0:6]),
            "性能/负载",
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart_black(
            page_one.add_subplot(grid_one[4, 6:12]),
            "网站流量",
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB",
            "下行 KB",
            "#F59E0B",
            "#10B981",
        )
        draw_baota_donut_black(
            page_one.add_subplot(grid_one[5, 0:6]),
            "蜘蛛统计",
            demo["spiders"],
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8"],
        )
        draw_baota_donut_black(
            page_one.add_subplot(grid_one[5, 6:12]),
            "状态码统计",
            demo["statuses"],
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B"],
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        grid_two = page_two.add_gridspec(4, 12, height_ratios=[0.70, 3.95, 1.95, 1.95])
        draw_baota_header_black(page_two.add_subplot(grid_two[0, :]), report, demo, generated_at, 2, 2)
        draw_baota_hot_table(
            page_two.add_subplot(grid_two[1, :]),
            "热门页面",
            ["URI", "PV", "UV", "请求数", "流量"],
            demo["hot_page_rows"],
            [0.50, 0.11, 0.11, 0.13, 0.15],
            title_center=True,
        )
        draw_baota_hot_table(
            page_two.add_subplot(grid_two[2, :]),
            "热门 IP",
            ["IP地址", "地区", "PV", "请求数", "流量"],
            demo["hot_ip_rows"],
            [0.20, 0.22, 0.12, 0.18, 0.28],
        )
        draw_baota_hot_table(
            page_two.add_subplot(grid_two[3, :]),
            "热门来源",
            ["Referer来源", "PV", "请求数", "流量"],
            demo["hot_referer_rows"],
            [0.54, 0.12, 0.14, 0.20],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)
    return output_path


def build_baota_daily_demo_v2(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    site = str(report.get("meta", {}).get("site") or "demo.server-mate.local")
    window_start = str(report.get("meta", {}).get("window_start") or "2026-03-25T00:00:00+08:00")
    window_end = str(report.get("meta", {}).get("window_end") or "2026-03-26T00:00:00+08:00")
    traffic = report.get("traffic", {})
    labels = TRANSLATIONS[report_language(config)]
    language = report_language(config)
    province_pairs = [
        ("Hong Kong", "香港", "9774", "19373"),
        ("Beijing", "北京", "1380", "5899"),
        ("Shanxi", "山西", "654", "912"),
        ("Jiangsu", "江苏", "100", "214"),
        ("Shanghai", "上海", "84", "910"),
        ("Zhejiang", "浙江", "1159", "15905"),
        ("Shaanxi", "陕西", "26", "71"),
        ("Shandong", "山东", "23", "32"),
        ("Guizhou", "贵州", "40", "86"),
        ("Anhui", "安徽", "27", "44"),
        ("Fujian", "福建", "15", "29"),
        ("Henan", "河南", "11", "31"),
        ("Inner Mongolia", "内蒙古", "68", "412"),
        ("Tianjin", "天津", "44", "205"),
        ("Hubei", "湖北", "52", "236"),
        ("Jiangxi", "江西", "38", "188"),
        ("Taiwan", "台湾", "597", "1660"),
        ("Guangdong", "广东", "5288", "6482"),
        ("Sichuan", "四川", "211", "1048"),
        ("Hebei", "河北", "88", "356"),
        ("Hunan", "湖南", "75", "298"),
        ("Liaoning", "辽宁", "67", "264"),
        ("Chongqing", "重庆", "33", "144"),
        ("Qinghai", "青海", "12", "46"),
        ("Ningxia", "宁夏", "14", "58"),
        ("Yunnan", "云南", "26", "103"),
    ]
    province_rows = [
        [en_name if language == "en" else zh_name, ip_count, visit_count]
        for en_name, zh_name, ip_count, visit_count in province_pairs
    ]
    province_categories = [row[0] for row in province_rows[:12]]
    province_ip_values = [int(row[1]) for row in province_rows[:12]]
    province_visit_values = [int(row[2]) for row in province_rows[:12]]

    client_pairs = [
        ("Safari", "Safari", 929135),
        ("Chrome", "Chrome", 698456),
        ("Firefox", "Firefox", 39618),
        ("Opera", "Opera", 1320),
        ("IE", "IE", 711),
        ("Edge", "Edge", 299),
        ("Crawler", "蜘蛛", 335308),
        ("Automation", "机器", 37474),
        ("WeChat", "微信", 343),
        ("Aoyou", "遨游", 92),
        ("Liebao", "猎豹", 15),
        ("UC", "UC", 545),
    ]
    client_distribution = {
        (en_name if language == "en" else zh_name): count
        for en_name, zh_name, count in client_pairs
    }
    hot_ip_pairs = [
        ("66.249.64.10", "美国 蒙克斯科纳", "US / Moncks Corner", "62655", "3.65 GB"),
        ("47.91.25.126", "日本 东京", "Japan / Tokyo", "61282", "260.07 MB"),
        ("66.249.64.11", "美国 蒙克斯科纳", "US / Moncks Corner", "25893", "1.53 GB"),
        ("127.0.0.1", "局域网 本地环回", "LAN / Loopback", "14851", "67.24 MB"),
        ("66.249.64.12", "美国 蒙克斯科纳", "US / Moncks Corner", "11078", "681.39 MB"),
        ("66.249.89.10", "美国 亚特兰大", "US / Atlanta", "7719", "274.19 MB"),
        ("202.215.117.120", "日本 ARTERIA", "Japan / ARTERIA", "6139", "216.42 MB"),
        ("20.151.11.236", "加拿大 多伦多", "Canada / Toronto", "5751", "585.40 MB"),
        ("20.220.232.240", "加拿大 多伦多", "Canada / Toronto", "3890", "422.65 MB"),
        ("66.249.89.11", "美国 亚特兰大", "US / Atlanta", "3787", "134.39 MB"),
        ("45.148.10.5", "中国 香港", "China / Hong Kong", "3588", "26.78 MB"),
        ("66.249.64.13", "美国 蒙克斯科纳", "US / Moncks Corner", "3110", "175.44 MB"),
        ("4.204.200.32", "加拿大 多伦多", "Canada / Toronto", "2857", "308.36 MB"),
        ("20.151.2.242", "加拿大 多伦多", "Canada / Toronto", "2248", "232.49 MB"),
        ("172.213.136.15", "意大利 米兰", "Italy / Milan", "1874", "235.15 MB"),
        ("57.141.6.50", "瑞士 Facebook", "Switzerland / Facebook", "1735", "576.56 MB"),
        ("172.190.142.176", "美国 阿什本", "US / Ashburn", "1707", "145.22 MB"),
        ("57.141.6.15", "瑞士 Facebook", "Switzerland / Facebook", "1693", "565.49 MB"),
        ("57.141.6.17", "瑞士 Facebook", "Switzerland / Facebook", "1693", "560.35 MB"),
        ("34.27.84.233", "美国 康瑟尔布拉夫斯", "US / Council Bluffs", "1672", "6.05 MB"),
        ("57.141.6.35", "瑞士 Facebook", "Switzerland / Facebook", "1657", "538.66 MB"),
        ("57.141.6.66", "瑞士 Facebook", "Switzerland / Facebook", "1639", "539.39 MB"),
        ("57.141.6.51", "瑞士 Facebook", "Switzerland / Facebook", "1632", "538.40 MB"),
        ("57.141.6.12", "瑞士 Facebook", "Switzerland / Facebook", "1610", "528.10 MB"),
        ("57.141.6.39", "瑞士 Facebook", "Switzerland / Facebook", "1601", "531.26 MB"),
        ("57.141.6.3", "瑞士 Facebook", "Switzerland / Facebook", "1597", "515.20 MB"),
        ("57.141.6.11", "瑞士 Facebook", "Switzerland / Facebook", "1588", "515.97 MB"),
    ]
    hot_ip_rows = [
        [ip, zh_info if language == "zh" else en_info, request_count, traffic_value]
        for ip, zh_info, en_info, request_count, traffic_value in hot_ip_pairs
    ]
    return {
        "title": labels["monitoring_report"],
        "site": site,
        "window": f"{window_start} - {window_end}",
        "total_requests": format_number(traffic.get("request_count")),
        "total_traffic": format_bytes(total_traffic_bytes(report)),
        "hour_labels": [f"{hour}:00" for hour in range(24)],
        "trend": {
            "pv": [480, 430, 390, 360, 320, 310, 420, 780, 1290, 1650, 1490, 1370, 1280, 1450, 1710, 1960, 2080, 1910, 1740, 1670, 1830, 1710, 1320, 860],
            "uv": [240, 212, 190, 170, 162, 155, 188, 362, 618, 790, 742, 701, 655, 690, 760, 835, 884, 826, 770, 733, 768, 742, 604, 428],
            "ip": [196, 182, 168, 150, 138, 132, 154, 294, 472, 598, 572, 546, 528, 551, 606, 653, 691, 664, 621, 598, 614, 603, 497, 352],
        },
        "performance": {
            "qps": [1.4, 1.2, 1.0, 0.9, 0.8, 0.7, 1.1, 2.2, 3.9, 4.8, 4.4, 4.0, 3.6, 4.1, 4.5, 5.2, 5.6, 5.1, 4.6, 4.2, 4.8, 4.5, 3.2, 2.1],
            "response_ms": [210, 205, 198, 192, 188, 186, 194, 228, 312, 428, 396, 372, 348, 360, 388, 446, 492, 460, 418, 402, 436, 410, 318, 264],
        },
        "network": {
            "upload_kb": [26, 24, 22, 20, 19, 18, 21, 35, 58, 92, 86, 82, 78, 84, 96, 118, 132, 125, 116, 110, 124, 118, 88, 54],
            "download_kb": [148, 136, 122, 116, 105, 101, 128, 236, 422, 618, 584, 560, 532, 574, 646, 732, 804, 760, 706, 684, 742, 711, 524, 338],
        },
        "spiders": {"Googlebot": 3620, "Baiduspider": 2310, "Bingbot": 1186, "Sogou": 904, "Other": 897},
        "statuses": {"200": 66194, "301": 2842, "302": 1016, "403": 384, "404": 2451, "500": 516, "502": 419},
        "hot_page_rows": [
            ["/estimate/myestimate", "22", "19", "180846", "640.51 MB"],
            ["/carport/pinpoint", "1", "1", "63167", "236.06 MB"],
            ["/", "16588", "4808", "38939", "7.77 GB"],
            ["/fence/pinpoint", "0", "0", "34165", "132.94 MB"],
            ["/images/review_img/ss/45162.JPEG", "0", "0", "14254", "45.38 MB"],
            ["/images/review_img/large/45162.JPEG", "0", "0", "12654", "40.16 MB"],
            ["/images/review_img/large/47076.JPEG", "0", "0", "12623", "40.22 MB"],
            ["/wooddeck/pinpoint", "0", "0", "9068", "33.34 MB"],
            ["/images/review_img/ss/47076.JPEG", "0", "0", "7130", "22.69 MB"],
            ["/robots.txt", "0", "0", "6575", "23.04 MB"],
            ["/terrace/pinpoint", "1", "0", "6463", "24.97 MB"],
            ["/html/upload/index_image/sshopping_cart_black.png", "0", "0", "5605", "17.90 MB"],
            ["/apple-touch-icon.png", "0", "0", "4186", "13.84 MB"],
            ["/carport", "3599", "1207", "4137", "415.85 MB"],
            ["/apple-touch-icon-precomposed.png", "0", "0", "4098", "13.84 MB"],
            ["/html/upload/save_image/kisyo_image/202/3002_118_200719/material_01.jpg", "0", "0", "3805", "12.62 MB"],
            ["/html/upload/save_image/kisyo_image/202/3002_118_200719/option_02_1.jpg", "0", "0", "3767", "12.49 MB"],
            ["/block/calendar", "0", "0", "3711", "73.22 MB"],
            ["/html/upload/save_image/kisyo_image/202/3002_118_200719/option_01_1.jpg", "0", "0", "3703", "12.29 MB"],
            ["/carport/common_search_ajax", "2", "0", "3050", "17.79 MB"],
            ["/campaign/campaign_20260205", "2173", "445", "2964", "227.81 MB"],
            ["/fence", "2499", "671", "2882", "302.50 MB"],
            ["/carport/m-ykkap/s-frougefirst/p-200677", "1443", "210", "2824", "260.95 MB"],
            ["/terrace-kakoi/case/2285", "2603", "1244", "2651", "155.25 MB"],
        ],
        "hot_ip_rows": hot_ip_rows,
        "hot_referer_rows": [
            ["https://www.baidu.com/", "3912", "7864", "418.6 MB"],
            ["https://www.google.com/", "3264", "6952", "392.2 MB"],
            ["https://cn.bing.com/", "1826", "3608", "188.4 MB"],
            ["https://m.weibo.cn/", "1542", "3204", "174.7 MB"],
            ["https://mp.weixin.qq.com/", "1308", "2846", "166.5 MB"],
            ["https://www.zhihu.com/", "1126", "2410", "152.2 MB"],
            ["https://news.qq.com/", "962", "2136", "144.8 MB"],
            ["https://partner.example.com/", "884", "1962", "139.7 MB"],
            ["https://www.douyin.com/", "826", "1814", "128.6 MB"],
            ["https://search.yahoo.com/", "764", "1698", "121.1 MB"],
        ],
        "spider_distribution": {"Googlebot": 4165, "Baiduspider": 670, "Bingbot": 147, "Sogou": 126, "Yandex": 9, "360Spider": 6, "Other": 11},
        "spider_daily_rows": [
            ["2026-03-23", "4165", "670", "147", "126", "9", "6", "11"],
            ["2026-03-24", "4136", "670", "4", "4", "0", "0", "0"],
            ["2026-03-25", "4138", "0", "147", "6", "7", "0", "0"],
            ["2026-03-26", "2224", "0", "126", "9", "9", "0", "0"],
            ["2026-03-27", "0", "0", "0", "0", "0", "0", "0"],
            ["2026-03-28", "0", "0", "0", "0", "0", "0", "0"],
            ["2026-03-29", "0", "0", "0", "0", "0", "0", "0"],
            [labels["total"], "19184", "1340", "298", "145", "25", "6", "11"],
        ],
        "status_distribution": {"200": 15192, "301": 312, "403": 76, "404": 1207, "500": 11, "502": 215, "504": 127, "416": 264},
        "province_rows": province_rows,
        "province_categories": province_categories,
        "province_ip_values": province_ip_values,
        "province_visit_values": province_visit_values,
        "client_distribution": client_distribution,
    }


def wrap_center_text_v2(value: str, width: int) -> str:
    return "\n".join(textwrap.wrap(str(value), width=max(width, 1), break_long_words=True, break_on_hyphens=False))


def build_status_table_rows_v2(distribution: dict[str, int]) -> list[list[str]]:
    total = max(sum(distribution.values()), 1)
    rows: list[list[str]] = []
    for code in ("200", "301", "403", "404", "500", "502", "504", "416"):
        if code in distribution:
            count = distribution[code]
            rows.append([code, format_number(count), f"{count / total * 100:.1f}%"])
    return rows


def build_client_table_rows_v2(distribution: dict[str, int]) -> list[list[str]]:
    total = max(sum(distribution.values()), 1)
    return [[name, format_number(count), f"{count / total * 100:.1f}%"] for name, count in distribution.items()]


def build_rank_value_rows_v2(
    items: list[tuple[str, int]],
    labels: dict[str, str] | None = None,
    limit: int = 10,
) -> list[list[str]]:
    rows: list[list[str]] = []
    for index, (name, value) in enumerate(items[:limit], start=1):
        label = localize_chart_item(name, labels) if labels else name
        rows.append([str(index), truncate_text(str(label), 24), format_number(value)])
    return rows


def build_rank_share_rows_v2(
    distribution: dict[str, int],
    labels: dict[str, str] | None = None,
    limit: int = 10,
) -> list[list[str]]:
    total = max(sum(distribution.values()), 1)
    sorted_items = sorted(distribution.items(), key=lambda item: (-int(item[1]), str(item[0])))
    rows: list[list[str]] = []
    for index, (name, value) in enumerate(sorted_items[:limit], start=1):
        label = localize_chart_item(name, labels) if labels else name
        rows.append([str(index), truncate_text(str(label), 20), format_number(value), f"{value / total * 100:.1f}%"])
    return rows


def draw_baota_donut_stats_v2(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    colors: list[str],
    labels: dict[str, str] | None = None,
) -> None:
    localized_distribution: dict[str, int] = {}
    for name, value in distribution.items():
        localized_distribution[localize_chart_item(name, labels)] = value

    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="left", pad=8, color="#000000", fontproperties=pdf_font(10.4, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    values = list(localized_distribution.values())
    total = max(sum(values), 1)
    wedges, _ = ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        labels=None,
        wedgeprops={"width": 0.26, "edgecolor": "#FFFFFF", "linewidth": 1.2},
        radius=0.88,
    )
    ax.text(0.0, 0.08, format_number(sum(values)), ha="center", va="center", color="#000000", fontproperties=pdf_font(11.4, "bold"))
    ax.text(0.0, -0.08, labels["count"] if labels else "Count", ha="center", va="center", color="#000000", fontproperties=pdf_font(7.0))
    legend_labels = [
        f"{name} {value / total * 100:.1f}% ({format_number(value)})"
        for name, value in localized_distribution.items()
    ]
    legend = ax.legend(
        wedges,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        frameon=False,
        prop=pdf_font(6.8),
        handlelength=0.9,
        ncol=2 if len(values) <= 4 else 3,
    )
    for text in legend.get_texts():
        text.set_color("#000000")
    ax.axis("equal")


def build_ring_summary_v2(distribution: dict[str, int]) -> str:
    labels = list(distribution.keys())
    values = list(distribution.values())
    total = max(sum(values), 1)
    max_label = labels[values.index(max(values))]
    min_label = labels[values.index(min(values))]
    return f"总数: {format_number(total)}\n最大: {max_label} ({format_number(max(values))})\n最小: {min_label} ({format_number(min(values))})"


def pad_table_rows(
    rows: list[list[str]],
    column_count: int,
    *,
    target_rows: int = 10,
    empty_label: str = "暂无数据",
) -> list[list[str]]:
    normalized_rows: list[list[str]] = []
    for row in rows[:target_rows]:
        normalized_rows.append(
            [str(row[index]) if index < len(row) else "" for index in range(column_count)]
        )

    if not normalized_rows:
        placeholder = [""] * column_count
        if column_count >= 1:
            placeholder[0] = "-"
        if column_count >= 2:
            placeholder[1] = empty_label
        if column_count >= 3:
            placeholder[-1] = "-"
        normalized_rows.append(placeholder)

    while len(normalized_rows) < target_rows:
        normalized_rows.append([""] * column_count)

    return normalized_rows


def draw_saas_table(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    *,
    title_align: str = "center",
    font_size: float = 8.6,
    header_font_size: float = 9.2,
    title_font_size: float = 11.8,
    row_height: float = 0.096,
    bbox_height: float = 0.97,
    wrap_widths: dict[int, int] | None = None,
    alignments: dict[int, str] | None = None,
    empty_label: str = "暂无数据",
) -> None:
    wrap_widths = wrap_widths or {}
    alignments = alignments or {}
    rows = pad_table_rows(rows, len(headers), empty_label=empty_label)

    def format_table_text(text: str, alignment: str) -> str:
        if alignment != "left":
            return text
        lines = str(text).splitlines() or [str(text)]
        return "\n".join(f"  {line}" for line in lines)

    prepared_rows: list[list[str]] = []
    for row in rows:
        prepared_row: list[str] = []
        for column_index, value in enumerate(row):
            text = str(value)
            if column_index in wrap_widths:
                text = wrap_center_text_v2(text, wrap_widths[column_index])
            text = format_table_text(text, alignments.get(column_index, "center"))
            prepared_row.append(text)
        prepared_rows.append(prepared_row)

    ax.set_axis_off()
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if title:
        title_x = 0.5 if title_align == "center" else 0.0
        title_ha = "center" if title_align == "center" else "left"
        ax.text(
            title_x,
            1.02,
            title,
            ha=title_ha,
            va="bottom",
            color="#000000",
            fontproperties=pdf_font(title_font_size, "bold"),
            transform=ax.transAxes,
        )

    table = ax.table(
        cellText=prepared_rows,
        colLabels=headers,
        bbox=[0.0, 0.0, 1.0, bbox_height if title else 1.0],
        cellLoc="center",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)

    for (row_index, column_index), cell in table.get_celld().items():
        if column_index < len(col_widths):
            cell.set_width(col_widths[column_index])
        cell.set_height(row_height)
        cell.set_edgecolor("#E5E7EB")
        cell.set_linewidth(0.8)
        cell.visible_edges = "B"
        cell.PAD = 0.11
        cell.get_text().set_color("#000000")
        cell.get_text().set_va("center")
        if row_index == 0:
            cell.set_facecolor("#F3F4F6")
            cell.get_text().set_color("#000000")
            cell.get_text().set_fontproperties(pdf_font(header_font_size, "bold"))
            cell.get_text().set_ha("center")
        else:
            cell.set_facecolor("#FFFFFF" if row_index % 2 == 1 else "#F9FAFB")
            cell.get_text().set_fontproperties(pdf_font(font_size))
            cell.get_text().set_ha(alignments.get(column_index, "center"))


def apply_bt_axis_style_black_v2(ax: Any, title: str, centered: bool = False) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="center" if centered else "left", pad=10, color="#000000", fontproperties=pdf_font(9.2 if not centered else 9.4, "bold"))
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=4, colors="#000000", labelsize=7.6)
    apply_axis_tick_fonts(ax, 7.4)
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_color("#000000")


def draw_baota_hot_table_v2(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    font_size: float = 8.6,
    header_font_size: float = 9.2,
    wrap_widths: dict[int, int] | None = None,
    row_height: float = 0.098,
    bbox_height: float = 0.97,
    alignments: dict[int, str] | None = None,
    empty_label: str = "暂无数据",
) -> None:
    draw_saas_table(
        ax,
        title,
        headers,
        rows,
        col_widths,
        title_align="center",
        font_size=font_size,
        header_font_size=header_font_size,
        title_font_size=11.8,
        row_height=row_height,
        bbox_height=bbox_height,
        wrap_widths=wrap_widths,
        alignments=alignments or {index: "center" for index in range(len(headers))},
        empty_label=empty_label,
    )


def build_rank_rows_from_source(rows: list[list[str]], item_index: int, count_index: int, limit: int = 10, join_index: int | None = None) -> list[list[str]]:
    ranked_rows: list[list[str]] = []
    for idx, row in enumerate(rows[:limit], start=1):
        item = str(row[item_index])
        if join_index is not None and join_index < len(row):
            extra = str(row[join_index]).strip()
            if extra:
                item = f"{item} · {extra}"
        item = item[:32] + "..." if len(item) > 35 else item
        ranked_rows.append([str(idx), item, str(row[count_index])])
    return ranked_rows


def draw_baota_rank_table_v2(
    ax: Any,
    title: str,
    item_header: str,
    rows: list[list[str]],
) -> None:
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 11.2)
    ax.text(0.5, 11.0, title, ha="center", va="top", color="#000000", fontproperties=pdf_font(11.8, "bold"))
    header_color = "#8C92A4"
    row_color = "#374151"
    x_rank = 0.10
    x_item = 0.48
    x_count = 0.88
    ax.text(x_rank, 10.45, "排名", ha="center", va="center", color=header_color, fontproperties=pdf_font(9.4, "bold"))
    ax.text(x_item, 10.45, item_header, ha="center", va="center", color=header_color, fontproperties=pdf_font(9.4, "bold"))
    ax.text(x_count, 10.45, "请求数", ha="center", va="center", color=header_color, fontproperties=pdf_font(9.4, "bold"))
    ax.axhline(y=10.0, xmin=0.02, xmax=0.98, color="#D1D5DB", linewidth=1.2)
    for index in range(10):
        y_pos = 9.5 - index
        if index < len(rows):
            rank, item, count = rows[index]
        else:
            rank, item, count = "", "", ""
        ax.text(x_rank, y_pos, rank, ha="center", va="center", color=row_color, fontproperties=pdf_font(9.6))
        ax.text(x_item, y_pos, item, ha="center", va="center", color=row_color, fontproperties=pdf_font(9.6))
        ax.text(x_count, y_pos, count, ha="center", va="center", color=row_color, fontproperties=pdf_font(9.6))
        ax.axhline(y=y_pos - 0.5, xmin=0.02, xmax=0.98, color="#F3F4F6", linewidth=0.8)


def draw_baota_ring_stats_v2(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    colors: list[str],
    labels: dict[str, str] | None = None,
) -> None:
    apply_bt_axis_style_black_v2(ax, title, centered=True)
    chart_labels = list(distribution.keys())
    values = list(distribution.values())
    total = max(sum(values), 1)
    y_positions = list(range(len(chart_labels)))
    ax.grid(False)
    ax.barh(y_positions, values, color=colors[: len(values)], height=0.56)
    ax.set_yticks(y_positions)
    localized_labels = [localize_chart_item(label, labels) for label in chart_labels] if labels else chart_labels
    ax.set_yticklabels(localized_labels)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(MaxNLocator(4) if MaxNLocator is not None else ax.xaxis.get_major_locator())
    ax.set_xlim(0, max(values) * 1.18 if values else 1)
    for idx, value in enumerate(values):
        ratio = value / total * 100
        ax.text(
            value + max(values) * 0.02 if values else 0.1,
            idx,
            f"{format_number(value)}  {ratio:.1f}%",
            va="center",
            ha="left",
            color="#000000",
            fontproperties=pdf_font(7.2),
        )
    apply_axis_tick_fonts(ax, 7.0)


def draw_baota_bar_line_distribution_v2(
    ax: Any,
    title: str,
    categories: list[str],
    visit_values: list[int],
    ip_values: list[int],
    visit_label: str,
    ip_label: str,
) -> None:
    apply_bt_axis_style_black_v2(ax, title, centered=True)
    x_positions = list(range(len(categories)))
    ax.bar(x_positions, visit_values, width=0.52, color="#8ED1FC", label=visit_label, alpha=0.90)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, rotation=35, ha="right")
    ax_right = ax.twinx()
    ax_right.plot(x_positions, ip_values, color="#45D64A", linewidth=1.6, marker="o", markersize=2.6, label=ip_label)
    ax_right.set_facecolor("#FFFFFF")
    ax_right.grid(False)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#000000", labelsize=7.0)
    apply_axis_tick_fonts(ax_right, 7.0)
    for label in list(ax_right.get_yticklabels()):
        label.set_color("#000000")
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(left_handles + right_handles, left_labels + right_labels, loc="upper right", frameon=False, prop=pdf_font(7.2))
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_baota_dense_table_v2(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    *,
    title_font_size: float = 21.0,
    font_size: float = 9.6,
    header_font_size: float = 10.3,
    row_height: float | None = None,
    bbox_height: float = 0.95,
    wrap_widths: dict[int, int] | None = None,
    alignments: dict[int, str] | None = None,
    header_facecolor: str = "#EAF2FF",
    edgecolor: str = "#D8E0EA",
    zebra: tuple[str, str] = ("#F5F7FA", "#FFFFFF"),
    show_verticals: bool = True,
    empty_label: str = "暂无数据",
) -> None:
    wrap_widths = wrap_widths or {}
    alignments = alignments or {}
    rows = pad_table_rows(rows, len(headers), empty_label=empty_label)

    def format_table_text(text: str, alignment: str) -> str:
        if alignment != "left":
            return text
        lines = str(text).splitlines() or [str(text)]
        return "\n".join(f"  {line}" for line in lines)

    prepared_rows: list[list[str]] = []
    for row in rows:
        prepared_row: list[str] = []
        for column_index, value in enumerate(row):
            text = str(value)
            if column_index in wrap_widths:
                text = wrap_center_text_v2(text, wrap_widths[column_index])
            text = format_table_text(text, alignments.get(column_index, "center"))
            prepared_row.append(text)
        prepared_rows.append(prepared_row)

    ax.set_axis_off()
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if title:
        ax.text(
            0.5,
            1.03,
            title,
            ha="center",
            va="bottom",
            color="#000000",
            fontproperties=pdf_font(title_font_size, "bold"),
            transform=ax.transAxes,
        )
    table = ax.table(
        cellText=prepared_rows,
        colLabels=headers,
        bbox=[0.0, 0.0, 1.0, bbox_height],
        cellLoc="center",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    total_rows = max(len(prepared_rows) + 1, 1)
    computed_height = row_height if row_height is not None else min(0.06, bbox_height / (total_rows + 0.4))
    header_height = max(computed_height * 1.8, 0.12)
    for (row_index, column_index), cell in table.get_celld().items():
        if column_index < len(col_widths):
            cell.set_width(col_widths[column_index])
        cell.set_height(header_height if row_index == 0 else computed_height)
        cell.set_edgecolor(edgecolor)
        cell.set_linewidth(0.55)
        cell.visible_edges = "LTRB" if show_verticals else "B"
        cell.PAD = 0.05
        cell.get_text().set_color("#000000")
        cell.get_text().set_va("center")
        if row_index == 0:
            cell.set_facecolor(header_facecolor)
            cell.get_text().set_fontproperties(pdf_font(header_font_size, "bold"))
            cell.get_text().set_ha("center")
            cell.get_text().set_va("center")
            cell.get_text().set_linespacing(1.12)
        else:
            cell.set_facecolor(zebra[0] if row_index % 2 == 1 else zebra[1])
            cell.get_text().set_fontproperties(pdf_font(font_size))
            cell.get_text().set_ha(alignments.get(column_index, "center"))


def build_province_table_rows_v2(
    province_rows: list[list[str]],
    *,
    limit: int = 12,
) -> list[list[str]]:
    sorted_rows = sorted(
        ((str(row[0]), int(row[1]), int(row[2])) for row in province_rows),
        key=lambda item: (-item[2], item[0]),
    )
    return [
        [name, format_number(ip_count), format_number(visit_count)]
        for name, ip_count, visit_count in sorted_rows[:limit]
    ]


def build_client_share_rows_v2(
    distribution: dict[str, int],
    *,
    limit: int = 12,
) -> list[list[str]]:
    total = max(sum(int(value) for value in distribution.values()), 1)
    sorted_items = sorted(distribution.items(), key=lambda item: (-int(item[1]), str(item[0])))
    return [
        [str(name), format_number(int(count)), f"{int(count) / total * 100:.1f}%"]
        for name, count in sorted_items[:limit]
    ]


def collapse_distribution_for_donut_v2(
    distribution: dict[str, int],
    *,
    limit: int = 7,
    other_label: str = "Other",
) -> dict[str, int]:
    sorted_items = sorted(distribution.items(), key=lambda item: (-int(item[1]), str(item[0])))
    if len(sorted_items) <= limit:
        return {str(name): int(value) for name, value in sorted_items}
    kept_items = sorted_items[:limit]
    other_total = sum(int(value) for _, value in sorted_items[limit:])
    collapsed = {str(name): int(value) for name, value in kept_items}
    if other_total > 0:
        collapsed[other_label] = other_total
    return collapsed


def dynamic_top_title(label: str, row_count: int, limit: int = 10) -> str:
    count = min(max(row_count, 0), limit)
    return str(label).replace("Top 10", f"Top {count}")


def draw_baota_province_distribution_v3(ax: Any, demo: dict[str, Any], labels: dict[str, str]) -> None:
    apply_bt_axis_style_black_v2(ax, labels["province_access_distribution"], centered=True)
    categories = demo["province_categories"]
    visit_values = demo["province_visit_values"]
    ip_values = demo["province_ip_values"]
    x_positions = list(range(len(categories)))
    bars = ax.bar(x_positions, visit_values, width=0.48, color="#78C8F9", label=labels["request_volume"], alpha=0.95)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, rotation=0, ha="center")
    ax.tick_params(axis="x", pad=6)
    ax.set_ylabel(labels["request_volume"], color="#000000", fontproperties=pdf_font(7.8))
    ax.set_ylim(0, max(visit_values) * 1.12 if visit_values else 1)
    ax_right = ax.twinx()
    ax_right.plot(
        x_positions,
        ip_values,
        color="#39D353",
        linewidth=1.6,
        marker="o",
        markersize=3.1,
        label=labels["ips"],
    )
    ax_right.set_facecolor("#FFFFFF")
    ax_right.grid(False)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#000000", labelsize=7.0)
    apply_axis_tick_fonts(ax_right, 7.0)
    ax_right.set_ylabel(labels["ips"], color="#000000", fontproperties=pdf_font(7.8))
    ax_right.set_ylim(0, max(ip_values) * 1.12 if ip_values else 1)
    for label in list(ax_right.get_yticklabels()):
        label.set_color("#000000")
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(
        left_handles + right_handles,
        left_labels + right_labels,
        loc="upper right",
        frameon=False,
        prop=pdf_font(7.2),
    )
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_baota_client_distribution_v3(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    labels: dict[str, str],
) -> None:
    localized_items = [(localize_chart_item(str(name), labels), int(value)) for name, value in distribution.items()]
    sorted_items = sorted(localized_items, key=lambda item: (-item[1], item[0]))
    values = [value for _, value in sorted_items]
    names = [name for name, _ in sorted_items]
    total = max(sum(values), 1)
    positive_items = [item for item in sorted_items if item[1] > 0]
    largest_name, largest_value = sorted_items[0]
    smallest_name, smallest_value = positive_items[-1] if positive_items else sorted_items[-1]
    palette = [
        "#FDB3AE",
        "#FFD79C",
        "#A7CBE8",
        "#DCC6F3",
        "#BEE3E8",
        "#BDE7B7",
        "#F8F1B1",
        "#E9D7C5",
        "#F7A7D1",
        "#C9D4E8",
        "#F4C095",
        "#D9E3F0",
    ]
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="center", pad=10, color="#000000", fontproperties=pdf_font(20.0, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    wedges, label_texts, pct_texts = ax.pie(
        values,
        labels=names,
        colors=palette[: len(values)],
        startangle=90,
        labeldistance=1.08,
        pctdistance=0.76,
        autopct=lambda pct: f"{pct:.2f}%" if pct >= 0.4 else "",
        wedgeprops={"width": 0.42, "edgecolor": "#FFFFFF", "linewidth": 1.0},
        radius=0.90,
    )
    for text in label_texts:
        text.set_color("#000000")
        text.set_fontproperties(pdf_font(7.4))
    for text in pct_texts:
        text.set_color("#000000")
        text.set_fontproperties(pdf_font(6.9))
    ax.text(0.0, 0.12, f"{labels['total']}: {format_number(total)}", ha="center", va="center", color="#000000", fontproperties=pdf_font(10.0, "bold"))
    ax.text(
        0.0,
        -0.02,
        f"{labels['largest']}: {largest_name}({format_number(largest_value)})",
        ha="center",
        va="center",
        color="#000000",
        fontproperties=pdf_font(8.1),
    )
    ax.text(
        0.0,
        -0.15,
        f"{labels['smallest']}: {smallest_name}({format_number(smallest_value)})",
        ha="center",
        va="center",
        color="#000000",
        fontproperties=pdf_font(8.1),
    )
    ax.axis("equal")


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    labels = TRANSLATIONS[report_language(config)]
    demo = build_baota_daily_demo_v2(report, config)
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    total_pages = 4
    spider_top_rows = build_rank_share_rows_v2(demo["spider_distribution"], labels, 10)
    status_top_rows = build_rank_share_rows_v2(demo["status_distribution"], labels, 10)
    province_table_rows = build_province_table_rows_v2(demo["province_rows"], limit=10)
    client_table_rows = build_client_share_rows_v2(demo["client_distribution"], limit=10)
    hot_ip_table_rows = [[row[0], row[2], row[3], row[1]] for row in demo["hot_ip_rows"]]
    hot_page_table_rows = demo["hot_page_rows"][:10]
    hot_ip_table_top_rows = hot_ip_table_rows[:10]
    hot_referer_table_rows = demo["hot_referer_rows"][:10]
    client_chart_distribution = collapse_distribution_for_donut_v2(
        demo["client_distribution"],
        limit=7,
        other_label=labels["other"],
    )
    hot_page_headers = [
        labels["url_path"],
        labels["pv"].replace("(", "\n("),
        labels["uv"].replace("(", "\n("),
        labels["requests"],
        labels["traffic_volume"],
    ]
    hot_referer_headers = [
        labels["referer_source"],
        labels["pv"].replace("(", "\n("),
        labels["requests"],
        labels["traffic_volume"],
    ]
    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        page_one.subplots_adjust(left=0.075, right=0.925, top=0.985, bottom=0.04, hspace=0.36, wspace=0.28)
        grid_one = page_one.add_gridspec(5, 12, height_ratios=[0.72, 1.24, 0.92, 3.42, 2.28])
        draw_baota_header_black(page_one.add_subplot(grid_one[0, :]), report, demo, labels, generated_at, 1, total_pages)
        draw_ai_review_card_black(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis_black(page_one.add_subplot(grid_one[2, :]), build_baota_period_kpis(report, config))
        draw_baota_three_line_chart_black(page_one.add_subplot(grid_one[3, :]), demo, labels)
        bottom_row = grid_one[4, :].subgridspec(1, 3, width_ratios=[45, 10, 45], wspace=0.0)
        draw_baota_dual_axis_chart_black(
            page_one.add_subplot(bottom_row[0, 0]),
            labels["performance_load"],
            demo["hour_labels"],
            demo["performance"]["qps"],
            demo["performance"]["response_ms"],
            "QPS",
            "平均响应耗时(ms)" if report_language(config) == "zh" else "Avg Response (ms)",
            "#2563EB",
            "#EF4444",
        )
        draw_baota_dual_axis_chart_black(
            page_one.add_subplot(bottom_row[0, 2]),
            labels["website_traffic"],
            demo["hour_labels"],
            demo["network"]["upload_kb"],
            demo["network"]["download_kb"],
            "上行 KB" if report_language(config) == "zh" else "Upload KB",
            "下行 KB" if report_language(config) == "zh" else "Download KB",
            "#F59E0B",
            "#10B981",
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        page_two.subplots_adjust(left=0.075, right=0.925, top=0.985, bottom=0.035, hspace=0.26, wspace=0.24)
        grid_two = page_two.add_gridspec(4, 12, height_ratios=[0.68, 2.78, 2.58, 2.48])
        draw_baota_header_black(page_two.add_subplot(grid_two[0, :]), report, demo, labels, generated_at, 2, total_pages)
        draw_baota_dense_table_v2(
            page_two.add_subplot(grid_two[1, :]),
            labels["hot_pages"],
            hot_page_headers,
            hot_page_table_rows,
            [0.56, 0.09, 0.09, 0.12, 0.14],
            title_font_size=16.0,
            font_size=8.5,
            header_font_size=8.8,
            row_height=0.067,
            bbox_height=0.95,
            wrap_widths={0: 56},
            alignments={0: "left", 1: "center", 2: "center", 3: "center", 4: "center"},
            header_facecolor="#E9F1FF",
            edgecolor="#D5DEE8",
            empty_label=labels["no_data"],
        )
        draw_baota_dense_table_v2(
            page_two.add_subplot(grid_two[2, :]),
            labels["hot_ips"],
            [labels["ip_address"], labels["request_volume"], labels["traffic_volume"], labels["info"]],
            hot_ip_table_top_rows,
            [0.29, 0.22, 0.15, 0.34],
            title_font_size=16.0,
            font_size=8.5,
            header_font_size=8.8,
            row_height=0.067,
            bbox_height=0.95,
            alignments={0: "left", 1: "center", 2: "center", 3: "left"},
            header_facecolor="#E9F1FF",
            edgecolor="#D5DEE8",
            empty_label=labels["no_data"],
        )
        draw_baota_dense_table_v2(
            page_two.add_subplot(grid_two[3, :]),
            labels["hot_referers"],
            hot_referer_headers,
            hot_referer_table_rows,
            [0.56, 0.11, 0.14, 0.19],
            title_font_size=16.0,
            font_size=8.5,
            header_font_size=8.8,
            row_height=0.074,
            bbox_height=0.95,
            wrap_widths={0: 44},
            alignments={0: "left", 1: "center", 2: "center", 3: "center"},
            header_facecolor="#E9F1FF",
            edgecolor="#D5DEE8",
            empty_label=labels["no_data"],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)

        page_three = create_baota_daily_figure()
        page_three.subplots_adjust(left=0.075, right=0.925, top=0.985, bottom=0.04, hspace=0.38, wspace=0.34)
        grid_three = page_three.add_gridspec(3, 12, height_ratios=[0.68, 2.25, 3.20])
        draw_baota_header_black(page_three.add_subplot(grid_three[0, :]), report, demo, labels, generated_at, 3, total_pages)
        draw_baota_donut_stats_v2(
            page_three.add_subplot(grid_three[1, 0:6]),
            labels["spider_distribution"],
            demo["spider_distribution"],
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8", "#06B6D4", "#CBD5E1"],
            labels,
        )
        draw_baota_donut_stats_v2(
            page_three.add_subplot(grid_three[1, 6:12]),
            labels["http_status_mix"],
            demo["status_distribution"],
            ["#22C55E", "#06B6D4", "#F59E0B", "#FB7185", "#EF4444", "#A855F7", "#64748B", "#CBD5E1"],
            labels,
        )
        draw_baota_hot_table_v2(
            page_three.add_subplot(grid_three[2, 0:6]),
            dynamic_top_title(labels["crawler_top10"], len(spider_top_rows)),
            [labels["rank"], labels["item"], labels["request_volume"], labels["share"]],
            spider_top_rows,
            [0.12, 0.44, 0.22, 0.22],
            font_size=7.8,
            header_font_size=8.4,
            row_height=0.090,
            bbox_height=0.95,
            alignments={0: "center", 1: "left", 2: "center", 3: "center"},
            empty_label=labels["no_data"],
        )
        draw_baota_hot_table_v2(
            page_three.add_subplot(grid_three[2, 6:12]),
            dynamic_top_title(labels["status_detail_top10"], len(status_top_rows)),
            [labels["rank"], labels["status_code"], labels["request_volume"], labels["share"]],
            status_top_rows,
            [0.12, 0.32, 0.28, 0.28],
            font_size=7.8,
            header_font_size=8.4,
            row_height=0.090,
            bbox_height=0.95,
            alignments={0: "center", 1: "left", 2: "center", 3: "center"},
            empty_label=labels["no_data"],
        )
        pdf.savefig(page_three, facecolor="#FFFFFF")
        plt.close(page_three)

        page_four = create_baota_daily_figure()
        page_four.subplots_adjust(left=0.070, right=0.930, top=0.985, bottom=0.032, hspace=0.40, wspace=0.30)
        grid_four = page_four.add_gridspec(3, 12, height_ratios=[0.68, 2.35, 3.12])
        draw_baota_header_black(page_four.add_subplot(grid_four[0, :]), report, demo, labels, generated_at, 4, total_pages)
        draw_baota_province_distribution_v3(page_four.add_subplot(grid_four[1, 0:6]), demo, labels)
        draw_baota_donut_stats_v2(
            page_four.add_subplot(grid_four[1, 6:12]),
            labels["client_distribution"],
            client_chart_distribution,
            ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#94A3B8", "#06B6D4", "#F97316", "#CBD5E1"],
            labels,
        )
        draw_baota_dense_table_v2(
            page_four.add_subplot(grid_four[2, 0:6]),
            dynamic_top_title(labels["province_top10"], len(province_table_rows)),
            [labels["province"], labels["ips"], labels["request_volume"]],
            province_table_rows,
            [0.44, 0.22, 0.34],
            title_font_size=14.0,
            font_size=8.6,
            header_font_size=8.8,
            row_height=0.074,
            bbox_height=0.90,
            alignments={0: "left", 1: "center", 2: "center"},
            header_facecolor="#E9F1FF",
            edgecolor="#D5DEE8",
            empty_label=labels["no_data"],
        )
        draw_baota_dense_table_v2(
            page_four.add_subplot(grid_four[2, 6:12]),
            dynamic_top_title(labels["client_top10"], len(client_table_rows)),
            [labels["client"], labels["visit_volume"], labels["share"]],
            client_table_rows,
            [0.44, 0.28, 0.28],
            title_font_size=14.0,
            font_size=8.6,
            header_font_size=8.8,
            row_height=0.074,
            bbox_height=0.90,
            alignments={0: "left", 1: "center", 2: "center"},
            header_facecolor="#E9F1FF",
            edgecolor="#D5DEE8",
            empty_label=labels["no_data"],
        )
        pdf.savefig(page_four, facecolor="#FFFFFF")
        plt.close(page_four)
    return output_path


def summarize_ai_review(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    snapshot = build_ai_review_snapshot(report)
    prompt = build_ai_review_prompt(snapshot)
    ai_block = report.get("ai_analysis") or {}
    text = str(ai_block.get("summary") or "").strip()
    source = str(ai_block.get("source") or "").strip() or "llm"
    if looks_like_garbled_text(text):
        text = ""
    if not text:
        text = request_ai_review(config, prompt)
        if not text:
            text = simulated_ai_review(snapshot)
            source = "simulated"
    return {
        "title": "AI 智能运维点评" if report_language(config) == "zh" else "AI Operations Review",
        "summary": text,
        "snapshot": snapshot,
        "prompt": prompt,
        "source": source,
    }


def draw_baota_donut_stats_v2(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    colors: list[str],
    labels: dict[str, str] | None = None,
) -> None:
    cleaned_distribution = {
        str(name): int(value)
        for name, value in (distribution or {}).items()
        if int(value) > 0
    }
    ax.set_facecolor("#FFFFFF")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, loc="left", pad=8, color="#000000", fontproperties=pdf_font(10.4, "bold"))
    if not cleaned_distribution:
        ax.text(
            0.5,
            0.5,
            labels["no_data"] if labels else "No data",
            ha="center",
            va="center",
            color="#000000",
            fontproperties=pdf_font(9.0),
            transform=ax.transAxes,
        )
        ax.axis("off")
        return
    localized_distribution: dict[str, int] = {}
    for name, value in cleaned_distribution.items():
        localized_distribution[localize_chart_item(name, labels)] = value
    values = list(localized_distribution.values())
    total = max(sum(values), 1)
    wedges, _ = ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        labels=None,
        wedgeprops={"width": 0.26, "edgecolor": "#FFFFFF", "linewidth": 1.2},
        radius=0.88,
    )
    ax.text(0.0, 0.08, format_number(sum(values)), ha="center", va="center", color="#000000", fontproperties=pdf_font(11.4, "bold"))
    ax.text(0.0, -0.08, labels["count"] if labels else "Count", ha="center", va="center", color="#000000", fontproperties=pdf_font(7.0))
    legend_labels = [
        f"{name} {value / total * 100:.1f}% ({format_number(value)})"
        for name, value in localized_distribution.items()
    ]
    legend = ax.legend(
        wedges,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        frameon=False,
        prop=pdf_font(6.8),
        handlelength=0.9,
        ncol=2 if len(values) <= 4 else 3,
    )
    for text in legend.get_texts():
        text.set_color("#000000")
    ax.axis("equal")


def draw_baota_province_distribution_v3(ax: Any, demo: dict[str, Any], labels: dict[str, str]) -> None:
    categories = list(demo.get("province_categories") or [])
    visit_values = list(demo.get("province_visit_values") or [])
    ip_values = list(demo.get("province_ip_values") or [])
    apply_bt_axis_style_black_v2(ax, labels["province_access_distribution"], centered=True)
    if not categories or not visit_values or not ip_values:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(9.0), transform=ax.transAxes)
        ax.axis("off")
        return
    x_positions = list(range(len(categories)))
    ax.bar(x_positions, visit_values, width=0.48, color="#78C8F9", label=labels["request_volume"], alpha=0.95)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, rotation=0, ha="center")
    ax.tick_params(axis="x", pad=6)
    apply_axis_tick_fonts(ax, 7.0)
    ax.set_ylabel(labels["request_volume"], color="#000000", fontproperties=pdf_font(7.8))
    ax.set_ylim(0, max(visit_values) * 1.12 if visit_values else 1)
    ax_right = ax.twinx()
    ax_right.plot(
        x_positions,
        ip_values,
        color="#39D353",
        linewidth=1.6,
        marker="o",
        markersize=3.1,
        label=labels["ips"],
    )
    ax_right.set_facecolor("#FFFFFF")
    ax_right.grid(False)
    for spine in ax_right.spines.values():
        spine.set_visible(False)
    ax_right.tick_params(axis="y", length=0, pad=4, colors="#000000", labelsize=7.0)
    apply_axis_tick_fonts(ax_right, 7.0)
    ax_right.set_ylabel(labels["ips"], color="#000000", fontproperties=pdf_font(7.8))
    ax_right.set_ylim(0, max(ip_values) * 1.12 if ip_values else 1)
    for label in list(ax_right.get_yticklabels()):
        label.set_color("#000000")
    left_handles, left_labels = ax.get_legend_handles_labels()
    right_handles, right_labels = ax_right.get_legend_handles_labels()
    legend = ax.legend(
        left_handles + right_handles,
        left_labels + right_labels,
        loc="upper right",
        frameon=False,
        prop=pdf_font(7.2),
    )
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_baota_client_distribution_v3(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    labels: dict[str, str],
) -> None:
    cleaned_distribution = {
        str(name): int(value)
        for name, value in (distribution or {}).items()
        if int(value) > 0
    }
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, loc="center", pad=10, color="#000000", fontproperties=pdf_font(20.0, "bold"))
    ax.set_xticks([])
    ax.set_yticks([])
    if not cleaned_distribution:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(9.0), transform=ax.transAxes)
        ax.axis("off")
        return
    localized_items = [(localize_chart_item(str(name), labels), int(value)) for name, value in cleaned_distribution.items()]
    sorted_items = sorted(localized_items, key=lambda item: (-item[1], item[0]))
    values = [value for _, value in sorted_items]
    names = [name for name, _ in sorted_items]
    total = max(sum(values), 1)
    positive_items = [item for item in sorted_items if item[1] > 0]
    largest_name, largest_value = sorted_items[0]
    smallest_name, smallest_value = positive_items[-1] if positive_items else sorted_items[-1]
    palette = [
        "#FDB3AE",
        "#FFD79C",
        "#A7CBE8",
        "#DCC6F3",
        "#BEE3E8",
        "#BDE7B7",
        "#F8F1B1",
        "#E9D7C5",
        "#F7A7D1",
        "#C9D4E8",
        "#F4C095",
        "#D9E3F0",
    ]
    wedges, label_texts, pct_texts = ax.pie(
        values,
        labels=names,
        colors=palette[: len(values)],
        startangle=90,
        labeldistance=1.08,
        pctdistance=0.76,
        autopct=lambda pct: f"{pct:.2f}%" if pct >= 0.4 else "",
        wedgeprops={"width": 0.42, "edgecolor": "#FFFFFF", "linewidth": 1.0},
        radius=0.90,
    )
    for text in label_texts:
        text.set_color("#000000")
        text.set_fontproperties(pdf_font(7.4))
    for text in pct_texts:
        text.set_color("#000000")
        text.set_fontproperties(pdf_font(6.9))
    ax.text(0.0, 0.12, f"{labels['total']}: {format_number(total)}", ha="center", va="center", color="#000000", fontproperties=pdf_font(10.0, "bold"))
    ax.text(0.0, -0.02, f"{labels['largest']}: {largest_name}({format_number(largest_value)})", ha="center", va="center", color="#000000", fontproperties=pdf_font(8.1))
    ax.text(0.0, -0.15, f"{labels['smallest']}: {smallest_name}({format_number(smallest_value)})", ha="center", va="center", color="#000000", fontproperties=pdf_font(8.1))
    ax.axis("equal")


def draw_baota_three_line_series_black(
    ax: Any,
    title: str,
    x_labels: list[str],
    pv_values: list[float],
    uv_values: list[float],
    ip_values: list[float],
    labels: dict[str, str],
    *,
    rotation: int = 0,
    max_ticks: int = 7,
) -> None:
    apply_bt_axis_style_black(ax, title)
    if not x_labels:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(9.0), transform=ax.transAxes)
        ax.axis("off")
        return
    x_positions = list(range(len(x_labels)))
    ax.plot(x_positions, pv_values, color="#2563EB", linewidth=1.5, label=labels["pv"])
    ax.fill_between(x_positions, pv_values, color="#2563EB", alpha=0.12)
    ax.plot(x_positions, uv_values, color="#10B981", linewidth=1.5, label=labels["uv"])
    ax.fill_between(x_positions, uv_values, color="#10B981", alpha=0.10)
    ax.plot(x_positions, ip_values, color="#F59E0B", linewidth=1.4, label=labels["ips"])
    ax.fill_between(x_positions, ip_values, color="#F59E0B", alpha=0.08)
    ax.set_xlim(-0.3, len(x_positions) - 0.7 if len(x_positions) > 1 else 0.7)
    tick_step = max(1, math.ceil(len(x_labels) / max(max_ticks, 1)))
    tick_positions = list(range(0, len(x_labels), tick_step))
    if tick_positions and tick_positions[-1] != len(x_labels) - 1:
        tick_positions.append(len(x_labels) - 1)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([x_labels[index] for index in tick_positions], rotation=rotation, ha="right" if rotation else "center")
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(7.6), ncol=3, handlelength=1.8)
    for text in legend.get_texts():
        text.set_color("#000000")


def localized_unclassified(config: dict[str, Any]) -> str:
    return "未分类" if report_language(config) == "zh" else "Unclassified"


def fallback_table_rows(column_count: int, config: dict[str, Any]) -> list[list[str]]:
    return [[t(config, "no_data")] + ["-"] * (column_count - 1)]


def build_status_distribution_map(report: dict[str, Any]) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for row in report.get("status_codes", []):
        distribution[str(row["item"])] = int(row["count"] or 0)
    return distribution


def build_spider_distribution_map(report: dict[str, Any]) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for row in report.get("spiders", []):
        distribution[str(row["item"])] = int(row["count"] or 0)
    return distribution


def build_hot_page_rows_from_report(report: dict[str, Any], config: dict[str, Any], limit: int = 10) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in (report.get("top_uri_details") or [])[:limit]:
        request_count = int(row.get("request_count") or row.get("count") or 0)
        uv_count = row.get("uv_count")
        rows.append(
            [
                sanitize_long_table_text(row.get("item") or "-", limit=45, strip_query=True),
                format_number(request_count),
                format_number(uv_count) if uv_count is not None else "-",
                format_number(request_count),
                format_bytes(int(row.get("bytes_out") or 0)) if int(row.get("bytes_out") or 0) > 0 else "-",
            ]
        )
    if rows:
        return rows
    for row in (report.get("top_uris") or [])[:limit]:
        request_count = int(row.get("count") or 0)
        rows.append(
            [
                sanitize_long_table_text(row.get("item") or "-", limit=45, strip_query=True),
                format_number(request_count),
                "-",
                format_number(request_count),
                "-",
            ]
        )
    return rows or fallback_table_rows(5, config)


def build_hot_source_rows_from_report(report: dict[str, Any], config: dict[str, Any], limit: int = 10) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in (report.get("top_sources") or [])[:limit]:
        request_count = int(row.get("request_count") or row.get("count") or 0)
        rows.append(
            [
                sanitize_long_table_text(row.get("item") or "-", limit=45, strip_query=True),
                format_number(request_count),
                format_number(request_count),
                format_bytes(int(row.get("bytes_out") or 0)) if int(row.get("bytes_out") or 0) > 0 else "-",
            ]
        )
    return rows or fallback_table_rows(4, config)


def build_hot_ip_rows_from_report(report: dict[str, Any], config: dict[str, Any], limit: int = 10) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in (report.get("top_client_ips") or [])[:limit]:
        rows.append(
            [
                str(row.get("item") or "-"),
                format_number(int(row.get("request_count") or row.get("count") or 0)),
                format_bytes(int(row.get("bytes_out") or 0)) if int(row.get("bytes_out") or 0) > 0 else "-",
                str(row.get("region") or localized_unknown_region(config)),
                str(row.get("info") or localized_unknown_info(config)),
            ]
        )
    if rows:
        return rows
    for row in (report.get("abnormal_ips") or [])[:limit]:
        rows.append(
            [
                str(row.get("item") or "-"),
                format_number(int(row.get("count") or 0)),
                "-",
                localized_unknown_region(config),
                localized_unknown_info(config),
            ]
        )
    return rows or fallback_table_rows(5, config)


def build_province_payload_from_report(report: dict[str, Any], config: dict[str, Any]) -> tuple[list[list[str]], list[str], list[int], list[int]]:
    rows = report.get("province_distribution") or []
    if not rows:
        rows = [
            {
                "item": localized_unknown_region(config),
                "request_count": int(report.get("traffic", {}).get("request_count") or 0),
                "unique_ips": int(report.get("traffic", {}).get("unique_ips") or 0),
            }
        ]
    table_rows = [
        [str(row.get("item") or localized_unknown_region(config)), format_number(int(row.get("unique_ips") or 0)), format_number(int(row.get("request_count") or 0))]
        for row in rows[:10]
    ]
    chart_rows = rows[:10]
    return (
        table_rows,
        [str(row.get("item") or localized_unknown_region(config)) for row in chart_rows],
        [int(row.get("unique_ips") or 0) for row in chart_rows],
        [int(row.get("request_count") or 0) for row in chart_rows],
    )


def build_client_distribution_from_report(report: dict[str, Any], config: dict[str, Any]) -> dict[str, int]:
    distribution = {
        str(row.get("item") or localized_unclassified(config)): int(row.get("request_count") or row.get("count") or 0)
        for row in (report.get("client_families") or [])
        if int(row.get("request_count") or row.get("count") or 0) > 0
    }
    if distribution:
        return distribution
    fallback_value = max(int(report.get("traffic", {}).get("request_count") or 0), 1)
    return {localized_unclassified(config): fallback_value}


def build_client_table_rows_from_distribution(distribution: dict[str, int], limit: int = 10) -> list[list[str]]:
    return build_client_share_rows_v2(distribution, limit=limit)


def build_dashboard_view(report: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    report_kind = report["meta"]["report_kind"]
    labels = TRANSLATIONS[report_language(config)]
    traffic = report.get("traffic", {})
    if report_kind == "daily":
        series = report.get("hourly_series") or []
        x_labels = [f"{int(item.get('hour') or 0):02d}:00" for item in series]
        trend = {
            "pv": [float(item.get("pv") or 0.0) for item in series],
            "uv": [float(item.get("uv") or 0.0) for item in series],
            "ip": [float(item.get("unique_ips") or 0.0) for item in series],
        }
        performance = {
            "qps": [float(item.get("peak_qps") or 0.0) for item in series],
            "response_ms": [float(item.get("avg_response_ms") or 0.0) for item in series],
        }
        network = {
            "upload_kb": [float(item.get("bandwidth_in_bytes") or 0.0) / 1024.0 for item in series],
            "download_kb": [float(item.get("bandwidth_out_bytes") or 0.0) / 1024.0 for item in series],
        }
        trend_title = labels["daily_hourly_trend"]
        rotation = 0
    else:
        series = report.get("traffic_series") or []
        x_labels = [str(item.get("date") or "")[5:] for item in series]
        trend = {
            "pv": [float(item.get("pv") or 0.0) for item in series],
            "uv": [float(item.get("uv") or 0.0) for item in series],
            "ip": [float(item.get("unique_ips") or 0.0) for item in series],
        }
        performance = {
            "qps": [float(item.get("qps_peak") or 0.0) for item in series],
            "response_ms": [float(item.get("avg_response_ms") or 0.0) for item in series],
        }
        network = {
            "upload_kb": [float(item.get("bandwidth_in_bytes") or 0.0) / 1024.0 for item in series],
            "download_kb": [float(item.get("bandwidth_out_bytes") or 0.0) / 1024.0 for item in series],
        }
        trend_title = labels["trend_pv_uv"] if report_kind == "weekly" else labels["trend_30d"]
        rotation = 28
    province_rows, province_categories, province_ip_values, province_visit_values = build_province_payload_from_report(report, config)
    client_distribution = build_client_distribution_from_report(report, config)
    return {
        "title": t(config, f"{report_kind}_title"),
        "site": str(report["meta"]["site"]),
        "window": f"{report['meta']['window_start']} - {report['meta']['window_end']}",
        "total_requests": format_number(traffic.get("request_count")),
        "total_traffic": format_bytes(total_traffic_bytes(report)),
        "ssl_summary": format_ssl_summary_text(config, report.get("ssl") or {}),
        "x_labels": x_labels,
        "trend": trend,
        "performance": performance,
        "network": network,
        "trend_title": trend_title,
        "x_rotation": rotation,
        "hot_page_rows": build_hot_page_rows_from_report(report, config),
        "hot_ip_rows": build_hot_ip_rows_from_report(report, config),
        "hot_referer_rows": build_hot_source_rows_from_report(report, config),
        "spider_distribution": build_spider_distribution_map(report),
        "status_distribution": build_status_distribution_map(report),
        "province_rows": province_rows,
        "province_categories": province_categories,
        "province_ip_values": province_ip_values,
        "province_visit_values": province_visit_values,
        "client_distribution": client_distribution,
    }


def compact_distribution(
    distribution: dict[str, int],
    *,
    limit: int = 10,
) -> dict[str, int]:
    sorted_items = sorted(
        (
            (str(name), int(value))
            for name, value in (distribution or {}).items()
            if int(value) > 0
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return {name: value for name, value in sorted_items[:limit]}


def draw_distribution_bar_panel(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    colors: list[str],
    labels: dict[str, str],
) -> None:
    cleaned_distribution = compact_distribution(distribution, limit=10)
    if not cleaned_distribution:
        apply_bt_axis_style_black_v2(ax, title, centered=True)
        ax.text(
            0.5,
            0.5,
            labels["no_data"],
            ha="center",
            va="center",
            color="#000000",
            fontproperties=pdf_font(9.0),
            transform=ax.transAxes,
        )
        ax.axis("off")
        return
    draw_baota_ring_stats_v2(ax, title, cleaned_distribution, colors, labels)


def looks_like_garbled_text(text: str) -> bool:
    compact = re.sub(r"\s+", "", str(text or ""))
    if not compact:
        return True
    marker_count = compact.count("?") + compact.count("？") + compact.count("\ufffd")
    return marker_count >= 4 and marker_count / max(len(compact), 1) >= 0.15


def build_spider_trend_dataset(
    report: dict[str, Any],
    *,
    limit: int = 5,
) -> tuple[list[str], dict[str, list[int]]]:
    top_distribution = compact_distribution(build_spider_distribution_map(report), limit=limit)
    if not top_distribution:
        return [], {}

    series_rows = report.get("spider_daily_series") or []
    if series_rows:
        x_labels = [str(row.get("date") or "")[5:] for row in series_rows]
        series_map = {name: [] for name in top_distribution}
        for row in series_rows:
            counts = row.get("counts") or {}
            for name in series_map:
                series_map[name].append(int(counts.get(name) or 0))
        return x_labels, series_map

    traffic_series = report.get("traffic_series") or []
    if not traffic_series:
        return [], {}

    x_labels = [str(item.get("date") or "")[5:] for item in traffic_series]
    total = max(sum(top_distribution.values()), 1)
    series_map = {name: [] for name in top_distribution}
    ordered_names = list(series_map.keys())
    for item in traffic_series:
        daily_total = int(item.get("spider_total") or 0)
        allocated = 0
        for index, name in enumerate(ordered_names):
            if index == len(ordered_names) - 1:
                value = max(daily_total - allocated, 0)
            else:
                value = int(round(daily_total * top_distribution[name] / total))
                allocated += value
            series_map[name].append(max(value, 0))
    return x_labels, series_map


def build_status_trend_dataset(report: dict[str, Any]) -> tuple[list[str], dict[str, list[int]]]:
    overall_families = {
        str(item.get("item") or ""): int(item.get("count") or 0)
        for item in (report.get("status_families") or aggregate_status_families(report.get("status_codes") or []))
        if int(item.get("count") or 0) > 0
    }
    family_order = [name for name in ("2xx", "3xx", "4xx", "5xx") if overall_families.get(name, 0) > 0]
    if not family_order:
        family_order = ["2xx", "3xx", "4xx", "5xx"]

    series_rows = report.get("status_family_series") or []
    if series_rows:
        x_labels = [str(row.get("date") or "")[5:] for row in series_rows]
        series_map = {family: [] for family in family_order}
        for row in series_rows:
            counts = row.get("counts") or {}
            for family in family_order:
                series_map[family].append(int(counts.get(family) or 0))
        return x_labels, series_map

    traffic_series = report.get("traffic_series") or []
    if not traffic_series:
        return [], {}

    x_labels = [str(item.get("date") or "")[5:] for item in traffic_series]
    total_family = max(sum(overall_families.get(name, 0) for name in family_order), 1)
    share_4xx = overall_families.get("4xx", 0) / total_family
    share_5xx = overall_families.get("5xx", 0) / total_family
    share_3xx_base = overall_families.get("3xx", 0)
    share_2xx_base = overall_families.get("2xx", 0)
    share_3xx = share_3xx_base / max(share_2xx_base + share_3xx_base, 1)
    series_map = {family: [] for family in family_order}
    for item in traffic_series:
        request_count = int(item.get("request_count") or 0)
        four_xx = max(int(item.get("http_404_count") or 0), int(round(request_count * share_4xx)))
        five_xx = max(int(item.get("http_5xx_count") or 0), int(round(request_count * share_5xx)))
        remainder = max(request_count - four_xx - five_xx, 0)
        three_xx = int(round(remainder * share_3xx))
        two_xx = max(remainder - three_xx, 0)
        derived = {"2xx": two_xx, "3xx": three_xx, "4xx": four_xx, "5xx": five_xx}
        for family in family_order:
            series_map[family].append(int(derived.get(family) or 0))
    return x_labels, series_map


def draw_spider_trend_panel(
    ax: Any,
    report: dict[str, Any],
    config: dict[str, Any],
    labels: dict[str, str],
) -> None:
    title = "蜘蛛抓取趋势" if report_language(config) == "zh" else "Spider Crawl Trend"
    apply_bt_axis_style_black_v2(ax, title, centered=True)
    x_labels, series_map = build_spider_trend_dataset(report, limit=5)
    if not x_labels or not series_map:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(9.0), transform=ax.transAxes)
        ax.axis("off")
        return
    palette = ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6", "#06B6D4"]
    x_positions = list(range(len(x_labels)))
    for index, (name, values) in enumerate(series_map.items()):
        color = palette[index % len(palette)]
        ax.plot(
            x_positions,
            values,
            color=color,
            linewidth=1.6,
            marker="o",
            markersize=2.6,
            label=localize_chart_item(name, labels),
        )
        ax.fill_between(x_positions, values, color=color, alpha=0.06)
    ax.set_xlim(-0.2, len(x_positions) - 0.8 if len(x_positions) > 1 else 0.8)
    tick_step = max(1, math.ceil(len(x_labels) / 6))
    tick_positions = list(range(0, len(x_labels), tick_step))
    if tick_positions and tick_positions[-1] != len(x_labels) - 1:
        tick_positions.append(len(x_labels) - 1)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([x_labels[index] for index in tick_positions], rotation=28, ha="right")
    apply_axis_tick_fonts(ax, 7.0)
    if MaxNLocator is not None:
        ax.yaxis.set_major_locator(MaxNLocator(4))
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(6.8), ncol=2, handlelength=1.5)
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_status_trend_panel(
    ax: Any,
    report: dict[str, Any],
    config: dict[str, str] | dict[str, Any],
    labels: dict[str, str],
) -> None:
    title = "状态码趋势" if report_language(config) == "zh" else "HTTP Status Trend"
    apply_bt_axis_style_black_v2(ax, title, centered=True)
    x_labels, series_map = build_status_trend_dataset(report)
    if not x_labels or not series_map:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(9.0), transform=ax.transAxes)
        ax.axis("off")
        return
    family_colors = {"2xx": "#22C55E", "3xx": "#06B6D4", "4xx": "#F59E0B", "5xx": "#EF4444"}
    x_positions = list(range(len(x_labels)))
    ordered_families = list(series_map.keys())
    ax.stackplot(
        x_positions,
        *[series_map[family] for family in ordered_families],
        colors=[family_colors.get(family, "#94A3B8") for family in ordered_families],
        alpha=0.20,
        labels=ordered_families,
    )
    for family in ordered_families:
        ax.plot(
            x_positions,
            series_map[family],
            color=family_colors.get(family, "#94A3B8"),
            linewidth=1.35,
            label=family,
        )
    ax.set_xlim(-0.2, len(x_positions) - 0.8 if len(x_positions) > 1 else 0.8)
    tick_step = max(1, math.ceil(len(x_labels) / 6))
    tick_positions = list(range(0, len(x_labels), tick_step))
    if tick_positions and tick_positions[-1] != len(x_labels) - 1:
        tick_positions.append(len(x_labels) - 1)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([x_labels[index] for index in tick_positions], rotation=28, ha="right")
    apply_axis_tick_fonts(ax, 7.0)
    if MaxNLocator is not None:
        ax.yaxis.set_major_locator(MaxNLocator(4))
    legend = ax.legend(loc="upper left", frameon=False, prop=pdf_font(6.8), ncol=2, handlelength=1.5)
    for text in legend.get_texts():
        text.set_color("#000000")


def locale_text(config: dict[str, Any], zh: str, en: str) -> str:
    return zh if report_language(config) == "zh" else en


def draw_enterprise_card_shell(ax: Any, title: str, subtitle: str | None = None) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    title_text = wrap_dashboard_text(title, width=26)
    subtitle_text = wrap_dashboard_text(subtitle, width=42) if subtitle else None
    patch = FancyBboxPatch(
        (0.0, 0.0),
        1.0,
        1.0,
        boxstyle="round,pad=0.014,rounding_size=0.040",
        facecolor=CARD_COLORS["face"],
        edgecolor=CARD_COLORS["edge"],
        linewidth=0.8,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)
    ax.text(
        0.05,
        0.93,
        title_text,
        ha="left",
        va="top",
        color="#111111",
        linespacing=1.25,
        fontproperties=pdf_font(9.0, "bold"),
        transform=ax.transAxes,
    )
    if subtitle_text:
        ax.text(
            0.05,
            0.84,
            subtitle_text,
            ha="left",
            va="top",
            color="#000000",
            linespacing=1.28,
            fontproperties=pdf_font(7.2),
            transform=ax.transAxes,
        )


def draw_enterprise_donut_card(
    ax: Any,
    title: str,
    distribution: dict[str, int],
    colors: list[str],
    labels: dict[str, str],
    center_caption: str,
) -> None:
    draw_enterprise_card_shell(ax, title)
    cleaned_distribution = compact_distribution(distribution, limit=5)
    if not cleaned_distribution:
        ax.text(0.5, 0.48, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(8.0), transform=ax.transAxes)
        return
    chart_ax = ax.inset_axes([0.06, 0.12, 0.48, 0.70])
    chart_ax.set_axis_off()
    chart_ax.set_aspect("equal")
    localized_items = [(localize_chart_item(name, labels), value) for name, value in cleaned_distribution.items()]
    values = [value for _, value in localized_items]
    total = max(sum(values), 1)
    wedges, _ = chart_ax.pie(
        values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        labels=None,
        wedgeprops={"width": 0.26, "edgecolor": CARD_COLORS["face"], "linewidth": 1.2},
        radius=0.94,
    )
    chart_ax.text(0.0, 0.04, format_number(total), ha="center", va="center", color="#111111", fontproperties=pdf_font(10.5, "bold"))
    chart_ax.text(0.0, -0.16, center_caption, ha="center", va="center", color="#000000", fontproperties=pdf_font(6.8))
    legend_labels = [f"{name}  {value / total * 100:.1f}%" for name, value in localized_items]
    legend = chart_ax.legend(
        wedges,
        legend_labels,
        loc="upper left",
        bbox_to_anchor=(1.02, 0.96),
        frameon=False,
        prop=pdf_font(6.7),
        handlelength=1.1,
        borderaxespad=0.0,
        labelspacing=0.8,
        handletextpad=0.6,
    )
    for text in legend.get_texts():
        text.set_color("#000000")


def draw_enterprise_metrics_card(
    ax: Any,
    title: str,
    metrics: list[dict[str, str]],
) -> None:
    draw_enterprise_card_shell(ax, title)
    y_positions = [0.75, 0.49, 0.23]
    for metric, y_pos in zip(metrics[:3], y_positions):
        value_text = str(metric.get("value") or "-")
        value_font = 18.5 if len(value_text) <= 10 else 14.0
        ax.text(0.06, y_pos + 0.08, str(metric.get("label") or ""), ha="left", va="top", color="#000000", fontproperties=pdf_font(7.4), transform=ax.transAxes)
        ax.text(0.06, y_pos - 0.01, value_text, ha="left", va="center", color="#111111", fontproperties=pdf_font(value_font, "bold"), transform=ax.transAxes)
        note_text = wrap_dashboard_text(str(metric.get("note") or ""), width=26)
        ax.text(0.06, y_pos - 0.12, note_text, ha="left", va="top", color="#000000", linespacing=1.35, fontproperties=pdf_font(6.8), transform=ax.transAxes)


def draw_enterprise_table_body(
    ax: Any,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    *,
    alignments: dict[int, str] | None = None,
    truncate_rules: dict[int, dict[str, Any]] | None = None,
    empty_label: str,
) -> None:
    alignments = alignments or {}
    truncate_rules = truncate_rules or {}
    normalized_rows = pad_table_rows(rows, len(headers), empty_label=empty_label)
    prepared_rows: list[list[str]] = []
    for row in normalized_rows:
        prepared_row: list[str] = []
        for column_index, value in enumerate(row):
            text = str(value or "")
            if column_index in truncate_rules and text:
                options = truncate_rules[column_index]
                text = sanitize_long_table_text(
                    text,
                    limit=int(options.get("limit", 40)),
                    strip_query=bool(options.get("strip_query", False)),
                )
            if alignments.get(column_index) == "left" and text:
                text = f"  {text}"
            prepared_row.append(text)
        prepared_rows.append(prepared_row)

    ax.set_axis_off()
    ax.axis("off")
    table = ax.table(
        cellText=prepared_rows,
        colLabels=headers,
        bbox=[0.0, 0.0, 1.0, 1.0],
        cellLoc="center",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.4)
    total_rows = max(len(prepared_rows) + 1, 1)
    row_height = min(0.088, 0.96 / total_rows)
    header_height = max(row_height * 1.18, 0.09)
    for (row_index, column_index), cell in table.get_celld().items():
        if column_index < len(col_widths):
            cell.set_width(col_widths[column_index])
        cell.set_height(header_height if row_index == 0 else row_height)
        cell.set_edgecolor(CARD_COLORS["edge"])
        cell.set_linewidth(0.6)
        cell.visible_edges = "B"
        cell.PAD = 0.08
        cell.get_text().set_color("#111111")
        cell.get_text().set_va("center")
        if row_index == 0:
            cell.set_facecolor(CARD_COLORS["header"])
            cell.get_text().set_fontproperties(pdf_font(7.4, "bold"))
            cell.get_text().set_ha("center")
        else:
            cell.set_facecolor("#FFFFFF" if row_index % 2 == 1 else CARD_COLORS["zebra"])
            cell.get_text().set_fontproperties(pdf_font(7.2))
            cell.get_text().set_ha(alignments.get(column_index, "center"))


def draw_enterprise_table_card(
    ax: Any,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float],
    *,
    subtitle: str | None = None,
    alignments: dict[int, str] | None = None,
    truncate_rules: dict[int, dict[str, Any]] | None = None,
    empty_label: str,
) -> None:
    draw_enterprise_card_shell(ax, title, subtitle)
    table_ax = ax.inset_axes([0.04, 0.08, 0.92, 0.68 if subtitle else 0.74])
    draw_enterprise_table_body(
        table_ax,
        headers,
        rows,
        col_widths,
        alignments=alignments,
        truncate_rules=truncate_rules,
        empty_label=empty_label,
    )


def build_traffic_uri_card_rows(view: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for index, row in enumerate((view.get("hot_page_rows") or [])[:10], start=1):
        path = sanitize_long_table_text(str(row[0]), limit=40, strip_query=True)
        rows.append([str(index), path, str(row[1]), str(row[2]), str(row[3]), str(row[4])])
    return rows


def build_traffic_ip_card_rows(view: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for index, row in enumerate((view.get("hot_ip_rows") or [])[:10], start=1):
        rows.append([str(index), str(row[0]), str(row[1]), str(row[2]), str(row[3])])
    return rows


def build_spider_metrics(report: dict[str, Any], config: dict[str, Any], labels: dict[str, str]) -> list[dict[str, str]]:
    spiders = sorted((report.get("spiders") or []), key=lambda item: (-int(item.get("count") or 0), str(item.get("item") or "")))
    total = total_spider_count(report)
    top_name = localize_chart_item(str(spiders[0].get("item") or labels["other"]), labels) if spiders else labels["other"]
    top_count = int(spiders[0].get("count") or 0) if spiders else 0
    top_share = safe_ratio(top_count, total) * 100.0
    day_count = int(report.get("meta", {}).get("days") or 1)
    avg_daily = int(round(total / max(day_count, 1)))
    return [
        {
            "label": locale_text(config, "总爬取次数", "Total Crawls"),
            "value": format_number(total),
            "note": locale_text(config, f"{day_count} 天累计，日均 {format_number(avg_daily)}", f"{day_count}-day total, avg {format_number(avg_daily)}/day"),
        },
        {
            "label": locale_text(config, "主力爬虫占比", "Dominant Bot"),
            "value": f"{top_share:.1f}%",
            "note": f"{top_name} · {format_number(top_count)}",
        },
        {
            "label": locale_text(config, "活跃爬虫种类", "Active Families"),
            "value": str(len(spiders)),
            "note": locale_text(config, "按抓取量统计的活跃蜘蛛家族", "Families observed in this period"),
        },
    ]


def build_status_metrics(report: dict[str, Any], config: dict[str, Any]) -> list[dict[str, str]]:
    families = {
        str(item.get("item") or ""): int(item.get("count") or 0)
        for item in (report.get("status_families") or aggregate_status_families(report.get("status_codes") or []))
    }
    four_xx = int(families.get("4xx", 0))
    five_xx = int(families.get("5xx", 0))
    total_requests = int(report.get("traffic", {}).get("request_count") or 0)
    error_ratio = safe_ratio(four_xx + five_xx, total_requests) * 100.0
    previous_summary = report.get("previous_summary") or {}
    previous_families = {
        str(item.get("item") or ""): int(item.get("count") or 0)
        for item in (previous_summary.get("status_families") or aggregate_status_families(previous_summary.get("status_codes") or []))
    }
    previous_requests = int(previous_summary.get("traffic", {}).get("request_count") or 0)
    previous_error_ratio = safe_ratio(
        int(previous_families.get("4xx", 0)) + int(previous_families.get("5xx", 0)),
        previous_requests,
    ) * 100.0 if previous_requests else None
    if previous_error_ratio is None or previous_error_ratio == 0:
        compare_value = "N/A"
        compare_note = locale_text(config, "无可用的上一周期基线", "No previous baseline")
    else:
        ratio_delta = ((error_ratio - previous_error_ratio) / previous_error_ratio) * 100.0
        compare_value = f"{ratio_delta:+.1f}%"
        compare_note = locale_text(config, f"上一周期错误率 {previous_error_ratio:.1f}%", f"Previous error ratio {previous_error_ratio:.1f}%")
    return [
        {
            "label": locale_text(config, "错误请求占比", "Error Ratio"),
            "value": f"{error_ratio:.1f}%",
            "note": locale_text(config, "4xx + 5xx 占总请求比例", "4xx + 5xx against total requests"),
        },
        {
            "label": locale_text(config, "5xx 请求总数", "Total 5xx"),
            "value": format_number(five_xx),
            "note": locale_text(config, f"4xx {format_number(four_xx)} · 5xx {format_number(five_xx)}", f"4xx {format_number(four_xx)} · 5xx {format_number(five_xx)}"),
        },
        {
            "label": locale_text(config, "上周期对比", "Previous Period"),
            "value": compare_value,
            "note": compare_note,
        },
    ]


def draw_enterprise_text_card(
    ax: Any,
    title: str,
    body: str,
    *,
    subtitle: str | None = None,
    width: int = 20,
) -> None:
    draw_enterprise_card_shell(ax, title, subtitle)
    wrapped = wrap_dashboard_text(body, width=width)
    line_count = max(wrapped.count("\n") + 1, 1)
    body_font_size = 7.0 if line_count >= 7 else 7.2
    ax.text(
        0.06,
        0.72 if subtitle else 0.78,
        wrapped,
        ha="left",
        va="top",
        color="#000000",
        linespacing=1.45,
        fontproperties=pdf_font(body_font_size),
        transform=ax.transAxes,
    )


def draw_enterprise_chart_card(
    ax: Any,
    title: str,
    renderer: Any,
    *,
    subtitle: str | None = None,
    inset: tuple[float, float, float, float] | None = None,
) -> None:
    draw_enterprise_card_shell(ax, title, subtitle)
    resolved_inset = inset or ((0.07, 0.14, 0.86, 0.60) if subtitle else (0.07, 0.14, 0.86, 0.68))
    inner_ax = ax.inset_axes(resolved_inset)
    renderer(inner_ax)


def build_top_share_summary(
    rows: list[tuple[str, int]],
    config: dict[str, Any],
    *,
    dimension_label: str,
    metric_label: str,
) -> str:
    if not rows:
        return locale_text(config, f"{dimension_label}暂无有效数据。", f"No {dimension_label.lower()} data is available.")
    total = max(sum(value for _, value in rows), 1)
    top_name, top_value = rows[0]
    share = top_value / total * 100.0
    extra = ""
    if len(rows) > 1:
        second_name, second_value = rows[1]
        extra = locale_text(
            config,
            f" 其次为{second_name}，占比约 {second_value / total * 100.0:.1f}%。",
            f" {second_name} follows at roughly {second_value / total * 100.0:.1f}%.",
        )
    return locale_text(
        config,
        f"{dimension_label}以{top_name}为主，{metric_label}{format_number(top_value)}，占比约 {share:.1f}%。{extra}",
        f"{dimension_label} is led by {top_name} with {format_number(top_value)} {metric_label.lower()}, about {share:.1f}% of the total.{extra}",
    )


def request_dimension_ai_insight(
    config: dict[str, Any],
    dimension_title: str,
    payload_rows: list[tuple[str, int]],
    *,
    metric_label: str,
) -> str | None:
    settings = resolve_ai_settings(config)
    if not settings["enabled"] or settings["simulate"] or not settings["endpoint"]:
        return None
    prompt = (
        f"你是一名运维分析师。请根据以下 {dimension_title} Top 数据，用中文输出约 50 字的精简点评，"
        "只需描述最核心的结构特征与风险，不要分点：\n"
        f"{json.dumps(payload_rows[:3], ensure_ascii=False)}"
        if report_language(config) == "zh"
        else (
            f"You are an operations analyst. Based on the following top {dimension_title} rows, "
            "write a concise 40-60 word insight in English. Focus on the dominant source and any anomaly risk.\n"
            f"{json.dumps(payload_rows[:3], ensure_ascii=False)}"
        )
    )
    text = request_ai_review(config, prompt)
    if text and not looks_like_garbled_text(text):
        return text
    return None


def summarize_dimension_insight(
    config: dict[str, Any],
    dimension_title: str,
    payload_rows: list[tuple[str, int]],
    *,
    metric_label: str,
) -> str:
    ai_text = request_dimension_ai_insight(
        config,
        dimension_title,
        payload_rows,
        metric_label=metric_label,
    )
    if ai_text:
        return ai_text
    return build_top_share_summary(
        payload_rows,
        config,
        dimension_label=dimension_title,
        metric_label=metric_label,
    )


def build_province_insight(report: dict[str, Any], config: dict[str, Any]) -> str:
    rows = sorted(
        (
            (str(row.get("item") or localized_unknown_region(config)), int(row.get("request_count") or 0))
            for row in (report.get("province_distribution") or [])
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return summarize_dimension_insight(
        config,
        locale_text(config, "省份流量", "Province traffic"),
        rows,
        metric_label=locale_text(config, "请求", "requests"),
    )


def build_client_insight(report: dict[str, Any], config: dict[str, Any]) -> str:
    rows = sorted(
        (
            (str(row.get("item") or localized_unclassified(config)), int(row.get("request_count") or row.get("count") or 0))
            for row in (report.get("client_families") or [])
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return summarize_dimension_insight(
        config,
        locale_text(config, "客户端分布", "Client distribution"),
        rows,
        metric_label=locale_text(config, "访问量", "visits"),
    )


def draw_daily_spider_status_page(
    pdf: Any,
    report: dict[str, Any],
    config: dict[str, Any],
    view: dict[str, Any],
    labels: dict[str, str],
    generated_at: str,
    total_pages: int,
    spider_chart_distribution: dict[str, int],
    status_chart_distribution: dict[str, int],
    spider_top_rows: list[list[str]],
    status_top_rows: list[list[str]],
) -> None:
    page = create_baota_daily_figure()
    page.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.22, wspace=0.16)
    grid = page.add_gridspec(3, 12, height_ratios=[0.68, 2.18, 2.72])
    draw_baota_header_black(page.add_subplot(grid[0, :]), report, view, labels, generated_at, 3, total_pages)
    top_grid = grid[1, :].subgridspec(1, 2, wspace=0.16)
    draw_enterprise_donut_card(
        page.add_subplot(top_grid[0, 0]),
        locale_text(config, "蜘蛛抓取占比", "Crawler Mix"),
        spider_chart_distribution,
        ENTERPRISE_DONUT_COLORS,
        labels,
        locale_text(config, "抓取次数", "Crawls"),
    )
    draw_enterprise_donut_card(
        page.add_subplot(top_grid[0, 1]),
        locale_text(config, "状态码占比", "Status Mix"),
        status_chart_distribution,
        ["#4E79A7", "#59A14F", "#F28E2B", "#E15759", "#76B7B2", "#EDC948"],
        labels,
        locale_text(config, "请求总量", "Requests"),
    )
    bottom_grid = grid[2, :].subgridspec(1, 2, wspace=0.16)
    draw_enterprise_table_card(
        page.add_subplot(bottom_grid[0, 0]),
        dynamic_top_title(labels["crawler_top10"], len(spider_top_rows)),
        [labels["rank"], labels["item"], labels["request_volume"], labels["share"]],
        spider_top_rows or fallback_table_rows(4, config),
        [0.10, 0.50, 0.16, 0.24],
        alignments={0: "center", 1: "left", 2: "center", 3: "center"},
        empty_label=labels["no_data"],
    )
    draw_enterprise_table_card(
        page.add_subplot(bottom_grid[0, 1]),
        dynamic_top_title(labels["status_detail_top10"], len(status_top_rows)),
        [labels["rank"], labels["status_code"], labels["request_volume"], labels["share"]],
        status_top_rows or fallback_table_rows(4, config),
        [0.10, 0.34, 0.24, 0.32],
        alignments={0: "center", 1: "left", 2: "center", 3: "center"},
        empty_label=labels["no_data"],
    )
    pdf.savefig(page, facecolor="#FFFFFF")
    plt.close(page)


def draw_compact_province_chart(ax: Any, view: dict[str, Any], labels: dict[str, str]) -> None:
    categories = list(view.get("province_categories") or [])[:6]
    visit_values = list(view.get("province_visit_values") or [])[:6]
    ip_values = list(view.get("province_ip_values") or [])[:6]
    apply_bt_axis_style_black_v2(ax, "", centered=False)
    if not categories or not visit_values:
        ax.text(0.5, 0.5, labels["no_data"], ha="center", va="center", color="#000000", fontproperties=pdf_font(8.0), transform=ax.transAxes)
        ax.axis("off")
        return
    x_positions = list(range(len(categories)))
    ax.bar(x_positions, visit_values, width=0.54, color="#6BAED6", alpha=0.95)
    ax.plot(x_positions, ip_values, color="#F28E2B", linewidth=1.5, marker="o", markersize=2.4)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([truncate_text(str(item), 10) for item in categories], rotation=18, ha="right")
    ax.set_xlim(-0.4, len(x_positions) - 0.6 if len(x_positions) > 1 else 0.6)
    apply_axis_tick_fonts(ax, 7.0)


def draw_period_province_page(
    pdf: Any,
    report: dict[str, Any],
    config: dict[str, Any],
    view: dict[str, Any],
    labels: dict[str, str],
    generated_at: str,
    page_number: int,
    total_pages: int,
    province_table_rows: list[list[str]],
) -> None:
    page = create_baota_daily_figure()
    page.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.19, wspace=0.14)
    grid = page.add_gridspec(3, 12, height_ratios=[0.68, 2.22, 2.98])
    draw_baota_header_black(page.add_subplot(grid[0, :]), report, view, labels, generated_at, page_number, total_pages)
    top_grid = grid[1, :].subgridspec(1, 2, wspace=0.14)
    draw_enterprise_chart_card(
        page.add_subplot(top_grid[0, 0]),
        labels["province_access_distribution"],
        lambda inner_ax: draw_compact_province_chart(inner_ax, view, labels),
        subtitle=locale_text(config, "聚焦访问量与活跃 IP 的区域集中度", "Focus on visits and active IP concentration"),
        inset=(0.07, 0.17, 0.87, 0.60),
    )
    draw_enterprise_text_card(
        page.add_subplot(top_grid[0, 1]),
        locale_text(config, "AI 专属点评", "AI Insight"),
        build_province_insight(report, config),
        subtitle=locale_text(config, "基于 Top 3 省份来源的结构性总结", "Based on the top 3 regions"),
        width=18,
    )
    draw_enterprise_table_card(
        page.add_subplot(grid[2, :]),
        dynamic_top_title(labels["province_top10"], len(province_table_rows)),
        [labels["province"], labels["ips"], labels["request_volume"]],
        province_table_rows,
        [0.44, 0.22, 0.34],
        subtitle=locale_text(config, "完整地区明细，支持横向比对访问质量", "Full regional detail for cross comparison"),
        alignments={0: "left", 1: "center", 2: "center"},
        empty_label=labels["no_data"],
    )
    pdf.savefig(page, facecolor="#FFFFFF")
    plt.close(page)


def draw_period_client_page(
    pdf: Any,
    report: dict[str, Any],
    config: dict[str, Any],
    view: dict[str, Any],
    labels: dict[str, str],
    generated_at: str,
    page_number: int,
    total_pages: int,
    client_chart_distribution: dict[str, int],
    client_table_rows: list[list[str]],
) -> None:
    page = create_baota_daily_figure()
    page.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.19, wspace=0.14)
    grid = page.add_gridspec(3, 12, height_ratios=[0.68, 2.22, 2.98])
    draw_baota_header_black(page.add_subplot(grid[0, :]), report, view, labels, generated_at, page_number, total_pages)
    top_grid = grid[1, :].subgridspec(1, 2, wspace=0.14)
    draw_enterprise_donut_card(
        page.add_subplot(top_grid[0, 0]),
        labels["client_distribution"],
        client_chart_distribution,
        ENTERPRISE_DONUT_COLORS,
        labels,
        locale_text(config, "访问量", "Visits"),
    )
    draw_enterprise_text_card(
        page.add_subplot(top_grid[0, 1]),
        locale_text(config, "AI 专属点评", "AI Insight"),
        build_client_insight(report, config),
        subtitle=locale_text(config, "基于 Top 3 客户端的结构性总结", "Based on the top 3 client families"),
        width=18,
    )
    draw_enterprise_table_card(
        page.add_subplot(grid[2, :]),
        dynamic_top_title(labels["client_top10"], len(client_table_rows)),
        [labels["client"], labels["visit_volume"], labels["share"]],
        client_table_rows,
        [0.44, 0.28, 0.28],
        subtitle=locale_text(config, "完整客户端明细，观察浏览器与自动化占比", "Full client detail for browser and automation analysis"),
        alignments={0: "left", 1: "center", 2: "center"},
        empty_label=labels["no_data"],
    )
    pdf.savefig(page, facecolor="#FFFFFF")
    plt.close(page)

def render_dashboard_pdf(
    report: dict[str, Any],
    config: dict[str, Any],
    output_path: Path,
) -> Path:
    labels = TRANSLATIONS[report_language(config)]
    view = build_dashboard_view(report, config)
    ai_review = summarize_ai_review(report, config)
    generated_at = dt.datetime.now(get_timezone(config)).strftime("%Y-%m-%d %H:%M")
    report_kind = str(report.get("meta", {}).get("report_kind") or "daily")
    split_security_pages = report_kind in {"weekly", "monthly"}
    total_pages = 6 if split_security_pages else 4
    spider_top_rows = build_rank_share_rows_v2(view["spider_distribution"], labels, 10)
    status_top_rows = build_rank_share_rows_v2(view["status_distribution"], labels, 10)
    province_table_rows = view["province_rows"][:10]
    client_table_rows = build_client_table_rows_from_distribution(view["client_distribution"], limit=10)
    client_chart_distribution = collapse_distribution_for_donut_v2(
        view["client_distribution"],
        limit=5,
        other_label=labels["other"],
    )
    spider_chart_distribution = collapse_distribution_for_donut_v2(
        view["spider_distribution"],
        limit=5,
        other_label=labels["other"],
    )
    status_chart_distribution = collapse_distribution_for_donut_v2(
        view["status_distribution"],
        limit=5,
        other_label=labels["other"],
    )
    hot_page_headers = [
        labels["url_path"],
        labels["pv"].replace("(", "\n("),
        labels["uv"].replace("(", "\n("),
        labels["requests"],
        labels["traffic_volume"],
    ]
    hot_referer_headers = [
        labels["referer_source"],
        labels["pv"].replace("(", "\n("),
        labels["requests"],
        labels["traffic_volume"],
    ]

    with PdfPages(output_path) as pdf:
        page_one = create_baota_daily_figure()
        page_one.subplots_adjust(left=0.060, right=0.940, top=0.985, bottom=0.040, hspace=0.28, wspace=0.18)
        grid_one = page_one.add_gridspec(5, 12, height_ratios=[0.72, 1.50, 0.90, 3.12, 2.26])
        draw_baota_header_black(page_one.add_subplot(grid_one[0, :]), report, view, labels, generated_at, 1, total_pages)
        draw_ai_review_card_black(page_one.add_subplot(grid_one[1, :]), ai_review)
        draw_baota_kpis_black(page_one.add_subplot(grid_one[2, :]), build_baota_period_kpis(report, config))
        draw_enterprise_chart_card(
            page_one.add_subplot(grid_one[3, :]),
            view["trend_title"],
            lambda inner_ax: draw_baota_three_line_series_black(
                inner_ax,
                "",
                view["x_labels"],
                view["trend"]["pv"],
                view["trend"]["uv"],
                view["trend"]["ip"],
                labels,
                rotation=view["x_rotation"],
            ),
            inset=(0.05, 0.12, 0.91, 0.74),
        )
        bottom_row = grid_one[4, :].subgridspec(1, 3, width_ratios=[45, 10, 45], wspace=0.0)
        draw_enterprise_chart_card(
            page_one.add_subplot(bottom_row[0, 0]),
            labels["performance_load"],
            lambda inner_ax: draw_baota_dual_axis_chart_black(
                inner_ax,
                "",
                view["x_labels"],
                view["performance"]["qps"],
                view["performance"]["response_ms"],
                "QPS",
                "平均响应耗时(ms)" if report_language(config) == "zh" else "Avg Response (ms)",
                "#2563EB",
                "#EF4444",
            ),
            inset=(0.07, 0.16, 0.86, 0.62),
        )
        draw_enterprise_chart_card(
            page_one.add_subplot(bottom_row[0, 2]),
            labels["website_traffic"],
            lambda inner_ax: draw_baota_dual_axis_chart_black(
                inner_ax,
                "",
                view["x_labels"],
                view["network"]["upload_kb"],
                view["network"]["download_kb"],
                "上行 KB" if report_language(config) == "zh" else "Upload KB",
                "下行 KB" if report_language(config) == "zh" else "Download KB",
                "#F59E0B",
                "#10B981",
            ),
            inset=(0.07, 0.16, 0.86, 0.62),
        )
        pdf.savefig(page_one, facecolor="#FFFFFF")
        plt.close(page_one)

        page_two = create_baota_daily_figure()
        page_two.subplots_adjust(left=0.060, right=0.940, top=0.985, bottom=0.042, hspace=0.24, wspace=0.18)
        grid_two = page_two.add_gridspec(3, 12, height_ratios=[0.68, 2.78, 2.78])
        draw_baota_header_black(page_two.add_subplot(grid_two[0, :]), report, view, labels, generated_at, 2, total_pages)
        draw_enterprise_table_card(
            page_two.add_subplot(grid_two[1, :]),
            locale_text(config, "热门页面 URI", "Top URI Insights"),
            [labels["rank"], labels["url_path"], labels["pageviews_pv"], labels["visitors_uv"], labels["request_volume"], labels["traffic_volume"]],
            build_traffic_uri_card_rows(view),
            [0.06, 0.46, 0.12, 0.12, 0.10, 0.14],
            subtitle=locale_text(config, "长 URI 已自动截断，按请求量排序", "Long URIs are safely truncated and sorted by requests"),
            alignments={0: "center", 1: "left", 2: "center", 3: "center", 4: "center", 5: "center"},
            truncate_rules={1: {"limit": 40, "strip_query": True}},
            empty_label=labels["no_data"],
        )
        draw_enterprise_table_card(
            page_two.add_subplot(grid_two[2, :]),
            locale_text(config, "热门访问 IP", "Top IP Insights"),
            [labels["rank"], labels["ip_address"], labels["request_volume"], labels["traffic_volume"], labels["region"]],
            build_traffic_ip_card_rows(view),
            [0.08, 0.26, 0.14, 0.16, 0.36],
            subtitle=locale_text(config, "聚焦高频访问来源，便于快速识别异常流量", "Focus on the highest-frequency visitor IPs"),
            alignments={0: "center", 1: "left", 2: "center", 3: "center", 4: "left"},
            empty_label=labels["no_data"],
        )
        pdf.savefig(page_two, facecolor="#FFFFFF")
        plt.close(page_two)

        if not split_security_pages:
            draw_daily_spider_status_page(
                pdf,
                report,
                config,
                view,
                labels,
                generated_at,
                total_pages,
                spider_chart_distribution,
                status_chart_distribution,
                spider_top_rows,
                status_top_rows,
            )
        else:
            page_three = create_baota_daily_figure()
            page_three.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.20, wspace=0.16)
            grid_three = page_three.add_gridspec(3, 12, height_ratios=[0.68, 2.28, 3.10])
            draw_baota_header_black(page_three.add_subplot(grid_three[0, :]), report, view, labels, generated_at, 3, total_pages)
            spider_cards = grid_three[1, :].subgridspec(1, 2, wspace=0.16)
            draw_enterprise_donut_card(
                page_three.add_subplot(spider_cards[0, 0]),
                locale_text(config, "蜘蛛抓取占比", "Crawler Mix"),
                spider_chart_distribution,
                ENTERPRISE_DONUT_COLORS,
                labels,
                locale_text(config, "抓取次数", "Crawls"),
            )
            draw_enterprise_metrics_card(
                page_three.add_subplot(spider_cards[0, 1]),
                locale_text(config, "蜘蛛抓取摘要", "Spider Shield"),
                build_spider_metrics(report, config, labels),
            )
            draw_enterprise_table_card(
                page_three.add_subplot(grid_three[2, :]),
                dynamic_top_title(labels["crawler_top10"], len(spider_top_rows)),
                [labels["rank"], labels["item"], labels["request_volume"], labels["share"]],
                spider_top_rows or fallback_table_rows(4, config),
                [0.10, 0.48, 0.18, 0.24],
                subtitle=locale_text(config, "按抓取量排序的蜘蛛家族详情", "Spider family details ranked by crawl volume"),
                alignments={0: "center", 1: "left", 2: "center", 3: "center"},
                empty_label=labels["no_data"],
            )
            pdf.savefig(page_three, facecolor="#FFFFFF")
            plt.close(page_three)

            page_four = create_baota_daily_figure()
            page_four.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.20, wspace=0.16)
            grid_four = page_four.add_gridspec(3, 12, height_ratios=[0.68, 2.28, 3.10])
            draw_baota_header_black(page_four.add_subplot(grid_four[0, :]), report, view, labels, generated_at, 4, total_pages)
            status_cards = grid_four[1, :].subgridspec(1, 2, wspace=0.16)
            draw_enterprise_donut_card(
                page_four.add_subplot(status_cards[0, 0]),
                locale_text(config, "状态码占比", "Status Mix"),
                status_chart_distribution,
                ["#4E79A7", "#59A14F", "#F28E2B", "#E15759", "#76B7B2", "#EDC948"],
                labels,
                locale_text(config, "请求总量", "Requests"),
            )
            draw_enterprise_metrics_card(
                page_four.add_subplot(status_cards[0, 1]),
                locale_text(config, "错误状态摘要", "Status Summary"),
                build_status_metrics(report, config),
            )
            draw_enterprise_table_card(
                page_four.add_subplot(grid_four[2, :]),
                dynamic_top_title(labels["status_detail_top10"], len(status_top_rows)),
                [labels["rank"], labels["status_code"], labels["request_volume"], labels["share"]],
                status_top_rows or fallback_table_rows(4, config),
                [0.10, 0.30, 0.28, 0.32],
                subtitle=locale_text(config, "保留 Top 10 状态码详情，便于横向比对", "Top 10 status details for quick comparison"),
                alignments={0: "center", 1: "left", 2: "center", 3: "center"},
                empty_label=labels["no_data"],
            )
            pdf.savefig(page_four, facecolor="#FFFFFF")
            plt.close(page_four)

        if not split_security_pages:
            page_four = create_baota_daily_figure()
            page_four.subplots_adjust(left=0.055, right=0.945, top=0.985, bottom=0.040, hspace=0.22, wspace=0.16)
            grid_four = page_four.add_gridspec(3, 12, height_ratios=[0.68, 2.16, 2.72])
            draw_baota_header_black(page_four.add_subplot(grid_four[0, :]), report, view, labels, generated_at, 4, total_pages)
            top_grid = grid_four[1, :].subgridspec(1, 2, wspace=0.16)
            draw_enterprise_chart_card(
                page_four.add_subplot(top_grid[0, 0]),
                labels["province_access_distribution"],
                lambda inner_ax: draw_compact_province_chart(inner_ax, view, labels),
                subtitle=locale_text(config, "聚焦主要区域与活跃 IP 的集中度", "Focus on the strongest regions and active IP density"),
            )
            draw_enterprise_donut_card(
                page_four.add_subplot(top_grid[0, 1]),
                labels["client_distribution"],
                client_chart_distribution,
                ENTERPRISE_DONUT_COLORS,
                labels,
                locale_text(config, "访问量", "Visits"),
            )
            bottom_grid = grid_four[2, :].subgridspec(1, 2, wspace=0.16)
            draw_enterprise_table_card(
                page_four.add_subplot(bottom_grid[0, 0]),
                dynamic_top_title(labels["province_top10"], len(province_table_rows)),
                [labels["province"], labels["ips"], labels["request_volume"]],
                province_table_rows,
                [0.44, 0.22, 0.34],
                alignments={0: "left", 1: "center", 2: "center"},
                empty_label=labels["no_data"],
            )
            draw_enterprise_table_card(
                page_four.add_subplot(bottom_grid[0, 1]),
                dynamic_top_title(labels["client_top10"], len(client_table_rows)),
                [labels["client"], labels["visit_volume"], labels["share"]],
                client_table_rows,
                [0.44, 0.28, 0.28],
                alignments={0: "left", 1: "center", 2: "center"},
                empty_label=labels["no_data"],
            )
            pdf.savefig(page_four, facecolor="#FFFFFF")
            plt.close(page_four)
        else:
            draw_period_province_page(
                pdf,
                report,
                config,
                view,
                labels,
                generated_at,
                5,
                total_pages,
                province_table_rows,
            )
            draw_period_client_page(
                pdf,
                report,
                config,
                view,
                labels,
                generated_at,
                6,
                total_pages,
                client_chart_distribution,
                client_table_rows,
            )

    return output_path


def render_baota_daily_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    return render_dashboard_pdf(report, config, output_path)


def render_standard_pdf(report: dict[str, Any], config: dict[str, Any], output_path: Path) -> Path:
    return render_dashboard_pdf(report, config, output_path)


def resolve_report_scope(config: dict[str, Any], report_kind: str) -> dict[str, Any]:
    reports = config.get("notifications", {}).get("reports", {})
    if report_kind not in reports:
        return {}
    return reports.get(report_kind, {})


def normalize_filename_part(value: str | None, fallback: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or fallback


def build_report_timestamp(config: dict[str, Any]) -> str:
    return dt.datetime.now(get_timezone(config)).strftime("%Y%m%d%H%M%S")


def compact_summary_text(value: str | None, limit: int = 55, strip_query: bool = False) -> str:
    text = str(value or "").strip()
    if strip_query:
        text = text.split("?", 1)[0]
    text = re.sub(r"\s+", " ", text)
    if len(text) > limit:
        text = text[: max(limit - 3, 1)] + "..."
    return text or "-"


def summarize_status_mix(report: dict[str, Any]) -> str:
    families = {str(item.get("item") or ""): int(item.get("count") or 0) for item in report.get("status_families") or []}
    ordered = ["2xx", "3xx", "4xx", "5xx"]
    return " | ".join(f"{family} {format_number(families.get(family, 0))}" for family in ordered)


def summarize_ranked_items(
    rows: list[dict[str, Any]] | None,
    limit: int = 3,
    strip_query: bool = False,
) -> str:
    items: list[str] = []
    for row in (rows or [])[:limit]:
        label = compact_summary_text(
            str(row.get("item") or row.get("uri") or row.get("source_name") or ""),
            limit=55,
            strip_query=strip_query,
        )
        count = row.get("request_count")
        if count is None:
            count = row.get("count")
        items.append(f"{label} ({format_number(count)})")
    return " | ".join(items) if items else "-"


def build_report_filename(
    config: dict[str, Any],
    report_kind: str,
    report_date: dt.date,
    suffix: str,
    site_name: str | None = None,
) -> str:
    language = report_language(config)
    agent = config.get("agent", {})
    resolved_site = site_name or agent.get("site") or agent.get("site_host") or agent.get("host_id") or "server"
    site_slug = normalize_filename_part(str(resolved_site), "server")
    report_slug = normalize_filename_part(report_kind, "report")
    timestamp = build_report_timestamp(config)
    locale = "zh" if language == "zh" else "en"
    return f"server-mate-{site_slug}-{report_slug}-{timestamp}-{locale}.{suffix}"


def resolve_output_path(
    config: dict[str, Any],
    report_kind: str,
    report_date: dt.date,
    suffix: str,
    site_name: str | None = None,
) -> Path:
    scope = resolve_report_scope(config, report_kind)
    output_dir = Path(scope.get("output_dir") or "./reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / build_report_filename(config, report_kind, report_date, suffix, site_name)


def resolve_requested_sites(config: dict[str, Any], site_name: str | None) -> list[dict[str, Any]]:
    if site_name:
        matched = find_site(config, site_name)
        return [matched] if matched else []
    sites = resolve_sites(config)
    if sites:
        return sites
    fallback_site = {
        "domain": config.get("agent", {}).get("site") or "default",
        "site_host": config.get("agent", {}).get("site_host") or config.get("agent", {}).get("site") or "default",
        "access_log": config.get("logs", {}).get("access_log") or "",
        "error_log": config.get("logs", {}).get("error_log") or "",
        "enabled": True,
    }
    return [fallback_site]


def resolve_site_output_path(
    output_override: Path | None,
    config: dict[str, Any],
    report_kind: str,
    report_date: dt.date,
    suffix: str,
    site_name: str,
    multi_site: bool,
) -> Path:
    if output_override is None:
        return resolve_output_path(config, report_kind, report_date, suffix, site_name)

    if not multi_site and output_override.suffix.lower() == f".{suffix.lower()}":
        output_override.parent.mkdir(parents=True, exist_ok=True)
        return output_override

    output_dir = output_override if output_override.suffix == "" else output_override.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / build_report_filename(config, report_kind, report_date, suffix, site_name)


def export_report_file(config: dict[str, Any], report_kind: str, local_path: Path) -> tuple[Path, str | None]:
    reports = config.get("notifications", {}).get("reports", {})
    scope = resolve_report_scope(config, report_kind)
    export_dir_value = str(scope.get("report_export_dir") or reports.get("report_export_dir") or "").strip()
    public_base_url = str(scope.get("public_base_url") or reports.get("public_base_url") or "").strip()
    if not export_dir_value:
        return local_path, None if not public_base_url else public_base_url.rstrip("/") + "/" + local_path.name

    export_dir = Path(export_dir_value).expanduser().resolve()
    export_dir.mkdir(parents=True, exist_ok=True)
    exported_path = export_dir / local_path.name
    shutil.copy2(local_path, exported_path)
    public_url = public_base_url.rstrip("/") + "/" + exported_path.name if public_base_url else None
    return exported_path, public_url


def send_report_notice(
    config: dict[str, Any],
    report_kind: str,
    report: dict[str, Any],
    local_path: Path,
    exported_path: Path,
    public_url: str | None,
    channels: list[str] | None,
) -> list[dict[str, Any]]:
    scope = resolve_report_scope(config, report_kind)
    selected_channels = channels or scope.get("channels", [])
    title_key = f"{report_kind}_title"
    title = f"{t(config, title_key)} | {report['meta']['site']} | {report['meta']['report_date']}"
    top_page_rows = report.get("top_uri_details") or report.get("top_uris") or []
    top_ip_rows = report.get("top_client_ips") or report.get("abnormal_ips") or []
    ssl_info = report.get("ssl") or {}
    lines = [
        f"# {title}",
        "",
        f"- {t(config, 'window')}: {report['meta']['window_start']} -> {report['meta']['window_end']}",
        f"- {t(config, 'pv')}/{t(config, 'uv')}: {format_number(report['traffic']['pv'])} / {format_number(report['traffic']['uv'])}",
        f"- {t(config, 'requests')}/{t(config, 'slow_requests')}: {format_number(report['traffic']['request_count'])} / {format_number(report['traffic']['slow_request_count'])}",
        f"- {t(config, 'peak_qps')}: {format_number(report['traffic']['qps_peak'], 4)}",
        f"- {format_ssl_markdown_line(config, ssl_info)}",
        f"- {t(config, 'http_status_distribution')}: {summarize_status_mix(report)}",
        f"- {t(config, 'top_pages_short')}: {summarize_ranked_items(top_page_rows, 3, strip_query=True)}",
        f"- {t(config, 'top_ips_short')}: {summarize_ranked_items(top_ip_rows, 3)}",
    ]
    if public_url:
        lines.append(f"- {t(config, 'download_url')}: [{local_path.name}]({public_url})")
    else:
        lines.append(f"- {t(config, 'download_url')}: {t(config, 'local_only')}")
    lines.extend(["", f"> {t(config, 'report_note')}"])
    return send_markdown_message(config, title, "\n".join(lines), selected_channels)


def build_json_payload(report_kind: str, report: dict[str, Any], local_path: Path, exported_path: Path, public_url: str | None, delivery_results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    payload = {
        "report_kind": report_kind,
        "report": report,
        "pdf_path": str(local_path.resolve()) if local_path.suffix.lower() == ".pdf" else None,
        "markdown_path": str(local_path.resolve()) if local_path.suffix.lower() != ".pdf" else None,
        "exported_path": str(exported_path.resolve()) if exported_path.exists() else str(exported_path),
        "public_url": public_url,
    }
    if delivery_results is not None:
        payload["delivery_results"] = delivery_results
    return payload


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    config, _generated = load_config(config_path)
    connection = open_database(Path(config["storage"]["database_file"]))
    try:
        selected_sites = resolve_requested_sites(config, getattr(args, "site", None))
        if not selected_sites:
            raise SystemExit(f"No matching site found for --site={getattr(args, 'site', '')}")

        if (args.command or "daily") == "pdf":
            timezone = get_timezone(config)
            report_kind = getattr(args, "range", "weekly")
            default_offset = -1 if report_kind == "daily" else 0
            report_date = parse_local_date(getattr(args, "end_date", None), timezone, default_offset)
            multi_site = len(selected_sites) > 1
            payloads: list[dict[str, Any]] = []
            for site in selected_sites:
                site_config = build_site_runtime_config(config, site)
                report = prepare_report(connection, site_config, report_kind, report_date)
                output_path = resolve_site_output_path(
                    getattr(args, "output", None),
                    site_config,
                    report_kind,
                    report_date,
                    "pdf",
                    str(report.get("meta", {}).get("site") or ""),
                    multi_site,
                )
                local_path = render_pdf(report, site_config, output_path)
                exported_path, public_url = export_report_file(site_config, report_kind, local_path)
                delivery_results = None
                if getattr(args, "send", False):
                    delivery_results = send_report_notice(
                        site_config,
                        report_kind,
                        report,
                        local_path,
                        exported_path,
                        public_url,
                        getattr(args, "channels", None),
                    )
                payloads.append(
                    build_json_payload(
                        report_kind,
                        report,
                        local_path,
                        exported_path,
                        public_url,
                        delivery_results,
                    )
                )
            if getattr(args, "json", False) or getattr(args, "send", False):
                emit_text(json.dumps(payloads[0] if len(payloads) == 1 else payloads, indent=2, ensure_ascii=False))
            else:
                emit_text("\n".join(item["pdf_path"] for item in payloads if item.get("pdf_path")))
            return 0

        timezone = get_timezone(config)
        report_date = parse_local_date(getattr(args, "date", None), timezone, -1)
        multi_site = len(selected_sites) > 1
        payloads: list[dict[str, Any]] = []
        rendered_markdowns: list[str] = []
        for site in selected_sites:
            site_config = build_site_runtime_config(config, site)
            report = prepare_report(connection, site_config, "daily", report_date)
            markdown = render_daily_markdown(report, site_config)
            output_path = resolve_site_output_path(
                getattr(args, "output", None),
                site_config,
                "daily",
                report_date,
                "md",
                str(report.get("meta", {}).get("site") or ""),
                multi_site,
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown, encoding="utf-8")
            exported_path, public_url = export_report_file(site_config, "daily", output_path)
            delivery_results = None
            if getattr(args, "send", False):
                delivery_results = send_report_notice(
                    site_config,
                    "daily",
                    report,
                    output_path,
                    exported_path,
                    public_url,
                    getattr(args, "channels", None),
                )
            payload = build_json_payload("daily", report, output_path, exported_path, public_url, delivery_results)
            payload["markdown"] = markdown
            payloads.append(payload)
            rendered_markdowns.append(markdown)
        if getattr(args, "json", False) or getattr(args, "send", False):
            emit_text(json.dumps(payloads[0] if len(payloads) == 1 else payloads, indent=2, ensure_ascii=False))
        else:
            emit_text(rendered_markdowns[0] if len(rendered_markdowns) == 1 else "\n".join(item["markdown_path"] for item in payloads if item.get("markdown_path")))
        return 0
    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
