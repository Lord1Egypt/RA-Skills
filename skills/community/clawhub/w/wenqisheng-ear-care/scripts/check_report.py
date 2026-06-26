#!/usr/bin/env python3
"""Read latest test report"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
report_path = os.path.join(SKILL_DIR, 'dist', 'test-report.json')

if os.path.exists(report_path):
    with open(report_path, encoding='utf-8') as f:
        d = json.load(f)
    print(f"Tests: {d['passed']}/{d['total']} passed ({d['pass_rate']})")
    print(f"Failed: {d['failed']}")
else:
    print("No test report found. Run test_skill.py first.")
