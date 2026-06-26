#!/usr/bin/env python3
from _bootstrap import bootstrap_src

bootstrap_src()


def main() -> int:
    from resource_hunter.packaging_gate import main as packaging_gate_main

    return packaging_gate_main()


if __name__ == "__main__":
    raise SystemExit(main())
