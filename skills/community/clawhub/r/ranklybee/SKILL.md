---
name: ranklybee
description: Read and act on a RanklyBee SEO workspace - Google Search Console and Bing data, content, backlinks, link prospects and outreach, community leads, and AI visibility - through the RanklyBee MCP server or Public API.
---

# RanklyBee

[RanklyBee](https://ranklybee.com) is an SEO and AI-visibility workspace for
websites. Use this skill when the user asks about their own site's search
performance, content plan, backlinks, link-building outreach, community leads,
or how AI assistants mention their brand, and they have a RanklyBee account.

RanklyBee only reads the signed-in user's own Projects and connected sites. It
cannot report rankings or traffic for websites the user does not own.

## Setup

1. Create an account at <https://ranklybee.com> (sign up with Google or email).
   Search Console and Bing data are free on every account; the other modules
   need an active plan (a 3-day trial is available).
2. Add a Project with your website, and connect Google Search Console or Bing
   Webmaster Tools inside RanklyBee if you want search data.
3. Connect the agent in one of two ways:
   - **MCP (recommended):** add the remote server
     `https://api.ranklybee.com/mcp` (Streamable HTTP). The client opens a
     RanklyBee sign-in and consent page; choose the permissions to grant.
     Reading is on by default; anything that changes data, sends email or
     publishes stays off until the user turns it on.
   - **Public API:** create a token in RanklyBee under Settings > API access
     and send it as `Authorization: Bearer <token>`. Keep the token in the
     client's secret store or an environment variable such as
     `RANKLYBEE_API_TOKEN`; never ask the user to paste it into the chat.

Full setup guide for Cursor, Claude Code, Codex and other clients:
<https://ranklybee.com/docs/mcp>

## Using the MCP server

Start with `list_projects`, then `list_sites`, to get the `projectId` and
`siteId` most tools need. Useful tools include:

- Search: `get_search_console_overview`, `get_search_console_report`,
  `get_search_console_trend`, `inspect_urls`, `get_seo_health`,
  `list_ctr_opportunities`, `get_bing_report`
- Content: `get_content_plan`, `list_articles`, `get_article`,
  `generate_article`, `publish_article`
- Backlinks and outreach: `list_backlinks`, `list_prospects`,
  `find_prospect_contact`, `prepare_outreach_draft`, `list_outreach_threads`
- Leads: `list_leads`, `get_lead`, `generate_lead_reply`
- AI visibility: `get_ai_visibility_overview`, `list_ai_visibility_prompts`,
  `get_ai_visibility_competitors`

Read before you write: fetch the current record, then change only what the
user asked for. Get the user's approval before any tool that publishes, sends
email or posts on their behalf.

## Using the Public API

Base URL: `https://api.ranklybee.com/api/public/v1`
OpenAPI document: <https://api.ranklybee.com/api/public/openapi.json>

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/me` | Current API account |
| GET | `/projects` | Projects the token can access |
| GET | `/projects/{projectId}/sites` | Websites in a Project |
| GET | `/projects/{projectId}/backlinks` | Tracked backlinks |
| GET | `/projects/{projectId}/prospects` | Link prospects |
| GET | `/projects/{projectId}/sites/{siteId}/drafts` | Outreach drafts |
| GET | `/projects/{projectId}/sites/{siteId}/threads` | Outreach conversations |
| GET | `/projects/{projectId}/leads` | Scored community leads |

Example:

```bash
curl -H "Authorization: Bearer $RANKLYBEE_API_TOKEN" \
  https://api.ranklybee.com/api/public/v1/projects
```

Write endpoints (queue outreach, reply to a thread, move a lead) act on the
user's account and mailbox. Confirm with the user before calling them.

## Links

- Website: <https://ranklybee.com>
- Docs: <https://ranklybee.com/docs/mcp>
- Help: <https://ranklybee.com/help>
- Support: support@ranklybee.com
