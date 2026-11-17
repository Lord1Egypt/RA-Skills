# Getting started with the Viral Outliers API & MCP server

Follow these steps in order. Steps 0 and the pricing lookup need no account at all. Connecting Claude.ai or ChatGPT? You only need an account and credits (Steps 1 and 3), then Step 5: they sign in instead of using a key.

## Step 0: try it without an account
```
curl https://viraloutliers.com/api/v1/trending
curl https://viraloutliers.com/api/v1/pricing
```
Both are free and unauthenticated: a live sample of the outlier feed, and the machine-readable price list.

## Step 1: create a free account (or skip it)
Sign up at https://viraloutliers.com/sign-up. A free account is enough to buy credits and use the API; a subscription additionally includes monthly credits (Basic Plan 250, Pro Plan 750, Agency Plan 3.000).
Shortcut for agents and one-off users: pay $15 for 1,500 credits at https://viraloutliers.com/api-access and an API key is shown right after checkout (an account is created for the email you pay with), which covers Steps 1 to 3 in one click. Any billable call made without a key returns HTTP 402 payment_required carrying that same link in error.payment.checkoutUrl.

## Step 2: create an API key
Go to https://viraloutliers.com/settings?tab=api-keys and create a key. It starts with so_live_ and is shown ONCE, so store it immediately. You can revoke and rotate keys on the same page.

## Step 3: add credits
On the same API Keys tab, buy a one-time pack (1.500 credits for $15, 4.200 credits for $39, 12.000 credits for $99) or subscribe for a monthly allowance. 1 credit = $0.01. Billing is prepaid with a hard stop at zero: no surprise bills, ever. Credits included with a subscription are valid until the end of the billing period they come with and do not roll over (a yearly plan's credits last the year); purchased credits are valid for 24 months; the credits that expire soonest are spent first.

## Step 4: make your first REST call
```
curl -X POST https://viraloutliers.com/api/v1/search/content \
  -H "Authorization: Bearer so_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "home workout", "platforms": ["tiktok"], "minOutlierScore": 5}'
```
Every billable response includes X-Credits-Charged and X-Credits-Balance headers, so you can track spend per call.

Or use the official CLI (npm package viral-outliers, Node 20+; one command per skill, JSON output, --wait for async jobs):
```
npx viral-outliers login --key so_live_YOUR_KEY
npx viral-outliers search-outliers --query "home workout" --platforms tiktok --min-outlier-score 5
```
CLI docs: https://viraloutliers.com/docs/cli

## Step 5: connect an AI agent via MCP
There are two ways in: sign in with your Viral Outliers account (OAuth, no key to copy) on the sign-in URL, or send an API key on the key URL. Both reach the same tools and spend the same credits.

In Claude.ai or ChatGPT, add a custom connector with the URL https://viraloutliers.com/api/mcp/oauth, then sign in and approve. Claude.ai and ChatGPT cannot send an API key header, so this is the way in for them. You can disconnect the app at any time on https://viraloutliers.com/settings?tab=api-keys, under Connected apps.

In Claude Code, add the sign-in URL, then run /mcp inside Claude Code and choose Authenticate:
```
claude mcp add --transport http viral-outliers https://viraloutliers.com/api/mcp/oauth
```
Or use an API key:
```
claude mcp add --transport http viral-outliers https://viraloutliers.com/api/mcp \
  --header "Authorization: Bearer so_live_YOUR_KEY"
```
The server is listed on the official MCP registry as com.viraloutliers/viral-outliers.

In Cursor, add the server to ~/.cursor/mcp.json (globally) or .cursor/mcp.json (one project). With a key:
```
{
  "mcpServers": {
    "viral-outliers": {
      "url": "https://viraloutliers.com/api/mcp",
      "headers": {
        "Authorization": "Bearer so_live_YOUR_KEY"
      }
    }
  }
}
```
Or set the url to https://viraloutliers.com/api/mcp/oauth with no headers, and Cursor asks you to sign in.
Cursor can also install it in one click from the plugin listing, and without a key the free tools still work while a billable tool answers with a payment link.

In OpenClaw (key in the VIRAL_OUTLIERS_API_KEY environment variable):
```
openclaw mcp add viral-outliers --url https://viraloutliers.com/api/mcp --transport streamable-http --header "Authorization=Bearer ${VIRAL_OUTLIERS_API_KEY}"
```
In Hermes Agent, add to config.yaml:
```
mcp_servers:
  viral-outliers:
    url: "https://viraloutliers.com/api/mcp"
    headers:
      Authorization: "Bearer ${VIRAL_OUTLIERS_API_KEY}"
```
A ready-made agent skill for this workflow: OpenClaw users run `openclaw skills install @MatsClaes2/viral-outliers`; Hermes users run `hermes skills search viral outliers`; it is also discoverable at https://viraloutliers.com/.well-known/skills/index.json. Shell-native agents (Claude Code, CI) can use the CLI instead: `npm i -g viral-outliers` (docs at https://viraloutliers.com/docs/cli).

## Step 6: run async work (crawls, transcripts, remixes)
Async skills charge on queueing and return a jobRef. Poll GET /api/v1/jobs/{jobRef} (free) every 10-30 seconds; when completed, fetch the result (transcripts and visual analyses land on GET /api/v1/posts/{postId}). Failed jobs refund automatically.

## Step 7: go further
- Full skill table and per-skill docs: https://viraloutliers.com/docs
- OpenAPI spec: https://viraloutliers.com/openapi.json
- Machine-readable site summary: https://viraloutliers.com/llms.txt
- On insufficient_credits (HTTP 402): call create_topup_link (POST /api/v1/credits/topup, free) for a payment link to hand the account owner. On payment_required (HTTP 402, no key sent): hand the user error.payment.checkoutUrl; paying it yields a key without an account.
- Found a bug? report_issue (POST /api/v1/feedback) is free.