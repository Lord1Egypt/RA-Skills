> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Best Practices for Extract

> Learn how to optimize content extraction, choose the right approach, and configure parameters for better performance.

## Extract Parameters

### Query

Use query to rerank extracted content chunks based on relevance:

```python  theme={null}
await tavily_client.extract(
    urls=["https://example.com/article"],
    query="machine learning applications in healthcare"
)
```

**When to use query:**

* To extract only relevant portions of long documents
* When you need focused content instead of full page extraction
* For targeted information retrieval from specific URLs

> When `query` is provided, chunks are reranked based on relevance to the query.

### Chunks Per Source

Control the amount of content returned per URL to prevent context window explosion:

```python  theme={null}
await tavily_client.extract(
    urls=["https://example.com/article"],
    query="machine learning applications in healthcare",
    chunks_per_source=3
)
```

**Key benefits:**

* Returns only relevant content snippets (max 500 characters each) instead of full page content
* Prevents context window from exploding
* Chunks appear in `raw_content` as: `<chunk 1> [...] <chunk 2> [...] <chunk 3>`
* Must be between 1 and 5 chunks per source

> `chunks_per_source` is only available when `query` is provided.

**Example with multiple URLs:**

```python  theme={null}
await tavily_client.extract(
    urls=[
        "https://example.com/ml-healthcare",
        "https://example.com/ai-diagnostics",
        "https://example.com/medical-ai"
    ],
    query="AI diagnostic tools accuracy",
    chunks_per_source=2
)
```

This returns the 2 most relevant chunks from each URL, giving you focused, relevant content without overwhelming your context window.

## Extraction Approaches

### Search with include\_raw\_content

Enable include\_raw\_content=true in Search API calls to retrieve both search results and extracted content simultaneously.

```python  theme={null}
response = await tavily_client.search(
    query="AI healthcare applications",
    include_raw_content=True,
    max_results=5
)
```

**When to use:**

* Quick prototyping
* Simple queries where search results are likely relevant
* Single API call convenience

### Direct Extract API

Use the Extract API when you want control over which specific URLs to extract from.

```python  theme={null}
await tavily_client.extract(
    urls=["https://example.com/article1", "https://example.com/article2"],
    query="machine learning applications",
    chunks_per_source=3
)
```

**When to use:**

* You already have specific URLs to extract from
* You want to filter or curate URLs before extraction
* You need targeted extraction with query and chunks\_per\_source

**Key difference:** The main distinction is control, with Extract you choose exactly which URLs to extract from, while Search with `include_raw_content` extracts from all search results.

## Extract Depth

The `extract_depth` parameter controls extraction comprehensiveness:

| Depth             | Use case                                      |
| ----------------- | --------------------------------------------- |
| `basic` (default) | Simple text extraction, faster processing     |
| `advanced`        | Complex pages, tables, structured data, media |

### Using `extract_depth=advanced`

Best for content requiring detailed extraction:

```python  theme={null}
await tavily_client.extract(
    url="https://example.com/complex-page",
    extract_depth="advanced"
)
```

**When to use advanced:**

* Dynamic content or JavaScript-rendered pages
* Tables and structured information
* Embedded media and rich content
* Higher extraction success rates needed

<Note>
  `extract_depth=advanced` provides better accuracy but increases latency and
  cost. Use `basic` for simple content.
</Note>

## Advanced Filtering Strategies

Beyond query-based filtering, consider these approaches for curating URLs before extraction:

| Strategy     | When to use                                    |
| ------------ | ---------------------------------------------- |
| Re-ranking   | Use dedicated re-ranking models for precision  |
| LLM-based    | Let an LLM assess relevance before extraction  |
| Clustering   | Group similar documents, extract from clusters |
| Domain-based | Filter by trusted domains before extracting    |
| Score-based  | Filter search results by relevance score       |

### Example: Score-based filtering

```python  theme={null}
import asyncio
from tavily import AsyncTavilyClient

tavily_client = AsyncTavilyClient(api_key="tvly-YOUR_API_KEY")

async def filtered_extraction():
    # Search first
    response = await tavily_client.search(
        query="AI healthcare applications",
        search_depth="advanced",
        max_results=20
    )

    # Filter by relevance score (>0.5)
    relevant_urls = [
        result['url'] for result in response.get('results', [])
        if result.get('score', 0) > 0.5
    ]

    # Extract from filtered URLs with targeted query
    extracted_data = await tavily_client.extract(
        urls=relevant_urls,
        query="machine learning diagnostic tools",
        chunks_per_source=3,
        extract_depth="advanced"
    )

    return extracted_data

asyncio.run(filtered_extraction())
```

## Integration with Search

### Optimal workflow

* **Search** to discover relevant URLs
* **Filter** by relevance score, domain, or content snippet
* **Re-rank** if needed using specialized models
* **Extract** from top-ranked sources with query and chunks\_per\_source
* **Validate** extracted content quality
* **Process** for your RAG or AI application

### Example end-to-end pipeline

```python  theme={null}
async def content_pipeline(topic):
    # 1. Search with sub-queries
    queries = generate_subqueries(topic)
    responses = await asyncio.gather(
        *[tavily_client.search(**q) for q in queries]
    )

    # 2. Filter and aggregate
    urls = []
    for response in responses:
        urls.extend([
            r['url'] for r in response['results']
            if r['score'] > 0.5
        ])

    # 3. Deduplicate
    urls = list(set(urls))[:20]  # Top 20 unique URLs

    # 4. Extract with error handling
    extracted = await asyncio.gather(
        *(tavily_client.extract(url, extract_depth="advanced") for url in urls),
        return_exceptions=True
    )

    # 5. Filter successful extractions
    return [e for e in extracted if not isinstance(e, Exception)]
```

## Summary

1. **Use query and chunks\_per\_source** for targeted, focused extraction
2. **Choose Extract API** when you need control over which URLs to extract from
3. **Filter URLs** before extraction using scores, re-ranking, or domain trust
4. **Choose appropriate extract\_depth** based on content complexity
5. **Process URLs concurrently** with async operations for better performance
6. **Implement error handling** to manage failed extractions gracefully
7. **Validate extracted content** before downstream processing
8. **Optimize costs** by extracting only necessary content with chunks\_per\_source

> Start with query and chunks\_per\_source for targeted extraction. Filter URLs strategically, extract with appropriate depth, and handle errors gracefully for production-ready pipelines.
