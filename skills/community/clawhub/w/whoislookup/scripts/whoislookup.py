#!/usr/bin/env python3
"""whoislookup — domain WHOIS lookup. Zero dependencies."""
import socket, sys, argparse, json, re
from datetime import datetime, timezone

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com", "net": "whois.verisign-grs.com",
    "org": "whois.pir.org", "io": "whois.nic.io", "dev": "whois.nic.google",
    "app": "whois.nic.google", "ai": "whois.nic.ai", "co": "whois.nic.co",
    "me": "whois.nic.me", "xyz": "whois.nic.xyz", "info": "whois.afilias.net",
    "uk": "whois.nic.uk", "de": "whois.denic.de", "fr": "whois.nic.fr",
    "eu": "whois.eu", "ca": "whois.cira.ca", "au": "whois.auda.org.au",
}

def whois_query(domain, server=None, port=43, timeout=10):
    tld = domain.rsplit(".", 1)[-1].lower()
    server = server or WHOIS_SERVERS.get(tld, f"whois.nic.{tld}")
    try:
        s = socket.create_connection((server, port), timeout=timeout)
        s.sendall((domain + "\r\n").encode())
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        s.close()
        return data.decode("utf-8", errors="replace")
    except Exception as e:
        return f"Error querying {server}: {e}"

def parse_whois(raw):
    """Extract key fields from raw WHOIS text."""
    fields = {}
    patterns = {
        "registrar": r"Registrar:\s*(.+)",
        "created": r"Creat(?:ion|ed)\s*Date:\s*(.+)",
        "expires": r"(?:Expir(?:y|ation)\s*Date|Registry Expiry Date):\s*(.+)",
        "updated": r"Updated?\s*Date:\s*(.+)",
        "status": r"(?:Domain )?Status:\s*(.+)",
        "nameservers": r"Name Server:\s*(.+)",
    }
    for key, pat in patterns.items():
        matches = re.findall(pat, raw, re.IGNORECASE)
        if matches:
            if key in ("status", "nameservers"):
                fields[key] = [m.strip() for m in matches]
            else:
                fields[key] = matches[0].strip()
    return fields

def cmd_lookup(args):
    for domain in args.domains:
        raw = whois_query(domain, server=args.server)
        if args.raw:
            print(raw)
            continue
        parsed = parse_whois(raw)
        print(f"\n🔍 {domain}")
        print(f"  Registrar:    {parsed.get('registrar', '?')}")
        print(f"  Created:      {parsed.get('created', '?')}")
        print(f"  Expires:      {parsed.get('expires', '?')}")
        print(f"  Updated:      {parsed.get('updated', '?')}")
        if parsed.get("nameservers"):
            print(f"  Nameservers:  {', '.join(parsed['nameservers'][:4])}")
        if parsed.get("status"):
            print(f"  Status:       {parsed['status'][0]}")
        if args.json:
            parsed["domain"] = domain
            print(json.dumps(parsed, indent=2))

def main():
    p = argparse.ArgumentParser(prog="whoislookup", description="Domain WHOIS lookup")
    p.add_argument("domains", nargs="+", help="Domains to look up")
    p.add_argument("--raw", action="store_true", help="Show raw WHOIS response")
    p.add_argument("--json", action="store_true", help="Output parsed JSON")
    p.add_argument("--server", help="Override WHOIS server")
    args = p.parse_args()
    cmd_lookup(args)

if __name__ == "__main__":
    main()
