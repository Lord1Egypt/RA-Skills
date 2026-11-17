---
name: socq-x-research
description: Research public X content, accounts, keywords, and performance data with SocQ. Use when an agent needs X-specific discovery, collection, endpoint selection, credit estimates, asynchronous task execution, pagination, or raw exports through the SocQ CLI, MCP, or REST API.
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

# SocQ X Research

## SocQ Links

- Website: <https://socq.ai/>
- Platform page: <https://socq.ai/apis/x>
- API documentation: <https://docs.socq.ai/api-manual/x>
- API key: <https://socq.ai/dashboard/api-key>
- MCP and CLI: <https://docs.socq.ai/integrations/overview>
- Agent Skill guide: <https://docs.socq.ai/integrations/skill>

Use this Skill to select and run SocQ endpoints for public X research. SocQ requests are asynchronous and credit-metered.

## Use When

- The user asks to discover, collect, compare, or analyze public X data.
- The workflow needs X-specific endpoint selection, input validation, pagination, or raw exports.
- An agent must estimate credits, submit a task, poll it to completion, and report normalized results.

## Plan X research

Choose the endpoint from the shape of the question instead of treating every X request as generic search:

- Use `x/community` for community metadata and rules, and `x/community-posts` for its posts. Both accept community URLs in `urls`.
- Use `x/thread-context` with post URLs to retain the target, ancestors and replies. Keep `conversation_id` and `in_reply_to_id` when reconstructing the thread; page sizes vary.

- Use `x/search` for topic, phrase, hashtag, or time-bounded conversation discovery. Preserve the user's query operators and requested ordering.
- Use `x/trends` for currently trending topics. Report the collection time and requested region because trends are time- and market-sensitive.
- Use `x/profiles` to resolve account identity before collecting an account's posts or network.
- Use `x/user-posts` for a known account's timeline and `x/posts` when the user supplies specific post URLs or IDs.
- Use `x/post-replies`, `x/post-quotes`, or `x/post-retweeters` for distinct engagement behaviors. Do not combine them into one engagement metric without labeling each source.
- Use `x/followers-list` and `x/following-list` for network questions. Treat the returned relationship snapshot as point-in-time data, not proof of historical following.

For conversation analysis, collect seed posts first, retain their IDs, and expand only the requested reply, quote, or repost branches. Distinguish original posts, replies, quotes, and reposts in the final report. When comparing accounts, use the same date window and collection method for each account. X search and trend results can change quickly, so state when the data was collected and avoid claiming exhaustive coverage when pagination or search visibility limits the result.


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

1. Prefer an already configured SocQ MCP server at `https://api.socq.ai/mcp?platforms=x`; use the typed tool listed in [platform.md](references/platform.md), or compact `socq_execute` when needed.
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
