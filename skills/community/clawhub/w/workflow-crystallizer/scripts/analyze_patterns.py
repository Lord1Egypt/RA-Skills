#!/usr/bin/env python3
"""
Workflow Crystallizer — Pattern Analyzer

Scans memory files (memory/YYYY-MM-DD.md), extracts structured events,
clusters them by similarity, and identifies recurring patterns.

Usage:
    python3 analyze_patterns.py [--memory-dir PATH] [--state-file PATH] [--full]
    
    --full: Re-analyze all files (ignore cache)
    
Outputs JSON array of detected clusters to stdout.
Updates state.json with event cache.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# Import sibling module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from state import (
    load_state, save_state, dates_to_analyze, add_events,
    get_all_events, log_analysis
)

DEFAULT_MEMORY_DIR = Path(__file__).resolve().parent.parent.parent.parent / "memory"

# ── Stopwords for keyword extraction ──────────────────────────────────

STOPWORDS = frozenset("""
a about above after again against all am an and any are as at be because been
before being below between both but by can could did do does doing down during
each few for from further get got had has have having he her here hers herself
him himself his how i if in into is it its itself just let like me more most
must my myself no nor not now of off on once only or other our ours ourselves
out over own s same she should so some such t than that the their theirs them
themselves then there these they this those through to too under until up us
very was we were what when where which while who whom why will with would you
your yours yourself yourselves also already using used use set done still via
one two first new made got even way back well still need needs needed run
running ran etc see also yes no true false none yes
""".split())

# Words that indicate actions/verbs in memory logs
ACTION_WORDS = frozenset("""
built build building created create creating configured set setup installed
deployed deploy fixed fix fixing debugged debug debugging researched research
wrote write writing published publish publishing tested test testing updated
update updating added add adding removed remove connected enabled disabled
scheduled launched restarted started stopped designed reviewed audited
analyzed committed pushed cloned spawned summarized documented migrated
refactored rewrote rebuilt upgraded downgraded verified confirmed established
""".split())

# Words that indicate formalized/automated patterns
FORMALIZED_MARKERS = frozenset("""
cron standing workflow automated always from_now_on pre-authorized
scheduled recurring nightly daily weekly hourly
""".split())


def parse_memory_file(filepath: Path) -> list[dict]:
    """Parse a memory file into structured events (one per H2 section)."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    sections = split_h2_sections(text)
    date_str = filepath.stem  # YYYY-MM-DD

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day_of_week = dt.strftime("%A")
    except ValueError:
        day_of_week = "Unknown"

    events = []
    for header, body in sections:
        if not body.strip():
            continue

        event = extract_event(header, body, date_str, day_of_week)
        if event:
            events.append(event)

    return events


def split_h2_sections(text: str) -> list[tuple[str, str]]:
    """Split markdown into (header, body) pairs by H2 headers."""
    sections = []
    current_header = None
    current_body = []

    for line in text.split("\n"):
        if line.startswith("## "):
            if current_header is not None:
                sections.append((current_header, "\n".join(current_body)))
            current_header = line[3:].strip()
            current_body = []
        elif current_header is not None:
            current_body.append(line)

    if current_header is not None:
        sections.append((current_header, "\n".join(current_body)))

    return sections


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from text."""
    # Lowercase, split on non-alphanumeric
    words = re.findall(r'[a-z][a-z0-9_-]+', text.lower())
    # Filter stopwords, short words, and pure numbers
    keywords = [
        w for w in words
        if w not in STOPWORDS and len(w) > 2 and not w.isdigit()
    ]
    # Count and return top keywords (deduped, preserving frequency order)
    counts = Counter(keywords)
    return [w for w, _ in counts.most_common(20)]


def extract_actions(text: str) -> list[str]:
    """Extract action verbs from text."""
    words = set(re.findall(r'[a-z]+', text.lower()))
    return sorted(words & ACTION_WORDS)


def extract_entities(text: str) -> list[str]:
    """Extract proper nouns / named entities (capitalized words, project names)."""
    entities = set()

    # CamelCase and PascalCase words (TokenPulse, ClawHub, etc.)
    for match in re.finditer(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', text):
        entities.add(match.group(1))

    # Known project/product names (checked first for reliable extraction)
    known = ["TokenPulse", "ClawHub", "OpenClaw", "Discord", "Obsidian",
             "Ollama", "Lilith", "GitHub", "Fiverr", "Claude", "Qwen",
             "Mission Control", "Open WebUI", "llama.cpp", "Tauri",
             "React", "Rust", "SQLite"]
    text_lower = text.lower()
    for name in known:
        if name.lower() in text_lower:
            entities.add(name)

    # Capitalized words after lowercase text (proper nouns mid-sentence)
    for match in re.finditer(r'(?<=[a-z.!?]\s)([A-Z][a-zA-Z0-9]+)', text):
        word = match.group(1)
        if word.lower() not in STOPWORDS and len(word) > 3:
            entities.add(word)

    # Filter out generic/noisy entities
    noise = {"The", "This", "That", "When", "What", "Where", "How", "New",
             "All", "Any", "Set", "Run", "Not", "Built", "Now", "Also",
             "Full", "Key", "Both", "Good", "Keep", "Phase", "Step",
             "Added", "First", "Next", "Last", "Same", "Test", "Need",
             "Done", "Still", "Made", "Used", "Gave", "Took", "Got"}
    entities -= noise

    return sorted(entities)[:15]  # Cap at 15


def extract_time_hint(header: str, body: str) -> str | None:
    """Try to extract a time-of-day hint from the section."""
    # Check header first: "Batch Build (2:00-2:25 AM ET)"
    time_pattern = r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))'
    m = re.search(time_pattern, header)
    if m:
        return m.group(1).strip()

    # Check for "late night", "morning", etc. in header
    for phrase, time in [("late night", "23:00"), ("morning", "09:00"),
                         ("afternoon", "14:00"), ("evening", "19:00"),
                         ("midnight", "00:00"), ("early morning", "06:00")]:
        if phrase in header.lower():
            return time

    # Check first few lines of body for timestamps
    for line in body.split("\n")[:5]:
        m = re.search(time_pattern, line)
        if m:
            return m.group(1).strip()

    return None


def detect_steps(body: str) -> bool:
    """Detect if the section describes a multi-step workflow."""
    # Numbered lists
    if re.search(r'^\s*\d+\.\s', body, re.MULTILINE):
        numbered = re.findall(r'^\s*\d+\.\s', body, re.MULTILINE)
        if len(numbered) >= 3:
            return True

    # Sequential markers
    seq_markers = ["then", "next", "after that", "finally", "first", "second",
                   "step 1", "step 2", "phase 1", "phase 2"]
    marker_count = sum(1 for m in seq_markers if m in body.lower())
    if marker_count >= 2:
        return True

    # Arrow chains
    if body.count("→") >= 2 or body.count("->") >= 2:
        return True

    return False


def detect_formalized(header: str, body: str) -> bool:
    """Detect if this pattern has already been formalized."""
    combined = (header + " " + body).lower()
    # Check for explicit formalization language
    formalized_phrases = [
        "standing workflow", "cron job", "from now on", "pre-authorized",
        "always do this", "automated", "nightly cron", "scheduled"
    ]
    return any(phrase in combined for phrase in formalized_phrases)


def extract_event(header: str, body: str, date_str: str, 
                  day_of_week: str) -> dict | None:
    """Extract a structured event from a section."""
    full_text = header + "\n" + body
    keywords = extract_keywords(full_text)
    actions = extract_actions(full_text)

    # Skip very thin sections (just a line or two with no substance)
    if len(body.strip()) < 50 and not keywords:
        return None

    return {
        "section": header,
        "keywords": keywords,
        "actions": actions,
        "entities": extract_entities(full_text),
        "has_steps": detect_steps(body),
        "time_hint": extract_time_hint(header, body),
        "day_of_week": day_of_week,
        "is_formalized": detect_formalized(header, body),
        "raw_summary": body[:500].strip(),
    }


# ── Clustering ────────────────────────────────────────────────────────

def similarity_score(event_a: dict, event_b: dict) -> float:
    """Compute similarity between two events."""
    kw_a = set(event_a.get("keywords", []))
    kw_b = set(event_b.get("keywords", []))
    act_a = set(event_a.get("actions", []))
    act_b = set(event_b.get("actions", []))
    ent_a = set(event_a.get("entities", []))
    ent_b = set(event_b.get("entities", []))

    shared_kw = len(kw_a & kw_b)
    shared_act = len(act_a & act_b)
    shared_ent = len(ent_a & ent_b)

    total = max(len(kw_a | kw_b), 1)

    # Weighted similarity
    score = (shared_kw * 2.0 + shared_act * 1.5 + shared_ent * 1.0) / (total + len(act_a | act_b) + len(ent_a | ent_b) + 1)
    return min(score, 1.0)


def cluster_events(events: list[dict], threshold: float = 0.30) -> list[list[dict]]:
    """Greedy single-linkage clustering of events by similarity."""
    if not events:
        return []

    clusters: list[list[dict]] = []
    assigned = [False] * len(events)

    for i, ev in enumerate(events):
        if assigned[i]:
            continue

        cluster = [ev]
        assigned[i] = True

        for j in range(i + 1, len(events)):
            if assigned[j]:
                continue
            # Check similarity against any member of the cluster
            for member in cluster:
                if similarity_score(member, events[j]) >= threshold:
                    cluster.append(events[j])
                    assigned[j] = True
                    break

        clusters.append(cluster)

    return clusters


def is_project_not_pattern(cluster: list[dict]) -> bool:
    """Distinguish a recurring project (same entity, different actions) from a 
    recurring pattern (same actions, possibly different entities).
    
    A "project" has high entity overlap but low action consistency.
    A "pattern" has high action overlap across instances.
    """
    if len(cluster) < 2:
        return False

    # Single-day clusters with 4+ events are almost always projects/setup days
    dates = set(ev.get("date") for ev in cluster)
    if len(dates) == 1 and len(cluster) >= 4:
        return True

    # Get entity sets and action sets for each event
    entity_sets = [set(ev.get("entities", [])) for ev in cluster]
    action_sets = [set(ev.get("actions", [])) for ev in cluster]

    # Compute entity overlap (how much they share the SAME entities)
    if len(entity_sets) >= 2:
        entity_overlap_pairs = []
        for i in range(len(entity_sets)):
            for j in range(i + 1, len(entity_sets)):
                union = entity_sets[i] | entity_sets[j]
                if union:
                    entity_overlap_pairs.append(
                        len(entity_sets[i] & entity_sets[j]) / len(union)
                    )
        avg_entity_overlap = (
            sum(entity_overlap_pairs) / len(entity_overlap_pairs)
            if entity_overlap_pairs else 0
        )
    else:
        avg_entity_overlap = 0

    # Compute action consistency (do they do the SAME things?)
    if len(action_sets) >= 2:
        action_overlap_pairs = []
        for i in range(len(action_sets)):
            for j in range(i + 1, len(action_sets)):
                union = action_sets[i] | action_sets[j]
                if union:
                    action_overlap_pairs.append(
                        len(action_sets[i] & action_sets[j]) / len(union)
                    )
        avg_action_overlap = (
            sum(action_overlap_pairs) / len(action_overlap_pairs)
            if action_overlap_pairs else 0
        )
    else:
        avg_action_overlap = 0

    # High entity overlap + low action overlap = project
    # (e.g., "TokenPulse bugs" then "TokenPulse dashboard" then "TokenPulse docs")
    if avg_entity_overlap > 0.5 and avg_action_overlap < 0.3:
        return True

    return False


def score_cluster(cluster: list[dict], total_days: int) -> dict:
    """Score a cluster for pattern confidence and classify it."""
    unique_dates = set(ev.get("date") for ev in cluster)
    count = len(cluster)
    unique_days = len(unique_dates)

    # ── Occurrence score (0-1) ──
    # 3+ occurrences starts scoring, 6+ maxes out
    occurrence_score = min((count - 1) / 5.0, 1.0) if count >= 2 else 0

    # ── Time span score (0-1) ──
    # Patterns across many days are stronger than same-day bursts
    if total_days > 0:
        span_score = min(unique_days / max(total_days * 0.5, 1), 1.0)
    else:
        span_score = 0

    # ── Time correlation score (0-1) ──
    time_hints = [ev.get("time_hint") for ev in cluster if ev.get("time_hint")]
    day_of_weeks = [ev.get("day_of_week") for ev in cluster if ev.get("day_of_week")]

    time_corr = 0
    if len(day_of_weeks) >= 2:
        dow_counts = Counter(day_of_weeks)
        most_common_dow, most_common_count = dow_counts.most_common(1)[0]
        if most_common_count >= 2 and most_common_count / len(day_of_weeks) > 0.5:
            time_corr = 0.7

    if len(time_hints) >= 2:
        # Basic: if multiple events have time hints, check if they're close
        time_corr = max(time_corr, 0.5)

    # ── Step consistency score (0-1) ──
    has_steps = [ev.get("has_steps", False) for ev in cluster]
    step_score = sum(has_steps) / len(has_steps) if has_steps else 0

    # ── Novelty score (0-1) ──
    formalized = [ev.get("is_formalized", False) for ev in cluster]
    if any(formalized):
        novelty = 0.1  # Already formalized — low novelty
    else:
        novelty = 1.0

    # ── Weighted confidence ──
    confidence = (
        occurrence_score * 0.30 +
        span_score * 0.25 +
        time_corr * 0.20 +
        step_score * 0.15 +
        novelty * 0.10
    )

    # ── Determine pattern type ──
    if time_corr >= 0.5 and count >= 2:
        pattern_type = "time_correlated"
    elif step_score >= 0.5 and count >= 2:
        pattern_type = "multi_step_workflow"
    elif any(formalized):
        pattern_type = "already_formalized"
    else:
        pattern_type = "recurring_request"

    # ── Determine suggestion type ──
    if pattern_type == "time_correlated":
        suggestion_type = "cron"
    elif pattern_type == "multi_step_workflow":
        suggestion_type = "skill"
    elif pattern_type == "already_formalized":
        suggestion_type = "none"
    else:
        if count >= 4:
            suggestion_type = "monitor"
        else:
            suggestion_type = "workflow"

    # ── Build cluster label ──
    # Use most common keywords across cluster
    all_keywords = []
    for ev in cluster:
        all_keywords.extend(ev.get("keywords", []))
    top_keywords = [w for w, _ in Counter(all_keywords).most_common(5)]

    all_entities = []
    for ev in cluster:
        all_entities.extend(ev.get("entities", []))
    entity_counts = Counter(all_entities)
    
    # Prefer more specific entities (longer names, project names) over generic ones
    # Score: frequency * (1 + 0.1 * len) to give longer names a slight edge
    generic_label_entities = {"Claude", "Code", "Build", "API", "Discord", 
                              "GitHub", "Python", "React", "Rust", "SQLite"}
    scored_entities = []
    for e, freq in entity_counts.most_common(10):
        specificity = 1.0 if e not in generic_label_entities else 0.5
        score = freq * specificity * (1 + 0.05 * len(e))
        scored_entities.append((e, score))
    scored_entities.sort(key=lambda x: x[1], reverse=True)
    top_entities = [e for e, _ in scored_entities[:3]]

    label = " + ".join(top_entities[:2]) if top_entities else " / ".join(top_keywords[:3])

    return {
        "label": label,
        "pattern_type": pattern_type,
        "suggestion_type": suggestion_type,
        "confidence": round(confidence, 3),
        "count": count,
        "unique_days": unique_days,
        "dates": sorted(unique_dates),
        "top_keywords": top_keywords,
        "top_entities": top_entities,
        "has_time_correlation": time_corr >= 0.5,
        "is_multi_step": step_score >= 0.5,
        "is_formalized": any(formalized),
        "is_project": is_project_not_pattern(cluster),
        "events": [
            {"date": ev.get("date"), "section": ev.get("section")}
            for ev in cluster
        ],
        "scores": {
            "occurrence": round(occurrence_score, 3),
            "span": round(span_score, 3),
            "time_correlation": round(time_corr, 3),
            "step_consistency": round(step_score, 3),
            "novelty": round(novelty, 3),
        }
    }


def analyze(memory_dir: str, state_path: str = None, 
            full: bool = False) -> list[dict]:
    """Main analysis pipeline. Returns scored clusters."""
    mem_path = Path(memory_dir)
    state = load_state(state_path)

    # Determine which files to analyze
    if full:
        # Re-analyze everything
        dates = sorted(f.stem for f in mem_path.glob("*.md"))
        state["event_cache"] = {}
    else:
        dates = dates_to_analyze(state, memory_dir)

    if not dates and not state.get("event_cache"):
        sys.stderr.write("No memory files to analyze.\n")
        return []

    # Parse new/modified files
    new_event_count = 0
    for date_str in dates:
        filepath = mem_path / f"{date_str}.md"
        if filepath.exists():
            events = parse_memory_file(filepath)
            add_events(state, date_str, events)
            new_event_count += len(events)
            sys.stderr.write(f"  Parsed {date_str}: {len(events)} events\n")

    # Get all events and cluster
    all_events = get_all_events(state)
    total_days = len(state.get("event_cache", {}))

    if not all_events:
        sys.stderr.write("No events extracted from memory files.\n")
        save_state(state, state_path)
        return []

    sys.stderr.write(f"  Total events: {len(all_events)} across {total_days} days\n")

    # Cluster
    clusters = cluster_events(all_events)
    sys.stderr.write(f"  Clusters found: {len(clusters)}\n")

    # Score each cluster
    scored = []
    for cluster in clusters:
        if len(cluster) < 2:
            continue  # Singleton clusters aren't patterns
        score_info = score_cluster(cluster, total_days)
        scored.append(score_info)

    # Sort by confidence descending
    scored.sort(key=lambda x: x["confidence"], reverse=True)

    # Log analysis
    log_analysis(
        state,
        files_analyzed=dates,
        events_extracted=new_event_count,
        clusters_found=len(scored),
        suggestions_generated=0  # Updated by generate_suggestions
    )

    # Update last analyzed date
    if dates:
        state["last_analyzed_date"] = max(dates)

    save_state(state, state_path)

    return scored


def main():
    parser = argparse.ArgumentParser(
        description="Analyze memory files for recurring patterns"
    )
    parser.add_argument(
        "--memory-dir", 
        default=str(DEFAULT_MEMORY_DIR),
        help="Path to memory/ directory"
    )
    parser.add_argument(
        "--state-file",
        default=None,
        help="Path to state.json"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Re-analyze all files (ignore cache)"
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=None,
        help="Minimum confidence to include in output"
    )
    args = parser.parse_args()

    clusters = analyze(args.memory_dir, args.state_file, args.full)

    if args.min_confidence is not None:
        clusters = [c for c in clusters if c["confidence"] >= args.min_confidence]

    print(json.dumps(clusters, indent=2))


if __name__ == "__main__":
    main()
