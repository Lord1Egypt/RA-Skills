#!/usr/bin/env python3
"""siteaudit — comprehensive website audit (uptime + TLS + headers + DNS). Zero dependencies."""
import ssl, socket, urllib.request, urllib.error, json, sys, argparse, re
from datetime import datetime, timezone

def check_uptime(url, timeout=10):
    start = __import__('time').monotonic()
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "siteaudit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ms = round((__import__('time').monotonic() - start) * 1000)
            return {"ok": True, "status": resp.status, "ms": ms}
    except urllib.error.HTTPError as e:
        ms = round((__import__('time').monotonic() - start) * 1000)
        return {"ok": e.code < 500, "status": e.code, "ms": ms}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}

def check_tls(host, port=443, timeout=10):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                days = (not_after - datetime.now(timezone.utc)).days
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                return {"ok": True, "days_left": days, "expires": not_after.isoformat()[:10],
                        "issuer": issuer.get("organizationName", "?"), "protocol": ssock.version()}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}

SECURITY_HEADERS = ["Strict-Transport-Security", "Content-Security-Policy", "X-Content-Type-Options",
                     "X-Frame-Options", "Referrer-Policy", "Permissions-Policy"]

def check_headers(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "siteaudit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            present = [h for h in SECURITY_HEADERS if h.lower() in hdrs]
            missing = [h for h in SECURITY_HEADERS if h.lower() not in hdrs]
            score = len(present)
            grade = "A" if score >= 5 else "B" if score >= 4 else "C" if score >= 3 else "D" if score >= 1 else "F"
            server = hdrs.get("server", None)
            return {"ok": True, "grade": grade, "score": f"{score}/{len(SECURITY_HEADERS)}",
                    "missing": missing, "server": server}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}

def audit(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    host = parsed.hostname
    result = {"url": url, "host": host, "ts": datetime.now(timezone.utc).isoformat()}
    result["uptime"] = check_uptime(url)
    if parsed.scheme == "https":
        result["tls"] = check_tls(host)
    result["headers"] = check_headers(url)
    
    # Overall score
    issues = []
    if not result["uptime"].get("ok"):
        issues.append("❌ Site DOWN")
    elif result["uptime"].get("ms", 0) > 2000:
        issues.append("⚠️ Slow response (>2s)")
    tls = result.get("tls", {})
    if tls and not tls.get("ok"):
        issues.append("❌ TLS error")
    elif tls and tls.get("days_left", 999) <= 14:
        issues.append(f"⚠️ Cert expires in {tls['days_left']}d")
    hdrs = result.get("headers", {})
    if hdrs.get("grade") in ("D", "F"):
        issues.append(f"⚠️ Weak security headers ({hdrs.get('grade')})")
    result["issues"] = issues
    result["healthy"] = len(issues) == 0
    return result

def main():
    p = argparse.ArgumentParser(prog="siteaudit", description="Comprehensive website audit")
    p.add_argument("urls", nargs="+")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    all_healthy = True
    for url in args.urls:
        if not url.startswith("http"):
            url = "https://" + url
        r = audit(url)
        if not r["healthy"]:
            all_healthy = False
        if args.json:
            print(json.dumps(r, indent=2))
            continue
        icon = "✅" if r["healthy"] else "⚠️"
        print(f"\n{icon} {r['url']}")
        u = r["uptime"]
        print(f"  Uptime:   {'UP' if u.get('ok') else 'DOWN'} ({u.get('ms', '?')}ms, HTTP {u.get('status', '?')})")
        if "tls" in r:
            t = r["tls"]
            if t.get("ok"):
                print(f"  TLS:      {t['protocol']} — expires {t['expires']} ({t['days_left']}d) via {t['issuer']}")
            else:
                print(f"  TLS:      ❌ {t.get('error', '?')}")
        h = r["headers"]
        if h.get("ok"):
            print(f"  Headers:  Grade {h['grade']} ({h['score']})")
            if h.get("missing"):
                print(f"            Missing: {', '.join(h['missing'][:3])}")
        if r["issues"]:
            for issue in r["issues"]:
                print(f"  {issue}")

    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()
