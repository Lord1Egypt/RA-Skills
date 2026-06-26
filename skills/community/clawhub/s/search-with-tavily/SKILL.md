---
name: tavily-search
description: Web search using Tavily API - a powerful search engine for AI agents. Use when you need to search the web for current information, news, research, or any topic that requires up-to-date web data. Supports multiple search modes including basic search, Q&A, and context retrieval for RAG applications.
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env:
        - TAVILY_API_KEY
---

# Tavily Search

Web search using Tavily API - optimized for AI agents and RAG applications.

## Quick Start

### Prerequisites

Set your Tavily API key:
```bash
export TAVILY_API_KEY="tvly-your-api-key"
```

Or use the Python client directly with API key.

### Basic Search

```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-your-api-key")
response = client.search("Latest AI developments")

for result in response['results']:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content'][:200]}...")
```

### Q&A Search (Get Direct Answers)

```python
answer = client.qna_search(query="Who won the 2024 US Presidential Election?")
print(answer)
```

### Context Search (For RAG Applications)

```python
context = client.get_search_context(
    query="Climate change effects on agriculture",
    max_tokens=4000
)
# Use context directly in LLM prompts
```

## Search Parameters

### Common Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `query` | string | Search query (required) | - |
| `search_depth` | string | "basic" or "comprehensive" | "basic" |
| `max_results` | int | Number of results (1-20) | 5 |
| `include_answer` | bool | Include AI-generated answer | False |
| `include_raw_content` | bool | Include full page content | False |
| `include_images` | bool | Include image URLs | False |

### Advanced Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | string | Search topic: "general" or "news" |
| `time_range` | string | Time filter: "day", "week", "month", "year" |
| `include_domains` | list | Restrict to specific domains |
| `exclude_domains` | list | Exclude specific domains |
| `exact_match` | bool | Require exact phrase matching |

## Response Format

### Standard Search Response

```json
{
  "query": "search query",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com/article",
      "content": "Snippet or full content...",
      "score": 0.95,
      "raw_content": "Full page content (if requested)..."
    }
  ],
  "answer": "AI-generated answer (if requested)",
  "images": ["image_url1", "image_url2"],
  "response_time": 1.23
}
```

## Error Handling

### Common Errors

```python
from tavily import TavilyClient
from tavily.exceptions import TavilyError, RateLimitError, InvalidAPIKeyError

client = TavilyClient(api_key="your-api-key")

try:
    response = client.search("query")
except InvalidAPIKeyError:
    print("Invalid API key. Check your TAVILY_API_KEY.")
except RateLimitError:
    print("Rate limit exceeded. Please wait before retrying.")
except TavilyError as e:
    print(f"Tavily error: {e}")
```

## Best Practices

### 1. Use Context Search for RAG

For retrieval-augmented generation, use `get_search_context()` instead of standard search:

```python
context = client.get_search_context(
    query=user_query,
    max_tokens=4000,  # Fit within your LLM's context window
    search_depth="comprehensive"
)

# Use in prompt
prompt = f"""Based on the following context:
{context}

Answer this question: {user_query}"""
```

### 2. Handle Rate Limits

Tavily has rate limits. Implement exponential backoff:

```python
import time
from tavily.exceptions import RateLimitError

def search_with_retry(client, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.search(query)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 3. Filter Results

Use domain filters to improve result quality:

```python
# Only search trusted news sources
response = client.search(
    query="breaking news",
    include_domains=["bbc.com", "reuters.com", "apnews.com"],
    time_range="day"  # Only recent news
)
```

### 4. Use Q&A Mode for Facts

For factual questions, use Q&A mode for direct answers:

```python
# Good for: "Who won the 2024 election?"
answer = client.qna_search("Who won the 2024 US Presidential Election?")

# Good for: "What is the capital of France?"
answer = client.qna_search("Capital of France")
```

## Additional Resources

- **Tavily Documentation**: https://docs.tavily.com
- **Python SDK**: https://github.com/tavily-ai/tavily-python
- **JavaScript SDK**: https://github.com/tavily-ai/tavily-js
- **API Reference**: https://docs.tavily.com/documentation/api-reference

## Skill Maintenance

This skill requires:
- `TAVILY_API_KEY` environment variable set
- `tavily-python` package installed (`pip install tavily-python`)

For issues or updates, refer to the Tavily documentation or GitHub repository.