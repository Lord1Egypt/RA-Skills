#!/usr/bin/env python3
"""
Self-Improving Agent Configuration
Universal paths using environment variables
"""

import os
from pathlib import Path

# Get workspace path - use environment variable or default
WORKSPACE = os.environ.get('OPENCLAW_WORKSPACE', '/root/.openclaw/workspace')

# Paths
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')
BACKLOG_DIR = os.path.join(WORKSPACE, 'backlog')
SCRIPTS_DIR = os.path.join(WORKSPACE, 'scripts')

# Files
ERROR_LOG = os.path.join(MEMORY_DIR, 'errors.jsonl')
TRIGGER_LOG = os.path.join(WORKSPACE, '.auto_trigger_log.json')
IMPACT_LOG = os.path.join(MEMORY_DIR, 'impact_measurements.jsonl')
PROCEDURAL_FILE = os.path.join(MEMORY_DIR, 'procedural.jsonl')
CIRCUIT_FILE = os.path.join(WORKSPACE, '.circuit_breakers.json')

# Backlog
TODAY = os.path.join(BACKLOG_DIR, '2026-03-10.md')
RESEARCH_DIR = os.path.join(BACKLOG_DIR, 'research')

# Commands (relative)
SELF_IMPROVEMENT_CMD = f'python3 {SCRIPTS_DIR}/self_improvement_cycle.py'
TOPIC_SELECTOR_CMD = f'python3 {SCRIPTS_DIR}/topic_selector.py'
