#!/usr/bin/env python3
"""recon_x402_market.py - measure the x402 market before you change anything.

READ-ONLY BY DESIGN. This artifact makes unpaid, anonymous GET/POST reads and writes its
reports into one local directory. It does NOT read a key, does NOT sign, does NOT settle a
payment, and never touches a wallet. Buying an endpoint is deliberately out of scope here:
a tool that can spend money deserves its own description, its own declared permissions and
its own review, so it lives in a separate artifact rather than hiding inside a measurement
tool.

Free, key-less steps:
  census    sweep the Coinbase CDP Bazaar discovery API and print the demand scoreboard
  probe     make unpaid calls to live 402 endpoints and report how they deliver terms
  manifest  compare a seller's discovery manifest against its own live 402 truth

Examples:
  python3 recon_x402_market.py census --out ./recon
  python3 recon_x402_market.py probe --sample 30 --out ./recon --allow-any-host
  python3 recon_x402_market.py manifest --seller https://seller.invalid --out ./recon

Destination policy, enforced in code (see fetch):
  * https only;
  * four documented hosts are allowed with no extra flag;
  * any other host requires --allow-any-host, which prints every off-domain host first, so
    contacting a stranger is a decision the operator made rather than one a listing chose;
  * loopback, private, link-local, multicast and reserved addresses are refused - including
    after DNS resolution and again on every redirect hop, so a hostile listing cannot aim
    this at an internal service or a cloud metadata endpoint;
  * every response is size-capped and every request counts against a hard budget.

Nothing is written outside --out (default: ./recon). No shell is executed.
"""
import argparse
import base64
import collections
import ipaddress
import json
import os
import random
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

DISCOVERY = "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources"
UA = "Mozilla/5.0 (compatible; x402-market-recon/1.1; read-only)"

DOCUMENTED_HOSTS = frozenset({
    "api.cdp.coinbase.com",   # Coinbase x402 discovery registry (census)
    "www.x402scan.com",       # registry read-back when verifying a listing
    "x402-list.com",          # directory scorecard pages
    "agent402.tools",         # published router ranking rule and buyer caps
})

MAX_BYTES = 750_000
REQUEST_BUDGET = 4_000
REQUEST_COUNT = 0
ALLOW_ANY_HOST = False
ALLOWED_SCHEMES = ("https",)


class Refused(SystemExit):
    """A destination was refused by policy. Never downgraded to a warning."""


def _require_public(host, port=None):
    """Resolve a host and require every address to be globally routable."""
    try:
        ipaddress.ip_address(host.split("%")[0])
        infos = [(socket.AF_UNSPEC, None, None, None, (host, 0))]
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, port or 443, proto=socket.IPPROTO_TCP)
        except OSError as e:
            raise Refused("REFUSED: cannot resolve %r (%s)" % (host, e))
    for _fam, _t, _p, _c, sockaddr in infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified):
            raise Refused("REFUSED: %s resolves to %s - a non-public address. Internal, "
                          "loopback, link-local and metadata targets are never contacted"
                          % (host, ip))
    return True


def assert_destination(url):
    """Validate one URL against the destination policy. Raises Refused when it fails."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES:
        raise Refused("REFUSED: scheme %r is not allowed (https only)" % (parts.scheme,))
    if not parts.hostname:
        raise Refused("REFUSED: no host in %r" % (url,))
    host = parts.hostname.lower()
    if host not in DOCUMENTED_HOSTS and not ALLOW_ANY_HOST:
        raise Refused("REFUSED: %s is not a documented host (%s). Off-domain reads need "
                      "--allow-any-host, so the contact is your decision."
                      % (host, ", ".join(sorted(DOCUMENTED_HOSTS))))
    _require_public(host, parts.port)
    return True


class _GuardedRedirect(urllib.request.HTTPRedirectHandler):
    """Re-validate every redirect hop: an open redirect is the classic way around a check."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        assert_destination(newurl)
        return urllib.request.HTTPRedirectHandler.redirect_request(
            self, req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_GuardedRedirect)


def fetch(url, data=None, method=None, timeout=45, headers=None, max_bytes=MAX_BYTES):
    """One guarded request: unpaid, anonymous, size-capped, budget-counted."""
    global REQUEST_COUNT
    assert_destination(url)
    REQUEST_COUNT += 1
    if REQUEST_COUNT > REQUEST_BUDGET:
        raise Refused("REFUSED: request budget of %d exhausted" % REQUEST_BUDGET)
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    if data is not None:
        h["Content-Type"] = "application/json"
    try:
        with _OPENER.open(urllib.request.Request(url, headers=h, data=data, method=method),
                          timeout=timeout) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(max_bytes)
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read(max_bytes)
    except Refused:
        raise
    except Exception as e:
        return None, {}, ("error: " + repr(e)[:120]).encode()


def envelope(headers, body):
    """Return (payload_dict, source) for a 402 answer, reading headers case-insensitively."""
    raw = headers.get("payment-required")
    if raw:
        try:
            return json.loads(base64.b64decode(raw + "=" * (-len(raw) % 4))), "header"
        except Exception:
            pass
    try:
        doc = json.loads(body)
        if isinstance(doc, dict) and (doc.get("accepts") or doc.get("paymentRequirements")):
            return doc, "body"
    except Exception:
        pass
    return None, None


def accept_amount(acc):
    """v2 puts the price in 'amount'; v1 sellers use 'maxAmountRequired'. Read both."""
    for key in ("amount", "maxAmountRequired"):
        v = acc.get(key)
        if v is not None:
            try:
                return int(v)
            except Exception:
                return None
    return None


def announce_offdomain(urls):
    hosts = sorted({urllib.parse.urlsplit(u).hostname for u in urls if u})
    print("   off-domain targets about to be contacted (%d hosts):" % len(hosts))
    for h in hosts[:25]:
        print("     -", h)
    if len(hosts) > 25:
        print("     ... and %d more" % (len(hosts) - 25))
    print("   each read is unpaid with an empty body: no key, no credentials, no payment")
    print("   header is ever sent. Private and link-local addresses are refused outright.")


def cmd_census(a):
    os.makedirs(a.out, exist_ok=True)
    print("1. SWEEP THE REGISTRY (read-only, key-less)")
    print("   Source:", DISCOVERY)
    code, _, body = fetch(DISCOVERY + "?limit=1&offset=0", timeout=60)
    if code != 200:
        print("   registry unreachable:", code)
        return 1
    total = json.loads(body).get("pagination", {}).get("total")
    print("   registry reports", total, "resources")
    offsets = (list(range(0, min(total or 0, a.pages * 100), 100)) if a.pages
               else list(range(0, total or 0, 100)))

    def one(off):
        c, _, b = fetch(DISCOVERY + "?limit=100&offset=%d" % off, timeout=60, max_bytes=2_000_000)
        if c != 200:
            return []
        try:
            return json.loads(b).get("items") or []
        except Exception:
            return []

    rows, failed = [], 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for items in ex.map(one, offsets):
            if not items:
                failed += 1
                continue
            for it in items:
                bz = ((it.get("extensions") or {}).get("bazaar") or {})
                info = bz.get("info") or {}
                outp = info.get("output") or {}
                acc = (it.get("accepts") or [{}])[0]
                res = it.get("resource") or ""
                rows.append({
                    "url": res.split("?")[0],
                    "origin": res.split("/")[2] if "//" in res else "",
                    "amount": accept_amount(acc),
                    "network": acc.get("network"),
                    "description_len": len(it.get("description") or ""),
                    "has_output_example": isinstance(outp.get("example"), (dict, list)),
                    "has_input": bool(info.get("input")),
                    "has_schema": bool(bz.get("schema")),
                    "tags": it.get("tags") or [],
                    "calls_30d": int((it.get("quality") or {}).get("l30DaysTotalCalls") or 0),
                    "payers_30d": int((it.get("quality") or {}).get("l30DaysUniquePayers") or 0),
                })
    path = os.path.join(a.out, "registry_census.jsonl")
    with open(path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    calls = sorted(r["calls_30d"] for r in rows)
    print("   sampled %d resources (%d failed pages) -> %s" % (len(rows), failed, path))
    if a.pages:
        print("   BIAS WARNING: --pages %d walks a PREFIX of the registry, not a random sample." % a.pages)
        print("   The registry returns items in its own order, so the medians and thresholds below")
        print("   are NOT representative of the whole catalogue. Use --pages 0 for a full sweep")
        print("   before quoting any of these numbers.")
    print("   NOTE: 'calls_30d' is the REGISTRY's own number and its definition is not published.")
    print("         Quote it as 'registry-reported calls', never as settlements you verified.")
    print("   median calls/30d: %d | p90: %d | p99: %d | max: %d" %
          (calls[len(calls) // 2], calls[int(.9 * len(calls))],
           calls[int(.99 * len(calls))], calls[-1]))
    total_calls = sum(calls)
    run, half = 0, None
    for i, c in enumerate(reversed(calls), 1):
        run += c
        if half is None and run >= total_calls * 0.5:
            half = i
    print("   resources holding 50%% of all calls: %s of %d" % (half, len(rows)))
    for label, pred in (("has output.example", lambda r: r["has_output_example"]),
                        ("no output.example", lambda r: not r["has_output_example"]),
                        ("description <120 chars", lambda r: r["description_len"] < 120),
                        ("description >400 chars", lambda r: r["description_len"] > 400)):
        g = [r["calls_30d"] for r in rows if pred(r)]
        if g:
            print("   %-24s n=%6d  median calls %5d  mean %6d" %
                  (label, len(g), sorted(g)[len(g) // 2], sum(g) // len(g)))
    bands = [(0, 0, "amount 0 (explicit)"), (1, 1000, "<= $0.001"), (1001, 5000, "$0.001-0.005"),
             (5001, 10000, "$0.005-0.01"), (10001, 30000, "$0.01-0.03"), (30001, 50000, "$0.03-0.05"),
             (50001, 100000, "$0.05-0.10"), (100001, 10 ** 18, "> $0.10")]
    print("   price band vs demand (median calls/30d):")
    for lo, hi, label in bands:
        g = [r["calls_30d"] for r in rows if r["amount"] is not None and lo <= r["amount"] <= hi]
        if g:
            print("     %-18s n=%6d  median %5d" % (label, len(g), sorted(g)[len(g) // 2]))
    print("   rank thresholds from this sample (calls/30d):")
    rc = sorted((r["calls_30d"] for r in rows), reverse=True)
    for rank in (10, 50, 100, 500, 1000):
        if rank <= len(rc):
            print("     rank %-5d %6d  (~%.1f/day)" % (rank, rc[rank - 1], rc[rank - 1] / 30.0))
    org = collections.Counter()
    for r in rows:
        org[r["origin"]] += r["calls_30d"]
    print("   origins ranked by registry-reported calls (server-level, top 10):")
    for host, v in org.most_common(10):
        print("     %9d  %s" % (v, host))
    print("   requests used: %d of %d budget" % (REQUEST_COUNT, REQUEST_BUDGET))
    return 0


def cmd_probe(a):
    os.makedirs(a.out, exist_ok=True)
    census = os.path.join(a.out, "registry_census.jsonl")
    if not os.path.exists(census):
        print("run 'census' first: probe needs the URL list it sampled")
        return 1
    with open(census) as fh:
        rows = [json.loads(l) for l in fh]
    rows.sort(key=lambda r: -r["calls_30d"])
    random.seed(a.seed)
    hot = rows[:max(1, len(rows) // 50)]
    cold = [r for r in rows if r["calls_30d"] <= 6]
    sample = (random.sample(hot, min(a.sample // 2, len(hot)))
              + random.sample(cold, min(a.sample // 2, len(cold))))
    print("3. PROBE LIVE 402 RESPONSES (unpaid reads of third-party endpoints)")
    print("   'where do the payment terms live?' is answered by measurement, not by worry.")
    print("   pools: %d busiest, %d tail; drew %d + %d" %
          (len(hot), len(cold), min(a.sample // 2, len(hot)), min(a.sample // 2, len(cold))))
    announce_offdomain([r["url"] for r in sample])

    def one(r):
        out = {"url": r["url"], "code": None, "source": None, "accept_keys": [],
               "output_schema": False, "description_in_accept": False, "mime_type": False}
        try:
            for method, data in (("POST", b"{}"), ("GET", None)):
                c, hd, bd = fetch(r["url"], data=data, method=method, timeout=20, max_bytes=200_000)
                out["code"] = c
                if c == 402:
                    pay, src = envelope(hd, bd)
                    if pay:
                        acc = (pay.get("accepts") or pay.get("paymentRequirements") or [{}])[0]
                        out.update(source=src, accept_keys=sorted(acc.keys()),
                                   output_schema=bool(acc.get("outputSchema")),
                                   description_in_accept=bool(acc.get("description")),
                                   mime_type=bool(acc.get("mimeType")))
                    return out
        except Refused as e:
            out["code"] = "refused"
            out["note"] = str(e)[:140]
        return out

    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(one, sample))
    path = os.path.join(a.out, "live_probe.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    got = [r for r in res if r["source"]]
    hdr = [r for r in got if r["source"] == "header"]
    bdy = [r for r in got if r["source"] == "body"]
    print("   probed %d endpoints, decoded %d payloads -> %s" % (len(res), len(got), path))
    print("   terms delivered in the PAYMENT-REQUIRED header: %d" % len(hdr))
    print("   terms delivered only in the BODY (v1-style sellers): %d" % len(bdy))
    print("   accepts[0] declares outputSchema: %d | description: %d | mimeType: %d" %
          (sum(1 for r in got if r["output_schema"]),
           sum(1 for r in got if r["description_in_accept"]),
           sum(1 for r in got if r["mime_type"])))
    other = collections.Counter(str(r["code"]) for r in res if r["code"] != 402)
    print("   endpoints that did NOT answer 402:", dict(other) or "none")
    print("   Reading: copying accepts[] into your body buys v1-reader compatibility only,")
    print("   and changes no published conformance check. Do not touch an audited payment path")
    print("   for it unless a specific consumer is proven to need it.")
    print("   requests used: %d of %d budget" % (REQUEST_COUNT, REQUEST_BUDGET))
    return 0


def cmd_manifest(a):
    os.makedirs(a.out, exist_ok=True)
    seller = a.seller.rstrip("/")
    print("4. MANIFEST vs LIVE TRUTH for", seller)
    manifest, manifest_path = None, None
    for cand in ("/.well-known/x402", "/.well-known/x402.json", "/x402.json"):
        c, _, b = fetch(seller + cand, timeout=30)
        if c == 200:
            try:
                manifest, manifest_path = json.loads(b), cand
                print("   manifest:", cand, "(%d bytes)" % len(b))
                break
            except Exception:
                pass
    report = {"seller": seller, "manifest_path": manifest_path, "resources": 0, "entries": 0,
              "per_resource": [], "manifest_bytes": 0}
    if manifest is None:
        print("   NO discovery manifest answered 200. A crawler that reads it sees nothing,")
        print("   even when every paid endpoint is perfect.")
    else:
        report["resources"] = len(manifest.get("resources") or [])
        report["entries"] = len(manifest.get("entries") or [])
        report["manifest_bytes"] = len(json.dumps(manifest))
        print("   keys:", list(manifest.keys()))
        print("   resources: %d | entries: %d" % (report["resources"], report["entries"]))
        if not report["entries"]:
            print("   entries[] is absent, so price and description are not published per route.")
            print("   A crawler that wants 'route, price, description' from this file starves here.")
    urls = (manifest or {}).get("resources") or []
    off_preview = [u for u in urls[:a.limit] if u]
    if off_preview:
        announce_offdomain(off_preview)
    for u in urls[:a.limit]:
        try:
            c, hd, bd = fetch(u, data=b"{}", method="POST", timeout=20, max_bytes=200_000)
        except Refused as e:
            report["per_resource"].append({"url": u, "code": "refused", "note": str(e)[:140]})
            continue
        if c != 402:
            report["per_resource"].append({"url": u, "code": c, "note": "not 402"})
            continue
        pay, src = envelope(hd, bd)
        acc = ((pay or {}).get("accepts") or [{}])[0]
        report["per_resource"].append({"url": u, "code": c, "source": src,
                                       "amount": accept_amount(acc), "pay_to": acc.get("payTo"),
                                       "asset": acc.get("asset"), "network": acc.get("network")})
    path = os.path.join(a.out, "manifest_vs_live.json")
    with open(path, "w") as fh:
        json.dump(report, fh, indent=1)
    ok = [r for r in report["per_resource"] if r.get("code") == 402]
    print("   probed %d of %d resources, %d answered 402 -> %s" %
          (len(report["per_resource"]), min(len(urls), a.limit), len(ok), path))
    paytos = sorted({r.get("pay_to") for r in ok if r.get("pay_to")})
    assets = sorted({r.get("asset") for r in ok if r.get("asset")})
    print("   distinct payTo:", paytos, "| distinct asset:", assets)
    print("   Build entries[] from THESE measured values, keep every other key byte-identical,")
    print("   keep backups OUTSIDE the docroot (anything under it is published), then re-fetch")
    print("   the public URL and compare hashes before believing the change landed.")
    print("   requests used: %d of %d budget" % (REQUEST_COUNT, REQUEST_BUDGET))
    return 0


def main():
    global ALLOW_ANY_HOST
    # The off-domain flag is accepted in EITHER position (before or after the subcommand),
    # because an operator should not lose a run to argument order.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--allow-any-host", dest="allow_any_sub", action="store_true",
                        default=argparse.SUPPRESS,
                        help="opt-in: also read hosts outside DOCUMENTED_HOSTS (each host is printed before it is read)")

    ap = argparse.ArgumentParser(description="measure the x402 market, read-only")
    ap.add_argument("--allow-any-host", dest="allow_any", action="store_true",
                    help="opt-in: also read hosts outside DOCUMENTED_HOSTS (each host is printed before it is read)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("census", parents=[common], help="sweep the registry and print the demand scoreboard")
    c.add_argument("--out", default="./recon")
    c.add_argument("--pages", type=int, default=0, help="0 = all pages")
    c.set_defaults(func=cmd_census)

    p = sub.add_parser("probe", parents=[common], help="unpaid probes of live 402 endpoints")
    p.add_argument("--out", default="./recon")
    p.add_argument("--sample", type=int, default=30)
    p.add_argument("--seed", type=int, default=7)
    p.set_defaults(func=cmd_probe)

    m = sub.add_parser("manifest", parents=[common], help="compare a manifest against live 402 truth")
    m.add_argument("--seller", required=True)
    m.add_argument("--out", default="./recon")
    m.add_argument("--limit", type=int, default=40)
    m.set_defaults(func=cmd_manifest)

    a = ap.parse_args()
    ALLOW_ANY_HOST = bool(getattr(a, "allow_any", False) or getattr(a, "allow_any_sub", False))
    print("x402 market recon - measured at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("mode: READ-ONLY. No key is read, nothing is signed, nothing is spent.")
    if ALLOW_ANY_HOST:
        print("--allow-any-host is ON: off-domain hosts may be contacted this run, and each one")
        print("is printed before it is read. Private, loopback and link-local stay refused.")
    try:
        rc = a.func(a)
    except Refused as e:
        print(e)
        rc = 3
    if a.cmd == "probe":
        print("")
        print("What the directory scorecards measure (read their check lists, not a summary):")
        print("  payment-ready comes from a free automatic unpaid probe and DECAYS when probes")
        print("  start failing; verified is earned only by a paid delivery probe and cannot be")
        print("  self-declared. Ownership verification is a signature by the payTo key, so a")
        print("  smart-contract payTo can never produce one - publish your own evidence instead.")
        print("  One public router states its order as task match, crawl health, distinct payers")
        print("  over 30 days, price, curated flag, shorter slug first, and it routes a seller")
        print("  with no settlement history last, capped low. Quote that together with its source.")
    print("")
    print("Report the numbers with their unit and their source. An unlabelled figure invites")
    print("each reader to supply their own definition, and yours will look wrong.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
