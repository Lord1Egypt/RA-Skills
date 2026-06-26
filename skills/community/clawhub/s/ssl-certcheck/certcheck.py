#!/usr/bin/env python3
"""certcheck — SSL/TLS certificate checker. Zero dependencies."""
import ssl, socket, sys, argparse, json
from datetime import datetime, timezone

def check_cert(host, port=443, timeout=10):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (not_after - now).days
                subject = dict(x[0] for x in cert.get("subject", ()))
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                sans = [v for t, v in cert.get("subjectAltName", ()) if t == "DNS"]
                return {
                    "host": host, "port": port, "ok": True,
                    "cn": subject.get("commonName", "?"),
                    "issuer": issuer.get("organizationName", issuer.get("commonName", "?")),
                    "not_before": not_before.isoformat(),
                    "not_after": not_after.isoformat(),
                    "days_left": days_left,
                    "sans": sans[:10],
                    "protocol": ssock.version(),
                    "cipher": ssock.cipher()[0],
                    "expired": days_left < 0,
                    "expiring_soon": 0 <= days_left <= 30,
                }
    except Exception as e:
        return {"host": host, "port": port, "ok": False, "error": str(e)[:300]}

def main():
    p = argparse.ArgumentParser(prog="certcheck", description="SSL/TLS certificate checker")
    p.add_argument("hosts", nargs="+", help="Hostnames to check")
    p.add_argument("-p", "--port", type=int, default=443)
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--days", type=int, default=30, help="Warning threshold for expiry (days)")
    args = p.parse_args()

    results = []
    for host in args.hosts:
        r = check_cert(host, port=args.port)
        results.append(r)
        if args.json:
            continue
        if not r["ok"]:
            print(f"❌ {host}: {r['error']}")
            continue
        icon = "❌" if r["expired"] else "⚠️" if r["days_left"] <= args.days else "✅"
        print(f"{icon} {host}")
        print(f"  CN:       {r['cn']}")
        print(f"  Issuer:   {r['issuer']}")
        print(f"  Expires:  {r['not_after'][:10]} ({r['days_left']}d left)")
        print(f"  Protocol: {r['protocol']}  Cipher: {r['cipher']}")
        if r["sans"]:
            print(f"  SANs:     {', '.join(r['sans'][:5])}")

    if args.json:
        print(json.dumps(results, indent=2))

    expiring = [r for r in results if r.get("expired") or r.get("expiring_soon")]
    if expiring:
        print(f"\n⚠️  {len(expiring)} cert(s) expired or expiring soon!")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
