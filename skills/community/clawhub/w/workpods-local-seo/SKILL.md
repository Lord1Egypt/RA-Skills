---
name: local-seo
description: Free, open-source checker for a local business's location pages and Google Business Profile. Runs the Local SEO by WorkPods.ai CLI and MCP server to check a site against its profile (name, address, phone, LocalBusiness schema, click-to-call, map). Use when asked to audit a location page, check NAP consistency, or verify local schema before or after a deploy.
version: 1.0.2
metadata:
  openclaw:
    emoji: "📍"
    homepage: https://workpods.ai/tools/local-seo
    requires:
      bins:
        - node
        - npx
---

# Local SEO by WorkPods.ai

Local SEO audits Google Business Profiles, reviews and Maps rankings, and checks a business's
website against its profile. It is free and open source (Apache-2.0). Made by
[WorkPods.ai](https://workpods.ai), an AI SEO agency.

- Tool page: https://workpods.ai/tools/local-seo
- Source: https://github.com/WorkPodsAgents/local-seo
- npm: `@workpods/local-seo` (Node.js 22 or later)

Nothing goes through a WorkPods.ai server and no account is needed.

## Setup

1. Make sure Node.js 22 or later is installed (`node --version`).
2. The website check below runs in Node with no browser. The profile audit (39 checks), reviews,
   posts, Maps scans and geo-grids need the Chrome extension from
   https://workpods.ai/tools/local-seo, paired with the bridge: run
   `npx -y @workpods/local-seo pair` and enter the code under **Settings → Agent connection** in
   the extension's side panel.
3. To use it as an MCP server, add this to your MCP client:

   ```json
   { "mcpServers": { "local-seo": { "command": "npx", "args": ["-y", "@workpods/local-seo", "mcp"] } } }
   ```

## Check a website against the profile

```bash
npx -y @workpods/local-seo audit-website https://example.com/locations/west-nyack \
  --name "Nyack Plumbing Co" --phone "+1 845-555-0100" --address "250 W Nyack Rd, West Nyack, NY"
```

Give the facts exactly as they appear on the Business Profile. `--name` is required; a fact left
out is not compared. The command fetches the page without running JavaScript and checks:

- the page shows the same name, address and phone as the profile;
- it has LocalBusiness schema with address, telephone, geo and opening hours;
- the phone number is a click-to-call link;
- it embeds a Google map.

The hours check needs the profile's hours, which only the extension reads, so the CLI reports it
as untested. Add `--json` for structured output.

Exit codes: `0` no high-severity check fails, `1` the name, address or phone differ from the
profile, `2` the command was wrong.

## How to report

- Lead with mismatches in name, address or phone; they matter most.
- Quote the exact text found on the page next to the profile value.
- Nothing here writes to Google. Suggested fixes are for the owner to make.

Full documentation: https://github.com/WorkPodsAgents/local-seo/blob/main/docs/command-line.md
