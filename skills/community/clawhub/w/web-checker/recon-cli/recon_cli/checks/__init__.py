"""Checks package - one module per check.

``ALL_CHECKS`` is the ordered registry used by the CLI. Add a new check by
implementing :class:`recon_cli.checks.base.Check` and appending its class here;
``--only``, ``--skip``, and ``--help`` pick it up automatically.
"""
from __future__ import annotations

from .base import Check
from .headers import HeadersCheck
from .html_shell import HtmlShellCheck
from .js_bundle import JsBundleCheck
from .tls import TlsCheck
from .dns import DnsCheck
from .subdomains import SubdomainCheck
from .sensitive_paths import SensitivePathsCheck
from .rdap import RdapCheck

ALL_CHECKS: list[type[Check]] = [
    HeadersCheck,
    HtmlShellCheck,
    JsBundleCheck,
    TlsCheck,
    DnsCheck,
    RdapCheck,
    SubdomainCheck,
    SensitivePathsCheck,
]

__all__ = [
    "Check",
    "HeadersCheck",
    "HtmlShellCheck",
    "JsBundleCheck",
    "TlsCheck",
    "DnsCheck",
    "RdapCheck",
    "SubdomainCheck",
    "SensitivePathsCheck",
    "ALL_CHECKS",
]
