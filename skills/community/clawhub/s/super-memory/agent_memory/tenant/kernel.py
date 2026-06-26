"""Unified TenantKernel — single entry point for tenant management.

Combines:
- TenantManager: quotas, rate limiting, concurrent limits, metering, billing
- TenantIsolationManager: data isolation (SHARED_DB / PER_TENANT_DB / HYBRID)

Usage:
    kernel = TenantKernel(store_path="memory.db", isolation_mode="shared_db")
    kernel.register_tenant("acme", tier="pro")
    allowed, reason = kernel.check_write_allowed("acme")
    ctx = kernel.get_tenant_context("acme")
"""
from __future__ import annotations

import importlib.util as _ilu
import logging
import os as _os
from typing import Any, Dict, Optional

from .manager import TenantConfig, TenantManager, TenantTier

logger = logging.getLogger(__name__)

# Load the legacy tenant.py module (agent_memory/tenant.py) to access
# TenantContext and TenantIsolationManager.  We cannot use a normal
# ``from ..tenant import ...`` because ``agent_memory.tenant`` resolves
# to this *package* (tenant/__init__.py), not the sibling tenant.py file.
_legacy_path = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), "tenant.py")
_spec = _ilu.spec_from_file_location("_tenant_legacy", _legacy_path)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
TenantContext = _mod.TenantContext
TenantIsolationManager = _mod.TenantIsolationManager
del _spec, _mod, _ilu, _os, _legacy_path


class TenantKernel:
    """Unified tenant management: quotas + isolation + metering + billing.

    This is the single entry point that coordinates the two previously
    separate tenant subsystems.  ``TenantManager`` and
    ``TenantIsolationManager`` can still be used independently for
    backward compatibility.
    """

    def __init__(
        self,
        store: Any = None,
        store_path: Optional[str] = None,
        isolation_mode: str = "shared_db",
        tenant_db_path: Optional[str] = None,
    ):
        # Quotas / rate limiting / metering
        self.manager = TenantManager(db_path=tenant_db_path)
        # Data isolation
        isolation_config: Dict[str, Any] = {"strategy": isolation_mode}
        if store_path:
            isolation_config["data_dir"] = store_path
        self.isolation = TenantIsolationManager(store=store, config=isolation_config)

    # ------------------------------------------------------------------
    # Tenant lifecycle
    # ------------------------------------------------------------------

    def register_tenant(
        self,
        tenant_id: str,
        tier: str = "free",
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> TenantConfig:
        """Register a tenant in both the quota manager and isolation manager."""
        tier_enum = TenantTier(tier)
        config = TenantConfig(
            tenant_id=tenant_id,
            name=name or tenant_id,
            tier=tier_enum,
            metadata=metadata or {},
        )
        # Register in quota manager
        self.manager.register_tenant(config)
        # Register in isolation manager
        try:
            self.isolation.create_tenant(tenant_id, metadata=metadata)
        except ValueError:
            # Already exists in isolation manager — that's fine
            pass
        return config

    def remove_tenant(self, tenant_id: str) -> bool:
        """Remove a tenant from both subsystems and clean up data."""
        removed_from_manager = self.manager.remove_tenant(tenant_id)
        removed_from_isolation = self.isolation.delete_tenant(tenant_id)
        return removed_from_manager or removed_from_isolation

    # ------------------------------------------------------------------
    # Write gate
    # ------------------------------------------------------------------

    def check_write_allowed(
        self,
        tenant_id: str,
        operation: str = "remember",
    ) -> tuple[bool, str, Optional[int]]:
        """Unified gate: checks quotas + isolation before allowing writes.

        Checks:
        1. Tenant exists in both subsystems
        2. Quota / rate limit / concurrent limit
        3. Storage quota (fetches current usage from isolation manager)
        """
        # Verify tenant exists in isolation registry
        if not self.isolation.registry.exists(tenant_id):
            return False, f"Tenant '{tenant_id}' not found in isolation registry", None

        # Fetch current storage usage for quota check
        memory_count: Optional[int] = None
        storage_bytes: Optional[int] = None
        try:
            stats = self.isolation.get_tenant_stats(tenant_id)
            memory_count = stats.get("memory_count")
            storage_bytes = stats.get("storage_size_bytes")
        except KeyError:
            pass  # Tenant not found in stats — will be caught by quota check

        return self.manager.check_write_allowed(
            tenant_id, operation, memory_count, storage_bytes
        )

    # ------------------------------------------------------------------
    # Usage recording
    # ------------------------------------------------------------------

    def record_usage(
        self,
        tenant_id: str,
        operation: str,
        tokens: int = 0,
        latency_ms: float = 0.0,
        memory_id: Optional[str] = None,
        is_error: bool = False,
    ):
        """Record usage for metering and billing."""
        self.manager.record_usage(
            tenant_id, operation, latency_ms, memory_id, is_error
        )

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    def get_tenant_context(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        permissions: Optional[set] = None,
    ) -> TenantContext:
        """Get a TenantContext for the given tenant."""
        config = self.manager.get_tenant(tenant_id)
        if permissions is None:
            permissions = {"read", "write"}
            if config and config.tier == TenantTier.ENTERPRISE:
                permissions.add("admin")
        return TenantContext(
            tenant_id=tenant_id,
            agent_id=agent_id,
            permissions=permissions,
        )

    # ------------------------------------------------------------------
    # Delegation helpers
    # ------------------------------------------------------------------

    def get_tenant(self, tenant_id: str) -> Optional[TenantConfig]:
        """Get tenant config from the quota manager."""
        return self.manager.get_tenant(tenant_id)

    def list_tenants(self) -> list:
        """List all registered tenants."""
        return self.manager.list_tenants()

    def get_billing_summary(self, tenant_id: str, period_days: int = 30) -> dict:
        """Get billing summary for a tenant."""
        return self.manager.get_billing_summary(tenant_id, period_days)

    def close(self):
        """Shut down both subsystems."""
        self.manager.close()
        self.isolation.close()
