# SEO Data Models and Output Formats

## Topic List Output Format

```json
{
  "project": {
    "product": "Product Name",
    "target_audience": "Target Customer Segment",
    "generated_at": "ISO8601 Timestamp"
  },
  "topics": [
    {
      "keyword": "Core Keyword",
      "title": "Article Title (including keyword)",
      "angle": "Content Angle / Unique Selling Point",
      "search_intent": "informational|commercial|transactional",
      "competitor_gap": "Content points not covered by competitors",
      "target_url": "/category/article-slug/",
      "priority": "high|medium|low",
      "estimated_difficulty": "easy|medium|hard",
      "template_type": "tutorial|comparison|product|list|case-study"
    }
  ]
}
```

## Content Generation Input Template

```json
{
  "article": {
    "keyword": "Core Keyword",
    "title": "Article Title",
    "template": "tutorial|comparison|product|list|case-study",
    "word_count_target": 1500,
    "include_images": true,
    "include_toc": true,
    "include_faq": true
  }
}
```

## Competitor Analysis Input Template

```json
{
  "competitor_analysis": {
    "product": "Product Name",
    "target_audience": "Target Customer",
    "competitors_to_analyze": ["Competitor 1", "Competitor 2", "Competitor 3"],
    "analysis_depth": "basic|detailed",
    "output_format": "json|markdown|both"
  }
}
```