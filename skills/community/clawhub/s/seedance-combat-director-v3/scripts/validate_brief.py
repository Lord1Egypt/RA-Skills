#!/usr/bin/env python3
"""Minimal human-readable brief gate for seedance-combat-director.

Usage:
  python validate_brief.py brief.json

Expected JSON keys:
  duration, aspect_ratio, combatants, relationship, scene, combat_mode,
  tempo_camera, ending

Designable fields may use values such as "ALLOW_DESIGN". This script only checks
presence; it does not judge creative quality or platform capability.
"""
import json, sys

REQUIRED = [
    "duration",
    "aspect_ratio",
    "combatants",
    "relationship",
    "scene",
    "combat_mode",
    "tempo_camera",
    "ending",
]

if len(sys.argv) != 2:
    print("Usage: python validate_brief.py brief.json")
    raise SystemExit(2)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)

missing = [k for k in REQUIRED if k not in data or data[k] in (None, "", [], {})]
if missing:
    print("INCOMPLETE: " + ", ".join(missing))
    raise SystemExit(1)
print("COMPLETE")
