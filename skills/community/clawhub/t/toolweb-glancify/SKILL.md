---
name: Glancify Proxy
description: A proxy service that wraps external web pages with Glancify, enabling interactive content visualization and keyword extraction.
---

# Overview

Glancify Proxy is a powerful proxy service designed to enhance web content visibility and interactivity by wrapping external pages with the Glancify framework. This tool bridges the gap between static web content and dynamic, interactive visualizations, making it ideal for developers, researchers, and content analysts who need to extract insights from web pages quickly.

The service provides multiple endpoints for content wrapping, keyword extraction, and topic-based information retrieval. With Glancify's JavaScript integration and API-driven architecture, users can transform any URL into an interactive, keyword-enhanced view. The platform supports both direct URL wrapping and structured data retrieval through topic-based queries.

Ideal users include web developers integrating content analysis tools, SEO specialists analyzing page keywords, data researchers extracting structured information from web sources, and organizations building content intelligence platforms.

# Usage

## Example: Wrapping a Web Page with Glancify

**Request:**
```json
GET /view?url=https://example.com/article
```

**Response:**
```json
{
  "status": "success",
  "wrapped_url": "https://api.toolweb.in/tools/glancify/view?url=https://example.com/article",
  "content": {
    "title": "Example Article",
    "glancify_enabled": true,
    "interactive": true,
    "message": "Page wrapped successfully with Glancify"
  }
}
```

## Example: Retrieving Keywords from API

**Request:**
```json
GET /api/keywords
```

**Response:**
```json
{
  "status": "success",
  "keywords": [
    "security",
    "api",
    "proxy",
    "content-analysis",
    "visualization"
  ],
  "count": 5
}
```

## Example: Fetching Topic Data

**Request:**
```json
GET /api/topics/cybersecurity
```

**Response:**
```json
{
  "topic_id": "cybersecurity",
  "title": "Cybersecurity",
  "description": "Topics related to security, threats, and protection",
  "related_keywords": [
    "threat-analysis",
    "vulnerability-assessment",
    "security-audits"
  ]
}
```

# Endpoints

## GET /
**Summary:** Home

**Description:** Returns service information and status.

**Parameters:** None

**Response:**
- **200 OK** – Service is running and ready to accept requests

---

## GET /view
**Summary:** View Wrapped

**Description:** Proxy endpoint that wraps an external web page with Glancify, enabling interactive content visualization and analysis.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string | Yes | The full URL of the external webpage to wrap with Glancify |

**Response:**
- **200 OK** – Successfully wrapped the page; returns wrapped content with Glancify integration
- **422 Unprocessable Entity** – Invalid or missing URL parameter

---

## GET /demo
**Summary:** Demo

**Description:** Returns a demonstration of Glancify proxy functionality with sample data.

**Parameters:** None

**Response:**
- **200 OK** – Demo content and example wrapped pages

---

## GET /tsrg
**Summary:** Tsrg

**Description:** Retrieves TSRG (Topic-Source-Relationship Graph) data for content analysis.

**Parameters:** None

**Response:**
- **200 OK** – TSRG data structure with topic relationships and mappings

---

## GET /glancify.js
**Summary:** Glancify Js

**Description:** Serves the Glancify JavaScript library required for interactive page wrapping and visualization.

**Parameters:** None

**Response:**
- **200 OK** – JavaScript library file for Glancify integration

---

## GET /api/keywords
**Summary:** Api Keywords

**Description:** Retrieves a comprehensive list of supported keywords used for content tagging and analysis.

**Parameters:** None

**Response:**
- **200 OK** – Array of available keywords with metadata

---

## GET /api/topics/{topic_id}
**Summary:** Api Topic

**Description:** Fetches detailed information about a specific topic, including related keywords and metadata.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic_id` | string | Yes | Unique identifier for the topic (e.g., 'cybersecurity', 'api-security') |

**Response:**
- **200 OK** – Topic data including description, related keywords, and references
- **422 Unprocessable Entity** – Invalid or missing topic_id parameter

# Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

# About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

# References

- **Kong Route:** https://api.toolweb.in/tools/glancify
- **API Docs:** https://api.toolweb.in:8167/docs
