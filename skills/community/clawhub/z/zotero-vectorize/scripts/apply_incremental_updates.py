#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from zotero_vectorize_lib import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_FULLTEXT_BATCH_SIZE,
    DEFAULT_METADATA_BATCH_SIZE,
    DEFAULT_MODEL,
    backup_store_files,
    build_item_metadata,
    chunk_text,
    connect_db,
    default_store_metadata,
    encode_texts,
    ensure_output_dir,
    extract_pdf_text,
    fulltext_vectors_path,
    get_embedding_model,
    get_fields_map,
    get_item_pdf_attachment,
    get_item_types_map,
    get_pdf_parent_rows,
    get_top_level_items,
    load_json,
    metadata_vectors_path,
    print_json,
    resolve_attachment_path,
    resolve_paths,
    save_json,
    scan_storage_for_pdfs,
    snapshot_database,
    store_metadata_path,
    update_store_metadata,
    write_store_readme,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply incremental updates to metadata/fulltext vector stores.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--metadata-batch-size", type=int, default=DEFAULT_METADATA_BATCH_SIZE)
    parser.add_argument("--fulltext-batch-size", type=int, default=DEFAULT_FULLTEXT_BATCH_SIZE)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--chunk-overlap", type=int, default=DEFAULT_CHUNK_OVERLAP)
    parser.add_argument("--snapshot-db", default=None)
    parser.add_argument(
        "--item-id",
        action="append",
        type=int,
        default=None,
        help="Restrict updates to one or more specific Zotero itemIDs.",
    )
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--fulltext-only", action="store_true")
    args = parser.parse_args()

    if args.metadata_only and args.fulltext_only:
        raise SystemExit("Choose at most one of --metadata-only or --fulltext-only")

    paths = resolve_paths(
        data_dir=args.data_dir,
        db_path=args.db,
        storage_dir=args.storage_dir,
        output_dir=args.output_dir,
    )
    ensure_output_dir(paths.output_dir)
    snapshot_db = Path(args.snapshot_db).expanduser() if args.snapshot_db else snapshot_database(paths.db_path, paths.output_dir / "snapshots")

    metadata_vectors = load_json(metadata_vectors_path(paths.output_dir), [])
    fulltext_vectors = load_json(fulltext_vectors_path(paths.output_dir), [])
    store_meta = load_json(store_metadata_path(paths.output_dir), default_store_metadata())

    metadata_ids = {int(item["itemID"]) for item in metadata_vectors}
    fulltext_ids = {int(item["itemID"]) for item in fulltext_vectors}
    requested_ids = set(args.item_id or [])

    conn = connect_db(snapshot_db)
    try:
        fields_map = get_fields_map(conn)
        item_types_map = get_item_types_map(conn)
        top_item_ids = [int(row["itemID"]) for row in get_top_level_items(conn)]
        pdf_parent_ids = [int(row["itemID"]) for row in get_pdf_parent_rows(conn)]

        missing_metadata_ids = [item_id for item_id in top_item_ids if item_id not in metadata_ids]
        missing_fulltext_ids = [item_id for item_id in pdf_parent_ids if item_id not in fulltext_ids]

        if requested_ids:
            missing_metadata_ids = [item_id for item_id in missing_metadata_ids if item_id in requested_ids]
            missing_fulltext_ids = [item_id for item_id in missing_fulltext_ids if item_id in requested_ids]

        if args.metadata_only:
            missing_fulltext_ids = []
        if args.fulltext_only:
            missing_metadata_ids = []

        backups = backup_store_files(paths.output_dir, keep=2)
        model = get_embedding_model(args.model)

        added_metadata_ids = []
        if missing_metadata_ids:
            texts = []
            payloads = []
            for item_id in missing_metadata_ids:
                metadata, embedding_text = build_item_metadata(
                    conn,
                    item_id,
                    fields_map=fields_map,
                    item_types_map=item_types_map,
                )
                row = conn.execute(
                    "SELECT key, itemTypeID FROM items WHERE itemID = ?",
                    (item_id,),
                ).fetchone()
                payloads.append(
                    {
                        "itemID": item_id,
                        "key": row["key"],
                        "metadata": metadata,
                        "embedding_text": embedding_text,
                        "itemType": item_types_map.get(int(row["itemTypeID"]), "unknown"),
                    }
                )
                texts.append(embedding_text)
            vectors = encode_texts(model, texts, batch_size=args.metadata_batch_size)
            for payload, vector in zip(payloads, vectors):
                payload = dict(payload)
                payload["vector"] = vector
                payload["vector_dimension"] = len(vector)
                payload["model"] = args.model
                metadata_vectors.append(payload)
                added_metadata_ids.append(payload["itemID"])

        added_fulltext_ids = []
        if missing_fulltext_ids:
            pdf_index = scan_storage_for_pdfs(paths.storage_dir)
            for item_id in missing_fulltext_ids:
                attachment = get_item_pdf_attachment(conn, item_id)
                if attachment is None:
                    continue
                pdf_path = resolve_attachment_path(attachment["path"], paths.storage_dir, pdf_index)
                if pdf_path is None:
                    continue
                pdf_text = extract_pdf_text(pdf_path)
                chunks = chunk_text(pdf_text["full_text"], chunk_size=args.chunk_size, overlap=args.chunk_overlap)
                vectors = encode_texts(model, [chunk["text"] for chunk in chunks], batch_size=args.fulltext_batch_size)
                metadata, _ = build_item_metadata(
                    conn,
                    item_id,
                    fields_map=fields_map,
                    item_types_map=item_types_map,
                )
                fulltext_vectors.append(
                    {
                        "itemID": item_id,
                        "attachmentID": int(attachment["attachmentID"]),
                        "title": metadata.get("title", f"Item {item_id}"),
                        "itemType": attachment["typeName"],
                        "total_pages": pdf_text["total_pages"],
                        "pdf_file": pdf_path.name,
                        "chunks": [
                            {
                                "chunk_id": f"{item_id}_{idx}",
                                "text": chunk["text"],
                                "vector": vector,
                                "word_count": chunk["word_count"],
                                "page": 1,
                            }
                            for idx, (chunk, vector) in enumerate(zip(chunks, vectors))
                        ],
                    }
                )
                added_fulltext_ids.append(item_id)

        save_json(metadata_vectors_path(paths.output_dir), metadata_vectors)
        save_json(fulltext_vectors_path(paths.output_dir), fulltext_vectors)

        total_chunks = sum(len(item.get("chunks", [])) for item in fulltext_vectors)
        updated_item_ids = sorted(set(added_metadata_ids) | set(added_fulltext_ids))
        store_meta = update_store_metadata(
            store_meta,
            paths=paths,
            model_name=args.model,
            embedding_dimension=model.get_sentence_embedding_dimension(),
            metadata_count=len(metadata_vectors),
            fulltext_count=len(fulltext_vectors),
            fulltext_chunks=total_chunks,
            operation="incremental_apply",
            item_ids=updated_item_ids,
        )
        store_meta["chunk_size"] = args.chunk_size
        store_meta["chunk_overlap"] = args.chunk_overlap
        save_json(store_metadata_path(paths.output_dir), store_meta)
        write_store_readme(paths.output_dir, store_meta)

        print_json(
            {
                "snapshot_db": str(snapshot_db),
                "output_dir": str(paths.output_dir),
                "created_backups": [str(path) for path in backups],
                "added_metadata_item_ids": added_metadata_ids,
                "added_fulltext_item_ids": added_fulltext_ids,
                "metadata_vectors_count": len(metadata_vectors),
                "fulltext_vectors_count": len(fulltext_vectors),
                "fulltext_chunk_count": total_chunks,
            }
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
