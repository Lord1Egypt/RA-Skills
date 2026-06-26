#!/usr/bin/env python3
from __future__ import annotations

import argparse
import platform
from pathlib import Path

from zotero_vectorize_lib import print_json, resolve_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect Zotero and output paths for zotero-vectorize.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )

    print_json(
        {
            "platform": platform.platform(),
            "data_dir": str(paths.data_dir),
            "db_path": str(paths.db_path),
            "storage_dir": str(paths.storage_dir),
            "output_dir": str(paths.output_dir),
            "exists": {
                "data_dir": paths.data_dir.exists(),
                "db_path": paths.db_path.exists(),
                "storage_dir": paths.storage_dir.exists(),
                "output_dir": paths.output_dir.exists(),
            },
            "note": "If db_path or storage_dir is missing, open Zotero → Settings/Preferences → Advanced → Show Data Directory.",
        }
    )


if __name__ == "__main__":
    main()
