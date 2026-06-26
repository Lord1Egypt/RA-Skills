#!/usr/bin/env python3
from _bootstrap import bootstrap_src

bootstrap_src()


def main() -> int:
    from resource_hunter.packaging_verify import main as packaging_verify_main

    return packaging_verify_main()


if __name__ == "__main__":
    raise SystemExit(main())
