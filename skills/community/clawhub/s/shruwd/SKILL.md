---
name: shruwd
description: Track how a brand shows up in AI answers, and act on the findings, through Shruwd's MCP server.
version: 1.0.3
metadata:
  openclaw:
    primaryEnv: SHRUWD_API_KEY
    envVars:
      - name: SHRUWD_API_KEY
        required: false
        description: Shruwd API key (dashboard → Account → API keys). Only for the API-key and local setups; the hosted server with sign-in needs no key. Needs a Shruwd account; see https://shruwd.io/pricing.
      - name: SHRUWD_API_URL
        required: false
        description: API base URL for the local server. Defaults to https://shruwd.io/api/v1.
    homepage: https://shruwd.io
---

# Shruwd

Shruwd measures a brand's AI-search visibility: how often AI answers mention it, its share of
voice against competitors, and which AI crawlers read its site. This skill connects Shruwd's
MCP server (source: https://github.com/ilpr/shruwd-mcp, MIT) so you can set up a brand, track
prompts and competitors, and read results.

**External service.** Every tool call goes to shruwd.io and acts as the signed-in user, or as the
holder of the API key. The user needs a Shruwd account. Access is bound to one workspace and
carries the user's role in it.

## Setup

### Hosted, with sign-in (recommended)

The server runs at `https://shruwd.io/mcp` (Streamable HTTP), so there's nothing to install and
no key to store:

```bash
openclaw mcp add shruwd --url https://shruwd.io/mcp --transport streamable-http --auth oauth --oauth-scope "read write"
openclaw mcp login shruwd
openclaw mcp doctor shruwd --probe
```

`login` opens a browser. The user signs in to Shruwd and picks the workspace. Use
`--oauth-scope read` for read-only access. The user can revoke access in Shruwd under
Account → Connected apps.

### Hosted, with an API key (mcporter)

```bash
mcporter call 'https://shruwd.io/mcp.shruwd_get_workspace' --header 'Authorization=Bearer ${SHRUWD_API_KEY}' --name shruwd
```

Keep the single quotes so that mcporter reads `SHRUWD_API_KEY` from the environment, not the
shell.

### Local (stdio), pinned

```bash
openclaw mcp add shruwd --command npx --arg -y --arg shruwd-mcp@0.1.9 --env SHRUWD_API_KEY="$SHRUWD_API_KEY"
openclaw mcp doctor shruwd --probe
```

## Using it

1. Start with `shruwd_get_workspace` to see the plan, usage and existing brands.
2. New brand: `shruwd_create_brand` (needs `owner`), then `shruwd_add_prompts` and
   `shruwd_add_competitor`.
3. `shruwd_run_measurement` starts a cycle. Results arrive over the following hours, so don't
   report numbers until `shruwd_list_cycles` shows the cycle has closed.
4. Read the results with `shruwd_get_visibility`, `shruwd_get_visibility_series` and
   `shruwd_get_crawlers`. Call `shruwd_get_visibility` once per engine the brand measures and
   report each separately. Rates and share of voice come with a 95% interval and n;
   `insufficient_data` means too few answers to give a number, not zero.
5. Visibility also gives the brand's mention rate per question type (buying questions apart from
   how-to ones) and, for each tracked company, how often it's the first of them an answer names.

Nothing is hard-deleted. Archiving a brand stops scheduling and keeps its history, removing a
prompt deactivates it, and removing a competitor closes it as of now.

Full docs: https://shruwd.io/docs/api/mcp-server · Machine-readable: https://shruwd.io/llms.txt
