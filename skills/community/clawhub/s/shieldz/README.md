# Shieldz skill for OpenClaw

Accept crypto payments from your [OpenClaw](https://github.com/openclaw/openclaw)
agent with **zero setup** — no account, no API key. Text your agent a wallet
address and get a live payment link back. Non-custodial: funds settle straight to
the address you name.

## Install

**From ClawHub:**

```
claw skill add @shieldz/mcp
```

**Or manually:** copy `SKILL.md` into your OpenClaw skills directory
(`~/.openclaw/skills/shieldz/SKILL.md`) and restart the agent.

## What it does

- `create_payment_link` — a one-time, fixed-amount checkout.
- `create_tip_jar` — a reusable "pay what you want" page.
- `get_account_status` — read paid/pending totals back out (great on a heartbeat).

The skill calls the keyless Shieldz REST API directly (works everywhere), and can
also use the remote MCP server at `https://shieldz.cash/mcp`.

Every link is OFAC sanctions-screened and rate-limited. See
[shieldz.cash/agents](https://shieldz.cash/agents) for the full picture.

## License

MIT © Shieldz
