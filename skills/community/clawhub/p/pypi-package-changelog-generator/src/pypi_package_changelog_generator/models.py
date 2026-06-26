from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class AuthInfo:
    token_provided: bool = False
    provider: str | None = None


@dataclass(slots=True)
class SourceInfo:
    provider: str | None = None
    repository_url: str | None = None
    compare_url: str | None = None


@dataclass(slots=True)
class WarningInfo:
    code: str
    message: str


@dataclass(slots=True)
class ErrorInfo:
    code: str
    message: str
    retryable: bool = False


@dataclass(slots=True)
class TruncationInfo:
    truncated: bool = False
    reason: str | None = None
    omitted_files: int = 0
    omitted_commits: int = 0


@dataclass(slots=True)
class ChangelogResult:
    package: str
    resolved_versions: dict[str, str | None]
    mode: str
    source: SourceInfo = field(default_factory=SourceInfo)
    auth: AuthInfo = field(default_factory=AuthInfo)
    commits: list[dict[str, Any]] = field(default_factory=list)
    reviews: list[dict[str, Any]] = field(default_factory=list)
    file_changes: list[dict[str, Any]] = field(default_factory=list)
    metadata_changes: list[dict[str, Any]] = field(default_factory=list)
    dependency_changes: list[dict[str, Any]] = field(default_factory=list)
    breaking_signals: list[dict[str, Any]] = field(default_factory=list)
    truncation: TruncationInfo = field(default_factory=TruncationInfo)
    warnings: list[WarningInfo] = field(default_factory=list)
    errors: list[ErrorInfo] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class VersionSelection:
    from_version: str
    to_version: str
    range_expression: str | None = None
