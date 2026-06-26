# Core Search & Extraction Workflows

This document details the standard, production-grade workflows for executing web search, semantic extraction, and RAG pipelines using Tavily.

---

## 1. Production-Grade RAG Pipeline

For mission-critical RAG applications, do not simply run a search and feed raw snippets to your model. Implement the **Retrieve, Filter, Rerank, and Synthesize** pattern:

```
[User Query]
     │
     ▼
Step 1: Execute Advanced Search ──> (POST /search {search_depth: "advanced"})
     │
     ▼
Step 2: Score-Based Filtering ───> (Discard results with score <= 0.65)
     │
     ▼
Step 3: Intent-Based Extract ────> (POST /extract {urls, query, chunks_per_source})
     │
     ▼
Step 4: Context Aggregation ─────> (Format Markdown chunks with source citations)
     │
     ▼
Step 5: LLM Synthesis ───────────> (Generate fact-grounded response)
```

---

## 2. Dynamic Crawl & Extraction Workflow

To scrape deep website content without consuming excessive credits, use a two-step map-then-crawl pattern:

1. **Map Discovery:** Map the site structure first using the Map API to identify URL topologies.
2. **Filter Paths:** Analyze the URL array using regular expressions to select target directories (e.g., `/docs/`, `/pricing/`).
3. **Targeted Crawl:** Execute the Crawl API passing `select_paths` to restrict the crawler's breadth and depth.

---

## 3. Asynchronous Research Polling Pattern

For long-running deep research tasks, use an asynchronous polling loop with backoff:

```python
import asyncio
from tavily import AsyncTavilyClient

async def poll_research(client: AsyncTavilyClient, request_id: str):
    while True:
        response = await client.get_research(request_id)
        status = response.get("status")
        
        if status == "complete":
            return response.get("content"), response.get("sources")
        elif status == "failed":
            raise Exception("Research task failed.")
            
        await asyncio.sleep(5)  # Poll every 5 seconds
```
