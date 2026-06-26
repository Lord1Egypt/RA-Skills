# Guide 07 — Ingestion Pipeline

## Purpose

This guide provides a complete, production-grade ingestion pipeline implementation — covering source capture, change detection, upsert patterns, deduplication, idempotency, and lifecycle management.

---

## Complete Pipeline Implementation

```python
import hashlib
import uuid
from datetime import datetime, timezone
from qdrant_client import QdrantClient, models
from typing import Optional

class IngestionPipeline:
    
    def __init__(self, qdrant_client: QdrantClient, embed_fn, config: dict):
        self.client = qdrant_client
        self.embed = embed_fn  # Function: list[str] → list[{dense, sparse}] or list[list[float]]
        self.config = config
        self.run_id = str(uuid.uuid4())
    
    def ingest_document(
        self,
        source_content: str,
        source_metadata: dict,
        collection_name: str,
        normalizer,
        chunker,
        tagger,
        classifier,
    ) -> dict:
        """
        Full pipeline for a single source document.
        Returns a summary of what was done.
        """
        
        # Step 1: Normalization
        normalized_text = normalizer.normalize(source_content, source_metadata)
        
        # Step 2: Document-level hash (change detection)
        doc_hash = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()
        
        # Step 3: Change detection — check if we've seen this document before
        existing_hash = self._get_existing_hash(
            source_metadata["source_system"],
            source_metadata["source_record_id"],
            collection_name,
        )
        
        if existing_hash == doc_hash:
            # Content unchanged — only refresh metadata timestamps
            self._refresh_metadata_only(source_metadata, collection_name)
            return {"status": "unchanged", "doc_hash": doc_hash}
        
        # Step 4: Classification
        sensitivity = classifier.classify(normalized_text, source_metadata)
        
        # Step 5: Scope tagging
        data_scope_tags = tagger.derive_tags(source_metadata)
        
        # Step 6: Chunking
        chunks = chunker.chunk(normalized_text, source_metadata)
        new_total = len(chunks)
        
        # Step 7: Build payloads, hash chunks, embed, upsert
        points = []
        for i, chunk_text in enumerate(chunks):
            chunk_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            
            # Check for within-source duplicate
            if self._is_duplicate_chunk(chunk_hash, source_metadata["source_record_id"], collection_name):
                continue  # Update metadata in place rather than writing new point
            
            doc_id = f"{source_metadata['source_type']}_{source_metadata['source_record_id']}_{i}"
            
            payload = self._build_payload(
                source_metadata=source_metadata,
                doc_id=doc_id,
                chunk_text=chunk_text,
                chunk_index=i,
                chunk_total=new_total,
                chunk_hash=chunk_hash,
                doc_hash=doc_hash,
                sensitivity=sensitivity,
                data_scope_tags=data_scope_tags,
                chunk_strategy=chunker.strategy_name,
            )
            
            # Step 8: Embedding
            embedding = self.embed([chunk_text])[0]
            
            # Build Qdrant point
            if isinstance(embedding, dict):
                # Hybrid: {dense: [...], sparse: {indices: [...], values: [...]}}
                vector = {
                    "dense": embedding["dense"],
                    "sparse": models.SparseVector(
                        indices=embedding["sparse"]["indices"],
                        values=embedding["sparse"]["values"],
                    )
                }
            else:
                # Dense-only: [...]
                vector = embedding
            
            points.append(models.PointStruct(
                id=self._stable_uuid(doc_id),
                vector=vector,
                payload=payload,
            ))
        
        # Step 9: Upsert all points
        if points:
            self.client.upsert(
                collection_name=collection_name,
                points=points,
                wait=True,  # Wait for confirmation before returning
            )
        
        # Step 10: Delete stale chunks (if re-ingestion produced fewer chunks)
        old_total = self._get_old_chunk_total(
            source_metadata["source_record_id"], collection_name
        )
        if old_total and old_total > new_total:
            self._delete_stale_chunks(
                source_metadata, collection_name, new_total, old_total
            )
        
        return {
            "status": "ingested",
            "doc_id_base": f"{source_metadata['source_type']}_{source_metadata['source_record_id']}",
            "chunks_written": len(points),
            "chunks_total": new_total,
            "sensitivity": sensitivity,
            "run_id": self.run_id,
        }
    
    def _stable_uuid(self, doc_id: str) -> str:
        """Generate a stable UUID from a doc_id string (deterministic)."""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))
    
    def _build_payload(self, **kwargs) -> dict:
        """Assemble the complete chunk payload."""
        now = datetime.now(timezone.utc).isoformat()
        source_metadata = kwargs["source_metadata"]
        
        return {
            "doc_id": kwargs["doc_id"],
            "source_type": source_metadata["source_type"],
            "source_system": source_metadata["source_system"],
            "source_record_id": source_metadata["source_record_id"],
            "integration_id": source_metadata.get("integration_id", "unknown"),
            "parent_doc_id": source_metadata.get("parent_doc_id", kwargs["doc_id"]),
            "document_content_hash": kwargs["doc_hash"],
            "chunk_index": kwargs["chunk_index"],
            "chunk_total": kwargs["chunk_total"],
            "content_hash": kwargs["chunk_hash"],
            "created_at": source_metadata.get("created_at", now),
            "ingested_at": now,
            "modified_at": source_metadata.get("modified_at", now),
            "source_last_modified": source_metadata.get("source_last_modified", now),
            "author_id": source_metadata.get("author_id", ""),
            "author_name": source_metadata.get("author_name", ""),
            "author_email": source_metadata.get("author_email"),
            "author_department": source_metadata.get("author_department"),
            "project_ids": source_metadata.get("project_ids", []),
            "team_ids": source_metadata.get("team_ids", []),
            "workspace_id": source_metadata["workspace_id"],
            "org_id": source_metadata["org_id"],
            "sensitivity": kwargs["sensitivity"],
            "allowed_groups": source_metadata.get("allowed_groups", []),
            "owner_user_ids": source_metadata.get("owner_user_ids", []),
            "is_pii": source_metadata.get("is_pii", False),
            "retention_days": source_metadata.get("retention_days", 1095),
            "data_scope_tags": kwargs["data_scope_tags"],
            "language": source_metadata.get("language", "en"),
            "content_type": source_metadata.get("content_type", "document"),
            "content_subtype": source_metadata.get("content_subtype"),
            "title": source_metadata.get("title"),
            "summary": None,  # Populate separately if using a summarization model
            "token_count": len(kwargs["chunk_text"]) // 4,
            "chunk_strategy": kwargs["chunk_strategy"],
            "embedding_model": self.config["embedding_model"],
            "sparse_model": self.config.get("sparse_model", "none"),
            "schema_version": "2.2",
            "ingestion_run_id": self.run_id,
            "connector_version": self.config["connector_version"],
            "normalizer_version": self.config["normalizer_version"],
            "chunker_version": self.config["chunker_version"],
            "source_metadata": source_metadata.get("source_specific", {}),
        }
    
    def _get_existing_hash(self, source_system: str, record_id: str, collection: str) -> Optional[str]:
        """Look up the stored document_content_hash for this record."""
        try:
            results = self.client.scroll(
                collection_name=collection,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(key="source_system", match=models.MatchValue(value=source_system)),
                        models.FieldCondition(key="source_record_id", match=models.MatchValue(value=record_id)),
                        models.FieldCondition(key="chunk_index", match=models.MatchValue(value=0)),
                    ]
                ),
                with_payload=True,
                limit=1,
            )
            if results[0]:
                return results[0][0].payload.get("document_content_hash")
        except Exception:
            pass
        return None
    
    def _is_duplicate_chunk(self, content_hash: str, source_record_id: str, collection: str) -> bool:
        """Check if a chunk with this content_hash already exists for this source record."""
        results = self.client.scroll(
            collection_name=collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="content_hash", match=models.MatchValue(value=content_hash)),
                    models.FieldCondition(key="source_record_id", match=models.MatchValue(value=source_record_id)),
                ]
            ),
            limit=1,
        )
        return len(results[0]) > 0
    
    def _get_old_chunk_total(self, source_record_id: str, collection: str) -> Optional[int]:
        """Get the previously stored chunk_total for this record."""
        results = self.client.scroll(
            collection_name=collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="source_record_id", match=models.MatchValue(value=source_record_id)),
                    models.FieldCondition(key="chunk_index", match=models.MatchValue(value=0)),
                ]
            ),
            with_payload=True,
            limit=1,
        )
        if results[0]:
            return results[0][0].payload.get("chunk_total")
        return None
    
    def _delete_stale_chunks(
        self, source_metadata: dict, collection: str, new_total: int, old_total: int
    ):
        """Delete chunks whose chunk_index is now out of range after re-ingestion."""
        stale_ids = []
        for stale_index in range(new_total, old_total):
            doc_id = f"{source_metadata['source_type']}_{source_metadata['source_record_id']}_{stale_index}"
            stale_ids.append(self._stable_uuid(doc_id))
        
        if stale_ids:
            self.client.delete(
                collection_name=collection,
                points_selector=models.PointIdsList(points=stale_ids),
            )
    
    def _refresh_metadata_only(self, source_metadata: dict, collection: str):
        """For unchanged content, update only the ingested_at and source_last_modified timestamps."""
        now = datetime.now(timezone.utc).isoformat()
        self.client.set_payload(
            collection_name=collection,
            payload={
                "ingested_at": now,
                "source_last_modified": source_metadata.get("source_last_modified", now),
                "ingestion_run_id": self.run_id,
            },
            points=models.Filter(
                must=[
                    models.FieldCondition(
                        key="source_record_id",
                        match=models.MatchValue(value=source_metadata["source_record_id"])
                    )
                ]
            ),
        )
    
    def delete_document(self, source_type: str, source_record_id: str, collection: str):
        """Hard-delete all chunks for a source record (e.g., content deleted from source)."""
        self.client.delete(
            collection_name=collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(key="source_type", match=models.MatchValue(value=source_type)),
                        models.FieldCondition(key="source_record_id", match=models.MatchValue(value=source_record_id)),
                    ]
                )
            ),
        )
```

---

## Lifecycle Event Handling

| Event | Action |
|---|---|
| **Create** | Run full ingestion pipeline → upsert chunks |
| **Update** | Detect via `document_content_hash` → re-normalize, re-chunk, upsert, delete stale chunks |
| **Delete** | Hard-delete all chunks for the `source_record_id` |
| **Move / reclassify** | Metadata refresh + collection migration if sensitivity tier changes |
| **Access revoked** | Hard-delete if the content should no longer be retrievable |

### Collection Migration (Sensitivity Change)

```python
def migrate_chunks_to_collection(
    client: QdrantClient,
    source_record_id: str,
    old_collection: str,
    new_collection: str,
    new_sensitivity: str,
    new_data_scope_tags: list[str],
    audit_logger,
):
    """Move chunks from one collection to another when sensitivity changes."""
    
    # 1. Retrieve all chunks for this record from the old collection
    results, _ = client.scroll(
        collection_name=old_collection,
        scroll_filter=models.Filter(
            must=[models.FieldCondition(
                key="source_record_id",
                match=models.MatchValue(value=source_record_id)
            )]
        ),
        with_payload=True,
        with_vectors=True,
        limit=1000,
    )
    
    if not results:
        return
    
    old_sensitivity = results[0].payload.get("sensitivity")
    
    # 2. Update sensitivity and scope tags
    now = datetime.now(timezone.utc).isoformat()
    new_points = []
    for point in results:
        updated_payload = {
            **point.payload,
            "sensitivity": new_sensitivity,
            "data_scope_tags": new_data_scope_tags,
            "ingested_at": now,
        }
        new_points.append(models.PointStruct(
            id=point.id,
            vector=point.vector,
            payload=updated_payload,
        ))
    
    # 3. Write to new collection
    client.upsert(collection_name=new_collection, points=new_points, wait=True)
    
    # 4. Delete from old collection
    client.delete(
        collection_name=old_collection,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[models.FieldCondition(
                    key="source_record_id",
                    match=models.MatchValue(value=source_record_id)
                )]
            )
        ),
    )
    
    # 5. Audit log
    audit_logger.log_reclassification(
        source_record_id=source_record_id,
        old_sensitivity=old_sensitivity,
        new_sensitivity=new_sensitivity,
        timestamp=now,
        doc_ids=[p.payload["doc_id"] for p in results],
    )
```

---

## Deduplication

### Within-Source Deduplication
Before writing a chunk, check if a point with the same `content_hash` and `parent_doc_id` already exists in the target collection. On match, update metadata in place rather than writing a new point.

### Cross-Source Deduplication
Exact duplicates across different `source_type` values are retained as separate chunks because they represent distinct provenance. At retrieval time, near-duplicate results from different sources should be collapsed or down-ranked.

---

## Error Handling and Retry

```python
import time
from functools import wraps

def with_exponential_backoff(max_retries: int = 5, base_delay: float = 1.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        # Route to dead-letter queue after max retries
                        dead_letter_queue.push({"fn": fn.__name__, "args": args, "error": str(e)})
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        return wrapper
    return decorator
```

Failed lifecycle events (after max retries) must be routed to a dead-letter queue for manual review.

---

## Idempotency Checklist

Before deploying an ingestion pipeline to production, verify:

- [ ] `doc_id` format is deterministic — no timestamps, no random components
- [ ] All writes use `upsert`, never raw `insert`
- [ ] Same input run twice produces the same Qdrant state (no duplicate points)
- [ ] Stale chunk cleanup runs after every re-ingestion
- [ ] `document_content_hash` change detection is working (run a golden doc test)
- [ ] `ingestion_run_id` is a fresh UUID per run (not per chunk)
