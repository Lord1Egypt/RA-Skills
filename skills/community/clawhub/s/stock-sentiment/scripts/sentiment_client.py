#!/usr/bin/env python3
"""Minimal, read-only stdlib client for the SentiSense API.

No third-party packages. Reads SENTISENSE_API_KEY from the environment, injects
the X-SentiSense-API-Key header, prepends the base URL, and normalizes the two
response envelopes so callers reason over clean values. Every endpoint is a GET;
nothing here can trade, move money, or modify account state.

Usage:
  python sentiment_client.py sentiment NVDA
  python sentiment_client.py mood
  python sentiment_client.py cluster-buys --days 30
  python sentiment_client.py peers ZS
  python sentiment_client.py mentions ZS --start 1787184000000 --end 1790467200000

A free-tier preview is a slice of the window, not the window: shaped output keeps
totalCount next to the rows so a slice is never read as a complete tally.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ORIGIN = "https://app.sentisense.ai"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sentisense_api_url(path, params=None):
    """Return a validated API URL at the one origin allowed to receive the key."""
    url = urllib.parse.urljoin(API_ORIGIN + "/", path)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "app.sentisense.ai"
            or parsed.netloc != "app.sentisense.ai"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None):
        raise ValueError("API URL must use https://app.sentisense.ai with no credentials or port")
    if params:
        url += ("&" if parsed.query else "?") + urllib.parse.urlencode(params)
    return url


def get(path, **params):
    """GET the fixed API origin with the auth header; returns parsed JSON or exits non-zero."""
    params = {k: v for k, v in params.items() if v is not None}
    url = sentisense_api_url(path, params)
    key = os.environ.get("SENTISENSE_API_KEY")
    if not key:
        sys.exit("SENTISENSE_API_KEY is not set "
                 "(free key: https://app.sentisense.ai/get-api-key)")
    req = urllib.request.Request(url, headers={"X-SentiSense-API-Key": key})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        retry = e.headers.get("Retry-After")
        hint = f" (Retry-After: {retry}s)" if retry else ""
        detail = ""
        try:
            body = json.loads(e.read().decode("utf-8", "replace"))
            if isinstance(body, dict):
                detail = f": {body.get('error', '')} {body.get('message', '')}".rstrip()
                names = [x.get("ticker") or x.get("urlSlug") or x.get("name")
                         for x in body.get("suggestions") or [] if isinstance(x, dict)]
                if names:
                    detail += f" (suggestions: {', '.join(str(n) for n in names if n)})"
        except (ValueError, OSError):
            pass
        sys.exit(f"HTTP {e.code} on {path}{hint}{detail}")
    except urllib.error.URLError as e:
        hint = ("  (CA certs missing: common on macOS python.org installs. Run the bundled "
                "'Install Certificates.command', or use the system python3, or plain curl.)"
                if "CERTIFICATE_VERIFY_FAILED" in str(e.reason) else "")
        sys.exit(f"network error on {path}: {e.reason}{hint}")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # A 200 with a non-JSON body (maintenance page, WAF/captcha, truncation).
        sys.exit(f"non-JSON response from {path}: {e}")


def rows(raw):
    """Wrap-vs-flat: bare arrays and flat dicts pass through; {..., data} unwraps."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "data" in raw:
        return raw["data"]
    return raw


def get_all(path, page_size=500, **params):
    """Walk a paged {isPreview, totalCount, data} feed to the end of its window.

    One call is one page, not the window: keep requesting while
    offset + len(data) < totalCount. A preview envelope stops after the first page,
    since FREE keys cannot page past their slice. Returns the first envelope with
    `data` holding every row."""
    first = get(path, limit=page_size, offset=0, **params)
    if not isinstance(first, dict) or "data" not in first or first.get("isPreview"):
        return first
    data, total = list(first["data"]), first.get("totalCount")
    while isinstance(total, int) and len(data) < total:
        page = get(path, limit=page_size, offset=len(data), **params)
        batch = page.get("data", []) if isinstance(page, dict) else []
        if not batch:
            break
        data.extend(batch)
    return {**first, "data": data}


def _returned(data):
    """Rows actually returned: a list's length, or the calendar's data.earnings length."""
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict) and isinstance(data.get("earnings"), list):
        return len(data["earnings"])
    return None


def shaped(raw):
    """Like rows(), but keep what a caller needs to label a partial result.

    A preview (or any envelope whose totalCount exceeds the rows returned) is a slice of
    the window, not the window: keep isPreview, previewReason, totalCount and the returned
    count beside data, with a note, so nobody tallies the slice as the whole window or
    reads a missing row as an absence. A complete envelope returns the bare rows."""
    if not (isinstance(raw, dict) and "data" in raw):
        return rows(raw)
    total, returned = raw.get("totalCount"), _returned(raw["data"])
    partial = isinstance(total, int) and returned is not None and total > returned
    if raw.get("isPreview") or partial:
        out = {"isPreview": bool(raw.get("isPreview")), "previewReason": raw.get("previewReason"),
               "totalCount": total, "returned": returned}
        if partial:
            meta = raw["data"].get("metadata") if isinstance(raw["data"], dict) else None
            if isinstance(meta, dict) and meta.get("windowStart"):
                out["note"] = (f"covers {meta.get('windowStart')} to {meta.get('windowEnd')} only: "
                               f"{returned} of {total} matching events; the rest fall outside this "
                               "window, they are not unscheduled")
            else:
                out["note"] = (f"slice: {returned} of {total} in the window; do not infer absence "
                               "or a complete tally from it")
        out["data"] = raw["data"]
        return out
    return rows(raw)


def sentiment_scalar(series):
    """Latest reading of a metric series, read from the flat top-level `value`.

    Every point carries `value` alongside the nested `metricValue`, and it holds the scalar
    for every metric type. Prefer it: the nested depth is not uniform, since a value metric
    nests at metricValue.value.value while a count metric like `mentions` puts the integer
    at metricValue.value. The nested read stays as a fallback for a point without `value`."""
    if not series:
        return None
    point = series[-1]
    flat = point.get("value")
    if flat is not None:
        return float(flat)
    nested = (point.get("metricValue") or {}).get("value")
    if isinstance(nested, dict):
        nested = nested.get("value")
    return None if nested is None else float(nested)


def out(obj):
    print(json.dumps(obj, indent=2, default=str))


def metric(ticker, slug, start=None, end=None):
    return get(f"/api/v2/metrics/entity/{urllib.parse.quote(ticker.upper(), safe='')}/metric/{slug}",
               startTime=start, endTime=end)


def cmd_series(a, slug):
    series = metric(a.ticker, slug, getattr(a, "start", None), getattr(a, "end", None))
    pts = series if isinstance(series, list) else []
    last = pts[-1] if pts else {}
    result = {"metric": slug, "ticker": a.ticker.upper(), "points": len(pts),
              "latest": sentiment_scalar(pts), "latestTimestamp": last.get("timestamp")}
    if slug == "sentisense":
        # Direction lives on the sentisense series: that day's bull, bear and directional.
        result["latestProperties"] = (last.get("metricValue") or {}).get("properties")
    if getattr(a, "points", False):
        result["series"] = [{"timestamp": p.get("timestamp"), "value": p.get("value"),
                             "properties": (p.get("metricValue") or {}).get("properties")}
                            for p in pts]
    out(result)


def cmd_peers(a):
    """Curated peer slugs for workflow 6; each slug works as a metric handle."""
    g = get(f"/api/v1/stocks/{urllib.parse.quote(a.ticker.upper(), safe='')}/graph", depth=1, cap=75)
    names = {n.get("slug"): n.get("displayName") for n in g.get("nodes", [])}
    peers = (g.get("groups") or {}).get("peers", [])
    out({"ticker": g.get("ticker"), "root": g.get("root"), "truncated": g.get("truncated"),
         "peers": [{"slug": p, "displayName": names.get(p)} for p in peers]})


def cmd_mood(_a):
    m = get("/api/v2/market-mood")
    market = m.get("market", {})
    sectors = m.get("sectors", {})
    # Dedupe overlapping GICS labels (e.g. "Health Care" vs "Healthcare",
    # "Information Technology" vs "Technology"), keeping the highest-scoring
    # variant, before ranking top/bottom.
    alias = {"information technology": "technology", "health care": "healthcare"}
    canon = lambda s: alias.get(s.strip().lower(), s.strip().lower())
    best = {}
    for label, v in sectors.items():
        k = canon(label)
        if k not in best or v.get("currentScore", 0) > best[k][1].get("currentScore", 0):
            best[k] = (label, v)
    ranked = sorted(best.values(), key=lambda kv: kv[1].get("currentScore", 0), reverse=True)
    out({"score": market.get("currentScore"), "phase": market.get("phase"),
         "weeklyChange": market.get("weeklyChange"),
         "signals": market.get("signals", []),
         "topSectors": [k for k, _ in ranked[:3]],
         "bottomSectors": [k for k, _ in ranked[-3:]]})


def cmd_holders(a):
    quarters = get("/api/v1/institutional/quarters")  # bare array, newest first
    if not quarters:
        sys.exit("no institutional quarters available")
    # Skip a quarter still filing (pending: true); fall back to [0] only if all are pending.
    settled = [q for q in quarters if not q.get("pending")]
    q = (settled or quarters)[0].get("reportDate")
    out(shaped(get(f"/api/v1/institutional/holders/{urllib.parse.quote(a.ticker.upper(), safe='')}", reportDate=q)))


def main():
    p = argparse.ArgumentParser(description="Read-only SentiSense API client.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def simple(name):
        return sub.add_parser(name)

    def ticker_cmd(name, *opts):
        sp = sub.add_parser(name)
        sp.add_argument("ticker")
        for o, d in opts:
            sp.add_argument(o, default=d)
        return sp

    # sentiment / score / mentions / social dominance time series
    for name in ("sentiment", "score", "mentions", "dominance"):
        s = ticker_cmd(name)
        s.add_argument("--start", help="epoch milliseconds")
        s.add_argument("--end", help="epoch milliseconds")
        s.add_argument("--points", action="store_true", help="print every point, not just the latest")
    ticker_cmd("peers")
    simple("mood")
    # AI insights
    ticker_cmd("insights"); simple("market-insights"); ticker_cmd("insight-types")
    # smart money
    cb = simple("cluster-buys"); cb.add_argument("--days", default="7")
    ticker_cmd("insider", ("--days", "90"))
    cg = simple("congress"); cg.add_argument("--days", default="7")
    ticker_cmd("filings", ("--days", "90"))
    ticker_cmd("holders"); ticker_cmd("consensus")
    ticker_cmd("actions", ("--days", "90")); ticker_cmd("estimates")
    aa = simple("analyst-activity"); aa.add_argument("--days", default="7")
    aa.add_argument("--action-types", default=None)  # CSV, e.g. UPGRADE,DOWNGRADE,INITIATE
    # calendar / news / stories / quotes
    ticker_cmd("earnings")
    ticker_cmd("news", ("--limit", "8"))
    st = simple("stories"); st.add_argument("--ticker"); st.add_argument("--limit", default="10")
    ticker_cmd("price")
    ch = ticker_cmd("chart"); ch.add_argument("--timeframe", default="1M")
    simple("popular")

    a = p.parse_args()
    t = getattr(a, "ticker", None)
    T = t.upper() if t else None
    TE = urllib.parse.quote(T, safe="") if T else None  # percent-encoded for URL path segments
    days = getattr(a, "days", None)

    if a.cmd == "sentiment":
        cmd_series(a, "sentiment")
    elif a.cmd == "score":
        cmd_series(a, "sentisense")
    elif a.cmd == "mentions":
        cmd_series(a, "mentions")
    elif a.cmd == "dominance":
        cmd_series(a, "social_dominance")
    elif a.cmd == "mood":
        cmd_mood(a)
    elif a.cmd == "peers":
        cmd_peers(a)
    elif a.cmd == "insights":
        out(shaped(get(f"/api/v1/insights/stock/{TE}")))
    elif a.cmd == "market-insights":
        out(shaped(get("/api/v1/insights/market")))
    elif a.cmd == "insight-types":
        out(get(f"/api/v1/insights/stock/{TE}/types"))
    elif a.cmd == "cluster-buys":
        out(shaped(get("/api/v1/insider/cluster-buys", lookbackDays=days)))
    elif a.cmd == "insider":
        out(shaped(get(f"/api/v1/insider/trades/{TE}", lookbackDays=days)))
    elif a.cmd == "congress":
        out(shaped(get_all("/api/v1/politicians/activity", lookbackDays=days)))
    elif a.cmd == "filings":
        out(shaped(get(f"/api/v1/politicians/filings/{TE}", lookbackDays=days)))
    elif a.cmd == "holders":
        cmd_holders(a)
    elif a.cmd == "consensus":
        out(shaped(get(f"/api/v1/analyst/{TE}/consensus")))
    elif a.cmd == "actions":
        out(shaped(get(f"/api/v1/analyst/{TE}/actions", lookbackDays=days)))
    elif a.cmd == "estimates":
        out(shaped(get(f"/api/v1/analyst/{TE}/estimates")))
    elif a.cmd == "analyst-activity":
        out(shaped(get_all("/api/v1/analyst/activity", lookbackDays=days,
                       actionTypes=getattr(a, "action_types", None))))
    elif a.cmd == "earnings":
        out(shaped(get("/api/v1/calendar/earnings", ticker=T)))
    elif a.cmd == "news":
        raw = get(f"/api/v1/documents/ticker/{TE}", limit=a.limit)
        out({"totalCount": raw.get("totalCount"), "documents": raw.get("documents", [])})
    elif a.cmd == "stories":
        path = (f"/api/v1/documents/stories/ticker/{urllib.parse.quote(a.ticker.upper(), safe='')}"
                if a.ticker else "/api/v1/documents/stories")
        out(shaped(get(path, limit=a.limit)))
    elif a.cmd == "price":
        out(get("/api/v1/stocks/price", ticker=T))
    elif a.cmd == "chart":
        out(get("/api/v1/stocks/chart", ticker=T, timeframe=a.timeframe))
    elif a.cmd == "popular":
        out(get("/api/v1/stocks/popular"))


if __name__ == "__main__":
    main()
