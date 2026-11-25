#!/usr/bin/env python3
"""Legacy entrypoint; this unified source uses the Vmake configuration by default."""

from vmake_ai import main

if __name__ == "__main__":
    raise SystemExit(main())
