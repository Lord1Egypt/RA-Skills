"""Compliance framework — extensible compliance checking system."""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"
    NOT_CHECKED = "not_checked"


@dataclass
class ComplianceCheck:
    check_id: str
    name: str
    description: str
    category: str
    status: ComplianceStatus = ComplianceStatus.NOT_CHECKED
    details: str = ""
    remediation: str = ""
    checked_at: float = 0.0


@dataclass
class ComplianceReport:
    framework: str
    version: str
    checks: list[ComplianceCheck] = field(default_factory=list)
    generated_at: float = 0.0

    def __post_init__(self):
        if self.generated_at == 0.0:
            self.generated_at = time.time()

    @property
    def pass_count(self) -> int:
        return sum(1 for c in self.checks if c.status == ComplianceStatus.PASS)

    @property
    def fail_count(self) -> int:
        return sum(1 for c in self.checks if c.status == ComplianceStatus.FAIL)

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.checks if c.status == ComplianceStatus.WARNING)

    @property
    def compliance_score(self) -> float:
        total = len([c for c in self.checks if c.status != ComplianceStatus.NOT_APPLICABLE])
        if total == 0:
            return 100.0
        passed = self.pass_count
        warned = self.warning_count * 0.5
        return round((passed + warned) / total * 100, 1)

    def to_dict(self) -> dict:
        return {
            "framework": self.framework,
            "version": self.version,
            "compliance_score": self.compliance_score,
            "pass": self.pass_count,
            "fail": self.fail_count,
            "warning": self.warning_count,
            "total_checks": len(self.checks),
            "generated_at": self.generated_at,
            "checks": [
                {
                    "id": c.check_id,
                    "name": c.name,
                    "category": c.category,
                    "status": c.status.value,
                    "details": c.details,
                    "remediation": c.remediation,
                }
                for c in self.checks
            ],
        }


class ComplianceFramework:
    def __init__(self):
        self._checkers: dict[str, Callable] = {}
        self._reports: list[ComplianceReport] = []

    def register_checker(self, name: str, checker: Callable):
        self._checkers[name] = checker

    def run_check(self, framework_name: str, store=None, config=None) -> ComplianceReport:
        checker = self._checkers.get(framework_name)
        if checker is None:
            raise ValueError(f"Unknown compliance framework: {framework_name}")
        report = checker(store=store, config=config)
        self._reports.append(report)
        return report

    def run_all_checks(self, store=None, config=None) -> list[ComplianceReport]:
        reports = []
        for name in self._checkers:
            try:
                report = self.run_check(name, store=store, config=config)
                reports.append(report)
            except Exception as e:
                logger.error("Compliance check failed for %s: %s", name, e)
        return reports

    def get_latest_report(self, framework_name: str) -> Optional[ComplianceReport]:
        for report in reversed(self._reports):
            if report.framework == framework_name:
                return report
        return None
