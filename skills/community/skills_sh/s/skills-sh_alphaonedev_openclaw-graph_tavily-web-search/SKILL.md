---
name: tavily-web-search
cluster: community
description: "Tavily: web search optimized for AI agents, answer synthesis, domain filtering, depth control"
tags: ["search","tavily","ai","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "tavily web search ai agent answer synthesis domain filter"
---

# tavily-web-search

## Purpose
This skill enables AI agents to perform web searches using Tavily, a service optimized for AI workflows. It synthesizes answers from search results, applies domain filters, and controls search depth to deliver relevant, concise information without overwhelming the agent.

## When to Use
Use this skill when you need real-time web data, such as fetching current news, verifying facts, or gathering research. Apply it in scenarios where standard search engines are too verbose, like synthesizing answers for user queries, filtering results to specific domains (e.g., .edu sites), or limiting depth for quick responses. Avoid it for internal data access or when offline sources suffice.

## Key Capabilities
- **Answer Synthesis**: Automatically summarizes search results into a coherent response; specify via `search_depth` parameter (e.g., 0 for shallow, 5 for deep).
- **Domain Filtering**: Restrict searches to domains like "example.com" using the `include_domains` flag; example: `include_domains=["wikipedia.org"]`.
- **Depth Control**: Set search depth with `max_results` (1-10) to control result volume; higher values increase detail but raise costs.
- **Optimized for AI**: Integrates with AI agents via API, supporting tags like "search" and "ai" for metadata embedding.
- **Configurable Queries**: Supports query parameters for customization, such as `query` string and `api_key` for authentication.

## Usage Patterns
Always initialize with an API key via environment variable `$TAVILY_API_KEY`. For basic searches, construct a query object and call the API endpoint. Use in loops for iterative refinement, e.g., refine queries based on initial results. Pattern: Set up auth, build query with filters, execute search, then parse and synthesize the response. For agent workflows, integrate as a subtool in multi-step processes, ensuring error checks between calls.

## Common Commands/API
Tavily uses a REST API endpoint: `https://api.tavily.com/search`. Authentication requires setting `$TAVILY_API_KEY` in your environment.

Example CLI curl command:
```
curl -H "Content-Type: application/json" \
     -H "X-Api-Key: $TAVILY_API_KEY" \
     https://api.tavily.com/search -d '{"query": "latest AI news", "max_results": 3}'
```

Python code snippet for API call:
```
import requests
api_key = os.environ.get('TAVILY_API_KEY')
response = requests.post('https://api.tavily.com/search', headers={'X-Api-Key': api_key}, json={'query': 'climate change effects', 'include_domains': ['nytimes.com']})
results = response.json()['results']
```

Common flags/parameters:
- `query`: String, required; e.g., "OpenAI updates".
- `max_results`: Integer (1-10); controls depth, e.g., 5 for balanced results.
- `include_domains`: Array of strings; e.g., ["bbc.com", "cnn.com"] for news sites.
- `exclude_domains`: Array; e.g., ["socialmedia.com"] to avoid certain sites.

## Integration Notes
To integrate, first obtain a Tavily API key from their dashboard and set it as `$TAVILY_API_KEY`. In code, import necessary libraries (e.g., requests in Python) and handle the API response as JSON. For OpenClaw agents, add this skill to your toolset by referencing the ID "tavily-web-search" in your agent config, like: `tools: ["tavily-web-search"]`. Config format example in YAML:
```
tools:
  - id: tavily-web-search
    config:
      api_key_env: TAVILY_API_KEY
      default_params:
        max_results: 3
```
Ensure your agent checks for key availability before calling; if missing, prompt the user. Test integrations in a sandbox environment to verify response formats.

## Error Handling
Common errors include 401 (unauthorized) for invalid API keys, 429 (rate limit exceeded), and 400 (bad request for invalid parameters). To handle: Check response status code before parsing; if 401, log "API key error: Set $TAVILY_API_KEY" and retry after user input. For 429, implement exponential backoff (e.g., wait 5 seconds then retry). Validate inputs beforehand, e.g., ensure `query` is not empty. Example error check in code:
```
if response.status_code == 401:
    raise ValueError("Authentication failed; ensure $TAVILY_API_KEY is set")
elif response.status_code >= 400:
    print(f"Error: {response.json().get('error')}")
```

## Concrete Usage Examples
1. **Fact Verification**: To verify recent events, use: Set query to "2023 election results" with `include_domains=["reuters.com"]` and `max_results=2`. Then, synthesize the response to extract key facts, e.g., in code: `synthesized_answer = summarize_results(results)`.
2. **Research Assistance**: For gathering AI trends, construct a query like "advancements in LLMs" with `search_depth=3`. Parse results to filter for dates or sources, then use in an agent response: "Based on Tavily search, key trends include...".

## Graph Relationships
- Related to: search tools (e.g., via "search" tag)
- Connected via: community cluster (shares nodes with other community tools)
- Links to: AI agents (through "ai" tag for embedding)
- Dependencies: Requires external API (Tavily), no direct graph edges to other skills unless configured.
