"""
enterprise/permission_matrix.py — Three-dimensional permission control.

Role × Department × Sensitivity → Action permissions.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# Standard roles
ROLES = ["admin", "manager", "member", "intern", "guest"]
# Standard departments
DEPARTMENTS = ["engineering", "sales", "marketing", "hr", "finance", "executive"]
# Sensitivity levels (mapped to visibility)
SENSITIVITIES = ["public", "internal", "confidential", "restricted"]
# Actions
ACTIONS = ["read", "read_summary", "write", "delete", "share", "export"]


@dataclass
class PermissionEntry:
    """A single permission entry in the matrix."""
    role: str
    department: str
    sensitivity: str
    allowed_actions: list[str] = field(default_factory=list)


class PermissionMatrix:
    """Three-dimensional permission control: Role × Department × Sensitivity.

    Default policy: deny all. Explicit grants only.
    """

    def __init__(self, config_path: str = ""):
        self._matrix: dict[str, PermissionEntry] = {}
        self._config_path = config_path
        if config_path and os.path.exists(config_path):
            self.load(config_path)
        else:
            self._init_defaults()

    def _init_defaults(self):
        """Initialize with sensible defaults."""
        # Admin: full access
        for dept in DEPARTMENTS:
            for sens in SENSITIVITIES:
                self._set("admin", dept, sens, ACTIONS)
        # Manager: full in own dept, read in others
        for dept in DEPARTMENTS:
            for sens in SENSITIVITIES:
                if sens == "restricted":
                    self._set("manager", dept, sens, ["read_summary"])
                else:
                    self._set("manager", dept, sens, ["read", "read_summary", "write", "share"])
        # Member: read internal and below
        for dept in DEPARTMENTS:
            for sens in SENSITIVITIES:
                if sens in ("public", "internal"):
                    self._set("member", dept, sens, ["read", "write"])
                elif sens == "confidential":
                    self._set("member", dept, sens, ["read_summary"])
                # restricted: no access
        # Intern: read public only
        for dept in DEPARTMENTS:
            self._set("intern", dept, "public", ["read"])
            self._set("intern", dept, "internal", ["read_summary"])
        # Guest: read public only
        for dept in DEPARTMENTS:
            self._set("guest", dept, "public", ["read"])

    def _key(self, role: str, dept: str, sens: str) -> str:
        return f"{role}:{dept}:{sens}"

    def _set(self, role: str, dept: str, sens: str, actions: list[str]):
        key = self._key(role, dept, sens)
        self._matrix[key] = PermissionEntry(role=role, department=dept,
                                             sensitivity=sens,
                                             allowed_actions=actions)

    def check_access(self, role: str, department: str,
                     sensitivity: str, action: str) -> bool:
        """Check if a role/department/sensitivity allows an action."""
        key = self._key(role, department, sensitivity)
        entry = self._matrix.get(key)
        if entry:
            return action in entry.allowed_actions
        return False

    def get_allowed_actions(self, role: str, department: str,
                            sensitivity: str) -> list[str]:
        """Get all allowed actions for a role/department/sensitivity."""
        key = self._key(role, department, sensitivity)
        entry = self._matrix.get(key)
        return entry.allowed_actions if entry else []

    def save(self, path: str = ""):
        """Save matrix to JSON."""
        path = path or self._config_path
        if not path:
            return
        data = {
            key: {"role": e.role, "department": e.department,
                  "sensitivity": e.sensitivity, "allowed_actions": e.allowed_actions}
            for key, e in self._matrix.items()
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, path: str):
        """Load matrix from JSON."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._matrix.clear()
        for key, entry_data in data.items():
            self._matrix[key] = PermissionEntry(**entry_data)
