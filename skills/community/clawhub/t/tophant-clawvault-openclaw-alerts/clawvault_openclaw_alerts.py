#!/usr/bin/env python3
"""ClawVault OpenClaw Alerts - standalone OpenClaw skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

APP_DIR = Path.home() / ".ClawVault" / "openclaw-alerts"
DEFAULT_CONFIG_PATH = APP_DIR / "config.yaml"
DEFAULT_STATE_PATH = APP_DIR / "state.json"
DEFAULT_PID_PATH = APP_DIR / "daemon.pid"
DEFAULT_LOG_PATH = APP_DIR / "alerts.log"
VERSION = "0.1.0"


def default_config() -> dict[str, Any]:
    return {
        "dashboard": {
            "base_url": "http://127.0.0.1:8766",
            "timeout_seconds": 5,
        },
        "openclaw": {
            "command": "openclaw",
            "agent_id": "main",
            "session_id": "clawvault-alerts",
            "local": True,
            "deliver": False,
            "channel": None,
            "reply_channel": None,
            "reply_to": None,
            "timeout_seconds": 180,
        },
        "alerts": {
            "enabled": True,
            "poll_interval_seconds": 10,
            "scan_history_limit": 200,
            "risk_threshold": 7.0,
            "threat_levels": ["high", "critical"],
            "actions": ["block", "ask_user", "sanitize"],
            "sources": ["proxy", "file", "plugin", "openclaw-file-guard", "local_scan", "test"],
            "dedup_ttl_seconds": 3600,
            "max_alerts_per_minute": 5,
            "max_alerts_per_hour": 60,
            "include_input_preview": False,
            "include_file_path": False,
            "max_message_chars": 1200,
        },
        "daily_report": {
            "enabled": True,
            "time": "09:00",
            "send_empty_report": True,
            "max_recent_events": 10,
        },
        "daemon": {
            "pid_file": str(DEFAULT_PID_PATH),
            "state_file": str(DEFAULT_STATE_PATH),
            "log_file": str(DEFAULT_LOG_PATH),
        },
    }


def deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    for key, value in update.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def expand_path(path: str | Path) -> Path:
    return Path(path).expanduser()


class AlertConfig:
    def __init__(self, path: str | None = None):
        self.path = expand_path(path) if path else DEFAULT_CONFIG_PATH

    def load(self) -> dict[str, Any]:
        cfg = default_config()
        if self.path.exists():
            if yaml is None:
                raise RuntimeError("pyyaml is required to read config.yaml")
            data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
            if not isinstance(data, dict):
                raise ValueError(f"Config must be a mapping: {self.path}")
            deep_merge(cfg, data)
        self._normalize_paths(cfg)
        errors = self.validate(cfg)
        if errors:
            raise ValueError("; ".join(errors))
        return cfg

    def save(self, cfg: dict[str, Any]) -> str:
        if yaml is None:
            raise RuntimeError("pyyaml is required to write config.yaml")
        self._normalize_paths(cfg)
        errors = self.validate(cfg)
        if errors:
            raise ValueError("; ".join(errors))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
        try:
            self.path.chmod(0o600)
        except OSError:
            pass
        return str(self.path)

    def configure(self, args: argparse.Namespace) -> dict[str, Any]:
        cfg = self.load() if self.path.exists() else default_config()
        if args.dashboard_url:
            cfg["dashboard"]["base_url"] = args.dashboard_url
        if args.agent:
            cfg["openclaw"]["agent_id"] = args.agent
        if args.session_id:
            cfg["openclaw"]["session_id"] = args.session_id
        if args.risk_threshold is not None:
            cfg["alerts"]["risk_threshold"] = args.risk_threshold
        if args.poll_interval is not None:
            cfg["alerts"]["poll_interval_seconds"] = args.poll_interval
        if args.daily_time:
            cfg["daily_report"]["time"] = args.daily_time
        if args.timeout is not None:
            cfg["openclaw"]["timeout_seconds"] = args.timeout
        if args.deliver is not None:
            cfg["openclaw"]["deliver"] = args.deliver
        if args.channel:
            cfg["openclaw"]["channel"] = args.channel
        if args.reply_channel:
            cfg["openclaw"]["reply_channel"] = args.reply_channel
        if args.reply_to:
            cfg["openclaw"]["reply_to"] = args.reply_to
        path = self.save(cfg)
        return {"success": True, "config_path": path, "config": public_config_summary(cfg)}

    def validate(self, cfg: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        base_url = str(cfg.get("dashboard", {}).get("base_url", ""))
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append("dashboard.base_url must be an http(s) URL")
        if float(cfg.get("alerts", {}).get("risk_threshold", 0)) < 0:
            errors.append("alerts.risk_threshold must be non-negative")
        if int(cfg.get("alerts", {}).get("poll_interval_seconds", 0)) <= 0:
            errors.append("alerts.poll_interval_seconds must be positive")
        if int(cfg.get("alerts", {}).get("max_alerts_per_minute", 0)) <= 0:
            errors.append("alerts.max_alerts_per_minute must be positive")
        if int(cfg.get("alerts", {}).get("max_alerts_per_hour", 0)) <= 0:
            errors.append("alerts.max_alerts_per_hour must be positive")
        if int(cfg.get("openclaw", {}).get("timeout_seconds", 0)) <= 0:
            errors.append("openclaw.timeout_seconds must be positive")
        daily_time = str(cfg.get("daily_report", {}).get("time", ""))
        if not re.match(r"^([01]\d|2[0-3]):[0-5]\d$", daily_time):
            errors.append("daily_report.time must be HH:MM")
        return errors

    def _normalize_paths(self, cfg: dict[str, Any]) -> None:
        daemon = cfg.setdefault("daemon", {})
        daemon.setdefault("pid_file", str(DEFAULT_PID_PATH))
        daemon.setdefault("state_file", str(DEFAULT_STATE_PATH))
        daemon.setdefault("log_file", str(DEFAULT_LOG_PATH))
        for key in ("pid_file", "state_file", "log_file"):
            daemon[key] = str(expand_path(daemon[key]))


class StateStore:
    def __init__(self, path: str | Path):
        self.path = expand_path(path)
        self.state = self.load()

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._empty()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                empty = self._empty()
                deep_merge(empty, data)
                return empty
        except (OSError, ValueError):
            pass
        return self._empty()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        try:
            self.path.chmod(0o600)
        except OSError:
            pass

    def cleanup(self, now: float, ttl_seconds: int) -> None:
        sent = self.state.setdefault("sent_events", {})
        expired = [key for key, value in sent.items() if now - float(value.get("sent_at", 0)) > ttl_seconds]
        for key in expired:
            sent.pop(key, None)
        stamps = [float(ts) for ts in self.state.setdefault("rate_limit", {}).setdefault("sent_timestamps", [])]
        self.state["rate_limit"]["sent_timestamps"] = [ts for ts in stamps if now - ts <= 3600]

    def has_event(self, key: str) -> bool:
        return key in self.state.setdefault("sent_events", {})

    def mark_event(self, key: str, event: dict[str, Any], now: float) -> None:
        self.state.setdefault("sent_events", {})[key] = {
            "sent_at": now,
            "event_id": event.get("id") or event.get("event_id"),
            "timestamp": event.get("timestamp") or event.get("ts"),
            "source": event.get("source"),
        }

    def record_send(self, now: float) -> None:
        self.state.setdefault("rate_limit", {}).setdefault("sent_timestamps", []).append(now)
        self.state["last_alert_sent_at"] = now

    def mark_suppressed(self, count: int = 1) -> None:
        self.state["suppressed_count"] = int(self.state.get("suppressed_count", 0)) + count

    def should_send_daily(self, date_str: str) -> bool:
        return self.state.setdefault("daily_report", {}).get("last_sent_date") != date_str

    def mark_daily(self, date_str: str, now: float) -> None:
        self.state.setdefault("daily_report", {})["last_sent_date"] = date_str
        self.state["daily_report"]["last_sent_at"] = now

    def heartbeat(self, error: str | None = None) -> None:
        self.state.setdefault("daemon", {})["last_heartbeat"] = time.time()
        self.state["daemon"]["last_error"] = error

    def _empty(self) -> dict[str, Any]:
        return {
            "version": 1,
            "sent_events": {},
            "rate_limit": {"sent_timestamps": []},
            "daily_report": {},
            "daemon": {},
            "suppressed_count": 0,
        }


class ClawVaultDashboardClient:
    def __init__(self, cfg: dict[str, Any]):
        dashboard = cfg["dashboard"]
        self.base_url = str(dashboard["base_url"]).rstrip("/")
        self.timeout = float(dashboard.get("timeout_seconds", 5))

    def get_scan_history(self, limit: int = 200) -> list[dict[str, Any]]:
        data = self._get_json(f"/api/scan-history?limit={limit}")
        return data if isinstance(data, list) else []

    def get_summary(self) -> dict[str, Any]:
        return self._dict("/api/summary")

    def get_budget(self) -> dict[str, Any]:
        return self._dict("/api/budget")

    def get_monitor_overview(self) -> dict[str, Any]:
        return self._dict("/api/monitor/overview")

    def get_local_scan_history(self, limit: int = 200) -> list[dict[str, Any]]:
        data = self._get_json(f"/api/local-scan/history?limit={limit}")
        return data if isinstance(data, list) else []

    def get_file_monitor_alerts(self, limit: int = 100) -> list[dict[str, Any]]:
        data = self._get_json(f"/api/file-monitor/alerts?limit={limit}")
        return data if isinstance(data, list) else []

    def health_check(self) -> dict[str, Any]:
        try:
            data = self._get_json("/api/health")
            return {"reachable": True, "data": data}
        except Exception as exc:
            return {"reachable": False, "error": str(exc)}

    def _dict(self, path: str) -> dict[str, Any]:
        data = self._get_json(path)
        return data if isinstance(data, dict) else {}

    def _get_json(self, path: str) -> Any:
        url = self.base_url + path
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status >= 400:
                    raise RuntimeError(f"dashboard returned HTTP {resp.status}: {path}")
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"dashboard request failed: {exc}") from exc


class EventClassifier:
    SECRET_PATTERNS = [
        (re.compile(r"sk-[A-Za-z0-9_-]{12,}"), "[REDACTED_API_KEY]"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
        (re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"), "[REDACTED_JWT]"),
        (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "[REDACTED_PRIVATE_KEY]"),
        (re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s:@]+:[^\s@]+@[^\s]+"), "[REDACTED_CREDENTIAL_URL]"),
    ]

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        alerts = cfg["alerts"]
        self.sources = {str(v).lower() for v in alerts.get("sources", [])}
        self.levels = {str(v).lower() for v in alerts.get("threat_levels", [])}
        self.actions = {str(v).lower() for v in alerts.get("actions", [])}
        self.risk_threshold = float(alerts.get("risk_threshold", 7.0))

    def is_high_risk(self, event: dict[str, Any]) -> bool:
        source = str(event.get("source", "")).lower()
        if self.sources and source not in self.sources:
            return False
        level = str(event.get("threat_level") or event.get("severity") or "").lower()
        action = str(event.get("action") or event.get("action_taken") or "").lower()
        risk = self._risk(event)
        return level in self.levels or action in self.actions or risk >= self.risk_threshold

    def dedup_key(self, event: dict[str, Any]) -> str:
        source = str(event.get("source") or "unknown")
        event_id = event.get("id") or event.get("event_id")
        if event_id:
            return f"{source}:{event_id}"
        preview = str(event.get("input_preview") or "")
        payload = {
            "timestamp": event.get("timestamp") or event.get("ts"),
            "source": source,
            "action": event.get("action") or event.get("action_taken"),
            "threat_level": event.get("threat_level") or event.get("severity"),
            "risk": event.get("max_risk_score") or event.get("risk_score"),
            "agent_id": event.get("agent_id"),
            "session_id": event.get("session_id"),
            "detections": event.get("total_detections"),
            "preview_hash": hashlib.sha256(preview.encode("utf-8", errors="ignore")).hexdigest()[:16],
        }
        raw = json.dumps(payload, sort_keys=True, default=str)
        return "hash:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def summarize_event(self, event: dict[str, Any]) -> str:
        alerts = self.cfg["alerts"]
        lines = [
            "ClawVault 高危安全事件",
            "",
            f"级别：{str(event.get('threat_level') or event.get('severity') or 'unknown').upper()}",
            f"来源：{event.get('source', 'unknown')}",
            f"动作：{event.get('action') or event.get('action_taken') or 'unknown'}",
            f"风险分：{self._risk(event):.1f}",
            f"检测数：{event.get('total_detections', self._detection_count(event))}",
            f"Agent：{event.get('agent_id') or event.get('agent_name') or 'unknown'}",
            f"Session：{self._short_session(event.get('session_id'))}",
            f"时间：{event.get('timestamp') or event.get('ts') or 'unknown'}",
        ]
        if alerts.get("include_file_path") and event.get("file_path"):
            lines.append(f"文件：{self.redact(str(event['file_path']))}")
        if alerts.get("include_input_preview") and event.get("input_preview"):
            lines.extend(["", "摘要：", self.redact(str(event["input_preview"]))])
        lines.extend(["", "说明：通知已脱敏。请打开 ClawVault Dashboard 查看完整详情。"])
        return self.redact("\n".join(lines))[: int(alerts.get("max_message_chars", 1200))]

    def redact(self, text: str) -> str:
        redacted = text
        for pattern, repl in self.SECRET_PATTERNS:
            redacted = pattern.sub(repl, redacted)
        return redacted

    def _risk(self, event: dict[str, Any]) -> float:
        try:
            return float(event.get("max_risk_score", event.get("risk_score", 0)) or 0)
        except (TypeError, ValueError):
            return 0.0

    def _detection_count(self, event: dict[str, Any]) -> int:
        return sum(len(event.get(key) or []) for key in ("sensitive", "commands", "injections"))

    def _short_session(self, session_id: Any) -> str:
        if not session_id:
            return "unknown"
        value = str(session_id)
        return value if len(value) <= 16 else value[:8] + "…" + value[-4:]


class RateLimiter:
    def __init__(self, cfg: dict[str, Any], state: StateStore):
        self.cfg = cfg
        self.state = state

    def allow(self, now: float) -> tuple[bool, str | None]:
        stamps = [float(ts) for ts in self.state.state.setdefault("rate_limit", {}).setdefault("sent_timestamps", [])]
        minute = [ts for ts in stamps if now - ts <= 60]
        hour = [ts for ts in stamps if now - ts <= 3600]
        alerts = self.cfg["alerts"]
        if len(minute) >= int(alerts.get("max_alerts_per_minute", 5)):
            return False, "minute_rate_limit"
        if len(hour) >= int(alerts.get("max_alerts_per_hour", 60)):
            return False, "hour_rate_limit"
        return True, None


class OpenClawNotifier:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg

    def send_message(self, message: str) -> dict[str, Any]:
        oc = self.cfg["openclaw"]
        cmd = [
            str(oc.get("command", "openclaw")),
            "agent",
            "--agent",
            str(oc.get("agent_id", "main")),
            "--session-id",
            str(oc.get("session_id", "clawvault-alerts")),
            "--message",
            message,
            "--json",
        ]
        if oc.get("local", True):
            cmd.insert(2, "--local")
        if oc.get("channel"):
            cmd.extend(["--channel", str(oc["channel"])])
        if oc.get("deliver"):
            cmd.append("--deliver")
        if oc.get("reply_channel"):
            cmd.extend(["--reply-channel", str(oc["reply_channel"])])
        if oc.get("reply_to"):
            cmd.extend(["--reply-to", str(oc["reply_to"])])
        try:
            timeout = int(oc.get("timeout_seconds", 180))
            run = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            timed_out = False
            error = None
        except subprocess.TimeoutExpired as exc:
            run = None
            timed_out = True
            error = "openclaw_agent_timeout"
            stdout = _tail(exc.stdout)
            stderr = _tail(exc.stderr)
        except OSError as exc:
            return {"success": False, "error": f"openclaw_agent_failed: {exc}"}

        if not timed_out:
            stdout = run.stdout[-2000:]
            stderr = run.stderr[-2000:]
        delivered = bool(
            (not timed_out and run and run.returncode == 0)
            or "message delivered" in stdout.lower()
            or "delivered" in stdout.lower()
            or "message delivered" in stderr.lower()
            or "delivered" in stderr.lower()
        )
        session_started = timed_out and "embedded run auto-compaction start" in stderr.lower()
        return {
            "success": delivered or session_started,
            "returncode": None if run is None else run.returncode,
            "error": None if delivered or session_started else error,
            "warning": "openclaw_agent_timeout_after_session_start" if session_started and not delivered else None,
            "stdout": stdout,
            "stderr": stderr,
        }

    def send_test(self, message: str | None = None) -> dict[str, Any]:
        msg = message or f"ClawVault OpenClaw Alerts test at {datetime.now().isoformat(timespec='seconds')}"
        return self.send_message(msg)


class DailyReportBuilder:
    def __init__(self, cfg: dict[str, Any], client: ClawVaultDashboardClient, classifier: EventClassifier):
        self.cfg = cfg
        self.client = client
        self.classifier = classifier

    def build(self, date_str: str | None = None) -> str:
        report_date = date_str or date.today().isoformat()
        summary = self.client.get_summary()
        budget = self.client.get_budget()
        overview = self.client.get_monitor_overview()
        events = self.client.get_scan_history(200)
        local_scans = self.client.get_local_scan_history(200)
        file_alerts = self.client.get_file_monitor_alerts(100)
        risky = [event for event in events if self.classifier.is_high_risk(event)]
        by_source = count_by(risky, "source")
        by_action = count_by(risky, "action")
        by_level = count_by(risky, "threat_level")
        max_recent = int(self.cfg["daily_report"].get("max_recent_events", 10))
        top_events = sorted(risky, key=lambda e: float(e.get("max_risk_score") or e.get("risk_score") or 0), reverse=True)[:max_recent]

        lines = [
            f"ClawVault 安全日报 {report_date}",
            "",
            "总体：",
            f"- 总请求：{summary.get('total_requests', overview.get('scan_count', 0))}",
            f"- 拦截：{summary.get('interceptions', overview.get('risk_count', 0))}",
            f"- 阻断：{summary.get('blocks', overview.get('block_count', 0))}",
            f"- 脱敏：{summary.get('sanitizations', overview.get('sanitize_count', 0))}",
            f"- 最高风险分：{float(summary.get('max_risk_score') or max([float(e.get('max_risk_score') or e.get('risk_score') or 0) for e in risky], default=0)):.1f}",
            "",
            "高危事件：",
            f"- 总数：{len(risky)}",
            f"- 按来源：{format_counts(by_source)}",
            f"- 按级别：{format_counts(by_level)}",
            f"- 按动作：{format_counts(by_action)}",
            "",
            "预算：",
            f"- 今日 token：{budget.get('daily_used', budget.get('daily_tokens', 0))} / {budget.get('daily_limit', 'unknown')}",
            f"- 今日费用：{budget.get('cost_usd', summary.get('total_cost_usd', 0))}",
            "",
            "扫描与文件：",
            f"- 本地扫描记录：{len(local_scans)}",
            f"- 文件告警：{len(file_alerts)}",
        ]
        if top_events:
            lines.extend(["", "最近高危事件："])
            for idx, event in enumerate(top_events, start=1):
                lines.append(
                    f"{idx}. [{str(event.get('threat_level', 'unknown')).upper()}] "
                    f"{event.get('source', 'unknown')} {event.get('action', 'unknown')} "
                    f"risk={float(event.get('max_risk_score') or event.get('risk_score') or 0):.1f} "
                    f"detections={event.get('total_detections', 0)}"
                )
        lines.extend(["", "隐私提示：报告已脱敏，未包含原始敏感内容。"])
        return self.classifier.redact("\n".join(lines))[:4000]


class AlertDaemon:
    def __init__(self, cfg: dict[str, Any], config_path: Path):
        self.cfg = cfg
        self.config_path = config_path
        self.state = StateStore(cfg["daemon"]["state_file"])
        self.client = ClawVaultDashboardClient(cfg)
        self.classifier = EventClassifier(cfg)
        self.notifier = OpenClawNotifier(cfg)
        self.rate_limiter = RateLimiter(cfg, self.state)

    def run_once(self, dry_run: bool = False) -> dict[str, Any]:
        now = time.time()
        alerts_cfg = self.cfg["alerts"]
        self.state.cleanup(now, int(alerts_cfg.get("dedup_ttl_seconds", 3600)))
        events = self.client.get_scan_history(int(alerts_cfg.get("scan_history_limit", 200)))
        eligible = [event for event in events if self.classifier.is_high_risk(event)]
        sent: list[dict[str, Any]] = []
        skipped = 0
        suppressed = 0
        for event in eligible:
            key = self.classifier.dedup_key(event)
            if self.state.has_event(key):
                skipped += 1
                continue
            allowed, reason = self.rate_limiter.allow(now)
            if not allowed:
                suppressed += 1
                self.state.mark_suppressed()
                continue
            message = self.classifier.summarize_event(event)
            result = {"success": True, "dry_run": True} if dry_run else self.notifier.send_message(message)
            sent.append({"key": key, "source": event.get("source"), "result": result})
            if result.get("success") and not dry_run:
                self.state.mark_event(key, event, now)
                self.state.record_send(now)
        if not dry_run:
            self.state.heartbeat()
            self.state.save()
        return {
            "success": True,
            "total_events": len(events),
            "eligible_events": len(eligible),
            "sent": sent,
            "sent_count": len(sent),
            "dedup_skipped": skipped,
            "rate_limited": suppressed,
            "dry_run": dry_run,
        }

    def daily_report(self, date_str: str | None = None, dry_run: bool = False, mark_sent: bool = False) -> dict[str, Any]:
        report_date = date_str or date.today().isoformat()
        report = DailyReportBuilder(self.cfg, self.client, self.classifier).build(report_date)
        result = {"success": True, "dry_run": True} if dry_run else self.notifier.send_message(report)
        if result.get("success") and mark_sent and not dry_run:
            self.state.mark_daily(report_date, time.time())
            self.state.save()
        return {"success": bool(result.get("success")), "date": report_date, "report": report if dry_run else None, "delivery": result}

    def maybe_daily_report(self) -> dict[str, Any] | None:
        if not self.cfg["daily_report"].get("enabled", True):
            return None
        hhmm = self.cfg["daily_report"].get("time", "09:00")
        now_dt = datetime.now()
        if now_dt.strftime("%H:%M") < hhmm:
            return None
        today = date.today().isoformat()
        if not self.state.should_send_daily(today):
            return None
        return self.daily_report(today, dry_run=False, mark_sent=True)

    def run_loop(self) -> None:
        interval = int(self.cfg["alerts"].get("poll_interval_seconds", 10))
        while True:
            try:
                if self.cfg["alerts"].get("enabled", True):
                    self.run_once(dry_run=False)
                self.maybe_daily_report()
                self.state.heartbeat()
            except Exception as exc:
                self.state.heartbeat(str(exc))
            finally:
                self.state.save()
            time.sleep(interval)

    def start(self, foreground: bool = False) -> dict[str, Any]:
        pid_file = expand_path(self.cfg["daemon"]["pid_file"])
        if foreground:
            pid_file.parent.mkdir(parents=True, exist_ok=True)
            pid_file.write_text(str(os.getpid()), encoding="utf-8")
            self.run_loop()
            return {"success": True}
        if is_pid_running(read_pid(pid_file)):
            return {"success": False, "error": "daemon_already_running", "pid": read_pid(pid_file)}
        log_file = expand_path(self.cfg["daemon"]["log_file"])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log = open(log_file, "a", encoding="utf-8")
        cmd = [sys.executable, __file__, "start", "--foreground", "--config", str(self.config_path)]
        process = subprocess.Popen(cmd, stdout=log, stderr=log, start_new_session=True)
        pid_file.parent.mkdir(parents=True, exist_ok=True)
        pid_file.write_text(str(process.pid), encoding="utf-8")
        return {"success": True, "pid": process.pid, "log_file": str(log_file)}

    def stop(self, force: bool = False) -> dict[str, Any]:
        pid_file = expand_path(self.cfg["daemon"]["pid_file"])
        pid = read_pid(pid_file)
        if not pid:
            return {"success": True, "running": False, "message": "daemon is not running"}
        if not is_pid_running(pid):
            pid_file.unlink(missing_ok=True)
            return {"success": True, "running": False, "message": "stale pid removed"}
        os.kill(pid, signal.SIGTERM)
        deadline = time.time() + 5
        while time.time() < deadline:
            if not is_pid_running(pid):
                pid_file.unlink(missing_ok=True)
                return {"success": True, "running": False, "stopped_pid": pid}
            time.sleep(0.2)
        if force:
            os.kill(pid, signal.SIGKILL)
            pid_file.unlink(missing_ok=True)
            return {"success": True, "running": False, "killed_pid": pid}
        return {"success": False, "running": True, "pid": pid, "error": "daemon_did_not_stop"}

    def status(self) -> dict[str, Any]:
        pid_file = expand_path(self.cfg["daemon"]["pid_file"])
        pid = read_pid(pid_file)
        health = self.client.health_check()
        state = self.state.state
        return {
            "success": True,
            "running": bool(pid and is_pid_running(pid)),
            "pid": pid,
            "dashboard": health,
            "openclaw": {
                "agent_id": self.cfg["openclaw"].get("agent_id"),
                "session_id": self.cfg["openclaw"].get("session_id"),
            },
            "state": {
                "sent_event_count": len(state.get("sent_events", {})),
                "last_alert_sent_at": state.get("last_alert_sent_at"),
                "last_daily_report": state.get("daily_report", {}).get("last_sent_date"),
                "last_heartbeat": state.get("daemon", {}).get("last_heartbeat"),
                "last_error": state.get("daemon", {}).get("last_error"),
                "suppressed_count": state.get("suppressed_count", 0),
            },
            "config_path": str(self.config_path),
        }


def public_config_summary(cfg: dict[str, Any]) -> dict[str, Any]:
    return {
        "dashboard_url": cfg["dashboard"].get("base_url"),
        "agent_id": cfg["openclaw"].get("agent_id"),
        "session_id": cfg["openclaw"].get("session_id"),
        "deliver": cfg["openclaw"].get("deliver"),
        "channel": cfg["openclaw"].get("channel"),
        "reply_channel": cfg["openclaw"].get("reply_channel"),
        "reply_to": cfg["openclaw"].get("reply_to"),
        "timeout_seconds": cfg["openclaw"].get("timeout_seconds"),
        "risk_threshold": cfg["alerts"].get("risk_threshold"),
        "poll_interval_seconds": cfg["alerts"].get("poll_interval_seconds"),
        "daily_time": cfg["daily_report"].get("time"),
    }


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return counts


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "无"
    return ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))


def read_pid(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def is_pid_running(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _tail(value: str | bytes | None, limit: int = 2000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")[-limit:]
    return value[-limit:]


def load_daemon(config_path: str | None) -> AlertDaemon:
    config_loader = AlertConfig(config_path)
    cfg = config_loader.load()
    return AlertDaemon(cfg, config_loader.path)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--json", action="store_true", help="Output JSON")


def main() -> None:
    parser = argparse.ArgumentParser(description="ClawVault OpenClaw Alerts")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    configure = subparsers.add_parser("configure", help="Configure OpenClaw alert delivery")
    configure.add_argument("--config", help="Config file path")
    configure.add_argument("--dashboard-url", help="ClawVault dashboard URL")
    configure.add_argument("--agent", help="OpenClaw agent id")
    configure.add_argument("--session-id", help="OpenClaw session id")
    configure.add_argument("--risk-threshold", type=float, help="Minimum risk score")
    configure.add_argument("--poll-interval", type=int, help="Realtime polling interval seconds")
    configure.add_argument("--daily-time", help="Daily report time, HH:MM")
    configure.add_argument("--deliver", action="store_true", default=None, help="Ask OpenClaw to deliver the reply through the configured channel")
    configure.add_argument("--no-deliver", action="store_false", dest="deliver", help="Disable OpenClaw delivery")
    configure.add_argument("--channel", help="OpenClaw channel to route through")
    configure.add_argument("--reply-channel", help="OpenClaw reply channel")
    configure.add_argument("--reply-to", help="OpenClaw reply target")
    configure.add_argument("--timeout", type=int, help="OpenClaw agent command timeout seconds")
    configure.add_argument("--json", action="store_true", help="Output JSON")

    start = subparsers.add_parser("start", help="Start background monitoring")
    add_common(start)
    start.add_argument("--foreground", action="store_true", help="Run in foreground")

    stop = subparsers.add_parser("stop", help="Stop background monitoring")
    add_common(stop)
    stop.add_argument("--force", action="store_true", help="Force kill if SIGTERM fails")

    status = subparsers.add_parser("status", help="Show monitoring status")
    add_common(status)

    send_test = subparsers.add_parser("send-test", help="Send a test notification")
    add_common(send_test)
    send_test.add_argument("--message", help="Test message")

    run_once = subparsers.add_parser("run-once", help="Poll ClawVault once")
    add_common(run_once)
    run_once.add_argument("--dry-run", action="store_true", help="Do not send or update state")

    daily = subparsers.add_parser("daily-report", help="Generate and send daily report")
    add_common(daily)
    daily.add_argument("--date", help="Report date YYYY-MM-DD")
    daily.add_argument("--dry-run", action="store_true", help="Print report without sending")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "configure":
            result = AlertConfig(args.config).configure(args)
        else:
            daemon = load_daemon(args.config)
            if args.command == "start":
                result = daemon.start(foreground=args.foreground)
            elif args.command == "stop":
                result = daemon.stop(force=args.force)
            elif args.command == "status":
                result = daemon.status()
            elif args.command == "send-test":
                result = daemon.notifier.send_test(args.message)
            elif args.command == "run-once":
                result = daemon.run_once(dry_run=args.dry_run)
            elif args.command == "daily-report":
                result = daemon.daily_report(date_str=args.date, dry_run=args.dry_run, mark_sent=not args.dry_run)
            else:
                result = {"success": False, "error": f"unknown command: {args.command}"}
    except Exception as exc:
        result = {"success": False, "error": str(exc)}

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print_human(args.command, result)
    sys.exit(0 if result.get("success", False) else 1)


def print_human(command: str, result: dict[str, Any]) -> None:
    if command == "daily-report" and result.get("report"):
        print(result["report"])
        return
    if result.get("success"):
        print("OK")
        for key, value in result.items():
            if key != "success":
                print(f"{key}: {value}")
    else:
        print(f"Error: {result.get('error', 'unknown')}")


if __name__ == "__main__":
    main()
