---
name: baidu-scholar-search
description: Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations.
homepage: https://xueshu.baidu.com/
metadata: { "openclaw": { "emoji": "🔬", "requires": { "bins": ["curl"] }, "requires_env": ["SKILLBOSS_API_KEY"] } }
---

> 📖 **Complete setup guide**: https://skillboss.co/skill.md


# Academic Scholar Search

Based on the keywords entered by the user, search for both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations

## Setup

1.  **API Key:** Ensure the SKILLBOSS_API_KEY environment variable is set with your valid SkillBoss API Hub key.
2.  **Environment:** The API key should be available in the runtime environment.

## API table
|     name    |               path              |            description                |
|-------------|---------------------------------|---------------------------------------|
|scholar_search|https://api.skillboss.co/v1/pilot|Based on the keywords entered, search for both Chinese and English literature via SkillBoss API Hub |


## Workflow

1. The script makes a POST request to the SkillBoss API Hub `/v1/pilot` endpoint with `type: "search"`
2. The API returns structured search results about a list of literature

## Scholar Search API

### Parameters

- `wd`: The search keywords (required, e.g. 'machine learning')
- `pageNum`: page num (default: 0)
- `enable_abstract`: whether to enable abstract (default: false)

### Example Usage
```bash
curl -s -X POST 'https://api.skillboss.co/v1/pilot' \
-H 'Authorization: Bearer $SKILLBOSS_API_KEY' \
-H 'Content-Type: application/json' \
-d '{"type": "search", "inputs": {"query": "人工智能"}, "prefer": "balanced"}'
```

## EXEC scripts
```bash
#!/bin/bash

# Academic Scholar Search Skill Implementation
# Powered by SkillBoss API Hub

set -e

# Check if required environment variable is set
if [ -z "$SKILLBOSS_API_KEY" ]; then
    echo '{"error": "SKILLBOSS_API_KEY environment variable not set"}'
    exit 1
fi

WD="$1"
if [ -z "$WD" ]; then
    echo '{"error": "Missing wd parameter"}'
    exit 1
fi

pageNum="${2:-0}"
enable_abstract="${3:-false}"

curl -s -X POST \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"search\", \"inputs\": {\"query\": \"$WD\"}, \"prefer\": \"balanced\"}" \
  "https://api.skillboss.co/v1/pilot"
# Response path: .result.results
```
