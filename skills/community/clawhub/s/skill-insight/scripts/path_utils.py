#!/usr/bin/env python3
# path_utils.py - Shared path resolution for skill-insight
# All scripts import this to get proper directory paths regardless of install location.
#
# Resolution order:
#   1. $SKILL_USAGE_TRACKER_DIR env var (if set)
#   2. <script_parent>/../  (relative to this file's location in scripts/)
#   3. ~/.openclaw/workspace/skills/skill-insight (default)

import os
from pathlib import Path

def get_skill_dir():
    """Get the skill root directory."""
    # Env var override
    if "SKILL_USAGE_TRACKER_DIR" in os.environ:
        return Path(os.environ["SKILL_USAGE_TRACKER_DIR"]).resolve()

    # Derive from this file's location: path_utils.py is in scripts/
    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent.resolve()

    # Sanity check: SKILL.md should exist in skill root
    if (skill_dir / "SKILL.md").exists():
        return skill_dir

    # Fallback to default workspace location
    default = Path.home() / ".openclaw" / "workspace" / "skills" / "skill-insight"
    if (default / "SKILL.md").exists():
        return default

    # Last resort: return derived path even without SKILL.md
    return skill_dir

def get_data_dir():
    """Get the data directory, create if missing."""
    data_dir = get_skill_dir() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

def get_sample_dir():
    """Get the sample data directory."""
    return get_skill_dir() / "sample"

# Convenience accessors
def get_usage_file():
    return get_data_dir() / "usage.json"

def get_registry_file():
    return get_data_dir() / "skill_registry.json"

def get_sample_usage_file():
    return get_sample_dir() / "usage_sample.json"

def get_sample_registry_file():
    return get_sample_dir() / "registry_sample.json"
