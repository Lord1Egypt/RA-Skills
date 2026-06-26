#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _prepend_import_path_if_present(path: Path) -> bool:
    if not path.is_dir():
        return False
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)
    return True


def _configure_import_paths() -> None:
    script_path = Path(__file__).resolve()
    checked: set[Path] = set()
    for root in (script_path.parent, *script_path.parents):
        if root in checked:
            continue
        checked.add(root)

        vendor_dir = root / "vendor"
        src_dir = root / "src"
        package_dir = src_dir / "pypi_package_changelog_generator"
        if package_dir.is_dir():
            _prepend_import_path_if_present(vendor_dir)
            _prepend_import_path_if_present(src_dir)
            return


def main() -> int:
    if sys.version_info < (3, 12):
        print("Python 3.12 or newer is required.", file=sys.stderr)
        return 2

    _configure_import_paths()

    from pypi_package_changelog_generator.cli import main as cli_main

    return cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
