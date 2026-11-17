# Unbrowse for Siriusxm — MCP & skill (unofficial)

siriusxm.com as agent tools, compiled by [Unbrowse](https://unbrowse.ai) from the site's own first-party requests. Verified results, no browser on your side. Not affiliated with or endorsed by siriusxm.com.

| Tool | What it does |
|---|---|
| `siriusxm_com__get_search` | Search SiriusXM |
| `siriusxm_com__get_mountain_purejazz` | Open a channel page |
| `siriusxm_com__read_page` | Read a page on siriusxm.com |

**MCP** (remote, streamable HTTP, OAuth): `https://unbrowse.ai/mcp/siriusxm.com`

```sh
claude mcp add --transport http siriusxm https://unbrowse.ai/mcp/siriusxm.com
```

**Skill**: `npx skills add https://unbrowse.ai --skill siriusxm` (or `npx skills add unbrowse-ai/sites --skill siriusxm`) — see [SKILL.md](SKILL.md).

REST + OpenAPI: https://unbrowse.ai/api/v1/sites/siriusxm.com/openapi.json
