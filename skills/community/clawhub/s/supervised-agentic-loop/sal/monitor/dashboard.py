"""Dashboard data functions for Command Center integration.

No standalone HTTP server — provides data functions that
Command Center's Flask app calls. (🟡 Dr. Neuron: specified)
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sal.monitor.heartbeat import MonitorHeartbeat


def _default_state_dir() -> str:
    import os
    return os.environ.get("MONITOR_STATE_DIR", ".state")


def get_monitor_stats(state_dir: Optional[str] = None) -> dict:
    """Get monitor overview stats.

    Returns:
        {
            total_sessions_today: int,
            alerts_by_severity: {LOW: n, MEDIUM: n, HIGH: n, CRITICAL: n},
            last_scan: ISO timestamp or null,
            monitor_alive: bool,
        }
    """
    sd = Path(state_dir or _default_state_dir())

    # Count today's tool call entries
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_path = sd / f"tool-call-log-{today}.jsonl"
    sessions_today: set[str] = set()
    if log_path.exists():
        with open(log_path) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    sid = entry.get("session_id", "")
                    if sid:
                        sessions_today.add(sid)
                except json.JSONDecodeError:
                    continue

    # Count alerts by severity
    alerts = _read_alerts(sd)
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for alert in alerts:
        sev = alert.get("severity", "LOW")
        if sev in severity_counts:
            severity_counts[sev] += 1

    # Monitor heartbeat
    hb = MonitorHeartbeat(state_dir=str(sd))
    alive_status = hb.check_alive()

    return {
        "total_sessions_today": len(sessions_today),
        "alerts_by_severity": severity_counts,
        "last_scan": alive_status.get("last_beat"),
        "monitor_alive": alive_status.get("alive", False),
    }


def get_recent_alerts(
    state_dir: Optional[str] = None, limit: int = 10
) -> list[dict]:
    """Get most recent alerts.

    Returns list of:
        {ts, agent_id, behavior, severity, evidence, action_taken}
    """
    sd = Path(state_dir or _default_state_dir())
    alerts = _read_alerts(sd)
    return alerts[-limit:]


def get_agent_risk_profile(
    agent_id: str, state_dir: Optional[str] = None
) -> dict:
    """Get risk profile for a specific agent.

    Returns:
        {agent_id, total_alerts, alerts_by_severity, risk_level, last_alert}
    """
    sd = Path(state_dir or _default_state_dir())
    alerts = _read_alerts(sd)

    agent_alerts = [a for a in alerts if a.get("agent_id") == agent_id]
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for a in agent_alerts:
        sev = a.get("severity", "LOW")
        if sev in severity_counts:
            severity_counts[sev] += 1

    # Determine risk level
    if severity_counts["CRITICAL"] > 0:
        risk_level = "critical"
    elif severity_counts["HIGH"] > 2:
        risk_level = "high"
    elif severity_counts["MEDIUM"] > 5:
        risk_level = "elevated"
    else:
        risk_level = "normal"

    return {
        "agent_id": agent_id,
        "total_alerts": len(agent_alerts),
        "alerts_by_severity": severity_counts,
        "risk_level": risk_level,
        "last_alert": agent_alerts[-1]["ts"] if agent_alerts else None,
    }


def log_alert(
    state_dir: str,
    agent_id: str,
    behavior_id: str,
    behavior_name: str,
    severity: str,
    evidence: str,
    action_taken: str = "logged",
    session_id: str = "",
) -> None:
    """Append an alert to monitor-alerts.jsonl."""
    sd = Path(state_dir)
    sd.mkdir(parents=True, exist_ok=True)
    alert_path = sd / "monitor-alerts.jsonl"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "session_id": session_id,
        "behavior": behavior_id,
        "behavior_name": behavior_name,
        "severity": severity,
        "evidence": evidence[:500],
        "action_taken": action_taken,
    }

    with open(alert_path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _read_alerts(state_dir: Path) -> list[dict]:
    """Read all alerts from JSONL."""
    alert_path = state_dir / "monitor-alerts.jsonl"
    if not alert_path.exists():
        return []

    alerts = []
    with open(alert_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                alerts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return alerts
