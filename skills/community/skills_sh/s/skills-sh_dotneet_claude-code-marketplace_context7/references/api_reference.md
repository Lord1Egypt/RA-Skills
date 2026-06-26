# Context7 API Reference

## Overview

Context7 is a service that provides LLMs with the latest library documentation. It solves the problem of outdated training data and non-existent APIs (hallucinations).

## API Endpoints

### Base URL
```
https://context7.com/api/v2
```

### Authentication
```
Authorization: Bearer CONTEXT7_API_KEY
```

The API key starts with the `ctx7sk-` prefix.

---

## 1. Library Search API

### Endpoint
```
GET /libs/search
```

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| libraryName | string | Yes | Library name to search (e.g., "react", "next.js") |
| query | string | No | Additional context query |

### Response
```json
{
  "libraries": [
    {
      "id": "/facebook/react",
      "name": "React",
      "description": "A JavaScript library for building user interfaces",
      "totalSnippets": 1250,
      "trustScore": 9.5,
      "benchmarkScore": 95,
      "versions": ["18.2.0", "18.3.0", "19.0.0"]
    }
  ]
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| id | string | Context7 library ID (`/org/project` format) |
| name | string | Library display name |
| description | string | Library description |
| totalSnippets | number | Number of available documentation snippets |
| trustScore | number | Trust score (0-10) |
| benchmarkScore | number | Benchmark score (0-100) |
| versions | string[] | List of available versions |

### Example
```bash
curl "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
  -H "Authorization: Bearer ctx7sk-xxx"
```

---

## 2. Documentation Retrieval API

### Endpoint
```
GET /context
```

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| libraryId | string | Yes | Context7 library ID (e.g., "/facebook/react") |
| query | string | Yes | Search query (e.g., "useEffect cleanup") |
| page | number | No | Page number (1-10, default: 1) |

### Response
```json
{
  "documentation": [
    {
      "title": "useEffect Hook",
      "content": "# useEffect\n\nThe `useEffect` Hook lets you synchronize a component with an external system...",
      "source": "https://react.dev/reference/react/useEffect"
    }
  ]
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| title | string | Documentation title |
| content | string | Documentation content in Markdown format |
| source | string | Original documentation source URL |

### Example
```bash
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useEffect" \
  -H "Authorization: Bearer ctx7sk-xxx"
```

---

## Rate Limits

| Tier | Requests/min |
|------|--------------|
| No API Key | 10 |
| Free | 100 |
| Pro | 1000 |
| Enterprise | Custom |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 404 | Not Found - Library not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## Best Practices

1. **Always resolve library ID before use**: Don't guess library IDs directly; first obtain the accurate ID through the search API
2. **Use specific queries**: Specific queries like "useEffect cleanup function" are more effective than "hooks"
3. **Error handling**: When receiving 404, try searching with a different library name
