# Submission links — use these exact URLs (with `?ref=` for attribution)

When listing the Vocab Voyage MCP endpoint in any directory or community post, use the variant that includes the `?ref=<channel>` query param. The MCP server records this on every tool call into `mcp_tool_calls.install_source`, so you can see which channel actually drives usage.

The server normalizes refs to lowercase `[a-z0-9_-]{1,32}`. The slugs below are the canonical ones — match these exactly so the Friday analytics query buckets cleanly.

## MCP endpoint, per channel

| Channel | URL to submit |
|---|---|
| **modelcontextprotocol/registry** (`mcp-publisher publish`) | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=mcp_registry` |
| **Glama** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=glama` |
| **Smithery** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=smithery` |
| **mcpmarket.com** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=mcpmarket` |
| **ClawHub** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=clawhub` |
| **Reddit r/ClaudeAI** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_claudeai` |
| **Reddit r/ChatGPT** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_chatgpt` |
| **Reddit r/OpenAI** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_openai` |
| **Reddit r/SAT** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_sat` |
| **Reddit r/ApplyingToCollege** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_a2c` |
| **Reddit r/ISEE** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=reddit_isee` |
| **X / Twitter** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=twitter` |
| **Hacker News (Show HN)** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=hn` |
| **YouTube demo** | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server?ref=youtube` |

## Discovery + auxiliary surfaces

When a directory or partner page lets you link more than one URL, include the relevant discovery surface so agents can introspect us without hitting the MCP endpoint first:

| Surface | URL |
|---|---|
| `agent_card` | `https://vocab.voyage/.well-known/agent-card.json` |
| `server_card` | `https://vocab.voyage/.well-known/mcp/server-card.json` |
| `mcp_apps` | `https://vocab.voyage/.well-known/mcp/apps.json` |
| `api_catalog` | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/api-catalog` |
| `nlweb` | `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/nlweb-ask` |
| `openapi` | `https://vocab.voyage/openapi.json` |
| `schemamap` | `https://vocab.voyage/schemamap.xml` |
| `auth_docs` | `https://vocab.voyage/developers/auth` |
| `oauth_protected_resource` | `https://vocab.voyage/.well-known/oauth-protected-resource` |
| `llms_txt` | `https://vocab.voyage/llms-full.txt` |
| `pricing` | `https://vocab.voyage/pricing.md` |

## Header alternative to `?ref=`

Channels and partners that can't add a query string can pass:

```
x-install-source: <slug>
```

Both produce identical `install_source` rows — pick whichever is easier.

## Friday attribution query

```sql
select
  coalesce(install_source, '(direct/no-ref)') as source,
  count(*) as calls,
  count(distinct user_id) as authed_users,
  count(distinct ip_hash) filter (where user_id is null) as anon_clients,
  round(avg(latency_ms))::int as avg_latency_ms,
  round(100.0 * count(*) filter (where status = 'ok') / count(*), 1) as success_pct
from public.mcp_tool_calls
where created_at >= now() - interval '7 days'
group by 1
order by calls desc;
```
