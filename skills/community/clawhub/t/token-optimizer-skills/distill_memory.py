import sys
import json
import argparse
import re
import uuid

# ---------------------------------------------------------------------------
# DISTILLATION RELIABILITY NOTE (v2.1)
# ---------------------------------------------------------------------------
# This script uses multi-pass regex heuristics. It is reliable for compression
# and budgeting, but NOT for high-trust memory persistence (e.g. financial
# decisions, security constraints). For critical memory, use an LLM-based
# distillation step (e.g. pass the history through your agent with a structured
# extraction prompt) and treat this script's output as a first-pass draft.
# source_turn is now resolved from structured JSON input when available.
# ---------------------------------------------------------------------------

FACT_PATTERNS = [
    # (type, confidence, pattern, content_group)
    ("decision",    "high",   r"(?i)(decided to|we will always|agreed to|let's go with|finalize on)\s+([^.\n]+)", 2),
    ("decision",    "high",   r"(?i)(the final approach is|we are going with|confirmed:\s*)([^.\n]+)",             2),
    ("preference",  "medium", r"(?i)(prefer|don't like|avoids?|wants? to use|hate)\s+([^.\n]+)",                   0),
    ("constraint",  "high",   r"(?i)(must be|must not|requires?|cannot|do not use|only use|never use)\s+([^.\n]+)",0),
    ("next_action", "low",    r"(?i)(todo|to-do|next step|next up|we need to|action item)\s*:?\s*([^.\n]+)",       2),
]

def _extract_from_plain_text(text: str) -> list:
    """
    Regex-based multi-pass extraction from unstructured text.
    source_turn is set to 'inferred' because there's no turn boundary info.
    """
    facts = []
    for fact_type, confidence, pattern, content_group in FACT_PATTERNS:
        for m in re.finditer(pattern, text):
            content = m.group(content_group).strip() if content_group > 0 else m.group(0).strip()
            if len(content.split()) < 2:   # skip single-word noise
                continue
            facts.append({
                "id":          str(uuid.uuid4())[:8],
                "type":        fact_type,
                "content":     content,
                "confidence":  confidence,
                "source_turn": "inferred",   # no turn info in plain text
            })
    return facts

def _extract_from_messages(messages: list) -> list:
    """
    Extraction from a structured JSON array of {role, content} messages.
    Resolves source_turn to the actual 1-indexed message index.
    """
    facts = []
    for turn_index, msg in enumerate(messages):
        role    = msg.get("role", "unknown")
        content = msg.get("content", "")
        if not isinstance(content, str):
            continue
        for fact_type, confidence, pattern, content_group in FACT_PATTERNS:
            for m in re.finditer(pattern, content):
                extracted = m.group(content_group).strip() if content_group > 0 else m.group(0).strip()
                if len(extracted.split()) < 2:
                    continue
                facts.append({
                    "id":          str(uuid.uuid4())[:8],
                    "type":        fact_type,
                    "content":     extracted,
                    "confidence":  confidence,
                    "source_turn": turn_index + 1,   # real 1-indexed turn
                    "source_role": role,
                })
    return facts

def _extract_entities(text: str) -> list:
    """
    Lightweight named-entity pass: CamelCase classes and snake_case identifiers.
    Capped at 8 to prevent noise flooding.
    """
    found = set(re.findall(r'\b([A-Z][a-z]+[A-Z][A-Za-z]+|[a-z]{2,}_[a-z_]{2,})\b', text))
    return [
        {
            "id":          str(uuid.uuid4())[:8],
            "type":        "entity",
            "content":     e,
            "confidence":  "medium",
            "source_turn": "inferred",
        }
        for e in list(found)[:8]
    ]

def _dedup(facts: list) -> list:
    seen = set()
    out  = []
    for f in facts:
        key = f["content"].lower()[:80]   # normalise to first 80 chars
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out

def distill(raw_content: str, messages: list | None = None) -> dict:
    """
    Main distillation entry point.
    If structured messages are provided, source_turn is exact.
    Otherwise falls back to plain-text regex (source_turn = 'inferred').
    """
    if messages:
        facts = _extract_from_messages(messages)
        flat_text = " ".join(m.get("content", "") for m in messages if isinstance(m.get("content"), str))
    else:
        facts = _extract_from_plain_text(raw_content)
        flat_text = raw_content

    facts += _extract_entities(flat_text)
    facts  = _dedup(facts)

    return {
        "metadata": {
            "distillation_version": "2.1-openclaw",
            "source_turn_resolved": messages is not None,   # tells consumer how accurate source_turn is
            "extraction_method":    "structured-json" if messages else "plain-text-regex",
            "reliability_note":     (
                "High confidence for structured JSON input. "
                "Regex-only extraction on plain text may miss nuance — treat as compression aid, "
                "not authoritative memory without human review."
            ),
            "original_chars":       len(raw_content),
            "turns_processed":      len(messages) if messages else None,
            "facts_extracted_count": len(facts),
        },
        "facts": facts or [
            {"type": "system", "content": "No distinct facts extracted.", "confidence": "low", "source_turn": None}
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Distill conversation history into a structured OpenClaw memory schema."
    )
    parser.add_argument("--input",  required=True, help="Path to JSON chat history or plain-text transcript.")
    parser.add_argument("--output", help="Path to write distilled JSON. Defaults to stdout.")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        print(f"Error reading {args.input}: {e}")
        sys.exit(1)

    messages = None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list) and all(isinstance(m, dict) for m in parsed):
            messages = parsed   # structured JSON — enables exact source_turn
    except json.JSONDecodeError:
        pass   # plain text fallback

    result = distill(raw, messages)
    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Distilled memory saved to: {args.output}")
        print(f"   {len(raw):,} chars → {len(output):,} chars  ({len(result['facts'])} facts extracted)")
        if not result["metadata"]["source_turn_resolved"]:
            print("   ⚠️  source_turn is 'inferred' (plain-text input). Provide a JSON messages array for exact turn tracking.")
    else:
        print(output)


if __name__ == "__main__":
    main()
