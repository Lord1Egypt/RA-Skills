#!/usr/bin/env python3
"""Agent token cost monitor with threshold alerts.

The script is intentionally stdlib-only so it can run from cron, OpenClaw,
Hermes, or a regular shell without installing dependencies.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - Python < 3.9 fallback
    ZoneInfo = None  # type: ignore


TZ_SHANGHAI = ZoneInfo("Asia/Shanghai") if ZoneInfo else timezone(timedelta(hours=8))


HERMES_API_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(?P<ms>\d{3})\s+"
    r"\S+\s+\[(?P<session>[^\]]+)\]\s+[^:]+:\s+API call #\d+:\s+"
    r"model=(?P<model>\S+)\s+provider=(?P<provider>\S+)\s+"
    r"in=(?P<input>\d+)\s+out=(?P<output>\d+)\s+total=(?P<total>\d+)"
    r"(?:.*?\scache=(?P<cache_read>\d+)/(?P<prompt_for_cache>\d+)\s+\([^)]*\))?"
)

INCLUDED_PROVIDERS = {"openai-codex"}


DEFAULT_PRICES_CNY = {
    "deepseek-v4-pro": {
        "cache_hit_cny_per_million": 0.025,
        "cache_miss_cny_per_million": 3.0,
        "output_cny_per_million": 6.0,
    },
    "deepseek-v4-flash": {
        "cache_hit_cny_per_million": 0.02,
        "cache_miss_cny_per_million": 1.0,
        "output_cny_per_million": 2.0,
    },
    "deepseek-chat": {
        "cache_hit_cny_per_million": 0.02,
        "cache_miss_cny_per_million": 1.0,
        "output_cny_per_million": 2.0,
    },
    "deepseek-reasoner": {
        "cache_hit_cny_per_million": 0.02,
        "cache_miss_cny_per_million": 1.0,
        "output_cny_per_million": 2.0,
    },
    "kimi-k2.6": {
        "cache_hit_cny_per_million": 1.16,
        "cache_miss_cny_per_million": 6.89,
        "output_cny_per_million": 29.0,
    },
    "kimi-k2.7-code": {
        "cache_hit_cny_per_million": 1.16,
        "cache_miss_cny_per_million": 6.89,
        "output_cny_per_million": 29.0,
    },
    "gateway-injected": {
        "cache_hit_cny_per_million": 0.0,
        "cache_miss_cny_per_million": 0.0,
        "output_cny_per_million": 0.0,
    },
}


@dataclass
class Bucket:
    calls: int = 0
    cache_miss_input: int = 0
    cache_hit_input: int = 0
    output: int = 0
    total_tokens: int = 0
    cost_cny: float = 0.0

    def add(self, miss: int, hit: int, output: int, total: int, cost_cny: float, calls: int = 1) -> None:
        self.calls += max(1, int(calls or 1))
        self.cache_miss_input += miss
        self.cache_hit_input += hit
        self.output += output
        self.total_tokens += total
        self.cost_cny += cost_cny

    def as_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "cache_miss_input": self.cache_miss_input,
            "cache_hit_input": self.cache_hit_input,
            "output": self.output,
            "total_tokens": self.total_tokens,
            "cost_cny": round(self.cost_cny, 6),
        }


@dataclass
class Snapshot:
    generated_at: str
    date: str
    data_source: str
    source_detail: str
    group_label: str
    total: Bucket
    by_model: dict[str, Bucket]
    by_agent: dict[str, Bucket]
    unpriced: dict[str, Bucket]
    usage_records: int
    priced_records: int

    def as_state(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "date": self.date,
            "data_source": self.data_source,
            "source_detail": self.source_detail,
            "total": self.total.as_dict(),
            "by_model": buckets_to_dict(self.by_model),
            "by_group": buckets_to_dict(self.by_agent),
            "unpriced": buckets_to_dict(self.unpriced),
            "usage_records": self.usage_records,
            "priced_records": self.priced_records,
        }


@dataclass
class AlertResult:
    status: str
    should_alert: bool
    delta_cny: float = 0.0
    delta_percent: float | None = None
    previous_total_cny: float | None = None
    reason: str = ""


def buckets_to_dict(buckets: dict[str, Bucket]) -> dict[str, dict[str, Any]]:
    return {
        key: bucket.as_dict()
        for key, bucket in sorted(buckets.items(), key=lambda item: item[1].cost_cny, reverse=True)
    }


def default_openclaw_dir() -> Path:
    for env_name in ("OPENCLAW_STATE_DIR", "OPENCLAW_HOME"):
        value = os.environ.get(env_name)
        if value:
            return Path(value).expanduser()
    return Path.home() / ".openclaw"


def default_hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))).expanduser()


def invoked_from_hermes() -> bool:
    for env_name in ("HERMES_HOME", "HERMES_STATE_DIR", "HERMES_DATA_DIR", "HERMES_SESSION_ID", "HERMES_PROFILE"):
        if os.environ.get(env_name):
            return True
    try:
        return ".hermes" in Path(__file__).resolve().parts
    except Exception:
        return False


def resolve_source(source: str) -> str:
    if source != "auto":
        return source
    if invoked_from_hermes():
        return "hermes"
    return "openclaw"


def default_state_dir(source: str, openclaw_dir: Path, hermes_home: Path) -> Path:
    value = os.environ.get("OPENCLAW_TOKEN_COST_GUARD_STATE_DIR")
    if value:
        return Path(value).expanduser()
    if source == "hermes":
        for env_name in ("HERMES_STATE_DIR", "HERMES_DATA_DIR"):
            value = os.environ.get(env_name)
            if value:
                return Path(value).expanduser() / "token-cost-guard"
        return hermes_home / "token-cost-guard"
    return openclaw_dir / "token-cost-guard"


def parse_args() -> argparse.Namespace:
    default_threshold = float(os.environ.get("OPENCLAW_TOKEN_COST_THRESHOLD_CNY", "20"))
    default_percent = float(os.environ.get("OPENCLAW_TOKEN_COST_THRESHOLD_PERCENT", "0"))
    openclaw_dir = default_openclaw_dir()
    hermes_home = default_hermes_home()

    parser = argparse.ArgumentParser(description="Monitor agent token cost and alert on spikes.")
    parser.add_argument("--source", choices=("auto", "openclaw", "hermes"), default="auto")
    parser.add_argument("--openclaw-dir", default=str(openclaw_dir))
    parser.add_argument("--hermes-home", default=str(hermes_home))
    parser.add_argument("--date", help="Date to inspect in YYYY-MM-DD, default today in Asia/Shanghai.")
    parser.add_argument(
        "--period",
        choices=("day", "current-hour", "previous-hour"),
        default="day",
        help="Time window to inspect. Use previous-hour for hourly cron alerts.",
    )
    parser.add_argument("--agent", action="append", help="Agent id to include. Repeatable. Defaults to all agents with sessions.")
    parser.add_argument("--pricing-file", help="JSON price override file.")
    parser.add_argument(
        "--usd-cny",
        type=float,
        default=float(os.environ.get("TOKEN_COST_GUARD_USD_CNY", os.environ.get("TOKEN_REPORT_USD_CNY", "6.81"))),
        help="USD/CNY conversion for Hermes state.db costs. Defaults to TOKEN_COST_GUARD_USD_CNY, TOKEN_REPORT_USD_CNY, or 6.81.",
    )
    parser.add_argument("--threshold-cny", type=float, default=default_threshold)
    parser.add_argument("--threshold-percent", type=float, default=default_percent)
    parser.add_argument(
        "--alert-mode",
        choices=("delta", "total"),
        default="delta",
        help="delta compares with the previous snapshot; total alerts when the current window exceeds --threshold-cny.",
    )
    parser.add_argument("--state-file")
    parser.add_argument("--reports-dir")
    parser.add_argument("--init-only", action="store_true", help="Write baseline without alerting.")
    parser.add_argument("--no-state-write", action="store_true", help="Do not update state file.")
    parser.add_argument("--always-report", action="store_true", help="Print report even when no alert fires.")
    parser.add_argument("--quiet-ok", action="store_true", help="Print nothing when status is OK and no alert fires.")
    parser.add_argument("--alert-exit-zero", action="store_true", help="Exit 0 even when an alert fires. Useful for cron jobs where alerts are expected outcomes.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--watch-interval", type=float, help="Run continuously every N seconds.")
    parser.add_argument("--send-openclaw", action="store_true", help="Send alert via `openclaw message send`.")
    parser.add_argument("--send-always", action="store_true", help="Send report even when no alert fires.")
    parser.add_argument("--channel", help="OpenClaw message channel, e.g. feishu.")
    parser.add_argument("--target", help="OpenClaw message target/chat id.")
    parser.add_argument("--account", help="Optional OpenClaw message account id.")
    parser.add_argument("--send-dry-run", action="store_true", help="Pass --dry-run to openclaw message send.")
    args = parser.parse_args()
    args.resolved_source = resolve_source(args.source)
    state_dir = default_state_dir(args.resolved_source, Path(args.openclaw_dir).expanduser(), Path(args.hermes_home).expanduser())
    if not args.state_file:
        args.state_file = str(state_dir / "state.json")
    if not args.reports_dir:
        args.reports_dir = str(state_dir / "reports")
    return args


def target_date(args: argparse.Namespace) -> str:
    if args.date:
        return args.date
    return datetime.now(TZ_SHANGHAI).date().isoformat()


def target_window(args: argparse.Namespace) -> tuple[datetime, datetime, str]:
    if args.period == "day":
        start_date = datetime.fromisoformat(target_date(args)).date()
        start = datetime(start_date.year, start_date.month, start_date.day, tzinfo=TZ_SHANGHAI)
        return start, start + timedelta(days=1), start.date().isoformat()

    now = datetime.now(TZ_SHANGHAI)
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    if args.period == "previous-hour":
        start = current_hour - timedelta(hours=1)
        end = current_hour
    else:
        start = current_hour
        end = current_hour + timedelta(hours=1)
    label = f"{start.strftime('%Y-%m-%dT%H%M%z')}..{end.strftime('%Y-%m-%dT%H%M%z')}"
    return start, end, label


def load_prices(pricing_file: str | None) -> dict[str, dict[str, float]]:
    prices: dict[str, dict[str, float]] = json.loads(json.dumps(DEFAULT_PRICES_CNY))
    if not pricing_file:
        return prices

    with open(pricing_file, "r", encoding="utf-8") as handle:
        overrides = json.load(handle)
    for model, value in overrides.items():
        prices[model] = {
            "cache_hit_cny_per_million": float(value.get("cache_hit_cny_per_million", value.get("cache_hit", 0))),
            "cache_miss_cny_per_million": float(value.get("cache_miss_cny_per_million", value.get("cache_miss", 0))),
            "output_cny_per_million": float(value.get("output_cny_per_million", value.get("output", 0))),
        }
    return prices


def discover_agents(openclaw_dir: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return requested
    agents_dir = openclaw_dir / "agents"
    if not agents_dir.exists():
        return []
    agents = []
    for child in sorted(agents_dir.iterdir()):
        if child.is_dir() and (child / "sessions").exists():
            agents.append(child.name)
    return agents


def parse_event_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            number = float(value)
            if number > 10_000_000_000:
                number = number / 1000.0
            return datetime.fromtimestamp(number, timezone.utc).astimezone(TZ_SHANGHAI)
        text = str(value)
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ_SHANGHAI)
        return dt.astimezone(TZ_SHANGHAI)
    except Exception:
        return None


def parse_event_date(value: Any) -> str | None:
    dt = parse_event_datetime(value)
    return dt.date().isoformat() if dt else None


def normalize_model(provider: str | None, model: str | None) -> str | None:
    if not model:
        return None
    normalized = str(model)
    if provider == "deepseek" and not normalized.startswith("deepseek-"):
        normalized = f"deepseek-{normalized}"
    if "/" in normalized:
        normalized = normalized.split("/", 1)[1]
    return normalized


def usage_int(usage: dict[str, Any], *keys: str) -> int:
    for key in keys:
        value = usage.get(key)
        if value is not None:
            try:
                return int(value or 0)
            except Exception:
                return 0
    return 0


def number_value(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", "")
            if not value:
                return None
        number = float(value)
    except Exception:
        return None
    if number < 0:
        return None
    return number


def cost_amount_to_cny(amount: Any, currency: Any, usd_cny: float, default_currency: str = "cny") -> float | None:
    number = number_value(amount)
    if number is None:
        return None
    normalized = str(currency or default_currency).strip().lower()
    if normalized in ("usd", "us$", "$"):
        return number * usd_cny
    if normalized in ("cny", "rmb", "yuan", "renminbi", "¥", "cn¥", "cnh"):
        return number
    return None


def native_cost_cny(value: Any, usd_cny: float, default_currency: str = "cny") -> float | None:
    if isinstance(value, dict):
        currency = value.get("currency") or value.get("unit")
        for key in ("cny", "costCny", "cost_cny", "totalCny", "total_cny", "amountCny", "amount_cny"):
            if key in value:
                return cost_amount_to_cny(value.get(key), "cny", usd_cny)
        for key in ("usd", "costUsd", "cost_usd", "totalUsd", "total_usd", "amountUsd", "amount_usd"):
            if key in value:
                return cost_amount_to_cny(value.get(key), "usd", usd_cny)
        for key in ("total", "amount", "value", "cost"):
            if key in value:
                converted = cost_amount_to_cny(value.get(key), currency, usd_cny, default_currency=default_currency)
                if converted is not None:
                    return converted
        return None
    return cost_amount_to_cny(value, default_currency, usd_cny, default_currency=default_currency)


def usage_native_cost_cny(usage: dict[str, Any], usd_cny: float) -> float | None:
    for key in ("cost", "costTotal", "cost_total", "totalCost", "total_cost"):
        if key in usage:
            converted = native_cost_cny(usage.get(key), usd_cny, default_currency="cny")
            if converted is not None:
                return converted
    for key in ("costCny", "cost_cny", "totalCostCny", "total_cost_cny", "estimatedCostCny", "estimated_cost_cny", "actualCostCny", "actual_cost_cny"):
        if key in usage:
            converted = cost_amount_to_cny(usage.get(key), "cny", usd_cny)
            if converted is not None:
                return converted
    for key in ("costUsd", "cost_usd", "totalCostUsd", "total_cost_usd", "estimatedCostUsd", "estimated_cost_usd", "actualCostUsd", "actual_cost_usd"):
        if key in usage:
            converted = cost_amount_to_cny(usage.get(key), "usd", usd_cny)
            if converted is not None:
                return converted
    return None


def compute_cost_cny(
    model: str,
    miss: int,
    hit: int,
    output: int,
    prices: dict[str, dict[str, float]],
    provider: str | None = None,
) -> float | None:
    if (provider or "").lower() in INCLUDED_PROVIDERS:
        return 0.0
    price = prices.get(model)
    if price is None:
        return None
    return (
        miss * price["cache_miss_cny_per_million"]
        + hit * price["cache_hit_cny_per_million"]
        + output * price["output_cny_per_million"]
    ) / 1_000_000


def collect_openclaw_snapshot(args: argparse.Namespace, prices: dict[str, dict[str, float]]) -> Snapshot:
    openclaw_dir = Path(args.openclaw_dir).expanduser()
    window_start, window_end, window_label = target_window(args)
    agents = discover_agents(openclaw_dir, args.agent)
    total = Bucket()
    by_model: dict[str, Bucket] = {}
    by_agent: dict[str, Bucket] = {}
    unpriced: dict[str, Bucket] = {}
    usage_records = 0
    priced_records = 0

    for agent in agents:
        sessions_dir = openclaw_dir / "agents" / agent / "sessions"
        if not sessions_dir.exists():
            continue
        by_agent.setdefault(agent, Bucket())
        for session_file in sorted(sessions_dir.glob("*.jsonl")):
            with open(session_file, "r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if event.get("type") != "message":
                        continue
                    message = event.get("message") or {}
                    if message.get("role") != "assistant":
                        continue
                    event_time = parse_event_datetime(event.get("timestamp") or message.get("timestamp"))
                    if event_time is None or not (window_start <= event_time < window_end):
                        continue

                    usage = message.get("usage") or {}
                    model = normalize_model(message.get("provider"), message.get("model"))
                    if not model:
                        continue

                    miss = usage_int(usage, "input", "inputTokens") + usage_int(usage, "cacheWrite", "cacheWriteInputTokens")
                    hit = usage_int(usage, "cacheRead", "cacheReadInputTokens")
                    output = usage_int(usage, "output", "outputTokens")
                    total_tokens = usage_int(usage, "totalTokens", "total_tokens") or (miss + hit + output)
                    if not (miss or hit or output or total_tokens):
                        continue

                    usage_records += 1
                    cost_cny = usage_native_cost_cny(usage, float(args.usd_cny))
                    if cost_cny is None:
                        cost_cny = compute_cost_cny(model, miss, hit, output, prices, message.get("provider"))
                    if cost_cny is None:
                        unpriced.setdefault(model, Bucket()).add(miss, hit, output, total_tokens, 0.0)
                        continue

                    priced_records += 1
                    total.add(miss, hit, output, total_tokens, cost_cny)
                    by_agent.setdefault(agent, Bucket()).add(miss, hit, output, total_tokens, cost_cny)
                    by_model.setdefault(model, Bucket()).add(miss, hit, output, total_tokens, cost_cny)

    return Snapshot(
        generated_at=datetime.now(TZ_SHANGHAI).isoformat(timespec="seconds"),
        date=window_label,
        data_source="openclaw",
        source_detail=str(openclaw_dir),
        group_label="Agents",
        total=total,
        by_model=by_model,
        by_agent=by_agent,
        unpriced=unpriced,
        usage_records=usage_records,
        priced_records=priced_records,
    )


def hermes_day_window(date: str) -> tuple[datetime, datetime]:
    start_date = datetime.fromisoformat(date).date()
    start = datetime(start_date.year, start_date.month, start_date.day, tzinfo=TZ_SHANGHAI)
    return start, start + timedelta(days=1)


def iter_hermes_log_lines(log_dir: Path):
    for path in sorted(log_dir.glob("agent.log*"), key=lambda item: item.name):
        try:
            if path.suffix == ".gz":
                with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as handle:
                    yield from handle
            else:
                with path.open("r", encoding="utf-8", errors="ignore") as handle:
                    yield from handle
        except Exception:
            continue


def infer_hermes_source(session_id: str | None) -> str:
    session = str(session_id or "")
    if session.startswith("cron_") or session.startswith("session_cron_"):
        return "cron"
    if session.startswith("session_"):
        return "legacy-session"
    if re.match(r"^\d{8}_", session):
        return "cli"
    return "unknown"


def load_hermes_session_sources(hermes_home: Path, start: datetime, end: datetime) -> dict[str, str]:
    db = hermes_home / "state.db"
    if not db.exists():
        return {}
    try:
        con = sqlite3.connect(str(db))
        rows = con.execute(
            "SELECT id, source FROM sessions WHERE started_at < ? AND COALESCE(ended_at, ?) >= ?",
            (end.timestamp(), end.timestamp(), start.timestamp()),
        ).fetchall()
        con.close()
    except Exception:
        return {}
    return {str(session_id): str(source or "") for session_id, source in rows if session_id}


def load_hermes_session_billing(hermes_home: Path, start: datetime, end: datetime) -> dict[str, dict[str, Any]]:
    db = hermes_home / "state.db"
    if not db.exists():
        return {}
    try:
        con = sqlite3.connect(str(db))
        con.row_factory = sqlite3.Row
        rows = con.execute(
            """
            SELECT id, source, estimated_cost_usd, actual_cost_usd,
                   COALESCE(input_tokens,0) + COALESCE(output_tokens,0) +
                   COALESCE(cache_read_tokens,0) + COALESCE(cache_write_tokens,0) AS total_tokens
            FROM sessions
            WHERE started_at < ? AND COALESCE(ended_at, ?) >= ?
            """,
            (end.timestamp(), end.timestamp(), start.timestamp()),
        ).fetchall()
        con.close()
    except Exception:
        return {}

    billing: dict[str, dict[str, Any]] = {}
    for row in rows:
        session_id = str(row["id"] or "")
        if not session_id:
            continue
        cost_usd = number_value(row["actual_cost_usd"])
        if cost_usd is None or cost_usd <= 0:
            cost_usd = number_value(row["estimated_cost_usd"])
        billing[session_id] = {
            "source": str(row["source"] or ""),
            "cost_usd": cost_usd if cost_usd is not None and cost_usd > 0 else None,
            "total_tokens": int(row["total_tokens"] or 0),
        }
    return billing


def add_usage_record(
    *,
    group: str,
    provider: str | None,
    model: str | None,
    miss: int,
    hit: int,
    output: int,
    total_tokens: int,
    calls: int,
    cost_cny: float | None,
    prices: dict[str, dict[str, float]],
    total: Bucket,
    by_model: dict[str, Bucket],
    by_agent: dict[str, Bucket],
    unpriced: dict[str, Bucket],
) -> bool:
    normalized_model = normalize_model(provider, model)
    if not normalized_model:
        return False
    if not (miss or hit or output or total_tokens):
        return False
    if cost_cny is None:
        cost_cny = compute_cost_cny(normalized_model, miss, hit, output, prices, provider)
    if cost_cny is None:
        unpriced.setdefault(normalized_model, Bucket()).add(miss, hit, output, total_tokens, 0.0, calls=calls)
        return False
    total.add(miss, hit, output, total_tokens, cost_cny, calls=calls)
    by_agent.setdefault(group, Bucket()).add(miss, hit, output, total_tokens, cost_cny, calls=calls)
    by_model.setdefault(normalized_model, Bucket()).add(miss, hit, output, total_tokens, cost_cny, calls=calls)
    return True


def collect_hermes_from_logs(
    hermes_home: Path,
    start: datetime,
    end: datetime,
    prices: dict[str, dict[str, float]],
    usd_cny: float,
    total: Bucket,
    by_model: dict[str, Bucket],
    by_agent: dict[str, Bucket],
    unpriced: dict[str, Bucket],
) -> tuple[int, int]:
    session_sources = load_hermes_session_sources(hermes_home, start, end)
    session_billing = load_hermes_session_billing(hermes_home, start, end)
    records: list[dict[str, Any]] = []
    session_tokens: dict[str, int] = {}

    for line in iter_hermes_log_lines(hermes_home / "logs"):
        match = HERMES_API_RE.search(line)
        if not match:
            continue
        try:
            ts = datetime.strptime(match.group("ts"), "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ_SHANGHAI)
        except Exception:
            continue
        if not (start <= ts < end):
            continue

        session_id = match.group("session")
        provider = match.group("provider") or "unknown"
        model = match.group("model") or "unknown"
        prompt = int(match.group("input") or 0)
        output = int(match.group("output") or 0)
        total_tokens = int(match.group("total") or (prompt + output))
        hit = int(match.group("cache_read") or 0)
        miss = max(0, prompt - hit)
        group = session_sources.get(session_id) or infer_hermes_source(session_id)

        records.append(
            {
                "session_id": session_id,
                "group": group,
                "provider": provider,
                "model": model,
                "miss": miss,
                "hit": hit,
                "output": output,
                "total_tokens": total_tokens,
            }
        )
        session_tokens[session_id] = session_tokens.get(session_id, 0) + max(0, total_tokens)

    priced_records = 0
    for record in records:
        session_id = record["session_id"]
        billing = session_billing.get(session_id) or {}
        if not record["group"]:
            record["group"] = billing.get("source") or infer_hermes_source(session_id)

        cost_cny = None
        session_cost_usd = billing.get("cost_usd")
        denominator = int(billing.get("total_tokens") or 0) or session_tokens.get(session_id, 0)
        if session_cost_usd is not None and denominator > 0:
            cost_cny = float(session_cost_usd) * usd_cny * (record["total_tokens"] / denominator)

        if add_usage_record(
            group=record["group"],
            provider=record["provider"],
            model=record["model"],
            miss=record["miss"],
            hit=record["hit"],
            output=record["output"],
            total_tokens=record["total_tokens"],
            calls=1,
            cost_cny=cost_cny,
            prices=prices,
            total=total,
            by_model=by_model,
            by_agent=by_agent,
            unpriced=unpriced,
        ):
            priced_records += 1
    return len(records), priced_records


def collect_hermes_from_state_db(
    hermes_home: Path,
    start: datetime,
    end: datetime,
    prices: dict[str, dict[str, float]],
    usd_cny: float,
    total: Bucket,
    by_model: dict[str, Bucket],
    by_agent: dict[str, Bucket],
    unpriced: dict[str, Bucket],
) -> tuple[int, int]:
    db = hermes_home / "state.db"
    if not db.exists():
        return 0, 0
    try:
        con = sqlite3.connect(str(db))
        con.row_factory = sqlite3.Row
        rows = con.execute(
            """
            SELECT id, source, model, billing_provider,
                   COALESCE(input_tokens,0) AS input_tokens,
                   COALESCE(output_tokens,0) AS output_tokens,
                   COALESCE(cache_read_tokens,0) AS cache_read_tokens,
                   COALESCE(cache_write_tokens,0) AS cache_write_tokens,
                   COALESCE(api_call_count,0) AS api_call_count,
                   estimated_cost_usd,
                   actual_cost_usd
            FROM sessions
            WHERE started_at >= ? AND started_at < ?
              AND (COALESCE(input_tokens,0) + COALESCE(output_tokens,0) +
                   COALESCE(cache_read_tokens,0) + COALESCE(cache_write_tokens,0)) > 0
            """,
            (start.timestamp(), end.timestamp()),
        ).fetchall()
        con.close()
    except Exception:
        return 0, 0

    usage_records = 0
    priced_records = 0
    for row in rows:
        provider = row["billing_provider"] or "unknown"
        model = row["model"] or "unknown"
        miss = int(row["input_tokens"] or 0) + int(row["cache_write_tokens"] or 0)
        hit = int(row["cache_read_tokens"] or 0)
        output = int(row["output_tokens"] or 0)
        total_tokens = miss + hit + output
        calls = int(row["api_call_count"] or 0) or 1
        group = row["source"] or infer_hermes_source(row["id"])

        cost_usd = row["actual_cost_usd"]
        if cost_usd is None:
            cost_usd = row["estimated_cost_usd"]
        cost_cny = None
        try:
            if cost_usd is not None and float(cost_usd) > 0:
                cost_cny = float(cost_usd) * usd_cny
        except Exception:
            cost_cny = None

        usage_records += 1
        if add_usage_record(
            group=group,
            provider=provider,
            model=model,
            miss=miss,
            hit=hit,
            output=output,
            total_tokens=total_tokens,
            calls=calls,
            cost_cny=cost_cny,
            prices=prices,
            total=total,
            by_model=by_model,
            by_agent=by_agent,
            unpriced=unpriced,
        ):
            priced_records += 1
    return usage_records, priced_records


def collect_hermes_snapshot(args: argparse.Namespace, prices: dict[str, dict[str, float]]) -> Snapshot:
    hermes_home = Path(args.hermes_home).expanduser()
    window_start, window_end, window_label = target_window(args)
    total = Bucket()
    by_model: dict[str, Bucket] = {}
    by_agent: dict[str, Bucket] = {}
    unpriced: dict[str, Bucket] = {}

    usage_records, priced_records = collect_hermes_from_logs(
        hermes_home,
        window_start,
        window_end,
        prices,
        float(args.usd_cny),
        total,
        by_model,
        by_agent,
        unpriced,
    )
    source_detail = f"{hermes_home}/logs/agent.log* + state.db billing"
    if usage_records == 0:
        usage_records, priced_records = collect_hermes_from_state_db(
            hermes_home,
            window_start,
            window_end,
            prices,
            float(args.usd_cny),
            total,
            by_model,
            by_agent,
            unpriced,
        )
        source_detail = f"{hermes_home}/state.db sessions"

    return Snapshot(
        generated_at=datetime.now(TZ_SHANGHAI).isoformat(timespec="seconds"),
        date=window_label,
        data_source="hermes",
        source_detail=source_detail,
        group_label="Hermes Sources",
        total=total,
        by_model=by_model,
        by_agent=by_agent,
        unpriced=unpriced,
        usage_records=usage_records,
        priced_records=priced_records,
    )


def collect_snapshot(args: argparse.Namespace, prices: dict[str, dict[str, float]]) -> Snapshot:
    if args.resolved_source == "hermes":
        return collect_hermes_snapshot(args, prices)
    return collect_openclaw_snapshot(args, prices)


def load_previous_state(state_file: Path) -> dict[str, Any] | None:
    if not state_file.exists():
        return None
    try:
        with open(state_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None


def compare(snapshot: Snapshot, previous: dict[str, Any] | None, args: argparse.Namespace) -> AlertResult:
    if args.init_only:
        return AlertResult(status="initialized", should_alert=False, reason="已初始化基线")
    if args.alert_mode == "total":
        current_total = snapshot.total.cost_cny
        should_alert = current_total > args.threshold_cny
        return AlertResult(
            status="alert" if should_alert else "ok",
            should_alert=should_alert,
            delta_cny=0.0,
            previous_total_cny=None,
            reason=(
                f"当前窗口费用 {current_total:.2f} 元 > 阈值 {args.threshold_cny:.2f} 元"
                if should_alert
                else f"当前窗口费用 {current_total:.2f} 元 <= 阈值 {args.threshold_cny:.2f} 元"
            ),
        )
    if not previous:
        return AlertResult(status="initialized", should_alert=False, reason="没有上一份快照，已建立基线")
    if previous.get("date") != snapshot.date:
        return AlertResult(status="initialized", should_alert=False, reason="新的日期或时间窗口，已建立基线")

    previous_total = float((previous.get("total") or {}).get("cost_cny") or 0.0)
    current_total = snapshot.total.cost_cny
    delta = current_total - previous_total
    percent = (delta / previous_total * 100.0) if previous_total > 0 else None

    absolute_alert = delta > args.threshold_cny
    percent_alert = percent is not None and args.threshold_percent > 0 and percent > args.threshold_percent
    should_alert = absolute_alert or percent_alert
    reason_parts = []
    if absolute_alert:
        reason_parts.append(f"费用增量 {delta:.2f} 元 > 阈值 {args.threshold_cny:.2f} 元")
    if percent_alert:
        reason_parts.append(f"费用增幅 {percent:.1f}% > 阈值 {args.threshold_percent:.1f}%")

    return AlertResult(
        status="alert" if should_alert else "ok",
        should_alert=should_alert,
        delta_cny=delta,
        delta_percent=percent,
        previous_total_cny=previous_total,
        reason="；".join(reason_parts) if reason_parts else "未超过阈值",
    )


def format_number(value: int) -> str:
    return f"{value:,}"


def top_rows(title: str, buckets: dict[str, Bucket], limit: int = 8) -> list[str]:
    rows = [f"## {title}", "", "| 名称 | 调用次数 | 总 Tokens | 费用（元） |", "|---|---:|---:|---:|"]
    visible = [
        (name, bucket)
        for name, bucket in buckets.items()
        if bucket.calls > 0 or bucket.total_tokens > 0 or bucket.cost_cny > 0
    ]
    for name, bucket in sorted(visible, key=lambda item: item[1].cost_cny, reverse=True)[:limit]:
        rows.append(f"| {name} | {bucket.calls} | {format_number(bucket.total_tokens)} | {bucket.cost_cny:.2f} |")
    if len(rows) == 4:
        rows.append("| 无 | 0 | 0 | 0.00 |")
    rows.append("")
    return rows


def status_zh(status: str) -> str:
    return {
        "alert": "报警",
        "ok": "正常",
        "initialized": "已初始化",
    }.get(status, status)


def group_title_zh(group_label: str) -> str:
    if group_label == "Agents":
        return "Agent 费用排行"
    if group_label == "Hermes Sources":
        return "Hermes 来源费用排行"
    return f"{group_label} 费用排行"


def render_report(snapshot: Snapshot, result: AlertResult, args: argparse.Namespace) -> str:
    window_label = "日期" if args.period == "day" else "时间窗口"
    threshold_label = "窗口阈值" if args.alert_mode == "total" else "阈值"
    lines = [
        "# Token 费用守卫报告",
        "",
        f"- 状态: {status_zh(result.status)}",
        f"- {window_label}: {snapshot.date}",
        f"- 数据源: {snapshot.data_source} ({snapshot.source_detail})",
        f"- 生成时间: {snapshot.generated_at}",
        f"- 当前已知费用: {snapshot.total.cost_cny:.2f} 元",
        f"- 当前已知 Tokens: {format_number(snapshot.total.total_tokens)}",
        f"- 用量记录: 共 {snapshot.usage_records} 条，已计价 {snapshot.priced_records} 条",
        f"- {threshold_label}: {args.threshold_cny:.2f} 元"
        + (f" 或 {args.threshold_percent:.1f}%" if args.threshold_percent > 0 else ""),
    ]
    if result.previous_total_cny is not None:
        lines.extend(
            [
                f"- 上次已知费用: {result.previous_total_cny:.2f} 元",
                f"- 费用增量: {result.delta_cny:.2f} 元"
                + (f" ({result.delta_percent:.1f}%)" if result.delta_percent is not None else ""),
            ]
        )
    lines.append(f"- 判断原因: {result.reason}")
    lines.append("")
    lines.extend(top_rows("模型费用排行", snapshot.by_model))
    lines.extend(top_rows(group_title_zh(snapshot.group_label), snapshot.by_agent))

    if snapshot.unpriced:
        lines.extend(["## 未定价模型", "", "| 模型 | 调用次数 | 总 Tokens |", "|---|---:|---:|"])
        for name, bucket in sorted(snapshot.unpriced.items(), key=lambda item: item[1].total_tokens, reverse=True):
            lines.append(f"| {name} | {bucket.calls} | {format_number(bucket.total_tokens)} |")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_report(report: str, snapshot: Snapshot, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = snapshot.generated_at.replace(":", "").replace("+", "_").replace("-", "")
    safe_label = re.sub(r"[^0-9A-Za-z_.+-]+", "_", snapshot.date)
    path = reports_dir / f"token-cost-{safe_label}-{stamp}.md"
    path.write_text(report, encoding="utf-8")
    return path


def write_state(snapshot: Snapshot, state_file: Path) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(snapshot.as_state(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def send_openclaw(report: str, args: argparse.Namespace) -> None:
    if not args.channel or not args.target:
        raise SystemExit("--send-openclaw requires --channel and --target")
    command = ["openclaw", "message", "send", "--channel", args.channel, "--target", args.target, "--message", report]
    if args.account:
        command.extend(["--account", args.account])
    if args.send_dry_run:
        command.append("--dry-run")
    subprocess.run(command, check=True, timeout=60)


def run_once(args: argparse.Namespace, prices: dict[str, dict[str, float]]) -> int:
    state_file = Path(args.state_file).expanduser()
    reports_dir = Path(args.reports_dir).expanduser()
    previous = load_previous_state(state_file)
    snapshot = collect_snapshot(args, prices)
    result = compare(snapshot, previous, args)
    report = render_report(snapshot, result, args)
    report_path = write_report(report, snapshot, reports_dir)

    if not args.no_state_write:
        write_state(snapshot, state_file)

    if args.json:
        print(json.dumps({"result": result.__dict__, "snapshot": snapshot.as_state(), "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    elif result.should_alert or args.always_report or args.init_only:
        print(report)
        print(f"报告文件: {report_path}")
    elif not args.quiet_ok:
        print(
            f"正常: 当前费用={snapshot.total.cost_cny:.2f} 元，"
            f"增量={result.delta_cny:.2f} 元，报告={report_path}"
        )

    if args.send_openclaw and (result.should_alert or args.send_always):
        send_openclaw(report, args)

    if result.should_alert and not args.alert_exit_zero:
        return 2
    return 0


def main() -> int:
    args = parse_args()
    prices = load_prices(args.pricing_file)

    if args.watch_interval:
        exit_code = 0
        try:
            while True:
                exit_code = max(exit_code, run_once(args, prices))
                time.sleep(args.watch_interval)
        except KeyboardInterrupt:
            return exit_code
    return run_once(args, prices)


if __name__ == "__main__":
    raise SystemExit(main())
