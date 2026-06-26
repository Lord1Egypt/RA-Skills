#!/usr/bin/env python3
"""
agent-sentinel / eval_engine.py  —  OpenClaw Evaluate-before-Execute (EBE) Guardrail
======================================================================================

Intercepts proposed agent actions and issues a GO / NO-GO decision via a
two-tier evaluation pipeline.  All internal reasoning is emitted to stderr as
[cot] Chain-of-Thought steps.  Only a single JSON object reaches stdout.

  Tier 1 — Global Safety
      Heuristic regex + optional LLM-as-judge.  Blocks adult content, graphic
      violence, and any material inappropriate for a child under 10 years old.

  Tier 2 — User Preferences (Travel)
      Policy Parser reads SENTINEL_CONFIG.md.  Enforces budget caps, night-
      flight bans, blocked airlines, stop limits, and cabin-class preferences.

Output schema (stdout, always valid JSON):
    {
      "decision":     "ALLOW" | "BLOCK" | "ADVISE",
      "severity":     "LOW"   | "MEDIUM" | "HIGH",
      "reason":       "<clear explanation of the evaluation outcome>",
      "alternatives": "<optional suggestion to resolve a violation>"
    }

Usage:
    python3 eval_engine.py \\
        --intent  "Book a family trip to Orlando" \\
        --action  booking_tool \\
        --data    "Spirit Airlines dep 23:15 arr 01:30, $620 total, 2 stops" \\
        [--provider  anthropic | openai | ollama] \\
        [--model     <model-id>] \\
        [--config_path /path/to/SENTINEL_CONFIG.md]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Optional SDK imports — fail gracefully; rule-based tiers still work without
# ─────────────────────────────────────────────────────────────────────────────
try:
    import anthropic as _anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai as _openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# ─────────────────────────────────────────────────────────────────────────────
# Chain-of-Thought logger  (stderr only — stdout is reserved for JSON output)
# ─────────────────────────────────────────────────────────────────────────────

def _cot(step: str, finding: str) -> None:
    """Emit one CoT reasoning step to stderr."""
    print(f"[cot] {step:30s} {finding}", file=sys.stderr)


def _log(msg: str) -> None:
    print(f"[sentinel] {msg}", file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# Tier 1 — Global Safety  (child-safety heuristics + LLM judge)
# ─────────────────────────────────────────────────────────────────────────────

# Hard-blocked patterns — any match is an immediate BLOCK (HIGH severity).
# These are deliberately broad so they cannot be trivially circumvented.
_CHILD_SAFETY_PATTERNS: list[tuple[str, str]] = [
    # Adult / sexual content
    (r"\b(porn(?:ograph(?:y|ic))?|xxx|erotic(?:\s+content)?|adult\s+content)\b",
     "adult/pornographic content"),
    (r"\b(nude[s]?|nudity|naked(?:\s+(?:video|image|photo))?|explicit\s+content)\b",
     "nudity or explicit content"),
    (r"\b(sex(?:ual)?\s+(?:content|video|scene|site|image))\b",
     "sexual content"),
    (r"\bnsfw\b",
     "NSFW-flagged content"),

    # Graphic violence
    (r"\b(gore|snuff|beheading|torture\s+(?:video|clip|scene)|execution\s+video)\b",
     "graphic violence or gore"),
    (r"\b(graphic\s+(?:violence|murder|death|injury))\b",
     "graphic violence"),

    # Age-inappropriate games / media
    (r"\b(grand\s+theft\s+auto|GTA\s*[0-9]|mortal\s+kombat)\b",
     "mature-rated video game (M/18+)"),
    (r"\b(horror\s+(?:movie|film|game|clip)|jump\s+scare)\b",
     "horror content inappropriate for young children"),

    # Gambling / substance promotion
    (r"\b(casino|gambling|sports\s+betting|poker\s+site|slot\s+machine)\b",
     "gambling content"),
    (r"\b(how\s+to\s+(?:make|buy|obtain)\s+(?:drugs?|alcohol|cigarettes?))\b",
     "substance acquisition instructions"),

    # Child exploitation — zero tolerance
    (r"\bchild\s+(?:sexual|nude|porn|exploit|abuse)\b",
     "child sexual exploitation material (CSEM)"),
    (r"\b(CSAM|CSEM)\b",
     "child sexual abuse material"),
]


def _tier1_heuristic(intent: str, data: str) -> tuple[bool, str]:
    """
    Regex scan of intent + data against child-safety blocklist.
    Returns (is_violation, reason).
    """
    combined = f"{intent} {data}"
    for pattern, label in _CHILD_SAFETY_PATTERNS:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            return True, f"Detected {label} (matched: '{m.group(0).strip()}')"
    return False, ""


_TIER1_LLM_SYSTEM = """\
You are a mandatory child-safety evaluator embedded in an AI agent.
The household has a child aged 9 (under 10 years old).

An AI agent is about to take an action. Evaluate strictly whether it is safe
and age-appropriate for this household.

Reason step by step:
1. What is the nature of the action and its payload?
2. Could it expose the child to adult content, graphic violence, horror,
   gambling, substance use, or any age-inappropriate material?
3. Is the web destination, search query, or booking content family-safe?
4. Weigh false-negative risk heavily — when in doubt, flag as UNSAFE.

Conclude your reasoning with EXACTLY one of these verdict lines:
  VERDICT: SAFE
  VERDICT: UNSAFE - <one-sentence reason>
"""


def _tier1_llm(
    intent: str,
    action: str,
    data: str,
    provider: str,
    model: str,
) -> tuple[Optional[bool], str]:
    """
    LLM-as-judge for Tier 1.  Returns (is_unsafe, reason) or (None, '').
    None means the LLM was unavailable — caller should fall back to heuristic.
    """
    user_prompt = (
        f"Action type : {action}\n"
        f"User intent : {intent}\n"
        f"Payload/data: {data}\n\n"
        "Evaluate for child safety (child is under 10 years old):"
    )
    raw = _llm_call(_TIER1_LLM_SYSTEM, user_prompt, provider, model, max_tokens=300)
    if raw is None:
        return None, ""

    _cot("TIER-1 LLM RAW", raw[:120].replace("\n", " "))

    m = re.search(r"VERDICT:\s*(SAFE|UNSAFE(?:\s*-\s*.+)?)", raw, re.IGNORECASE)
    if not m:
        _cot("TIER-1 LLM PARSE", "Could not extract verdict; skipping LLM result")
        return None, ""

    verdict = m.group(1).strip().upper()
    if verdict.startswith("SAFE"):
        return False, ""

    # Extract reason from "UNSAFE - <reason>"
    reason_m = re.search(r"UNSAFE\s*-\s*(.+)", verdict, re.IGNORECASE)
    reason = reason_m.group(1).strip() if reason_m else "Content deemed unsafe for child under 10"
    return True, reason


# ─────────────────────────────────────────────────────────────────────────────
# Tier 2 — User Preferences  (travel policy parser)
# ─────────────────────────────────────────────────────────────────────────────

_CONFIG_NAME = "SENTINEL_CONFIG.md"
_CONFIG_SEARCH = [
    Path(__file__).parent / _CONFIG_NAME,
    Path.cwd() / _CONFIG_NAME,
    Path.home() / ".openclaw" / _CONFIG_NAME,
]


def _find_config(override: Optional[str]) -> Optional[Path]:
    if override:
        p = Path(override)
        return p if p.is_file() else None
    for p in _CONFIG_SEARCH:
        if p.is_file():
            return p
    return None


def _parse_config(text: str) -> dict:
    """
    Extract travel policy rules from SENTINEL_CONFIG.md.

    Reads key=value / key: value pairs case-insensitively. Restricted to the
    ## User_Preferences section so Global_Safety prose does not confuse the
    parser.
    """
    rules: dict = {}

    # Isolate the User_Preferences section (everything after its H2 header)
    pref_m = re.search(
        r"##\s+User_Preferences\b(.+?)(?=\n##\s|\Z)", text, re.IGNORECASE | re.DOTALL
    )
    section = pref_m.group(1) if pref_m else text  # fall back to full text

    def _val(pattern: str) -> Optional[str]:
        m = re.search(pattern, section, re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else None

    raw_budget = _val(r"Max_Budget\s*[:=]\s*\$?([\d,]+(?:\.\d{1,2})?)")
    if raw_budget:
        rules["max_budget"] = float(raw_budget.replace(",", ""))

    night_flag = _val(r"Night_Flights_Blocked\s*[:=]\s*(true|yes|1)")
    if night_flag:
        rules["night_flights_blocked"] = True
        window = _val(r"Night_Flight_Window\s*[:=]\s*(\d{1,2}:\d{2}\s*[-–]\s*\d{1,2}:\d{2})")
        if window:
            parts = re.split(r"\s*[-–]\s*", window)
            rules["night_start"] = parts[0].strip()
            rules["night_end"]   = parts[1].strip()
        else:
            rules["night_start"] = "22:00"
            rules["night_end"]   = "06:00"

    preferred_raw = _val(r"Preferred_Airlines\s*[:=]\s*(.+)")
    if preferred_raw:
        rules["preferred_airlines"] = [
            a.strip().lower() for a in re.split(r"[,;|]", preferred_raw) if a.strip()
        ]

    blocked_raw = _val(r"Blocked_Airlines\s*[:=]\s*(.+)")
    if blocked_raw and blocked_raw.lower() not in ("none", "n/a", "-", ""):
        rules["blocked_airlines"] = [
            a.strip().lower() for a in re.split(r"[,;|]", blocked_raw) if a.strip()
        ]

    stops_raw = _val(r"Max_Stops\s*[:=]\s*(\d+)")
    if stops_raw:
        rules["max_stops"] = int(stops_raw)

    cabin_raw = _val(r"Preferred_Cabin\s*[:=]\s*(economy|premium\s+economy|business|first)")
    if cabin_raw:
        rules["preferred_cabin"] = cabin_raw.lower()

    advance_raw = _val(r"Max_Booking_Advance_Days\s*[:=]\s*(\d+)")
    if advance_raw:
        rules["max_booking_advance_days"] = int(advance_raw)

    return rules


# ── Time helpers ──────────────────────────────────────────────────────────────

def _parse_minutes(t: str) -> Optional[int]:
    """Convert 'HH:MM', 'HH:MM AM/PM', or 'HHMM' to minutes since midnight."""
    t = t.strip()
    # HH:MM 24h
    m = re.match(r"^(\d{1,2}):(\d{2})$", t)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    # HHMM
    m = re.match(r"^(\d{2})(\d{2})$", t)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    # HH:MM AM/PM
    m = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", t, re.IGNORECASE)
    if m:
        h, mins, period = int(m.group(1)), int(m.group(2)), m.group(3).upper()
        if period == "PM" and h != 12:
            h += 12
        elif period == "AM" and h == 12:
            h = 0
        return h * 60 + mins
    return None


def _is_night(minutes: int, start_str: str, end_str: str) -> bool:
    """Return True if 'minutes' falls inside the night window (wraps midnight)."""
    s = _parse_minutes(start_str) or 22 * 60
    e = _parse_minutes(end_str)   or  6 * 60
    if s > e:           # window crosses midnight (e.g. 22:00 – 06:00)
        return minutes >= s or minutes <= e
    return s <= minutes <= e


def _extract_flight_times(data: str) -> list[tuple[str, int]]:
    """
    Pull departure / arrival times from free-text flight data.
    Returns list of (label, minutes) tuples.
    """
    results: list[tuple[str, int]] = []

    # Patterns: "dep 23:15", "departure at 11:15 PM", "departs 2315"
    time_pat = (
        r"(?P<label>dep(?:arture|arts?)?|arr(?:ival|ives?)?)"
        r"\s*(?:at\s+)?(?P<time>\d{1,2}:\d{2}(?:\s*[AP]M)?|\d{4})"
    )
    for m in re.finditer(time_pat, data, re.IGNORECASE):
        mins = _parse_minutes(m.group("time"))
        if mins is not None:
            label = "departure" if m.group("label").lower().startswith("dep") else "arrival"
            results.append((label, mins))

    # Standalone times that follow flight codes or slashes: "AA123 23:15/01:30"
    standalone = re.findall(r"\b(\d{1,2}:\d{2}(?:\s*[AP]M)?)\b", data)
    if not results and len(standalone) >= 1:
        results.append(("departure", _parse_minutes(standalone[0]) or 0))
    if not results and len(standalone) >= 2:
        results.append(("arrival", _parse_minutes(standalone[1]) or 0))

    return results


def _extract_prices(data: str) -> set[float]:
    """Pull distinct numeric prices from data (deduplicates multiple patterns)."""
    patterns = [
        r"\$\s*([\d,]+(?:\.\d{1,2})?)",
        r"USD\s*([\d,]+(?:\.\d{1,2})?)",
        r"([\d,]+(?:\.\d{1,2})?)\s*USD",
        r"(?:costs?|price[sd]?|fare[sd]?|total[s]?)\s+(?:of\s+)?\$?([\d,]+(?:\.\d{1,2})?)",
    ]
    prices: set[float] = set()
    for pat in patterns:
        for m in re.finditer(pat, data, re.IGNORECASE):
            try:
                prices.add(float(m.group(1).replace(",", "")))
            except ValueError:
                pass
    return prices


# Violation record — carries enough info to build the final JSON response
_Violation = dict  # keys: decision, severity, reason, alternatives


def _tier2_travel(data: str, rules: dict) -> list[_Violation]:
    """
    Run all travel-policy checks.  Returns a list of violations ordered by
    severity (HIGH first).  An empty list means no issues found.
    """
    violations: list[_Violation] = []

    # ── Budget ───────────────────────────────────────────────────────────────
    if "max_budget" in rules:
        cap = rules["max_budget"]
        for price in sorted(_extract_prices(data)):
            if price > cap:
                violations.append({
                    "decision": "BLOCK",
                    "severity": "MEDIUM",
                    "reason": (
                        f"Price ${price:,.2f} exceeds your maximum budget of ${cap:,.2f}."
                    ),
                    "alternatives": (
                        f"Look for options priced at or below ${cap:,.2f}. "
                        "Consider flexible dates or alternate airports."
                    ),
                })
            elif price > cap * 0.85:
                violations.append({
                    "decision": "ADVISE",
                    "severity": "LOW",
                    "reason": (
                        f"Price ${price:,.2f} is within 15% of your ${cap:,.2f} budget cap."
                    ),
                    "alternatives": (
                        "Confirm this cost is acceptable or search for cheaper alternatives."
                    ),
                })

    # ── Night flights ─────────────────────────────────────────────────────────
    if rules.get("night_flights_blocked"):
        ns, ne = rules.get("night_start", "22:00"), rules.get("night_end", "06:00")
        for label, mins in _extract_flight_times(data):
            if _is_night(mins, ns, ne):
                h, m = divmod(mins, 60)
                violations.append({
                    "decision": "BLOCK",
                    "severity": "MEDIUM",
                    "reason": (
                        f"{label.capitalize()} time {h:02d}:{m:02d} falls within your "
                        f"blocked night-flight window ({ns} – {ne})."
                    ),
                    "alternatives": (
                        f"Search for flights departing after {ne} and arriving before {ns}."
                    ),
                })

    # ── Blocked airlines ─────────────────────────────────────────────────────
    for airline in rules.get("blocked_airlines", []):
        if airline and re.search(re.escape(airline), data, re.IGNORECASE):
            violations.append({
                "decision": "BLOCK",
                "severity": "MEDIUM",
                "reason": f"'{airline.title()}' is on your blocked-airlines list.",
                "alternatives": (
                    f"Choose a preferred carrier instead: "
                    f"{', '.join(rules.get('preferred_airlines', ['any other airline']))}."
                ),
            })

    # ── Preferred airlines (advisory only) ───────────────────────────────────
    preferred = rules.get("preferred_airlines", [])
    if preferred:
        any_preferred = any(
            re.search(re.escape(a), data, re.IGNORECASE) for a in preferred if a
        )
        if not any_preferred:
            violations.append({
                "decision": "ADVISE",
                "severity": "LOW",
                "reason": (
                    "None of your preferred airlines "
                    f"({', '.join(preferred)}) appear in the proposed booking."
                ),
                "alternatives": (
                    "Consider searching specifically for "
                    f"{' or '.join(preferred)} to match your preferences."
                ),
            })

    # ── Max stops ────────────────────────────────────────────────────────────
    if "max_stops" in rules:
        max_stops = rules["max_stops"]
        sm = re.search(r"(\d+)\s+stop[s]?", data, re.IGNORECASE)
        if sm:
            stops = int(sm.group(1))
            if stops > max_stops:
                violations.append({
                    "decision": "BLOCK",
                    "severity": "MEDIUM",
                    "reason": (
                        f"Flight has {stops} stop(s); your policy allows max {max_stops}."
                    ),
                    "alternatives": (
                        f"Filter your search to flights with ≤{max_stops} stop(s)."
                    ),
                })

    # ── Cabin class (advisory) ────────────────────────────────────────────────
    if "preferred_cabin" in rules:
        pref = rules["preferred_cabin"]
        cm = re.search(
            r"\b(economy|premium\s+economy|business|first)(?:\s+class)?\b",
            data,
            re.IGNORECASE,
        )
        if cm and cm.group(1).lower() != pref:
            violations.append({
                "decision": "ADVISE",
                "severity": "LOW",
                "reason": (
                    f"Cabin class '{cm.group(1)}' differs from your preferred '{pref}'."
                ),
                "alternatives": f"Filter results to '{pref}' class tickets.",
            })

    return violations


# ─────────────────────────────────────────────────────────────────────────────
# LLM helper (shared by both tiers)
# ─────────────────────────────────────────────────────────────────────────────

def _llm_call(
    system: str,
    user: str,
    provider: str,
    model: str,
    max_tokens: int = 300,
) -> Optional[str]:
    """Send a single-turn message to the chosen LLM.  Returns text or None."""
    try:
        if provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                _log("anthropic SDK not installed; skipping LLM tier")
                return None
            key = os.getenv("ANTHROPIC_API_KEY")
            if not key:
                _log("ANTHROPIC_API_KEY not set; skipping LLM tier")
                return None
            client = _anthropic.Anthropic(api_key=key)
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return resp.content[0].text.strip()

        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                _log("openai SDK not installed; skipping LLM tier")
                return None
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                _log("OPENAI_API_KEY not set; skipping LLM tier")
                return None
            client = _openai.OpenAI(api_key=key)
            resp = client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return resp.choices[0].message.content.strip()

        elif provider == "ollama":
            import urllib.request, urllib.error
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
                "options": {"temperature": 0.0},
            }).encode()
            req = urllib.request.Request(
                f"{OLLAMA_HOST}/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())["message"]["content"].strip()

    except Exception as exc:
        _log(f"LLM call error ({provider}): {exc}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Decision aggregation
# ─────────────────────────────────────────────────────────────────────────────

_SEVERITY_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
_DECISION_RANK = {"BLOCK": 3, "ADVISE": 2, "ALLOW": 1}


def _aggregate(violations: list[_Violation]) -> dict:
    """
    Collapse a list of violations into a single EBE response.

    Priority rule: the most severe BLOCK wins over any ADVISE.
    Among equal-decision items the highest-severity one is surfaced.
    """
    if not violations:
        return {
            "decision": "ALLOW",
            "severity": "LOW",
            "reason": "No policy violations detected. Action is cleared to proceed.",
            "alternatives": "",
        }

    # Sort: BLOCK > ADVISE, then HIGH > MEDIUM > LOW
    ranked = sorted(
        violations,
        key=lambda v: (
            _DECISION_RANK.get(v["decision"], 0),
            _SEVERITY_RANK.get(v["severity"], 0),
        ),
        reverse=True,
    )
    primary = ranked[0]

    # Collect additional reasons if multiple violations exist
    extra_count = len(ranked) - 1
    reason = primary["reason"]
    if extra_count > 0:
        extras = "; ".join(v["reason"] for v in ranked[1:])
        reason += f"  Additional violation(s): {extras}"

    return {
        "decision":     primary["decision"],
        "severity":     primary["severity"],
        "reason":       reason,
        "alternatives": primary.get("alternatives", ""),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "OpenClaw Sentinel — Evaluate-before-Execute guardrail. "
            "Returns a GO/NO-GO JSON decision for a proposed agent action."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--intent",
        required=True,
        help="What the user asked for (natural-language description of the goal).",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["booking_tool", "web_search", "shell_command", "payment_tool", "other"],
        help="The tool the agent intends to invoke.",
    )
    parser.add_argument(
        "--data",
        required=True,
        help=(
            "The specific payload: flight details, URL, command string, "
            "payment amount, etc."
        ),
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai", "ollama"],
        default="anthropic",
        help="LLM provider for Tier-1 judge calls (default: anthropic).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Model ID for LLM judge calls. "
            "Defaults: anthropic → claude-haiku-4-5-20251001, "
            "openai → gpt-4o-mini, ollama → qwen3:4b."
        ),
    )
    parser.add_argument(
        "--config_path",
        default=None,
        metavar="PATH",
        help=(
            "Explicit path to SENTINEL_CONFIG.md. "
            "When omitted, searched in skill dir → cwd → ~/.openclaw/."
        ),
    )
    args = parser.parse_args()

    # Provider model defaults
    if args.model is None:
        args.model = {
            "anthropic": "claude-haiku-4-5-20251001",
            "openai":    "gpt-4o-mini",
            "ollama":    "qwen3:4b",
        }.get(args.provider, "claude-haiku-4-5-20251001")

    t_start = time.perf_counter()

    # ── Chain-of-Thought: session header ─────────────────────────────────────
    _cot("SESSION START", f"action={args.action} provider={args.provider}/{args.model}")
    _cot("INTENT", args.intent[:120])
    _cot("DATA PREVIEW", args.data[:120])

    all_violations: list[_Violation] = []

    # ═════════════════════════════════════════════════════════════════════════
    # TIER 1 — Global Safety
    # ═════════════════════════════════════════════════════════════════════════
    _cot("TIER-1 START", "Running global child-safety heuristics")

    heuristic_hit, heuristic_reason = _tier1_heuristic(args.intent, args.data)
    _cot("TIER-1 HEURISTIC", f"hit={heuristic_hit}" + (f" reason={heuristic_reason}" if heuristic_hit else ""))

    if heuristic_hit:
        # Hard block — no need for LLM call
        _cot("TIER-1 DECISION", "BLOCK (HIGH) — heuristic violation, skipping LLM")
        all_violations.append({
            "decision": "BLOCK",
            "severity": "HIGH",
            "reason": f"Child-safety violation (heuristic): {heuristic_reason}",
            "alternatives": (
                "This action is blocked under the household child-safety policy. "
                "If you believe this is a false positive, please adjust your request "
                "or ask the primary adult user to override."
            ),
        })
    else:
        # No heuristic hit → run LLM judge for deeper semantic check
        _cot("TIER-1 LLM", f"Calling {args.provider}/{args.model} for semantic safety check")
        llm_unsafe, llm_reason = _tier1_llm(
            args.intent, args.action, args.data, args.provider, args.model
        )
        if llm_unsafe is True:
            _cot("TIER-1 DECISION", f"BLOCK (HIGH) — LLM judge: {llm_reason}")
            all_violations.append({
                "decision": "BLOCK",
                "severity": "HIGH",
                "reason": f"Child-safety violation (LLM judge): {llm_reason}",
                "alternatives": (
                    "This action was flagged as inappropriate for a household with a "
                    "child under 10. Please modify your request or seek adult supervision."
                ),
            })
        elif llm_unsafe is None:
            _cot("TIER-1 LLM", "LLM unavailable — relying on heuristic result (PASS)")
        else:
            _cot("TIER-1 DECISION", "PASS — no child-safety concerns detected")

    # ═════════════════════════════════════════════════════════════════════════
    # TIER 2 — User Preferences (travel policy)
    # Only run for booking and search actions; also run for 'other' + travel data
    # ═════════════════════════════════════════════════════════════════════════
    _cot("TIER-2 START", "Loading SENTINEL_CONFIG.md for preference policy")

    config_path = _find_config(args.config_path)
    if config_path is None:
        _cot("TIER-2 CONFIG", f"SENTINEL_CONFIG.md not found in search path — skipping Tier 2")
        all_violations.append({
            "decision": "ADVISE",
            "severity": "LOW",
            "reason": (
                "SENTINEL_CONFIG.md was not found. "
                "User preference rules (budget, night-flight ban, etc.) are not being enforced."
            ),
            "alternatives": (
                f"Create SENTINEL_CONFIG.md in one of: "
                f"{', '.join(str(p) for p in _CONFIG_SEARCH)}"
            ),
        })
    else:
        _cot("TIER-2 CONFIG", f"Loaded from {config_path}")
        try:
            config_text = config_path.read_text(encoding="utf-8")
        except OSError as e:
            _cot("TIER-2 CONFIG", f"Read error: {e}")
            config_text = ""

        rules = _parse_config(config_text)
        _cot("TIER-2 RULES", f"{len(rules)} rules parsed: {list(rules.keys())}")

        if args.action in ("booking_tool", "web_search", "payment_tool", "other"):
            t2_violations = _tier2_travel(args.data, rules)
            _cot("TIER-2 CHECKS", f"{len(t2_violations)} violation(s) found")
            for v in t2_violations:
                _cot("TIER-2 VIOLATION", f"{v['decision']} ({v['severity']}) — {v['reason'][:80]}")
            all_violations.extend(t2_violations)
        else:
            _cot("TIER-2 SKIPPED", f"action={args.action} does not require travel-policy check")

    # ═════════════════════════════════════════════════════════════════════════
    # Aggregate and emit final decision
    # ═════════════════════════════════════════════════════════════════════════
    result = _aggregate(all_violations)
    elapsed_ms = round((time.perf_counter() - t_start) * 1000, 1)

    _cot(
        "FINAL DECISION",
        f"{result['decision']} | severity={result['severity']} | {elapsed_ms}ms",
    )
    _cot("REASON", result["reason"][:120])

    # Only valid JSON to stdout — OpenClaw agent parses this directly
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
