---
name: execute-openclaw-pipeline
description: Autonomous AEO and SEO content generation and optimization engine for scaling business operations. Use when Codex needs to run end-to-end programmatic SEO workflows, including semantic keyword generation, multi-tiered competitor scraping, dynamic JSON-LD schema generation, and direct WordPress publishing. Also use this skill to trigger the analytics worker for detecting and repairing CTR decay on existing posts.
---

# OpenClaw Pipeline Execution

## Initial Setup and Configuration
Before running the pipeline, ensure the environment is correctly configured:
1. Verify `.env` contains necessary credentials (WP_URL, LLM provider keys, Scraper keys).
2. Run `scripts/setup.py` to initialize the SQLite database (`openclaw.db`) and ChromaDB vector storage.

## Executing the Daily Worker (Content Generation)
To generate and publish new content for scaling operations:
1. Execute `scripts/daily_worker.py`.
2. The pipeline handles:
   - Semantic query generation based on `TARGET_NICHE`.
   - Competitor scraping via the waterfall method (Playwright, Firecrawl, Jina).
   - Content generation using the designated LLM.
   - Semantic internal link injection.
   - Direct publication to WordPress.

## Executing the Analytics Worker (Content Optimization)
To optimize existing content experiencing CTR decay:
1. Execute `scripts/analytics_worker.py`.
2. The worker evaluates Google Search Console data against established age gates.
3. Eligible posts are updated via the WordPress REST API, and ChromaDB vector embeddings are re-synced.

## Critical Architectural Constraints
- **Concurrency:** ChromaDB writes are serialized via `filelock`. Do not attempt to write to ChromaDB concurrently without acquiring `get_chroma_lock()` from `setup.py`.
- **Scraping Fallbacks:** If Tier 1-5 scrapers fail, the pipeline falls back gracefully to LLM grounded search synthesis (Tier 6). Do not halt execution if competitor scraping fails.
- **Schema Generation:** JSON-LD schema is dynamically constructed via `schema_engine.py` based on the parsed Pydantic content outline.