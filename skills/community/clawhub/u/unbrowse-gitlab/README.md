# Unbrowse for Gitlab — MCP & skill (unofficial)

gitlab.com as agent tools, compiled by [Unbrowse](https://unbrowse.ai) from the site's own first-party requests. Verified results, no browser on your side. Not affiliated with or endorsed by gitlab.com.

| Tool | What it does |
|---|---|
| `about_gitlab_com__get_pricing_payload_json` | View GitLab pricing tiers and plans |
| `gitlab_com__render_page` | Search GitLab explore projects by name |
| `docs_gitlab_com__read_page` | Read a docs.gitlab.com page by name |

**MCP** (remote, streamable HTTP, OAuth): `https://unbrowse.ai/mcp/gitlab.com`

```sh
claude mcp add --transport http gitlab https://unbrowse.ai/mcp/gitlab.com
```

**Skill**: `npx skills add https://unbrowse.ai --skill gitlab` (or `npx skills add unbrowse-ai/sites --skill gitlab`) — see [SKILL.md](SKILL.md).

REST + OpenAPI: https://unbrowse.ai/api/v1/sites/gitlab.com/openapi.json
