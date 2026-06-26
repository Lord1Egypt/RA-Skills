"""Consent Manager — 用户授权管理

管理用户对Agent访问记忆的授权。
"""
from __future__ import annotations

import time
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ConsentRecord:
    """A single consent record."""
    agent_id: str
    user_id: str = "default"
    scopes: list[str] = field(default_factory=lambda: ["personal"])
    max_sensitivity: str = "normal"
    granted_at: float = 0.0
    expires_at: float | None = None  # None = never expires
    revoked: bool = False

    def is_valid(self) -> bool:
        """Check if this consent is still valid."""
        if self.revoked:
            return False
        if self.expires_at and time.time() > self.expires_at:
            return False
        return True


class ConsentManager:
    """Manages user consent for agent memory access.

    Consent records are stored in a JSON file for persistence.
    """

    def __init__(self, consent_file: str | Path | None = None):
        self._consents: dict[str, ConsentRecord] = {}
        self._file = Path(consent_file) if consent_file else None
        if self._file and self._file.exists():
            self._load()

    def grant(self, agent_id: str, scopes: list[str] | None = None,
              max_sensitivity: str = "normal", expires_in: float | None = None,
              user_id: str = "default") -> ConsentRecord:
        """Grant consent for an agent to access memories.

        Args:
            agent_id: The agent requesting access
            scopes: List of memory scopes allowed (e.g., ['personal', 'work'])
            max_sensitivity: Maximum sensitivity level allowed
            expires_in: Seconds until consent expires (None = never)
            user_id: The user granting consent

        Returns:
            The consent record
        """
        now = time.time()
        expires_at = now + expires_in if expires_in else None

        record = ConsentRecord(
            agent_id=agent_id,
            user_id=user_id,
            scopes=scopes or ["personal"],
            max_sensitivity=max_sensitivity,
            granted_at=now,
            expires_at=expires_at,
        )
        self._consents[agent_id] = record
        self._save()
        logger.info("Consent granted: agent=%s scopes=%s sensitivity=%s",
                     agent_id, scopes, max_sensitivity)
        return record

    def revoke(self, agent_id: str) -> bool:
        """Revoke consent for an agent."""
        if agent_id in self._consents:
            self._consents[agent_id].revoked = True
            self._save()
            logger.info("Consent revoked: agent=%s", agent_id)
            return True
        return False

    def check(self, agent_id: str) -> ConsentRecord | None:
        """Check if an agent has valid consent.

        Returns the consent record if valid, None otherwise.
        """
        record = self._consents.get(agent_id)
        if record and record.is_valid():
            return record
        return None

    def list_consents(self, user_id: str = "default") -> list[dict]:
        """List all active consents for a user."""
        results = []
        for record in self._consents.values():
            if record.user_id == user_id and record.is_valid():
                results.append({
                    "agent_id": record.agent_id,
                    "scopes": record.scopes,
                    "max_sensitivity": record.max_sensitivity,
                    "granted_at": record.granted_at,
                    "expires_at": record.expires_at,
                })
        return results

    def _save(self):
        """Persist consents to file."""
        if not self._file:
            return
        data = {}
        for aid, record in self._consents.items():
            data[aid] = {
                "agent_id": record.agent_id,
                "user_id": record.user_id,
                "scopes": record.scopes,
                "max_sensitivity": record.max_sensitivity,
                "granted_at": record.granted_at,
                "expires_at": record.expires_at,
                "revoked": record.revoked,
            }
        try:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error("ConsentManager._save: %s", e)

    def _load(self):
        """Load consents from file."""
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for aid, d in data.items():
                self._consents[aid] = ConsentRecord(
                    agent_id=d["agent_id"],
                    user_id=d.get("user_id", "default"),
                    scopes=d.get("scopes", ["personal"]),
                    max_sensitivity=d.get("max_sensitivity", "normal"),
                    granted_at=d.get("granted_at", 0),
                    expires_at=d.get("expires_at"),
                    revoked=d.get("revoked", False),
                )
        except Exception as e:
            logger.error("ConsentManager._load: %s", e)
