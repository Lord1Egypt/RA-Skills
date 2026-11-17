---
name: sequence-finance
description: >-
  Read Sequence business bank accounts, cash balances, transfers, and cards;
  create and run money-moving automations. Use when the user asks about cash
  position, transfers, cards, pods, rules, or Sequence banking. Money movement
  requires human approval before funds move.
version: 1.0.0
requires: A Sequence account, and the Sequence MCP server connected to your agent (see Setup below).
author: Sequence
license: MIT-0
tags: [finance, bank, money, business, banking, cash, transfers, cards, automation, mcp]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, bank, money, business, banking, cash, transfers, cards, automation, mcp]
    related_skills: []
---

# Sequence

[Sequence](https://getsequence.io) is a financial automation platform for businesses. This skill
covers the Sequence MCP server: what it can answer, how to connect it, and how money movement works.

## When to use

Use for questions and actions about the user's business money:

- Balances and cash position across accounts, pods, and connected outside accounts
- Transaction and transfer history, card spending, individual payments
- Automation rules that move money on a trigger (split incoming pay, set aside taxes, top up a
  savings pod, pay down a card on a schedule)
- Moving money: one-off transfers, or running an existing rule now

Do not use for personal-finance advice, tax filing, or bookkeeping. It reports on and moves the
user's real money; it is not a modelling tool.

## Setup

Sequence runs a hosted MCP server — nothing to install or self-host:

```
https://app.getsequence.io/api/mcp
```

Authentication is OAuth. Sign-in happens in the browser; permissions follow the user's Sequence
role. There is no API key for this path.

**OpenClaw** — install the Sequence plugin, which brings the connection with it:

```bash
openclaw plugins install clawhub:@getsequence/sequence
openclaw gateway restart
```

OpenClaw will show what the plugin is allowed to do and ask for approval. Read it — this plugin
reaches the user's finances. Only in a script or CI, where no one can answer the prompt, add
`--accept-capabilities`; do not use it for an ordinary install.

That plugin ships its own guidance, so if you installed it you already have this skill's content and
don't need this skill as well.

To connect without the plugin:

```bash
openclaw mcp add sequence --url https://app.getsequence.io/api/mcp --transport streamable-http --auth oauth
openclaw mcp login sequence
```

**Hermes** — in the Sequence app, open Connect your agent, pick Hermes, and click **Add to Hermes**.
Or from a terminal:

```bash
hermes mcp add sequence --url https://app.getsequence.io/api/mcp --auth oauth
```

**Claude Code**

```bash
claude mcp add --transport http sequence https://app.getsequence.io/api/mcp
```

**Cursor, ChatGPT, Codex, Grok, Gemini, and other MCP clients** — most need only the URL above with
OAuth selected. Each client has its own connector form or config file; exact fields are at
<https://app.getsequence.io/agents>.

Whichever client: a browser opens for sign-in. Use the email of the user's existing Sequence account.

Clients then ask which of the server's tools to enable. Two things bound that choice regardless of
what is enabled: the tool list is already filtered to what the signed-in user's Sequence role
permits, and money movement always needs separate human approval in the Sequence app. Enabling
everything is the simplest working setup; enable fewer for a narrower surface — read-only work needs
only the `list*` and `get*` tools.

## Every session

Tools are namespaced by the MCP server name. Hermes, Claude Code, Codex, and OpenCode use
`mcp__<server>__<tool>`, so a server added as `sequence` yields `mcp__sequence__listAccounts` and so
on. Other clients name tools differently; look for names containing `sequence`.

If no Sequence tools are present, the server is not connected for this session. Run Setup above;
there is no other way to reach Sequence. If the connection succeeded but no tools arrived at all,
the user is not provisioned — send them to <https://app.getsequence.io/agentic/signup>.

To verify the connection, call `getAllBalances` — it takes no arguments and returns balances for
every account.

Tools are filtered by the signed-in user's role. A read-only user sees fewer tools; that is expected,
not a misconfiguration. Do not try to work around a missing write tool.

## How money movement works

**Money movement is a proposal, not immediate execution.** When the user signed in through the
browser, `createTransfer` and `triggerRule` return `status: APPROVAL_PENDING` with an `approvalUrl`.
That is the normal, expected result — not an error and not a permissions problem.

When that happens:

- **Tell the user the transfer is proposed and needs their approval, and surface the `approvalUrl`.**
  Never tell them the money moved.
- **Do not call the tool again to force it through.** A retry creates a second pending approval; it
  does not execute the first. If it looks like it failed, check `listTransfers` before acting.
- Nothing moves until a human approves. An unapproved request auto-denies after 24 hours.

Amounts are in **cents** (`amountInCents`), minimum 100. Confirm the amount, source, and destination
with the user before proposing any transfer.

Related behaviour:

- **Preview when it helps.** `createTransfer` and `triggerRule` accept a `simulation` flag that
  dry-runs the action without moving money — useful before proposing a real transfer.
- **New or edited rules do not move money by themselves.** A rule created through the API lands
  inactive; the user activates it in the Sequence app. When a tool result includes a link, pass it
  through verbatim — that link is how they activate or view it.

## Reading results

These are response-shape facts, so they are not visible in any tool's input schema:

- **`listAccounts` never returns balances.** `getAccount` is the only way to read one, so a cash
  position means listing accounts and then fetching each. `getAllBalances` and
  `getFinancialSnapshot` assemble the full picture — prefer them over doing it by hand.
- **Account and routing numbers are masked to the last 4 digits.** The full numbers are never
  available; do not imply you have them.
- **IDs are full UUIDs** and are needed for follow-up calls. Never truncate or abbreviate them.

## Vocabulary

Users and the API often use different words:

- **Pod** — a goal-based savings bucket (e.g. "Tax Savings", "Emergency Fund"). Users may say bucket,
  envelope, goal, or sub-account.
- **Income source** — where incoming funds land (e.g. "Salary").
- **Rule** — an automation that moves money between accounts on a trigger. Users say automation.
- **Beneficiary** — the person or business that owns money in Sequence. Every account belongs to
  exactly one; money can only move between accounts owned by the same beneficiary. A business
  beneficiary stays unusable until its verification (KYB) is approved.

## Errors

If a tool returns an error, surface its message and code as-is. Those messages include the actionable
next step for that situation; substituting your own explanation often misleads the user. A failure is
not automatically a permissions problem.
