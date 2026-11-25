#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Domain Risk & Xuan-Ping Review - read-only black-box scanner (generic v1.2.1)
Input: any domain. Output: structured JSON (DNS / TLS / HTTP headers / subdomains /
sensitive content / whois registration age / CDN-range hints / compliance-publicity evidence /
suspected hosting-region hint).

Universality contract:
  - No domain-specific constants; all facts are driven by collected evidence.
  - Unavailable data stays empty and is marked "evidence failed"; never fabricated,
    never filled with defaults.
  - CDN attribution is only a "suspected" hint from public IP ranges; it never
    asserts the origin location / hosting geography.
  - Compliance-publicity evidence (v1.2) reports only page "present / absent" facts;
    absence != violation / no filing obligation, and no legal conclusion is drawn.
  - Pure external read-only: no config changes, no credentials, no panel login.
"""
import sys, json, socket, ssl, re, ipaddress
from datetime import datetime, timezone
import requests

TIMEOUT = 12

# Generic common subdomains only (no business-specific names; probe results ARE the evidence, no assumed existence)
COMMON_SUBS = ["www", "api", "mail", "webmail", "m", "app", "dev", "admin",
               "status", "cdn", "img", "static", "blog", "shop", "test",
               "staging", "docs", "ftp", "ns1", "ns2", "origin", "assets"]

# Public CDN edge IPv4 ranges (for "suspected" hints only; NOT origin location)
# A hit only means the A record falls in a public edge range; it cannot be used to infer the server physical location.
CDN_RANGES = {
    "Cloudflare": [
        "104.16.0.0/13", "172.64.0.0/13", "162.158.0.0/15", "173.245.48.0/20",
        "103.21.244.0/22", "141.101.64.0/18", "108.162.192.0/18",
        "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22",
        "198.41.128.0/17", "131.0.72.0/22",
    ],
}

# Suspected hosting-region hint from CDN hits (U4): "suspected" only, NOT proof of origin.
# Values: "Overseas" / "Mainland" / "Unknown". Register new CDN ranges here; unregistered => "Unknown",
# never infer geography or filing obligation from an unregistered hit.
CDN_REGION = {
    "Cloudflare": "Overseas",
}

def norm_domain(d):
    d = d.strip().lower()
    d = re.sub(r'^https?://', '', d)
    d = re.sub(r'^www\.', '', d)
    d = d.split('/')[0].split('?')[0]
    return d

def detect_cdn(ips):
    """Return a "suspected CDN" hint from public IP ranges. Empty list on no hit (never concludes "not CDN")."""
    hits = []
    for name, ranges in CDN_RANGES.items():
        nets = [ipaddress.ip_network(r) for r in ranges]
        for ip in ips or []:
            try:
                addr = ipaddress.ip_address(ip)
                if addr.version == 4 and any(addr in n for n in nets):
                    if name not in hits:
                        hits.append(name)
            except ValueError:
                pass
    return hits

def hosting_region_hint(cdn_hint):
    """Suspected hosting-region hint from matched CDN names (U4, NOT proof of origin location).

    ICP filing obligation depends on whether the server is in mainland China, so check the
    region hint before judging ICP:
      - overseas CDN edge hit -> suspected overseas hosting -> usually no ICP obligation;
        an absent filing number on page is normal (not anomalous, not a risk, no urging);
      - mainland CDN edge hit -> suspected mainland hosting -> ICP obligation, owner verifies;
      - no hit / unregistered -> geography not confirmable, no inference, no risk from a missing number.
    Edge IP != origin; wording is always "suspected"; owner confirms in the hosting panel.
    """
    names = cdn_hint or []
    if not names:
        return {"region": "Unknown",
                "hint": "No known CDN edge range matched; hosting geography not confirmable by black box",
                "basis": [], "ok": True}
    regions = [CDN_REGION.get(n, "Unknown") for n in names]
    if "Overseas" in regions:
        return {"region": "Overseas",
                "hint": "Suspected overseas CDN edge (overseas hosting likely, NOT proof of origin)",
                "basis": names, "ok": True}
    if "Mainland" in regions:
        return {"region": "Mainland",
                "hint": "Suspected mainland CDN edge (mainland hosting likely, NOT proof of origin)",
                "basis": names, "ok": True}
    return {"region": "Unknown",
            "hint": "CDN with unregistered region matched; hosting geography not confirmable",
            "basis": names, "ok": True}

def get_a(domain):
    try:
        infos = socket.getaddrinfo(domain, None)
        v4 = sorted({i[4][0] for i in infos if ':' not in i[4][0]})
        v6 = sorted({i[4][0] for i in infos if ':' in i[4][0]})
        return {"v4": v4, "v6": v6, "cdn_hint": detect_cdn(v4), "ok": bool(v4 or v6)}
    except Exception as e:
        return {"v4": [], "v6": [], "cdn_hint": [], "ok": False, "error": str(e)}

def get_tls(domain, port=443):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        san = [t[1] for t in cert.get('subjectAltName', ()) if t[0] == 'DNS']
        nb = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
        na = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
        days = (na - datetime.now(timezone.utc)).days
        issuer = dict(x[0] for x in cert.get('issuer', ()))
        subject = dict(x[0] for x in cert.get('subject', ()))
        return {"subject_cn": subject.get('commonName'), "issuer_org": issuer.get('organizationName'),
                "issuer_cn": issuer.get('commonName'), "san": san,
                "not_before": nb.strftime('%Y-%m-%d'), "not_after": na.strftime('%Y-%m-%d'),
                "days_left": days, "ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_http_headers(domain):
    security = ["strict-transport-security", "content-security-policy", "x-content-type-options",
                "referrer-policy", "permissions-policy", "x-frame-options", "x-xss-protection"]
    try:
        r = requests.get(f"https://{domain}/", timeout=TIMEOUT, allow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0 universal-domain-xuanping/1.2.1"})
        h = {k.lower(): v for k, v in r.headers.items()}
        found = {s: h[s] for s in security if s in h}
        missing = [s for s in security if s not in h]
        redirect = {"from": r.history[0].status_code, "to": r.url} if r.history else None
        return {"status": r.status_code, "server": h.get('server'), "redirect": redirect,
                "security_present": found, "security_missing": missing,
                "body": r.text[:200000], "final_url": r.url, "ok": True,
                "raw_headers": h}  # v1.2: for compliance-publicity evidence (Cookie etc.)
    except Exception as e:
        return {"status": None, "ok": False, "error": str(e),
                "security_present": {}, "security_missing": [], "body": "", "final_url": None,
                "raw_headers": {}}

def scan_subdomains(domain, base_ips):
    """Enumerate generic common subdomains. Skip on evidence failure; never conclude "does not exist"."""
    results = []
    base_set = set(base_ips or [])
    for sub in COMMON_SUBS:
        host = f"{sub}.{domain}"
        try:
            ips = sorted({i[4][0] for i in socket.getaddrinfo(host, None)})
        except Exception:
            continue  # unresolvable = not recorded, never treated as "absent / no asset"
        code = None
        try:
            rr = requests.get(f"https://{host}/", timeout=6, allow_redirects=True,
                              headers={"User-Agent": "Mozilla/5.0 universal-domain-xuanping/1.2.1"})
            code = rr.status_code
        except requests.RequestException:
            code = "000"  # resolved but unreachable, recorded as-is
        results.append({"host": host, "ips": ips, "http": code,
                        "same_as_base": bool(set(ips) & base_set)})
    return results

def content_scan(body):
    findings = {"emails": [], "private_key_marks": [], "secret_words": [],
                "external_links": [], "analytics_scripts": []}
    b = body or ''
    for m in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', b):
        if m not in findings['emails']:
            findings['emails'].append(m)
    # Private-key header = high risk; password/api_key words = needs attention (may be documentation; human determination required)
    pk = re.findall(r'-----BEGIN [A-Z ]*PRIVATE KEY-----', b)
    if pk:
        findings['private_key_marks'].append({"label": "private-key header", "count": len(pk)})
    for pat, label in [(r'api[_-]?key\s*[:=]', 'api_key word'),
                       (r'(secret|password|passwd)\s*[:=]', 'password word')]:
        hits = re.findall(pat, b, re.I)
        if hits:
            findings['secret_words'].append({"label": label, "count": len(hits)})
    links = re.findall(r'https?://([A-Za-z0-9.-]+)', b)
    for l in links:
        if l not in findings['external_links']:
            findings['external_links'].append(l)
    for kw in ['gtag', 'googletagmanager', 'google-analytics', 'analytics',
               'hm.js', 'hm.baidu', 'clarity', 'plausible', 'umami']:
        if kw in b.lower():
            findings['analytics_scripts'].append(kw)
    return findings

# ---------- Compliance-publicity evidence (v1.2 new) ----------
# Chinese province abbreviations for ICP / public-security filing-number regex (fully generic, no domain-specific values)
_PROV = r'[京沪粤浙苏蜀鲁闽湘鄂豫冀辽吉黑皖赣桂琼渝川贵云藏陕甘青宁新]'
_RE_ICP = re.compile(_PROV + r'ICP备\s*\d{4,10}\s*号?')
_RE_POLICE = re.compile(_PROV + r'公网安备\s*\d{6,15}\s*号?')

# Keyword groups for privacy / terms / disclaimer (hit = "word appears on page" only, no semantic/legal judgment)
_KW_PRIVACY = ['隐私政策', '隐私权政策', '个人信息保护', '隐私说明', 'privacy policy', 'privacy']
_KW_TERMS = ['用户协议', '服务协议', '使用条款', '服务条款', 'terms of service', 'terms & conditions', 'terms']
_KW_DISCLAIM = ['免责声明', '免责', '不构成', '仅供参考', '不作任何', '风险提示',
                'disclaimer', 'not constitute', 'for reference only']

def _kw_hits(body, words):
    """Return the list of matched keywords; a hit only means the word appears, with no semantic/legal judgment."""
    low = (body or '').lower()
    return [w for w in words if w.lower() in low]

def compliance_publicity(body, headers):
    """Compliance-publicity read-only evidence: report page 'present / absent' facts only;
    no violation / obligation conclusion is drawn (legal determination left to the owner / counsel).

    All output fields are evidence facts or booleans; no 'compliant / non-compliant / obligated /
    not obligated' determination is included.
    """
    b = body or ''
    icp = sorted(set(x.strip() for x in _RE_ICP.findall(b)))
    police = sorted(set(x.strip() for x in _RE_POLICE.findall(b)))
    h = {str(k).lower(): v for k, v in (headers or {}).items()}
    set_cookie = bool(h.get('set-cookie'))
    return {
        "icp_no": icp,                       # ICP filing numbers appearing on the page (may be empty)
        "police_no": police,                 # public-security filing numbers on the page (may be empty)
        "privacy_marks": _kw_hits(b, _KW_PRIVACY),
        "terms_marks": _kw_hits(b, _KW_TERMS),
        "disclaimer_marks": _kw_hits(b, _KW_DISCLAIM),
        "set_cookie": set_cookie,            # whether the response sets a Cookie (tracking/session hint)
        "cookie_brand": ('cloudflare' if 'cloudflare' in str(h.get('set-cookie', '')).lower()
                         else ('other' if set_cookie else None)),
        "ok": True,                          # evidence action completed (does NOT mean compliant)
    }

def check_http_https(domain, final_url=None):
    """Check whether the ACTUAL SERVICE HOST forces http -> https. Reports facts only (status + Location).

    v1.2 correction: probe the final landing host, not the input bare domain —
    e.g. a bare domain may 301 to https properly while the www host's http returns 200 with no
    redirect; the two conclusions are opposite and probing the wrong host misleads. final_url is
    obtained from get_http_headers after redirects; its netloc is the actual service host.

    (examples are generic behavior patterns, not hard-coded facts about any domain)
    """
    host = domain
    if final_url:
        try:
            host = requests.utils.urlparse(final_url).netloc or domain
        except Exception:
            pass
    try:
        r = requests.get(f"http://{host}/", timeout=TIMEOUT, allow_redirects=False,
                         headers={"User-Agent": "Mozilla/5.0 universal-domain-xuanping/1.2.1"})
        loc = r.headers.get('location', '')
        forced = r.status_code in (301, 302, 307, 308) and loc.lower().startswith('https://')
        return {"host": host, "http_status": r.status_code, "location": loc or None,
                "forces_https": forced, "ok": True}
    except Exception as e:
        return {"host": host, "ok": False, "error": f"HTTP redirect probe failed: {type(e).__name__}"}

def parse_date(s):
    """Accept Unix timestamp (int/float) / ISO8601 / 'YYYY-MM-DD HH:MM:SS' / 'DD-Mon-YYYY'.
    api.whois.vu returns integer timestamps for some gTLDs and strings for .cn, so all must be handled."""
    if s is None or s == '':
        return None
    # Numeric timestamp (int/float or pure-digit string)
    if isinstance(s, (int, float)) or (isinstance(s, str) and re.fullmatch(r'\d{9,13}', s.strip())):
        try:
            ts = int(s)
            if ts > 10**12:  # milliseconds
                ts //= 1000
            return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d')
        except (ValueError, OSError, OverflowError):
            return None
    s = str(s).strip()
    m = re.match(r'(\d{4}-\d{2}-\d{2})', s)
    if m:
        return m.group(1)
    m = re.match(r'(\d{2})-([A-Za-z]{3})-(\d{4})', s)  # 02-Sep-2006
    if m:
        try:
            return datetime.strptime(s[:11], '%d-%b-%Y').strftime('%Y-%m-%d')
        except Exception:
            return None
    return None

def whois_lookup(domain):
    """Prefer structured fields (created/expires), fall back to multi-format regex.
    Compatible with .com / .cn / other suffixes. Missing -> ok=False, no fabrication."""
    try:
        r = requests.get(f"https://api.whois.vu/?q={domain}", timeout=TIMEOUT)
        if r.status_code != 200 or not r.text.strip().startswith('{'):
            return {"ok": False, "error": "whois API returned no valid data (verify manually in the registrar panel)"}
        d = r.json()
        raw = d.get('whois', '') or ''

        def grab(labels):
            for label in labels:
                m = re.search(rf'^\s*{label}\s*:\s*(.+)$', raw, re.I | re.M)
                if m:
                    return m.group(1).strip()
            return None

        # 1) Structured fields (most gTLDs provide these directly)
        created = parse_date(d.get('created'))
        expires = parse_date(d.get('expires'))
        # 2) Raw regex fallback (.cn / registrars differ in format)
        created = created or parse_date(grab([
            'Creation Date', 'Registration Time', 'Registered on', 'Created Date',
            'Registration Date', 'Domain Registration Date', 'created']))
        expires = expires or parse_date(grab([
            'Registry Expiry Date', 'Expiration Time', 'Expiry Date', 'Expires On',
            'Expiration Date', 'paid-till', 'Registrar Registration Expiration Date']))
        registrar = d.get('registrar') or grab([
            'Sponsoring Registrar', 'Registrar Name', 'Registrar'])
        name_servers = d.get('name_servers') or re.findall(
            r'^\s*(?:Name Server|nserver|Nserver)\s*:\s*(.+)$', raw, re.I | re.M)

        age = None
        if created:
            try:
                cd = datetime.strptime(created, '%Y-%m-%d')
                age = round((datetime.now() - cd).days / 365.25, 1)
            except Exception:
                pass
        ok = bool(created)
        return {"ok": ok, "source": "api.whois.vu", "registrar": registrar,
                "created": created, "expires": expires, "age_years": age,
                "statuses": d.get('statuses', []), "name_servers": name_servers,
                "error": None if ok else "Could not parse registration date (verify in the registrar panel)"}
    except Exception as e:
        return {"ok": False, "error": f"whois query failed: {type(e).__name__} (manual check needed)"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: scan_domain.py <domain>"}, ensure_ascii=False))
        sys.exit(1)
    domain = norm_domain(sys.argv[1])
    out = {"domain": domain,
           "scanned_at": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
           "tld": domain.rsplit('.', 1)[-1] if '.' in domain else ''}
    out['dns'] = get_a(domain)
    # U4: suspected hosting-region hint from CDN hits, for the report layer's ICP judgment (NOT proof of origin)
    out['hosting'] = hosting_region_hint(out['dns'].get('cdn_hint', []))
    out['tls'] = get_tls(domain)
    hdr = get_http_headers(domain)
    out['http'] = {k: v for k, v in hdr.items() if k not in ('body', 'raw_headers')}
    out['content'] = content_scan(hdr.get('body', ''))
    out['subdomains'] = scan_subdomains(domain, out['dns'].get('v4', []))
    out['whois'] = whois_lookup(domain)
    # v1.2 compliance-publicity evidence (facts only, no legal conclusion)
    out['compliance'] = compliance_publicity(hdr.get('body', ''), hdr.get('raw_headers', {}))
    out['http_https'] = check_http_https(domain, final_url=hdr.get('final_url'))
    # Evidence completeness: lets the report layer degrade, avoiding "evidence failed but reported normal"
    out['evidence'] = {
        "dns_ok": bool(out['dns'].get('ok')),
        "tls_ok": bool(out['tls'].get('ok')),
        "http_ok": bool(hdr.get('ok')),
        "whois_ok": bool(out['whois'].get('ok')),
        "compliance_ok": bool(out['compliance'].get('ok')),
        "http_https_ok": bool(out['http_https'].get('ok')),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
