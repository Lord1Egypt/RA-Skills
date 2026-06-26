#!/usr/bin/env python3
"""WHOIS domain lookup toolkit.

Queries WHOIS information for domains including registrar, creation/expiry dates,
nameservers, and domain availability. Uses socket-based WHOIS queries (no external deps).
"""

import argparse
import json
import re
import socket
import sys
from datetime import datetime, timezone


# WHOIS servers by TLD
WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "info": "whois.afilias.net",
    "io": "whois.nic.io",
    "co": "whois.nic.co",
    "dev": "whois.nic.google",
    "app": "whois.nic.google",
    "me": "whois.nic.me",
    "xyz": "whois.nic.xyz",
    "ai": "whois.nic.ai",
    "tech": "whois.nic.tech",
    "online": "whois.nic.online",
    "site": "whois.nic.site",
    "uk": "whois.nic.uk",
    "de": "whois.denic.de",
    "fr": "whois.nic.fr",
    "nl": "whois.sidn.nl",
    "eu": "whois.eu",
    "us": "whois.nic.us",
    "ca": "whois.cira.ca",
    "au": "whois.auda.org.au",
    "in": "whois.registry.in",
    "jp": "whois.jprs.jp",
}

# Fallback
DEFAULT_WHOIS = "whois.iana.org"


def get_whois_server(domain):
    """Determine the WHOIS server for a domain."""
    parts = domain.lower().strip(".").split(".")
    if len(parts) >= 2:
        tld = parts[-1]
        return WHOIS_SERVERS.get(tld, DEFAULT_WHOIS)
    return DEFAULT_WHOIS


def raw_whois(domain, server=None, port=43, timeout=10):
    """Perform a raw WHOIS query via socket."""
    if not server:
        server = get_whois_server(domain)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((server, port))
        query = domain + "\r\n"
        sock.sendall(query.encode("utf-8"))

        response = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        sock.close()
        return response.decode("utf-8", errors="replace")
    except socket.error as e:
        return f"Error connecting to {server}: {e}"


def parse_whois(text):
    """Parse WHOIS response into structured data."""
    info = {}

    patterns = {
        "domain": [
            r"Domain Name:\s*(.+)",
        ],
        "registrar": [
            r"Registrar:\s*(.+)",
            r"Registrar Name:\s*(.+)",
            r"Sponsoring Registrar:\s*(.+)",
        ],
        "creation_date": [
            r"Creation Date:\s*(.+)",
            r"Created Date:\s*(.+)",
            r"Created:\s*(.+)",
            r"Registration Date:\s*(.+)",
            r"created:\s*(.+)",
        ],
        "expiry_date": [
            r"(?:Registry )?Expir(?:y|ation) Date:\s*(.+)",
            r"Expiration Date:\s*(.+)",
            r"paid-till:\s*(.+)",
            r"expires:\s*(.+)",
        ],
        "updated_date": [
            r"Updated Date:\s*(.+)",
            r"Last Updated:\s*(.+)",
            r"last-modified:\s*(.+)",
        ],
        "status": [
            r"(?:Domain )?Status:\s*(.+)",
        ],
        "nameservers": [
            r"Name Server:\s*(.+)",
            r"nserver:\s*(.+)",
        ],
        "registrant_org": [
            r"Registrant Organization:\s*(.+)",
            r"Registrant:\s*(.+)",
        ],
        "registrant_country": [
            r"Registrant Country:\s*(.+)",
            r"Registrant State/Province:\s*(.+)",
        ],
    }

    for field, field_patterns in patterns.items():
        values = []
        for pat in field_patterns:
            matches = re.findall(pat, text, re.IGNORECASE | re.MULTILINE)
            values.extend([m.strip() for m in matches])
        if values:
            if field in ("status", "nameservers"):
                info[field] = list(dict.fromkeys(values))  # Deduplicate preserving order
            else:
                info[field] = values[0]

    return info


def parse_date(date_str):
    """Try to parse a date string."""
    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    # Try dateutil-like fallback
    try:
        # Remove timezone abbreviation suffixes
        cleaned = re.sub(r"\s+\w{3,4}$", "", date_str.strip())
        for fmt in formats:
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
    except Exception:
        pass
    return None


def days_until_expiry(info):
    """Calculate days until domain expiry."""
    expiry = info.get("expiry_date")
    if not expiry:
        return None
    dt = parse_date(expiry)
    if not dt:
        return None
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = dt - now
    return delta.days


def format_output(domain, info, raw_text, show_raw=False):
    """Format WHOIS results for display."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  WHOIS: {domain}")
    lines.append(f"{'='*60}\n")

    fields = [
        ("Domain", info.get("domain", domain)),
        ("Registrar", info.get("registrar", "N/A")),
        ("Organization", info.get("registrant_org", "N/A")),
        ("Country", info.get("registrant_country", "N/A")),
        ("Created", info.get("creation_date", "N/A")),
        ("Updated", info.get("updated_date", "N/A")),
        ("Expires", info.get("expiry_date", "N/A")),
    ]

    for label, value in fields:
        lines.append(f"  {label:15s} {value}")

    # Expiry warning
    days = days_until_expiry(info)
    if days is not None:
        if days < 0:
            lines.append(f"\n  \033[91m⚠ EXPIRED {abs(days)} days ago!\033[0m")
        elif days < 30:
            lines.append(f"\n  \033[91m⚠ Expires in {days} days!\033[0m")
        elif days < 90:
            lines.append(f"\n  \033[93m⚠ Expires in {days} days\033[0m")
        else:
            lines.append(f"\n  \033[92m✓ {days} days until expiry\033[0m")

    # Status
    statuses = info.get("status", [])
    if statuses:
        lines.append(f"\n  Status:")
        for s in statuses[:5]:
            lines.append(f"    - {s}")

    # Nameservers
    ns = info.get("nameservers", [])
    if ns:
        lines.append(f"\n  Nameservers:")
        for n in ns:
            lines.append(f"    - {n.lower()}")

    lines.append(f"\n{'='*60}\n")

    if show_raw:
        lines.append("--- Raw WHOIS Response ---")
        lines.append(raw_text)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="WHOIS domain lookup toolkit — query registrar, dates, nameservers, and expiry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s example.com                  Basic WHOIS lookup
  %(prog)s example.com example.org      Multiple domains
  %(prog)s example.com --json           JSON output
  %(prog)s example.com --raw            Show raw WHOIS response
  %(prog)s example.com --expiry-only    Show only expiry info
  %(prog)s example.com --server whois.verisign-grs.com  Use specific WHOIS server
        """,
    )
    parser.add_argument("domains", nargs="+", help="Domain name(s) to look up")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--raw", action="store_true", help="Show raw WHOIS response")
    parser.add_argument("--expiry-only", action="store_true", help="Show only expiry information")
    parser.add_argument("--server", help="Override WHOIS server")

    args = parser.parse_args()

    all_results = []

    for domain in args.domains:
        domain = domain.lower().strip()
        if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$", domain):
            print(f"Warning: '{domain}' doesn't look like a valid domain, trying anyway...")

        raw_text = raw_whois(domain, server=args.server)
        info = parse_whois(raw_text)
        info["_domain"] = domain
        days = days_until_expiry(info)
        if days is not None:
            info["_days_until_expiry"] = days

        all_results.append({"domain": domain, "info": info, "raw": raw_text})

        if not args.json:
            if args.expiry_only:
                expiry = info.get("expiry_date", "N/A")
                days_str = f" ({days} days)" if days is not None else ""
                print(f"{domain}: expires {expiry}{days_str}")
            else:
                print(format_output(domain, info, raw_text, show_raw=args.raw))

    if args.json:
        output = []
        for r in all_results:
            entry = dict(r["info"])
            entry.pop("_domain", None)
            entry["domain"] = r["domain"]
            if args.raw:
                entry["raw_response"] = r["raw"]
            output.append(entry)
        print(json.dumps(output if len(output) > 1 else output[0], indent=2))


if __name__ == "__main__":
    main()
