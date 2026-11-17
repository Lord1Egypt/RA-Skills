#!/usr/bin/env python3
"""Frozen regression sample: runtime-injected — expect 0 WARN."""
import os

agent_id = os.environ.get("MULTICA_AGENT_ID", "")
task_id = os.environ.get("MULTICA_TASK_ID")
agent_name = os.getenv("MULTICA_AGENT_NAME")
