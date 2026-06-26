"""Feature flag system with percentage rollout, tenant targeting, A/B testing, and SQLite persistence."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import sqlite3
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class RolloutStrategy(Enum):
    ALL = "all"
    NONE = "none"
    PERCENTAGE = "percentage"
    TENANT_LIST = "tenant_list"
    GRADUAL = "gradual"


@dataclass
class FeatureFlag:
    name: str
    description: str = ""
    enabled: bool = False
    strategy: RolloutStrategy = RolloutStrategy.NONE
    percentage: float = 0.0
    tenant_allowlist: list[str] = field(default_factory=list)
    tenant_blocklist: list[str] = field(default_factory=list)
    variants: dict[str, Any] = field(default_factory=dict)
    default_variant: str = "control"
    created_at: float = 0.0
    updated_at: float = 0.0

    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.updated_at == 0.0:
            self.updated_at = self.created_at

    def is_active_for(self, tenant_id: str = None, user_id: str = None) -> tuple[bool, str]:
        if not self.enabled:
            return False, self.default_variant

        if self.strategy == RolloutStrategy.ALL:
            return True, self._get_variant(tenant_id)

        if self.strategy == RolloutStrategy.NONE:
            return False, self.default_variant

        if self.strategy == RolloutStrategy.TENANT_LIST:
            if tenant_id and tenant_id in self.tenant_blocklist:
                return False, self.default_variant
            if tenant_id and tenant_id in self.tenant_allowlist:
                return True, self._get_variant(tenant_id)
            return False, self.default_variant

        if self.strategy == RolloutStrategy.PERCENTAGE:
            bucket = self._hash_to_bucket(tenant_id or user_id or "anonymous")
            if bucket < self.percentage:
                return True, self._get_variant(tenant_id)
            return False, self.default_variant

        if self.strategy == RolloutStrategy.GRADUAL:
            elapsed_hours = (time.time() - self.updated_at) / 3600
            current_pct = min(100.0, self.percentage + elapsed_hours * 2)
            bucket = self._hash_to_bucket(tenant_id or user_id or "anonymous")
            if bucket < current_pct:
                return True, self._get_variant(tenant_id)
            return False, self.default_variant

        return False, self.default_variant

    def _hash_to_bucket(self, key: str) -> float:
        h = int(hashlib.md5(f"{self.name}:{key}".encode()).hexdigest(), 16)
        return (h % 10000) / 100.0

    def _get_variant(self, tenant_id: str = None) -> str:
        if not self.variants:
            return "enabled"
        if tenant_id and tenant_id in self.variants:
            return self.variants[tenant_id]
        return self.default_variant

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "strategy": self.strategy.value,
            "percentage": self.percentage,
            "tenant_allowlist": self.tenant_allowlist,
            "tenant_blocklist": self.tenant_blocklist,
            "variants": self.variants,
            "description": self.description,
            "default_variant": self.default_variant,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class FeatureFlagManager:
    def __init__(self, config_path: str = None):
        self._flags: dict[str, FeatureFlag] = {}
        self._config_path = config_path or os.environ.get(
            "AGENT_MEMORY_FEATURE_FLAGS_CONFIG", ""
        )
        self._change_listeners: list[Callable] = []
        self._db_path: str | None = None

        # 1. Load from SQLite first (most persistent source)
        self._init_db()
        self._load_from_db()

        # 2. Overlay from JSON config file
        if self._config_path:
            self.load_from_file(self._config_path)

        # 3. Overlay from env vars (highest priority for initial load)
        self._load_from_env()

    # ── SQLite persistence ──────────────────────────────────────────

    def _init_db(self):
        db_path = os.environ.get("AGENT_MEMORY_FLAGS_DB", "")
        if not db_path:
            data_dir = os.environ.get("AGENT_MEMORY_DATA_DIR", os.path.expanduser("~/.agent_memory"))
            db_path = os.path.join(data_dir, "feature_flags.db")
        self._db_path = db_path

        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            conn = sqlite3.connect(db_path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS feature_flags "
                "(name TEXT PRIMARY KEY, config TEXT, updated_at REAL)"
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning("Failed to initialize feature flags DB at %s: %s", db_path, e)
            self._db_path = None

    def _load_from_db(self):
        if not self._db_path:
            return
        try:
            conn = sqlite3.connect(self._db_path)
            rows = conn.execute("SELECT name, config, updated_at FROM feature_flags").fetchall()
            conn.close()
            for name, config_json, _updated_at in rows:
                try:
                    config = json.loads(config_json)
                    # Use _set_flag_no_persist to avoid writing back to DB during load
                    self._set_flag_no_persist(
                        name,
                        enabled=config.get("enabled", False),
                        description=config.get("description", ""),
                        strategy=RolloutStrategy(config.get("strategy", "none")),
                        percentage=config.get("percentage", 0),
                        tenant_allowlist=config.get("tenant_allowlist", []),
                        tenant_blocklist=config.get("tenant_blocklist", []),
                        variants=config.get("variants", {}),
                        default_variant=config.get("default_variant", "control"),
                        created_at=config.get("created_at", 0),
                        updated_at=config.get("updated_at", 0),
                    )
                except Exception as e:
                    logger.warning("Failed to load flag '%s' from DB: %s", name, e)
        except Exception as e:
            logger.warning("Failed to load feature flags from DB: %s", e)

    def _save_flag_to_db(self, flag: FeatureFlag):
        if not self._db_path:
            return
        try:
            conn = sqlite3.connect(self._db_path)
            config_json = json.dumps(flag.to_dict(), ensure_ascii=False)
            conn.execute(
                "INSERT OR REPLACE INTO feature_flags (name, config, updated_at) VALUES (?, ?, ?)",
                (flag.name, config_json, flag.updated_at),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning("Failed to persist flag '%s' to DB: %s", flag.name, e)

    # ── Change listeners ────────────────────────────────────────────

    def add_change_listener(self, callback: Callable):
        """Register a callback invoked on every flag change.

        Signature: callback(flag_name: str, action: str, flag: FeatureFlag)
        action is one of: "create", "update", "delete"
        """
        self._change_listeners.append(callback)

    def _notify_listeners(self, flag_name: str, action: str, flag: FeatureFlag):
        for cb in self._change_listeners:
            try:
                cb(flag_name, action, flag)
            except Exception as e:
                logger.warning("Change listener error for '%s': %s", flag_name, e)

    # ── Flag version ────────────────────────────────────────────────

    def get_flag_version(self, name: str) -> float | None:
        """Return the updated_at timestamp for consistency checking across instances."""
        flag = self._flags.get(name)
        return flag.updated_at if flag else None

    # ── Core operations ─────────────────────────────────────────────

    def _load_from_env(self):
        prefix = "AGENT_MEMORY_FEATURE_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                flag_name = key[len(prefix):].lower()
                self._set_flag_no_persist(flag_name, enabled=value.lower() in ("true", "1", "yes"))
                # Also persist env-loaded flags so other instances can see them
                flag = self._flags.get(flag_name)
                if flag:
                    self._save_flag_to_db(flag)

    def _set_flag_no_persist(self, name: str, enabled: bool = True, **kwargs) -> FeatureFlag:
        """Internal set that skips DB persistence (used during loading)."""
        if name not in self._flags:
            if "strategy" not in kwargs:
                kwargs["strategy"] = RolloutStrategy.ALL if enabled else RolloutStrategy.NONE
            flag = FeatureFlag(name=name, enabled=enabled, **kwargs)
            self._flags[name] = flag
        else:
            self._flags[name].enabled = enabled
            self._flags[name].updated_at = time.time()
            for k, v in kwargs.items():
                if hasattr(self._flags[name], k):
                    setattr(self._flags[name], k, v)
        return self._flags[name]

    def create_flag(self, name: str, description: str = "", **kwargs) -> FeatureFlag:
        if name in self._flags:
            raise ValueError(f"Flag '{name}' already exists")
        flag = FeatureFlag(name=name, description=description, **kwargs)
        self._flags[name] = flag
        self._save_flag_to_db(flag)
        self._notify_listeners(name, "create", flag)
        logger.info("Created feature flag: %s", name)
        return flag

    def set_flag(self, name: str, enabled: bool = True, **kwargs) -> FeatureFlag:
        action = "create" if name not in self._flags else "update"
        flag = self._set_flag_no_persist(name, enabled=enabled, **kwargs)
        self._save_flag_to_db(flag)
        self._notify_listeners(name, action, flag)
        return flag

    def get_flag(self, name: str) -> Optional[FeatureFlag]:
        return self._flags.get(name)

    def is_enabled(self, name: str, tenant_id: str = None, user_id: str = None) -> bool:
        flag = self._flags.get(name)
        if flag is None:
            return False
        active, _ = flag.is_active_for(tenant_id, user_id)
        return active

    def get_variant(self, name: str, tenant_id: str = None, user_id: str = None) -> str:
        flag = self._flags.get(name)
        if flag is None:
            return "control"
        _, variant = flag.is_active_for(tenant_id, user_id)
        return variant

    def rollout_to_percentage(self, name: str, percentage: float) -> FeatureFlag:
        flag = self._flags.get(name)
        if flag is None:
            raise ValueError(f"Flag '{name}' not found")
        flag.strategy = RolloutStrategy.PERCENTAGE
        flag.percentage = max(0.0, min(100.0, percentage))
        flag.updated_at = time.time()
        self._save_flag_to_db(flag)
        self._notify_listeners(name, "update", flag)
        logger.info("Rollout %s to %.1f%%", name, flag.percentage)
        return flag

    def gradual_rollout(self, name: str, start_percentage: float = 1.0) -> FeatureFlag:
        flag = self._flags.get(name)
        if flag is None:
            raise ValueError(f"Flag '{name}' not found")
        flag.enabled = True
        flag.strategy = RolloutStrategy.GRADUAL
        flag.percentage = start_percentage
        flag.updated_at = time.time()
        self._save_flag_to_db(flag)
        self._notify_listeners(name, "update", flag)
        logger.info("Gradual rollout %s starting at %.1f%%", name, start_percentage)
        return flag

    def add_tenant_to_rollout(self, name: str, tenant_id: str) -> FeatureFlag:
        flag = self._flags.get(name)
        if flag is None:
            raise ValueError(f"Flag '{name}' not found")
        if flag.strategy not in (RolloutStrategy.TENANT_LIST, RolloutStrategy.PERCENTAGE):
            flag.strategy = RolloutStrategy.TENANT_LIST
        if tenant_id not in flag.tenant_allowlist:
            flag.tenant_allowlist.append(tenant_id)
        flag.updated_at = time.time()
        self._save_flag_to_db(flag)
        self._notify_listeners(name, "update", flag)
        return flag

    def block_tenant(self, name: str, tenant_id: str) -> FeatureFlag:
        flag = self._flags.get(name)
        if flag is None:
            raise ValueError(f"Flag '{name}' not found")
        if tenant_id not in flag.tenant_blocklist:
            flag.tenant_blocklist.append(tenant_id)
        flag.updated_at = time.time()
        self._save_flag_to_db(flag)
        self._notify_listeners(name, "update", flag)
        return flag

    def list_flags(self) -> list[dict]:
        return [
            {
                "name": f.name,
                "enabled": f.enabled,
                "strategy": f.strategy.value,
                "percentage": f.percentage,
                "tenant_allowlist": f.tenant_allowlist,
                "updated_at": f.updated_at,
            }
            for f in self._flags.values()
        ]

    def save_to_file(self, path: str = None):
        path = path or self._config_path
        if not path:
            return
        data = {
            name: {
                "enabled": f.enabled,
                "strategy": f.strategy.value,
                "percentage": f.percentage,
                "tenant_allowlist": f.tenant_allowlist,
                "tenant_blocklist": f.tenant_blocklist,
                "variants": f.variants,
                "description": f.description,
            }
            for name, f in self._flags.items()
        }
        with open(path, "w") as fp:
            json.dump(data, fp, indent=2)

    def load_from_file(self, path: str):
        try:
            with open(path) as fp:
                data = json.load(fp)
            for name, config in data.items():
                self.set_flag(
                    name,
                    enabled=config.get("enabled", False),
                    description=config.get("description", ""),
                    strategy=RolloutStrategy(config.get("strategy", "none")),
                    percentage=config.get("percentage", 0),
                    tenant_allowlist=config.get("tenant_allowlist", []),
                    tenant_blocklist=config.get("tenant_blocklist", []),
                    variants=config.get("variants", {}),
                )
        except FileNotFoundError:
            logger.debug("Feature flags config not found: %s", path)
        except Exception as e:
            logger.warning("Failed to load feature flags: %s", e)
