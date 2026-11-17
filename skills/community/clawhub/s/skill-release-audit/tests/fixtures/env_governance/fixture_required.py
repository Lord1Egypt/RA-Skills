#!/usr/bin/env python3
"""Frozen regression sample: required undeclared — expect ENV_REQUIRED_UNDECLARED."""
import os
import sys

TOKEN = os.environ["API_TOKEN"]
BASE = os.getenv("DB_URL")
if not BASE:
    raise RuntimeError("DB_URL is required")
