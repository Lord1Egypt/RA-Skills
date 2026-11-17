"""sluice - an outbound egress guard.

Scans any text bound for outside this machine (emails, social drafts, Telegram
replies, public-site writes) for leaked secrets and private identifiers, and
either reports them or redacts them in place.
"""
from .core import Finding, scan, redact, Severity

__all__ = ["Finding", "scan", "redact", "Severity"]
