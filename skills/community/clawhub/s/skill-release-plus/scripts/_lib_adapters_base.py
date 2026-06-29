#!/usr/bin/env python3
"""
_lib_adapters_base.py — Adapter base class for skill-release-plus targets.

Each target hub (clawhub, clawhub-cn, skillhub-cn, github-release, user-hook)
implements this interface so the main dispatcher can treat them uniformly.

Adapter responsibilities:
  - publish(slug, version, changelog, tar_path, skill_dir, extra) -> PublishResult
  - inspect(slug) -> InspectResult (best-effort; may return {exists: None} if unsupported)
  - check_slug_available(slug) -> bool | None  (None = unknown)

All adapters MUST handle their own auth (token reading from env) and MUST raise
or return ok=False on failure rather than calling sys.exit().
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PublishResult:
    """Uniform result envelope for adapter.publish()."""
    ok: bool
    target: str = ""
    slug: str = ""
    version: str = ""
    url: str = ""          # public URL of the published skill (best-effort)
    error: str = ""
    raw: Any = None        # raw response for debugging
    action: str = ""       # publish-new | publish-update | contribute | git-tag


@dataclass
class InspectResult:
    """Uniform result envelope for adapter.inspect()."""
    exists: Optional[bool] = None  # None = adapter can't tell (e.g., user-hook)
    version: str = ""
    display_name: str = ""
    owner: str = ""
    license: str = ""
    visibility: Optional[str] = None
    raw: Any = None
    error: str = ""


class BaseAdapter:
    """Subclass and implement publish() / inspect() / check_slug_available()."""

    target_name: str = "base"

    def __init__(self, cfg: dict):
        """cfg = resolved SRP_* config dict from _lib_config.resolve_config()."""
        self.cfg = cfg

    # ── Required ──────────────────────────────────────────────────────────

    def publish(
        self,
        slug: str,
        version: str,
        changelog: str,
        tar_path: str,
        skill_dir: str,
        extra: dict = None,
    ) -> PublishResult:
        raise NotImplementedError

    # ── Optional (default: not supported) ─────────────────────────────────

    def inspect(self, slug: str) -> InspectResult:
        return InspectResult(exists=None, error="inspect not supported by this adapter")

    def check_slug_available(self, slug: str) -> Optional[bool]:
        """Return True if available, False if taken, None if adapter can't tell."""
        return None

    # ── Helpers ───────────────────────────────────────────────────────────

    def _err(self, msg: str, raw: Any = None) -> PublishResult:
        return PublishResult(
            ok=False, target=self.target_name, error=msg, raw=raw
        )

    def _ok(self, slug: str, version: str, url: str = "",
            action: str = "publish", raw: Any = None) -> PublishResult:
        return PublishResult(
            ok=True, target=self.target_name, slug=slug, version=version,
            url=url, action=action, raw=raw
        )


__all__ = [
    "PublishResult",
    "InspectResult",
    "BaseAdapter",
]
