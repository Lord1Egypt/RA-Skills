#!/usr/bin/env python3
from _bootstrap import bootstrap_src

bootstrap_src()

from resource_hunter.cli import legacy_pansou_main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(legacy_pansou_main())
