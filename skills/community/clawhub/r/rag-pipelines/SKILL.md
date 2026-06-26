---
name: rag-pipelines
description: Deep RAG workflow—document ingestion, chunking, metadata, retrieval and reranking, grounding and citations, evaluation, and failure modes (hallucination, staleness). Use when building or debugging retrieval-augmented generation systems.
---

# RAG Pipelines (Deep Workflow)

RAG quality is dominated by **chunking**, **retrieval**, and **evaluation**—not the LLM alone. Treat the system as data engineering plus generation with explicit failure modes.

## When to Offer This Workflow

**Trigger conditions:**

- Building Q&A over internal docs, support assistants, or copilots
- Hallucinations, wrong citations, or stale answers
- New content types (PDF, HTML, code repositories)

**Initial offer:**

Use **six stages**: (1) task & success criteria, (2) ingestion & cleaning, (3) chunking & metadata, (4) retrieval & rerank, (5) generation & grounding, (6) evaluation & monitoring). Confirm embedding model and retrieval stack (vector DB, search engine, hybrid).

---

## Stage 1: Task & Success Criteria

**Goal:** Define what a “good” answer contains: required citations, length, tone, and when to refuse.

**Exit condition:** Written rubric with examples of acceptable vs unacceptable answers.

---

## Stage 2: Ingestion & Cleaning

**Goal:** Deterministic text extraction (strip boilerplate, handle PDF/OCR if needed); deduplicate documents; track source URL and `updated_at` for staleness.

### Practices

- Version pipelines when parsers change (re-embed job)

---

## Stage 3: Chunking & Metadata

**Goal:** Tune chunk size and overlap to query patterns—not one global token count for all content.

### Practices

- Attach metadata for ACL filtering (tenant, product area)
- Prefer structure-aware splits for docs (headings, sections)

---

## Stage 4: Retrieval & Rerank

**Goal:** Hybrid lexical + dense retrieval often beats vector-only for keyword-heavy queries.

### Practices

- Cross-encoder reranking on top-k for quality (watch latency)
- Query rewriting for multi-turn contexts

---

## Stage 5: Generation & Grounding

**Goal:** System prompts that require using only provided context; explicit “not found” behavior; optional citation format (snippet, doc id, link).

---

## Stage 6: Evaluation & Monitoring

**Goal:** Offline golden questions with expected supporting docs; online thumbs-down reasons; monitor retrieval hit rate, nDCG@k, and age of sources used.

---

## Final Review Checklist

- [ ] Rubric and refusal behavior defined
- [ ] Ingestion deterministic; dedupe and versioning
- [ ] Chunking and metadata match queries and ACLs
- [ ] Hybrid retrieval and rerank tuned with metrics
- [ ] Grounding and citation behavior enforced in prompts
- [ ] Offline eval plus production monitoring

## Tips for Effective Guidance

- Debug retrieval before blaming the LLM.
- Long chunks hurt precision; short chunks hurt context—sweep experiments.
- See also **vector-databases** and **llm-evaluation** skills for depth.

## Handling Deviations

- **Code RAG:** symbol- or AST-aware chunking often beats line-based splits.
- **High-stakes domains:** add human review gates and audit logs for sources cited.
