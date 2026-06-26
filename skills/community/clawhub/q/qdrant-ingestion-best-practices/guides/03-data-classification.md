# Guide 03 — Data Classification & Collections

## Purpose

This guide defines the four-tier sensitivity model, collection architecture patterns, and classification logic for determining where each chunk belongs in Qdrant.

---

## Four-Tier Sensitivity Model

Every chunk must be assigned exactly one sensitivity tier at ingest time. Classification must never be deferred to retrieval time.

| Tier | Description | Target Collection |
|---|---|---|
| `public` | Explicitly approved for external distribution. Marketing materials, published docs, public blog posts. | `company_memory` |
| `internal` | Intended for all staff but not for external distribution. Public Slack channels, all-hands transcripts, internal project docs. | `company_memory` |
| `restricted` | Limited to specific groups. Executive email, finance reports, legal contracts, HR communications (non-PII). | `restricted_memory` |
| `confidential` | Contains PII or requires highest protection. Salary data, performance reviews, health records, tax identifiers. | `pii_memory` |

**Default tier:** When no rule matches and no classifier flags the content, default to `internal`.

---

## Classification Logic (Precedence Order)

Apply in this exact order — stop at the first match:

1. **Explicit override** — A human-applied classification label on the source content. Highest precedence. Always respected.

2. **Rule-based classification** — Deterministic rules based on source metadata:
   - Folder location (e.g., `/Finance/Reports/` → `restricted`)
   - Distribution list (e.g., executives-only DL → `restricted`)
   - Channel type (e.g., `private` Slack channel with HR members → `restricted`)
   - Sender/recipient patterns (e.g., external domain sender → review)
   - Document sharing scope (e.g., `specific` share → at least `restricted`)

3. **Content-based classifier** — For content that cannot be classified by metadata alone, scan for signals:
   - Salary figures, compensation data → `confidential`
   - Tax identifiers, SSN, health information → `confidential`
   - Legal contract language → `restricted`
   - Explicitly internal communications → `internal`
   - This is `model_inferred` — log the classification event for audit.

4. **Default** — `internal` if nothing matches.

---

## Collection Architecture

### Standard Three-Collection Pattern

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

# Shared HNSW config for all collections
hnsw_config = models.HnswConfigDiff(m=16, ef_construct=100)

# Dense-only collection (text-embedding-3-small)
def create_collection_dense(name: str):
    client.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE,
            hnsw_config=hnsw_config,
        ),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True,
            )
        ),
    )

# Hybrid collection (BGE-M3: dense 1024-dim + sparse SPLADE)
def create_collection_hybrid(name: str):
    client.create_collection(
        collection_name=name,
        vectors_config={
            "dense": models.VectorParams(
                size=1024,  # BGE-M3 dense dimension
                distance=models.Distance.COSINE,
                hnsw_config=hnsw_config,
            )
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams(
                modifier=models.Modifier.IDF  # Enable IDF for BM25-style sparse
            )
        },
    )

# Create the three standard collections
create_collection_hybrid("company_memory")
create_collection_hybrid("restricted_memory")
create_collection_hybrid("pii_memory")
```

### HNSW Tuning by Collection Size

| Collection Size | Recommended m | Recommended ef_construct |
|---|---|---|
| < 100K chunks | 16 | 100 |
| 100K – 1M chunks | 32 | 200 |
| > 1M chunks | 64 | 400 |

Increasing `m` improves recall but increases memory and build time. Increase only when measured recall drops below target.

### Quantization

For production at scale, use scalar quantization (INT8) to reduce memory by ~75% with minimal quality loss:

```python
quantization_config=models.ScalarQuantization(
    scalar=models.ScalarQuantizationConfig(
        type=models.ScalarType.INT8,
        quantile=0.99,    # Clips outlier values for better quantization
        always_ram=True,  # Keep quantized vectors in RAM for speed
    )
)
```

For very large collections (>10M chunks) where memory is critical, binary quantization reduces by 32x but requires careful quality validation:

```python
quantization_config=models.BinaryQuantization(
    binary=models.BinaryQuantizationConfig(always_ram=True)
)
```

---

## Multi-Tenancy Pattern

If you're building a SaaS system with multiple organizations sharing a single Qdrant cluster, use the `is_tenant=True` flag on the `org_id` index rather than creating separate collections per tenant:

```python
# Create the tenant-aware payload index
client.create_payload_index(
    collection_name="company_memory",
    field_name="org_id",
    field_schema=models.KeywordIndexParams(
        type="keyword",
        is_tenant=True,  # Co-locates vectors for the same org for performance
    ),
)
```

**Why:** Creating one collection per tenant exhausts RAM and cluster resources quickly. Qdrant's `is_tenant` optimization co-locates tenant data in the HNSW graph, providing performance close to a dedicated collection without the resource cost.

**Always apply `org_id` as the outermost filter on every query** to enforce tenant isolation:

```python
client.query_points(
    collection_name="company_memory",
    query=dense_vector,
    using="dense",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="org_id",
                match=models.MatchValue(value="org-456")
            ),
            # ... additional filters
        ]
    ),
    limit=20,
)
```

---

## Classification Rules by Source Type

### Slack Channels
| Condition | Sensitivity |
|---|---|
| Public channel, no HR/Finance/Legal members | `internal` |
| Private channel with Finance or Legal members | `restricted` |
| HR channel discussing non-PII matters | `restricted` |
| Any channel with salary, SSN, health data | `confidential` |
| Any public-facing content | `public` |

### Email
| Condition | Sensitivity |
|---|---|
| External recipient in To/CC | `restricted` (at minimum) |
| Executive distribution list only | `restricted` |
| Finance or Legal content | `restricted` |
| Content with salary, compensation, health data | `confidential` |
| All-staff announcement | `internal` |

### Google Drive
| Condition | Sensitivity |
|---|---|
| Share scope = `anyone` | `public` |
| Share scope = `domain` | `internal` |
| Share scope = `specific`, folder = `/Finance/` or `/Legal/` | `restricted` |
| Share scope = `specific`, folder = `/HR/Compensation/` | `confidential` |

### Meeting Transcripts (Fireflies)
| Condition | Sensitivity |
|---|---|
| All-hands or team meeting, general topic | `internal` |
| Meeting with external attendees discussing internal matters | `restricted` |
| Executive strategy discussions | `restricted` |
| HR meeting with compensation or performance data | `confidential` |

### ClickUp Tasks
| Condition | Sensitivity |
|---|---|
| Project tasks in general spaces | `internal` |
| Tasks in Finance or Legal spaces | `restricted` |
| Tasks containing PII in description or comments | `confidential` |

---

## Sensitivity Change / Reclassification

When a source record's sensitivity tier changes (e.g., an internal document is reclassified as restricted), the ingestion pipeline must:

1. Detect the change via `document_content_hash` or source metadata comparison during the next sync cycle.
2. Re-ingest the affected chunks with the updated `sensitivity`, target collection, and any updated `data_scope_tags`.
3. Delete old chunks from the prior collection (e.g., `company_memory`).
4. Write new chunks to the correct collection (e.g., `restricted_memory`).
5. Log the reclassification event to the audit log: `old_sensitivity`, `new_sensitivity`, `doc_id`, timestamp.

Unlike access policy changes (which only require updating your orchestration layer config), sensitivity reclassification requires pipeline action because sensitivity determines **collection placement** — a hard architectural boundary in Qdrant.
