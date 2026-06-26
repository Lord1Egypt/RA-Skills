#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from zotero_vectorize_lib import print_json, resolve_paths, snapshot_database


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a SQLite snapshot of the Zotero database.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument(
        "--snapshot-dir",
        default=None,
        help="Directory for snapshots (default: <output-dir>/snapshots)",
    )
    args = parser.parse_args()

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )
    snapshot_dir = Path(args.snapshot_dir).expanduser() if args.snapshot_dir else paths.output_dir / "snapshots"
    snapshot_path = snapshot_database(paths.db_path, snapshot_dir)

    print_json(
        {
            "source_db": str(paths.db_path),
            "snapshot_db": str(snapshot_path),
            "snapshot_exists": snapshot_path.exists(),
        }
    )


if __name__ == "__main__":
    main()
