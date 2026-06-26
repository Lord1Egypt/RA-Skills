---
name: tly-short-link-creator
description: Create T.LY short links through the T.LY API. Use when an agent needs to shorten a URL, generate a shareable T.LY link, return a `short_url`, or call T.LY programmatically. This skill requires a valid T.LY API key and should only be used when `TLY_API_TOKEN` is available or the user can provide one.
homepage: https://t.ly/
license: Proprietary. Internal use for T.LY agents
compatibility: Requires Python 3 and internet access to reach https://api.t.ly. Uses TLY_API_TOKEN.
---

# T.LY Short Link Creator

## Quick Start

1. Confirm a T.LY API key is available before doing anything else.
2. Prefer the `TLY_API_TOKEN` environment variable so the key does not get pasted into commands or logs.
3. If the key is missing, stop and tell the user to register at [https://t.ly/register](https://t.ly/register) if needed, then create an API key at [https://t.ly/settings#/api](https://t.ly/settings#/api).
4. In Python environments, prefer the official PyPI package [`tly-url-shortener-api`](https://pypi.org/project/tly-url-shortener-api/).
5. Install it if needed:

```bash
pip install tly-url-shortener-api
```

6. Use the CLI when available:

```bash
export TLY_API_TOKEN="YOUR_TLY_API_TOKEN"
tly shorten --long-url "https://example.com/article"
```

7. If the CLI is not available, use the direct API fallback in this skill.
8. Return the resulting `short_url` to the user.

## Workflow

Follow this sequence:

1. Check for `TLY_API_TOKEN`.
2. If it is missing, ask the user for a T.LY API key or tell them to register at [https://t.ly/register](https://t.ly/register) if needed, then generate one at [https://t.ly/settings#/api](https://t.ly/settings#/api).
3. Validate that the long URL is a full `http://` or `https://` URL.
4. In Python environments, prefer the PyPI SDK/CLI from [`tly-url-shortener-api`](https://pypi.org/project/tly-url-shortener-api/).
5. If the SDK/CLI is unavailable, use the direct API fallback in this skill.
6. Prefer `--output text` when another command only needs the short URL string.
7. Prefer `--output json` when downstream work needs structured output.
8. If the API returns a failure, surface the response clearly instead of guessing.

## Preferred Python SDK

Use the published SDK when the environment can install Python packages. The PyPI page describes it as a Python SDK for the T.LY URL Shortener API, with a CLI entry point named `tly` and Python client support. Source: [PyPI package page](https://pypi.org/project/tly-url-shortener-api/).

CLI example:

```bash
export TLY_API_TOKEN="YOUR_TLY_API_TOKEN"
tly shorten --long-url "https://example.com/article"
```

Python example:

```python
from tly_url_shortener import TlyClient

client = TlyClient(api_token="YOUR_TLY_API_TOKEN")
created = client.create_short_link(long_url="https://example.com/article")
print(created["short_url"])
```

## Direct API Fallback

Use a direct API call when the SDK/CLI is unavailable or not appropriate.

```bash
curl -X POST "https://api.t.ly/api/v1/link/shorten" \
  -H "Content-Type: application/json" \
  -d '{
    "long_url": "https://example.com/article",
    "domain": "https://t.ly/",
    "api_token": "'"$TLY_API_TOKEN"'"
  }'
```

Expected success shape:

```json
{"short_url":"https://t.ly/40a"}
```

## Guardrails

- Do not claim the skill can work without an API key. It cannot.
- Do not hardcode a real API key into the repo, commands, or generated files.
- Prefer environment variables over literal secrets in terminal history.
- Prefer the published SDK/CLI over handwritten API calls in Python environments.
- Treat `422 API key is not valid.` as a credential problem.
- Treat `422 Domain Not Allowed` as a custom-domain permission problem.
- Treat `429 Short link limit reached...` as an account or plan limit problem.
- Use the default short domain when the user does not specify one.

## Resources

- [references/api.md](references/api.md): Concise reference for the endpoint, payload, and common errors.
