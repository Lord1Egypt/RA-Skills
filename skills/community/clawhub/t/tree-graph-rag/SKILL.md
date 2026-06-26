---
name: tree-graph-rag
description: Guide for designing and implementing a PostgreSQL database that fuses PageIndex-style document trees with LightRAG-style entity-relationship anchors. Use this skill when Claude needs to design schemas, write ingestion logic, or implement retrieval SQL for a hybrid tree-graph knowledge base, especially when converting nested tree output into relational tables.
---

# Tree-Graph Hybrid RAG 

This skill teaches Claude how to build the **database layer** of a Tree-Graph Hybrid RAG system. It focuses on the integration seam between PageIndex-style tree output and LightRAG-style graph extraction, both stored in PostgreSQL.

## Core Philosophy

- **Tree (Macro)**: Represents the document's native hierarchy. Gives the LLM the structural skeleton (Chapter -> Section).
- **Graph (Micro)**: Represents Entities and Relationships. Gives the LLM cross-document, fine-grained factual connections.
- **Fusion**: Every node and edge in the Graph is anchored to a specific `node_id` in the Tree, enabling bidirectional traversal (from graph detail to tree context, or tree context to graph detail).

## Bundled Resources

This skill includes the minimum resources needed to teach Claude the database design and data flow:

- **[schema.sql](references/schema.sql)**: The complete PostgreSQL table definitions required for this architecture.
- **[ingestion_core.py](scripts/ingestion_core.py)**: Python script demonstrating how to flatten the Tree JSON into Postgres and how to extract graph entities anchored to the tree.
- **[retrieval_core.py](scripts/retrieval_core.py)**: Python script demonstrating the Hybrid Retrieval logic (Querying the Graph to find Tree node_ids, then extracting the macro context).
- **[smoke_test.py](scripts/smoke_test.py)**: Minimal no-database smoke test that validates the ingestion and retrieval flow with a fake pool.
- **[integration-pattern.md](references/integration-pattern.md)**: Explains what this skill covers, what it intentionally does not reimplement, and where it should sit in a real service.
- **[queries.md](references/queries.md)**: Common SQL patterns for loading skeletons, anchoring graph hits, and assembling answer context.

## Standard Workflows

### 1. Indexing Workflow
1. **Tree Extraction**: Extract headers/TOC. Save skeleton to `nodes` and text to `node_contents`.
2. **Graph Extraction**: Pass each `node_contents` to an LLM to extract entities and relations.
3. **Anchoring**: Save entities/relations with their corresponding `node_id` as a foreign key.

### 2. Retrieval Workflow
1. **Entity/Relation Search**: Extract keywords from the user query. Search the `entities` and `relationships` tables to find matching factual details.
2. **Anchor Resolution**: Get the `node_id`s associated with the matched graph elements.
3. **Contextualization (Tree Traversal)**: Query the `nodes` table using the `node_id`s. Traverse up (`parent_id`) to gather the section titles and summaries.
4. **Content Fetch**: Retrieve the full text from `node_contents` only for the required nodes.
5. **Synthesis**: Feed the LLM a prompt containing:
   - Found Entities & Relations
   - Tree Context (e.g., "This was mentioned in Chapter 3: Financials")
   - Raw Text Chunks

## Output Expectations

When this skill is triggered, prefer producing:

1. PostgreSQL DDL or migration SQL
2. Tree-flattening ingestion code
3. Graph anchoring logic tied to `node_id`
4. Retrieval SQL that starts from graph hits and resolves back to tree context
5. Clear explanation of why this database design is preferable to storing one giant nested JSON blob

## Developer Guidelines
- **Always enforce bone-meat separation**: Never store massive text chunks in the `nodes` or `entities` tables.
- **Always maintain multi-tenancy**: Ensure every query filters by `workspace`.
- When users ask to implement a retrieval function, write SQL queries that join `relationships` -> `nodes` -> `node_contents` to demonstrate the hybrid power.
- Do not build a full product scaffold inside the skill. Keep the focus on database design, ingestion, anchoring, and retrieval patterns.
- Do not rewrite PageIndex or LightRAG in full inside the skill. Reuse their existing pipelines and apply this skill at the integration seam.
