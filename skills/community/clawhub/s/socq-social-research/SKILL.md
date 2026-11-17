---
name: socq-social-research
description: Research public social-platform content, accounts, keywords, and SEO search data with SocQ. Use when an agent needs keyword volume, suggestions, related terms, difficulty, intent, organic results, site rankings, or social data; or needs to discover a SocQ endpoint, estimate credits, submit asynchronous jobs, poll results, paginate normalized records, and retrieve raw files through SocQ MCP or CLI.
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

# SocQ Social and SEO Research

## SocQ Links

- Website: <https://socq.ai/>
- Platform catalog: <https://socq.ai/platforms>
- API documentation: <https://docs.socq.ai/api-manual>
- API key: <https://socq.ai/dashboard/api-key>
- MCP and CLI: <https://docs.socq.ai/integrations/overview>
- Agent Skill guide: <https://docs.socq.ai/integrations/skill>

Use this Skill to select and run SocQ endpoints for public social-platform and SEO research. SocQ requests are asynchronous and credit-metered.

## Use When

- The user asks to discover, collect, compare, monitor, or analyze public social or SEO data.
- The workflow spans platforms or needs endpoint discovery through the Capability Registry.
- An agent must estimate credits, submit tasks, poll results, paginate normalized records, or retrieve raw exports.

## Endpoint Selection

- Search the live Capability Registry first. Read [catalog.md](references/catalog.md) when tool discovery is unavailable.
- Read the matching generated platform reference before selecting endpoints or constructing input: [Facebook](references/platforms/facebook.md), [Facebook Ad Library](references/platforms/facebook-ad-library.md), [Facebook Marketplace](references/platforms/facebook-marketplace.md), [Google Ad Library](references/platforms/google-ad-library.md), [Instagram](references/platforms/instagram.md), [LinkedIn](references/platforms/linkedin.md), [LinkedIn Ad Library](references/platforms/linkedin-ad-library.md), [Pinterest](references/platforms/pinterest.md), [Reddit](references/platforms/reddit.md), [Threads](references/platforms/threads.md), [TikTok](references/platforms/tiktok.md), [TikTok Ad Library](references/platforms/tiktok-ad-library.md), [TikTok Shop](references/platforms/tiktok-shop.md), [X](references/platforms/x.md), [YouTube](references/platforms/youtube.md), or [SEO](references/platforms/seo.md).
- Choose endpoints from the requested resource shape rather than routing every request through broad search.
- Prefer direct URLs, canonical usernames, or platform IDs when supplied.
- For multi-network research, follow [cross-platform.md](references/cross-platform.md) and use comparable date windows, limits, locales, and content types.

## Key Inputs

- Preserve the requested platforms, entities, query terms, date range, locale, filters, ordering, and result cap.
- Ask only for missing input required by the selected endpoint.
- Use `view: "standard"` for MCP and Skill result reads. Use `_result_view: "standard"` for typed MCP tools or `--result-view standard` for CLI output.
- Add a reusable idempotency key when a submission might be retried.
- Treat `next_cursor` as opaque and stop only at the requested scope or user-approved cap.

## Execution

1. Prefer an already configured hosted SocQ MCP server at `https://api.socq.ai/mcp`.
2. Filter MCP with `?platforms=youtube,tiktok` for up to five platforms or `?tools=youtube_comments,x_search` for up to thirty endpoint tools when scope is known.
3. Use `npx @socq/mcp` for local stdio-only clients. If MCP is unavailable, use `socq` or `npx @socq/cli`; use REST only as the final fallback.
4. Read [authentication.md](references/authentication.md), keep `SOCQ_API_KEY` in the environment, and never put it in prompts, URLs, committed files, or retained commands.
5. Read [billing.md](references/billing.md), report expected cost, and obtain confirmation before a paid large-volume, cross-platform, or multi-endpoint run.
6. Submit with `_request_source: "skill"`, `--request-source skill`, or `X-Socq-Source: skill-rest` for MCP, CLI, or REST.
7. Save every task ID. Treat `queued` and `running` as incomplete and follow [async-tasks.md](references/async-tasks.md) until `succeeded` or `failed`.
8. Follow [pagination.md](references/pagination.md) for requested pages and retrieve task files when complete raw JSONL output is required.
9. Read [errors.md](references/errors.md) before retrying authentication, credit, rate-limit, validation, or provider failures.

## Output Expectations

Include:

- selected endpoints, platforms, and execution path
- concise input, filter, window, and comparability summary
- expected and reported credit usage when available
- task IDs and terminal statuses
- result counts, pages read, and whether more data remains
- normalized findings or raw export locations
- collection time, failed platforms, unsupported filters, and incomplete coverage

## Guardrails

- Collect only public data supported by the selected endpoint.
- Do not retry a failed paid request blindly; inspect the normalized error first.
- Do not start a paid large-volume, cross-platform, or multi-endpoint run without user confirmation.
- Do not invent unsupported parameters; re-read the live endpoint schema after validation errors.
- Do not claim completeness when pagination stopped early, a provider failed, or the requested date filter is unsupported.
- Do not compare metrics collected with different windows, filters, locales, or content types without labeling the difference.
- Keep task IDs in working notes so interrupted research can resume without resubmitting.
