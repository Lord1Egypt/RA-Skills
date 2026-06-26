"""SentiClaw — shared data models."""
from dataclasses import dataclass, field
from enum import Enum


class TrustLevel(Enum):
    OWNER   = "owner"
    TRUSTED = "trusted"
    UNKNOWN = "unknown"
    BLOCKED = "blocked"
    SPOOFED = "spoofed"


class RiskLevel(Enum):
    SAFE     = "safe"
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class AuditEvent(Enum):
    ALLOWED           = "allowed"
    BLOCKED           = "blocked"
    FLAGGED           = "flagged"
    REDACTED          = "redacted"
    RATE_LIMITED      = "rate_limited"
    LOOP_DETECTED     = "loop_detected"
    INJECTION_ATTEMPT = "injection_attempt"
    SPOOFING_ATTEMPT  = "spoofing_attempt"
    OUTBOUND_BLOCKED  = "outbound_blocked"


@dataclass
class InboundMessage:
    text:       str
    sender_id:  str = ""
    channel:    str = ""
    session_id: str = ""
    metadata:   dict = field(default_factory=dict)


@dataclass
class LayerResult:
    layer:         str
    passed:        bool
    risk_level:    RiskLevel = RiskLevel.SAFE
    details:       dict      = field(default_factory=dict)
    block_message: str       = ""


@dataclass
class PipelineResult:
    allowed:       bool
    text:          str
    session_id:    str              = ""
    sender_id:     str              = ""
    channel:       str              = ""
    block_message: str              = ""
    blocked_by:    str              = ""
    risk_level:    RiskLevel        = RiskLevel.SAFE
    layer_results: list[LayerResult] = field(default_factory=list)


@dataclass
class OutboundResult:
    allowed:        bool
    response:       str
    blocked_reason: str = ""
