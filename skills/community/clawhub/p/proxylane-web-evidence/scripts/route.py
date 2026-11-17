#!/usr/bin/env python3
"""Validate proposed phrase routing without claiming an LLM resolver evaluation."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    return re.sub(r"\s+", " ", str(text).casefold()).strip().strip(".!?")


def resolve(text):
    proposal = json.loads((ROOT / "references/routing-proposal.json").read_text())
    query = normalize(text)
    match = next((trigger for trigger in proposal["resolver_triggers"] if query == normalize(trigger)), None)
    return {"route": proposal["name"] if match else "other", "matched_trigger": match, "method": "exact documented phrase, case/spacing/punctuation normalized", "llm_evaluation": False, "global_resolver_registration_verified": False}


if __name__ == "__main__":
    print(json.dumps(resolve(" ".join(sys.argv[1:])), ensure_ascii=False, indent=2))
