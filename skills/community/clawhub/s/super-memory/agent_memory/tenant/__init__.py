"""Multi-tenant management for Agent Memory.

Unified entry point: TenantKernel (combines quotas + isolation).
Backward-compatible exports: TenantManager, TenantContext, TenantIsolationManager.
"""
from __future__ import annotations

import importlib.util as _ilu
import os as _os

from .kernel import TenantKernel
from .manager import TenantConfig, TenantManager, TenantQuota, TenantTier
from .middleware import TenantMiddleware

# Load the legacy tenant.py module to re-export TenantContext,
# TenantIsolationManager, and TenantPartitionStrategy.
# We use importlib.util because ``agent_memory.tenant`` resolves to this
# package (tenant/__init__.py), not the sibling tenant.py file.
_legacy_path = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), "tenant.py")
if _os.path.isfile(_legacy_path):
    _spec = _ilu.spec_from_file_location("_tenant_legacy", _legacy_path)
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    TenantContext = _mod.TenantContext
    TenantIsolationManager = _mod.TenantIsolationManager
    TenantPartitionStrategy = _mod.TenantPartitionStrategy
    del _spec, _mod
del _ilu, _os, _legacy_path

__all__ = [
    # Unified entry point
    "TenantKernel",
    # Quota / rate-limiting / metering
    "TenantManager",
    "TenantConfig",
    "TenantQuota",
    "TenantTier",
    # Data isolation
    "TenantIsolationManager",
    "TenantPartitionStrategy",
    # Per-request context
    "TenantContext",
    # Middleware
    "TenantMiddleware",
]
