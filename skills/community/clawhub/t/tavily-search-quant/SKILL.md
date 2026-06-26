---
name: tavily-search
description: Tavily AI search API integration for OpenClaw. Provides web search functionality with AI-powered summarization optimized for RAG and question answering. Use when you need web search and the default web_search tool is not configured or you prefer Tavily's search results.
---

# Tavily Search

Tavily Search is a specialized AI search API designed for LLMs and RAG applications. It provides:
- Real-time web search with AI-summarized results
- Built-in content extraction
- Date range filtering
- Domain filtering
- Free tier: 1000 searches/month

## Configuration

Before using, you need to configure your Tavily API key:

1. Get your API key from https://tavily.com/
2. Set it in your environment: `export TAVILY_API_KEY=your_api_key_here`
3. Or add it to OpenClaw config at `tools.tavily.apiKey`

## Core Capabilities

### 1. Basic Search (`tavily_search`)
Search the web with optional depth control and topic filtering.

**Parameters:**
- `query` (required): Search query string
- `max_results` (optional, default 5): Number of results (1-10)
- `search_depth` (optional): `basic` or `deep` (default `basic`)
- `topic` (optional): `general` or `news` (default `general`)
- `days` (optional): Time range in days back from current date

### 2. Search with Date Range (`tavily_search_date_range`)
Search with specific start and end dates.

**Parameters:**
- `query` (required): Search query string
- `start_date` (required): YYYY-MM-DD
- `end_date` (required): YYYY-MM-DD
- `max_results` (optional, default 5)
- `search_depth` (optional): `basic` or `deep`

### 3. Q&A Search (`tavily_answer`)
Get a direct AI answer to your question with citations.

**Parameters:**
- `query` (required): Question to answer
- `max_results` (optional, default 5)
- `search_depth` (optional): `basic` or `deep`

### 4. Extract Content (`tavily_extract`)
Extract clean, readable content from one or more URLs.

**Parameters:**
- `urls` (required): Array of URLs to extract

## Usage Example

```python
# Search for recent news about OpenClaw
python scripts/tavily_search.py "openclaw github" --days 1 --max_results 5
```

## Output Format

All search commands return JSON with:
- `results`: Array of search results with title, content, url, score
- `answer`: AI-generated answer (for answer mode)
- `response_time`: Query response time

## scripts/

| Script | Purpose |
|--------|---------|
| `tavily_cli.py` | Main CLI interface for all Tavily search operations |
| `tavily_api.py` | Python API client module |

## references/

| File | Purpose |
|------|---------|
| `api_docs.md` | Tavily API documentation reference |

