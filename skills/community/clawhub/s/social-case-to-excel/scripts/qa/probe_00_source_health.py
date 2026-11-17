#!/usr/bin/env python3
"""ClaudeBaby-only gate; compatibility entry point. Defaults to offline check."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claudebaby_preflight import main
if __name__ == '__main__':
    sys.exit(main())
