"""Base protocol and data types for pattern checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, runtime_checkable


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CheckResult:
    file: str
    line: int
    col: int
    severity: Severity
    code: str
    message: str
    check_name: str
    context: str = ""

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.col}: {self.severity.value.upper()} [{self.code}] {self.message}"


@runtime_checkable
class PatternCheck(Protocol):
    """Protocol that all pattern checks must satisfy."""

    name: str
    enabled: bool

    def check(self, file_path: str, source: str, config: dict) -> list[CheckResult]:
        """Run check against file source, return list of findings."""
        ...
