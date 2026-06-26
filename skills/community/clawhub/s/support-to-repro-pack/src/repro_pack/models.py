"""Data models for repro-pack pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PIIType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    IP_ADDRESS = "ip_address"
    AUTH_TOKEN = "auth_token"
    API_KEY = "api_key"
    CREDIT_CARD = "credit_card"
    SSN = "ssn"
    ID_CARD = "id_card"
    AWS_KEY = "aws_key"
    PRIVATE_KEY = "private_key"
    PASSWORD = "password"
    JWT = "jwt"
    URL_WITH_CREDENTIALS = "url_with_credentials"
    COOKIE = "cookie"
    UUID = "uuid"
    CUSTOMER_ID = "customer_id"
    ORDER_ID = "order_id"


class Severity(str, Enum):
    P0 = "P0"  # Service down
    P1 = "P1"  # Critical feature broken, no workaround
    P2 = "P2"  # Core feature broken, workaround exists
    P3 = "P3"  # Minor issue
    P4 = "P4"  # Cosmetic / enhancement


class LogFormat(str, Enum):
    JSON = "json"
    SYSLOG = "syslog"
    PLAIN = "plain"
    UNKNOWN = "unknown"


@dataclass
class PIIMatch:
    pii_type: PIIType
    line_number: int
    start: int
    end: int
    original_snippet: str  # masked partial, e.g. "j***@example.com"
    placeholder: str  # e.g. "[EMAIL_1]"


@dataclass
class RedactionReport:
    total_found: int
    replacements: list[PIIMatch] = field(default_factory=list)
    regex_matched: int = 0
    lines_processed: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_pii_found": self.total_found,
            "replacements": [
                {
                    "type": m.pii_type.value,
                    "line": m.line_number,
                    "original_pattern": m.original_snippet,
                    "replaced_with": m.placeholder,
                }
                for m in self.replacements
            ],
            "stats": {
                "regex_matched": self.regex_matched,
                "lines_processed": self.lines_processed,
            },
        }


@dataclass
class LogEntry:
    timestamp: str | None = None
    level: str | None = None
    message: str = ""
    source: str | None = None
    raw: str = ""
    line_number: int = 0


@dataclass
class StackFrame:
    file_path: str
    line_number: int | None = None
    function_name: str | None = None
    code_context: str | None = None


@dataclass
class StackTrace:
    language: str
    exception_type: str
    exception_message: str
    frames: list[StackFrame] = field(default_factory=list)
    raw: str = ""


@dataclass
class EnvironmentFacts:
    os: str | None = None
    browser: str | None = None
    browser_version: str | None = None
    app_version: str | None = None
    build_number: str | None = None
    environment: str | None = None  # prod / staging / dev
    region: str | None = None
    user_role: str | None = None
    feature_flags: dict[str, str] = field(default_factory=dict)
    error_codes: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    extra: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if v is not None and v != [] and v != {}:
                d[k] = v
        return d


@dataclass
class TimelineEvent:
    timestamp: str
    event: str
    source: str | None = None
    level: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "timestamp": self.timestamp,
            "event": self.event,
            "source": self.source,
            "level": self.level,
        }


@dataclass
class MissingField:
    field_name: str
    importance: str  # critical / important / nice_to_have
    question: str  # suggested question to ask
