"""Shared helpers for the website-audit scripts. Standard library only.

Design rules:
- Passive: only GET/HEAD, bounded body size, bounded redirects, explicit timeouts.
- Honest: network failures are returned as data (result["error"]), never hidden.
- Safe by default: refuses loopback/private/link-local targets unless --allow-private.
"""
import datetime
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib

USER_AGENT = "website-audit-skill/0.1 (passive, read-only audit)"
MAX_BODY = 2_000_000
REDIRECT_CODES = (301, 302, 303, 307, 308)
EXAMPLE_LIMIT = 5


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def proxy_env():
    """Names (never values: they may hold credentials) of proxy variables that are set."""
    import os
    names = ("http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY")
    return sorted({n.lower() for n in names if os.environ.get(n)})


PROXY_CAVEAT = ("A proxy is configured in this environment. TLS certificate details (and possibly some "
                "headers) may describe the proxy rather than the audited site, so treat them as unconfirmed.")


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_header(headers, name):
    name = name.lower()
    for k, v in headers:
        if k.lower() == name:
            return v
    return None


def get_headers(headers, name):
    name = name.lower()
    return [v for k, v in headers if k.lower() == name]


def blocked_reason(url, allow_private=False):
    """Return a string if the URL must not be fetched, else None."""
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https"):
        return "unsupported scheme (only http/https): %s" % url
    if not p.hostname:
        return "no host in URL: %s" % url
    if allow_private:
        return None
    try:
        port = p.port or (443 if p.scheme == "https" else 80)
        infos = socket.getaddrinfo(p.hostname, port, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, ValueError) as e:
        return "DNS lookup failed for %s: %s" % (p.hostname, e)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            return ("refused: %s resolves to non-public address %s "
                    "(use --allow-private only for sites you control)" % (p.hostname, ip))
    return None


def _inflate(data, limit):
    for wbits in (16 + zlib.MAX_WBITS, zlib.MAX_WBITS, -zlib.MAX_WBITS):
        try:
            return zlib.decompressobj(wbits).decompress(data, limit)
        except zlib.error:
            continue
    return b""


def fetch(url, method="GET", timeout=15.0, read_body=True, max_bytes=MAX_BODY,
          accept_encoding="gzip", allow_private=False):
    """One request, no redirect following. Never raises; failures go in result['error']."""
    result = {"url": url, "method": method, "status": None, "headers": [], "body": b"",
              "body_truncated": False, "wire_bytes": None, "error": None,
              "headers_ms": None, "total_ms": None}
    reason = blocked_reason(url, allow_private)
    if reason:
        result["error"] = reason
        return result
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": accept_encoding,
    })
    t0 = time.monotonic()
    try:
        resp = _OPENER.open(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        resp = e
    except Exception as e:  # network-level failure, TLS error, timeout, bad URL
        why = getattr(e, "reason", None) or e
        result["error"] = "%s: %s" % (type(e).__name__, why)
        result["total_ms"] = round((time.monotonic() - t0) * 1000)
        return result
    try:
        result["headers_ms"] = round((time.monotonic() - t0) * 1000)
        result["status"] = getattr(resp, "status", None) or resp.code
        result["headers"] = [(k, v) for k, v in resp.headers.items()]
        if read_body and method == "GET":
            raw = resp.read(max_bytes + 1)
            result["body_truncated"] = len(raw) > max_bytes
            raw = raw[:max_bytes]
            result["wire_bytes"] = len(raw)
            enc = (get_header(result["headers"], "content-encoding") or "").lower()
            if enc in ("gzip", "x-gzip", "deflate"):
                raw = _inflate(raw, max_bytes)
            result["body"] = raw
    except Exception as e:
        result["error"] = "%s while reading response: %s" % (type(e).__name__, e)
    finally:
        try:
            resp.close()
        except Exception:
            pass
    result["total_ms"] = round((time.monotonic() - t0) * 1000)
    return result


def follow(url, max_hops=10, **kw):
    """Follow redirects manually. Returns (hops, final_result). Each hop is a dict."""
    hops = []
    seen = set()
    cur = url
    for _ in range(max_hops + 1):
        r = fetch(cur, **kw)
        loc = get_header(r["headers"], "location")
        hop = {"url": cur, "status": r["status"], "error": r["error"]}
        hops.append(hop)
        if r["error"] or r["status"] not in REDIRECT_CODES or not loc:
            return hops, r
        nxt = urllib.parse.urljoin(cur, loc)
        hop["location"] = nxt
        seen.add(cur)
        if nxt in seen:
            r["error"] = "redirect loop at %s" % nxt
            return hops, r
        cur = nxt
    r["error"] = "too many redirects (more than %d)" % max_hops
    return hops, r


def decode_text(result):
    body = result["body"]
    ctype = get_header(result["headers"], "content-type") or ""
    m = re.search(r"charset=([\w\-]+)", ctype, re.I)
    enc = m.group(1) if m else None
    if not enc:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w\-]+)", body[:4096], re.I)
        enc = m.group(1).decode("ascii", "ignore") if m else "utf-8"
    try:
        return body.decode(enc, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def make_issue(id_, category, severity_hint, message, evidence=None, count=None,
               examples=None, wcag=None, confidence="verified"):
    d = {"id": id_, "category": category, "severity_hint": severity_hint,
         "confidence": confidence, "message": message}
    if wcag:
        d["wcag"] = wcag
    if count is not None:
        d["count"] = count
    if evidence is not None:
        d["evidence"] = evidence
    if examples:
        d["examples"] = list(examples)[:EXAMPLE_LIMIT]
    return d


def add_common_args(ap):
    ap.add_argument("--allow-private", action="store_true",
                    help="allow loopback/private addresses (only for sites you control)")
    ap.add_argument("--timeout", type=float, default=15.0, help="per-request timeout, seconds")


def fetch_kwargs(args):
    return {"timeout": args.timeout, "allow_private": args.allow_private}


def normalize_url(u):
    return u if "://" in u else "https://" + u


def emit(obj):
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False, default=str)
    sys.stdout.write("\n")
