# Operations and Maintenance Reference

This reference covers operational surfaces and maintenance workflows for the crypto-news-analyzer HTTP API.

## Health Endpoint

The service exposes a health check endpoint for load balancers and monitoring systems.

- **Endpoint:** `GET /health`
- **Response:** `{"status": "healthy", "initialized": true/false}`
- **Use case:** Load balancer health checks, deployment verification, uptime monitoring

The `initialized` field indicates whether the underlying controller has completed startup initialization. A value of `false` may indicate the service is still starting or encountered an error during initialization.

## Telegram Webhook

The Telegram webhook is a maintainer-only integration surface for receiving Telegram Bot updates via webhook delivery.

### Webhook Route

- **Endpoint:** `POST` to the path configured in `TELEGRAM_WEBHOOK_PATH` environment variable
- **Default path:** `/telegram/webhook`
- **Purpose:** Integration point for Telegram Bot API webhook delivery, not the primary user path

### Authentication Header

Webhook requests must include a secret token header for validation:

- **Header:** `X-Telegram-Bot-Api-Secret-Token`
- **Behavior:** The handler validates the token against the configured secret; mismatches return HTTP 403
- **Error responses:**
  - `403 Forbidden` - Invalid or missing secret token
  - `503 Service Unavailable` - Runtime processing error (e.g., handler not ready)

### Operational Notes

- Operators and end users should prefer the HTTP API routes and Telegram slash commands instead of interacting directly with the webhook endpoint
- The webhook is intended for infrastructure integration and bot delivery, not for manual invocation
- Configure the webhook path via environment variable to match your deployment routing needs

## Self-Update Workflow

When updating this skill reference to match code changes, follow this workflow to ensure accuracy.

### Canonical Source Files

These files contain the ground truth for HTTP behavior:

1. **`crypto_news_analyzer/api_server.py`** - FastAPI route definitions, health endpoint, and webhook handler
2. **`tests/news/test_api_server.py`** - Contract tests for endpoints, including webhook secret validation
3. **`docs/AI_ANALYZE_API_GUIDE.md`** - Production verification notes and API usage guidance

### Verification Commands

Before merge, run the full planned verification suite to verify the skill docs, the backing API contract, and the legacy-reference guardrails stay aligned:

```bash
uv run pytest tests/shared/test_openclaw_skill_smart_news.py -v
uv run pytest tests/news/test_api_server.py -k "health or analyze or datasource or webhook" -v
uv run pytest tests/shared/test_banned_legacy_reference_scan.py -v
uv run python tests/helpers/banned_legacy_reference_scan.py
```

Do not merge until all four commands pass.

### Release Command

Publish a new ClawHub version from the repo root with:

```bash
skills/publish_clawhub_skill.sh smart-news 0.3.0 "Describe the release briefly."
```

Use a semver version string. The script checks `clawhub` login state and runs the skill-specific test file before publishing unless `CLAWHUB_SKIP_TESTS=1` is set.

### Update Steps

1. Read the canonical source files to identify behavioral changes
2. Update the relevant sections in this reference
3. Run the full verification suite above before merge
4. Address any failures before committing or merging

### Source Precedence

When documentation sources conflict, trust code and tests over prose. The live implementation in `api_server.py` and its test coverage in `tests/news/test_api_server.py` are the authoritative references.
