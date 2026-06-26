---
name: web-crawl
version: "1.0.0"
description: Advanced web crawling and content extraction tool with multiple extraction modes
activation:
  keywords: ["crawl", "抓取", "提取网页", "研究", "深度研究", "research", "analyze website"]
  tags: ["web", "research", "crawling"]
---

# Web Crawl Skill

Advanced web content extraction with multiple modes and intelligent content detection.

## When to Use

Use this skill when:
- User asks to "研究" / "深度研究" a topic
- User wants to "抓取" / "提取" content from websites
- Need to analyze multiple web pages systematically
- Current `web_fetch` output is insufficient

## Extraction Modes

| Mode | Use Case |
|------|----------|
| `text` | Clean plain text |
| `markdown` | Formatted Markdown (recommended) |
| `links` | Extract all links |
| `structured` | JSON metadata + content |
| `full` | Markdown + links combined |

## Tools Available

- `web_crawl` - Extract content from a single URL
- `parallel_crawl` - Extract from multiple URLs in parallel
- `research_topic` - Multi-step research with search + crawl

## Example Usage

```
User: "研究一下 OpenManus-Max 项目"
→ Use research_topic tool with query="OpenManus-Max GitHub features"
```
