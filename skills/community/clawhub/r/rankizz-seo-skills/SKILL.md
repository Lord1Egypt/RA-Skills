---
name: rankizz-seo-skills
description: Set up and orchestrate Rankizz SEO Skills for a website, repository, or client. Use when an agent needs to initialize SEO project context, choose and install the right Rankizz specialist skills, configure Rankizz MCP or REST API access, or route a broad SEO request into audits, research, roadmaps, content, social, or outreach workflows.
---

# Set up and route Rankizz SEO work

Act as the entry point for the Rankizz skill collection. Inspect the task and current workspace, install only the specialist workflows the task needs, and add live Rankizz access only when it materially improves the outcome.

Read [references/skill-catalog.md](references/skill-catalog.md) before selecting or installing specialist skills.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Inspect before changing the project

1. Identify the canonical site, business goal, target market, requested outcome, deadline, and available evidence.
2. Search the workspace for an existing `PROJECT.md`, installed skills, exports, audit reports, Search Console data, or analytics data.
3. Reuse valid context. Do not reinstall a skill or recreate project files that are already current.
4. Ask only for missing information that would change the workflow.

Never ask the user to paste an API key, OAuth token, password, or other secret into chat or a project file.

## Select the smallest useful skill set

Choose one primary specialist skill for a focused request. Add a second skill only when it supplies a clear prerequisite or downstream deliverable.

- Start with `rankizz-setup-seo-project` when durable site, audience, market, and evidence context is missing.
- Use `rankizz-audit-site-local` for a no-account crawl with local resources.
- Use `rankizz-audit-site-cloud` when the user wants a hosted crawl, persisted results, or Rankizz page-level evidence.
- Use `rankizz-audit-on-page-seo` for one page, one template, or publication QA.
- Use `rankizz-build-seo-roadmap` for a prioritized 1–30 day execution plan.
- Route keyword, competitor, backlink, editorial, social, and outreach requests with the decision table in the catalog reference.

Do not download the entire collection by default. Explain which skills were selected and why.

## Install selected skills

Every public skill has:

- readable instructions: `https://www.rankizz.com/docs/skills/<skill-name>`
- raw instructions: `https://www.rankizz.com/skills/<skill-name>/SKILL.md`
- upload-ready ZIP: `https://www.rankizz.com/skills/<skill-name>.zip`

For a local folder client, create one directory per skill and extract the ZIP into it. Example for a repository-scoped portable installation:

```sh
mkdir -p .agents/skills/rankizz-audit-site-local
curl -L https://www.rankizz.com/skills/rankizz-audit-site-local.zip -o rankizz-audit-site-local.zip
unzip -q rankizz-audit-site-local.zip -d .agents/skills/rankizz-audit-site-local
```

Remove the downloaded archive after the user confirms installation. Use the client-specific path documented at `https://www.rankizz.com/docs/skills` when the client does not scan `.agents/skills`.

For Claude.ai, ChatGPT, Perplexity Computer, and other upload-based clients, download the selected ZIP and upload it through the client's Skills interface. The ZIP keeps `SKILL.md` at its root so references, scripts, and assets remain attached.

Review every `SKILL.md` and bundled script before enabling it. Never run an unreviewed script merely because it came from a skill package.

## Choose local work, MCP, or REST

Prefer local resources when the workflow can use the site, repository, browser, files, or user-provided exports. A Rankizz account is not required for local-only work.

Use Rankizz MCP when an interactive AI agent needs live Rankizz tools or saved project data:

1. Open the client's connectors or MCP settings.
2. Add `https://www.rankizz.com/mcp` as a remote HTTPS Streamable HTTP server.
3. Prefer browser-based OAuth. Do not create an API key for an interactive client that supports OAuth.
4. Use the client-specific guide at `https://www.rankizz.com/docs/mcp`.
5. Verify the connection by listing Rankizz projects before starting project-scoped work.

For Perplexity, use Perplexity Computer or an eligible workspace: open Settings > Connectors, add a custom Remote connector, select Streamable HTTP, paste the Rankizz MCP URL, choose OAuth, and authenticate. If the workspace does not expose custom remote connectors, continue locally or use the REST API from an authorized external workflow.

Use the Rankizz REST API for headless services, CI, deterministic scripts, or applications:

- API access and key management: `https://www.rankizz.com/api-access`
- API documentation: `https://www.rankizz.com/docs/api`
- OpenAPI document: `https://www.rankizz.com/api/v1/openapi.json`
- base URL: `https://www.rankizz.com/api/v1`
- tool call: `POST /api/v1/tools/<tool-name>`
- authentication: `Authorization: Bearer <key>`

Tell the user to store the key in a secret manager or environment variable. Do not display, persist, log, or commit the key.

## Route AI prompt research

For an AI brand-mention or source-check request, discover `research_ai_rank_tracking_prompt` with `search_tools` and `includeSchemas: true`, then invoke it through `call_tool`. REST uses `POST /api/v1/tools/research_ai_rank_tracking_prompt`. Supply `projectId`, one `prompt`, and selected `providers`: `chatgpt`, `google_ai_mode`, `perplexity`, `gemini`, or `claude`. This metered check does not change the saved prompt set.

Read every provider result's `status` even when the outer call succeeds. Blocked, empty, or timed-out responses return `UPSTREAM_UNAVAILABLE`; treat them as missing evidence. Successful results have a non-empty answer and may have an empty citation list. The citation list includes source links, with Google AI Mode attached sources as a fallback, so it does not prove every URL was cited inline. Keep the prompt, market, provider, and research timestamp with any visibility conclusion.

## Enforce Rankizz access rules

Rankizz-hosted MCP and REST calls require at least 10 available credits before execution. If the balance is lower, stop the live call, explain that Rankizz access is paused, and direct the user to `https://www.rankizz.com/billing`. Continue with a local workflow when one can still satisfy the request.

Installing, reading, or running a local-only skill consumes no Rankizz credits. A successful zero-cost Rankizz operation can require the minimum balance without deducting credits.

## Finish setup

Return:

1. the project context found or created
2. the specialist skills selected and installed
3. why each skill matches the task
4. whether the workflow is local, MCP, REST, or hybrid
5. any required authorization or credit action
6. the exact next prompt or command to begin the primary workflow
