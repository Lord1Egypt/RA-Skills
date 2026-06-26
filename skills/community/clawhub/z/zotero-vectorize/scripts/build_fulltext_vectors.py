#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from zotero_vectorize_lib import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_FULLTEXT_BATCH_SIZE,
    DEFAULT_MODEL,
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
    parser = argparse.ArgumentParser(description="Build full-text vectors from Zotero PDF attachments.")
    parser.add_argument("--data-dir")
    parser.add_argument("--db")
    parser.add_argument("--storage-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_FULLTEXT_BATCH_SIZE)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--chunk-overlap", type=int, default=DEFAULT_CHUNK_OVERLAP)
    parser.add_argument("--snapshot-db", default=None)
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
        model = get_embedding_model(args.model)
        pdf_index = scan_storage_for_pdfs(paths.storage_dir)
        pdf_parent_rows = get_pdf_parent_rows(conn)

        results = []
        failures = []
        for row in pdf_parent_rows:
            item_id = int(row["itemID"])
            attachment = get_item_pdf_attachment(conn, item_id)
            if attachment is None:
                failures.append({"itemID": item_id, "error": "No PDF attachment row found"})
                continue
            pdf_path = resolve_attachment_path(attachment["path"], paths.storage_dir, pdf_index)
            if pdf_path is None:
                failures.append({"itemID": item_id, "error": f"PDF file not found for path {attachment['path']}"})
                continue

            try:
                pdf_text = extract_pdf_text(pdf_path)
            except Exception as exc:  # noqa: BLE001
                failures.append({"itemID": item_id, "error": f"PDF extraction failed: {exc}"})
                continue

            chunks = chunk_text(
                pdf_text["full_text"],
                chunk_size=args.chunk_size,
                overlap=args.chunk_overlap,
            )
            vectors = encode_texts(
                model,
                [chunk["text"] for chunk in chunks],
                batch_size=args.batch_size,
            )

            metadata = None
            try:
                metadata, _ = build_item_metadata(
                    conn,
                    item_id,
                    fields_map=fields_map,
                    item_types_map=item_types_map,
                )
            except Exception:
                metadata = {"title": f"Item {item_id}"}

            results.append(
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

        save_json(fulltext_vectors_path(paths.output_dir), results)

        store_meta = load_json(store_metadata_path(paths.output_dir), default_store_metadata())
        metadata_vectors = load_json(metadata_vectors_path(paths.output_dir), [])
        total_chunks = sum(len(item.get("chunks", [])) for item in results)
        store_meta = update_store_metadata(
            store_meta,
            paths=paths,
            model_name=args.model,
            embedding_dimension=model.get_sentence_embedding_dimension(),
            metadata_count=len(metadata_vectors),
            fulltext_count=len(results),
            fulltext_chunks=total_chunks,
            operation="build_fulltext_full",
        )
        store_meta["statistics"]["fulltext_failures"] = failures
        store_meta["chunk_size"] = args.chunk_size
        store_meta["chunk_overlap"] = args.chunk_overlap
        save_json(store_metadata_path(paths.output_dir), store_meta)
        write_store_readme(paths.output_dir, store_meta)

        print_json(
            {
                "snapshot_db": str(snapshot_db),
                "fulltext_vectors": str(fulltext_vectors_path(paths.output_dir)),
                "item_count": len(results),
                "chunk_count": total_chunks,
                "failure_count": len(failures),
                "embedding_dimension": model.get_sentence_embedding_dimension(),
                "model": args.model,
            }
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
