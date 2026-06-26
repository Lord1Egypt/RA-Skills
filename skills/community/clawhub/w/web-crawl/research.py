#!/usr/bin/env python3
"""
Deep Research Tool - Multi-step research with search + crawl

This tool combines Brave search with advanced crawling for comprehensive research.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

# Import the crawler
from web_crawl import WebCrawler, parallel_crawl


async def brave_search(query: str, count: int = 8) -> List[Dict[str, str]]:
    """
    Perform Brave search using OpenClaw's web_search tool
    
    Returns list of results with title, url, snippet
    """
    # This is a wrapper that will be called via OpenClaw's tool system
    # For now, return mock structure
    return []


async def research_topic(
    query: str,
    max_sources: int = 5,
    extract_mode: str = "markdown",
    max_content_length: int = 8000,
) -> str:
    """
    Perform deep research on a topic
    
    Workflow:
    1. Search for relevant URLs
    2. Crawl top results in parallel
    3. Synthesize findings
    
    Args:
        query: Research topic/question
        max_sources: Maximum number of sources to analyze
        extract_mode: Content extraction mode
        max_content_length: Max content length per source
    
    Returns:
        Comprehensive research report
    """
    # Step 1: Search (will be done via OpenClaw's web_search tool)
    # For now, we return instructions on how to use this
    
    instructions = f"""# Deep Research Instructions

To perform deep research on "{query}", follow these steps:

## Step 1: Search
Use OpenClaw's web_search tool to find relevant sources:
```
web_search:0 {{
  "query": "{query}",
  "count": {max_sources + 3}
}}
```

## Step 2: Crawl Sources
Use the parallel_crawl function on the top {max_sources} URLs:
```python
parallel_crawl(urls=[url1, url2, ...], mode="{extract_mode}", max_length={max_content_length})
```

## Step 3: Synthesize
Analyze the crawled content and provide:
- Key findings summary
- Important quotes/data points
- Source citations
- Any contradictions or gaps

---

**Tip**: For academic research, use mode="structured" to get metadata.
For content creation, use mode="markdown" for clean text.
"""
    
    return instructions


async def analyze_website(
    url: str,
    depth: int = 1,
    max_pages: int = 10,
) -> str:
    """
    Comprehensive website analysis
    
    Analyzes a website's structure, content, and linked pages
    """
    crawler = WebCrawler()
    
    # First, get the main page and extract links
    result = await crawler.crawl(url, mode="structured", max_length=50000)
    
    if not result["success"]:
        return f"❌ Failed to analyze {url}: {result.get('error')}"
    
    # Parse structured data to get links
    try:
        data = json.loads(result["content"])
        links_count = data.get("links_count", 0)
        title = data.get("title", "")
    except:
        links_count = 0
        title = ""
    
    report = f"""# Website Analysis: {url}

## Overview
- **Title**: {title}
- **Total Links**: {links_count}

## Main Page Content
{result["content"][:3000]}

---

**Note**: For deeper analysis (following linked pages), use parallel_crawl on specific URLs.
"""
    
    return report


# Research planning templates
RESEARCH_TEMPLATES = {
    "product": {
        "description": "Research a product or service",
        "search_queries": [
            "{topic} review",
            "{topic} features",
            "{topic} pricing",
            "{topic} vs competitors",
        ],
    },
    "company": {
        "description": "Research a company or organization",
        "search_queries": [
            "{topic} company profile",
            "{topic} funding",
            "{topic} leadership",
            "{topic} news",
        ],
    },
    "technology": {
        "description": "Research a technology or framework",
        "search_queries": [
            "{topic} documentation",
            "{topic} tutorial",
            "{topic} github",
            "{topic} best practices",
        ],
    },
    "person": {
        "description": "Research a person",
        "search_queries": [
            "{topic} biography",
            "{topic} achievements",
            "{topic} interviews",
        ],
    },
    "topic": {
        "description": "General topic research",
        "search_queries": [
            "{topic} guide",
            "{topic} explained",
            "{topic} latest developments",
        ],
    },
}


def get_research_plan(topic: str, research_type: str = "topic") -> str:
    """
    Generate a research plan for a given topic
    
    Args:
        topic: Research topic
        research_type: Type of research (product, company, technology, person, topic)
    
    Returns:
        Research plan with suggested search queries
    """
    template = RESEARCH_TEMPLATES.get(research_type, RESEARCH_TEMPLATES["topic"])
    
    queries = [q.format(topic=topic) for q in template["search_queries"]]
    
    plan = f"""# Research Plan: {topic}

**Type**: {template['description']}

## Suggested Search Queries
"""
    for i, query in enumerate(queries, 1):
        plan += f"{i}. `{query}`\n"
    
    plan += f"""
## Execution Steps

1. **Search Phase**: Run each query, collect top 3-5 URLs per query
2. **Crawl Phase**: Use `parallel_crawl` to extract content from all URLs
3. **Analysis Phase**: Synthesize findings, identify key insights
4. **Verification Phase**: Cross-reference important claims across sources

## Extraction Mode Recommendations
- **For data/numbers**: Use `structured` mode
- **For content/ideas**: Use `markdown` mode  
- **For link discovery**: Use `links` mode

---

Ready to start research? Run the search queries above!
"""
    
    return plan


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python research.py <command> [args]")
        print("Commands:")
        print("  plan <topic> [type]  - Generate research plan")
        print("  crawl <url> [mode]   - Crawl single URL")
        print("  analyze <url>        - Analyze website")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "plan":
        topic = sys.argv[2]
        rtype = sys.argv[3] if len(sys.argv) > 3 else "topic"
        print(get_research_plan(topic, rtype))
        
    elif command == "crawl":
        url = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "markdown"
        result = asyncio.run(crawl_url(url, mode))
        print(result)
        
    elif command == "analyze":
        url = sys.argv[2]
        result = asyncio.run(analyze_website(url))
        print(result)
