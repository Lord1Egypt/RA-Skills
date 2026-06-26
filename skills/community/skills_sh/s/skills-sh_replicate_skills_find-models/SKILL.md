---
name: find-models
description: Find AI models on Replicate using search and curated collections.
---

## Always search the API for current models

The AI model landscape changes weekly. New models ship constantly and older ones are deprecated or surpassed. Don't rely on model names you've seen before, including names from past conversations or training data. A specific model you "know" may no longer be the best choice, may be slower than newer alternatives, or may not exist anymore.

Always start by querying the Replicate API. Use search and collections to discover what's currently available, then read schemas to understand inputs and outputs before running anything.

## Docs

- Reference: <https://replicate.com/docs/llms.txt>
- OpenAPI schema: <https://api.replicate.com/openapi.json>
- MCP server: <https://mcp.replicate.com>
- Per-model docs: `https://replicate.com/{owner}/{model}/llms.txt`
- Set `Accept: text/markdown` when requesting docs pages for Markdown responses.

## Search

- Use the search API (`GET /v1/search?query=...`) to find models by task. Returns models, collections, and docs.
- Search returns metadata for each model including `tags`, `generated_description`, and `run_count`.
- The search API also returns matching collections alongside model results.
- Avoid listing all models via API. It's a firehose. Use targeted queries.

## Collections

- Collections are curated groups of models maintained by Replicate staff.
- The `official` collection contains always-warm models with stable APIs and predictable pricing.
- Use collections to narrow a shortlist before deep comparison.
- List collections with `GET /v1/collections`. Get one by slug with `GET /v1/collections/{slug}`.

## Reading model schemas

- Every model exposes its input/output schema via the models API (`GET /v1/models/{owner}/{name}`).
- Schema path: `model.latest_version.openapi_schema.components.schemas.Input.properties`
- Each property may include: `type`, `description`, `default`, `minimum`/`maximum`, `enum`, `format` (e.g. `uri` for file inputs).
- Always fetch the schema before running a model. Schemas change.

## Picking the right model

- Prefer official models. They're always warm (no cold boot), have stable APIs, and predictable pricing.
- Prefer the latest version. If search returns v2.5 and v3.0, use v3.
- Run count can be misleading. Old models accumulate runs over time but may be outdated. A model with 10M runs from 2023 is likely worse than a model with 100K runs from 2025.
- Prefer recently released models. The AI space moves fast.
- Check model tags to help filter by task (`image-generation`, `video`, `audio`, etc.).

## Model identifiers

- **Official models** use `owner/name` format (e.g. `owner/model-name`). Routes to the latest version automatically.
- **Community models** require `owner/name:version_id`. You must pin a specific version. Community models can cold-boot and take time to start.
- If you must use a community model, be aware that it can take a long time to boot. You can create always-on deployments, but you pay for model uptime.
