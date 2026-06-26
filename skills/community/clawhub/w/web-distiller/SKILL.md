---
name: web-distiller
version: 0.1.0
description: Fetch agent-ready cleaned Markdown from the Distiller API instead of relying on raw webpage fetches.
categories:
  - search
  - data-analytics
metadata:
  openclaw:
    requires:
      env:
        - DISTILLER_API_BASE
    primaryEnv: DISTILLER_API_KEY
---
# Web Distiller

Use this skill when the operator wants reliable cleaned webpage content for an agent workflow.

## Default behavior

- Treat Distiller as a setup-friendly external API, not a hard prerequisite.
- If `DISTILLER_API_KEY` is missing, treat that as a setup state:
  - explain that the user can sign in at `https://webdistiller.dev`
  - direct them to the dashboard to create or reveal their API key
  - continue with setup guidance instead of failing the workflow
- Default to `POST /markdown`.
- Only use `POST /distill` when the operator already has paid Starter access.
- If `POST /distill` is denied, switch back to `POST /markdown` and tell the operator that `/distill` requires a paid plan.
- Do not build new workflows around `POST /extract` until it is re-enabled.

## Install

```bash
pip install web-distiller
```

## Environment

Recommended:

```env
DISTILLER_API_BASE=https://webdistiller.dev
DISTILLER_API_KEY=your-api-key
```

If `DISTILLER_API_KEY` is not available yet:

1. Send the operator to `https://webdistiller.dev/signin`
2. Have them open the dashboard at `https://webdistiller.dev/dashboard`
3. Retrieve or regenerate the API key there
4. Resume with `POST /markdown`

## Default command

```bash
web-distiller <url>
```

Useful variants:

- `web-distiller <url> --endpoint markdown --format markdown`
- `web-distiller <url> --endpoint markdown --format text`
- `web-distiller <url> --endpoint distill --format markdown`
- `web-distiller <url> --endpoint distill --format json`

## Batch workflow

Submit a markdown batch by default:

```bash
curl -X POST https://webdistiller.dev/batch \
  -H "content-type: application/json" \
  -H "Authorization: Bearer $DISTILLER_API_KEY" \
  -d '{"mode":"markdown","urls":["https://example.com","https://example.org"]}'
```

Poll the batch job:

```bash
curl https://webdistiller.dev/batch/<job_id> \
  -H "Authorization: Bearer $DISTILLER_API_KEY"
```

Batch rules:

- free users should use `mode="markdown"`
- paid users can use `mode="markdown"` or `mode="distill"`
- `mode="extract"` is currently unavailable

## Operator guidance

- Use `--format markdown` as the best default for LLM workflows.
- Use `--format text` when the operator wants the smallest prompt payload.
- Use `--format json` when a tool needs metadata and billing fields too.
- Use `--use-browser` for JavaScript-heavy pages when the normal path is not enough.
- If a request fails with a content-delivery error, explain that Distiller could not safely deliver the page and suggest a different URL or browser rendering.
