#!/usr/bin/env python3
"""Passive check of redirects, TLS, security headers, cookies and delivery headers.

Usage: python check_headers.py https://example.com/ [--allow-private] [--timeout 15]

Prints JSON. Every issue carries the evidence it is based on. A header reported as
missing is missing from the one response observed here; other paths may differ.
"""
import argparse
import datetime
import os
import re
import socket
import ssl
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (add_common_args, emit, fetch_kwargs, follow, get_header, get_headers,  # noqa: E402
                   make_issue, normalize_url, now_iso, proxy_env)

INTERCEPT_RE = re.compile(r"egress|gateway|proxy|inspection|zscaler|forcepoint|fortinet|fortigate|"
                          r"palo alto|blue ?coat|netskope|umbrella|mitm", re.I)
INTERCEPT_CAVEAT = ("The certificate issuer or environment suggests TLS inspection or a proxy on this network path. "
                    "Certificate details (and possibly some headers) may describe that intermediary, not the audited site.")


def looks_intercepted(issuer):
    """Heuristic only: True if the issuer name looks like a proxy/inspection CA."""
    return bool(issuer and INTERCEPT_RE.search(issuer))


SESSION_RE = re.compile(r"(sess|sid|auth|token|jwt|login)", re.I)
HSTS_MIN = 15552000  # 180 days


def analyse_hsts(v):
    d = {"present": v is not None, "value": v}
    if v is None:
        return d
    m = re.search(r"max-age\s*=\s*\"?(\d+)", v, re.I)
    d["max_age"] = int(m.group(1)) if m else None
    d["include_subdomains"] = "includesubdomains" in v.lower()
    d["preload"] = "preload" in v.lower()
    return d


def analyse_csp(v):
    d = {"present": v is not None, "value": None if v is None else v[:1000]}
    if not v:
        return d
    dirs = {}
    for part in v.split(";"):
        toks = part.strip().split()
        if toks:
            dirs[toks[0].lower()] = [t.lower() for t in toks[1:]]
    weaknesses = []
    script_src = dirs.get("script-src", dirs.get("default-src"))
    if script_src is None:
        weaknesses.append("no script-src or default-src directive: script sources are not restricted")
    else:
        protected = any(t.startswith("'nonce-") or t.startswith("'sha") or t == "'strict-dynamic'" for t in script_src)
        if "'unsafe-inline'" in script_src and not protected:
            weaknesses.append("script-src allows 'unsafe-inline' without a nonce or hash")
        if "'unsafe-eval'" in script_src:
            weaknesses.append("script-src allows 'unsafe-eval'")
        broad = [t for t in script_src if t in ("*", "http:", "https:", "data:")]
        if broad:
            weaknesses.append("script-src allows broad sources: %s" % ", ".join(broad))
    d["directives"] = sorted(dirs)
    d["has_frame_ancestors"] = "frame-ancestors" in dirs
    d["weaknesses"] = weaknesses
    return d


def parse_set_cookie(v):
    parts = [x.strip() for x in v.split(";")]
    name = parts[0].split("=", 1)[0]
    attrs = {}
    for a in parts[1:]:
        k, _, val = a.partition("=")
        attrs[k.strip().lower()] = val.strip()
    return {"name": name, "secure": "secure" in attrs, "httponly": "httponly" in attrs,
            "samesite": attrs.get("samesite"), "session_like_name": bool(SESSION_RE.search(name))}


def redact_headers(headers):
    out = []
    for k, v in headers:
        if k.lower() == "set-cookie":
            name, _, rest = v.partition("=")
            _, _, attrs = rest.partition(";")
            v = "%s=<redacted>;%s" % (name, attrs)
        out.append([k, v])
    return out


def check_tls(host, port, timeout):
    out = {"checked": True, "host": host, "port": port}
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            with ctx.wrap_socket(s, server_hostname=host) as ss:
                cert = ss.getpeercert()
                out["protocol"] = ss.version()
        not_after = ssl.cert_time_to_seconds(cert["notAfter"])
        out["verified"] = True
        out["not_after"] = datetime.datetime.fromtimestamp(not_after, datetime.timezone.utc).strftime("%Y-%m-%d")
        out["days_remaining"] = int((not_after - time.time()) // 86400)
        out["issuer"] = ", ".join("%s=%s" % kv for rdn in cert.get("issuer", ()) for kv in rdn)
        out["san"] = [v for k, v in cert.get("subjectAltName", ()) if k == "DNS"][:10]
    except ssl.SSLCertVerificationError as e:
        out["verified"] = False
        out["error"] = "certificate verification failed: %s" % (e.verify_message or e)
    except (OSError, ssl.SSLError, KeyError) as e:
        out["error"] = "%s: %s" % (type(e).__name__, e)
    return out


def build(url, hops, r, tls, http_probe):
    final = hops[-1]["url"]
    https = urllib.parse.urlsplit(final).scheme == "https"
    h = r["headers"]
    issues = []
    meas = {}

    # Redirects
    meas["redirect_chain"] = hops
    if len(hops) - 1 >= 2:
        issues.append(make_issue("redirect.chain", "seo", "medium",
                                 "Reaching the final URL takes %d redirects." % (len(hops) - 1),
                                 evidence=[x["url"] for x in hops]))
    if not https:
        issues.append(make_issue("https.not_used", "security", "high",
                                 "The final URL is served over plain HTTP.", evidence=final))
    if http_probe is not None:
        meas["http_to_https"] = http_probe
        if http_probe.get("error"):
            meas["http_to_https"]["note"] = "Port 80 request failed; this is not necessarily a problem."
        elif http_probe["final_scheme"] != "https":
            issues.append(make_issue("https.no_redirect", "security", "high",
                                     "http:// does not end up on https://.", evidence=http_probe["chain"]))
        elif http_probe["first_status"] in (302, 303, 307):
            issues.append(make_issue("https.temporary_redirect", "security", "low",
                                     "http to https uses a temporary redirect status.",
                                     evidence={"first_status": http_probe["first_status"]}))

    # TLS
    meas["tls"] = tls
    if tls.get("checked"):
        if tls.get("verified") is False:
            issues.append(make_issue("tls.invalid", "security", "critical",
                                     "TLS certificate did not verify.", evidence=tls.get("error")))
        elif tls.get("error"):
            meas["tls"]["note"] = "TLS details could not be read."
        elif tls.get("days_remaining") is not None and tls["days_remaining"] < 0:
            issues.append(make_issue("tls.expired", "security", "critical",
                                     "TLS certificate is expired.", evidence=tls))
        elif tls.get("days_remaining") is not None and tls["days_remaining"] < 21:
            issues.append(make_issue("tls.expiring", "security", "high",
                                     "TLS certificate expires in %d days." % tls["days_remaining"], evidence=tls))

    # Security headers
    hsts = analyse_hsts(get_header(h, "strict-transport-security"))
    csp = analyse_csp(get_header(h, "content-security-policy"))
    xcto = get_header(h, "x-content-type-options")
    xfo = get_header(h, "x-frame-options")
    refpol = get_header(h, "referrer-policy")
    perm = get_header(h, "permissions-policy")
    meas["security_headers"] = {
        "strict-transport-security": hsts, "content-security-policy": csp,
        "content-security-policy-report-only": get_header(h, "content-security-policy-report-only"),
        "x-content-type-options": xcto, "x-frame-options": xfo,
        "referrer-policy": refpol, "permissions-policy": perm}
    if https:
        if not hsts["present"]:
            issues.append(make_issue("hsts.missing", "security", "medium",
                                     "No Strict-Transport-Security header on the HTTPS response."))
        elif hsts.get("max_age") is None or hsts["max_age"] < HSTS_MIN:
            issues.append(make_issue("hsts.weak", "security", "low",
                                     "HSTS max-age is missing, zero or under 180 days.", evidence=hsts["value"]))
    if not csp["present"]:
        issues.append(make_issue("csp.missing", "security", "medium",
                                 "No Content-Security-Policy header on this response.",
                                 evidence={"report_only_present": meas["security_headers"]["content-security-policy-report-only"] is not None}))
    elif csp.get("weaknesses"):
        issues.append(make_issue("csp.weak", "security", "low", "CSP is present but has weaknesses.",
                                 evidence=csp["weaknesses"]))
    if (xcto or "").strip().lower() != "nosniff":
        issues.append(make_issue("xcto.missing", "security", "low",
                                 "X-Content-Type-Options: nosniff not present.", evidence=xcto))
    if not xfo and not csp.get("has_frame_ancestors"):
        issues.append(make_issue("clickjacking.unprotected", "security", "medium",
                                 "Neither X-Frame-Options nor CSP frame-ancestors was sent."))
    if not refpol:
        issues.append(make_issue("referrer_policy.missing", "security", "low", "No Referrer-Policy header."))
    if not perm:
        issues.append(make_issue("permissions_policy.missing", "security", "low", "No Permissions-Policy header."))

    # Information leakage (raw values only)
    server, powered = get_header(h, "server"), get_header(h, "x-powered-by")
    meas["disclosure"] = {"server": server, "x-powered-by": powered,
                          "via": get_header(h, "via"), "x-cache": get_header(h, "x-cache")}
    leaks = {}
    if server and re.search(r"\d+\.\d+", server):
        leaks["server"] = server
    if powered:
        leaks["x-powered-by"] = powered
    if leaks:
        issues.append(make_issue("disclosure.version", "security", "low",
                                 "Response headers reveal software or version details.", evidence=leaks))

    # Cookies
    cookies = [parse_set_cookie(v) for v in get_headers(h, "set-cookie")]
    meas["cookies"] = cookies
    if cookies:
        miss_secure = [c["name"] for c in cookies if https and not c["secure"]]
        miss_http = [c for c in cookies if not c["httponly"]]
        miss_ss = [c["name"] for c in cookies if not c["samesite"]]
        if miss_secure:
            issues.append(make_issue("cookie.no_secure", "security", "medium",
                                     "Cookies set over HTTPS without the Secure flag.", evidence=miss_secure))
        if miss_http:
            sess = any(c["session_like_name"] for c in miss_http)
            issues.append(make_issue("cookie.no_httponly", "security", "medium" if sess else "low",
                                     "Cookies without HttpOnly%s." % (" (includes session-like names)" if sess else ""),
                                     evidence=[c["name"] for c in miss_http]))
        if miss_ss:
            issues.append(make_issue("cookie.no_samesite", "security", "low",
                                     "Cookies without an explicit SameSite attribute.", evidence=miss_ss))

    # Delivery
    meas["delivery"] = {
        "status": r["status"], "content_type": get_header(h, "content-type"),
        "content_encoding": get_header(h, "content-encoding"),
        "cache_control": get_header(h, "cache-control"), "etag": get_header(h, "etag") is not None,
        "last_modified": get_header(h, "last-modified") is not None,
        "access_control_allow_origin": get_header(h, "access-control-allow-origin"),
        "time_to_headers_ms": r["headers_ms"],
        "timing_note": "single request from this machine; not a performance score"}
    meas["raw_headers"] = redact_headers(h)
    return meas, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    add_common_args(ap)
    args = ap.parse_args()
    kw = fetch_kwargs(args)
    url = normalize_url(args.url)
    out = {"tool": "check_headers", "checked_at": now_iso(), "target": url, "errors": [],
           "caveats": ["Headers are from one response; other paths, methods or user agents may differ.",
                       "A header reported missing means missing in this response, not necessarily absent site-wide."]}
    hops, r = follow(url, read_body=False, accept_encoding="gzip, br", **kw)
    if r["error"]:
        out["errors"].append({"url": hops[-1]["url"], "error": r["error"]})
        out["status"] = "not_checked"
        emit(out)
        sys.exit(2)

    final = urllib.parse.urlsplit(hops[-1]["url"])
    tls = {"checked": False, "reason": "final URL is not https"}
    if final.scheme == "https":
        tls = check_tls(final.hostname, final.port or 443, args.timeout)

    http_probe = None
    if final.hostname and (final.port in (None, 80, 443)):
        probe_url = "http://%s/" % final.hostname
        ph, pr = follow(probe_url, max_hops=5, read_body=False, **kw)
        http_probe = {"probe_url": probe_url, "chain": [x["url"] for x in ph],
                      "first_status": ph[0]["status"], "error": pr["error"] or ph[0].get("error"),
                      "final_scheme": urllib.parse.urlsplit(ph[-1]["url"]).scheme}

    meas, issues = build(url, hops, r, tls, http_probe)
    proxies = proxy_env()
    suspect = bool(proxies) or looks_intercepted(tls.get("issuer", "")) if isinstance(tls, dict) else bool(proxies)
    out["environment"] = {"proxy_variables_set": proxies, "tls_interception_suspected": suspect}
    out["caveats"].append("Certificate details are what this machine's network path presents; networks with "
                          "TLS inspection (corporate proxies, sandboxes) substitute their own certificate.")
    if suspect:
        out["caveats"].append(INTERCEPT_CAVEAT)
        if isinstance(meas.get("tls"), dict) and meas["tls"].get("checked"):
            meas["tls"]["note"] = "Possible interception: the certificate may belong to an intermediary, not the site."
        for i in issues:
            if i["id"].startswith("tls."):
                i["confidence"] = "needs_manual_check"
                i["note"] = "Possible TLS interception on this network path; verify from a different network."
    out["final_url"] = hops[-1]["url"]
    out["measurements"] = meas
    out["issues"] = issues
    emit(out)


if __name__ == "__main__":
    main()
