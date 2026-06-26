#!/usr/bin/env python3
"""
Topic Selector - Self-Improvement
Универсальная версия - использует config.py
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

# Add skill directory to path for config import
import sys
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from config import ERROR_LOG, SELF_IMPROVE_LOG, CIRCUIT_FILE, BACKLOG_DIR

OUTPUT_FILE = '/tmp/selected_topic.json'


def analyze_error_patterns():
    """Analyze recent errors to find patterns."""
    errors = []
    
    if os.path.exists(ERROR_LOG):
        with open(ERROR_LOG) as f:
            for line in f:
                try:
                    errors.append(json.loads(line))
                except:
                    pass
    
    error_types = Counter()
    for e in errors:
        err_type = e.get('type', 'unknown')
        error_types[err_type] += 1
    
    recent_errors = errors[-50:] if errors else []
    
    return {
        'total_errors': len(errors),
        'recent_errors': len(recent_errors),
        'error_types': dict(error_types.most_common(10)),
        'recent_sample': recent_errors[-5:]
    }


def analyze_gaps():
    """Analyze what capabilities are missing."""
    gaps = []
    
    if os.path.exists(CIRCUIT_FILE):
        with open(CIRCUIT_FILE) as f:
            circuits = json.load(f)
            for name, state in circuits.items():
                if state.get('failure_count', 0) > 0:
                    gaps.append(f"Circuit breaker open: {name}")
    
    return gaps


def analyze_backlog():
    """Analyze backlog for patterns."""
    tasks = []
    
    if os.path.exists(BACKLOG_DIR):
        for f in Path(BACKLOG_DIR).glob("*.md"):
            content = f.read_text()
            open_count = content.count('- [ ]')
            tasks.append({'file': f.name, 'open': open_count})
    
    return tasks


def select_topic(error_analysis, gaps, backlog_analysis):
    """Select topic based on analysis."""
    
    if error_analysis.get('recent_errors', 0) > 0:
        error_types = error_analysis.get('error_types', {})
        
        if 'cron_timeout' in error_types:
            return {
                'topic': "Fix cron timeout issues - optimize execution",
                'reason': f"Cron timeout errors detected ({error_types.get('cron_timeout')}x)",
                'priority': 9,
                'source': 'error-driven'
            }
        
        top_errors = error_types
        if top_errors:
            top_error = list(top_errors.keys())[0]
            return {
                'topic': f"Error handling for {top_error}",
                'reason': f"High error rate: {top_errors[top_error]} occurrences",
                'priority': 8,
                'source': 'error-driven'
            }
    
    if gaps:
        return {
            'topic': gaps[0],
            'reason': 'Circuit breaker indicates systemic issue',
            'priority': 9,
            'source': 'error-driven'
        }
    
    old_backlog = [t for t in backlog_analysis if t['open'] > 10]
    if old_backlog:
        return {
            'topic': f"Analyze backlog for {old_backlog[0]['file']}",
            'reason': 'High number of open tasks',
            'priority': 5,
            'source': 'gap-driven'
        }
    
    return {
        'topic': 'Agent self-improvement patterns',
        'reason': 'No specific issues found, general improvement',
        'priority': 3,
        'source': 'scheduled'
    }


def main(analyze_only=False):
    print("=" * 60)
    print("🎯 TOPIC SELECTOR - Self-Improvement")
    print("=" * 60)
    
    error_analysis = analyze_error_patterns()
    gaps = analyze_gaps()
    backlog_analysis = analyze_backlog()
    
    print(f"\n📊 Error Analysis:")
    print(f"   Total errors: {error_analysis['total_errors']}")
    print(f"   Recent: {error_analysis['recent_errors']}")
    print(f"   Top types: {error_analysis['error_types']}")
    
    print(f"\n🔍 Gaps: {gaps if gaps else 'None'}")
    print(f"\n📋 Backlog: {backlog_analysis}")
    
    if analyze_only:
        return
    
    topic = select_topic(error_analysis, gaps, backlog_analysis)
    
    print(f"\n✅ SELECTED TOPIC:")
    print(f"   Topic: {topic['topic']}")
    print(f"   Reason: {topic['reason']}")
    print(f"   Priority: {topic['priority']}/10")
    print(f"   Source: {topic['source']}")
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(topic, f, indent=2)
    
    print(f"\n💾 Saved to: {OUTPUT_FILE}")
    
    return topic


if __name__ == "__main__":
    analyze_only = '--analyze-only' in sys.argv
    main(analyze_only)
