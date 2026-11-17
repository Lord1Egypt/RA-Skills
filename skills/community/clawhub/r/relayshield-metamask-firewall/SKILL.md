---
name: relayshield-metamask-firewall
description: "Use when the user asks anything about screening a MetaMask Agent Wallet action before it executes, protecting an agent that trades, swaps, bridges, or pays through the MetaMask `mm` CLI or a MetaMask MCP server, or routing MetaMask agent traffic through the RelayShield MCP Proxy Firewall. Single entry point for RelayShield screening of MetaMask agent write calls: pre-payment counterparty screening, payTo pin checks, and the hosted or self-hosted Firewall proxy. Screening is advice and enforcement at the tool call: it never replaces the human's approval, and it never moves funds."
license: MIT
metadata:
  author: relayshield
  version: "0.1.0"
---

# RelayShield MCP Proxy Firewall for MetaMask Agent Wallet

DRAFT skill entry, prepared 2026-11-10 for Andrew's review. Not submitted
to MetaMask and not published. It follows the shape of the MetaMask
agent-skills SKILL.md at github.com/MetaMask/agent-skills: YAML frontmatter
with name, description, license, and metadata, then detection, onboarding,
a routing table, configuration, and install steps.

Status notes for the reviewer, remove before publishing:
- The self-hosted proxy path below is live today (same proxy as the
  Coinbase Wallet MCP skill). The hosted proxy endpoint is in build, not
  live yet: do not publish the hosted-proxy section until the hosted
  endpoint is deployed and verified.
- The MetaMask MCP surface named below is the Embedded Wallets MCP server
  at https://mcp.web3auth.io, per MetaMask docs. Verify its tool surface
  and URL on the live docs before publishing.

## Name

RelayShield MCP Proxy Firewall for MetaMask Agent Wallet

## Description

Screens a MetaMask agent's write calls against RelayShield's live
threat-intelligence corpus before they execute. Two paths, same corpus:

1. Pre-payment screen (lightweight, works today with the `mm` CLI).
   Before the agent runs any `mm` write command, it screens the recipient
   with RelayShield's x402 checks: counterparty-screen ($0.10, corpus
   first, GoPlus failover, citations) and pin-check ($0.02, payTo pin
   against the tenant's pinned payee). A HIGH verdict means do not pay.
2. Firewall proxy (full screening). The agent's MCP client connects to
   the RelayShield proxy instead of connecting to the MetaMask MCP server
   directly. The proxy screens each wallet write tool call against 139
   monitored Telegram marketplaces, 800K+ indicators, and 10.9M citations,
   plus the tenant's intent binding, including the known recipients list.
   A call the corpus flags is flagged or blocked at the tool call, before
   it reaches the wallet.

Human approval still applies on top of everything here. The Firewall never
approves a payment on the human's behalf, and it never moves funds.

## Detection

Check how the agent reaches MetaMask before doing real work.

- If the agent runs the `mm` CLI directly, there is no proxy screening.
  Use the pre-payment screen path in the routing table below.
- If the agent's MCP client points at a RelayShield proxy URL (a hosted
  `<tenant-id>.proxy.relayshield.net` URL, or `http://localhost:8090/`
  when the proxy runs on the same host), Firewall screening is on.
- If the agent's MCP client points at the MetaMask MCP server directly,
  there is no Firewall screening. Route it through the proxy instead.
- If no MetaMask tool is callable at all, MetaMask Agent Wallet is not
  installed: direct the user to the MetaMask Agent Wallet quickstart at
  https://docs.metamask.io/agent-wallet/quickstart/ and stop.

## Onboarding

Keep it short. Do this once per session, before doing real work:

1. Briefly mention what is available, one or two sentences. The agent's
   MetaMask calls run through the RelayShield Firewall, which screens
   transfers, swaps, bridges, perpetuals, prediction orders, and earn
   deposits against a live threat-intelligence corpus and the tenant's
   intent binding before they execute. Reads such as balance checks pass
   through.
2. Show this disclaimer verbatim before proceeding:

   > RelayShield screens MetaMask tool calls against its
   > threat-intelligence corpus and your intent binding. Screening is
   > advice and enforcement at the tool call: it does not replace your
   > approval. Every write action still needs your approval, and nothing
   > moves until you approve it. Transactions are irreversible, always
   > review before approving.

3. Do not volunteer a wallet dump up front. Fetch address and balance
   only when the user asks, or when a pending operation actually needs
   the address.

## Command routing

Match the user's intent to a command, screen first, then run the command.
Screening always comes before execution, never after. If the screen returns
HIGH / do_not_pay, stop and report the flag and the citations to the human.
Do not retry the same call, do not route around the screen.

| User intent | Screen first | Then run |
| --- | --- | --- |
| Transfer native tokens or ERC-20 tokens | counterparty-screen on the recipient, pin-check if a pin exists for the seller | `mm transfer` |
| Get a swap or bridge quote | counterparty-screen on the recipient and the token contract | `mm swap quote` |
| Execute a token swap or bridge | counterparty-screen on the recipient and the token contract | `mm swap execute` |
| Open a perpetual position | counterparty-screen on the venue and the collateral token | `mm perps open` |
| Place a prediction market order | counterparty-screen on the market contract | `mm predict place` |
| Supply tokens to an earn vault | counterparty-screen on the vault contract | `mm earn supply` |
| Pay an HTTP 402 / x402 paywalled request | counterparty-screen on the payTo, pin-check if a pin exists | `python3 scripts/x402_pay.py` (per the MetaMask agent-skills x402 reference) |
| Check a balance, list transactions, get prices | None. Reads pass through. | `mm wallet balance`, `mm tx history`, `mm price ...` |

When the agent works through the Firewall proxy instead of the `mm` CLI,
the proxy does the screening at the tool call and the routing table above
does not apply: the agent calls the MCP tools normally and the proxy flags
or blocks. The x402 pre-payment screens are still available as an extra
check before a high-value call.

### The x402 screens

Both are POST endpoints on https://api.relayshield.net, paid in USDC on
Base, and payable by a MetaMask agent through the x402 flow the MetaMask
skill already documents.

- POST /v1/payg/counterparty-screen, $0.10. Corpus first (DynamoDB
  relayshield_intel_iocs), auto failover to GoPlus on a corpus miss.
  Corpus hit with a malware or scam-kit family is HIGH / do_not_pay.
  Bare corpus hit is MEDIUM / review. GoPlus sanctions or 2+ combined
  flags is HIGH / do_not_pay. Clean is LOW / proceed. UNKNOWN / review
  only when both corpus and GoPlus fail to produce a verdict. Citations
  included, capped at 5, ordered by confidence, with first seen, last
  seen, and sighting count.
- POST /v1/payg/pin-check, $0.02. Checks the payTo against the tenant's
  pinned payee for that seller. PIN_OK is LOW / proceed. PIN_MISMATCH is
  HIGH / do_not_pay (or MEDIUM / review if the tenant set step-up mode).
  NO_PIN is UNKNOWN / review. Pins are set with POST /v1/payg/pin (free,
  API-key auth). Re-pin is a new POST /v1/payg/pin, never automatic.

## Configuration

### Path 1: pre-payment screen with the `mm` CLI (works today)

No proxy needed. The agent needs a RelayShield API key for the x402
checks (payable per call) or an API key for the free pin endpoint. The
`mm` CLI itself is installed with
`npm install -g @metamask/agent-wallet@latest`, and its own skill is
installed with `npx skills add MetaMask/agent-skills`.

### Path 2: Firewall proxy (full tool-call screening)

The agent's MCP client connects to the RelayShield proxy, and the proxy
forwards clean calls to the MetaMask MCP server. Two values:

1. Upstream. The proxy needs `MCP_PROXY_UPSTREAM` set to the MetaMask
   MCP server:
   `MCP_PROXY_UPSTREAM=https://mcp.web3auth.io`
2. Client URL. The agent's MCP client points at the proxy, not at the
   MetaMask MCP server directly. Hosted: the per-tenant URL from the
   RelayShield console, `<tenant-id>.proxy.relayshield.net`. Self-hosted:
   `http://localhost:8090/` when the proxy runs on the same host (the
   proxy listens on port 8090 by default, serves JSON-RPC 2.0 over HTTP
   at the root path, and forwards to the upstream).

Example client configuration (Claude Code style, adjust for your harness):

```json
{
  "mcpServers": {
    "metamask": {
      "url": "https://<tenant-id>.proxy.relayshield.net/",
      "transport": "http"
    }
  }
}
```

The proxy also needs a RelayShield API key for deeper screening
(`RELAYSHIELD_API_KEY`). The proxy's own health endpoint is
`/_rs/health` and its dashboard is `/_rs/dashboard` on the same host
and port.

Screening rules, all from the proxy's verified defaults: block levels are
high and medium by default, unknown never blocks. If the screening call
times out (5 seconds by default), the call is allowed through and logged
(fail-open), so a screening outage never blocks a legitimate payment. Tool
results are also screened for poisoned content, and OAuth URLs are validated
against known identity providers.

Policy is per tenant. Policy 1, bound actions only, and Policy 2, step-up
for high-risk actions, apply here the same as anywhere else in the
Firewall. The known-recipients list is durable and survives restarts. A
recipient not on the tenant's durable known-recipients list needs step-up,
even if the binding allows it.

## Example: a flagged call

The agent prepares a transfer of 25 USDC to an address the corpus lists as
linked to a scam-kit family. The agent screens it first with
counterparty-screen. The verdict comes back HIGH / do_not_pay with the
corpus sightings (first seen, last seen, sighting count). The agent stops,
reports the flag and the citations to the human, and never runs
`mm transfer`. If the same address were clean, the screen would return LOW
/ proceed, the agent would run the transfer, and the human would still
approve it before anything moves. Through the proxy path, the same call is
blocked at the tool call and never reaches the MetaMask MCP server, so no
approval is ever issued for it.

## Pricing and how to get it

The Firewall is a subscription product. There is no pay-as-you-go Firewall.
A wallet-agent user gets it through the direct subscription: $49 per month
for a single-tenant SMB, 20,000 screened calls included, $0.002 per call
above that. MSPs and distributors use the $69 per-org per-month plan, one
subscription per client org. An appliance license is available for
self-hosted deployments on Vultr, DigitalOcean, and OpenNebula. The x402
pre-payment screens are pay-as-you-go instead: counterparty-screen $0.10
per call, pin-check $0.02 per call. Get started at
https://api.relayshield.net/developers, or email
support@relayshield.net.

## Limits, stated plainly

- The Firewall does not replace human approval. Every write still needs
  the human to approve it.
- There is no pay-as-you-go Firewall. A per-call Firewall only comes with
  a future agent-to-agent scenario; for now there is always a human behind
  the agent, so the subscription is the model.
- Unknown never blocks. A call the corpus has no verdict for passes
  through and relies on human approval.
- A screening timeout fails open (the call is allowed and logged), so a
  screening outage never blocks a legitimate payment.
- The Firewall screens MCP protocol traffic. It does not sandbox app UI
  code or enforce iframe isolation in MCP client apps.
- MetaMask Agent Wallet has its own Guard Mode, allowlists, and outflow
  limits. RelayShield screening is an additional layer, not a replacement
  for them.

## Install

Planned repo layout, mirroring MetaMask's agent-skills repo and the
Onchain Bridges third-party precedent (github.com/onchainbridges/agent-skills):

```text
relayshield/agent-skills
├── skills/
│   └── relayshield-metamask-firewall/
│       └── SKILL.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
└── README.md
```

Install as a skill (once the repo is public):

```bash
npx skills add relayshield/agent-skills
```

Install as a Claude Code plugin (once the repo is public):

```bash
claude plugin marketplace add relayshield/agent-skills
claude plugin install relayshield-metamask-firewall@relayshield
```

Cursor: open Customize, Plugins, Add from Git:
`https://github.com/relayshield/agent-skills`, then enable
relayshield-metamask-firewall.

Also listable on the OpenClaw Skills Registry (ClawHub), Vercel skills.sh,
and agentskill.sh once the repo is public.
