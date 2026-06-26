#!/usr/bin/env python3
"""
Researcher's Narrative Generator

Reads execution metadata from execution_meta.json and applies narrative templates
to generate a first-person reflection. Zero LLM calls, purely rule-based templates.
"""

import json
import random
import sys
import argparse

TEMPLATES = {
    "opening": [
        "This research session took approximately {duration} seconds, with {fetch_attempts} information fetch attempts.",
        "I completed this research in {duration} seconds, conducting {fetch_attempts} network probes.",
    ],
    "static_fetch": [
        "I first searched for relevant whitepapers and patents using lightweight scraping tools, returning {static_success} valid results.",
        "During static scraping, I identified {static_success} usable sources.",
    ],
    "playwright_trigger": [
        "Upon detecting {pw_count} patent/documentation links, I switched to dynamic browser scraping, as core content on such pages often hides behind interactive tabs.",
        "Finding {pw_count} pages requiring dynamic rendering, I launched Playwright to patiently wait for content to load.",
    ],
    "gaps": [
        "During breakdown, I encountered {gap_count} public information blanks and honestly marked them as 'Info Missing' rather than fabricating details.",
        "This session had {gap_count} technical details unverifiable from public channels; I explicitly left blanks in the report.",
    ],
    "weak_chapter": [
        "The software section was my least confident chapter; public information was extremely sparse, and most descriptions are derived from similar solutions. Please treat with caution.",
        "Regarding software architecture, due to lack of primary sources, credibility is relatively low. I recommend cross-verification.",
    ],
    "closing": [
        "If you can provide official manuals or field data, I can re-run the research to fill those gaps.",
        "That concludes my research notes. For more precise information, please provide additional sources for deeper investigation.",
    ]
}

def generate_narrative(meta: dict) -> str:
    exec_summary = meta.get('execution_summary', {})
    data_acq = meta.get('data_acquisition', {})
    info_bound = meta.get('info_boundaries', {})
    
    duration = int(exec_summary.get('total_duration_sec', 0))
    fetch_attempts = data_acq.get('static_fetch_attempts', 0)
    static_success = data_acq.get('static_fetch_success', 0)
    pw_triggers = data_acq.get('playwright_triggers', [])
    pw_count = len(pw_triggers)
    gap_count = info_bound.get('gaps_count', 0)
    
    has_weak = False
    for step_meta in meta.get('step_details', []):
        if step_meta.get('step') == 3 and step_meta.get('fact_ratio', 0) < 0.4:
            has_weak = True
            break
    
    lines = []
    lines.append(random.choice(TEMPLATES['opening']).format(duration=duration, fetch_attempts=fetch_attempts))
    
    if static_success > 0:
        lines.append(random.choice(TEMPLATES['static_fetch']).format(static_success=static_success))
    
    if pw_count > 0:
        lines.append(random.choice(TEMPLATES['playwright_trigger']).format(pw_count=pw_count))
    
    if gap_count > 0:
        lines.append(random.choice(TEMPLATES['gaps']).format(gap_count=gap_count))
    
    if has_weak:
        lines.append(random.choice(TEMPLATES['weak_chapter']))
    
    lines.append(random.choice(TEMPLATES['closing']))
    
    return ' '.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Generate researcher narrative')
    parser.add_argument('--meta', '-m', required=True, help='Path to execution_meta.json')
    parser.add_argument('--output', '-o', help='Output file path (default stdout)')
    args = parser.parse_args()
    
    try:
        with open(args.meta, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception as e:
        print(f"Failed to read metadata: {e}", file=sys.stderr)
        sys.exit(1)
    
    narrative = generate_narrative(meta)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(narrative)
    else:
        print(narrative)

if __name__ == '__main__':
    main()
