#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from zotero_vectorize_lib import (
    DEFAULT_METADATA_BATCH_SIZE,
    DEFAULT_MODEL,
    build_item_metadata,
    connect_db,
    default_store_metadata,
    encode_texts,
    ensure_output_dir,
    get_embedding_model,
    get_fields_map,
    get_item_types_map,
    get_top_level_items,
    metadata_vectors_path,
    print_json,
    resolve_paths,
    save_json,
    snapshot_database,
    store_metadata_path,
    update_store_metadata,
    write_store_readme,
    fulltext_vectors_path,
    load_json,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build metadata vectors for Zotero items.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_METADATA_BATCH_SIZE)
    parser.add_argument(
        "--snapshot-db",
        default=None,
        help="Use an existing database snapshot instead of creating one.",
    )
    args = parser.parse_args()

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )
    ensure_output_dir(paths.output_dir)

    snapshot_db = Path(args.snapshot_db).expanduser() if args.snapshot_db else snapshot_database(paths.db_path, paths.output_dir / "snapshots")
    conn = connect_db(snapshot_db)
    try:
        fields_map = get_fields_map(conn)
        item_types_map = get_item_types_map(conn)
        items = get_top_level_items(conn)

        payloads = []
        texts = []
        for row in items:
            metadata, embedding_text = build_item_metadata(
                conn,
                int(row["itemID"]),
                fields_map=fields_map,
                item_types_map=item_types_map,
            )
            item_type = item_types_map.get(int(row["itemTypeID"]), "unknown")
            payloads.append(
                {
                    "itemID": int(row["itemID"]),
                    "key": row["key"],
                    "metadata": metadata,
                    "embedding_text": embedding_text,
                    "itemType": item_type,
                }
            )
            texts.append(embedding_text)

        model = get_embedding_model(args.model)
        vectors = encode_texts(model, texts, batch_size=args.batch_size)

        results = []
        for payload, vector in zip(payloads, vectors):
            payload = dict(payload)
            payload["vector"] = vector
            payload["vector_dimension"] = len(vector)
            payload["model"] = args.model
            results.append(payload)

        save_json(metadata_vectors_path(paths.output_dir), results)

        store_meta = load_json(store_metadata_path(paths.output_dir), default_store_metadata())
        fulltext_vectors = load_json(fulltext_vectors_path(paths.output_dir), [])
        fulltext_chunks = sum(len(item.get("chunks", [])) for item in fulltext_vectors)
        store_meta = update_store_metadata(
            store_meta,
            paths=paths,
            model_name=args.model,
            embedding_dimension=model.get_sentence_embedding_dimension(),
            metadata_count=len(results),
            fulltext_count=len(fulltext_vectors),
            fulltext_chunks=fulltext_chunks,
            operation="build_metadata_full",
        )
        save_json(store_metadata_path(paths.output_dir), store_meta)
        write_store_readme(paths.output_dir, store_meta)

        print_json(
            {
                "snapshot_db": str(snapshot_db),
                "metadata_vectors": str(metadata_vectors_path(paths.output_dir)),
                "item_count": len(results),
                "embedding_dimension": model.get_sentence_embedding_dimension(),
                "model": args.model,
            }
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
