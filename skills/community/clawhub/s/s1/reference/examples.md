# Search1API CLI – Usage Examples

> Read this file when you need more examples beyond the basics in SKILL.md.

## 1. Quick web search

```bash
s1 search "Claude Code skills best practices" -n 5
```

## 2. Non-English search

When the query is Chinese, use Baidu for better results:

```bash
s1 search "大语言模型最新进展" -n 10 -s baidu -t month
```

## 3. Domain-scoped search

Restrict results to specific sites:

```bash
s1 search "transformer architecture" -n 5 --include arxiv.org openai.com
```

Exclude specific sites:

```bash
s1 search "JavaScript framework" -n 10 --exclude medium.com
```

## 4. Breaking news

```bash
s1 news "AI regulation" -n 10 -t day
```

## 5. Trending → news deep dive

Step 1 – discover trending:
```bash
s1 trending hackernews -n 10
```

Step 2 – search for details:
```bash
s1 search "interesting topic from step 1" -n 5 -t day
```

Step 3 – crawl the most relevant result:
```bash
s1 crawl https://example.com/full-article
```

## 6. URL summarization

User shares a link:
```bash
s1 crawl https://example.com/blog-post
```
Then summarize the returned content for the user.

## 7. Sitemap discovery

```bash
s1 sitemap https://docs.example.com
```

## 8. Deep research workflow

Step 1 – broad search:
```bash
s1 search "zero-knowledge proofs applications" -n 15 -t year
```

Step 2 – crawl top results:
```bash
s1 crawl https://result1.com/article
s1 crawl https://result2.com/article
s1 crawl https://result3.com/article
```

Step 3 – check for recent news:
```bash
s1 news "zero-knowledge proofs" -n 5 -t day
```

Step 4 – synthesize all gathered content into a report.

## 9. Platform-specific search

```bash
s1 search "MCP server best practices" -s github -n 10
s1 search "AI agent framework" -s reddit -n 10
s1 search "attention mechanism explained" -s arxiv -n 10
s1 search "LLM tutorial" -s youtube -n 5
```

## 10. Deep reasoning

```bash
s1 reasoning "Analyze the pros and cons of microservices vs monolith for a startup"
```

## 11. Check remaining credits

```bash
s1 balance
```

## 12. JSON output for scripting

Any command supports `--json` for raw output:

```bash
s1 search "test" --json
s1 balance --json
```
