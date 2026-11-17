---
id: chatgpt-apps
kind: platform
unlocks: [chatgpt-apps]
source: https://developers.openai.com/apps-sdk/deploy/submission, https://developers.openai.com/apps-sdk/app-submission-guidelines (loaded 2026-11-08)
---
Note: the docs now call these "plugins" and submission is at https://platform.openai.com/plugins ("Upload new or existing plugin") with a ZIP package; update the catalog's `submit` and the "3 starter prompts / 5+3 test cases" artifacts accordingly (the 5 positive + 3 negative is confirmed).

## Smallest version
An Agent Plugin ZIP pointing at the existing OAuth-protected remote MCP server (see mcp-remote, mcp-oauth), with listing metadata, up to three starter prompts, and 5 positive + 3 negative review cases written from the existing tool list. No UI widgets unless the product needs them.

## Scaffold
No generator on the pages loaded. ZIP root: `plugin.json` + `mcp.json` (+ optional `skills/`).

## Fields the listings check
- `plugin.json` (Agent Plugins): `name` (required), `version`, `description`, `author.name`; `extensions.com.openai.interface`: `displayName` and `shortDescription` (<=30 chars each), `longDescription` (<=4,000), `developerName`, `category`; for public MCP review `websiteURL`, `supportURL`, `privacyPolicyURL`, `termsOfServiceURL`; icons as `./` relative paths (primary icon required before submission). Codex variant: `.codex-plugin/plugin.json` with `interface`, `composerIcon`, `logo`.
- `mcp.json`: `$schema` `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`, `mcpServers.<id>: { "type": "streamable-http", "url": "https://<host>/mcp" }`. One server per plugin; stable public HTTPS; no nonempty `headers`; no `clientSecret`; protected server must not be `type: "none"`.
- Auth: OAuth only in the portal (no API-key or bearer input). Registration: registered client, Dynamic Client Registration, or Client ID Metadata Document; register the portal's callback URL with the OAuth provider; client secret entered in the portal.
- Domain verification: exact token as plain text at `https://<mcp host or parent>/.well-known/openai-apps-challenge`.
- Tools: unique names; nonempty accurate descriptions matching schema/behavior; `readOnlyHint`, `destructiveHint`, `openWorldHint` set to explicit booleans; minimal inputs.
- Review form: exactly 5 positive cases (scenario, user prompt, expected tools, expected result) + 3 negative (prompt, why not to act, expected refusal/fallback); video walkthrough URL; reviewer test account with sample data, login URL, instructions, no MFA/email/SMS codes. Starter prompts: up to 3, <=128 chars.
- Policy: published privacy policy; data minimization; suitable for ages 13-17; no ads; no trial/demo plugins; organization identity verification; owner or Apps Management Write permission to submit. `publication.countries` optional allowlist.
- After approval OpenAI scans the server daily; new tools stay unavailable until approved.

## Steps
claude: add explicit `readOnlyHint`/`destructiveHint`/`openWorldHint` to every tool; tighten descriptions
claude: write `plugin.json`, `mcp.json`, starter prompts, 5 positive + 3 negative cases from the tool list; zip it (no secrets)
claude: add the `/.well-known/openai-apps-challenge` route serving the token (after the human copies it)
human: verify organization identity in OpenAI platform settings
human: create the reviewer test account (sample data, no MFA); record the video walkthrough of all 8 cases
human: platform.openai.com/plugins -> Upload new or existing plugin; enter OAuth client details and callback URL; copy the domain token
approve: deploy the challenge route
human: wait for the tool scan, resolve Issues, fill Review details (credentials, video URL, cases), submit; choose when to publish after approval

## Verify locally
`npx @modelcontextprotocol/inspector@2.15.0` completes OAuth and lists tools with all three hints; `curl https://<host>/.well-known/openai-apps-challenge` returns only the token; run the 8 cases in ChatGPT developer mode before submitting (developer mode not described on the pages loaded, unconfirmed).
