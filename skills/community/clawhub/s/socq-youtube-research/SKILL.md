---
name: socq-youtube-research
description: Research public YouTube content, accounts, keywords, and performance data with SocQ. Use when an agent needs YouTube-specific discovery, collection, endpoint selection, credit estimates, asynchronous task execution, pagination, or raw exports through the SocQ CLI, MCP, or REST API.
metadata:
  openclaw:
    homepage: https://github.com/SocQAPI/socq-devtools
    primaryEnv: SOCQ_API_KEY
    requires:
      env:
        - SOCQ_API_KEY
      anyBins:
        - socq
        - npx
    envVars:
      - name: SOCQ_API_KEY
        required: true
        description: SocQ API key used to authenticate CLI, MCP, and REST requests.
    install:
      - kind: node
        package: "@socq/cli"
        bins:
          - socq
---

# SocQ YouTube Research

## SocQ Links

- Website: <https://socq.ai/>
- Platform page: <https://socq.ai/apis/youtube>
- API documentation: <https://docs.socq.ai/api-manual/youtube>
- API key: <https://socq.ai/dashboard/api-key>
- MCP and CLI: <https://docs.socq.ai/integrations/overview>
- Agent Skill guide: <https://docs.socq.ai/integrations/skill>

Use this Skill to select and run SocQ endpoints for public YouTube research. SocQ requests are asynchronous and credit-metered.

## Use When

- The user asks to discover, collect, compare, or analyze public YouTube data.
- The workflow needs YouTube-specific endpoint selection, input validation, pagination, or raw exports.
- An agent must estimate credits, submit a task, poll it to completion, and report normalized results.

## Plan YouTube research

Select an endpoint based on the YouTube content object the user needs:

- Use `youtube/search` or `youtube/hashtag-search` for discovery, then resolve selected results with `youtube/videos` or `youtube/channels` when detailed metadata is required.
- Use `youtube/channel-videos`, `youtube/channel-live-videos`, and `youtube/shorts` for format-specific channel inventories. Keep regular uploads, live streams, and Shorts separate in comparisons.
- Use `youtube/playlist-videos` only when playlist membership or ordering matters; do not treat a playlist as the channel's complete catalog.
- Use `youtube/comments` for top-level discussion and `youtube/comment-replies` for a selected thread. Preserve parent comment IDs so replies remain attributable.
- Use `youtube/transcripts` for spoken-content analysis. Report unavailable, disabled, auto-generated, or language-mismatched transcripts instead of substituting descriptions.
- Use `youtube/community-posts` for channel community activity and keep it distinct from video publishing activity.

Resolve channel and video URLs to canonical IDs before joining results across endpoints. For performance comparisons, align publication windows and distinguish cumulative counters from activity observed during the requested period. A video's current views or comments are not the number gained inside a historical date range. When analyzing themes from transcripts and comments, identify which evidence comes from creator speech and which comes from audience discussion. State whether the result includes videos, Shorts, live streams, playlists, community posts, or only a subset.


## Endpoint Selection

- Read [platform.md](references/platform.md) before selecting an endpoint or constructing input. It contains the current endpoint IDs, typed MCP tools, CLI mappings, costs, input choices, and validated examples generated from the Capability Registry.
- Choose from the shape of the requested resource; do not route every request through broad search.
- Prefer direct URLs, canonical usernames, or platform IDs when the user supplies them.
- Re-read the live schema after a validation error instead of inventing parameters.

## Key Inputs

- Preserve the user's entities, query terms, date range, locale, filters, ordering, and requested result limit.
- Ask only for missing input required by the selected endpoint.
- Use `view: "standard"` for MCP and Skill result reads. Use `_result_view: "standard"` for typed MCP tools or `--result-view standard` for CLI output.
- Add a reusable idempotency key when a submission might be retried.
- Treat `next_cursor` as opaque and continue only until the requested scope or user-approved cap is reached.

## Execution

1. Prefer an already configured SocQ MCP server at `https://api.socq.ai/mcp?platforms=youtube`; use the typed tool listed in [platform.md](references/platform.md), or compact `socq_execute` when needed.
2. If MCP is unavailable, use `socq` or `npx @socq/cli`. Use REST only as the final fallback.
3. Read [authentication.md](references/authentication.md), keep `SOCQ_API_KEY` in the environment, and never put it in prompts, URLs, committed files, or retained commands.
4. Read [billing.md](references/billing.md), report the expected cost, and obtain confirmation before a paid large-volume or multi-endpoint run.
5. Submit with `_request_source: "skill"`, `--request-source skill`, or `X-Socq-Source: skill-rest` for MCP, CLI, or REST.
6. Save the returned task ID. Treat `queued` and `running` as incomplete and follow [async-tasks.md](references/async-tasks.md) until `succeeded` or `failed`.
7. Follow [pagination.md](references/pagination.md) for all requested pages. Retrieve task files when complete raw JSONL output is required.
8. Read [errors.md](references/errors.md) before retrying authentication, credit, rate-limit, validation, or provider failures.

## Output Expectations

Include:

- selected endpoint and execution path (MCP, CLI, or REST)
- concise input and filter summary
- expected and reported credit usage when available
- task ID and terminal status
- result count, pages read, and whether more data remains
- normalized findings or the raw export location
- collection time, failed requests, unsupported filters, and incomplete coverage

## Guardrails

- Collect only public data supported by the selected endpoint.
- Do not retry a failed paid request blindly; inspect the normalized error first.
- Do not start a paid large-volume or multi-endpoint run without user confirmation.
- Do not claim completeness when pagination stops early, a provider fails, or a requested filter is unsupported.
- Do not compare metrics collected with different date windows, filters, locales, or content types without labeling the difference.
- Keep task IDs in working notes so interrupted research can resume without resubmitting.
