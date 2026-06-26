---
name: vector-databases
description: Deep vector database workflow—embedding choice, index algorithms, recall/latency trade-offs, hybrid search, filtering, operational tuning, and cost. Use when selecting or optimizing Pinecone, Milvus, Qdrant, Weaviate, pgvector, OpenSearch kNN, etc.
---

# Vector Databases (Deep Workflow)

Vector search is **approximate nearest neighbor (ANN)** at scale—**not** magic semantic understanding. Success requires **embedding model alignment**, **index parameters**, **metadata filters**, and **evaluation** against real queries.

## When to Offer This Workflow

**Trigger conditions:**

- Building RAG, similarity search, dedup, recommendations, anomaly clustering
- Comparing **managed vector DB** vs **pgvector** vs **search engine kNN**
- **Recall** issues, **stale** vectors, **slow** queries, or **cost** explosions

**Initial offer:**

Use **six stages**: (1) problem & metrics, (2) embeddings & schema, (3) index & parameters, (4) hybrid & filtering, (5) operations & cost, (6) evaluation & iteration. Confirm **scale** (vectors, QPS, dimension) and **latency SLO**.

---

## Stage 1: Problem & Metrics

**Goal:** Define **what “similar” means** for the product—not only cosine similarity.

### Questions

1. **Query types**: short keyword vs long paragraph? multilingual?
2. **Precision vs recall** preference: legal/medical may need **high precision**
3. **Freshness**: how often do vectors change? **Real-time** upserts?
4 **Ground truth**: any labeled **relevant** pairs for eval?

### Metrics

- **Recall@k**, **MRR**, **nDCG** when judgments exist; otherwise **human** spot checks + **proxy** tasks

**Exit condition:** **Success metric** and **minimum acceptable** recall/latency stated.

---

## Stage 2: Embeddings & Schema

**Goal:** **Stable embedding pipeline** with **versioning** and **metadata** design.

### Embeddings

- **Model choice**: domain fit (code vs general text); **dimension**; **distance metric** (cosine vs dot vs L2)—**match** DB defaults
- **Chunking** strategy upstream—bad chunks → bad retrieval regardless of DB

### Schema

- **Payload/metadata** per vector: `doc_id`, `tenant_id`, `acl`, `source`, **timestamps**
- **Multi-vector** per doc (passages) vs single centroid—**trade-offs**

### Versioning

- **Re-embed** all on model change—**plan** downtime or **dual-write** period

**Exit condition:** **ID strategy** + **metadata filter** needs documented.

---

## Stage 3: Index & Parameters

**Goal:** Pick **index type** and **build params** for data size and recall.

### Common families (vendor-specific names)

- **HNSW**: strong latency/recall; **memory** hungry; **tunable** `efConstruction`, `M`
- **IVF**: better memory; needs **training** **nlist**; **probe** tuning
- **PQ/OPQ**: compression—**recall** hit; good for **huge** scale

### Tuning loop

- Start **defaults**; **sweep** parameters with **benchmark** queries
- Watch **insert** throughput during **index build** on large backfills

**Exit condition:** **Benchmark** results: p95 latency vs recall at fixed **k**.

---

## Stage 4: Hybrid Search & Filtering

**Goal:** Combine **vector** similarity with **structured** constraints—most production needs this.

### Patterns

- **Pre-filter** metadata (tenant, date) **before** ANN when supported—**verify** filter selectivity
- **Hybrid**: BM25 + vector with **weighted** fusion or **rerank** stage
- **Reranking**: cross-encoder on **top-k** candidates—**quality** boost, **latency** cost

### Pitfalls

- **Filtering** that leaves **too few** candidates—empty results despite “similar” existing in other tenants

**Exit condition:** **Query plan** documented: ANN → filter → rerank (as applicable).

---

## Stage 5: Operations & Cost

**Goal:** **Reliable** ingestion, **monitoring**, and **predictable** bills.

### Ops

- **Upsert** idempotency; **delete** tombstones for compliance
- **Backups**, **multi-region** if needed—**eventual consistency** semantics per vendor
- **Capacity**: memory per node vs **sharding**; **replication** factor

### Cost

- **Managed** per **dimension × count**; **egress**; **query** units—**estimate** from **peak QPS**

**Exit condition:** **Runbook** for **reindex**, **scaling**, and **incident** “search degraded.”

---

## Stage 6: Evaluation & Iteration

**Goal:** **Continuous** improvement with **labeled** or **proxy** eval.

### Loop

- **Golden** query set updated when product changes
- **A/B** embedding models or **rerankers** with **guardrails** on latency
- **Monitor** **click-through**, **thumbs**, or **human** grading in RAG

### Debugging bad retrieval

- **Chunk** inspection, **metadata** leaks, **wrong** tenant filter, **stale** index

---

## Final Review Checklist

- [ ] Metrics and embedding/model versioning plan
- [ ] Index family chosen with benchmark evidence
- [ ] Hybrid/filter strategy matches product needs
- [ ] Ops: upsert, delete, scaling, backup understood
- [ ] Eval set and iteration process in place

## Tips for Effective Guidance

- **Never** promise “semantic search understands intent”—**ground** with eval.
- **pgvector** vs **specialized**: trade-offs on **scale**, **ops**, **features**—state honestly.
- Warn: **high-cardinality** filters + ANN can be **slow**—**design** metadata carefully.

## Handling Deviations

- **Tiny corpus**: **brute force** or **simple** index may suffice—avoid over-engineering.
- **Multimodal**: **separate** embedding spaces or **unified** model—**fusion** strategy required.
