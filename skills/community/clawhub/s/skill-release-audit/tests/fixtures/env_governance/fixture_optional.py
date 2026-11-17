#!/usr/bin/env python3
"""Frozen regression sample: optional override patterns — expect 0 WARN."""
import os

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", "/default/ws")
HUB_BASE = os.getenv("SKILL_RELEASE_HUB_BASE", "https://default.example.com")
TIMEOUT = os.getenv("SRP_TIMEOUT") or "30"
