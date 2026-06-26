# Parker's TODO ... Memory Crystal Cloud

**Updated:** 2026-02-28
**Status:** Code complete. Needs deploy + connect.

---

## Deploy (do these in order)

- [ ] Merge PR #10 on GitHub (`mini/dev` -> `main`)
- [ ] Create D1 database:
  ```bash
  cd cloud && npx wrangler d1 create memory-crystal-cloud
  ```
- [ ] Paste the `database_id` into `cloud/wrangler.toml` (line 12)
- [ ] Run remote migrations:
  ```bash
  npm run cloud:db:migrate:remote
  ```
- [ ] Set three secrets:
  ```bash
  cd cloud
  npx wrangler secret put CRYSTAL_RELAY_KEY
  # paste the same base64 key the poller uses (check ~/.openclaw/secrets/)

  npx wrangler secret put OAUTH_SIGNING_SECRET
  # generate: openssl rand -hex 32

  npx wrangler secret put OPENAI_API_KEY
  # from 1Password (same key as local)
  ```
- [ ] Deploy cloud Worker:
  ```bash
  npm run cloud:deploy
  ```
- [ ] Redeploy relay Worker (it needs the new `chatgpt` channels):
  ```bash
  npm run build:worker
  npx wrangler deploy --config wrangler.toml
  ```
- [ ] Run `wip-release minor --notes="Cloud MCP server for ChatGPT + Claude"`

## Verify

- [ ] Health check: `curl https://memory-crystal-cloud.<your-subdomain>.workers.dev/health`
- [ ] OAuth discovery: `curl .../.well-known/oauth-authorization-server`
- [ ] Poller is running in `--watch` mode (picks up cloud drops every 2 min)

## Connect ChatGPT

- [ ] Open ChatGPT > Settings > Developer Mode (or Apps)
- [ ] Add MCP server with the cloud Worker URL
- [ ] Go through OAuth consent (enter your email)
- [ ] Test: "Remember that I prefer dark mode"
- [ ] Test: have a normal conversation, then check Mini for JSONL transcripts
- [ ] Verify: `crystal search "dark mode"` finds it on the Mini

## Connect Claude

- [ ] Open claude.ai > Settings > Connectors
- [ ] Add remote MCP server with same Worker URL
- [ ] Go through OAuth consent
- [ ] Test same as ChatGPT
- [ ] Also test from Claude iOS and Claude macOS apps

## When Ready to Go Public

- [ ] Write real privacy policy (replace placeholder at `/docs/privacy`)
- [ ] Write real security disclosure (replace placeholder at `/docs/security`)
- [ ] Write terms of service
- [ ] Submit to ChatGPT Apps Directory
- [ ] Submit to Anthropic Connectors Directory
- [ ] Developer verification with OpenAI
- [ ] Developer verification with Anthropic
