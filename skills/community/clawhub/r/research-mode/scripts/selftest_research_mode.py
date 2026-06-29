#!/usr/bin/env python3
"""Research Mode self-test runner.

Discovers and runs all ``test_*`` functions from modules under ``selftest/``.
Each test receives an isolated temporary research root via the ``root`` parameter.
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
import tempfile
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import cast

TestFn = Callable[[Path], None]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--filter",
        dest="filter_text",
        default=None,
        help="Run only tests whose fully qualified name contains this substring",
    )
    return parser.parse_args()


def discover_tests() -> list[TestFn]:
    package_name = "selftest"
    package = importlib.import_module(package_name)
    tests: list[TestFn] = []

    for module_info in sorted(
        pkgutil.iter_modules(package.__path__), key=lambda item: item.name
    ):
        if not module_info.name.startswith("test_"):
            continue
        module = importlib.import_module(f"{package_name}.{module_info.name}")
        for name, value in sorted(vars(module).items()):
            if not name.startswith("test_") or not callable(value):
                continue
            signature = inspect.signature(value)
            if list(signature.parameters) != ["root"]:
                continue
            tests.append(cast(TestFn, value))

    return tests


def main() -> int:
    args = parse_args()
    tests = discover_tests()
    if args.filter_text:
        tests = [
            test_fn
            for test_fn in tests
            if args.filter_text in f"{test_fn.__module__}.{test_fn.__name__}"
        ]
        if not tests:
            print(
                json.dumps(
                    {
                        "status": "fail",
                        "reason": "no_tests_matched",
                        "filter": args.filter_text,
                        "total": 0,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 1

    with tempfile.TemporaryDirectory(prefix="research-mode-selftest-") as tmp:
        suite_root = Path(tmp)
        passed = 0
        failed = 0
        errors: list[str] = []

        for test_fn in tests:
            name = f"{test_fn.__module__}.{test_fn.__name__}"
            test_root = suite_root / name.replace(".", "__")
            test_root.mkdir(parents=True, exist_ok=True)
            try:
                test_fn(test_root)
                passed += 1
            except Exception:
                failed += 1
                errors.append(f"FAIL: {name}\n{traceback.format_exc()}")

        if errors:
            for err in errors:
                print(err, file=sys.stderr)
            print(
                json.dumps(
                    {
                        "status": "fail",
                        "passed": passed,
                        "failed": failed,
                        "total": len(tests),
                        "root": str(suite_root),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 1

        print(
            json.dumps(
                {
                    "status": "ok",
                    "passed": passed,
                    "total": len(tests),
                    "root": str(suite_root),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
