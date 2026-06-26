#!/usr/bin/env python3
"""
Skill Doctor — deep_analysis.py
Optional AI-narrated layer on top of the rule-based diagnostics.

Never called unless --deep is passed and an API key is configured.
Sends only structured metrics and rule outputs — never raw tokens,
secrets, or full clawhub payloads.
"""

import json
import sys
import urllib.request
import urllib.error

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-6"


def build_prompt(structured_results: list[dict]) -> str:
    summary = []
    for r in structured_results:
        summary.append({
            "key": r["key"],
            "status": r["diagnosis"]["status"],
            "vitals": {
                "downloads": r["current"]["downloads"],
                "installs_all_time": r["current"]["installs_all_time"],
                "active_installs": r["current"]["active_installs"],
                "stars": r["current"]["stars"],
                "verdict": r["current"]["verdict"],
            },
            "findings": [f["text"] for f in r["diagnosis"]["findings"]],
        })

    return (
        "You are reviewing a portfolio check-up for someone's published ClawHub "
        "skills and plugins. Here is the structured diagnostic data (already "
        "computed by rule-based checks):\n\n"
        f"{json.dumps(summary, indent=2)}\n\n"
        "Write a short (under 150 words) prioritized narrative: which item "
        "deserves attention first and why, in plain language. Do not repeat "
        "the raw numbers verbatim — synthesize. End with one concrete "
        "recommendation for the highest-leverage next action across the "
        "whole portfolio."
    )


def run_deep_analysis(structured_results: list[dict], api_key: str | None):
    if not api_key:
        print(
            "ℹ️  --deep requested but no Anthropic API key configured in "
            "~/.skill-doctor/config.json — skipping AI analysis.\n"
            "   Rule-based diagnostics above are still complete and reliable.",
            file=sys.stderr,
        )
        return

    prompt = build_prompt(structured_results)
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"⚠️  Deep analysis request failed ({e.code}): {e.reason}", file=sys.stderr)
        return
    except urllib.error.URLError as e:
        print(f"⚠️  Deep analysis request failed: {e.reason}", file=sys.stderr)
        return

    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    narrative = "\n".join(text_blocks).strip()

    if narrative:
        print("## 🧠 AI Commentary\n")
        print(narrative)
        print()
