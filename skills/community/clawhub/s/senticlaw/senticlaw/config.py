"""SentiClawConfig — all settings in one place."""
from dataclasses import dataclass, field
import json, os


@dataclass
class SentiClawConfig:
    # Layer toggles
    layer_identity:   bool = True
    layer_sanitizer:  bool = True
    layer_outbound:   bool = True
    layer_redactor:   bool = True
    layer_governance: bool = True
    layer_access:     bool = True

    # Layer 0 — Identity
    owner_ids:            dict = field(default_factory=dict)   # {channel: [ids]}
    trusted_senders:      dict = field(default_factory=dict)
    block_unknown_senders: bool = False

    # Layer 1 — Sanitizer
    custom_injection_patterns: list = field(default_factory=list)

    # Layer 2 — Outbound Gate
    outbound_block_api_keys:    bool = True
    outbound_block_file_paths:  bool = True
    outbound_block_internal_ips: bool = True

    # Layer 3 — Redactor
    redact_pii:      bool = True
    redact_secrets:  bool = True
    redaction_mode:  str  = "mask"   # mask | remove | tokenize

    # Layer 4 — Governance
    spend_cap_daily_usd:     float = 10.0
    max_messages_per_hour:   int   = 100
    max_messages_per_minute: int   = 20
    loop_threshold:          int   = 3
    loop_window_seconds:     int   = 60
    max_tool_calls_per_turn: int   = 10

    # Layer 5 — Access
    allowed_dirs:       list = field(default_factory=lambda: ["/tmp", os.path.expanduser("~")])
    allowed_tools:      list = field(default_factory=list)
    block_private_urls: bool = True

    # Alerts — set alert_channel to your platform, alert_channel_id to your target
    # discord:  channel ID (e.g. "1234567890")
    # telegram: chat ID   (e.g. "8496230457")
    # slack:    channel ID (e.g. "C12345678")
    # whatsapp: phone number (e.g. "+12035551234")
    alert_channel:    str = "discord"   # discord | telegram | slack | whatsapp
    alert_channel_id: str = ""          # target ID/number for alerts

    # Audit
    audit_db_path: str  = "senticlaw_audit.db"
    audit_enabled: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> "SentiClawConfig":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})

    @classmethod
    def from_json(cls, path: str) -> "SentiClawConfig":
        with open(path) as f:
            return cls.from_dict(json.load(f))
