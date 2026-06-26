"""
Mock OpenClaw Native Dreamer Simulator

Purpose: Simulate OpenClaw's native dream cycle in tests without needing
the actual dreamer running. Allows us to test the full pipeline (pre-feed →
dreamer → post-archiver) in isolated, deterministic tests.

This module reads a memory file (as created by pre_dream_sql_feed.py),
simulates the native dreamer's processing, and creates dream output files
in the expected format for post_dream_archiver.py to parse.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def simulate_dream_cycle(
    input_file: str,
    output_dir: str,
    date_str: str = None
) -> Dict[str, str]:
    """
    Simulate a complete native dreamer cycle.

    Args:
        input_file: Path to memory/YYYY-MM-DD.md (created by pre_dream_sql_feed)
        output_dir: Base directory for dream outputs (e.g., memory/dreaming/)
        date_str: Date string for output files (YYYY-MM-DD); defaults to today

    Returns:
        Dict with keys 'light', 'rem', 'deep' mapping to output file paths

    Process:
        1. Read input memory file
        2. Parse into categories/items
        3. Simulate light sleep (low-importance candidates)
        4. Simulate REM sleep (themes, patterns, lasting truths)
        5. Simulate deep sleep (promotions, synthesis)
        6. Write output files in native dreamer format
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Ensure output directories exist
    light_dir = Path(output_dir) / "light"
    rem_dir = Path(output_dir) / "rem"
    deep_dir = Path(output_dir) / "deep"

    light_dir.mkdir(parents=True, exist_ok=True)
    rem_dir.mkdir(parents=True, exist_ok=True)
    deep_dir.mkdir(parents=True, exist_ok=True)

    # Parse input memory file
    with open(input_file, 'r') as f:
        content = f.read()

    memories = _parse_memory_file(content)

    # Simulate each sleep phase
    light_candidates = _simulate_light_sleep(memories)
    rem_themes, lasting_truths = _simulate_rem_sleep(memories)
    deep_promotions = _simulate_deep_sleep(memories)

    # Write output files
    light_file = light_dir / f"{date_str}.md"
    rem_file = rem_dir / f"{date_str}.md"
    deep_file = deep_dir / f"{date_str}.md"

    _write_light_file(light_file, light_candidates)
    _write_rem_file(rem_file, rem_themes, lasting_truths)
    _write_deep_file(deep_file, deep_promotions)

    return {
        'light': str(light_file),
        'rem': str(rem_file),
        'deep': str(deep_file),
    }


def _parse_memory_file(content: str) -> List[Dict[str, any]]:
    """Parse memory file into structured items."""
    memories = []
    current_category = None

    for line in content.split('\n'):
        line = line.strip()

        # Skip empty lines and headers
        if not line or line.startswith('#'):
            if line.startswith('## '):
                current_category = line.replace('## ', '')
            continue

        # Parse list items (- item text)
        if line.startswith('- '):
            item_text = line[2:].strip()
            memories.append({
                'text': item_text,
                'category': current_category or 'uncategorized',
            })

    return memories


def _simulate_light_sleep(memories: List[Dict]) -> List[Dict]:
    """
    Simulate light sleep phase: identify low-importance candidates,
    observations, and patterns to remember.

    Returns list of candidates with structure:
    {
        'text': 'candidate text',
        'confidence': 0.0-1.0,
        'recall_count': N,
        'status': 'candidate',
        'evidence_path': 'memory/YYYY-MM-DD.md:line',
        'snippet': 'snippet text'
    }
    """
    candidates = []

    for i, mem in enumerate(memories):
        # Assign confidence based on category heuristics
        category = mem.get('category', '')
        if 'decision' in category.lower():
            confidence = 0.85
        elif 'fact' in category.lower():
            confidence = 0.75
        elif 'lesson' in category.lower():
            confidence = 0.8
        else:
            confidence = 0.6

        candidates.append({
            'text': mem['text'],
            'confidence': confidence,
            'recall_count': 0,
            'status': 'candidate',
            'evidence_path': f'memory/test.md:line_{i}',
            'snippet': mem['text'][:100],
        })

    return candidates


def _simulate_rem_sleep(memories: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Simulate REM sleep phase: identify themes, patterns, and lasting truths.

    Returns:
        (themes, lasting_truths) where each is a list of dicts
    """
    themes = []
    lasting_truths = []

    # Group by category to find themes
    categories = {}
    for mem in memories:
        cat = mem.get('category', 'uncategorized')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(mem['text'])

    # Create themes from categories
    for category, items in categories.items():
        if items:
            themes.append({
                'text': f"{category} — {len(items)} items",
                'frequency': len(items),
            })

            # One lasting truth per category
            lasting_truths.append({
                'content': f"Key insight from {category}: {items[0][:80]}",
            })

    return themes, lasting_truths


def _simulate_deep_sleep(memories: List[Dict]) -> List[Dict]:
    """
    Simulate deep sleep phase: identify high-value promotions for synthesis.

    Returns list of promotions with structure:
    {
        'text': 'promotion text',
        'rank': N,
        'promoted': True,
        'snippet': 'snippet text'
    }
    """
    # Take top items (by category count) as promotions
    categories = {}
    for mem in memories:
        cat = mem.get('category', 'uncategorized')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(mem['text'])

    promotions = []
    for rank, (category, items) in enumerate(sorted(categories.items(), key=lambda x: len(x[1]), reverse=True), 1):
        if items:
            promotions.append({
                'text': f"{category}: {items[0]}",
                'rank': rank,
                'promoted': True,
                'snippet': items[0][:100],
            })

    return promotions


def _write_light_file(filepath: Path, candidates: List[Dict]) -> None:
    """Write light sleep phase output file."""
    with open(filepath, 'w') as f:
        f.write("# Light Sleep — Dream Candidates\n\n")

        for cand in candidates:
            f.write(f"- {cand['text']}\n")
            f.write(f"  confidence: {cand['confidence']}\n")
            f.write(f"  recalls: {cand['recall_count']}\n")
            f.write(f"  status: {cand['status']}\n")
            f.write(f"  evidence: {cand['evidence_path']}\n")
            f.write(f"  snippet: {cand['snippet']}\n\n")


def _write_rem_file(filepath: Path, themes: List[Dict], truths: List[Dict]) -> None:
    """Write REM sleep phase output file."""
    with open(filepath, 'w') as f:
        f.write("# REM Sleep — Themes & Patterns\n\n")

        f.write("## Dream Themes\n\n")
        for theme in themes:
            f.write(f"- {theme['text']} (frequency: {theme['frequency']})\n")

        f.write("\n## Lasting Truths\n\n")
        for truth in truths:
            f.write(f"- {truth['content']}\n")


def _write_deep_file(filepath: Path, promotions: List[Dict]) -> None:
    """Write deep sleep phase output file."""
    with open(filepath, 'w') as f:
        f.write("# Deep Sleep — Synthesis & Promotions\n\n")

        for promo in promotions:
            f.write(f"- Rank {promo['rank']}: {promo['text']}\n")
            f.write(f"  promoted: {promo['promoted']}\n")
            f.write(f"  snippet: {promo['snippet']}\n\n")
