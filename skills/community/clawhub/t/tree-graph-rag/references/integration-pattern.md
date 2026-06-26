# Integration Pattern

## What this skill contains
- A schema for storing document trees, contents, entities, and relationships in PostgreSQL
- Glue code for the two critical seams:
  - flattening PageIndex tree output into relational rows
  - anchoring LightRAG-style entities and relations onto `node_id`
- Retrieval code that starts from graph hits and resolves back to tree context
- Query templates for the most common hybrid lookups

## What this skill does not reimplement
- PDF parsing, TOC extraction, node refinement, and summary generation from PageIndex
- Full entity extraction prompts, graph deduplication, vector storage, and graph analytics from LightRAG
- Web APIs, UI, auth, background jobs, storage adapters, or end-to-end product scaffolding

## How to use it correctly
1. Use your existing PageIndex pipeline to produce tree nodes and content.
2. Use your preferred LLM extraction pipeline to return normalized entities and relationships.
3. Use the scripts in this skill as the canonical persistence and retrieval pattern.
4. Use the query templates as a baseline when implementing answer-time retrieval.
5. Extend from this base inside your real service layer instead of copying LightRAG and PageIndex wholesale into the skill.
