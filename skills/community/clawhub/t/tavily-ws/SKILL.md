---
name: tavily
description: Connect agents to the web using Tavily APIs and SDKs. Use for executing search, scraping URLs, semantic crawls, mapping sites, and asynchronous deep research workflows.
metadata:
  author: Simon-Pierre Boucher
---

# Tavily Skill

This skill extends Manus's capabilities by providing highly specialized workflows, reference guides, and helper scripts to integrate Tavily's search, extraction, and research APIs. It is designed to be highly token-efficient, leveraging progressive disclosure.

## Quick Navigation

- **Core Search & RAG Workflow:** See [workflows.md](references/workflows.md) for step-by-step sequential patterns.
- **API Reference & Specifications:** See [api_reference.md](references/api_reference.md) for endpoint details, parameter ranges, and JSON schemas.
- **Troubleshooting & Diagnostics:** See [troubleshooting.md](references/troubleshooting.md) for diagnostic checklists and error handling strategies.

## Basic Principles

### 1. Match Search Depth to Query Complexity
- Use `basic` (1 credit) for simple queries (e.g., factual lookups, company names).
- Use `advanced` (2 credits) for complex research questions requiring multi-query expansion and synthesis.
- Use `fast` or `ultra-fast` (1 credit) for latency-critical applications (e.g., real-time chat, voice assistants).

### 2. Prefer Extract over Raw Search for RAG
- Avoid downloading full HTML or uncleaned pages.
- Use the **Extract API** with `query` to trigger **Intent-Based Extraction**.
- Limit the chunks returned per source using `chunks_per_source` (range: 1 to 5) to save downstream LLM context window tokens.

### 3. Handle Rate Limits Gracefully
- Development keys are capped at **100 RPM**. Production keys are capped at **1,000 RPM**.
- Always wrap Tavily API calls in a retry wrapper that parses the `retry-after` header during `429 Too Many Requests` responses.

---

## Code Boilerplate

### Synchronous Python Search
```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = client.search(
    query="quantum computing trends 2026",
    search_depth="advanced",
    max_results=5
)
```

### Asynchronous Python Extract
```python
import asyncio
from tavily import AsyncTavilyClient

async def extract_links():
    client = AsyncTavilyClient(api_key="tvly-YOUR_API_KEY")
    response = await client.extract(
        urls=["https://example.com/ai-agents"],
        query="agent orchestration",
        chunks_per_source=3
    )
    return response
```
