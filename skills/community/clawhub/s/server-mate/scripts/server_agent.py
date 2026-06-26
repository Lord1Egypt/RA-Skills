#!/usr/bin/env python3
"""Config-driven collector and rollup writer for the Server-Mate skill."""

from __future__ import annotations

import argparse
import collections
import copy
import datetime as dt
import hashlib
import ipaddress
import json
import os
import re
import shlex
import socket
import sqlite3
import statistics
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Iterable
import urllib.error
import urllib.request
from urllib.parse import urlparse

from webhook_center import SEVERITY_RANK, send_markdown_message

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None


ACCESS_RE = re.compile(
    r'^(?P<client_ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<body_bytes_sent>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"(?: (?P<tail>.*))?$'
)

NGINX_ERROR_RE = re.compile(
    r"^(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>[^\]]+)\] (?P<message>.*)$"
)

APACHE_ERROR_RE = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\] \[(?P<module>[^\]]+)\]"
    r"(?: \[pid (?P<pid>\d+)(?::tid [^\]]+)?\])?"
    r"(?: \[client (?P<client>[^\]]+)\])? (?P<message>.*)$"
)

SSH_FAILED_PASSWORD_RE = re.compile(
    r"Failed password for (?:invalid user )?(?P<username>\S+) from (?P<client_ip>\S+) port (?P<port>\d+)",
    re.IGNORECASE,
)
AUTH_LOG_PREFIX_RE = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+(?P<program>[\w.@/-]+)(?:\[(?P<pid>\d+)\])?:\s+(?P<message>.*)$"
)

IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")

SEARCH_HOSTS = {
    "google.": "google",
    "bing.com": "bing",
    "baidu.com": "baidu",
    "yandex.": "yandex",
    "duckduckgo.com": "duckduckgo",
    "so.com": "360-search",
    "sogou.com": "sogou",
}

SPIDER_PATTERNS = [
    (re.compile(r"googlebot", re.I), "googlebot"),
    (re.compile(r"baiduspider", re.I), "baiduspider"),
    (re.compile(r"bingbot", re.I), "bingbot"),
    (re.compile(r"yandexbot", re.I), "yandexbot"),
    (re.compile(r"duckduckbot", re.I), "duckduckbot"),
    (re.compile(r"slurp", re.I), "yahoo-slurp"),
    (re.compile(r"petalbot", re.I), "petalbot"),
    (re.compile(r"semrushbot", re.I), "semrushbot"),
    (re.compile(r"ahrefsbot", re.I), "ahrefsbot"),
    (re.compile(r"mj12bot", re.I), "mj12bot"),
    (re.compile(r"curl|python-requests|wget", re.I), "cli-client"),
    (re.compile(r"sqlmap|nikto|nmap|masscan|zgrab|gobuster|dirbuster", re.I), "scanner"),
]

CLIENT_FAMILY_PATTERNS = [
    (re.compile(r"micromessenger", re.I), "WeChat"),
    (re.compile(r"edg|edge", re.I), "Edge"),
    (re.compile(r"opr|opera", re.I), "Opera"),
    (re.compile(r"firefox", re.I), "Firefox"),
    (re.compile(r"chrome|crios", re.I), "Chrome"),
    (re.compile(r"safari", re.I), "Safari"),
    (re.compile(r"msie|trident", re.I), "IE"),
    (re.compile(r"curl|python-requests|wget|httpie", re.I), "Automation"),
]

ERROR_RULES = [
    ("primary_script_unknown", ["primary script unknown"]),
    ("permission_denied", ["permission denied"]),
    ("client_denied", ["client denied"]),
    ("ssl_error", ["ssl"]),
    ("upstream_timeout", ["upstream timed out"]),
    ("upstream_connect_failed", ["connect() failed"]),
    ("bad_gateway", ["bad gateway"]),
    ("php_fatal", ["php fatal"]),
]

HOST_METRIC_SITE = "__host__"
DEFAULT_AUTOMATION_WHITELIST_IPS = [
    "127.0.0.1",
    "::1",
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "100.64.0.0/10",
]
DEFAULT_AUTOMATION_WHITELIST_SPIDERS = ["googlebot", "baiduspider", "bingbot"]

DEFAULT_CONFIG = {
    "agent": {
        "host_id": socket.gethostname(),
        "site": "default",
        "site_host": "",
        "timezone": "Asia/Shanghai",
        "mode": "once",
        "poll_interval_seconds": 60,
        "state_file": "./server_agent_state.json",
        "startup_mode": "tail",
        "bootstrap_tail_lines": 5000,
        "retention_minutes": 180,
        "max_buffer_events": 20000,
        "emit_events": False,
    },
    "system_metrics": {
        "enabled": True,
        "disk_root": "/",
        "collect_network_io": True,
    },
    "logs": {
        "access_log": "./access.log",
        "error_log": "./error.log",
        "auth_log": "",
    },
    "sites": [
        {
            "domain": "default",
            "site_host": "",
            "enabled": True,
            "access_log": "./access.log",
            "error_log": "./error.log",
        }
    ],
    "thresholds": {
        "summary_window_minutes": 10,
        "slow_ms": 2000.0,
        "attack_rpm_threshold": 200,
        "cpu_pct": 85.0,
        "memory_pct": 85.0,
        "hardware_window_minutes": 5,
        "disk_free_ratio": 0.10,
        "server_error_window_minutes": 1,
        "server_error_count": 20,
        "scan_404_count": 20,
        "scan_404_distinct_uris": 10,
        "ssh_bruteforce_window_minutes": 5,
        "ssh_bruteforce_failures": 10,
    },
    "storage": {
        "database_file": "./metrics.db",
        "rollup_minutes": [10, 60],
    },
    "notifications": {
        "webhooks": {
            "dingtalk": {
                "enabled": False,
                "url": "",
                "timeout_seconds": 10,
                "at_all": False,
            },
            "wecom": {
                "enabled": False,
                "url": "",
                "timeout_seconds": 10,
            },
            "feishu": {
                "enabled": False,
                "url": "",
                "timeout_seconds": 10,
            },
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "chat_id": "",
                "timeout_seconds": 10,
                "disable_web_page_preview": True,
            },
        },
        "alerts": {
            "enabled": True,
            "minimum_severity": "warning",
            "cooldown_seconds": 300,
            "channels": ["dingtalk"],
        },
        "reports": {
            "report_language": "zh",
            "report_export_dir": "",
            "public_base_url": "",
            "geoip_city_db": "",
            "geoip_update_config": "./data/GeoIP.conf",
            "ai_analysis": {
                "enabled": True,
                "simulate": False,
                "endpoint": "",
                "base_url": "",
                "model": "gpt-4o-mini",
                "api_key_env": "OPENAI_API_KEY",
                "timeout_seconds": 20,
            },
            "daily": {
                "enabled": False,
                "push_time": "08:30",
                "channels": ["dingtalk"],
                "output_dir": "./reports",
                "report_export_dir": "",
                "public_base_url": "",
                "send_on_startup_if_missed": False,
            },
            "weekly": {
                "enabled": False,
                "push_weekday": 1,
                "push_time": "09:00",
                "channels": ["dingtalk"],
                "output_dir": "./reports",
                "report_export_dir": "",
                "public_base_url": "",
            },
            "monthly": {
                "enabled": False,
                "push_day": 1,
                "push_time": "09:30",
                "channels": ["dingtalk"],
                "output_dir": "./reports",
                "report_export_dir": "",
                "public_base_url": "",
            },
        },
    },
    "automation": {
        "dry_run": True,
        "auto_ban": {
            "enabled": False,
            "channels": ["dingtalk"],
            "whitelist_ips": DEFAULT_AUTOMATION_WHITELIST_IPS,
            "whitelist_spiders": DEFAULT_AUTOMATION_WHITELIST_SPIDERS,
            "ban_ttl_seconds": 86400,
            "timeout_seconds": 15,
            "max_active_bans": 200,
            "command_template": "iptables -I INPUT -s {ip} -j DROP",
            "unban_command_template": "iptables -D INPUT -s {ip} -j DROP",
        },
        "auto_heal": {
            "enabled": False,
            "channels": ["dingtalk"],
            "services": ["php-fpm"],
            "trigger_kinds": ["server_error_burst"],
            "cooldown_seconds": 3600,
            "timeout_seconds": 30,
            "command_template": "systemctl restart {service}",
        },
    },
}

DEFAULT_STATE = {
    "sites": {},
    "system_history": {
        "snapshots": [],
    },
    "host_security": {
        "cursors": {},
        "history": {
            "ssh_auth_events": [],
        },
    },
    "delivery": {
        "alert_cooldowns": {},
        "reports": {
            "daily": {},
            "weekly": {},
            "monthly": {},
        },
    },
}

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS agent_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_started_at TEXT NOT NULL,
    run_finished_at TEXT NOT NULL,
    host_id TEXT NOT NULL,
    site TEXT NOT NULL,
    mode TEXT NOT NULL,
    access_lines_read INTEGER NOT NULL DEFAULT 0,
    access_lines_dropped INTEGER NOT NULL DEFAULT 0,
    error_lines_read INTEGER NOT NULL DEFAULT 0,
    error_lines_dropped INTEGER NOT NULL DEFAULT 0,
    rollups_upserted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metric_rollups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id TEXT NOT NULL,
    site TEXT NOT NULL,
    bucket_start TEXT NOT NULL,
    bucket_end TEXT NOT NULL,
    bucket_minutes INTEGER NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 0,
    pv INTEGER NOT NULL DEFAULT 0,
    uv INTEGER NOT NULL DEFAULT 0,
    unique_ips INTEGER NOT NULL DEFAULT 0,
    active_users INTEGER NOT NULL DEFAULT 0,
    qps REAL NOT NULL DEFAULT 0,
    avg_response_ms REAL,
    slow_request_count INTEGER NOT NULL DEFAULT 0,
    bandwidth_out_bytes INTEGER NOT NULL DEFAULT 0,
    bandwidth_in_bytes INTEGER,
    total_errors INTEGER NOT NULL DEFAULT 0,
    avg_cpu_pct REAL,
    max_cpu_pct REAL,
    avg_memory_pct REAL,
    max_memory_pct REAL,
    min_disk_free_bytes INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(host_id, site, bucket_start, bucket_minutes)
);

CREATE TABLE IF NOT EXISTS automation_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id TEXT NOT NULL,
    site TEXT NOT NULL,
    action_type TEXT NOT NULL,
    target TEXT,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    dry_run INTEGER NOT NULL DEFAULT 0,
    command_text TEXT,
    stdout TEXT,
    stderr TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS banned_ips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id TEXT NOT NULL,
    site TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    reason TEXT NOT NULL,
    command_text TEXT,
    dry_run INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    lifted_at TEXT,
    lift_status TEXT,
    unban_command_text TEXT
);
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Server-Mate collector in once or daemon mode."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to config.yaml. A default file is created automatically if missing.",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuously using poll_interval_seconds from the config.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single collection cycle and exit.",
    )
    parser.add_argument(
        "--print-config",
        action="store_true",
        help="Print the normalized config and exit.",
    )
    parser.add_argument(
        "--generate-service",
        action="store_true",
        help="Print a systemd service unit for the current workspace and exit.",
    )
    return parser.parse_args()


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def safe_json_text(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def write_default_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(safe_json_text(DEFAULT_CONFIG) + "\n", encoding="utf-8")


def resolve_config_path(base_dir: Path, value: Any) -> Path:
    path = Path(str(value or "")).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def normalize_string_list(value: Any, default: list[str] | None = None) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        items = default or []

    normalized = []
    for item in items:
        name = str(item or "").strip().lower()
        if name and name not in normalized:
            normalized.append(name)
    return normalized


def normalize_clock_time(value: Any, default: str) -> str:
    candidate = str(value or default).strip()
    try:
        hour_text, minute_text = candidate.split(":", 1)
        hour = int(hour_text)
        minute = int(minute_text)
    except (ValueError, AttributeError):
        return default
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return default
    return f"{hour:02d}:{minute:02d}"


def normalize_ip_whitelist(value: Any) -> list[str]:
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        items = list(DEFAULT_AUTOMATION_WHITELIST_IPS)
    normalized: list[str] = []
    for item in items:
        text = str(item or "").strip()
        if text and text not in normalized:
            normalized.append(text)
    for fallback in DEFAULT_AUTOMATION_WHITELIST_IPS:
        if fallback not in normalized:
            normalized.append(fallback)
    return normalized


def default_site_state() -> dict[str, Any]:
    return {
        "cursors": {},
        "history": {
            "access_events": [],
            "error_events": [],
        },
    }


def ensure_host_security_state(state: dict[str, Any]) -> dict[str, Any]:
    host_state = state.setdefault("host_security", {})
    host_state.setdefault("cursors", {})
    history = host_state.setdefault("history", {})
    history.setdefault("ssh_auth_events", [])
    return host_state


def detect_default_auth_log_path() -> str:
    os_release = Path("/etc/os-release")
    distro_hints = ""
    if os_release.exists():
        try:
            distro_hints = os_release.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            distro_hints = ""

    if "ubuntu" in distro_hints or "debian" in distro_hints:
        return "/var/log/auth.log"
    if any(name in distro_hints for name in ("centos", "rhel", "rocky", "alma", "fedora")):
        return "/var/log/secure"

    for candidate in ("/var/log/auth.log", "/var/log/secure"):
        if Path(candidate).exists():
            return candidate
    return "/var/log/auth.log"


def normalize_site_entry(
    raw_site: Any,
    index: int,
    base_dir: Path,
    fallback_access_log: Any = None,
    fallback_error_log: Any = None,
) -> dict[str, Any]:
    site_data = raw_site if isinstance(raw_site, dict) else {}
    domain = str(
        site_data.get("domain")
        or site_data.get("site")
        or site_data.get("name")
        or f"site-{index}"
    ).strip()
    site_host = str(site_data.get("site_host") or site_data.get("host") or domain).strip()
    access_log_value = site_data.get("access_log")
    error_log_value = site_data.get("error_log")
    if not access_log_value and fallback_access_log is not None:
        access_log_value = fallback_access_log
    if not error_log_value and fallback_error_log is not None:
        error_log_value = fallback_error_log
    return {
        "domain": domain or f"site-{index}",
        "site_host": site_host or domain or f"site-{index}",
        "enabled": bool(site_data.get("enabled", True)),
        "access_log": str(resolve_config_path(base_dir, access_log_value or f"./site-{index}.access.log")),
        "error_log": str(resolve_config_path(base_dir, error_log_value or f"./site-{index}.error.log")),
    }


def normalize_sites_config(config: dict[str, Any], base_dir: Path) -> list[dict[str, Any]]:
    agent = config.setdefault("agent", {})
    logs = config.setdefault("logs", {})
    raw_sites = config.get("sites")
    site_entries = raw_sites if isinstance(raw_sites, list) and raw_sites else None

    if not site_entries:
        site_entries = [
            {
                "domain": agent.get("site") or "default",
                "site_host": agent.get("site_host") or agent.get("site") or "default",
                "enabled": True,
                "access_log": logs.get("access_log"),
                "error_log": logs.get("error_log"),
            }
        ]

    normalized: list[dict[str, Any]] = []
    seen_domains: set[str] = set()
    for index, raw_site in enumerate(site_entries, start=1):
        site = normalize_site_entry(
            raw_site,
            index,
            base_dir,
            logs.get("access_log") if index == 1 else None,
            logs.get("error_log") if index == 1 else None,
        )
        domain_key = site["domain"].lower()
        if domain_key in seen_domains:
            continue
        seen_domains.add(domain_key)
        normalized.append(site)

    if not normalized:
        normalized.append(
            normalize_site_entry(
                {"domain": "default", "enabled": True},
                1,
                base_dir,
                logs.get("access_log"),
                logs.get("error_log"),
            )
        )

    first_site = normalized[0]
    agent["site"] = first_site["domain"]
    agent["site_host"] = first_site["site_host"]
    logs["access_log"] = first_site["access_log"]
    logs["error_log"] = first_site["error_log"]
    config["sites"] = normalized
    return normalized


def resolve_sites(config: dict[str, Any], enabled_only: bool = True) -> list[dict[str, Any]]:
    sites = config.get("sites")
    if not isinstance(sites, list):
        return []
    if not enabled_only:
        return [dict(site) for site in sites if isinstance(site, dict)]
    return [dict(site) for site in sites if isinstance(site, dict) and bool(site.get("enabled", True))]


def find_site(config: dict[str, Any], site_name: str | None) -> dict[str, Any] | None:
    if not site_name:
        return None
    needle = str(site_name).strip().lower()
    for site in resolve_sites(config, enabled_only=False):
        aliases = {
            str(site.get("domain") or "").strip().lower(),
            str(site.get("site_host") or "").strip().lower(),
        }
        if needle in aliases:
            return site
    return None


def build_site_runtime_config(config: dict[str, Any], site: dict[str, Any]) -> dict[str, Any]:
    runtime_config = copy.deepcopy(config)
    runtime_config.setdefault("agent", {})
    runtime_config.setdefault("logs", {})
    runtime_config["agent"]["site"] = str(site.get("domain") or runtime_config["agent"].get("site") or "default")
    runtime_config["agent"]["site_host"] = str(
        site.get("site_host") or runtime_config["agent"]["site"]
    )
    runtime_config["logs"]["access_log"] = str(site.get("access_log") or runtime_config["logs"].get("access_log") or "")
    runtime_config["logs"]["error_log"] = str(site.get("error_log") or runtime_config["logs"].get("error_log") or "")
    return runtime_config


def ensure_site_state(state: dict[str, Any], domain: str) -> dict[str, Any]:
    sites_state = state.setdefault("sites", {})
    site_state = sites_state.get(domain)
    if not isinstance(site_state, dict):
        site_state = default_site_state()
        sites_state[domain] = site_state
    else:
        site_state.setdefault("cursors", {})
        history = site_state.setdefault("history", {})
        history.setdefault("access_events", [])
        history.setdefault("error_events", [])
    return site_state


def normalize_config(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    agent = config.setdefault("agent", {})
    logs = config.setdefault("logs", {})
    system_metrics = config.setdefault("system_metrics", {})
    thresholds = config.setdefault("thresholds", {})
    storage = config.setdefault("storage", {})
    notifications = config.setdefault("notifications", {})
    automation = config.setdefault("automation", {})
    webhooks = notifications.setdefault("webhooks", {})
    alerts_config = notifications.setdefault("alerts", {})
    reports_config = notifications.setdefault("reports", {})

    base_dir = config_path.parent.resolve()

    agent["host_id"] = str(agent.get("host_id") or socket.gethostname())
    agent["timezone"] = str(agent.get("timezone") or "UTC")
    agent["mode"] = str(agent.get("mode") or "once").lower()
    agent["poll_interval_seconds"] = max(int(agent.get("poll_interval_seconds", 60)), 1)
    agent["startup_mode"] = str(agent.get("startup_mode") or "tail").lower()
    agent["bootstrap_tail_lines"] = max(int(agent.get("bootstrap_tail_lines", 5000)), 0)
    agent["retention_minutes"] = max(int(agent.get("retention_minutes", 180)), 10)
    agent["max_buffer_events"] = max(int(agent.get("max_buffer_events", 20000)), 100)
    agent["emit_events"] = bool(agent.get("emit_events", False))
    agent["state_file"] = str(resolve_config_path(base_dir, agent.get("state_file")))

    system_metrics["enabled"] = bool(system_metrics.get("enabled", True))
    system_metrics["disk_root"] = str(
        system_metrics.get("disk_root") or agent.get("disk_root") or "/"
    )
    system_metrics["collect_network_io"] = bool(
        system_metrics.get("collect_network_io", True)
    )

    raw_auth_log = str(logs.get("auth_log") or "").strip()
    if raw_auth_log:
        logs["auth_log"] = str(resolve_config_path(base_dir, raw_auth_log))
    else:
        logs["auth_log"] = detect_default_auth_log_path()

    normalize_sites_config(config, base_dir)

    thresholds["summary_window_minutes"] = max(
        int(thresholds.get("summary_window_minutes", 10)),
        1,
    )
    thresholds["slow_ms"] = float(thresholds.get("slow_ms", 2000.0))
    thresholds["attack_rpm_threshold"] = max(
        int(thresholds.get("attack_rpm_threshold", 200)),
        1,
    )
    thresholds["cpu_pct"] = float(thresholds.get("cpu_pct", 85.0))
    thresholds["memory_pct"] = float(thresholds.get("memory_pct", 85.0))
    thresholds["hardware_window_minutes"] = max(
        int(thresholds.get("hardware_window_minutes", 5)),
        1,
    )
    thresholds["disk_free_ratio"] = float(thresholds.get("disk_free_ratio", 0.10))
    thresholds["server_error_window_minutes"] = max(
        int(thresholds.get("server_error_window_minutes", 1)),
        1,
    )
    thresholds["server_error_count"] = max(
        int(thresholds.get("server_error_count", 20)),
        1,
    )
    thresholds["scan_404_count"] = max(int(thresholds.get("scan_404_count", 20)), 1)
    thresholds["scan_404_distinct_uris"] = max(
        int(thresholds.get("scan_404_distinct_uris", 10)),
        1,
    )
    thresholds["ssh_bruteforce_window_minutes"] = max(
        int(thresholds.get("ssh_bruteforce_window_minutes", 5)),
        1,
    )
    thresholds["ssh_bruteforce_failures"] = max(
        int(thresholds.get("ssh_bruteforce_failures", 10)),
        1,
    )

    rollup_minutes = storage.get("rollup_minutes", [10, 60])
    if not isinstance(rollup_minutes, list) or not rollup_minutes:
        rollup_minutes = [10, 60]
    storage["rollup_minutes"] = sorted(
        {max(int(value), 1) for value in rollup_minutes}
    )
    storage["database_file"] = str(
        resolve_config_path(base_dir, storage.get("database_file"))
    )

    for channel_name in ("dingtalk", "wecom", "feishu", "telegram"):
        channel = webhooks.setdefault(channel_name, {})
        channel["enabled"] = bool(channel.get("enabled", False))
        channel["timeout_seconds"] = max(
            int(channel.get("timeout_seconds", 10)),
            1,
        )
        if channel_name == "telegram":
            channel["bot_token"] = str(channel.get("bot_token") or "").strip()
            channel["chat_id"] = str(channel.get("chat_id") or "").strip()
            channel["disable_web_page_preview"] = bool(
                channel.get("disable_web_page_preview", True)
            )
            channel["url"] = ""
        else:
            channel["url"] = str(channel.get("url") or "").strip()
        if channel_name == "dingtalk":
            channel["at_all"] = bool(channel.get("at_all", False))

    alerts_config["enabled"] = bool(alerts_config.get("enabled", True))
    alerts_config["minimum_severity"] = str(
        alerts_config.get("minimum_severity", "warning")
    ).lower()
    if alerts_config["minimum_severity"] not in SEVERITY_RANK:
        alerts_config["minimum_severity"] = "warning"
    alerts_config["cooldown_seconds"] = max(
        int(alerts_config.get("cooldown_seconds", 300)),
        0,
    )
    alerts_config["channels"] = normalize_string_list(
        alerts_config.get("channels"),
        ["dingtalk"],
    )

    reports_config["report_language"] = str(
        reports_config.get("report_language", "zh") or "zh"
    ).strip().lower()
    if reports_config["report_language"] not in {"zh", "en"}:
        reports_config["report_language"] = "zh"
    reports_config["report_export_dir"] = str(
        reports_config.get("report_export_dir") or ""
    ).strip()
    if reports_config["report_export_dir"]:
        reports_config["report_export_dir"] = str(
            resolve_config_path(base_dir, reports_config["report_export_dir"])
        )
    reports_config["public_base_url"] = str(
        reports_config.get("public_base_url") or ""
    ).strip()
    reports_config["geoip_city_db"] = str(
        reports_config.get("geoip_city_db") or ""
    ).strip()
    if reports_config["geoip_city_db"]:
        reports_config["geoip_city_db"] = str(
            resolve_config_path(base_dir, reports_config["geoip_city_db"])
        )
    reports_config["geoip_update_config"] = str(
        reports_config.get("geoip_update_config") or ""
    ).strip()
    if reports_config["geoip_update_config"]:
        reports_config["geoip_update_config"] = str(
            resolve_config_path(base_dir, reports_config["geoip_update_config"])
        )

    ai_analysis = reports_config.setdefault("ai_analysis", {})
    ai_analysis["enabled"] = bool(ai_analysis.get("enabled", True))
    ai_analysis["simulate"] = bool(ai_analysis.get("simulate", False))
    ai_analysis["endpoint"] = str(
        ai_analysis.get("endpoint") or ai_analysis.get("base_url") or ""
    ).strip()
    ai_analysis["base_url"] = ai_analysis["endpoint"]
    ai_analysis["model"] = str(ai_analysis.get("model") or "gpt-4o-mini").strip()
    ai_analysis["api_key_env"] = str(
        ai_analysis.get("api_key_env") or "OPENAI_API_KEY"
    ).strip()
    ai_analysis["timeout_seconds"] = max(
        int(ai_analysis.get("timeout_seconds", 20)),
        3,
    )

    daily_report = reports_config.setdefault("daily", {})
    daily_report["enabled"] = bool(daily_report.get("enabled", False))
    daily_report["push_time"] = normalize_clock_time(
        daily_report.get("push_time"),
        "08:30",
    )
    daily_report["channels"] = normalize_string_list(
        daily_report.get("channels"),
        ["dingtalk"],
    )
    daily_report["output_dir"] = str(
        resolve_config_path(base_dir, daily_report.get("output_dir") or "./reports")
    )
    daily_report["report_export_dir"] = str(
        daily_report.get("report_export_dir") or reports_config["report_export_dir"]
    ).strip()
    if daily_report["report_export_dir"]:
        daily_report["report_export_dir"] = str(
            resolve_config_path(base_dir, daily_report["report_export_dir"])
        )
    daily_report["public_base_url"] = str(daily_report.get("public_base_url") or "").strip()
    if not daily_report["public_base_url"]:
        daily_report["public_base_url"] = reports_config["public_base_url"]
    daily_report["send_on_startup_if_missed"] = bool(
        daily_report.get("send_on_startup_if_missed", False)
    )

    weekly_report = reports_config.setdefault("weekly", {})
    weekly_report["enabled"] = bool(weekly_report.get("enabled", False))
    weekly_report["push_weekday"] = min(
        max(int(weekly_report.get("push_weekday", 1)), 1),
        7,
    )
    weekly_report["push_time"] = normalize_clock_time(
        weekly_report.get("push_time"),
        "09:00",
    )
    weekly_report["channels"] = normalize_string_list(
        weekly_report.get("channels"),
        ["dingtalk"],
    )
    weekly_report["output_dir"] = str(
        resolve_config_path(base_dir, weekly_report.get("output_dir") or "./reports")
    )
    weekly_report["report_export_dir"] = str(
        weekly_report.get("report_export_dir") or reports_config["report_export_dir"]
    ).strip()
    if weekly_report["report_export_dir"]:
        weekly_report["report_export_dir"] = str(
            resolve_config_path(base_dir, weekly_report["report_export_dir"])
        )
    weekly_report["public_base_url"] = str(weekly_report.get("public_base_url") or "").strip()
    if not weekly_report["public_base_url"]:
        weekly_report["public_base_url"] = reports_config["public_base_url"]

    monthly_report = reports_config.setdefault("monthly", {})
    monthly_report["enabled"] = bool(monthly_report.get("enabled", False))
    monthly_report["push_day"] = min(
        max(int(monthly_report.get("push_day", 1)), 1),
        28,
    )
    monthly_report["push_time"] = normalize_clock_time(
        monthly_report.get("push_time"),
        "09:30",
    )
    monthly_report["channels"] = normalize_string_list(
        monthly_report.get("channels"),
        ["dingtalk"],
    )
    monthly_report["output_dir"] = str(
        resolve_config_path(base_dir, monthly_report.get("output_dir") or "./reports")
    )
    monthly_report["report_export_dir"] = str(
        monthly_report.get("report_export_dir") or reports_config["report_export_dir"]
    ).strip()
    if monthly_report["report_export_dir"]:
        monthly_report["report_export_dir"] = str(
            resolve_config_path(base_dir, monthly_report["report_export_dir"])
        )
    monthly_report["public_base_url"] = str(monthly_report.get("public_base_url") or "").strip()
    if not monthly_report["public_base_url"]:
        monthly_report["public_base_url"] = reports_config["public_base_url"]

    automation["dry_run"] = bool(automation.get("dry_run", True))

    auto_ban = automation.setdefault("auto_ban", {})
    auto_ban["enabled"] = bool(auto_ban.get("enabled", False))
    auto_ban["channels"] = normalize_string_list(
        auto_ban.get("channels"),
        alerts_config.get("channels") or ["dingtalk"],
    )
    auto_ban["whitelist_ips"] = normalize_ip_whitelist(auto_ban.get("whitelist_ips"))
    auto_ban["whitelist_spiders"] = normalize_string_list(
        auto_ban.get("whitelist_spiders"),
        list(DEFAULT_AUTOMATION_WHITELIST_SPIDERS),
    )
    auto_ban["ban_ttl_seconds"] = max(int(auto_ban.get("ban_ttl_seconds", 86400)), 60)
    auto_ban["timeout_seconds"] = max(int(auto_ban.get("timeout_seconds", 15)), 1)
    auto_ban["max_active_bans"] = max(int(auto_ban.get("max_active_bans", 200)), 1)
    auto_ban["command_template"] = str(
        auto_ban.get("command_template") or "iptables -I INPUT -s {ip} -j DROP"
    ).strip()
    auto_ban["unban_command_template"] = str(
        auto_ban.get("unban_command_template") or "iptables -D INPUT -s {ip} -j DROP"
    ).strip()

    auto_heal = automation.setdefault("auto_heal", {})
    auto_heal["enabled"] = bool(auto_heal.get("enabled", False))
    auto_heal["channels"] = normalize_string_list(
        auto_heal.get("channels"),
        alerts_config.get("channels") or ["dingtalk"],
    )
    auto_heal["services"] = normalize_string_list(
        auto_heal.get("services"),
        ["php-fpm"],
    )
    auto_heal["trigger_kinds"] = normalize_string_list(
        auto_heal.get("trigger_kinds"),
        ["server_error_burst"],
    )
    auto_heal["cooldown_seconds"] = max(int(auto_heal.get("cooldown_seconds", 3600)), 60)
    auto_heal["timeout_seconds"] = max(int(auto_heal.get("timeout_seconds", 30)), 1)
    auto_heal["command_template"] = str(
        auto_heal.get("command_template") or "systemctl restart {service}"
    ).strip()

    minimum_retention = max(
        storage["rollup_minutes"]
        + [
            thresholds["summary_window_minutes"],
            thresholds["hardware_window_minutes"],
            thresholds["server_error_window_minutes"],
        ]
    ) + 10
    agent["retention_minutes"] = max(agent["retention_minutes"], minimum_retention)
    return config


def load_config(path: Path) -> tuple[dict[str, Any], bool]:
    generated = False
    if not path.exists():
        write_default_config(path)
        generated = True

    raw_text = path.read_text(encoding="utf-8-sig")
    if yaml is not None:
        loaded = yaml.safe_load(raw_text) or {}
    else:
        loaded = json.loads(raw_text)
    if not isinstance(loaded, dict):
        raise ValueError("Config file must contain a top-level mapping.")
    config = normalize_config(deep_merge(DEFAULT_CONFIG, loaded), path)
    return config, generated


def migrate_state_shape(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    migrated = deep_merge(DEFAULT_STATE, state if isinstance(state, dict) else {})
    sites = resolve_sites(config, enabled_only=False)
    primary_site = sites[0]["domain"] if sites else str(config.get("agent", {}).get("site") or "default")

    legacy_cursors = migrated.pop("cursors", None)
    legacy_history = migrated.pop("history", None)
    if (legacy_cursors or legacy_history) and primary_site:
        site_state = ensure_site_state(migrated, primary_site)
        if isinstance(legacy_cursors, dict):
            site_state["cursors"] = deep_merge(site_state.get("cursors", {}), legacy_cursors)
        if isinstance(legacy_history, dict):
            if legacy_history.get("access_events"):
                site_state["history"]["access_events"] = list(legacy_history.get("access_events") or []) + list(site_state["history"].get("access_events") or [])
            if legacy_history.get("error_events"):
                site_state["history"]["error_events"] = list(legacy_history.get("error_events") or []) + list(site_state["history"].get("error_events") or [])
            if legacy_history.get("system_snapshots"):
                migrated.setdefault("system_history", {}).setdefault("snapshots", [])
                migrated["system_history"]["snapshots"] = list(legacy_history.get("system_snapshots") or []) + list(migrated["system_history"].get("snapshots") or [])

    migrated.setdefault("sites", {})
    for site in sites:
        ensure_site_state(migrated, str(site.get("domain") or "default"))

    migrated.setdefault("system_history", {})
    migrated["system_history"].setdefault("snapshots", [])
    ensure_host_security_state(migrated)
    return migrated


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return copy.deepcopy(DEFAULT_STATE)
    try:
        with path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return copy.deepcopy(DEFAULT_STATE)
    if not isinstance(loaded, dict):
        return copy.deepcopy(DEFAULT_STATE)
    return deep_merge(DEFAULT_STATE, loaded)


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
    temp_path.replace(path)


def init_database(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA_SQL)
    connection.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_metric_rollups_bucket
        ON metric_rollups (host_id, site, bucket_minutes, bucket_start);

        CREATE INDEX IF NOT EXISTS idx_automation_actions_lookup
        ON automation_actions (host_id, site, action_type, created_at);

        CREATE INDEX IF NOT EXISTS idx_banned_ips_active
        ON banned_ips (host_id, site, ip_address, expires_at, lifted_at);

        CREATE TABLE IF NOT EXISTS status_code_rollups (
            rollup_id INTEGER NOT NULL,
            status_code TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, status_code),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS spider_rollups (
            rollup_id INTEGER NOT NULL,
            spider_family TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            bytes_out INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, spider_family),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS error_category_rollups (
            rollup_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            error_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, category),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS error_fingerprint_rollups (
            rollup_id INTEGER NOT NULL,
            fingerprint TEXT NOT NULL,
            error_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, fingerprint),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS uri_rollups (
            rollup_id INTEGER NOT NULL,
            uri TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, uri),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS uri_detail_rollups (
            rollup_id INTEGER NOT NULL,
            uri TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            uv_count INTEGER NOT NULL DEFAULT 0,
            bytes_out INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, uri),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS source_rollups (
            rollup_id INTEGER NOT NULL,
            source_name TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            uv_count INTEGER NOT NULL DEFAULT 0,
            bytes_out INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, source_name),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS visitor_rollups (
            rollup_id INTEGER NOT NULL,
            visitor_hash TEXT NOT NULL,
            PRIMARY KEY (rollup_id, visitor_hash),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS client_ip_rollups (
            rollup_id INTEGER NOT NULL,
            client_ip TEXT NOT NULL,
            PRIMARY KEY (rollup_id, client_ip),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS client_ip_request_rollups (
            rollup_id INTEGER NOT NULL,
            client_ip TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            bytes_out INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, client_ip),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS client_family_rollups (
            rollup_id INTEGER NOT NULL,
            client_family TEXT NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, client_family),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS slow_request_rollups (
            rollup_id INTEGER NOT NULL,
            uri TEXT NOT NULL,
            slow_request_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, uri),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS suspicious_ip_rollups (
            rollup_id INTEGER NOT NULL,
            client_ip TEXT NOT NULL,
            max_requests_per_minute INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (rollup_id, client_ip),
            FOREIGN KEY (rollup_id) REFERENCES metric_rollups(id) ON DELETE CASCADE
        );
        """
    )
    return connection


def get_timezone(config: dict[str, Any]) -> dt.tzinfo:
    timezone_name = config["agent"].get("timezone", "UTC")
    if ZoneInfo is None:
        return dt.timezone.utc
    try:
        return ZoneInfo(timezone_name)
    except Exception:
        return dt.timezone.utc


def parse_iso_ts(value: Any) -> dt.datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed


def event_timestamp(event: dict[str, Any]) -> dt.datetime | None:
    timestamp = event.get("timestamp")
    if isinstance(timestamp, dt.datetime):
        return timestamp
    return parse_iso_ts(event.get("ts"))


def read_tail_lines(path: Path | None, max_lines: int) -> list[str]:
    if not path or not path.exists() or max_lines <= 0:
        return []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return list(collections.deque(handle, maxlen=max_lines))
    except OSError:
        return []


def build_log_cursor(
    path: Path,
    offset: int,
    inode: int | None,
    cursor: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    next_cursor = dict(cursor or {})
    next_cursor.update(
        {
            "offset": max(int(offset), 0),
            "inode": inode,
            "path": str(path),
        }
    )
    for key, value in extra.items():
        next_cursor[key] = value
    return next_cursor


def read_incremental_lines(
    path: Path,
    cursor: dict[str, Any] | None,
    startup_mode: str,
    bootstrap_tail_lines: int,
) -> tuple[list[str], dict[str, Any]]:
    previous_cursor = dict(cursor or {})
    try:
        stat = path.stat()
    except FileNotFoundError:
        missing_since = previous_cursor.get("missing_since") or utcnow().isoformat()
        return [], build_log_cursor(
            path,
            int(previous_cursor.get("offset", 0)),
            previous_cursor.get("inode"),
            previous_cursor,
            missing_since=missing_since,
            status="missing",
        )
    except OSError:
        return [], build_log_cursor(
            path,
            int(previous_cursor.get("offset", 0)),
            previous_cursor.get("inode"),
            previous_cursor,
            status="stat_error",
        )

    inode = getattr(stat, "st_ino", None)
    previous_offset = max(int(previous_cursor.get("offset", 0)), 0)
    previous_inode = previous_cursor.get("inode")

    try:
        if not previous_cursor or previous_cursor.get("path") != str(path):
            if startup_mode == "full":
                with path.open("r", encoding="utf-8", errors="replace") as handle:
                    lines = handle.readlines()
                    offset = handle.tell()
            else:
                lines = read_tail_lines(path, bootstrap_tail_lines)
                with path.open("r", encoding="utf-8", errors="replace") as handle:
                    handle.seek(0, 2)
                    offset = handle.tell()
            return lines, build_log_cursor(path, offset, inode, previous_cursor, status="ready", missing_since=None)

        rotation_detected = previous_inode != inode or stat.st_size < previous_offset
        if rotation_detected:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                handle.seek(0)
                lines = handle.readlines()
                offset = handle.tell()
            return lines, build_log_cursor(
                path,
                offset,
                inode,
                previous_cursor,
                status="rotated",
                rotated_at=utcnow().isoformat(),
                missing_since=None,
            )

        with path.open("r", encoding="utf-8", errors="replace") as handle:
            handle.seek(previous_offset)
            lines = handle.readlines()
            offset = handle.tell()
        return lines, build_log_cursor(path, offset, inode, previous_cursor, status="ready", missing_since=None)
    except FileNotFoundError:
        missing_since = previous_cursor.get("missing_since") or utcnow().isoformat()
        return [], build_log_cursor(
            path,
            previous_offset,
            previous_inode,
            previous_cursor,
            missing_since=missing_since,
            status="missing",
        )
    except OSError:
        return [], build_log_cursor(
            path,
            previous_offset,
            previous_inode,
            previous_cursor,
            status="read_error",
        )


def parse_access_timestamp(raw: str, default_timezone: dt.tzinfo) -> dt.datetime | None:
    formats = ["%d/%b/%Y:%H:%M:%S %z", "%d/%b/%Y:%H:%M:%S"]
    for fmt in formats:
        try:
            parsed = dt.datetime.strptime(raw, fmt)
        except ValueError:
            continue
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=default_timezone).astimezone(dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    return None


def parse_error_timestamp(raw: str, default_timezone: dt.tzinfo) -> dt.datetime | None:
    formats = [
        "%Y/%m/%d %H:%M:%S",
        "%a %b %d %H:%M:%S.%f %Y",
        "%a %b %d %H:%M:%S %Y",
    ]
    for fmt in formats:
        try:
            parsed = dt.datetime.strptime(raw, fmt)
        except ValueError:
            continue
        return parsed.replace(tzinfo=default_timezone).astimezone(dt.timezone.utc)
    return None


def parse_auth_timestamp(
    raw: str,
    default_timezone: dt.tzinfo,
    reference_time: dt.datetime | None = None,
) -> dt.datetime | None:
    try:
        parsed = dt.datetime.strptime(raw, "%b %d %H:%M:%S")
    except ValueError:
        return None
    now_local = (reference_time or utcnow()).astimezone(default_timezone)
    candidate = parsed.replace(year=now_local.year, tzinfo=default_timezone)
    if candidate - now_local > dt.timedelta(days=1):
        candidate = candidate.replace(year=now_local.year - 1)
    return candidate.astimezone(dt.timezone.utc)


def parse_request(request: str) -> tuple[str | None, str | None, str | None]:
    if not request or request == "-":
        return None, None, None
    parts = request.split()
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], parts[1], None
    return None, request, None


def looks_number(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def parse_tail_tokens(tail: str | None) -> dict[str, Any]:
    data: dict[str, Any] = {"request_time_s": None, "request_length": None}
    if not tail:
        return data
    try:
        tokens = shlex.split(tail)
    except ValueError:
        tokens = tail.split()
    numeric_tokens = [token for token in tokens if looks_number(token)]
    float_tokens = [token for token in numeric_tokens if "." in token]
    int_tokens = [token for token in numeric_tokens if token.isdigit()]
    if float_tokens:
        data["request_time_s"] = float(float_tokens[0])
    elif len(int_tokens) == 1:
        candidate = int(int_tokens[0])
        if candidate <= 60:
            data["request_time_s"] = float(candidate)
    if int_tokens:
        candidate = max(int(token) for token in int_tokens)
        if candidate > 60:
            data["request_length"] = candidate
    return data


def to_int(value: str) -> int | None:
    if not value or value == "-":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def classify_source(referer: str, site_host: str) -> tuple[str, str]:
    if not referer or referer == "-":
        return "direct", "direct"
    parsed = urlparse(referer)
    host = (parsed.netloc or "").lower()
    if not host:
        return "external", "unknown"
    if site_host and host.endswith(site_host.lower()):
        return "internal", host
    for needle, name in SEARCH_HOSTS.items():
        if needle in host:
            return "search", name
    return "external", host


def classify_spider(user_agent: str) -> str | None:
    for pattern, family in SPIDER_PATTERNS:
        if pattern.search(user_agent or ""):
            return family
    return None


def classify_client_family(user_agent: str, spider_family: str | None = None) -> str:
    if spider_family in {"scanner", "cli-client"}:
        return "Automation"
    if spider_family:
        return "Crawler"
    for pattern, family in CLIENT_FAMILY_PATTERNS:
        if pattern.search(user_agent or ""):
            return family
    return "Other"


def classify_error(message: str) -> str:
    lowered = message.lower()
    for category, needles in ERROR_RULES:
        if all(needle in lowered for needle in needles):
            return category
    return "other"


def normalize_error_message(message: str) -> str:
    normalized = IP_RE.sub("<ip>", message.lower())
    normalized = re.sub(r"\b\d+\b", "<n>", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized[:240]


def visitor_hash(client_ip: str | None, user_agent: str | None) -> str:
    base = f"{client_ip or '-'}|{user_agent or '-'}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def parse_access_line(
    line: str,
    host_id: str,
    site: str,
    site_host: str,
    default_timezone: dt.tzinfo,
) -> dict[str, Any] | None:
    match = ACCESS_RE.match(line.lstrip("\ufeff").strip())
    if not match:
        return None
    method, uri, protocol = parse_request(match.group("request"))
    timestamp = parse_access_timestamp(match.group("timestamp"), default_timezone)
    tail = parse_tail_tokens(match.group("tail"))
    source_channel, source_name = classify_source(match.group("referer"), site_host)
    user_agent = match.group("user_agent")
    return {
        "event_type": "access_event",
        "host_id": host_id,
        "site": site,
        "ts": timestamp.isoformat() if timestamp else None,
        "timestamp": timestamp,
        "client_ip": match.group("client_ip"),
        "method": method,
        "uri": uri,
        "protocol": protocol,
        "status": int(match.group("status")),
        "bytes_out": to_int(match.group("body_bytes_sent")),
        "bytes_in": tail["request_length"],
        "response_ms": (
            round(float(tail["request_time_s"]) * 1000.0, 2)
            if tail["request_time_s"] is not None
            else None
        ),
        "referer": match.group("referer"),
        "source_channel": source_channel,
        "source_name": source_name,
        "user_agent": user_agent,
        "spider_family": classify_spider(user_agent),
        "raw": line.rstrip("\n"),
    }


def parse_error_line(
    line: str,
    host_id: str,
    site: str,
    default_timezone: dt.tzinfo,
) -> dict[str, Any] | None:
    stripped = line.lstrip("\ufeff").strip()
    nginx_match = NGINX_ERROR_RE.match(stripped)
    if nginx_match:
        timestamp = parse_error_timestamp(nginx_match.group("timestamp"), default_timezone)
        message = nginx_match.group("message")
        client_match = re.search(r"client: (?P<client>\S+)", message)
        request_match = re.search(r'request: "(?P<request>[^"]+)"', message)
        method, uri, _protocol = (
            parse_request(request_match.group("request"))
            if request_match
            else (None, None, None)
        )
        category = classify_error(message)
        fingerprint = f"{category}:{normalize_error_message(message)}"
        return {
            "event_type": "error_event",
            "host_id": host_id,
            "site": site,
            "ts": timestamp.isoformat() if timestamp else None,
            "timestamp": timestamp,
            "component": "nginx",
            "severity": nginx_match.group("level"),
            "category": category,
            "fingerprint": fingerprint,
            "client_ip": client_match.group("client") if client_match else None,
            "method": method,
            "uri": uri,
            "message": message,
            "raw": line.rstrip("\n"),
        }

    apache_match = APACHE_ERROR_RE.match(stripped)
    if not apache_match:
        return None
    timestamp = parse_error_timestamp(apache_match.group("timestamp"), default_timezone)
    client_raw = apache_match.group("client") or ""
    client_match = IP_RE.search(client_raw)
    message = apache_match.group("message")
    category = classify_error(message)
    fingerprint = f"{category}:{normalize_error_message(message)}"
    return {
        "event_type": "error_event",
        "host_id": host_id,
        "site": site,
        "ts": timestamp.isoformat() if timestamp else None,
        "timestamp": timestamp,
        "component": "apache",
        "severity": apache_match.group("module"),
        "category": category,
        "fingerprint": fingerprint,
        "client_ip": client_match.group(0) if client_match else None,
        "method": None,
        "uri": None,
        "message": message,
        "raw": line.rstrip("\n"),
    }


def parse_auth_log_line(
    line: str,
    host_id: str,
    default_timezone: dt.tzinfo,
    reference_time: dt.datetime | None = None,
) -> dict[str, Any] | None:
    stripped = line.lstrip("\ufeff").strip()
    prefix_match = AUTH_LOG_PREFIX_RE.match(stripped)
    if not prefix_match:
        return None
    message = prefix_match.group("message") or ""
    failed_match = SSH_FAILED_PASSWORD_RE.search(message)
    if not failed_match:
        return None
    timestamp = parse_auth_timestamp(
        prefix_match.group("timestamp"),
        default_timezone,
        reference_time=reference_time,
    )
    if timestamp is None:
        return None
    return {
        "event_type": "ssh_auth_event",
        "host_id": host_id,
        "site": HOST_METRIC_SITE,
        "ts": timestamp.isoformat(),
        "timestamp": timestamp,
        "program": str(prefix_match.group("program") or "sshd"),
        "pid": prefix_match.group("pid"),
        "client_ip": str(failed_match.group("client_ip") or ""),
        "username": str(failed_match.group("username") or "unknown"),
        "port": int(failed_match.group("port") or 0),
        "auth_result": "failed_password",
        "fingerprint": "ssh_failed_password",
        "message": message,
        "raw": line.rstrip("\n"),
    }


def serialize_events(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized = []
    for event in events:
        cloned = dict(event)
        timestamp = cloned.pop("timestamp", None)
        if isinstance(timestamp, dt.datetime):
            cloned["ts"] = timestamp.isoformat()
        serialized.append(cloned)
    return serialized


def prune_history(state: dict[str, Any], config: dict[str, Any], now: dt.datetime) -> None:
    retention_minutes = config["agent"]["retention_minutes"]
    max_events = config["agent"]["max_buffer_events"]
    cutoff = now - dt.timedelta(minutes=retention_minutes)

    for site_state in state.get("sites", {}).values():
        history = site_state.get("history", {}) if isinstance(site_state, dict) else {}
        for key in ("access_events", "error_events"):
            items = history.get(key, [])
            trimmed = []
            for item in items:
                timestamp = parse_iso_ts(item.get("ts"))
                if timestamp and timestamp >= cutoff:
                    trimmed.append(item)
            if len(trimmed) > max_events:
                trimmed = trimmed[-max_events:]
            history[key] = trimmed

    system_history = state.setdefault("system_history", {}).setdefault("snapshots", [])
    trimmed_system = []
    for item in system_history:
        timestamp = parse_iso_ts(item.get("ts"))
        if timestamp and timestamp >= cutoff:
            trimmed_system.append(item)
    state["system_history"]["snapshots"] = trimmed_system

    host_security_state = ensure_host_security_state(state)
    ssh_events = host_security_state.get("history", {}).get("ssh_auth_events", [])
    trimmed_ssh_events = []
    for item in ssh_events:
        timestamp = parse_iso_ts(item.get("ts"))
        if timestamp and timestamp >= cutoff:
            trimmed_ssh_events.append(item)
    if len(trimmed_ssh_events) > max_events:
        trimmed_ssh_events = trimmed_ssh_events[-max_events:]
    host_security_state["history"]["ssh_auth_events"] = trimmed_ssh_events


def filter_window(
    events: list[dict[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
) -> list[dict[str, Any]]:
    filtered = []
    for event in events:
        timestamp = event_timestamp(event)
        if timestamp is None:
            continue
        if window_start <= timestamp < window_end:
            filtered.append(event)
    return filtered


def summarize_access_window(
    events: list[dict[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
    slow_ms: float,
    attack_rpm_threshold: int,
) -> dict[str, Any]:
    window_events = filter_window(events, window_start, window_end)
    if not window_events:
        return {
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "total_requests": 0,
            "active_users_10m": 0,
            "pv": 0,
            "uv": 0,
            "unique_ips": 0,
            "qps": 0.0,
            "avg_response_ms": None,
            "slow_request_count": 0,
            "slow_request_top_uris": [],
            "status_families": {},
            "status_codes": {},
            "top_uris": [],
            "top_sources": [],
            "uri_stats": [],
            "source_stats": [],
            "spiders": [],
            "suspicious_ips": [],
            "client_ip_stats": [],
            "client_families": [],
            "bandwidth_out_bytes": 0,
            "bandwidth_in_bytes": None,
            "bandwidth_in_coverage": 0.0,
            "visitor_hashes": [],
            "client_ips": [],
        }

    visitor_keys = {
        f"{event['client_ip']}|{event['user_agent']}" for event in window_events
    }
    visitor_hashes = {
        visitor_hash(event.get("client_ip"), event.get("user_agent"))
        for event in window_events
    }
    client_ips = sorted(
        {str(event["client_ip"]) for event in window_events if event.get("client_ip")}
    )
    response_values = [
        event["response_ms"]
        for event in window_events
        if event.get("response_ms") is not None
    ]
    status_codes = collections.Counter(str(event["status"]) for event in window_events)
    status_families = collections.Counter(
        f"{int(event['status']) // 100}xx" for event in window_events
    )
    top_uris = collections.Counter(event["uri"] or "-" for event in window_events).most_common(10)
    top_sources = collections.Counter(
        str(event["source_name"]) for event in window_events
    ).most_common(10)
    uri_request_counts: collections.Counter[str] = collections.Counter()
    uri_bytes_out: collections.Counter[str] = collections.Counter()
    uri_visitors: dict[str, set[str]] = collections.defaultdict(set)
    source_request_counts: collections.Counter[str] = collections.Counter()
    source_bytes_out: collections.Counter[str] = collections.Counter()
    source_visitors: dict[str, set[str]] = collections.defaultdict(set)
    client_ip_request_counts: collections.Counter[str] = collections.Counter()
    client_ip_bytes_out: collections.Counter[str] = collections.Counter()
    client_family_counts: collections.Counter[str] = collections.Counter()

    spider_counter: collections.Counter[str] = collections.Counter()
    spider_bytes: collections.Counter[str] = collections.Counter()
    for event in window_events:
        spider = event.get("spider_family")
        uri = str(event.get("uri") or "-")
        source_name = str(event.get("source_name") or "direct")
        client_ip = str(event.get("client_ip") or "-")
        visitor_digest = visitor_hash(event.get("client_ip"), event.get("user_agent"))
        bytes_out = int(event.get("bytes_out") or 0)
        uri_request_counts[uri] += 1
        uri_bytes_out[uri] += bytes_out
        uri_visitors[uri].add(visitor_digest)
        source_request_counts[source_name] += 1
        source_bytes_out[source_name] += bytes_out
        source_visitors[source_name].add(visitor_digest)
        if client_ip and client_ip != "-":
            client_ip_request_counts[client_ip] += 1
            client_ip_bytes_out[client_ip] += bytes_out
        client_family_counts[
            classify_client_family(str(event.get("user_agent") or ""), spider)
        ] += 1
        if spider:
            spider_counter[spider] += 1
            spider_bytes[spider] += bytes_out

    per_ip_per_minute: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter
    )
    for event in window_events:
        timestamp = event_timestamp(event)
        if timestamp is None:
            continue
        bucket = timestamp.replace(second=0, microsecond=0).isoformat()
        per_ip_per_minute[str(event["client_ip"])][bucket] += 1
    suspicious_ips = []
    for ip, buckets in per_ip_per_minute.items():
        max_rpm = max(buckets.values()) if buckets else 0
        if max_rpm >= attack_rpm_threshold:
            suspicious_ips.append({"ip": ip, "max_requests_per_minute": max_rpm})
    suspicious_ips.sort(key=lambda item: item["max_requests_per_minute"], reverse=True)

    duration_seconds = max(int((window_end - window_start).total_seconds()), 1)
    slow_counts = collections.Counter(
        event["uri"] or "-"
        for event in window_events
        if event.get("response_ms") is not None and event["response_ms"] >= slow_ms
    )
    bytes_in_values = [
        int(event["bytes_in"]) for event in window_events if event.get("bytes_in") is not None
    ]
    bandwidth_in = sum(bytes_in_values) if bytes_in_values else None
    coverage = round(len(bytes_in_values) / len(window_events), 4)

    return {
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "total_requests": len(window_events),
        "active_users_10m": len(visitor_keys),
        "pv": len(window_events),
        "uv": len(visitor_keys),
        "unique_ips": len({event["client_ip"] for event in window_events}),
        "qps": round(len(window_events) / duration_seconds, 4),
        "avg_response_ms": (
            round(statistics.mean(response_values), 2) if response_values else None
        ),
        "slow_request_count": sum(slow_counts.values()),
        "slow_request_top_uris": [
            {"uri": uri, "count": count} for uri, count in slow_counts.most_common(10)
        ],
        "status_families": dict(status_families),
        "status_codes": dict(status_codes),
        "top_uris": [{"uri": uri, "count": count} for uri, count in top_uris],
        "top_sources": [{"source": source, "count": count} for source, count in top_sources],
        "uri_stats": [
            {
                "uri": uri,
                "count": count,
                "uv_count": len(uri_visitors[uri]),
                "bytes_out": int(uri_bytes_out[uri]),
            }
            for uri, count in uri_request_counts.most_common(20)
        ],
        "source_stats": [
            {
                "source": source,
                "count": count,
                "uv_count": len(source_visitors[source]),
                "bytes_out": int(source_bytes_out[source]),
            }
            for source, count in source_request_counts.most_common(20)
        ],
        "spiders": [
            {
                "family": family,
                "requests": spider_counter[family],
                "bytes_out": spider_bytes[family],
            }
            for family, _count in spider_counter.most_common()
        ],
        "suspicious_ips": suspicious_ips[:10],
        "client_ip_stats": [
            {
                "ip": client_ip,
                "count": count,
                "bytes_out": int(client_ip_bytes_out[client_ip]),
            }
            for client_ip, count in client_ip_request_counts.most_common(20)
        ],
        "client_families": [
            {"family": family, "count": count}
            for family, count in client_family_counts.most_common(20)
        ],
        "bandwidth_out_bytes": sum(int(event.get("bytes_out") or 0) for event in window_events),
        "bandwidth_in_bytes": bandwidth_in,
        "bandwidth_in_coverage": coverage,
        "visitor_hashes": sorted(visitor_hashes),
        "client_ips": client_ips,
    }


def summarize_errors_window(
    events: list[dict[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
) -> dict[str, Any]:
    window_events = filter_window(events, window_start, window_end)
    if not window_events:
        return {
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "total_errors": 0,
            "categories": {},
            "top_fingerprints": [],
        }
    categories = collections.Counter(str(event["category"]) for event in window_events)
    fingerprints = collections.Counter(str(event["fingerprint"]) for event in window_events)
    return {
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "total_errors": len(window_events),
        "categories": dict(categories),
        "top_fingerprints": [
            {"fingerprint": fingerprint, "count": count}
            for fingerprint, count in fingerprints.most_common(10)
        ],
    }


def summarize_ssh_auth_window(
    events: list[dict[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
    brute_force_threshold: int,
) -> dict[str, Any]:
    window_events = filter_window(events, window_start, window_end)
    if not window_events:
        return {
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "failed_attempts": 0,
            "top_source_ips": [],
            "top_usernames": [],
            "bruteforce_ips": [],
        }

    ip_counter = collections.Counter(
        str(event.get("client_ip") or "-")
        for event in window_events
        if event.get("client_ip")
    )
    username_counter = collections.Counter(
        str(event.get("username") or "unknown")
        for event in window_events
    )
    bruteforce_ips = [
        {"ip": ip_address, "count": count}
        for ip_address, count in ip_counter.most_common()
        if count >= brute_force_threshold
    ]
    return {
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "failed_attempts": len(window_events),
        "top_source_ips": [
            {"ip": ip_address, "count": count}
            for ip_address, count in ip_counter.most_common(10)
        ],
        "top_usernames": [
            {"username": username, "count": count}
            for username, count in username_counter.most_common(10)
        ],
        "bruteforce_ips": bruteforce_ips[:10],
    }


def summarize_system_snapshots_window(
    snapshots: list[dict[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
) -> dict[str, Any]:
    window_snapshots = filter_window(snapshots, window_start, window_end)
    if not window_snapshots:
        return {
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "avg_cpu_pct": None,
            "max_cpu_pct": None,
            "avg_memory_pct": None,
            "max_memory_pct": None,
            "min_disk_free_bytes": None,
        }

    cpu_values = [
        float(snapshot["cpu_pct"])
        for snapshot in window_snapshots
        if snapshot.get("cpu_pct") is not None
    ]
    memory_values = [
        float(snapshot["memory_pct"])
        for snapshot in window_snapshots
        if snapshot.get("memory_pct") is not None
    ]
    disk_values = [
        int(snapshot["disk_free_bytes"])
        for snapshot in window_snapshots
        if snapshot.get("disk_free_bytes") is not None
    ]

    return {
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
        "avg_cpu_pct": round(statistics.mean(cpu_values), 2) if cpu_values else None,
        "max_cpu_pct": round(max(cpu_values), 2) if cpu_values else None,
        "avg_memory_pct": round(statistics.mean(memory_values), 2) if memory_values else None,
        "max_memory_pct": round(max(memory_values), 2) if memory_values else None,
        "min_disk_free_bytes": min(disk_values) if disk_values else None,
    }


def collect_system_snapshot(
    disk_root: str,
    host_id: str,
    site: str,
    collect_network_io: bool = True,
) -> dict[str, Any]:
    snapshot = {
        "event_type": "system_snapshot",
        "host_id": host_id,
        "site": site,
        "ts": utcnow().isoformat(),
        "metrics_available": psutil is not None,
    }
    if psutil is None:
        snapshot["warning"] = "psutil is not installed; system metrics are unavailable."
        return snapshot

    cpu_pct = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(disk_root)
    snapshot.update(
        {
            "cpu_pct": round(cpu_pct, 2),
            "memory_pct": round(memory.percent, 2),
            "disk_used_pct": round(disk.percent, 2),
            "disk_free_bytes": int(disk.free),
        }
    )
    if collect_network_io:
        net = psutil.net_io_counters()
        snapshot.update(
            {
                "net_rx_bytes": int(net.bytes_recv),
                "net_tx_bytes": int(net.bytes_sent),
            }
        )
    try:
        load_1m, load_5m, load_15m = psutil.getloadavg()
    except (AttributeError, OSError):
        load_1m = load_5m = load_15m = None
    snapshot.update(
        {
            "load_1m": load_1m,
            "load_5m": load_5m,
            "load_15m": load_15m,
        }
    )
    return snapshot


def evaluate_alerts(
    system_snapshot: dict[str, Any],
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
    thresholds: dict[str, Any],
) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []

    cpu_pct = system_snapshot.get("cpu_pct")
    memory_pct = system_snapshot.get("memory_pct")
    disk_free_bytes = system_snapshot.get("disk_free_bytes")
    disk_used_pct = system_snapshot.get("disk_used_pct")

    if isinstance(cpu_pct, (int, float)) and cpu_pct > thresholds["cpu_pct"]:
        alerts.append({"kind": "cpu_high", "severity": "warning", "value": cpu_pct})
    if isinstance(memory_pct, (int, float)) and memory_pct > thresholds["memory_pct"]:
        alerts.append({"kind": "memory_high", "severity": "warning", "value": memory_pct})
    if (
        isinstance(disk_free_bytes, int)
        and isinstance(disk_used_pct, (int, float))
        and (1.0 - (float(disk_used_pct) / 100.0)) < thresholds["disk_free_ratio"]
    ):
        alerts.append({"kind": "disk_low", "severity": "critical", "value": disk_free_bytes})

    five_xx = sum(
        count
        for code, count in access_summary.get("status_codes", {}).items()
        if code in {"500", "502", "504"}
    )
    if five_xx > thresholds["server_error_count"]:
        alerts.append({"kind": "server_error_burst", "severity": "critical", "count": five_xx})

    suspicious_ips = access_summary.get("suspicious_ips", [])
    if suspicious_ips:
        alerts.append(
            {
                "kind": "suspicious_ip_burst",
                "severity": "critical",
                "top_ip": suspicious_ips[0]["ip"],
                "top_rpm": suspicious_ips[0]["max_requests_per_minute"],
            }
        )

    four_oh_four = int(access_summary.get("status_codes", {}).get("404", 0))
    if four_oh_four >= thresholds["scan_404_count"]:
        alerts.append(
            {"kind": "scan_or_route_breakage", "severity": "warning", "count": four_oh_four}
        )

    avg_response_ms = access_summary.get("avg_response_ms")
    if isinstance(avg_response_ms, (int, float)) and avg_response_ms > thresholds["slow_ms"]:
        alerts.append(
            {
                "kind": "latency_degradation",
                "severity": "critical",
                "avg_response_ms": avg_response_ms,
            }
        )

    if error_summary.get("categories", {}).get("primary_script_unknown"):
        alerts.append({"kind": "php_entrypoint_error", "severity": "warning"})

    return alerts


def evaluate_host_security_alerts(
    ssh_auth_summary: dict[str, Any],
    thresholds: dict[str, Any],
) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    brute_force_ips = ssh_auth_summary.get("bruteforce_ips", [])
    if brute_force_ips:
        top_ip = brute_force_ips[0]
        top_user = (ssh_auth_summary.get("top_usernames") or [{}])[0]
        alerts.append(
            {
                "kind": "ssh_brute_force",
                "severity": "critical",
                "top_ip": top_ip.get("ip"),
                "failure_count": int(top_ip.get("count") or 0),
                "top_username": str(top_user.get("username") or "unknown"),
                "window_minutes": int(thresholds.get("ssh_bruteforce_window_minutes", 5)),
            }
        )
    return alerts


def severity_value(name: str) -> int:
    return SEVERITY_RANK.get(str(name or "").lower(), 0)


def format_human_bytes(num_bytes: int | None) -> str:
    if num_bytes is None:
        return "N/A"
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < 1024.0 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} TB"


def alert_cooldown_key(config: dict[str, Any], alert: dict[str, Any]) -> str:
    site = config["agent"]["site"]
    host_id = config["agent"]["host_id"]
    parts = [host_id, site, str(alert.get("kind") or "unknown")]
    if alert.get("kind") in {"suspicious_ip_burst", "ssh_brute_force"}:
        parts.append(str(alert.get("top_ip") or "-"))
    return ":".join(parts)


def alert_display_site(config: dict[str, Any]) -> str:
    site = str(config.get("agent", {}).get("site") or "-")
    if site == HOST_METRIC_SITE:
        return "host-security"
    return site


def resolve_shared_ai_settings(config: dict[str, Any]) -> dict[str, Any]:
    ai_settings = dict(config.get("notifications", {}).get("reports", {}).get("ai_analysis") or {})
    return {
        "enabled": bool(ai_settings.get("enabled", True)),
        "simulate": bool(ai_settings.get("simulate", False)),
        "endpoint": str(ai_settings.get("endpoint") or ai_settings.get("base_url") or "").strip(),
        "model": str(ai_settings.get("model") or "gpt-4o-mini").strip(),
        "api_key_env": str(ai_settings.get("api_key_env") or "OPENAI_API_KEY").strip(),
        "timeout_seconds": max(int(ai_settings.get("timeout_seconds", 20)), 3),
    }


def build_alert_ai_payload(
    config: dict[str, Any],
    alert: dict[str, Any],
    system_snapshot: dict[str, Any],
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "host_id": config.get("agent", {}).get("host_id"),
        "site": alert_display_site(config),
        "kind": alert.get("kind"),
        "severity": alert.get("severity"),
        "cpu_pct": system_snapshot.get("cpu_pct"),
        "memory_pct": system_snapshot.get("memory_pct"),
        "disk_free_bytes": system_snapshot.get("disk_free_bytes"),
        "request_count": access_summary.get("total_requests"),
        "avg_response_ms": access_summary.get("avg_response_ms"),
        "http_404_count": access_summary.get("status_codes", {}).get("404", 0),
        "http_5xx_count": sum(
            count
            for code, count in access_summary.get("status_codes", {}).items()
            if str(code).startswith("5")
        ),
        "top_ip": alert.get("top_ip"),
        "top_rpm": alert.get("top_rpm"),
        "failure_count": alert.get("failure_count"),
        "top_username": alert.get("top_username"),
        "top_uri": access_summary.get("top_uris", [{}])[0].get("uri") if access_summary.get("top_uris") else None,
        "top_error_fingerprint": error_summary.get("top_fingerprints", [{}])[0].get("fingerprint") if error_summary.get("top_fingerprints") else None,
    }


def alert_ai_prompt(config: dict[str, Any], payload: dict[str, Any]) -> str:
    return (
        "你是资深 Linux 运维专家。请根据以下告警数据，只输出两句话。\n"
        "第 1 句话：用大白话解释发生了什么。\n"
        "第 2 句话：给出最具体的下一步处理建议。\n"
        "不要输出标题、序号或多余解释。\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def log_alert_ai_fallback(reason: str, settings: dict[str, Any]) -> None:
    simulate_enabled = bool(settings.get("simulate"))
    hint = (
        " 请检查 config.yaml 中 notifications.reports.ai_analysis.simulate 是否误设为 true。"
        if simulate_enabled
        else ""
    )
    print(
        f"Warning: AI 请求失败，使用本地兜底话术。原因: {reason}.{hint}",
        file=sys.stderr,
        flush=True,
    )


def request_alert_ai_diagnosis(config: dict[str, Any], payload: dict[str, Any]) -> str | None:
    settings = resolve_shared_ai_settings(config)
    if not settings["enabled"]:
        return None
    if settings["simulate"]:
        log_alert_ai_fallback("simulate=true，已显式启用本地兜底模式", settings)
        return None
    if not settings["endpoint"]:
        log_alert_ai_fallback("未配置 ai_analysis.endpoint/base_url", settings)
        return None
    api_key = os.getenv(settings["api_key_env"])
    if not api_key:
        log_alert_ai_fallback(
            f"未读取到环境变量 {settings['api_key_env']}",
            settings,
        )
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
            {"role": "system", "content": "You are an expert Linux SRE assistant."},
            {"role": "user", "content": alert_ai_prompt(config, payload)},
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
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        log_alert_ai_fallback(str(exc), settings)
        return None
    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        log_alert_ai_fallback("AI 响应格式不符合预期", settings)
        return None


def simulate_alert_ai_diagnosis(alert: dict[str, Any]) -> str:
    kind = str(alert.get("kind") or "")
    if kind == "ssh_brute_force":
        return (
            f"有来源 IP 正在高频尝试 SSH 口令爆破，目标账号集中在 {alert.get('top_username') or '常见账户'}，"
            f"{alert.get('window_minutes') or 5} 分钟内失败 {alert.get('failure_count') or 0} 次。\n"
            "请优先核对白名单与管理 IP，确认后启用或保留自动封禁，并检查是否需要关闭密码登录或更换 SSH 端口。"
        )
    if kind == "suspicious_ip_burst":
        return "同一来源 IP 在短时间内发起异常密集访问，表现更像扫描或 CC 试探而不是正常用户行为。\n请先确认是否命中白名单或搜索引擎爬虫，再视情况启用临时封禁并回看上游日志。"
    if kind == "server_error_burst":
        return "站点在短窗口内连续出现大量 5xx，说明上游应用或服务链路已经进入不稳定状态。\n请优先检查 PHP-FPM、Nginx upstream 和数据库连接池，再决定是否执行一次受控自愈。"
    return "当前告警说明服务出现了短时异常波动，需要尽快确认影响面和触发源头。\n请先查看同一时间段的访问日志、错误日志和系统负载，再按告警建议逐项排查。"


def normalize_alert_ai_diagnosis(text: str | None) -> dict[str, str]:
    cleaned = str(text or "").strip()
    if not cleaned:
        return {"analysis": "", "suggestion": ""}
    lines = [line.strip(" -\t") for line in cleaned.splitlines() if line.strip()]
    if len(lines) >= 2:
        return {"analysis": lines[0], "suggestion": lines[1]}
    sentences = re.split(r"(?<=[。！？.!?])\s*", cleaned)
    sentences = [item.strip() for item in sentences if item.strip()]
    if len(sentences) >= 2:
        return {"analysis": sentences[0], "suggestion": sentences[1]}
    return {"analysis": cleaned, "suggestion": ""}


def build_alert_ai_diagnosis(
    config: dict[str, Any],
    alert: dict[str, Any],
    system_snapshot: dict[str, Any],
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
) -> dict[str, str]:
    payload = build_alert_ai_payload(config, alert, system_snapshot, access_summary, error_summary)
    ai_text = request_alert_ai_diagnosis(config, payload)
    source = "llm"
    if not ai_text:
        ai_text = simulate_alert_ai_diagnosis(alert)
        source = "simulated"
    normalized = normalize_alert_ai_diagnosis(ai_text)
    normalized["source"] = source
    return normalized


def alert_label(alert: dict[str, Any]) -> str:
    labels = {
        "cpu_high": "CPU 使用率过高",
        "memory_high": "内存使用率过高",
        "disk_low": "磁盘剩余空间不足",
        "server_error_burst": "5xx 错误突增",
        "suspicious_ip_burst": "疑似高频攻击",
        "ssh_brute_force": "SSH 暴力破解",
        "scan_or_route_breakage": "404 扫描或路由异常",
        "latency_degradation": "接口性能劣化",
        "php_entrypoint_error": "PHP 入口脚本异常",
    }
    return labels.get(str(alert.get("kind")), str(alert.get("kind") or "unknown_alert"))


def alert_suggestion(alert: dict[str, Any]) -> str:
    suggestions = {
        "cpu_high": "检查高负载进程、慢 SQL 或异常爬虫流量。",
        "memory_high": "检查 PHP-FPM、数据库缓存或大对象泄漏情况。",
        "disk_low": "清理日志/备份目录，并确认是否需要扩容。",
        "server_error_burst": "优先检查 Nginx upstream、PHP-FPM 与最近发布变更。",
        "suspicious_ip_burst": "确认是否为 CC/扫描流量，必要时执行临时封禁。",
        "ssh_brute_force": "优先核对来源 IP 是否可信，并关闭密码登录或启用自动封禁。",
        "scan_or_route_breakage": "检查最近路由变更、静态资源发布或扫描器访问。",
        "latency_degradation": "查看慢请求 URI、上游依赖与数据库响应时间。",
        "php_entrypoint_error": "检查站点根目录、伪静态与 PHP 文件权限。",
    }
    return suggestions.get(str(alert.get("kind")), "请结合最近日志与服务状态继续排查。")


def render_alert_markdown(
    config: dict[str, Any],
    alert: dict[str, Any],
    generated_at: dt.datetime,
    system_snapshot: dict[str, Any],
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
    ai_diagnosis: dict[str, str] | None = None,
) -> str:
    site = alert_display_site(config)
    host_id = config["agent"]["host_id"]
    timezone = get_timezone(config)
    timestamp_local = generated_at.astimezone(timezone).isoformat()
    top_uri = (
        access_summary.get("top_uris", [{}])[0].get("uri")
        if access_summary.get("top_uris")
        else None
    )
    top_error = (
        error_summary.get("top_fingerprints", [{}])[0].get("fingerprint")
        if error_summary.get("top_fingerprints")
        else None
    )
    detail_lines = []
    if alert["kind"] == "cpu_high":
        detail_lines.append(f"- CPU: {system_snapshot.get('cpu_pct')}%")
    elif alert["kind"] == "memory_high":
        detail_lines.append(f"- 内存: {system_snapshot.get('memory_pct')}%")
    elif alert["kind"] == "disk_low":
        detail_lines.append(
            f"- 剩余磁盘: {format_human_bytes(system_snapshot.get('disk_free_bytes'))}"
        )
    elif alert["kind"] == "server_error_burst":
        detail_lines.append(f"- 近窗口 5xx 次数: {alert.get('count', 0)}")
    elif alert["kind"] == "suspicious_ip_burst":
        detail_lines.append(
            f"- 高频 IP: `{alert.get('top_ip')}` ({alert.get('top_rpm')} req/min)"
        )
    elif alert["kind"] == "ssh_brute_force":
        detail_lines.append(
            f"- 攻击来源: `{alert.get('top_ip')}` ({alert.get('failure_count', 0)} failures / {alert.get('window_minutes', 5)} min)"
        )
        detail_lines.append(f"- 目标账号: `{alert.get('top_username') or 'unknown'}`")
    elif alert["kind"] == "scan_or_route_breakage":
        detail_lines.append(f"- 404 次数: {alert.get('count', 0)}")
    elif alert["kind"] == "latency_degradation":
        detail_lines.append(
            f"- 平均响应: {alert.get('avg_response_ms')} ms"
        )

    if top_uri and top_uri != "-":
        detail_lines.append(f"- 热点 URI: `{top_uri}`")
    if top_error:
        detail_lines.append(f"- 主要错误指纹: `{top_error}`")
    detail_lines.append(f"- 建议动作: {alert_suggestion(alert)}")

    lines = [
        f"# Server-Mate 告警 | {alert_label(alert)}",
        "",
        f"- 级别: `{str(alert.get('severity', 'warning')).upper()}`",
        f"- 主机: `{host_id}`",
        f"- 站点: `{site}`",
        f"- 触发时间: {timestamp_local}",
        f"- 当前窗口请求数: {access_summary.get('total_requests', 0)}",
        f"- 当前窗口错误数: {error_summary.get('total_errors', 0)}",
    ]
    lines.extend(detail_lines)
    if ai_diagnosis and (ai_diagnosis.get("analysis") or ai_diagnosis.get("suggestion")):
        lines.extend(
            [
                "",
                "## 💡 AI 智能诊断",
                f"- 原因分析: {ai_diagnosis.get('analysis') or 'N/A'}",
                f"- 行动建议: {ai_diagnosis.get('suggestion') or alert_suggestion(alert)}",
            ]
        )
    return "\n".join(lines)


def deliver_alerts(
    config: dict[str, Any],
    state: dict[str, Any],
    generated_at: dt.datetime,
    alerts: list[dict[str, Any]],
    system_snapshot: dict[str, Any],
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    alerts_config = config.get("notifications", {}).get("alerts", {})
    if not alerts_config.get("enabled", True):
        return []

    minimum_severity = str(alerts_config.get("minimum_severity", "warning")).lower()
    channels = alerts_config.get("channels", [])
    cooldown_seconds = int(alerts_config.get("cooldown_seconds", 300))
    delivery_state = state.setdefault("delivery", {}).setdefault("alert_cooldowns", {})

    results = []
    for alert in alerts:
        if severity_value(alert.get("severity", "warning")) < severity_value(minimum_severity):
            continue

        cooldown_key = alert_cooldown_key(config, alert)
        last_sent = parse_iso_ts(delivery_state.get(cooldown_key))
        if last_sent is not None and cooldown_seconds > 0:
            elapsed = (generated_at - last_sent).total_seconds()
            if elapsed < cooldown_seconds:
                results.append(
                    {
                        "kind": alert["kind"],
                        "severity": alert["severity"],
                        "skipped": True,
                        "reason": "cooldown",
                        "cooldown_key": cooldown_key,
                        "cooldown_remaining_seconds": int(cooldown_seconds - elapsed),
                    }
                )
                continue

        title = f"Server-Mate 告警 | {alert_display_site(config)} | {alert_label(alert)}"
        ai_diagnosis = build_alert_ai_diagnosis(
            config,
            alert,
            system_snapshot,
            access_summary,
            error_summary,
        )
        markdown = render_alert_markdown(
            config,
            alert,
            generated_at,
            system_snapshot,
            access_summary,
            error_summary,
            ai_diagnosis,
        )
        channel_results = send_markdown_message(config, title, markdown, channels)
        success = any(result.get("success") for result in channel_results)
        if success:
            delivery_state[cooldown_key] = generated_at.isoformat()
        results.append(
            {
                "kind": alert["kind"],
                "severity": alert["severity"],
                "success": success,
                "cooldown_key": cooldown_key,
                "ai_diagnosis": ai_diagnosis,
                "channels": channel_results,
            }
        )
    return results


def compact_json(data: dict[str, Any] | None) -> str | None:
    if not data:
        return None
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


def truncate_text(value: str | None, limit: int = 2000) -> str:
    text = str(value or "")
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def format_command_template(template: str, **kwargs: Any) -> str:
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def execute_guarded_command(command_text: str, timeout_seconds: int, dry_run: bool) -> dict[str, Any]:
    if dry_run:
        return {
            "success": True,
            "status": "dry-run",
            "stdout": "",
            "stderr": "",
            "returncode": 0,
            "command_text": command_text,
        }
    try:
        completed = subprocess.run(
            shlex.split(command_text),
            capture_output=True,
            text=True,
            timeout=max(int(timeout_seconds), 1),
            check=False,
        )
    except Exception as exc:
        return {
            "success": False,
            "status": "failed",
            "stdout": "",
            "stderr": str(exc),
            "returncode": None,
            "command_text": command_text,
        }
    return {
        "success": completed.returncode == 0,
        "status": "success" if completed.returncode == 0 else "failed",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "returncode": completed.returncode,
        "command_text": command_text,
    }


def record_automation_action(
    connection: sqlite3.Connection,
    host_id: str,
    site: str,
    action_type: str,
    target: str | None,
    reason: str,
    status: str,
    dry_run: bool,
    command_text: str | None,
    stdout: str | None = None,
    stderr: str | None = None,
    metadata: dict[str, Any] | None = None,
    created_at: dt.datetime | None = None,
) -> None:
    timestamp = (created_at or utcnow()).isoformat()
    connection.execute(
        """
        INSERT INTO automation_actions (
            host_id,
            site,
            action_type,
            target,
            reason,
            status,
            dry_run,
            command_text,
            stdout,
            stderr,
            metadata_json,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            host_id,
            site,
            action_type,
            target,
            reason,
            status,
            1 if dry_run else 0,
            command_text,
            truncate_text(stdout),
            truncate_text(stderr),
            compact_json(metadata),
            timestamp,
        ),
    )


def ip_is_whitelisted(ip_address: str, whitelist: list[str]) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip_address)
    except ValueError:
        return False
    for item in whitelist:
        candidate = str(item or "").strip()
        if not candidate:
            continue
        try:
            if "/" in candidate:
                if ip_obj in ipaddress.ip_network(candidate, strict=False):
                    return True
            elif ip_obj == ipaddress.ip_address(candidate):
                return True
        except ValueError:
            continue
    return False


def ip_matches_whitelisted_spider(
    events: list[dict[str, Any]],
    ip_address: str,
    window_start: dt.datetime,
    window_end: dt.datetime,
    whitelist_spiders: list[str],
) -> bool:
    allowed = {str(item or "").strip().lower() for item in whitelist_spiders if str(item or "").strip()}
    if not allowed:
        return False
    for event in filter_window(events, window_start, window_end):
        if str(event.get("client_ip") or "") != ip_address:
            continue
        spider = str(event.get("spider_family") or "").strip().lower()
        if spider and spider in allowed:
            return True
    return False


def active_ban_row(
    connection: sqlite3.Connection,
    host_id: str,
    site: str,
    ip_address: str,
    now: dt.datetime,
) -> tuple[Any, ...] | None:
    return connection.execute(
        """
        SELECT id, dry_run, expires_at
        FROM banned_ips
        WHERE host_id = ?
          AND site = ?
          AND ip_address = ?
          AND lifted_at IS NULL
          AND expires_at > ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (host_id, site, ip_address, now.isoformat()),
    ).fetchone()


def active_ban_count(
    connection: sqlite3.Connection,
    host_id: str,
    site: str,
    now: dt.datetime,
) -> int:
    row = connection.execute(
        """
        SELECT COUNT(1)
        FROM banned_ips
        WHERE host_id = ?
          AND site = ?
          AND lifted_at IS NULL
          AND expires_at > ?
        """,
        (host_id, site, now.isoformat()),
    ).fetchone()
    return int(row[0] or 0) if row else 0


def recent_automation_action(
    connection: sqlite3.Connection,
    host_id: str,
    site: str,
    action_type: str,
    target: str | None,
    now: dt.datetime,
    cooldown_seconds: int,
) -> tuple[Any, ...] | None:
    if cooldown_seconds <= 0:
        return None
    cutoff = (now - dt.timedelta(seconds=cooldown_seconds)).isoformat()
    if target:
        return connection.execute(
            """
            SELECT id, created_at, status
            FROM automation_actions
            WHERE host_id = ?
              AND site = ?
              AND action_type = ?
              AND target = ?
              AND created_at >= ?
              AND status IN ('success', 'dry-run')
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (host_id, site, action_type, target, cutoff),
        ).fetchone()
    return connection.execute(
        """
        SELECT id, created_at, status
        FROM automation_actions
        WHERE host_id = ?
          AND site = ?
          AND action_type = ?
          AND created_at >= ?
          AND status IN ('success', 'dry-run')
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (host_id, site, action_type, cutoff),
    ).fetchone()


def render_automation_notice(config: dict[str, Any], action: dict[str, Any]) -> tuple[str, str]:
    site = str(action.get("site") or config.get("agent", {}).get("site") or "-")
    if site == HOST_METRIC_SITE:
        site = "host-security"
    title = f"⚠️ 自动化干预通知 | {site} | {action.get('action_type', 'automation')}"
    lines = [
        f"# {title}",
        "",
        f"- 主机: `{config['agent']['host_id']}`",
        f"- 站点: `{site}`",
        f"- 动作: `{action.get('action_type', '-')}`",
        f"- 触发原因: {action.get('reason', '-')}",
        f"- 目标: `{action.get('target', '-')}`",
        f"- 状态: `{action.get('status', '-')}`",
        f"- Dry-Run: `{str(bool(action.get('dry_run', False))).lower()}`",
    ]
    if action.get("command_text"):
        lines.append(f"- 命令: `{action['command_text']}`")
    if action.get("stdout"):
        lines.append(f"- stdout: `{truncate_text(action['stdout'], 300)}`")
    if action.get("stderr"):
        lines.append(f"- stderr: `{truncate_text(action['stderr'], 300)}`")
    return title, "\n".join(lines)


def send_automation_notice(
    config: dict[str, Any],
    channels: list[str],
    action: dict[str, Any],
) -> list[dict[str, Any]]:
    title, markdown = render_automation_notice(config, action)
    return send_markdown_message(config, title, markdown, channels)


def release_expired_bans(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    now: dt.datetime,
) -> list[dict[str, Any]]:
    automation = config.get("automation", {})
    auto_ban = automation.get("auto_ban", {})
    rows = connection.execute(
        """
        SELECT id, site, ip_address, reason, dry_run, unban_command_text
        FROM banned_ips
        WHERE host_id = ?
          AND lifted_at IS NULL
          AND expires_at <= ?
        ORDER BY expires_at ASC
        """,
        (config["agent"]["host_id"], now.isoformat()),
    ).fetchall()
    results: list[dict[str, Any]] = []
    for row in rows:
        site = str(row[1])
        ip_address = str(row[2])
        row_dry_run = bool(row[4])
        command_text = str(row[5] or "").strip() or format_command_template(
            str(auto_ban.get("unban_command_template") or ""),
            ip=ip_address,
            site=site,
            host_id=config["agent"]["host_id"],
        )
        dry_run = bool(automation.get("dry_run", True) or row_dry_run)
        execution = execute_guarded_command(command_text, int(auto_ban.get("timeout_seconds", 15)), dry_run)
        connection.execute(
            """
            UPDATE banned_ips
            SET lifted_at = ?, lift_status = ?, unban_command_text = ?
            WHERE id = ?
            """,
            (now.isoformat(), execution["status"], command_text, int(row[0])),
        )
        action = {
            "host_id": config["agent"]["host_id"],
            "site": site,
            "action_type": "auto_unban",
            "target": ip_address,
            "reason": f"ban ttl expired ({row[3]})",
            "status": execution["status"],
            "dry_run": dry_run,
            "command_text": command_text,
            "stdout": execution.get("stdout"),
            "stderr": execution.get("stderr"),
        }
        record_automation_action(
            connection,
            config["agent"]["host_id"],
            site,
            "auto_unban",
            ip_address,
            action["reason"],
            execution["status"],
            dry_run,
            command_text,
            execution.get("stdout"),
            execution.get("stderr"),
        )
        site_config = build_site_runtime_config(config, find_site(config, site) or {"domain": site, "site_host": site})
        action["notifications"] = send_automation_notice(site_config, auto_ban.get("channels", []), action)
        results.append(action)
    if rows:
        connection.commit()
    return results


def handle_auto_ban(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    site_state: dict[str, Any],
    now: dt.datetime,
    window_start: dt.datetime,
    access_summary: dict[str, Any],
    alerts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    automation = config.get("automation", {})
    auto_ban = automation.get("auto_ban", {})
    if not auto_ban.get("enabled", False):
        return []

    matched_alert = next(
        (
            alert
            for alert in alerts
            if alert.get("kind") in {"suspicious_ip_burst", "ssh_brute_force"}
        ),
        None,
    )
    if not matched_alert:
        return []

    host_id = config["agent"]["host_id"]
    site = config["agent"]["site"]
    ip_address = str(matched_alert.get("top_ip") or "").strip()
    if matched_alert.get("kind") == "ssh_brute_force":
        reason = (
            f"ssh brute-force failures ({matched_alert.get('failure_count', 0)} in "
            f"{matched_alert.get('window_minutes', 5)} minutes)"
        )
    else:
        reason = f"suspicious request burst ({matched_alert.get('top_rpm', 0)} req/min)"
    dry_run = bool(automation.get("dry_run", True))
    actions: list[dict[str, Any]] = []

    action = {
        "host_id": host_id,
        "site": site,
        "action_type": "auto_ban",
        "target": ip_address or "-",
        "reason": reason,
        "dry_run": dry_run,
    }

    if not ip_address:
        action["status"] = "skipped"
        action["stderr"] = "missing target ip"
    elif ip_is_whitelisted(ip_address, list(auto_ban.get("whitelist_ips", []))):
        action["status"] = "skipped"
        action["stderr"] = "ip matched whitelist"
    elif matched_alert.get("kind") == "suspicious_ip_burst" and ip_matches_whitelisted_spider(
        site_state.get("history", {}).get("access_events", []),
        ip_address,
        window_start,
        now,
        list(auto_ban.get("whitelist_spiders", [])),
    ):
        action["status"] = "skipped"
        action["stderr"] = "ip matched spider whitelist"
    elif active_ban_row(connection, host_id, site, ip_address, now):
        action["status"] = "skipped"
        action["stderr"] = "active ban already exists"
    elif active_ban_count(connection, host_id, site, now) >= int(auto_ban.get("max_active_bans", 200)):
        action["status"] = "skipped"
        action["stderr"] = "active ban limit reached"
    else:
        command_text = format_command_template(
            str(auto_ban.get("command_template") or ""),
            ip=ip_address,
            site=site,
            host_id=host_id,
        )
        execution = execute_guarded_command(command_text, int(auto_ban.get("timeout_seconds", 15)), dry_run)
        if execution["status"] in {"success", "dry-run"}:
            expires_at = now + dt.timedelta(seconds=int(auto_ban.get("ban_ttl_seconds", 86400)))
            connection.execute(
                """
                INSERT INTO banned_ips (
                    host_id,
                    site,
                    ip_address,
                    reason,
                    command_text,
                    dry_run,
                    created_at,
                    expires_at,
                    unban_command_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    host_id,
                    site,
                    ip_address,
                    reason,
                    command_text,
                    1 if dry_run else 0,
                    now.isoformat(),
                    expires_at.isoformat(),
                    format_command_template(
                        str(auto_ban.get("unban_command_template") or ""),
                        ip=ip_address,
                        site=site,
                        host_id=host_id,
                    ),
                ),
            )
        action.update(
            {
                "status": execution["status"],
                "command_text": command_text,
                "stdout": execution.get("stdout"),
                "stderr": execution.get("stderr"),
            }
        )

    record_automation_action(
        connection,
        host_id,
        site,
        "auto_ban",
        ip_address or None,
        reason,
        str(action.get("status") or "skipped"),
        dry_run,
        action.get("command_text"),
        action.get("stdout"),
        action.get("stderr"),
        {
            "alert_kind": matched_alert.get("kind"),
            "top_rpm": matched_alert.get("top_rpm"),
            "failure_count": matched_alert.get("failure_count"),
            "top_uri": access_summary.get("top_uris", [{}])[0].get("uri") if access_summary.get("top_uris") else None,
        },
        created_at=now,
    )
    action["notifications"] = send_automation_notice(config, auto_ban.get("channels", []), action)
    connection.commit()
    actions.append(action)
    return actions


def handle_auto_heal(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    now: dt.datetime,
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
    alerts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    automation = config.get("automation", {})
    auto_heal = automation.get("auto_heal", {})
    if not auto_heal.get("enabled", False):
        return []

    trigger_kinds = {str(item or "").strip().lower() for item in auto_heal.get("trigger_kinds", [])}
    matched_alert = next(
        (alert for alert in alerts if str(alert.get("kind") or "").strip().lower() in trigger_kinds),
        None,
    )
    if not matched_alert:
        return []

    host_id = config["agent"]["host_id"]
    site = config["agent"]["site"]
    dry_run = bool(automation.get("dry_run", True))
    actions: list[dict[str, Any]] = []
    reason = f"matched alert {matched_alert.get('kind')} with 5xx pressure"
    top_error = (
        error_summary.get("top_fingerprints", [{}])[0].get("fingerprint")
        if error_summary.get("top_fingerprints")
        else None
    )

    for service in auto_heal.get("services", []):
        service_name = str(service or "").strip()
        if not service_name:
            continue
        recent = recent_automation_action(
            connection,
            host_id,
            site,
            "auto_heal",
            service_name,
            now,
            int(auto_heal.get("cooldown_seconds", 3600)),
        )
        action = {
            "host_id": host_id,
            "site": site,
            "action_type": "auto_heal",
            "target": service_name,
            "reason": reason,
            "dry_run": dry_run,
        }
        if recent:
            action["status"] = "skipped"
            action["stderr"] = "cooldown active"
        else:
            command_text = format_command_template(
                str(auto_heal.get("command_template") or ""),
                service=service_name,
                site=site,
                host_id=host_id,
            )
            execution = execute_guarded_command(command_text, int(auto_heal.get("timeout_seconds", 30)), dry_run)
            action.update(
                {
                    "status": execution["status"],
                    "command_text": command_text,
                    "stdout": execution.get("stdout"),
                    "stderr": execution.get("stderr"),
                }
            )
        record_automation_action(
            connection,
            host_id,
            site,
            "auto_heal",
            service_name,
            reason,
            str(action.get("status") or "skipped"),
            dry_run,
            action.get("command_text"),
            action.get("stdout"),
            action.get("stderr"),
            {
                "alert_kind": matched_alert.get("kind"),
                "http_5xx": sum(
                    count
                    for code, count in access_summary.get("status_codes", {}).items()
                    if code in {"500", "502", "504"}
                ),
                "top_error": top_error,
            },
            created_at=now,
        )
        action["notifications"] = send_automation_notice(config, auto_heal.get("channels", []), action)
        actions.append(action)
    connection.commit()
    return actions


def run_guarded_automation(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    site_state: dict[str, Any],
    now: dt.datetime,
    window_start: dt.datetime,
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
    alerts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    actions.extend(
        handle_auto_ban(
            connection,
            config,
            site_state,
            now,
            window_start,
            access_summary,
            alerts,
        )
    )
    actions.extend(
        handle_auto_heal(
            connection,
            config,
            now,
            access_summary,
            error_summary,
            alerts,
        )
    )
    return actions


def floor_bucket(timestamp: dt.datetime, bucket_minutes: int, timezone: dt.tzinfo) -> dt.datetime:
    local_timestamp = timestamp.astimezone(timezone)
    minute = (local_timestamp.minute // bucket_minutes) * bucket_minutes
    return local_timestamp.replace(minute=minute, second=0, microsecond=0)


def iter_closed_buckets(
    timestamps: list[dt.datetime],
    now: dt.datetime,
    bucket_minutes: int,
    timezone: dt.tzinfo,
) -> list[tuple[dt.datetime, dt.datetime]]:
    if not timestamps:
        return []
    earliest = floor_bucket(min(timestamps), bucket_minutes, timezone)
    current_open_bucket = floor_bucket(now, bucket_minutes, timezone)
    buckets = []
    cursor = earliest
    delta = dt.timedelta(minutes=bucket_minutes)
    while cursor < current_open_bucket:
        buckets.append(
            (
                cursor.astimezone(dt.timezone.utc),
                (cursor + delta).astimezone(dt.timezone.utc),
            )
        )
        cursor += delta
    return buckets


def rewrite_rollup_details(
    connection: sqlite3.Connection,
    rollup_id: int,
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
) -> None:
    connection.execute("DELETE FROM status_code_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM spider_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM error_category_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM error_fingerprint_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM uri_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM uri_detail_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM source_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM visitor_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM client_ip_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM client_ip_request_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM client_family_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM slow_request_rollups WHERE rollup_id = ?", (rollup_id,))
    connection.execute("DELETE FROM suspicious_ip_rollups WHERE rollup_id = ?", (rollup_id,))

    for status_code, request_count in access_summary.get("status_codes", {}).items():
        connection.execute(
            """
            INSERT INTO status_code_rollups (rollup_id, status_code, request_count)
            VALUES (?, ?, ?)
            """,
            (rollup_id, str(status_code), int(request_count)),
        )

    for spider in access_summary.get("spiders", []):
        connection.execute(
            """
            INSERT INTO spider_rollups (rollup_id, spider_family, request_count, bytes_out)
            VALUES (?, ?, ?, ?)
            """,
            (
                rollup_id,
                str(spider["family"]),
                int(spider["requests"]),
                int(spider["bytes_out"]),
            ),
        )

    for category, error_count in error_summary.get("categories", {}).items():
        connection.execute(
            """
            INSERT INTO error_category_rollups (rollup_id, category, error_count)
            VALUES (?, ?, ?)
            """,
            (rollup_id, str(category), int(error_count)),
        )

    for fingerprint_entry in error_summary.get("top_fingerprints", [])[:20]:
        connection.execute(
            """
            INSERT INTO error_fingerprint_rollups (rollup_id, fingerprint, error_count)
            VALUES (?, ?, ?)
            """,
            (
                rollup_id,
                str(fingerprint_entry["fingerprint"]),
                int(fingerprint_entry["count"]),
            ),
        )

    for uri_entry in access_summary.get("top_uris", [])[:20]:
        connection.execute(
            """
            INSERT INTO uri_rollups (rollup_id, uri, request_count)
            VALUES (?, ?, ?)
            """,
            (rollup_id, str(uri_entry["uri"]), int(uri_entry["count"])),
        )

    for uri_entry in access_summary.get("uri_stats", [])[:20]:
        connection.execute(
            """
            INSERT INTO uri_detail_rollups (rollup_id, uri, request_count, uv_count, bytes_out)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                rollup_id,
                str(uri_entry["uri"]),
                int(uri_entry["count"]),
                int(uri_entry.get("uv_count") or 0),
                int(uri_entry.get("bytes_out") or 0),
            ),
        )

    for source_entry in access_summary.get("source_stats", [])[:20]:
        connection.execute(
            """
            INSERT INTO source_rollups (rollup_id, source_name, request_count, uv_count, bytes_out)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                rollup_id,
                str(source_entry["source"]),
                int(source_entry["count"]),
                int(source_entry.get("uv_count") or 0),
                int(source_entry.get("bytes_out") or 0),
            ),
        )

    for visitor_digest in access_summary.get("visitor_hashes", []):
        connection.execute(
            """
            INSERT INTO visitor_rollups (rollup_id, visitor_hash)
            VALUES (?, ?)
            """,
            (rollup_id, str(visitor_digest)),
        )

    for client_ip in access_summary.get("client_ips", []):
        connection.execute(
            """
            INSERT INTO client_ip_rollups (rollup_id, client_ip)
            VALUES (?, ?)
            """,
            (rollup_id, str(client_ip)),
        )

    for client_entry in access_summary.get("client_ip_stats", [])[:20]:
        connection.execute(
            """
            INSERT INTO client_ip_request_rollups (rollup_id, client_ip, request_count, bytes_out)
            VALUES (?, ?, ?, ?)
            """,
            (
                rollup_id,
                str(client_entry["ip"]),
                int(client_entry["count"]),
                int(client_entry.get("bytes_out") or 0),
            ),
        )

    for family_entry in access_summary.get("client_families", [])[:20]:
        connection.execute(
            """
            INSERT INTO client_family_rollups (rollup_id, client_family, request_count)
            VALUES (?, ?, ?)
            """,
            (
                rollup_id,
                str(family_entry["family"]),
                int(family_entry["count"]),
            ),
        )

    for slow_entry in access_summary.get("slow_request_top_uris", [])[:20]:
        connection.execute(
            """
            INSERT INTO slow_request_rollups (rollup_id, uri, slow_request_count)
            VALUES (?, ?, ?)
            """,
            (
                rollup_id,
                str(slow_entry["uri"]),
                int(slow_entry["count"]),
            ),
        )

    for suspicious_entry in access_summary.get("suspicious_ips", [])[:20]:
        connection.execute(
            """
            INSERT INTO suspicious_ip_rollups (rollup_id, client_ip, max_requests_per_minute)
            VALUES (?, ?, ?)
            """,
            (
                rollup_id,
                str(suspicious_entry["ip"]),
                int(suspicious_entry["max_requests_per_minute"]),
            ),
        )


def empty_access_summary() -> dict[str, Any]:
    return {
        "total_requests": 0,
        "pv": 0,
        "uv": 0,
        "unique_ips": 0,
        "active_users_10m": 0,
        "qps": 0.0,
        "avg_response_ms": None,
        "slow_request_count": 0,
        "bandwidth_out_bytes": 0,
        "bandwidth_in_bytes": None,
        "status_codes": {},
        "spiders": [],
        "top_uris": [],
        "uri_stats": [],
        "source_stats": [],
        "visitor_hashes": [],
        "client_ips": [],
        "client_ip_stats": [],
        "client_families": [],
        "slow_request_top_uris": [],
        "suspicious_ips": [],
    }


def empty_error_summary() -> dict[str, Any]:
    return {
        "total_errors": 0,
        "categories": {},
        "top_fingerprints": [],
    }


def empty_system_summary() -> dict[str, Any]:
    return {
        "avg_cpu_pct": None,
        "max_cpu_pct": None,
        "avg_memory_pct": None,
        "max_memory_pct": None,
        "min_disk_free_bytes": None,
    }


def upsert_metric_rollup(
    connection: sqlite3.Connection,
    host_id: str,
    site: str,
    bucket_start_local: str,
    bucket_end_local: str,
    bucket_minutes: int,
    access_summary: dict[str, Any],
    error_summary: dict[str, Any],
    system_summary: dict[str, Any],
) -> int:
    connection.execute(
        """
        INSERT INTO metric_rollups (
            host_id,
            site,
            bucket_start,
            bucket_end,
            bucket_minutes,
            request_count,
            pv,
            uv,
            unique_ips,
            active_users,
            qps,
            avg_response_ms,
            slow_request_count,
            bandwidth_out_bytes,
            bandwidth_in_bytes,
            total_errors,
            avg_cpu_pct,
            max_cpu_pct,
            avg_memory_pct,
            max_memory_pct,
            min_disk_free_bytes,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(host_id, site, bucket_start, bucket_minutes)
        DO UPDATE SET
            bucket_end = excluded.bucket_end,
            request_count = excluded.request_count,
            pv = excluded.pv,
            uv = excluded.uv,
            unique_ips = excluded.unique_ips,
            active_users = excluded.active_users,
            qps = excluded.qps,
            avg_response_ms = excluded.avg_response_ms,
            slow_request_count = excluded.slow_request_count,
            bandwidth_out_bytes = excluded.bandwidth_out_bytes,
            bandwidth_in_bytes = excluded.bandwidth_in_bytes,
            total_errors = excluded.total_errors,
            avg_cpu_pct = excluded.avg_cpu_pct,
            max_cpu_pct = excluded.max_cpu_pct,
            avg_memory_pct = excluded.avg_memory_pct,
            max_memory_pct = excluded.max_memory_pct,
            min_disk_free_bytes = excluded.min_disk_free_bytes,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            host_id,
            site,
            bucket_start_local,
            bucket_end_local,
            bucket_minutes,
            access_summary["total_requests"],
            access_summary["pv"],
            access_summary["uv"],
            access_summary["unique_ips"],
            access_summary["active_users_10m"],
            access_summary["qps"],
            access_summary["avg_response_ms"],
            access_summary["slow_request_count"],
            access_summary["bandwidth_out_bytes"],
            access_summary["bandwidth_in_bytes"],
            error_summary["total_errors"],
            system_summary["avg_cpu_pct"],
            system_summary["max_cpu_pct"],
            system_summary["avg_memory_pct"],
            system_summary["max_memory_pct"],
            system_summary["min_disk_free_bytes"],
        ),
    )
    row = connection.execute(
        """
        SELECT id
        FROM metric_rollups
        WHERE host_id = ?
          AND site = ?
          AND bucket_start = ?
          AND bucket_minutes = ?
        """,
        (host_id, site, bucket_start_local, bucket_minutes),
    ).fetchone()
    return int(row[0])


def persist_rollups(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    state: dict[str, Any],
    now: dt.datetime,
) -> dict[str, int]:
    host_id = config["agent"]["host_id"]
    thresholds = config["thresholds"]
    timezone = get_timezone(config)
    system_snapshots = state.get("system_history", {}).get("snapshots", [])
    system_timestamps = []
    for item in system_snapshots:
        timestamp = event_timestamp(item)
        if timestamp is not None:
            system_timestamps.append(timestamp)

    upserts: dict[str, int] = {}
    zero_access = empty_access_summary()
    zero_error = empty_error_summary()
    zero_system = empty_system_summary()
    for bucket_minutes in config["storage"]["rollup_minutes"]:
        for bucket_start, bucket_end in iter_closed_buckets(system_timestamps, now, bucket_minutes, timezone):
            system_summary = summarize_system_snapshots_window(
                system_snapshots,
                bucket_start,
                bucket_end,
            )
            if system_summary["avg_cpu_pct"] is None:
                continue

            bucket_start_local = bucket_start.astimezone(timezone).isoformat()
            bucket_end_local = bucket_end.astimezone(timezone).isoformat()
            upsert_metric_rollup(
                connection,
                host_id,
                HOST_METRIC_SITE,
                bucket_start_local,
                bucket_end_local,
                bucket_minutes,
                zero_access,
                zero_error,
                system_summary,
            )
            upserts[HOST_METRIC_SITE] = upserts.get(HOST_METRIC_SITE, 0) + 1

        for site in resolve_sites(config):
            domain = str(site.get("domain") or "default")
            site_state = ensure_site_state(state, domain)
            access_events = site_state.get("history", {}).get("access_events", [])
            error_events = site_state.get("history", {}).get("error_events", [])
            timestamps = []
            for item in access_events + error_events:
                timestamp = event_timestamp(item)
                if timestamp is not None:
                    timestamps.append(timestamp)

            for bucket_start, bucket_end in iter_closed_buckets(
                timestamps,
                now,
                bucket_minutes,
                timezone,
            ):
                access_summary = summarize_access_window(
                    access_events,
                    bucket_start,
                    bucket_end,
                    thresholds["slow_ms"],
                    thresholds["attack_rpm_threshold"],
                )
                error_summary = summarize_errors_window(
                    error_events,
                    bucket_start,
                    bucket_end,
                )
                if access_summary["total_requests"] == 0 and error_summary["total_errors"] == 0:
                    continue

                bucket_start_local = bucket_start.astimezone(timezone).isoformat()
                bucket_end_local = bucket_end.astimezone(timezone).isoformat()
                rollup_id = upsert_metric_rollup(
                    connection,
                    host_id,
                    domain,
                    bucket_start_local,
                    bucket_end_local,
                    bucket_minutes,
                    access_summary,
                    error_summary,
                    zero_system,
                )
                rewrite_rollup_details(connection, rollup_id, access_summary, error_summary)
                upserts[domain] = upserts.get(domain, 0) + 1

    connection.commit()
    return upserts


def record_run(
    connection: sqlite3.Connection,
    config: dict[str, Any],
    run_started_at: dt.datetime,
    run_finished_at: dt.datetime,
    parser_stats: dict[str, int],
    rollups_upserted: int,
    mode: str,
) -> None:
    connection.execute(
        """
        INSERT INTO agent_runs (
            run_started_at,
            run_finished_at,
            host_id,
            site,
            mode,
            access_lines_read,
            access_lines_dropped,
            error_lines_read,
            error_lines_dropped,
            rollups_upserted
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_started_at.isoformat(),
            run_finished_at.isoformat(),
            config["agent"]["host_id"],
            config["agent"]["site"],
            mode,
            parser_stats["access_lines_read"],
            parser_stats["access_lines_dropped"],
            parser_stats["error_lines_read"],
            parser_stats["error_lines_dropped"],
            rollups_upserted,
        ),
    )
    connection.commit()


def run_cycle(
    config: dict[str, Any],
    state: dict[str, Any],
    connection: sqlite3.Connection,
    config_path: Path,
    config_generated: bool,
    mode: str,
) -> dict[str, Any]:
    run_started_at = utcnow()
    now = run_started_at
    host_id = config["agent"]["host_id"]
    thresholds = config["thresholds"]
    state_file = Path(config["agent"]["state_file"])
    database_file = Path(config["storage"]["database_file"])
    timezone = get_timezone(config)
    sites = resolve_sites(config)
    expired_unbans = release_expired_bans(connection, config, now)

    system_metrics = config.get("system_metrics", {})
    if system_metrics.get("enabled", True):
        system_snapshot = collect_system_snapshot(
            str(system_metrics.get("disk_root") or "/"),
            host_id,
            HOST_METRIC_SITE,
            bool(system_metrics.get("collect_network_io", True)),
        )
    else:
        system_snapshot = {
            "event_type": "system_snapshot",
            "host_id": host_id,
            "site": HOST_METRIC_SITE,
            "ts": utcnow().isoformat(),
            "metrics_available": False,
            "disabled": True,
        }

    if system_metrics.get("enabled", True):
        state.setdefault("system_history", {}).setdefault("snapshots", []).append(
            serialize_events([system_snapshot])[0]
        )

    host_security_state = ensure_host_security_state(state)
    auth_log_value = str(config.get("logs", {}).get("auth_log") or "").strip()
    auth_log_path = Path(auth_log_value) if auth_log_value else None
    auth_lines: list[str] = []
    auth_cursor: dict[str, Any] = {}
    if auth_log_path:
        auth_lines, auth_cursor = read_incremental_lines(
            auth_log_path,
            host_security_state["cursors"].get("auth_log"),
            config["agent"]["startup_mode"],
            config["agent"]["bootstrap_tail_lines"],
        )
        host_security_state["cursors"]["auth_log"] = auth_cursor

    ssh_auth_events: list[dict[str, Any]] = []
    dropped_auth = 0
    for line in auth_lines:
        event = parse_auth_log_line(
            line,
            host_id,
            timezone,
            reference_time=now,
        )
        if event is None:
            dropped_auth += 1
            continue
        ssh_auth_events.append(event)
    host_security_state["history"]["ssh_auth_events"].extend(serialize_events(ssh_auth_events))

    site_results: dict[str, dict[str, Any]] = {}
    collected_events: dict[str, dict[str, list[dict[str, Any]]]] = {}

    for site in sites:
        domain = str(site.get("domain") or "default")
        site_config = build_site_runtime_config(config, site)
        site_state = ensure_site_state(state, domain)
        access_path = Path(site_config["logs"]["access_log"])
        error_path = Path(site_config["logs"]["error_log"])

        access_lines, access_cursor = read_incremental_lines(
            access_path,
            site_state["cursors"].get("access_log"),
            config["agent"]["startup_mode"],
            config["agent"]["bootstrap_tail_lines"],
        )
        error_lines, error_cursor = read_incremental_lines(
            error_path,
            site_state["cursors"].get("error_log"),
            config["agent"]["startup_mode"],
            config["agent"]["bootstrap_tail_lines"],
        )
        site_state["cursors"]["access_log"] = access_cursor
        site_state["cursors"]["error_log"] = error_cursor

        access_events: list[dict[str, Any]] = []
        dropped_access = 0
        for line in access_lines:
            event = parse_access_line(
                line,
                host_id,
                domain,
                str(site.get("site_host") or domain),
                timezone,
            )
            if event is None:
                dropped_access += 1
                continue
            access_events.append(event)

        error_events: list[dict[str, Any]] = []
        dropped_errors = 0
        for line in error_lines:
            event = parse_error_line(line, host_id, domain, timezone)
            if event is None:
                dropped_errors += 1
                continue
            error_events.append(event)

        site_state["history"]["access_events"].extend(serialize_events(access_events))
        site_state["history"]["error_events"].extend(serialize_events(error_events))
        collected_events[domain] = {
            "access_events": serialize_events(access_events),
            "error_events": serialize_events(error_events),
        }
        site_results[domain] = {
            "site": domain,
            "site_host": str(site.get("site_host") or domain),
            "access_log": str(access_path),
            "error_log": str(error_path),
            "parser_stats": {
                "access_lines_read": len(access_lines),
                "access_lines_dropped": dropped_access,
                "error_lines_read": len(error_lines),
                "error_lines_dropped": dropped_errors,
            },
            "cursors": {
                "access_log": access_cursor,
                "error_log": error_cursor,
            },
            "_site_config": site_config,
        }

    prune_history(state, config, now)
    save_state(state_file, state)

    summary_window_start = now - dt.timedelta(minutes=thresholds["summary_window_minutes"])
    ssh_window_start = now - dt.timedelta(minutes=thresholds["ssh_bruteforce_window_minutes"])
    ssh_auth_summary = summarize_ssh_auth_window(
        host_security_state["history"]["ssh_auth_events"],
        ssh_window_start,
        now,
        thresholds["ssh_bruteforce_failures"],
    )
    host_security_config = build_site_runtime_config(
        config,
        {
            "domain": HOST_METRIC_SITE,
            "site_host": host_id,
            "enabled": True,
            "access_log": config.get("logs", {}).get("access_log") or "",
            "error_log": config.get("logs", {}).get("error_log") or "",
        },
    )
    host_alerts = evaluate_host_security_alerts(ssh_auth_summary, thresholds)
    host_access_summary = empty_access_summary()
    host_error_summary = empty_error_summary()
    host_alert_deliveries = deliver_alerts(
        host_security_config,
        state,
        now,
        host_alerts,
        system_snapshot,
        host_access_summary,
        host_error_summary,
    )
    host_automation_actions = run_guarded_automation(
        connection,
        host_security_config,
        {"history": {"access_events": []}},
        now,
        ssh_window_start,
        host_access_summary,
        host_error_summary,
        host_alerts,
    )
    for domain, site_result in site_results.items():
        site_config = site_result.pop("_site_config")
        site_state = ensure_site_state(state, domain)
        access_summary = summarize_access_window(
            site_state["history"]["access_events"],
            summary_window_start,
            now,
            thresholds["slow_ms"],
            thresholds["attack_rpm_threshold"],
        )
        error_summary = summarize_errors_window(
            site_state["history"]["error_events"],
            summary_window_start,
            now,
        )
        alerts = evaluate_alerts(system_snapshot, access_summary, error_summary, thresholds)
        alert_deliveries = deliver_alerts(
            site_config,
            state,
            now,
            alerts,
            system_snapshot,
            access_summary,
            error_summary,
        )
        site_result["traffic"] = access_summary
        site_result["errors"] = error_summary
        site_result["alerts"] = alerts
        site_result["notifications"] = {
            "alert_deliveries": alert_deliveries,
        }
        automation_actions = run_guarded_automation(
            connection,
            site_config,
            site_state,
            now,
            summary_window_start,
            access_summary,
            error_summary,
            alerts,
        )
        site_result["automation"] = {
            "actions": automation_actions,
        }
        site_result["storage"] = {
            "history_access_events": len(site_state["history"]["access_events"]),
            "history_error_events": len(site_state["history"]["error_events"]),
        }
        if config["agent"]["emit_events"]:
            site_result["access_events"] = collected_events.get(domain, {}).get("access_events", [])
            site_result["error_events"] = collected_events.get(domain, {}).get("error_events", [])

    save_state(state_file, state)
    rollups_upserted = persist_rollups(connection, config, state, now)
    run_finished_at = utcnow()

    total_parser_stats = {
        "access_lines_read": sum(item["parser_stats"]["access_lines_read"] for item in site_results.values()),
        "access_lines_dropped": sum(item["parser_stats"]["access_lines_dropped"] for item in site_results.values()),
        "error_lines_read": sum(item["parser_stats"]["error_lines_read"] for item in site_results.values()),
        "error_lines_dropped": sum(item["parser_stats"]["error_lines_dropped"] for item in site_results.values()),
        "auth_lines_read": len(auth_lines),
        "auth_lines_dropped": dropped_auth,
    }

    for domain, site_result in site_results.items():
        site_config = build_site_runtime_config(config, find_site(config, domain) or {"domain": domain})
        record_run(
            connection,
            site_config,
            run_started_at,
            run_finished_at,
            site_result["parser_stats"],
            int(rollups_upserted.get(domain, 0)),
            mode,
        )
        site_result["storage"]["rollups_upserted"] = int(rollups_upserted.get(domain, 0))

    payload = {
        "meta": {
            "host_id": host_id,
            "generated_at": now.isoformat(),
            "config_path": str(config_path),
            "config_generated": config_generated,
            "mode": mode,
            "state_file": str(state_file),
            "database_file": str(database_file),
            "summary_window_minutes": thresholds["summary_window_minutes"],
            "rollup_minutes": config["storage"]["rollup_minutes"],
            "site_count": len(sites),
            "sites": [site["domain"] for site in sites],
        },
        "system_snapshot": system_snapshot,
        "sites": site_results,
        "host_security": {
            "auth_log": str(auth_log_path) if auth_log_path else "",
            "parser_stats": {
                "auth_lines_read": len(auth_lines),
                "auth_lines_dropped": dropped_auth,
            },
            "cursor": auth_cursor,
            "ssh_auth": ssh_auth_summary,
            "alerts": host_alerts,
            "notifications": {
                "alert_deliveries": host_alert_deliveries,
            },
            "automation": {
                "actions": host_automation_actions,
            },
            "storage": {
                "history_ssh_auth_events": len(host_security_state["history"]["ssh_auth_events"]),
            },
        },
        "parser_stats": total_parser_stats,
        "storage": {
            "rollups_upserted": rollups_upserted,
            "history_system_snapshots": len(state.get("system_history", {}).get("snapshots", [])),
        },
        "automation": {
            "expired_unbans": expired_unbans,
            "dry_run": bool(config.get("automation", {}).get("dry_run", True)),
        },
    }
    if config["agent"]["emit_events"]:
        payload["host_security"]["ssh_auth_events"] = serialize_events(ssh_auth_events)
    return payload


def mask_secret_url(url: str) -> str:
    cleaned = str(url or "")
    if not cleaned:
        return ""
    if len(cleaned) <= 24:
        return cleaned[:8] + "***"
    return cleaned[:24] + "..." + cleaned[-8:]


def sanitize_config_for_output(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    output = copy.deepcopy(config)
    for channel_name in ("dingtalk", "wecom", "feishu"):
        channel = output.get("notifications", {}).get("webhooks", {}).get(channel_name)
        if isinstance(channel, dict) and channel.get("url"):
            channel["url"] = mask_secret_url(str(channel["url"]))
    telegram_channel = output.get("notifications", {}).get("webhooks", {}).get("telegram")
    if isinstance(telegram_channel, dict):
        if telegram_channel.get("bot_token"):
            telegram_channel["bot_token"] = mask_secret_url(str(telegram_channel["bot_token"]))
        if telegram_channel.get("chat_id"):
            telegram_channel["chat_id"] = mask_secret_url(str(telegram_channel["chat_id"]))
    output["meta"] = {
        "config_path": str(config_path.resolve()),
        "yaml_parser_available": yaml is not None,
    }
    return output


def quote_systemd_value(value: str) -> str:
    text = str(value)
    if not text:
        return '""'
    if any(char.isspace() for char in text) or any(char in text for char in ('"', "\\")):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def build_systemd_service_unit(config_path: Path) -> str:
    workspace_dir = config_path.parent.resolve()
    script_path = Path(__file__).resolve()
    python_path = Path(sys.executable).resolve() if sys.executable else Path("/usr/bin/python3")
    exec_parts = [
        quote_systemd_value(str(python_path)),
        quote_systemd_value(str(script_path)),
        "--config",
        quote_systemd_value(str(config_path.resolve())),
        "--daemon",
    ]
    lines = [
        "# Copy this unit to /etc/systemd/system/server-mate.service",
        "[Unit]",
        "Description=Server-Mate Agent",
        "After=network-online.target",
        "Wants=network-online.target",
        "",
        "[Service]",
        "Type=simple",
        f"WorkingDirectory={quote_systemd_value(str(workspace_dir))}",
        "Environment=PYTHONUNBUFFERED=1",
        f"ExecStart={' '.join(exec_parts)}",
        "Restart=always",
        "RestartSec=5",
        "",
        "[Install]",
        "WantedBy=multi-user.target",
    ]
    return "\n".join(lines) + "\n"


def resolve_mode(args: argparse.Namespace, config: dict[str, Any]) -> str:
    if args.daemon:
        return "daemon"
    if args.once:
        return "once"
    return config["agent"].get("mode", "once")


def run_daemon(
    config: dict[str, Any],
    state: dict[str, Any],
    connection: sqlite3.Connection,
    config_path: Path,
    config_generated: bool,
) -> int:
    interval_seconds = config["agent"]["poll_interval_seconds"]
    while True:
        try:
            payload = run_cycle(
                config,
                state,
                connection,
                config_path,
                config_generated,
                "daemon",
            )
            print(json.dumps(payload, sort_keys=True), flush=True)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            try:
                connection.rollback()
            except sqlite3.Error:
                pass
            failure_payload = {
                "meta": {
                    "mode": "daemon",
                    "host_id": config["agent"]["host_id"],
                    "site": "*",
                    "generated_at": utcnow().isoformat(),
                    "cycle_status": "failed",
                },
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "traceback": traceback.format_exc(limit=8),
                },
            }
            print(json.dumps(failure_payload, sort_keys=True), flush=True)
        time.sleep(interval_seconds)


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()

    if args.generate_service:
        print(build_systemd_service_unit(config_path), end="")
        return 0

    config, config_generated = load_config(config_path)

    if args.print_config:
        print(
            json.dumps(
                sanitize_config_for_output(config, config_path),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    mode = resolve_mode(args, config)
    state_file = Path(config["agent"]["state_file"])
    database_file = Path(config["storage"]["database_file"])
    state = migrate_state_shape(load_state(state_file), config)
    connection = init_database(database_file)
    try:
        if mode == "daemon":
            return run_daemon(config, state, connection, config_path, config_generated)
        payload = run_cycle(
            config,
            state,
            connection,
            config_path,
            config_generated,
            "once",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
