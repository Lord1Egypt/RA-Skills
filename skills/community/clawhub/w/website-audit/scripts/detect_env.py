#!/usr/bin/env python3
"""Report which audit tier this environment supports (A, B or C) with evidence.

Usage: python detect_env.py [https://target.example]
A = no usable network/shell for the target (static fetch tool only)
B = scripts can reach the target
C = B plus a headless browser or Lighthouse is installed
"""
import argparse
import os
import platform
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import (PROXY_CAVEAT, add_common_args, emit, fetch, fetch_kwargs, normalize_url,  # noqa: E402
                   now_iso, proxy_env)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    add_common_args(ap)
    args = ap.parse_args()

    tools = {n: shutil.which(n) for n in ("curl", "node", "npx", "lighthouse", "chromium",
                                          "chromium-browser", "google-chrome", "chrome")}
    out = {"tool": "detect_env", "checked_at": now_iso(), "python": platform.python_version(),
           "tools_found": {k: v for k, v in tools.items() if v}}
    out["proxy_variables_set"] = proxy_env()
    if out["proxy_variables_set"]:
        out["proxy_note"] = PROXY_CAVEAT
    reachable = None
    if args.url:
        r = fetch(normalize_url(args.url), read_body=False, **fetch_kwargs(args))
        reachable = r["error"] is None
        out["network_test"] = {"url": r["url"], "reachable": reachable, "status": r["status"],
                               "error": r["error"]}
    has_browser = any(tools.get(n) for n in ("lighthouse", "chromium", "chromium-browser",
                                             "google-chrome", "chrome"))
    if reachable is None:
        out["tier"] = "unknown"
        out["note"] = "No URL given, so network access to the target was not tested."
    elif not reachable:
        out["tier"] = "A"
        out["note"] = ("Scripts cannot reach the target from here. Use the page-fetch tool "
                       "only and mark header/redirect/link checks as Not checked.")
    elif has_browser:
        out["tier"] = "C"
    else:
        out["tier"] = "B"
    emit(out)


if __name__ == "__main__":
    main()
