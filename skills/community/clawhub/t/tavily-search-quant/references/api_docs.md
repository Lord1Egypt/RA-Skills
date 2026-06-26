# Tavily API Documentation Reference

## Base URL
`https://api.tavily.com`

## Authentication
All requests require an `api_key` parameter obtained from https://tavily.com/

## Endpoints

### POST /search
Main search endpoint.

**Request Body:**
```json
{
  "api_key": "string",
  "query": "string",
  "max_results": number (1-10, default 5),
  "search_depth": "basic" | "deep" (default "basic"),
  "topic": "general" | "news" (default "general"),
  "days": number (optional, time range in days),
  "start_date": "YYYY-MM-DD" (optional),
  "end_date": "YYYY-MM-DD" (optional),
  "include_answer": boolean (default false),
  "include_raw_content": boolean (default false),
  "include_images": boolean (default false),
  "domain": string[] (optional, include only),
  "exclude_domains": string[] (optional, exclude)
}
```

**Response:**
```json
{
  "query": "string",
  "answer": "string" (optional, if include_answer=true),
  "response_time": number (seconds),
  "results": [
    {
      "title": "string",
      "url": "string",
      "content": "string",
      "score": number (0-1 relevance),
      "raw_content": "string" (optional)
    }
  ],
  "images": string[] (optional, if include_images=true)
}
```

### POST /extract
Extract content from URLs.

**Request Body:**
```json
{
  "api_key": "string",
  "urls": string[],
  "include_images": boolean (default false)
}
```

**Response:**
```json
{
  "results": [
    {
      "url": "string",
      "raw_content": "string",
      "images": string[] (optional)
    }
  ],
  "failed_results": [
    {
      "url": "string",
      "error": "string"
    }
  ]
}
```

## Rate Limits & Pricing

- Free tier: 1000 searches/month
- Paid tiers: More requests available
- See https://tavily.com/pricing for current pricing

## Usage Tips

1. For recent news, use `topic: "news"`
2. `search_depth: "deep"` gives better quality but is slower
3. For daily summaries, the `days` parameter is convenient
4. The `content` field already contains a clean summary, no need to extract again most of the time
