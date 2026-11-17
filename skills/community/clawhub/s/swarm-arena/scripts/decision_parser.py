#!/usr/bin/env python3
"""decision_parser.py — parse + validate raw LLM output into a safe decision.

Arena LLMs answer with prose, markdown fences, or plain JSON. This module
extracts the first complete JSON object, validates it against the decision
schema, clamps leverage to config caps, and degrades to "hold" on garbage
(never raises on model output — a bad answer is a hold, not a crash).

Decision schema:
  {"action": "open_long"|"open_short"|"close"|"hold",
   "symbol": "ETH", "confidence": 0.0-1.0,
   "size_usd": float, "leverage": int,
   "stop_loss": float|null, "take_profit": float|null,
   "exit_plan": str, "reasoning": str}

Module:  from decision_parser import parse_decision
CLI:     cat llm_output.txt | python3 decision_parser.py
"""

import argparse
import json
import re
import sys

ACTIONS = ("open_long", "open_short", "close", "hold")

# Match ```json ... ``` / ``` ... ``` fenced blocks first, then any {...}.
_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_BRACE_RE = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", re.DOTALL)


def extract_json(text):
    """First parseable JSON object in the text, or None."""
    if not text:
        return None
    candidates = [m.group(1) for m in _FENCE_RE.finditer(text)]
    candidates.extend(m.group(0) for m in _BRACE_RE.finditer(text))
    stripped = text.strip()
    if stripped.startswith("{"):
        candidates.insert(0, stripped)
    for raw in candidates:
        try:
            obj = json.loads(raw)
        except (ValueError, TypeError):
            continue
        if isinstance(obj, dict):
            return obj
    return None


def _num(value, default=None):
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if out == out else default  # NaN guard


def _str(value, default=""):
    return value.strip() if isinstance(value, str) else default


def parse_decision(text, config=None, allowed_symbols=None):
    """Raw LLM text -> decision dict. Never raises; garbage becomes hold."""
    config = config or {}
    symbols = [s.upper() for s in (allowed_symbols or config.get("allowed_symbols") or [])]

    hold = {"action": "hold", "symbol": None, "confidence": 0.0,
            "size_usd": 0.0, "leverage": 0, "stop_loss": None,
            "take_profit": None, "exit_plan": "", "reasoning": "",
            "parse_error": None}

    obj = extract_json(text)
    if obj is None:
        hold["parse_error"] = "no JSON object found"
        hold["reasoning"] = _str(text)[:500]
        return hold

    action = _str(obj.get("action")).lower().replace(" ", "_")
    aliases = {"long": "open_long", "short": "open_short", "buy": "open_long",
               "sell": "open_short", "exit": "close", "flat": "close",
               "wait": "hold", "none": "hold", "no_trade": "hold"}
    action = aliases.get(action, action)
    if action not in ACTIONS:
        hold["parse_error"] = "unknown action %r" % obj.get("action")
        hold["reasoning"] = _str(obj.get("reasoning"))[:500]
        return hold

    symbol = _str(obj.get("symbol")).upper()
    if action in ("open_long", "open_short") and symbols and symbol not in symbols:
        hold["parse_error"] = "symbol %r not allowed" % symbol
        hold["reasoning"] = _str(obj.get("reasoning"))[:500]
        return hold

    confidence = _num(obj.get("confidence"), 0.0)
    confidence = min(1.0, max(0.0, confidence))

    max_lev = int(config.get("max_leverage", 25) or 25)
    min_lev = max(1, int(config.get("min_leverage", 1) or 1))
    leverage = int(_num(obj.get("leverage"), min_lev) or min_lev)
    leverage = max(min_lev, min(max_lev, leverage))

    size_usd = _num(obj.get("size_usd"), 0.0) or 0.0
    if size_usd < 0:
        size_usd = 0.0

    sl = _num(obj.get("stop_loss"))
    tp = _num(obj.get("take_profit"))
    if sl is not None and sl <= 0:
        sl = None
    if tp is not None and tp <= 0:
        tp = None

    return {
        "action": action,
        "symbol": symbol or None,
        "confidence": round(confidence, 4),
        "size_usd": round(size_usd, 2),
        "leverage": leverage,
        "stop_loss": sl,
        "take_profit": tp,
        "exit_plan": _str(obj.get("exit_plan"))[:1000],
        "reasoning": _str(obj.get("reasoning"))[:2000],
        "parse_error": None,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Parse raw LLM output into a decision")
    parser.add_argument("input", nargs="?", help="file with LLM output (default: stdin)")
    args = parser.parse_args(argv)
    text = open(args.input).read() if args.input else sys.stdin.read()
    print(json.dumps(parse_decision(text), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
