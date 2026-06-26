#!/usr/bin/env python3
"""Show calibration report config and journal status."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calibration_report import _config, find_journal

print("📊 Simmer Calibration Report — Status")
print("=" * 40)
for k, v in _config.items():
    print(f"  {k}: {v}")

journal = find_journal(_config, live=True)
if journal and os.path.exists(journal):
    lines = sum(1 for _ in open(journal))
    print(f"\n  Journal: {journal}")
    print(f"  Entries: {lines}")
else:
    print("\n  ⚠️  No journal found")
