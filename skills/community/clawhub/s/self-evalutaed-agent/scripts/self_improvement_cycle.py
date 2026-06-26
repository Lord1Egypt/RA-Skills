#!/usr/bin/env python3
"""
Self-Improvement V2 - Trigger-Based Cycle
ONE AGENT does: analyze logs → research → create backlog tasks
Универсальная версия - использует config.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add skill directory to path for config import
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

from config import (
    ERROR_LOG, CIRCUIT_FILE, BACKLOG_DIR, RESEARCH_DIR,
    WORKSPACE
)

# Import topic selector
sys.path.insert(0, skill_dir)
import topic_selector


def analyze_logs_for_errors():
    """Parse logs and find errors."""
    print("=" * 60)
    print("🔍 STEP 1: Analyze Logs for Errors")
    print("=" * 60)
    
    errors_found = []
    
    # Check error log
    if os.path.exists(ERROR_LOG):
        with open(ERROR_LOG) as f:
            lines = f.readlines()
            if lines:
                errors_found.append("known_errors_in_log")
                print(f"⚠️ Found: {len(lines)} errors in log")
    
    # Check circuit breakers
    if os.path.exists(CIRCUIT_FILE):
        with open(CIRCUIT_FILE) as f:
            circuits = json.load(f)
            open_circuits = [k for k, v in circuits.items() 
                           if v.get('state') == 'open']
            if open_circuits:
                errors_found.append(f"open_circuits: {open_circuits}")
                print(f"⚠️ Found: open circuits: {open_circuits}")
    
    print(f"\n✅ Analysis complete: {len(errors_found)} issues found")
    return errors_found


def run_topic_selector(errors_found):
    """Run topic selector with error context."""
    print("\n" + "=" * 60)
    print("🎯 STEP 2: Topic Selection")
    print("=" * 60)
    
    try:
        topic = topic_selector.select_topic(
            topic_selector.analyze_error_patterns(),
            topic_selector.analyze_gaps(),
            topic_selector.analyze_backlog()
        )
    except Exception as e:
        print(f"Topic selector error: {e}")
        topic = {
            'topic': 'General agent improvement',
            'reason': 'No specific issues found',
            'priority': 3,
            'source': 'log_analysis'
        }
    
    print(f"\n✅ Selected: {topic['topic']} (priority: {topic['priority']})")
    return topic


def run_research_and_create_tasks(topic):
    """Research + create backlog tasks."""
    print("\n" + "=" * 60)
    print("📚 STEP 3: Research + Create Backlog Tasks")
    print("=" * 60)
    
    # Create research file
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    research_file = os.path.join(
        RESEARCH_DIR, 
        f"self-improvement-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    )
    
    content = f"""# Self-Improvement Research

**Generated:** {datetime.now().isoformat()}
**Source:** Log analysis
**Priority:** {topic['priority']}/10

## Topic
{topic['topic']}

## Why
{topic['reason']}

## Key Improvements Needed

Based on log analysis:
1. Analyze and fix root cause
2. Add monitoring for this issue
3. Verify fix works

## Backlog Tasks

- [ ] 1. {topic['topic']}
  - type: implementation
  - priority: {topic['priority']}
  - impact: {topic['priority']}/10
  - source: log_analysis
  - status: backlog

"""
    
    with open(research_file, 'w') as f:
        f.write(content)
    
    # Add to backlog
    today = datetime.now().strftime('%Y-%m-%d')
    backlog_file = os.path.join(BACKLOG_DIR, f"{today}.md")
    
    if not os.path.exists(backlog_file):
        with open(backlog_file, 'w') as f:
            f.write(f"# Backlog {today}\n\n")
    
    with open(backlog_file) as f:
        content = f.read()
    
    task = f"""
### From Log Analysis: {topic['topic']}
- [ ] 1. {topic['topic']}
  - type: implementation
  - priority: {topic['priority']}
  - impact: {topic['priority']}/10
  - source: log_analysis
  - research: {os.path.basename(research_file)}
  - status: backlog
"""
    
    with open(backlog_file, 'w') as f:
        f.write(content + task)
    
    print(f"✅ Research: {research_file}")
    print(f"✅ Backlog: updated with priority {topic['priority']}")
    
    return research_file


def main():
    print("=" * 60)
    print("🔄 SELF-IMPROVEMENT CYCLE")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Workspace: {WORKSPACE}")
    
    # Step 1: ONE agent analyzes logs
    errors_found = analyze_logs_for_errors()
    
    # Step 2: Select topic based on logs
    topic = run_topic_selector(errors_found)
    
    # Step 3: Research + create backlog (ONE AGENT)
    research_file = run_research_and_create_tasks(topic)
    
    print("\n" + "=" * 60)
    print("✅ CYCLE COMPLETE")
    print("=" * 60)
    print(f"Topic: {topic['topic']}")
    print(f"Priority: {topic['priority']}/10")
    
    return {
        "status": "complete",
        "topic": topic['topic'],
        "priority": topic['priority'],
        "errors_found": len(errors_found)
    }


if __name__ == "__main__":
    result = main()
    print(f"\nResult: {json.dumps(result, indent=2)}")
