---
name: rankizz-audit-site-cloud
description: Run and interpret a hosted Rankizz website audit through Rankizz MCP or REST API, including a robots-aware crawl, prioritized SEO issues, crawled-page evidence, and optional Lighthouse measurements. Use when the user explicitly wants a Rankizz, cloud, hosted, large-site, or repeatable site audit. Do not use for a local-only audit without Rankizz access.
---

# Audit a site with Rankizz cloud

Use Rankizz for the crawl and persisted findings. Produce an evidence-based report, not a generic checklist.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Resolve access safely

Prefer Rankizz MCP in interactive AI clients. Use the REST API only for headless clients or when the user explicitly chooses it. Never ask the user to paste an API key into chat; direct them to `https://www.rankizz.com/api-access` and their client's secret storage.

Use OAuth for ChatGPT, Claude.ai, and other interactive remote MCP clients. The MCP endpoint is:

```text
https://www.rankizz.com/mcp
```

Rankizz-hosted MCP and API calls require a current balance of at least 10 credits. If any call returns the low-credit or payment-required error, stop cloud calls and link to `https://www.rankizz.com/billing`. Do not silently switch to a different paid provider.

## Confirm the crawl scope

Infer scope from an explicit request. Ask one concise question only when the request does not make the intended depth clear.

- **Quick audit:** use the default 10-page budget and representative Lighthouse sampling.
- **Full audit:** use the user's requested page budget or path scope. If absent, propose a bounded page budget based on the known site size.

State that the crawl costs approximately one credit per crawled page and that Lighthouse can reserve additional credits for up to ten representative pages. Obtain confirmation before starting a scope that the user did not already authorize.

Never describe a full audit as unlimited. Respect Rankizz account limits and the `maxPages` accepted by the tool.

## Run the audit

1. Call `list_projects` and select the project whose canonical domain matches the target.
2. Ask before calling `create_project` if no matching project exists.
3. Call `run_site_audit` with the confirmed URL, optional path scope, page budget, and Lighthouse choice.
4. Poll `get_audit_status` at sensible intervals until it completes or fails. Do not start a duplicate audit because one is still running.
5. Call `get_audit_issues` for the prioritized issue set.
6. Call `get_audit_pages` for page-level evidence and coverage. Increase its limit only when the report genuinely needs more rows.
7. If the crawler reports blocked pages, describe the incomplete coverage honestly. Do not reinterpret blocking as broken pages.

Read [references/rankizz-audit-tools.md](references/rankizz-audit-tools.md) for the tool sequence and [references/report-contract.md](references/report-contract.md) before writing the result.

## Enrich only when it changes the decision

Do not automatically run unrelated paid research.

- Use Search Console or Bing Webmaster only when the user asks about indexing or connected search performance.
- Use Google Analytics only when organic landing-page behavior or conversions affect prioritization.
- Use domain, SERP, keyword, or backlink tools only when the audit question requires off-page or demand evidence.
- Prefer cached or no-credit reads before fresh paid research.
- Batch keywords and SERP queries where the tool supports it.

Do not infer rankings, traffic, backlinks, conversions, or AI citations from crawl HTML.

## Assess SEO, GEO, and AEO honestly

Treat technical crawl findings as SEO evidence. Assess GEO and AEO only from retrieved page content or explicit structured-data evidence. Mark a dimension `not assessed` when the available output cannot support it.

Do not turn heuristic checks into claims about how Google, Bing, ChatGPT, Claude, Gemini, or another system will rank or cite a page.

## Deliver the report

Return a concise chat recap and save a Markdown or HTML report when the environment supports files. Generate PDF or DOCX only when the user asks or the agent has an appropriate document tool.

Every finding must include:

- severity
- affected URL or scope
- observed evidence
- why it matters
- exact recommended action
- impact and effort
- evidence source and retrieval date

End with the three highest-value actions, what is already working, coverage limitations, and a link to the Rankizz audit page returned in tool metadata.
