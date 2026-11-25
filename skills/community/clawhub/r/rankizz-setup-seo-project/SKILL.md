---
name: rankizz-setup-seo-project
description: Create or refresh a reusable local SEO project workspace containing a site's goals, audience, positioning, markets, competitors, constraints, and available data. Use when starting ongoing SEO work for a website or client, when later research needs durable project context, or when the user asks to organize an SEO workspace. Rankizz access is optional.
---

# Set up an SEO project

Create durable project context before running research. Keep this workflow local unless the user explicitly asks to associate it with Rankizz.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Gather the minimum context

Inspect the current workspace before asking questions. Reuse information already present in briefs, analytics exports, repository files, or an existing project summary.

Collect only missing information that affects the work:

- canonical website and relevant subdomains
- business model, products, and positioning
- target audiences and their problems
- primary countries, languages, or local markets
- business and SEO goals
- known business and search competitors
- conversion actions that matter
- constraints, exclusions, compliance needs, and tone
- available sources such as Search Console, analytics, keyword exports, audits, or Rankizz

Do not block setup on unknown fields. Mark them as unknown and list the most valuable follow-up question.

## Create or update the workspace

Use an existing user-selected folder when provided. Otherwise create an `seo-project` folder in the current working directory. Do not overwrite existing content without reviewing it.

Create this minimal structure only when it is useful:

```text
seo-project/
  PROJECT.md
  audits/
  keywords/
  competitors/
  research/
  reports/
```

Write `PROJECT.md` using [references/project-template.md](references/project-template.md). Keep facts separate from assumptions and record the source and date for important evidence.

Do not store passwords, API keys, OAuth tokens, private customer data, or copied credentials in the workspace.

## Associate Rankizz only when requested

If Rankizz MCP is already connected and the user wants cloud workflows:

1. Call `list_projects` before creating anything.
2. Match by canonical domain and organization context.
3. Ask before calling `create_project` when no safe match exists.
4. Save only the returned project ID and public project URL in `PROJECT.md`; never save credentials.

Rankizz-hosted API or MCP access requires at least 10 credits. If access reports a low balance, link the user to `https://www.rankizz.com/billing` and continue the local setup without Rankizz.

## Finish

Return:

1. the workspace path
2. a short project summary
3. known evidence sources and their dates
4. assumptions and unanswered questions
5. the next best skill to run

Recommend one next workflow based on the user's goal: site audit, keyword research, clustering, competitive landscape, competitor analysis, or link prospecting.
