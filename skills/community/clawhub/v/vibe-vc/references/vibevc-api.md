# Vibe VC API + workflow reference

Canonical: https://vibevc.md/skill.md

## Base URLs

- Primary: https://vibevc.md
- Fallback: https://the-vibe-vc.fly.dev

## Endpoints

### Register project

`POST /api/register`

Body fields:
- projectName (string, required)
- creatorName (string, required)
- oneliner (string, required)
- repositoryUrl (url, required)
- email (email, required)
- telegram (string, optional)
- discord (string, optional)
- mcpWorkspace (string, optional)
- activityLevel: active | steady | quiet
- repoAccess: invite-diff-fund | guest-repository | mcp-only
- analyticsConnected (boolean)
- stripeConnected (boolean)

Result notes:
- Returns `humanVerificationInstructions` to be relayed to a human.

Human verification post templates (use the real project name):
- LinkedIn: I just submitted my vibe-coded project '[project name]' to @the-vibe-vc. They're a micro VC investing only in vibe-coded apps
- X: I just submitted my vibe-coded project '[project name]' to @thevibevc. They're a micro VC investing only in vibe-coded apps. Check out https://vibevc.md/

LinkedIn note: the human should manually type `@the-vibe-vc` in the composer so LinkedIn turns it into a company mention.

### Connect integration

`POST /api/integrations/connect`

Body fields:
- projectId (integer, optional)
- provider: github | gitlab | bitbucket | lovable | mcp | google-analytics | stripe | other
- connectionKind: repository | workspace | analytics | billing
- accessLevel: read-only | guest | pull-request | webhook
- repositoryUrl (url, optional)
- metadata (string, optional; notes or JSON)

TEASER.md note:
- TEASER.md must never contain secrets or personal/sensitive data (private emails, phone numbers, addresses, API keys, tokens, etc.).

### Subscribe newsletter

`POST /api/newsletter`

Body fields:
- name (string, optional)
- email (email, required)
- source (string, optional)

### Contact limited partner

`POST /api/contact`

Body fields:
- name (string, required)
- email (email, required)
- firm (string, optional)
- location (string, optional)
- checkSize (string, optional)
- thesis (string, optional)
- message (string, required)

## MCP endpoint (FYI)

- Discovery: GET /.well-known/mcp.json
- JSON-RPC: POST /mcp
