#!/usr/bin/env python3
"""
gather_week.py — Read memory files for the past N days, extract structured data.

Outputs JSON with per-day breakdown and cross-day aggregation.
Handles missing days gracefully (weekends, gaps).

Usage:
    python3 gather_week.py [--memory-dir PATH] [--days N] [--config PATH] [--end-date YYYY-MM-DD]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

# Patterns that signal accomplishments (shipped, built, fixed, deployed, etc.)
ACCOMPLISHMENT_VERBS = re.compile(
    r'\b(shipped|deployed|published|built|created|fixed|resolved|completed|'
    r'committed|merged|launched|released|verified|tested|confirmed working|'
    r'live on|running on|installed|configured|set up|wired|connected|rewritten|'
    r'rewrote|pushed to|all \d+ skills)\b',
    re.IGNORECASE,
)

# Patterns that signal failures or breakage
FAILURE_PATTERNS = re.compile(
    r'\b(bug|broke|broken|error|failed|failure|crash|issue|hang|timeout|'
    r'401|403|404|500|missing|wrong|not working|doesn\'t work|didn\'t work|'
    r'junk|corrupt|empty|stuck|blocked|rate.?limit|unauthorized)\b',
    re.IGNORECASE,
)

# Patterns for action items / TODOs
ACTION_PATTERNS = re.compile(
    r'(?:^|\n)\s*[-*]\s*(?:TODO|FIXME|NEXT|⬜|Action|Remaining|Need to|'
    r'needs? (?:to be|manual|restart|setup)|should (?:be|have))',
    re.IGNORECASE,
)

# Patterns for decisions made
DECISION_PATTERNS = re.compile(
    r'\b(decided|decision|chose|chosen|confirmed|approved|pivot|finalized|'
    r'approach:|strategy:|architecture|went with|correct approach|'
    r'name (?:confirmed|finalized)|domain)\b',
    re.IGNORECASE,
)

# Known tools and services to track
TOOL_KEYWORDS = [
    'tokenpulse', 'openclaw', 'obsidian', 'discord', 'claude', 'opus',
    'sonnet', 'haiku', 'ollama', 'llama.cpp', 'lilith', 'docker',
    'github', 'clawhub', 'tauri', 'react', 'python', 'rust', 'cargo',
    'sqlite', 'launchd', 'open webui', 'fiverr', 'qwen', 'cliproxy',
    'mission control', 'next.js', 'tailwind', 'claude code', 'codex',
    'lm studio', 'huggingface',
]


def load_config(config_path):
    """Load config from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def parse_memory_file(filepath):
    """Parse a single memory/YYYY-MM-DD.md file into structured sections."""
    text = Path(filepath).read_text(encoding='utf-8')
    lines = text.split('\n')

    sections = []
    current_section = None
    current_lines = []

    for line in lines:
        # Detect headers (## or ###)
        header_match = re.match(r'^(#{1,4})\s+(.+)', line)
        if header_match:
            if current_section:
                sections.append({
                    'header': current_section,
                    'content': '\n'.join(current_lines).strip(),
                })
            current_section = header_match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Flush last section
    if current_section:
        sections.append({
            'header': current_section,
            'content': '\n'.join(current_lines).strip(),
        })

    return text, sections


def extract_bullets(text):
    """Extract bullet points from markdown text."""
    bullets = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith(('- ', '* ', '• ')):
            bullets.append(stripped[2:].strip())
        elif re.match(r'^\d+\.\s', stripped):
            bullets.append(re.sub(r'^\d+\.\s*', '', stripped).strip())
    return bullets


def extract_accomplishments(text):
    """Find lines that describe something completed/shipped."""
    results = []
    for line in text.split('\n'):
        if ACCOMPLISHMENT_VERBS.search(line) and line.strip():
            clean = line.strip().lstrip('-*• ').strip()
            if len(clean) > 10:  # Filter noise
                results.append(clean)
    return results


def extract_failures(text):
    """Find lines describing failures, bugs, or breakage."""
    # Lines that are clearly categorization, not failures
    false_positive_patterns = re.compile(
        r'^\s*[-*]\s*(?:Personal Productivity|Developer|Hardware|Network|'
        r'Key insight|Key finding|Best business|Revenue target|'
        r'Build approach|Data export)',
        re.IGNORECASE,
    )
    results = []
    for line in text.split('\n'):
        if FAILURE_PATTERNS.search(line) and line.strip():
            if false_positive_patterns.search(line):
                continue
            clean = line.strip().lstrip('-*• ').strip()
            if len(clean) > 10:
                results.append(clean)
    return results


def extract_action_items(text):
    """Find TODOs, remaining work, and action items."""
    results = []
    for line in text.split('\n'):
        if ACTION_PATTERNS.search(line):
            clean = line.strip().lstrip('-*• ').strip()
            if len(clean) > 5:
                results.append(clean)
    return results


def extract_decisions(text):
    """Find decisions and strategic choices."""
    results = []
    for line in text.split('\n'):
        if DECISION_PATTERNS.search(line) and line.strip():
            clean = line.strip().lstrip('-*• ').strip()
            if len(clean) > 10:
                results.append(clean)
    return results


def extract_tools_mentioned(text):
    """Find which tools/services were mentioned."""
    text_lower = text.lower()
    found = []
    for tool in TOOL_KEYWORDS:
        if tool in text_lower:
            found.append(tool)
    return found


def extract_topics(sections):
    """Extract main topics from section headers."""
    topics = []
    for s in sections:
        header = s['header']
        # Skip generic headers
        if header.lower() in ('end of day', 'daily recap', 'discussions', 'notable'):
            continue
        topics.append(header)
    return topics


def estimate_section_weight(section):
    """Estimate how much attention a topic got based on content volume."""
    content = section['content']
    # Count substantive lines (not blank, not just bullets markers)
    lines = [l for l in content.split('\n') if l.strip() and len(l.strip()) > 5]
    return len(lines)


def detect_time_of_day(text):
    """Detect timestamps or time-of-day references in the text."""
    patterns = {
        'late_night': re.compile(r'\b(?:2[3-9]|[012][0-3]):\d{2}\b|late night|2:\d{2}\s*AM|3:\d{2}\s*AM|midnight', re.IGNORECASE),
        'morning': re.compile(r'\b(?:0[6-9]|1[01]):\d{2}\b|morning|AM ET', re.IGNORECASE),
        'afternoon': re.compile(r'\b(?:1[2-7]):\d{2}\b|afternoon|PM ET', re.IGNORECASE),
        'evening': re.compile(r'\b(?:1[89]|2[0-2]):\d{2}\b|evening|tonight', re.IGNORECASE),
    }
    detected = []
    for period, pat in patterns.items():
        if pat.search(text):
            detected.append(period)
    return detected


def process_day(date_str, filepath):
    """Process a single day's memory file into structured data."""
    text, sections = parse_memory_file(filepath)

    # Per-section analysis
    section_data = []
    for s in sections:
        full_text = s['header'] + '\n' + s['content']
        section_data.append({
            'header': s['header'],
            'weight': estimate_section_weight(s),
            'accomplishments': extract_accomplishments(full_text),
            'failures': extract_failures(full_text),
            'action_items': extract_action_items(s['content']),
            'decisions': extract_decisions(full_text),
            'tools': extract_tools_mentioned(full_text),
        })

    return {
        'date': date_str,
        'file_size': len(text),
        'section_count': len(sections),
        'topics': extract_topics(sections),
        'time_of_day': detect_time_of_day(text),
        'accomplishments': extract_accomplishments(text),
        'failures': extract_failures(text),
        'action_items': extract_action_items(text),
        'decisions': extract_decisions(text),
        'tools_mentioned': extract_tools_mentioned(text),
        'sections': section_data,
    }


def aggregate_week(days_data):
    """Cross-day aggregation: find themes, patterns, totals."""
    all_topics = []
    all_tools = Counter()
    all_accomplishments = []
    all_failures = []
    all_action_items = []
    all_decisions = []
    time_patterns = Counter()
    total_content = 0
    active_days = 0

    topic_day_map = {}  # topic -> list of dates

    for day in days_data:
        if day.get('missing'):
            continue
        active_days += 1
        total_content += day['file_size']

        for topic in day['topics']:
            all_topics.append(topic)
            # Normalize topic for grouping
            topic_key = normalize_topic(topic)
            if topic_key not in topic_day_map:
                topic_day_map[topic_key] = set()
            topic_day_map[topic_key].add(day['date'])

        for tool in day['tools_mentioned']:
            all_tools[tool] += 1

        for t in day.get('time_of_day', []):
            time_patterns[t] += 1

        all_accomplishments.extend(
            [{'text': a, 'date': day['date']} for a in day['accomplishments']]
        )
        all_failures.extend(
            [{'text': f, 'date': day['date']} for f in day['failures']]
        )
        all_action_items.extend(
            [{'text': a, 'date': day['date']} for a in day['action_items']]
        )
        all_decisions.extend(
            [{'text': d, 'date': day['date']} for d in day['decisions']]
        )

    # Find recurring topics (appeared on 2+ days) — convert sets to sorted lists
    recurring_topics = {
        topic: sorted(dates) for topic, dates in topic_day_map.items()
        if len(dates) >= 2
    }

    # Content distribution across days
    day_weights = {}
    for day in days_data:
        if not day.get('missing'):
            day_weights[day['date']] = day['file_size']

    return {
        'active_days': active_days,
        'total_days': len(days_data),
        'total_content_bytes': total_content,
        'day_weights': day_weights,
        'all_topics': all_topics,
        'recurring_topics': recurring_topics,
        'tool_frequency': dict(all_tools.most_common()),
        'time_patterns': dict(time_patterns),
        'accomplishment_count': len(all_accomplishments),
        'failure_count': len(all_failures),
        'action_item_count': len(all_action_items),
        'decision_count': len(all_decisions),
        'accomplishments': all_accomplishments,
        'failures': all_failures,
        'action_items': all_action_items,
        'decisions': all_decisions,
    }


def normalize_topic(topic):
    """Normalize a section header for grouping related topics."""
    t = topic.lower().strip()
    # Remove date stamps like "(2026-03-23)" or "(2026-03-23 continued)"
    t = re.sub(r'\(?\d{4}-\d{2}-\d{2}[^)]*\)?', '', t).strip()
    # Remove leading date like "2026-03-22"
    t = re.sub(r'^\d{4}-\d{2}-\d{2}\s*', '', t).strip()

    # Collapse TokenPulse variants
    if 'tokenpulse' in t or 'token pulse' in t or 'token flow' in t:
        return 'tokenpulse'
    if 'lilith' in t:
        return 'lilith'
    # Check for skills/clawhub (careful with word boundaries)
    if 'clawhub' in t or ('skill' in t and ('batch' in t or 'built' in t or 'publish' in t or 'niche' in t)):
        return 'clawhub-skills'
    if 'mission control' in t:
        return 'mission-control'
    if 'claude' in t and ('max' in t or 'swap' in t):
        return 'claude-auth'
    if 'smart routing' in t or ('model' in t and ('routing' in t or 'tier' in t or 'inventory' in t)):
        return 'model-routing'
    if 'youtube' in t or 'media vault' in t:
        return 'media-vault'
    if 'soul' in t or 'identity' in t or 'workspace file' in t:
        return 'identity-rewrite'
    if 'workflow' in t or 'crystallizer' in t:
        return 'workflow-crystallizer'
    if 'open webui' in t:
        return 'open-webui'
    if 'fiverr' in t or 'freelance' in t:
        return 'freelance'
    if 'domain' in t:
        return 'domain'
    if 'setup' in t or 'config' in t:
        return 'setup-config'
    if 'audit' in t:
        return 'audit'
    if 'daily recap' in t or 'end of day' in t:
        return 'daily-recap'
    if 'trending' in t or 'scanner' in t:
        return 'trending-scanner'
    if 'api' in t and ('tokenizer' in t or 'dashboard' in t or 'brainstorm' in t):
        return 'tokenpulse'
    if 'build progress' in t:
        return 'tokenpulse'
    if 'beta' in t:
        return 'tokenpulse'
    if 'mac mini' in t or 'hardware' in t:
        return 'infrastructure'
    if 'git' in t and 'status' in t:
        return 'tokenpulse'
    if 'market' in t or 'research' in t:
        return 'research'
    if 'strategy' in t or 'first.?principle' in t or 'quality' in t:
        return 'strategy'
    if 'ryan' in t and ('feedback' in t or 'task' in t):
        return 'user-feedback'
    if 'account' in t or 'token' in t and 'auth' in t:
        return 'accounts'
    if 'documentation' in t or 'doc' in t:
        return 'documentation'
    if 'bug' in t or 'fix' in t:
        return 'tokenpulse'
    # Keep original if no match (cleaned up)
    return t if t else topic.lower().strip()


def main():
    parser = argparse.ArgumentParser(description='Gather memory files for weekly retrospective')
    parser.add_argument('--memory-dir', type=str, help='Path to memory directory')
    parser.add_argument('--days', type=int, help='Number of days to look back (default: 7)')
    parser.add_argument('--end-date', type=str, help='End date YYYY-MM-DD (default: today)')
    parser.add_argument('--config', type=str, help='Path to config JSON file')
    args = parser.parse_args()

    # Load config
    config = {}
    if args.config and os.path.exists(args.config):
        config = load_config(args.config)
    elif os.environ.get('WEEKLY_RETRO_CONFIG') and os.path.exists(os.environ['WEEKLY_RETRO_CONFIG']):
        config = load_config(os.environ['WEEKLY_RETRO_CONFIG'])

    # Resolve parameters
    memory_dir = args.memory_dir or config.get('memory_dir', os.path.expanduser(
        '~/.openclaw/workspace/memory'
    ))
    lookback = args.days or config.get('lookback_days', 7)

    if args.end_date:
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=lookback - 1)

    # Gather days
    days_data = []
    for i in range(lookback):
        day = start_date + timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        filepath = os.path.join(memory_dir, f'{date_str}.md')

        if os.path.exists(filepath):
            # Check if file has real content (not just a blank/stub)
            content = Path(filepath).read_text(encoding='utf-8').strip()
            if len(content) < 50:
                days_data.append({
                    'date': date_str,
                    'missing': True,
                    'reason': 'stub_or_empty',
                })
            else:
                try:
                    day_data = process_day(date_str, filepath)
                    days_data.append(day_data)
                except Exception as e:
                    days_data.append({
                        'date': date_str,
                        'missing': True,
                        'reason': f'parse_error: {str(e)}',
                    })
        else:
            days_data.append({
                'date': date_str,
                'missing': True,
                'reason': 'file_not_found',
            })

    # Aggregate
    aggregation = aggregate_week(days_data)

    output = {
        'meta': {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'memory_dir': memory_dir,
            'lookback_days': lookback,
            'generated_at': datetime.now().isoformat(),
        },
        'days': days_data,
        'aggregation': aggregation,
    }

    json.dump(output, sys.stdout, indent=2, default=str)
    print()  # trailing newline


if __name__ == '__main__':
    main()
