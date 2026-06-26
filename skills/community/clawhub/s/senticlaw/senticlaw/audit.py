"""SentiClaw Audit Logger — SQLite-backed event log."""
import sqlite3, json, subprocess
from datetime import datetime, timedelta
from .models import AuditEvent

_IMMEDIATE = {"injection_attempt", "spoofing_attempt", "outbound_blocked"}


class AuditLogger:
    def __init__(self, db_path: str = "senticlaw_audit.db",
                 enabled: bool = True,
                 alert_channel: str = "discord",
                 alert_channel_id: str = ""):
        self.db_path          = db_path
        self.enabled          = enabled
        self.alert_channel    = alert_channel
        self.alert_channel_id = alert_channel_id
        if enabled:
            self._init()

    def _conn(self):
        c = sqlite3.connect(self.db_path, timeout=5)
        c.execute("PRAGMA journal_mode=WAL")
        return c

    def _init(self):
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS audit_events (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp  TEXT NOT NULL,
                session_id TEXT NOT NULL,
                sender_id  TEXT NOT NULL,
                channel    TEXT NOT NULL,
                layer      TEXT NOT NULL,
                event_type TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                details    TEXT NOT NULL
            )""")
            c.execute("CREATE INDEX IF NOT EXISTS idx_ae_session ON audit_events(session_id)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_ae_ts     ON audit_events(timestamp)")

    def log(self, event_type: AuditEvent, session_id: str, sender_id: str,
            channel: str, layer: str, risk_level: str = "safe", details: dict | None = None):
        if not self.enabled:
            return
        with self._conn() as c:
            c.execute(
                "INSERT INTO audit_events(timestamp,session_id,sender_id,channel,layer,event_type,risk_level,details)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (datetime.utcnow().isoformat(), session_id, sender_id, channel, layer,
                 event_type.value, risk_level, json.dumps(details or {})),
            )
        if event_type.value in _IMMEDIATE and self.alert_channel_id:
            self._alert(event_type.value, session_id, sender_id, channel, details or {})

    def _alert(self, event_type: str, session_id: str, sender_id: str,
               channel: str, details: dict):
        ts  = datetime.now().strftime("%H:%M:%S")
        ch  = channel.upper() if channel else "?"
        msg = (
            f"🚨 SentiClaw Alert [{ts}]\n"
            f"{event_type.replace('_', ' ').upper()}\n"
            f"Channel: {ch} | Session: {session_id} | Sender: {sender_id}"
        )

        alert_ch = self.alert_channel.lower()
        target   = self.alert_channel_id

        # Build --to flag based on channel type
        if alert_ch == "discord":
            to_arg = f"channel:{target}"
        elif alert_ch in ("telegram", "whatsapp", "signal"):
            to_arg = target          # chat ID or phone number
        elif alert_ch == "slack":
            to_arg = f"channel:{target}"
        else:
            to_arg = target          # generic fallback

        try:
            subprocess.run(
                ["openclaw", "message", "send",
                 "--channel", alert_ch,
                 "--to", to_arg,
                 "--message", msg],
                capture_output=True, timeout=10,
            )
        except Exception:
            pass

    def query(self, session_id: str, limit: int = 50) -> list[dict]:
        if not self.enabled:
            return []
        with self._conn() as c:
            cur = c.execute(
                "SELECT * FROM audit_events WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def recent_threats(self, hours: int = 24) -> list[dict]:
        if not self.enabled:
            return []
        since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        evts  = ("injection_attempt", "spoofing_attempt", "outbound_blocked", "blocked")
        ph    = ",".join("?" * len(evts))
        with self._conn() as c:
            cur = c.execute(
                f"SELECT * FROM audit_events WHERE timestamp>=? AND event_type IN ({ph}) ORDER BY id DESC",
                (since, *evts),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def stats(self) -> dict:
        if not self.enabled:
            return {}
        with self._conn() as c:
            cur = c.execute("SELECT event_type,COUNT(*) FROM audit_events GROUP BY event_type")
            return {r[0]: r[1] for r in cur.fetchall()}
