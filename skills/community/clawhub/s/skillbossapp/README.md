# skillboss-openclaw-plugin

> **Give your OpenClaw agent access to 700+ AI tools via one wallet.**
> Web scraping, web search, image/video/audio generation, email, TTS, and
> 100+ LLMs. One API key. Audit trail included.

[SkillBoss](https://www.skillboss.co) is the wallet and shopping rail for AI
agents. This is the official OpenClaw plugin.

## Install

```bash
openclaw plugins install skillboss-openclaw-plugin
```

OpenClaw accepts npm specs only (git / URL / file are rejected).

## Configure

1. Grab an API key at <https://www.skillboss.co/console>. First top-up of $25
   grants a $5 bonus ($30 usable).
2. Add to your OpenClaw config:

```json5
{
  plugins: {
    entries: {
      skillboss: {
        config: {
          apiKey: "sk_skillboss_...",
          agentName: "openclaw-main",
          maxCostPerCallUsd: 2.0,
          defaultChatModel: "claude-4-6-sonnet",
          defaultImageModel: "vertex/gemini-3-pro-image-preview"
        }
      }
    }
  },
  agents: {
    list: [
      {
        id: "main",
        tools: {
          // Enable all SkillBoss tools for this agent
          allow: ["skillboss"]
        }
      }
    ]
  }
}
```

3. Restart the OpenClaw gateway.

## Tools

This plugin registers the following tools:

| Tool | Description |
| --- | --- |
| `skillboss_run` | Generic dispatcher — call any skill by id |
| `skillboss_catalog_search` | Natural-language search over the 700+ SkillBoss catalog |
| `skillboss_get_balance` | Check the current wallet balance |
| `skillboss_web_scrape` | Scrape a web page (Firecrawl) |
| `skillboss_web_search` | Live web search (Perplexity / Brave / Exa) |
| `skillboss_send_email` | Send an email (AWS SES) |
| `skillboss_generate_image` | Generate an image (Gemini 3 Pro Image by default) |
| `skillboss_chat` | Call any LLM (Claude, GPT, Gemini, DeepSeek, Kimi, ...) |

Need a skill that isn't in this list? Use `skillboss_catalog_search` to find it,
then pass its id to `skillboss_run`.

## How it works

Every tool call hits `POST https://api.skillboss.co/v1/run` with your API key.
SkillBoss:

1. Validates the request against your wallet balance + `max_cost_per_call_usd` limit.
2. Routes to the underlying vendor (Firecrawl, OpenAI, Anthropic, Imagen, etc).
3. Returns the vendor response plus a **signed receipt** with `cost_usd`,
   `wallet_balance_after_usd`, and a `X-Agent-Name` audit tag.

The plugin surfaces the cost and balance in the tool result `meta` so your
agent can track spend.

## Agent Shopping Protocol

This plugin implements [Agent Shopping Protocol v0.1](https://www.skillboss.co/docs/agent-shopping-protocol).
That means:

- Every call goes through `/v1/run` with `X-Payment-Protocol: skillboss_wallet`.
- Every product the plugin can reach is discoverable at
  <https://www.skillboss.co/api/catalog> as machine JSON.
- Every product page has a sibling `/product.json` for single-product
  lookups.
- Retry semantics are declared per product in the catalog (`retry_policy`
  field).

## Safety + audit

- `X-Agent-Name` header tags every call, so your spend shows up in
  <https://www.skillboss.co/admin/analytics> (for your account).
- Server-side `max_cost_per_call_usd` limit. Calls that would exceed it are
  rejected with `402`.
- Signed JWT receipts (ASP v0.2) let you reconcile against an auditor without
  trusting the SkillBoss dashboard.

## Development

```bash
pnpm install
pnpm run build      # compile to dist/
pnpm run typecheck  # strict typecheck
```

The plugin lives under `packages/openclaw-plugin/` in the
[SkillBoss monorepo](https://github.com/SkillBoss-AI/skillboss).

## License

MIT — see [LICENSE](./LICENSE).

## Links

- Website: <https://www.skillboss.co>
- Agent Shopping Protocol spec: <https://www.skillboss.co/docs/agent-shopping-protocol>
- Catalog JSON: <https://www.skillboss.co/api/catalog>
- OpenClaw docs: <https://docs.openclaw.ai>
- Support: <support@skillboss.co>
