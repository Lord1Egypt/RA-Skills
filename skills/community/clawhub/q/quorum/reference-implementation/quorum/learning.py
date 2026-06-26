# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Learning memory — persistent tracking of recurring failure patterns.

Reads and writes known_issues.json. High-frequency patterns are automatically
promoted to mandatory checks prepended to every critic prompt.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import date
from pathlib import Path

from quorum.models import Finding, Issue, UpdateResult

logger = logging.getLogger(__name__)


def _make_pattern_id(description: str, critic: str) -> str:
    """Generate a stable 12-char hex ID from description + critic name."""
    key = f"{description.lower().strip()}|{critic.lower().strip()}"
    return "P-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:10]


class LearningMemory:
    """
    Persistent learning memory backed by known_issues.json.

    Default path: ~/.quorum/known_issues.json
    If ./known_issues.json exists in the working directory it is preferred,
    allowing project-local overrides without touching the user's global store.
    """

    DEFAULT_PATH = Path.home() / ".quorum" / "known_issues.json"
    PROMOTION_THRESHOLD = 3

    def __init__(self, path: Path | None = None):
        if path is not None:
            self._path = path
        else:
            local = Path("known_issues.json")
            self._path = local if local.exists() else self.DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> list[Issue]:
        """Load issues from JSON file. Returns empty list if file does not exist."""
        if not self._path.exists():
            return []
        try:
            raw = self._path.read_text(encoding="utf-8")
            data = json.loads(raw)
            return [Issue(**item) for item in data]
        except Exception as e:
            logger.warning("Failed to load %s: %s", self._path, e)
            return []

    def save(self, issues: list[Issue]) -> None:
        """Write issues to JSON using atomic tmp+rename to prevent corruption."""
        tmp = self._path.with_suffix(".tmp")
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            data = [issue.to_dict() for issue in issues]
            tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
            tmp.replace(self._path)
            logger.debug("Saved %d known issues to %s", len(issues), self._path)
        except Exception as e:
            tmp.unlink(missing_ok=True)  # Clean up partial write on failure
            logger.warning("Failed to save learning memory to %s: %s", self._path, e)

    def update_from_findings(
        self,
        findings: list[Finding],
        domain: str,
        threshold: int = PROMOTION_THRESHOLD,
    ) -> UpdateResult:
        """
        Update known issues from a run's findings.

        - Existing patterns: increment frequency, update last_seen
        - New patterns: create Issue with frequency=1, first_seen=today
        - Promotes patterns at/above threshold to mandatory

        Returns UpdateResult with counts.
        """
        existing = self.load()
        index: dict[str, Issue] = {issue.pattern_id: issue for issue in existing}
        today = date.today().isoformat()
        new_count = 0
        updated_count = 0

        for finding in findings:
            pid = _make_pattern_id(finding.description, finding.critic)
            if pid in index:
                index[pid].frequency += 1
                index[pid].last_seen = today
                updated_count += 1
            else:
                index[pid] = Issue(
                    pattern_id=pid,
                    description=finding.description,
                    domain=domain,
                    severity=finding.severity,
                    frequency=1,
                    first_seen=today,
                    last_seen=today,
                    mandatory=False,
                )
                new_count += 1

        updated_issues = list(index.values())
        promoted_count = 0
        for issue in updated_issues:
            if not issue.mandatory and issue.frequency >= threshold:
                issue.mandatory = True
                promoted_count += 1
                logger.info(
                    "Promoted pattern '%s' to mandatory (frequency=%d): %s",
                    issue.pattern_id, issue.frequency, issue.description[:60],
                )

        self.save(updated_issues)
        logger.info(
            "Learning memory updated: %d new, %d updated, %d promoted, %d total",
            new_count, updated_count, promoted_count, len(updated_issues),
        )
        return UpdateResult(
            new_patterns=new_count,
            updated_patterns=updated_count,
            promoted_patterns=promoted_count,
            total_known=len(updated_issues),
        )

    def get_mandatory(self) -> list[Issue]:
        """Return all issues where mandatory=True."""
        return [i for i in self.load() if i.mandatory]

    def promote(self, threshold: int = PROMOTION_THRESHOLD) -> int:
        """
        Set mandatory=True for all issues with frequency >= threshold.

        Returns count of newly promoted issues.
        """
        issues = self.load()
        promoted = 0
        for issue in issues:
            if not issue.mandatory and issue.frequency >= threshold:
                issue.mandatory = True
                promoted += 1
        if promoted:
            self.save(issues)
        return promoted

    def to_critic_context(self) -> str:
        """
        Format mandatory issues as brief instructions for critic system prompts.

        Returns empty string if no mandatory issues exist.
        """
        mandatory = self.get_mandatory()
        if not mandatory:
            return ""
        lines = ["## Known Recurring Issues (Always Check For These)"]
        for issue in mandatory:
            lines.append(
                f"- Known recurring issue: {issue.description}. "
                "Always check for this pattern."
            )
        return "\n".join(lines)
