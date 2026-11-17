"""Errors that never carry secret material."""

from __future__ import annotations


class SecretDropError(Exception):
    """User-facing failure. Message must never include secret bytes or URL fragments."""
