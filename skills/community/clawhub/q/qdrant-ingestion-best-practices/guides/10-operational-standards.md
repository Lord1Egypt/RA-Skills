# Guide 10 — Operational Standards

## Purpose

This guide covers the operational requirements for running a production Qdrant RAG system: schema versioning, data retention, monitoring, conformance testing, and observability.

---

## Schema Versioning and Migration

### Version Management

The `schema_version` field enables backward-compatible evolution. When the schema is updated:

1. Increment the version number in the schema definition
2. Update all ingestion pipelines to write the new version
3. Provide a migration script for existing chunks
4. Configure the retrieval layer to gracefully handle chunks written under prior schema versions during the migration window

### Migration Pattern

```python
def migrate_schema(
    client: QdrantClient,
    collection: str,
    from_version: str,
    to_version: str,
    migration_fn: callable,
    migration_run_id: str,
    batch_size: int = 100,
):
    """
    Migrate all chunks in a collection from one schema version to another.
    Safe to re-run (idempotent): skips chunks already on the target version.
    """
    offset = None
    migrated = 0
    skipped = 0
    
    while True:
        results, next_offset = client.scroll(
            collection_name=collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="schema_version",
                        match=models.MatchValue(value=from_version)
                    )
                ]
            ),
            with_payload=True,
            limit=batch_size,
            offset=offset,
        )
        
        if not results:
            break
        
        for point in results:
            new_payload = migration_fn(point.payload)
            new_payload["schema_version"] = to_version
            new_payload["migration_run_id"] = migration_run_id
            
            client.set_payload(
                collection_name=collection,
                payload=new_payload,
                points=[point.id],
            )
            migrated += 1
        
        offset = next_offset
        if offset is None:
            break
    
    return {"migrated": migrated, "skipped": skipped}
```

### Migration Note: v2.1 → v2.2 (data_scope_tags)

During migration from v2.1 to v2.2, chunks without `data_scope_tags` will have no scope tags. Configure your orchestration layer to treat absent `data_scope_tags` as a pass-through (no tag filter applied) to avoid breaking retrieval for untagged content. Backfill high-value collections first. Record the `migration_run_id` on all backfilled chunks.

---

## Data Retention

```python
from datetime import datetime, timezone, timedelta

def run_retention_cleanup(client: QdrantClient, collection: str, batch_size: int = 500):
    """
    Delete chunks whose retention period has expired.
    retention_days counts from created_at.
    """
    now = datetime.now(timezone.utc)
    deleted_count = 0
    
    # Find expired chunks
    # Strategy: compute cutoff dates for common retention windows
    # (Alternative: use Qdrant datetime range filter if created_at is indexed as datetime)
    
    offset = None
    while True:
        results, next_offset = client.scroll(
            collection_name=collection,
            with_payload=True,
            limit=batch_size,
            offset=offset,
        )
        
        if not results:
            break
        
        expired_ids = []
        for point in results:
            payload = point.payload
            created_str = payload.get("created_at")
            retention_days = payload.get("retention_days", 1095)
            
            if not created_str:
                continue
            
            created_at = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
            expires_at = created_at + timedelta(days=retention_days)
            
            if now > expires_at:
                expired_ids.append(point.id)
                # Log deletion event
                _log_deletion(
                    doc_id=payload.get("doc_id"),
                    parent_doc_id=payload.get("parent_doc_id"),
                    deletion_timestamp=now.isoformat(),
                    reason="retention_expired",
                )
        
        if expired_ids:
            client.delete(
                collection_name=collection,
                points_selector=models.PointIdsList(points=expired_ids),
            )
            deleted_count += len(expired_ids)
        
        offset = next_offset
        if offset is None:
            break
    
    return {"deleted": deleted_count}

def _log_deletion(doc_id, parent_doc_id, deletion_timestamp, reason):
    """Audit log for deletion events."""
    print(f"DELETED doc_id={doc_id} parent={parent_doc_id} at={deletion_timestamp} reason={reason}")
    # Write to your audit log store
```

**Retention defaults by content type:**

| Content Type | Default Retention |
|---|---|
| Operational / conversational (Slack, email, transcripts) | 3 years (1,095 days) |
| Project documentation | 5 years (1,825 days) |
| Financial / legal records | 7 years (2,555 days) — check regulatory requirements |
| PII content | Per data privacy regulations (often shorter) |

---

## Conformance Testing

Every ingestion pipeline must pass automated conformance checks before being promoted to production. These are mandatory gates in CI/CD.

### Mandatory Conformance Checks

```python
class PipelineConformanceTests:
    
    def test_metadata_completeness(self, client, collection, sample_size=1000):
        """All required fields must be non-null on every chunk."""
        REQUIRED_FIELDS = [
            "doc_id", "source_type", "source_system", "source_record_id",
            "document_content_hash", "chunk_index", "chunk_total", "content_hash",
            "created_at", "ingested_at", "modified_at", "author_id", "author_name",
            "workspace_id", "org_id", "sensitivity", "allowed_groups", "owner_user_ids",
            "is_pii", "retention_days", "data_scope_tags", "language", "content_type",
            "token_count", "chunk_strategy", "embedding_model", "schema_version",
            "ingestion_run_id", "connector_version", "normalizer_version", "chunker_version",
        ]
        
        results, _ = client.scroll(collection_name=collection, limit=sample_size, with_payload=True)
        
        failures = []
        for point in results:
            for field in REQUIRED_FIELDS:
                if point.payload.get(field) is None:
                    failures.append({"doc_id": point.payload.get("doc_id"), "missing_field": field})
        
        assert not failures, f"Metadata completeness failures: {failures}"
    
    def test_data_scope_tags_coverage(self, client, collection, source_type, threshold=0.80):
        """At least 80% of newly ingested chunks per source type must have ≥1 data_scope_tag."""
        from datetime import datetime, timedelta, timezone
        
        cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        
        results, _ = client.scroll(
            collection_name=collection,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="source_type", match=models.MatchValue(value=source_type)),
                    models.FieldCondition(key="ingested_at", range=models.DatetimeRange(gte=cutoff)),
                ]
            ),
            with_payload=True,
            limit=5000,
        )
        
        if not results:
            return  # No recent ingestion to check
        
        tagged = sum(1 for p in results if p.payload.get("data_scope_tags"))
        coverage = tagged / len(results)
        
        assert coverage >= threshold, (
            f"data_scope_tags coverage for {source_type} is {coverage:.1%}, "
            f"below {threshold:.0%} threshold. Investigate tagging pipeline."
        )
    
    def test_deterministic_chunking(self, client, golden_docs: list, pipeline):
        """Re-ingest golden documents and verify chunks are byte-identical."""
        for golden_doc in golden_docs:
            previous_chunks = golden_doc["expected_chunks"]
            actual_chunks = pipeline.chunk(golden_doc["normalized_text"], golden_doc["metadata"])
            
            assert len(actual_chunks) == len(previous_chunks), (
                f"Chunk count mismatch for {golden_doc['id']}: "
                f"expected {len(previous_chunks)}, got {len(actual_chunks)}"
            )
            for i, (expected, actual) in enumerate(zip(previous_chunks, actual_chunks)):
                assert expected == actual, f"Chunk {i} mismatch for {golden_doc['id']}"
    
    def test_idempotent_rerun(self, client, collection, source_record_id, pipeline):
        """Re-run pipeline for a document and verify Qdrant point count doesn't increase."""
        before_count = self._count_chunks(client, collection, source_record_id)
        pipeline.ingest_document(...)  # Re-ingest
        after_count = self._count_chunks(client, collection, source_record_id)
        
        assert after_count == before_count, (
            f"Idempotency failure: chunk count went from {before_count} to {after_count}"
        )
    
    def test_duplicate_suppression(self, client, collection):
        """No duplicate content_hash values within the same parent_doc_id."""
        # Check for duplicate content_hashes within the same parent
        # Implementation: scroll and group by parent_doc_id, check content_hash uniqueness
        pass
    
    def test_delete_propagation(self, client, collection, source_record_id, pipeline):
        """Delete a source record and verify chunks are removed within propagation SLA."""
        pipeline.delete_document(source_type="slack", source_record_id=source_record_id, collection=collection)
        remaining = self._count_chunks(client, collection, source_record_id)
        assert remaining == 0, f"Delete propagation failed: {remaining} chunks remain"
    
    def test_lineage_fields_complete(self, client, collection, sample_size=1000):
        """ingestion_run_id, connector_version, normalizer_version, chunker_version must be set."""
        LINEAGE_FIELDS = ["ingestion_run_id", "connector_version", "normalizer_version", "chunker_version"]
        results, _ = client.scroll(collection_name=collection, limit=sample_size, with_payload=True)
        failures = [
            point.payload.get("doc_id")
            for point in results
            if any(not point.payload.get(f) for f in LINEAGE_FIELDS)
        ]
        assert not failures, f"Lineage field gaps in {len(failures)} chunks"
    
    def test_access_control_smoke(self, query_fn, test_cases: list):
        """
        For each agent configuration, verify that returned chunks satisfy expected filters.
        This validates the end-to-end filter chain, not just chunk payload.
        """
        for case in test_cases:
            results = query_fn(
                query=case["query"],
                permission_scope=case["permission_scope"],
            )
            for result in results:
                p = result.payload
                assert p["sensitivity"] in case["permitted_sensitivity"], (
                    f"Access control violation: chunk {p['doc_id']} has sensitivity "
                    f"{p['sensitivity']}, not in {case['permitted_sensitivity']}"
                )
    
    def _count_chunks(self, client, collection, source_record_id):
        results, _ = client.scroll(
            collection_name=collection,
            scroll_filter=models.Filter(
                must=[models.FieldCondition(
                    key="source_record_id",
                    match=models.MatchValue(value=source_record_id)
                )]
            ),
            limit=1000,
        )
        return len(results)
```

---

## Monitoring and Alerting

Instrument your pipeline for these signals:

| Signal | Alert Threshold | Action |
|---|---|---|
| Ingestion failure rate | > 1% of documents in a run | Investigate connector or pipeline error |
| Schema validation errors | Any | Block pipeline promotion; fix immediately |
| `data_scope_tags` coverage | < 80% of newly ingested chunks for any source type | Investigate tagging pipeline within one sprint |
| Retrieval p95 latency | Exceeds SLA (e.g., 500ms for hybrid) | Scale compute or tune HNSW parameters |
| Collection point count | Within 20% of collection capacity | Plan scaling |
| Stale data detection | Most recent `ingested_at` for active source > configurable threshold | Check connector health |
| Dead-letter queue depth | > configurable threshold | Review failed lifecycle events |
| Duplicate `content_hash` count | Any within same `parent_doc_id` | Deduplication regression |

---

## Golden Document Registry

Maintain a registry of golden documents for each content type. These are used for determinism testing and regression validation.

Each golden document must include:
- The raw source input
- The expected normalized output
- The expected chunk set (chunk text + metadata)
- The `chunker_version` and `normalizer_version` that produced this output

**Required coverage patterns (per source type):**
- Edited/deleted messages within threads
- Forwarded emails with nested quoted replies
- Documents with duplicate content or broken formatting
- Transcript segments with filler words and low-confidence speech
- Tasks with extensive comment threads
- Content that has been moved or reclassified
- Content where `data_scope_tags` derivation is ambiguous

Version the golden document registry alongside `chunker_version` and `normalizer_version`. When either bumps, update the expected outputs and document why the output changed.

---

## Replay Capability

The ingestion system must support replaying ingestion for:
- A specific document (by `source_record_id`)
- All documents from a specific source type
- All documents ingested within a date range
- All documents associated with a specific `ingestion_run_id`

Replay must be idempotent: replaying always produces the same final state in Qdrant as the original run (assuming the source content hasn't changed).

```python
def replay_ingestion(
    pipeline: IngestionPipeline,
    scope: dict,  # {"source_record_id": "..."} or {"source_type": "slack"} or {"run_id": "..."}
):
    """
    Replay ingestion for a specific scope.
    Fetches source records from the source system and re-ingests them.
    """
    source_records = fetch_source_records(scope)
    results = []
    for record in source_records:
        result = pipeline.ingest_document(record["content"], record["metadata"], ...)
        results.append(result)
    return results
```
