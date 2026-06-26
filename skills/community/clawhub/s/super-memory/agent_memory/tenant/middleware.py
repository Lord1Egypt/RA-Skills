"""Tenant middleware for API request isolation.

Supports both TenantKernel (unified) and TenantManager (legacy) as the
backend, maintaining backward compatibility.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TenantMiddleware:
    def __init__(self, tenant_kernel=None):
        """
        Args:
            tenant_kernel: A TenantKernel instance (preferred) or a
                TenantManager instance (legacy backward compatibility).
        """
        self._kernel = tenant_kernel
        # Detect whether we have a unified kernel or a legacy manager
        self._is_kernel = hasattr(tenant_kernel, 'isolation')
        # Track slot_id per (tenant_id, operation) for correct release
        self._slot_ids: dict[str, str] = {}

    def process_request(self, tenant_id: str, operation: str) -> tuple[bool, str, Optional[int]]:
        if not tenant_id:
            return False, "Missing tenant_id", None

        if self._is_kernel:
            # Unified path: TenantKernel.check_write_allowed covers
            # quota + rate limit + concurrent + storage + isolation
            allowed, reason, retry_after = self._kernel.check_write_allowed(tenant_id, operation)
            if not allowed:
                logger.warning(
                    "Tenant write not allowed: %s op=%s reason=%s",
                    tenant_id, operation, reason,
                )
                return False, reason, retry_after
            # Acquire concurrent slot
            slot_id = self._kernel.manager.acquire_concurrent(tenant_id)
            if not slot_id:
                return False, "Concurrent query limit exceeded", None
            if isinstance(slot_id, str):
                self._slot_ids[tenant_id] = slot_id
        else:
            # Legacy path: TenantManager only
            allowed, reason, retry_after = self._kernel.check_quota(tenant_id, operation)
            if not allowed:
                logger.warning(
                    "Tenant quota exceeded: %s op=%s reason=%s",
                    tenant_id, operation, reason,
                )
                return False, reason, retry_after
            slot_id = self._kernel.acquire_concurrent(tenant_id)
            if not slot_id:
                return False, "Concurrent query limit exceeded", None
            if isinstance(slot_id, str):
                self._slot_ids[tenant_id] = slot_id

        return True, "", None

    def process_response(self, tenant_id: str, operation: str,
                         latency_ms: float, memory_id: str = None,
                         is_error: bool = False):
        slot_id = self._slot_ids.pop(tenant_id, None)
        if self._is_kernel:
            self._kernel.manager.release_concurrent(tenant_id, slot_id=slot_id)
            self._kernel.record_usage(
                tenant_id, operation, latency_ms=latency_ms,
                memory_id=memory_id, is_error=is_error,
            )
        else:
            self._kernel.release_concurrent(tenant_id, slot_id=slot_id)
            self._kernel.record_usage(
                tenant_id, operation, latency_ms, memory_id, is_error
            )
