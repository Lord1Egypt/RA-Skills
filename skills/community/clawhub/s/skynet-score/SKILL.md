---
name: skynet-score
description: Use for searching CertiK Skynet project scores, looking up blockchain project security ratings, comparing score breakdowns, and integrating the public Skynet project search endpoint. Trigger when the user asks for a project score, tier, score factors, updated time, or how to query Skynet scores by keyword.
license: MIT
compatibility: Compatible with Cursor/Codex Agent Skills, Claude Agent Skills runtimes (Claude Code/claude.ai/API), and OpenClaw Skills. Requires Python >=3.9, outbound HTTPS access to open.api.certik.com, and permission to execute `{skillDir}/scripts/skynet_score.py`.
metadata:
  url: https://open.api.certik.com/projects
  script: <skillDir>/scripts/skynet_score.py
  primary-commands: search
---

# Skynet Score

Use `{skillDir}/scripts/skynet_score.py` to inspect project score search results with the CertiK public project API.

Use this skill when the user wants to look up a blockchain project's CertiK Skynet score or needs help integrating the public project score API.

## When to use this skill

- Search projects by keyword or approximate project name
- Return a project's overall score, tier, and last update time
- Explain the score breakdown fields
- Show how to query the public endpoint from code or `curl`

## Workflow

1. Extract the project keyword from the user request.
2. Prefer the bundled Python script for execution.
3. If Python is unavailable, use the documented `curl` fallback.
4. If multiple projects match, list the best candidates instead of guessing.
5. When a clear match exists, summarize:
   - project name
   - overall Skynet score
   - tier
   - last updated time
   - score breakdown fields that matter to the user's question
6. If the user asks for implementation details, provide a minimal request example and note rate limits.

## Execution

Prefer Python first:

```bash
python3 scripts/skynet_score.py --keyword "uniswap"
```

If Python is unavailable, use `curl`:

```bash
curl -sG "https://open.api.certik.com/projects" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "keyword=uniswap"
```

## Output guidance

- Do not invent a score when no project match is returned.
- If there are several close matches, ask the user to confirm which project they mean.
- When explaining the result, keep the overall score first and the component scores second.
- If the user asks for raw payloads or integration help, include the response shape below.

## Public API

- Base URL: `https://open.api.certik.com`
- Endpoint: `GET /projects`
- Query parameter: `keyword` (required)

Example:

```bash
curl -sG "https://open.api.certik.com/projects" \
  -H "Accept: application/json, text/plain, */*" \
  --data-urlencode "keyword=uniswap"
```

Important score fields:

- `score`: overall Skynet score
- `scoreCodeSecurity`: code security score
- `scoreCommunity`: community score
- `scoreFundamental`: fundamentals score
- `scoreGovernance`: governance score
- `scoreMarket`: market score
- `scoreOperation`: operations score
- `tier`: score tier
- `updatedAt`: last update time

## Limits and errors

- Rate limit: 50 requests per 60-second window per IP
- Headers:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
  - `Retry-After` on `429`

Error payload:

```json
{
  "error": "Human-readable error message"
}
```

Common status codes:

- `400`: missing or invalid parameters
- `429`: rate limit exceeded
- `500`: server-side failure
