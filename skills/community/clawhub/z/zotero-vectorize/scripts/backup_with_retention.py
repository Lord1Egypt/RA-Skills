#!/usr/bin/env python3
from __future__ import annotations

import argparse

from zotero_vectorize_lib import backup_store_files, ensure_output_dir, print_json, resolve_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Back up vector store files and retain only the latest backups.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--keep", type=int, default=2, help="Number of backups to retain per file (default: 2)")
    args = parser.parse_args()

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )
    ensure_output_dir(paths.output_dir)
    backups = backup_store_files(paths.output_dir, keep=args.keep)
    print_json({"output_dir": str(paths.output_dir), "created_backups": [str(p) for p in backups], "keep": args.keep})


if __name__ == "__main__":
    main()
