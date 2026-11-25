"""RDAP check - registration age, registrar, status, and nameservers.

RDAP is the modern, JSON-based replacement for WHOIS. It is queried over
HTTPS via the public ``rdap.org`` bootstrap, so no API key or extra
dependency is required.

If a TLD has no RDAP service (or the lookup fails), the check is reported as
``skipped`` rather than failing the run.
"""
from __future__ import annotations

import datetime
import json
from typing import Dict, List, Optional

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import get
from ..util import base_domain, strip_host
from .base import Check

RDAP_BASE = "https://rdap.org/domain/"

# Status values that indicate the domain is not in normal, active use.
PROBLEM_STATUSES = {
    "client hold", "server hold", "pending delete", "redemption period",
    "pending transfer", "pending renew", "pending restore",
}


def _parse_dt(value: str) -> Optional[datetime.datetime]:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _find_event(events: List[dict], action: str) -> Optional[str]:
    for event in events:
        if event.get("eventAction", "").lower() == action.lower():
            return event.get("eventDate")
    return None


def _vcard_fn(entity: dict) -> str:
    """Extract the formatted name (``fn``) from an RDAP vCard."""
    vcard = entity.get("vcardArray")
    if not isinstance(vcard, list) or len(vcard) < 2:
        return ""
    for item in vcard[1]:
        if isinstance(item, list) and len(item) >= 4 and item[0] == "fn":
            return str(item[3])
    return ""


def _registrar(entities: List[dict]) -> str:
    for entity in entities:
        if "registrar" in entity.get("roles", []):
            return _vcard_fn(entity) or entity.get("handle", "") or "unknown"
    return ""


def _nameservers(nameservers: List[dict]) -> List[str]:
    out = []
    for ns in nameservers:
        name = ns.get("ldhName") or ns.get("unicodeName") or ""
        if name:
            out.append(name.lower().rstrip("."))
    return sorted(set(out))


def _days_until(value: str) -> Optional[int]:
    dt = _parse_dt(value)
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return (dt - datetime.datetime.now(datetime.timezone.utc)).days


class RdapCheck(Check):
    name = "rdap"
    description = "Registration age, registrar, status, expiry, and nameservers (RDAP)"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        domain = base_domain(strip_host(target))
        if "." not in domain:
            return CheckResult(self.name, "skipped", summary="need a real domain")

        ok, body = get(RDAP_BASE + domain, cfg, follow=True)
        if not ok:
            return CheckResult(self.name, "skipped", summary="RDAP lookup unavailable",
                               error=body[:300])
        try:
            data: Dict = json.loads(body)
        except (ValueError, TypeError):
            return CheckResult(self.name, "skipped", summary="RDAP returned non-JSON",
                               error=body[:300])

        events = data.get("events") or []
        statuses = data.get("status") or []
        registrar = _registrar(data.get("entities") or [])
        nameservers = _nameservers(data.get("nameservers") or [])

        registered = _find_event(events, "registration")
        expires = _find_event(events, "expiration")
        updated = _find_event(events, "last changed")

        if registered:
            days_ago = _days_until(registered)
            days_ago = -days_ago if days_ago is not None else None
            years = days_ago // 365 if days_ago is not None and days_ago >= 0 else None
            findings.append(Finding(
                self.name,
                f"Registered: {registered[:10]}" + (f" (~{years} year(s) old)" if years is not None else ""),
                Severity.INFO, f"registration: {registered}",
            ))
            if days_ago is not None and 0 <= days_ago < 365:
                findings.append(Finding(
                    self.name, "Domain registered less than a year ago", Severity.LOW,
                    f"registration: {registered}",
                    "New domains deserve extra scrutiny, but are often legitimate.",
                ))
        else:
            findings.append(Finding(self.name, "No registration date in RDAP", Severity.INFO))

        if expires:
            days = _days_until(expires)
            findings.append(Finding(self.name, f"Expires: {expires[:10]}", Severity.INFO,
                                    f"expiration: {expires}"))
            if days is not None and days < 0:
                findings.append(Finding(self.name, "Domain registration has EXPIRED", Severity.HIGH,
                                        f"expiration: {expires}",
                                        "Renew the domain immediately."))
            elif days is not None and days <= 30:
                findings.append(Finding(self.name, f"Domain expires in {days} day(s)", Severity.MED,
                                        f"expiration: {expires}",
                                        "Renew soon and enable auto-renew."))
            elif days is not None and days <= 90:
                findings.append(Finding(self.name, f"Domain expires in {days} day(s)", Severity.LOW,
                                        f"expiration: {expires}",
                                        "Confirm auto-renew is enabled."))

        if updated:
            findings.append(Finding(self.name, f"Last changed: {updated[:10]}", Severity.INFO,
                                    f"last changed: {updated}"))

        if registrar:
            findings.append(Finding(self.name, f"Registrar: {registrar}", Severity.INFO))

        if statuses:
            findings.append(Finding(self.name, "Status: " + ", ".join(statuses), Severity.INFO,
                                    "status: " + ", ".join(statuses)))
            problems = [s for s in statuses if s.lower() in PROBLEM_STATUSES]
            if problems:
                findings.append(Finding(
                    self.name, "Domain has a problem status: " + ", ".join(problems), Severity.HIGH,
                    "status: " + ", ".join(problems),
                    "Investigate the registration status with the registrar.",
                ))

        if nameservers:
            findings.append(Finding(self.name, "Nameservers: " + ", ".join(nameservers),
                                    Severity.INFO, "; ".join(nameservers)))
        else:
            findings.append(Finding(self.name, "No nameservers in RDAP", Severity.LOW,
                                    "Nameservers missing from the registration record."))

        summary = (
            f"registrar={registrar or '-'}; "
            f"registered={registered[:10] if registered else '-'}; "
            f"expires={expires[:10] if expires else '-'}; statuses={len(statuses)}"
        )
        return CheckResult(self.name, "ok", findings, summary)
