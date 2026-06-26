#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from zotero_vectorize_lib import (
    connect_db,
    get_fields_map,
    get_item_pdf_attachment,
    get_item_types_map,
    get_pdf_parent_rows,
    get_top_level_items,
    load_json,
    metadata_vectors_path,
    resolve_paths,
    snapshot_database,
    build_item_metadata,
    print_json,
    fulltext_vectors_path,
)


def summarize_item(conn, item_id: int, fields_map, item_types_map) -> dict:
    metadata, _ = build_item_metadata(
        conn,
        item_id,
        fields_map=fields_map,
        item_types_map=item_types_map,
    )
    attachment = get_item_pdf_attachment(conn, item_id)
    return {
        "itemID": item_id,
        "title": metadata.get("title", ""),
        "DOI": metadata.get("DOI", ""),
        "url": metadata.get("url", ""),
        "dateAdded": metadata.get("dateAdded", ""),
        "dateModified": metadata.get("dateModified", ""),
        "has_pdf": attachment is not None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Zotero items missing from the vector store.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--snapshot-db", default=None)
    parser.add_argument("--limit", type=int, default=20, help="Limit preview rows (default: 20)")
    args = parser.parse_args()

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )
    snapshot_db = Path(args.snapshot_db).expanduser() if args.snapshot_db else snapshot_database(paths.db_path, paths.output_dir / "snapshots")

    metadata_vectors = load_json(metadata_vectors_path(paths.output_dir), [])
    fulltext_vectors = load_json(fulltext_vectors_path(paths.output_dir), [])
    metadata_ids = {int(item["itemID"]) for item in metadata_vectors}
    fulltext_ids = {int(item["itemID"]) for item in fulltext_vectors}

    conn = connect_db(snapshot_db)
    try:
        fields_map = get_fields_map(conn)
        item_types_map = get_item_types_map(conn)
        top_items = get_top_level_items(conn)
        pdf_parent_rows = get_pdf_parent_rows(conn)

        missing_metadata_ids = [int(row["itemID"]) for row in top_items if int(row["itemID"]) not in metadata_ids]
        missing_fulltext_ids = [int(row["itemID"]) for row in pdf_parent_rows if int(row["itemID"]) not in fulltext_ids]

        print_json(
            {
                "snapshot_db": str(snapshot_db),
                "metadata_vectors_path": str(metadata_vectors_path(paths.output_dir)),
                "fulltext_vectors_path": str(fulltext_vectors_path(paths.output_dir)),
                "counts": {
                    "db_top_level_items": len(top_items),
                    "db_pdf_parent_items": len(pdf_parent_rows),
                    "metadata_vectors": len(metadata_vectors),
                    "fulltext_vectors": len(fulltext_vectors),
                    "missing_metadata": len(missing_metadata_ids),
                    "missing_fulltext": len(missing_fulltext_ids),
                },
                "missing_metadata_preview": [
                    summarize_item(conn, item_id, fields_map, item_types_map)
                    for item_id in missing_metadata_ids[: args.limit]
                ],
                "missing_fulltext_preview": [
                    summarize_item(conn, item_id, fields_map, item_types_map)
                    for item_id in missing_fulltext_ids[: args.limit]
                ],
            }
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
