#!/usr/bin/env python3
"""Rendered-page checks via Lighthouse (Tier C): Core Web Vitals (lab) + rendered accessibility.

Usage: python check_rendered.py https://example.com/page [--preset mobile|desktop]
                                [--lighthouse-bin PATH] [--chrome-path PATH]
                                [--allow-private] [--timeout 240]

This is a thin wrapper: Lighthouse (Node) does the rendering and measuring; this script
only finds the tools, runs one Lighthouse pass, and translates its report (LHR) into the
same issue format as the other scripts, so merge_reports.py can combine them unchanged.

Honesty rules, same as the rest of the skill:
- Every number below is copied from the LHR. Nothing is estimated.
- Lab data is not field data: one run, emulated device and throttling. Findings are
  labelled confidence "likely" for that reason, and the caveats say so.
- INP is usually not measurable in a lab run. When Lighthouse returns no INP value this
  script reports that plainly and uses Total Blocking Time only as a labelled proxy;
  it never invents an INP number.
- If Lighthouse or Chrome is missing, or the run fails, the output is
  {"status": "not_checked", ...} with exit code 2, exactly like the other scripts.
- The same SSRF guard as the other scripts applies up front: non-public targets are
  refused unless --allow-private (Chrome would resolve the name itself, so the check
  here is a pre-flight refusal, not a network sandbox).
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (add_common_args, blocked_reason, emit, make_issue, normalize_url, now_iso,  # noqa: E402
                   proxy_env)

# Thresholds are the Core Web Vitals "good" bounds (web.dev/vitals). Severity mapping is
# deterministic and documented in references/performance.md.
LCP_GOOD_S = 2.5
LCP_POOR_S = 4.0
CLS_GOOD = 0.1
CLS_POOR = 0.25
INP_GOOD_MS = 200
INP_POOR_MS = 500
TBT_PROXY_MS = 200       # lab proxy hint only; TBT is not INP
TBT_PROXY_BAD_MS = 600


def find_lighthouse(arg):
    if arg:
        return arg if os.path.isfile(arg) and os.access(arg, os.X_OK) else None
    env = os.environ.get("LIGHTHOUSE_BIN")
    if env and os.path.isfile(env):
        return env
    return shutil.which("lighthouse")


def find_chrome(arg):
    if arg:
        return arg if os.path.isfile(arg) else None
    env = os.environ.get("CHROME_PATH")
    if env and os.path.isfile(env):
        return env
    for name in ("google-chrome", "chrome", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    cache_dirs = [os.path.expanduser("~/.cache/puppeteer")]
    if os.environ.get("PUPPETEER_CACHE_DIR"):
        cache_dirs.insert(0, os.environ["PUPPETEER_CACHE_DIR"])
    for base in cache_dirs:
        hits = sorted(glob.glob(os.path.join(base, "chrome", "*", "chrome-linux64", "chrome")))
        if hits:
            return hits[-1]
    return None


def metric(audits, audit_id):
    a = audits.get(audit_id) or {}
    return {"display": a.get("displayValue"), "numeric": a.get("numericValue"),
            "unit": a.get("numericUnit"), "score": a.get("score")}


def failing_nodes(audit):
    items = ((audit.get("details") or {}).get("items")) or []
    out = []
    for it in items[:5]:
        node = it.get("node") or {}
        out.append(node.get("snippet") or node.get("selector") or str(it)[:120])
    return out


def translate(lhr, url):
    audits = lhr.get("audits", {})
    cats = lhr.get("categories", {})
    issues = []
    meas = {"lighthouse_version": lhr.get("lighthouseVersion"),
            "fetch_time": lhr.get("fetchTime"),
            "final_url": lhr.get("finalDisplayedUrl") or lhr.get("finalUrl") or url,
            "scores": {k: (v or {}).get("score") for k, v in cats.items()},
            "metrics": {}}
    for mid, aid in (("lcp", "largest-contentful-paint"), ("cls", "cumulative-layout-shift"),
                     ("inp", "interaction-to-next-paint"), ("tbt", "total-blocking-time"),
                     ("fcp", "first-contentful-paint"), ("speed_index", "speed-index")):
        meas["metrics"][mid] = metric(audits, aid)

    lcp = meas["metrics"]["lcp"]["numeric"]
    if lcp is not None:
        s = lcp / 1000.0
        if s > LCP_POOR_S:
            issues.append(make_issue("cwv.lcp_slow", "performance", "high",
                                     "Largest Contentful Paint is %.2fs in this lab run (poor is over %.1fs)."
                                     % (s, LCP_POOR_S),
                                     evidence={"lcp_display": meas["metrics"]["lcp"]["display"],
                                               "lcp_seconds": round(s, 2)}, confidence="likely"))
        elif s > LCP_GOOD_S:
            issues.append(make_issue("cwv.lcp_slow", "performance", "medium",
                                     "Largest Contentful Paint is %.2fs in this lab run (good is %.1fs or less)."
                                     % (s, LCP_GOOD_S),
                                     evidence={"lcp_display": meas["metrics"]["lcp"]["display"],
                                               "lcp_seconds": round(s, 2)}, confidence="likely"))
    cls = meas["metrics"]["cls"]["numeric"]
    if cls is not None:
        if cls > CLS_POOR:
            issues.append(make_issue("cwv.cls_high", "performance", "high",
                                     "Cumulative Layout Shift is %.3f in this lab run (poor is over %.2f)."
                                     % (cls, CLS_POOR),
                                     evidence={"cls": cls}, confidence="likely"))
        elif cls > CLS_GOOD:
            issues.append(make_issue("cwv.cls_high", "performance", "medium",
                                     "Cumulative Layout Shift is %.3f in this lab run (good is %.2f or less)."
                                     % (cls, CLS_GOOD),
                                     evidence={"cls": cls}, confidence="likely"))
    inp = meas["metrics"]["inp"]["numeric"]
    if inp is not None:
        if inp > INP_POOR_MS:
            issues.append(make_issue("cwv.inp_slow", "performance", "high",
                                     "Interaction to Next Paint is %dms in this run (poor is over %dms)."
                                     % (inp, INP_POOR_MS), evidence={"inp_ms": inp}, confidence="likely"))
        elif inp > INP_GOOD_MS:
            issues.append(make_issue("cwv.inp_slow", "performance", "medium",
                                     "Interaction to Next Paint is %dms in this run (good is %dms or less)."
                                     % (inp, INP_GOOD_MS), evidence={"inp_ms": inp}, confidence="likely"))
    else:
        meas["inp_note"] = ("Lighthouse returned no INP value (normal for a lab run with no scripted "
                            "interaction). INP is therefore NOT measured here; Total Blocking Time "
                            "below is a lab proxy only, not an INP score.")
        tbt = meas["metrics"]["tbt"]["numeric"]
        if tbt is not None and tbt > TBT_PROXY_MS:
            issues.append(make_issue("cwv.tbt_high", "performance", "medium" if tbt > TBT_PROXY_BAD_MS else "low",
                                     "Total Blocking Time is %dms in this lab run. TBT correlates with "
                                     "responsiveness but is not INP." % tbt,
                                     evidence={"tbt_ms": tbt, "tbt_display": meas["metrics"]["tbt"]["display"]},
                                     confidence="likely"))

    manual = []
    a11y_refs = ((cats.get("accessibility") or {}).get("auditRefs")) or []
    for ref in a11y_refs:
        a = audits.get(ref.get("id")) or {}
        mode = a.get("scoreDisplayMode")
        if mode == "manual":
            manual.append(a.get("id"))
        elif mode == "binary" and a.get("score") == 0:
            nodes = failing_nodes(a)
            issues.append(make_issue("a11y." + a.get("id", "unknown"), "accessibility", "medium",
                                     "Lighthouse accessibility check failed: %s" % (a.get("title") or a.get("id")),
                                     evidence={"audit": a.get("id"), "title": a.get("title"),
                                               "failing_elements": nodes},
                                     confidence="likely"))
    meas["accessibility_manual_checks_not_done"] = manual
    return meas, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--preset", choices=("mobile", "desktop"), default="mobile")
    ap.add_argument("--lighthouse-bin")
    ap.add_argument("--chrome-path")
    ap.add_argument("--ignore-cert-errors", action="store_true",
                    help="pass --ignore-certificate-errors to Chrome (for TLS-intercepting proxies; "
                         "the run is then labelled, and TLS itself stays check_headers.py's job)")
    ap.add_argument("--proxy-server",
                    help="proxy for Chrome, e.g. http://127.0.0.1:18080. Overrides the environment's "
                         "proxy variables. Needed when the real proxy requires credentials embedded "
                         "in its URL: Chrome rejects those in --proxy-server, so run a local relay "
                         "that injects the auth and point this at the relay.")
    ap.add_argument("--run-timeout", type=float, default=240.0, help="whole Lighthouse run timeout, seconds")
    add_common_args(ap)
    args = ap.parse_args()
    url = normalize_url(args.url)
    out = {"tool": "check_rendered", "tier": "C", "checked_at": now_iso(), "target": url, "errors": []}

    def not_checked(msg):
        out["errors"].append({"url": url, "error": msg})
        out["status"] = "not_checked"
        emit(out)
        sys.exit(2)

    reason = blocked_reason(url, args.allow_private)
    if reason:
        not_checked(reason)
    lh = find_lighthouse(args.lighthouse_bin)
    if not lh:
        not_checked("Lighthouse not found (looked at --lighthouse-bin, $LIGHTHOUSE_BIN, PATH). "
                    "Install it with: npm install -g lighthouse")
    chrome = find_chrome(args.chrome_path)
    if not chrome:
        not_checked("No Chrome/Chromium found (looked at --chrome-path, $CHROME_PATH, PATH, Puppeteer cache).")

    out["environment"] = {"lighthouse_bin": lh, "chrome_path": chrome, "preset": args.preset,
                          "proxy_variables_set": proxy_env(),
                          "ignore_cert_errors": bool(args.ignore_cert_errors)}
    with tempfile.TemporaryDirectory(prefix="wa-lhr-") as td:
        lhr_path = os.path.join(td, "lhr.json")
        flags = ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage"]
        # Behind a proxy (corporate network, sandbox), Chrome needs the proxy spelled out;
        # urllib-based scripts get it from the environment automatically, Chrome does not.
        # The proxy VALUE is used here only and never printed (it may hold credentials).
        proxy = (args.proxy_server or os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
                 or os.environ.get("all_proxy") or os.environ.get("ALL_PROXY")
                 or os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"))
        if proxy:
            flags.append("--proxy-server=" + proxy)
        if args.ignore_cert_errors:
            flags.append("--ignore-certificate-errors")
        cmd = [lh, url, "--output=json", "--output-path=" + lhr_path,
               "--only-categories=performance,accessibility",
               "--chrome-path=" + chrome,
               "--chrome-flags=" + " ".join(flags),
               "--quiet"]
        if args.preset == "desktop":
            # Lighthouse's --preset accepts perf/experimental/desktop; "mobile" is not a
            # preset name — mobile emulation is the default when no preset is passed.
            cmd.append("--preset=desktop")
        env = dict(os.environ, CHROME_PATH=chrome)  # chrome-launcher honours this reliably
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.run_timeout, env=env)
        except subprocess.TimeoutExpired:
            not_checked("Lighthouse run timed out after %ss." % args.run_timeout)
        except OSError as e:
            not_checked("Could not start Lighthouse: %s" % e)
        if not os.path.isfile(lhr_path):
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()
            not_checked("Lighthouse produced no report (exit %s): %s"
                        % (proc.returncode, tail[-1][:300] if tail else "no output"))
        try:
            with open(lhr_path, encoding="utf-8") as f:
                lhr = json.load(f)
        except ValueError as e:
            not_checked("Lighthouse report was not valid JSON: %s" % e)
        # Lighthouse can exit non-zero AND still write a report whose audits are all in
        # "error" mode (e.g. Chrome showed an interstitial). That is not a measurement:
        # report it as not checked, quoting Lighthouse's own runtime error.
        runtime_error = (lhr.get("runtimeError") or {}).get("message")
        scores = [((c or {}).get("score")) for c in (lhr.get("categories") or {}).values()]
        if runtime_error or (scores and all(s is None for s in scores)):
            not_checked("Lighthouse run failed: %s" % (runtime_error or "all category scores are null"))

    meas, issues = translate(lhr, url)
    out["measurements"] = meas
    out["issues"] = issues
    out["caveats"] = ["Lab data from ONE Lighthouse run with an emulated device and throttling; "
                      "it is not field data (no CrUX) and varies between runs.",
                      "Rendered checks see the page as this Chrome rendered it; logged-in or "
                      "geo-personalised content is not covered."]
    if args.ignore_cert_errors:
        out["caveats"].append("This run used --ignore-certificate-errors, so it says nothing about "
                               "the site's TLS; certificate findings belong to check_headers.py.")
    emit(out)


if __name__ == "__main__":
    main()
