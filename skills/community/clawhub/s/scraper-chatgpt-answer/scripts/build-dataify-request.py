#!/usr/bin/env python3
import os
import sys

TASK_RUNTIME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "dataify-task-operations", "scripts"))
if TASK_RUNTIME_DIR not in sys.path:
    sys.path.insert(0, TASK_RUNTIME_DIR)

from catalog_builder import build_curl, run_catalog_builder




def _configure_utf8_output():
    import sys
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass

if __name__ == "__main__":
    _configure_utf8_output()
    raise SystemExit(run_catalog_builder(os.path.dirname(__file__)))