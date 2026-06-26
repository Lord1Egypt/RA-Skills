#!/usr/bin/env python3
from __future__ import annotations

import argparse

from zotero_vectorize_lib import (
    file_size_bytes,
    fulltext_vectors_path,
    human_size,
    load_json,
    metadata_vectors_path,
    print_json,
    readme_path,
    resolve_paths,
    store_metadata_path,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify vector store counts, sizes, and metadata.")
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

    metadata_vectors = load_json(metadata_vectors_path(paths.output_dir), [])
    fulltext_vectors = load_json(fulltext_vectors_path(paths.output_dir), [])
    store_meta = load_json(store_metadata_path(paths.output_dir), {})

    print_json(
        {
            "output_dir": str(paths.output_dir),
            "exists": {
                "metadata_vectors": metadata_vectors_path(paths.output_dir).exists(),
                "fulltext_vectors": fulltext_vectors_path(paths.output_dir).exists(),
                "store_metadata": store_metadata_path(paths.output_dir).exists(),
                "readme": readme_path(paths.output_dir).exists(),
            },
            "counts": {
                "metadata_items": len(metadata_vectors),
                "fulltext_items": len(fulltext_vectors),
                "fulltext_chunks": sum(len(item.get("chunks", [])) for item in fulltext_vectors),
            },
            "sizes": {
                "metadata_vectors_bytes": file_size_bytes(metadata_vectors_path(paths.output_dir)),
                "metadata_vectors_human": human_size(file_size_bytes(metadata_vectors_path(paths.output_dir))),
                "fulltext_vectors_bytes": file_size_bytes(fulltext_vectors_path(paths.output_dir)),
                "fulltext_vectors_human": human_size(file_size_bytes(fulltext_vectors_path(paths.output_dir))),
            },
            "store_metadata": store_meta,
        }
    )


if __name__ == "__main__":
    main()
