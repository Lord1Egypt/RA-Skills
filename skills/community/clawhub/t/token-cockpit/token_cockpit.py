#!/usr/bin/env python3
"""
token_cockpit.py - See and slash your OpenClaw / LLM token bill.

Reads local usage logs (no API key, nothing leaves your machine), prices them
with an editable model-price table, and tells you where the money goes:

  report    - spend + token breakdown by model, with a monthly projection
  budget    - compare spend to a budget and emit an alert if you're over/close
  route     - find expensive-model calls that could run on a cheaper model
  simulate  - what-if savings from moving one model's traffic to another

Usage:
  python token_cockpit.py report   [--logs PATH] [--days N] [--json]
  python token_cockpit.py budget   --limit 50 [--period month] [--logs PATH]
  python token_cockpit.py route    [--logs PATH] [--small-tokens 2000]
  python token_cockpit.py simulate --from claude-opus --to claude-haiku [--logs PATH]

Prices are EDITABLE DEFAULTS (USD per 1M tokens) and change over time - override
with --pricing pricing.json. Confirm current prices before quoting hard numbers.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --------------------------------------------------------------------------- #
# Editable default price table: name-substring -> (input $/1M, output $/1M)
# These are DEFAULTS and drift over time. Override with --pricing pricing.json.
# Order matters: more specific substrings first.
# --------------------------------------------------------------------------- #

DEFAULT_PRICES = [
    ("gpt-4o-mini", (0.15, 0.60)),
    ("gpt-4.1-mini", (0.40, 1.60)),
    ("gpt-4.1", (2.00, 8.00)),
    ("gpt-4o", (2.50, 10.00)),
    ("o3-mini", (1.10, 4.40)),
    ("o3", (10.00, 40.00)),
    ("claude-3-opus", (15.00, 75.00)),
    ("claude-opus", (15.00, 75.00)),
    ("opus", (15.00, 75.00)),
    ("claude-3-5-sonnet", (3.00, 15.00)),
    ("claude-sonnet", (3.00, 15.00)),
    ("sonnet", (3.00, 15.00)),
    ("claude-3-5-haiku", (0.80, 4.00)),
    ("claude-haiku", (1.00, 5.00)),
    ("haiku", (1.00, 5.00)),
    ("gemini-1.5-flash", (0.075, 0.30)),
    ("gemini-flash", (0.10, 0.40)),
    ("gemini-2.5-pro", (1.25, 10.00)),
    ("gemini-pro", (1.25, 10.00)),
    ("deepseek", (0.27, 1.10)),
    ("llama", (0.20, 0.20)),
    ("mistral", (0.25, 0.25)),
]

# Cheaper alternatives suggested by the router, in rough quality tiers.
DOWNGRADE_HINTS = {
    "opus": "claude-haiku (or claude-sonnet for harder tasks)",
    "sonnet": "claude-haiku",
    "gpt-4o": "gpt-4o-mini",
    "gpt-4.1": "gpt-4.1-mini",
    "o3": "o3-mini",
    "gemini-pro": "gemini-flash",
}

LOG_CANDIDATES = [
    os.environ.get("OPENCLAW_USAGE_LOG", ""),
    "~/.openclaw/usage.jsonl",
    "~/.openclaw/logs/usage.jsonl",
    "~/.openclaw/usage.json",
    "/data/.openclaw/usage.jsonl",
    "/data/.openclaw/logs/usage.jsonl",
]


# --------------------------------------------------------------------------- #
# Pricing
# --------------------------------------------------------------------------- #

def load_pricing(path: str | None):
    if path:
        data = json.loads(Path(os.path.expanduser(path)).read_text())
        # accept {"model": [in, out]} or {"model": {"input":..,"output":..}}
        rules = []
        for k, v in data.items():
            if isinstance(v, dict):
                rules.append((k.lower(), (float(v["input"]), float(v["output"]))))
            else:
                rules.append((k.lower(), (float(v[0]), float(v[1]))))
        return rules
    return DEFAULT_PRICES


def price_for(model: str, rules) -> tuple[float, float]:
    m = (model or "").lower()
    for key, price in rules:
        if key in m:
            return price
    return (0.0, 0.0)  # unknown model -> 0 cost, surfaced separately


# --------------------------------------------------------------------------- #
# Log loading (tolerant of field-name variants)
# --------------------------------------------------------------------------- #

MODEL_KEYS = ("model", "model_id", "modelId", "model_name")
IN_KEYS = ("input_tokens", "prompt_tokens", "tokens_in", "inputTokens", "input")
OUT_KEYS = ("output_tokens", "completion_tokens", "tokens_out", "outputTokens", "output")
TS_KEYS = ("timestamp", "ts", "time", "created_at", "date")


def _first(d: dict, keys, default=None):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def _coerce_event(raw: dict) -> dict | None:
    # usage may be nested under "usage"
    usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else raw
    model = _first(raw, MODEL_KEYS) or _first(usage, MODEL_KEYS)
    tin = _first(usage, IN_KEYS, 0)
    tout = _first(usage, OUT_KEYS, 0)
    ts = _first(raw, TS_KEYS)
    if model is None and not tin and not tout:
        return None
    try:
        tin, tout = int(tin or 0), int(tout or 0)
    except (TypeError, ValueError):
        return None
    return {"model": str(model or "unknown"), "in": tin, "out": tout, "ts": _parse_ts(ts)}


def _parse_ts(ts):
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        # epoch seconds or millis
        val = ts / 1000 if ts > 1e12 else ts
        try:
            return datetime.fromtimestamp(val, tz=timezone.utc)
        except (OSError, ValueError):
            return None
    s = str(ts).strip().replace("Z", "+00:00")
    for parse in (datetime.fromisoformat,):
        try:
            dt = parse(s)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def find_log(explicit: str | None) -> Path | None:
    for raw in ([explicit] if explicit else LOG_CANDIDATES):
        if not raw:
            continue
        p = Path(os.path.expanduser(raw))
        if p.is_file():
            return p
    return None


def load_events(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    rows = []
    if text.startswith("["):
        rows = json.loads(text)
    else:
        for line in text.splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    out = []
    for r in rows:
        if isinstance(r, dict):
            ev = _coerce_event(r)
            if ev:
                out.append(ev)
    return out


def filter_days(events: list[dict], days: int | None) -> list[dict]:
    if not days:
        return events
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    kept = [e for e in events if e["ts"] is None or e["ts"] >= cutoff]
    return kept


# --------------------------------------------------------------------------- #
# Aggregation + cost
# --------------------------------------------------------------------------- #

def summarize(events: list[dict], rules) -> dict:
    by_model = defaultdict(lambda: {"calls": 0, "in": 0, "out": 0, "cost": 0.0, "priced": True})
    total_cost = 0.0
    for e in events:
        pin, pout = price_for(e["model"], rules)
        cost = e["in"] / 1e6 * pin + e["out"] / 1e6 * pout
        m = by_model[e["model"]]
        m["calls"] += 1
        m["in"] += e["in"]
        m["out"] += e["out"]
        m["cost"] += cost
        if pin == 0 and pout == 0:
            m["priced"] = False
        total_cost += cost
    span = _span_days(events)
    return {
        "total_cost": total_cost,
        "total_calls": len(events),
        "by_model": dict(by_model),
        "span_days": span,
        "monthly_projection": (total_cost / span * 30) if span else None,
    }


def _span_days(events: list[dict]) -> float | None:
    times = [e["ts"] for e in events if e["ts"]]
    if len(times) < 2:
        return None
    delta = (max(times) - min(times)).total_seconds() / 86400
    return max(delta, 0.5)


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #

def render_report(s: dict) -> str:
    L = ["# Token Cockpit report", ""]
    L.append(f"- Total calls: **{s['total_calls']:,}**")
    L.append(f"- Total spend: **${s['total_cost']:.2f}**")
    if s["span_days"]:
        L.append(f"- Window: ~{s['span_days']:.1f} days")
    if s["monthly_projection"] is not None:
        L.append(f"- Projected monthly: **${s['monthly_projection']:.2f}**")
    L.append("")
    L.append("## By model")
    rows = sorted(s["by_model"].items(), key=lambda kv: kv[1]["cost"], reverse=True)
    for name, m in rows:
        share = (m["cost"] / s["total_cost"] * 100) if s["total_cost"] else 0
        note = "" if m["priced"] else "  ⚠ no price on file (counted as $0)"
        L.append(
            f"- **{name}** — ${m['cost']:.2f} ({share:.0f}%), "
            f"{m['calls']:,} calls, {m['in']:,} in / {m['out']:,} out{note}"
        )
    L.append("")
    if any(not m["priced"] for m in s["by_model"].values()):
        L.append("_Models marked ⚠ have no entry in the price table - add one via `--pricing` for accurate totals._")
    return "\n".join(L)


def budget_alert(s: dict, limit: float, period: str) -> dict:
    spend = s["monthly_projection"] if period == "month" and s["monthly_projection"] is not None else s["total_cost"]
    basis = "projected monthly" if (period == "month" and s["monthly_projection"] is not None) else "spend so far"
    pct = (spend / limit * 100) if limit else 0
    if pct >= 100:
        level, msg = "OVER", f"🔴 Over budget: {basis} ${spend:.2f} vs ${limit:.2f} limit ({pct:.0f}%)."
    elif pct >= 80:
        level, msg = "WARN", f"🟠 Approaching budget: {basis} ${spend:.2f} is {pct:.0f}% of your ${limit:.2f} limit."
    else:
        level, msg = "OK", f"🟢 Within budget: {basis} ${spend:.2f} is {pct:.0f}% of your ${limit:.2f} limit."
    return {"level": level, "message": msg, "spend": spend, "limit": limit, "pct": pct}


def route_suggestions(events: list[dict], rules, small_tokens: int) -> dict:
    """Find expensive-model calls small enough to likely run fine on a cheaper model."""
    suggestions = defaultdict(lambda: {"calls": 0, "current_cost": 0.0, "cheaper": None, "est_savings": 0.0})
    for e in events:
        pin, pout = price_for(e["model"], rules)
        if pin == 0 and pout == 0:
            continue
        total_tok = e["in"] + e["out"]
        hint_key = next((k for k in DOWNGRADE_HINTS if k in e["model"].lower()), None)
        if not hint_key or total_tok > small_tokens:
            continue
        cheaper_name = DOWNGRADE_HINTS[hint_key]
        cpin, cpout = price_for(cheaper_name.split()[0], rules)
        # Skip if the "cheaper" target isn't actually cheaper (e.g. gpt-4o-mini
        # matching the gpt-4o rule and pointing back at itself).
        if cpin >= pin and cpout >= pout:
            continue
        cur = e["in"] / 1e6 * pin + e["out"] / 1e6 * pout
        new = e["in"] / 1e6 * cpin + e["out"] / 1e6 * cpout
        s = suggestions[e["model"]]
        s["calls"] += 1
        s["current_cost"] += cur
        s["cheaper"] = cheaper_name
        s["est_savings"] += max(cur - new, 0)
    return dict(suggestions)


def render_route(sug: dict, small_tokens: int) -> str:
    if not sug:
        return (f"No obvious routing wins: no small (<{small_tokens:,} token) calls are "
                "running on premium models. Your model choice already looks efficient.")
    total = sum(v["est_savings"] for v in sug.values())
    L = ["# Routing opportunities", ""]
    L.append(f"Small tasks (<{small_tokens:,} tokens) currently on premium models:\n")
    for model, v in sorted(sug.items(), key=lambda kv: kv[1]["est_savings"], reverse=True):
        L.append(
            f"- **{v['calls']:,}** `{model}` calls → route to **{v['cheaper']}**: "
            f"save ~${v['est_savings']:.2f} (of ${v['current_cost']:.2f})"
        )
    L.append("")
    L.append(f"**Estimated total savings: ~${total:.2f}** over this window if those small calls were downgraded.")
    L.append("\n_Estimate assumes equal token counts on the cheaper model. Verify quality before switching defaults._")
    return "\n".join(L)


def simulate(events: list[dict], rules, frm: str, to: str) -> str:
    cur = new = moved = 0.0
    n = 0
    for e in events:
        if frm.lower() not in e["model"].lower():
            continue
        pin, pout = price_for(e["model"], rules)
        tpin, tpout = price_for(to, rules)
        c = e["in"] / 1e6 * pin + e["out"] / 1e6 * pout
        t = e["in"] / 1e6 * tpin + e["out"] / 1e6 * tpout
        cur += c
        new += t
        moved += c
        n += 1
    if n == 0:
        return f"No calls matched model '{frm}' in this window."
    saved = cur - new
    pct = (saved / cur * 100) if cur else 0
    return (f"Moving {n:,} '{frm}' calls → '{to}':\n"
            f"  current: ${cur:.2f}\n  after:   ${new:.2f}\n"
            f"  savings: ${saved:.2f} ({pct:.0f}%)\n"
            "  (Assumes identical token usage; check output quality before committing.)")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _load_or_exit(args) -> list[dict]:
    p = find_log(getattr(args, "logs", None))
    if not p:
        print(
            "Token Cockpit could not find a usage log.\n"
            "Point it at one: --logs /path/to/usage.jsonl\n"
            "Expected a JSONL or JSON array of events with a model name and input/output token counts.\n"
            "Auto-detect looked at: " + ", ".join(c for c in LOG_CANDIDATES if c),
            file=sys.stderr,
        )
        sys.exit(2)
    events = load_events(p)
    if not events:
        print(f"No usable usage events found in {p}", file=sys.stderr)
        sys.exit(2)
    return filter_days(events, getattr(args, "days", None))


def main(argv=None):
    ap = argparse.ArgumentParser(description="See and slash your token bill.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--logs", help="Path to usage log (JSONL or JSON array). Auto-detected if omitted.")
        p.add_argument("--pricing", help="Path to a pricing override JSON.")

    pr = sub.add_parser("report", help="Spend + token breakdown by model.")
    common(pr); pr.add_argument("--days", type=int); pr.add_argument("--json", action="store_true")

    pb = sub.add_parser("budget", help="Compare spend to a budget and emit an alert.")
    common(pb); pb.add_argument("--limit", type=float, required=True)
    pb.add_argument("--period", choices=["month", "window"], default="month")
    pb.add_argument("--days", type=int); pb.add_argument("--json", action="store_true")

    pt = sub.add_parser("route", help="Find premium-model calls that could be downgraded.")
    common(pt); pt.add_argument("--small-tokens", type=int, default=2000)
    pt.add_argument("--days", type=int); pt.add_argument("--json", action="store_true")

    psim = sub.add_parser("simulate", help="What-if savings of moving one model to another.")
    common(psim); psim.add_argument("--from", dest="frm", required=True)
    psim.add_argument("--to", required=True); psim.add_argument("--days", type=int)

    args = ap.parse_args(argv)
    rules = load_pricing(getattr(args, "pricing", None))
    events = _load_or_exit(args)

    if args.cmd == "report":
        s = summarize(events, rules)
        print(json.dumps(s, default=str, indent=2) if args.json else render_report(s))
    elif args.cmd == "budget":
        s = summarize(events, rules)
        alert = budget_alert(s, args.limit, args.period)
        print(json.dumps(alert, indent=2) if args.json else alert["message"])
    elif args.cmd == "route":
        sug = route_suggestions(events, rules, args.small_tokens)
        if args.json:
            print(json.dumps(sug, indent=2))
        else:
            print(render_route(sug, args.small_tokens))
    elif args.cmd == "simulate":
        print(simulate(events, rules, args.frm, args.to))


if __name__ == "__main__":
    main()
