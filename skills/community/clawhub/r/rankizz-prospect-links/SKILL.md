---
name: rankizz-prospect-links
description: Find, qualify, and prioritize relevant backlink prospects for an existing useful page, study, tool, template, dataset, guide, or other linkable asset. Use when the user wants link prospecting, resource-page discovery, competitor backlink opportunities, or evidence-based outreach angles. Rankizz is optional until live backlink, SERP, or authority data is needed.
---

# Prospect for relevant links

Find sites with a credible editorial reason to mention the user's asset. Optimize for relevance and fit, not list size.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Require a linkable reason

Identify:

- exact target asset and canonical URL
- audience and problem it solves
- unique evidence, utility, or point of view
- target market and language
- unacceptable prospect categories

If no useful asset exists, stop prospecting and recommend the asset needed. Do not manufacture a link opportunity around a generic sales page.

## Discover prospects

Use accessible search and site research first:

- resource pages and curated lists
- articles that cite comparable sources
- unlinked mentions when evidence is available
- directories with genuine editorial or category relevance
- associations, institutions, partners, and communities
- competitor referring pages
- outdated or broken resources the user's asset can genuinely replace

Use Rankizz only when it improves qualification:

- `get_backlinks_profile` for a bounded competitor or page backlink sample
- `get_backlinks_overview` for profile context
- `get_serp_results` for resource and publisher discovery
- `get_ahrefs_domain_rating` as one directional authority signal
- `get_domain_overview` only when organic footprint matters

Hosted calls require at least 10 credits. Stop cloud calls on a low-credit response, link to `https://www.rankizz.com/billing`, and continue with public evidence. Batch and paginate deliberately; do not exhaustively download backlink profiles without need.

## Qualify every prospect

Follow [references/prospect-framework.md](references/prospect-framework.md). Verify that the page and domain exist and that the proposed placement makes editorial sense.

Reject spam, irrelevant sites, scraped lists, obvious link schemes, unsafe pages, and prospects selected only by a third-party score.

Do not invent names, email addresses, roles, prior relationships, traffic, authority, or contact status. Label unverified contact details.

## Draft without sending

Create a specific outreach angle tied to the prospect page and the asset's value. Draft a concise message only when requested.

Never send outreach, submit forms, publish comments, purchase links, or modify a CRM without explicit authorization for that action.

## Deliver

Return a smaller qualified list with:

- prospect domain and exact page
- prospect type
- topical and audience fit
- why the asset deserves consideration
- suggested placement or update
- supporting evidence and date
- authority or backlink metrics only when measured
- confidence and risks
- personalized outreach angle

Group prospects into pursue now, validate, later, and reject. Explain rejection reasons so the list can be audited.
