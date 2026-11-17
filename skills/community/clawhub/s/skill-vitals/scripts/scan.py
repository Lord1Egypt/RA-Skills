#!/usr/bin/env python3
"""Compatibility entry point for the modular Skill Vitals Python CLI."""
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import skill_vitals.cli as _cli
import skill_vitals.compat as _compat
for _name in _compat.COMPAT_EXPORTS:
    globals()[_name] = getattr(_compat, _name)

HOME_N, CWD_N = _compat.HOME_N, _compat.CWD_N

def redact(obj, names=False, name_map=None):
    return _compat.redact(obj, names=names, name_map=name_map,
                          home_n=HOME_N, cwd_n=CWD_N)

def classify(skill_dir, host):
    return _compat.classify(skill_dir, host, home_n=HOME_N, cwd_n=CWD_N)

def scan_skill_dir(skill_dir, host, enabled_plugins, usage, plugins_known, source_meta=None):
    return _compat.scan_skill_dir(skill_dir, host, enabled_plugins, usage,
        plugins_known, source_meta, home_n=HOME_N, cwd_n=CWD_N)

def collect(roots, enabled_plugins, usage, plugins_known):
    return _compat.collect(roots, enabled_plugins, usage, plugins_known,
                           home_n=HOME_N, cwd_n=CWD_N)

def apply_codex_runtime(skills, runtime):
    return _compat.apply_codex_runtime(skills, runtime, scanner=scan_skill_dir)

if __name__ == "__main__":
    _cli.main()
