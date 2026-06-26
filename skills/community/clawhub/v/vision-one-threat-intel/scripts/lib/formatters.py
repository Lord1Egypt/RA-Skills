"""Structured text output formatters optimized for AI agent consumption.

Handles two response formats:
- STIX 2.1 bundles (feedIndicators, feeds/reports)
- Standard JSON (suspiciousObjects)
"""

import re


def format_error(what_wrong, what_expected, example):
    return f"ERROR: {what_wrong}\nEXPECTED: {what_expected}\nEXAMPLE: {example}"


def _trunc(text, maxlen=120):
    if not text:
        return ""
    text = str(text)
    return text[:maxlen] + "..." if len(text) > maxlen else text


def _fmt_list(items, label):
    if not items:
        return ""
    if isinstance(items, list):
        return f"{label}: {', '.join(str(i) for i in items)}"
    return f"{label}: {items}"


# ---------------------------------------------------------------------------
# STIX indicator parsing
# ---------------------------------------------------------------------------

# Extract observable values from STIX patterns
_STIX_VALUE_RE = re.compile(r"=\s*'([^']+)'")
_STIX_TYPE_MAP = {
    "ipv4-addr": "IP",
    "ipv6-addr": "IP",
    "domain-name": "DOMAIN",
    "url": "URL",
    "file": "FILE",
    "email-addr": "EMAIL",
    "network-traffic": "NETWORK",
}


def _parse_stix_pattern(pattern):
    """Extract human-readable type and values from a STIX pattern."""
    if not pattern:
        return "UNKNOWN", ""

    # Determine type from pattern
    ioc_type = "INDICATOR"
    for stix_type, label in _STIX_TYPE_MAP.items():
        if stix_type in pattern:
            ioc_type = label
            break

    # Extract values
    values = _STIX_VALUE_RE.findall(pattern)
    return ioc_type, ", ".join(values) if values else pattern


def _format_kill_chain(phases):
    """Format kill chain phases into a readable string."""
    if not phases:
        return ""
    names = [p.get("phase_name", "") for p in phases if p.get("phase_name")]
    return ", ".join(names) if names else ""


def format_stix_indicator(ind):
    """Format a single STIX 2.1 indicator object."""
    lines = []
    pattern = ind.get("pattern", "")
    ioc_type, values = _parse_stix_pattern(pattern)

    lines.append(f"Type: {ioc_type}")
    lines.append(f"Value: {values}")
    lines.append(f"Pattern: {_trunc(pattern, 200)}")

    valid_from = ind.get("valid_from", "")
    valid_until = ind.get("valid_until", "")
    created = ind.get("created", "")
    modified = ind.get("modified", "")

    kill_chain = _format_kill_chain(ind.get("kill_chain_phases", []))
    if kill_chain:
        lines.append(f"Kill Chain: {kill_chain}")

    if created:
        lines.append(f"Created: {created}")
    if valid_from:
        lines.append(f"Valid From: {valid_from}")
    if valid_until:
        lines.append(f"Valid Until: {valid_until}")

    stix_id = ind.get("id", "")
    if stix_id:
        lines.append(f"ID: {stix_id}")

    return "\n".join(lines)


def format_indicator_table(indicators, title="Feed Indicators"):
    """Format multiple STIX indicators as a compact summary."""
    if not indicators:
        return f"=== {title}: 0 results ==="

    lines = [f"=== {title}: {len(indicators)} results ===", ""]

    for i, ind in enumerate(indicators, 1):
        pattern = ind.get("pattern", "")
        ioc_type, values = _parse_stix_pattern(pattern)
        valid_from = ind.get("valid_from", "")
        date_part = valid_from[:10] if valid_from else ""
        kill_chain = _format_kill_chain(ind.get("kill_chain_phases", []))

        line = f"{i:3d}. [{ioc_type}] {_trunc(values, 60)}"
        if kill_chain:
            line += f" | {_trunc(kill_chain, 30)}"
        if date_part:
            line += f" | {date_part}"
        lines.append(line)

    lines.append("")
    lines.append(f"Total: {len(indicators)} indicators")
    lines.append("===")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Suspicious objects (standard JSON format)
# ---------------------------------------------------------------------------

_SO_VALUE_FIELDS = ["value", "ip", "domain", "url", "fileSha1", "fileSha256", "senderMailAddress"]


def _get_so_value(obj):
    """Extract the indicator value from a suspicious object.

    The value field name matches the type (e.g., fileSha256: 'HASH').
    """
    for field in _SO_VALUE_FIELDS:
        v = obj.get(field)
        if v:
            return v
    return "?"


def format_suspicious_object(obj):
    """Format a single suspicious object entry."""
    lines = []
    obj_type = obj.get("type", "?")
    value = _get_so_value(obj)

    lines.append(f"Type: {obj_type}")
    lines.append(f"Value: {value}")
    lines.append(f"Scan Action: {obj.get('scanAction', '?')}")
    lines.append(f"Risk Level: {obj.get('riskLevel', '?').upper()}")

    desc = obj.get("description", "")
    if desc:
        lines.append(f"Description: {_trunc(desc, 200)}")

    exp = obj.get("expiredDateTime", "")
    if exp:
        lines.append(f"Expires: {exp}")

    last_mod = obj.get("lastModifiedDateTime", "")
    if last_mod:
        lines.append(f"Last Modified: {last_mod}")

    in_exception = obj.get("inExceptionList")
    if in_exception is not None:
        lines.append(f"In Exception List: {'Yes' if in_exception else 'No'}")

    return "\n".join(lines)


def format_suspicious_table(objects, title="Suspicious Objects"):
    """Format multiple suspicious objects as a compact summary."""
    if not objects:
        return f"=== {title}: 0 results ==="

    lines = [f"=== {title}: {len(objects)} results ===", ""]

    for i, obj in enumerate(objects, 1):
        obj_type = obj.get("type", "?")
        value = _trunc(_get_so_value(obj), 64)
        action = obj.get("scanAction", "?")
        risk = obj.get("riskLevel", "?").upper()
        exp = obj.get("expiredDateTime", "")
        exp_date = exp[:10] if exp else ""
        lines.append(f"{i:3d}. [{obj_type}] {value} | {action} | {risk} | expires {exp_date}" if exp_date else
                     f"{i:3d}. [{obj_type}] {value} | {action} | {risk}")

    lines.append("")
    lines.append(f"Total: {len(objects)} objects")
    lines.append("===")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# STIX reports (from feeds endpoint)
# ---------------------------------------------------------------------------

def format_report(report):
    """Format a single STIX report object."""
    lines = []
    lines.append(f"Report: {report.get('name', '?')}")

    report_id = report.get("id", "")
    if report_id:
        lines.append(f"ID: {report_id}")

    published = report.get("published", "")
    if published:
        lines.append(f"Published: {published}")

    created = report.get("created", "")
    if created:
        lines.append(f"Created: {created}")

    modified = report.get("modified", "")
    if modified:
        lines.append(f"Modified: {modified}")

    report_types = report.get("report_types", [])
    if report_types:
        lines.append(f"Types: {', '.join(report_types)}")

    obj_refs = report.get("object_refs", [])
    if obj_refs:
        lines.append(f"Associated IOCs: {len(obj_refs)}")

    return "\n".join(lines)


def format_report_table(reports, title="Intelligence Reports"):
    """Format multiple STIX reports as a compact summary."""
    if not reports:
        return f"=== {title}: 0 results ==="

    lines = [f"=== {title}: {len(reports)} results ===", ""]

    for i, r in enumerate(reports, 1):
        name = _trunc(r.get("name", "?"), 70)
        published = r.get("published", r.get("created", ""))
        date_part = published[:10] if published else ""
        refs = r.get("object_refs", [])
        ref_count = len(refs) if refs else 0
        rid = r.get("id", "?")

        lines.append(f"{i:3d}. {name} | {date_part} | {ref_count} IOCs")
        lines.append(f"     ID: {rid}")

    lines.append("")
    lines.append(f"Total: {len(reports)} reports")
    lines.append("===")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Combined lookup
# ---------------------------------------------------------------------------

def format_lookup_result(indicator_matches, suspicious_match):
    """Format a combined lookup result (feed indicators + suspicious object check)."""
    lines = []

    if indicator_matches:
        lines.append(f"=== Feed Intelligence: {len(indicator_matches)} matches ===")
        lines.append("")
        for i, ind in enumerate(indicator_matches, 1):
            if i > 1:
                lines.append("---")
            lines.append(format_stix_indicator(ind))
    else:
        lines.append("=== Feed Intelligence: No matches ===")

    lines.append("")

    if suspicious_match:
        lines.append("=== Suspicious Object Status: FOUND ===")
        lines.append("")
        if isinstance(suspicious_match, list):
            for obj in suspicious_match:
                lines.append(format_suspicious_object(obj))
        else:
            lines.append(format_suspicious_object(suspicious_match))
    else:
        lines.append("=== Suspicious Object Status: Not on list ===")

    lines.append("===")
    return "\n".join(lines)
