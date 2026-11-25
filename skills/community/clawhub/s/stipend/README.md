# stipend.sh

A non-custodial USDC wallet on Base that an AI agent installs by itself, with
spending limits enforced below the instruction layer.

```
pip install eth-account && curl -sL stipend.sh/install | sh
```

This is the source of the package that installer fetches. It is published so
that the claims made for it can be checked rather than believed.

It ships an **MCP (Model Context Protocol) server** — `stipend mcp` — exposing
seven tools over stdio, so an agent can hold and spend money through the tool
interface it already has. See [MCP server](#mcp-server) below.

## The claim worth checking

The failure that matters for an agent holding money is not a stolen key. It is a
correctly signed transaction it was argued into.

Almost every defence against that lives in the instruction layer — a system
prompt saying "do not send funds to unverified addresses." That is a suggestion
to a model, sitting in the same context window as the text attacking it.

In here the limits are not advice. They are code that a transaction passes
through on its way to being signed, and no wording in any context window reaches
them.

**Start at [`stipend/policy.py`](stipend/policy.py).** It is about three hundred
lines and it is the whole argument.

## The three controls

| control | what it does |
|---|---|
| per-transaction and daily caps | a ceiling that no instruction can raise |
| one-time approvals | authorise a single payment — bound to that recipient, that amount, expiring, single use — instead of raising a cap |
| new-destination confirmation | the first payment to any address you have never paid needs confirming, whatever the size |

The second is the one people get wrong. Raising a cap to afford one purchase
weakens every future payment to everyone, which is precisely what an attacker
asks for. Authorise the payment, not the capability.

The third is what stops a drain by many small payments that each sit under the
threshold. An attacker's address is, by definition, one you have never paid.

And if you turn on an allowlist, it is absolute. Funds reach nothing else — not
with a confirmation, not with an approval, not with any instruction from
anywhere.

## MCP server

The wallet is also a Model Context Protocol (MCP) server, so an agent can use it
through the tool interface it already has rather than by shelling out.

```
stipend mcp
```

It speaks JSON-RPC over stdin and stdout — the MCP stdio transport. Your MCP
client spawns the process; nothing listens on a port and nothing is exposed to a
network.

In a client's config that looks like:

```json
{
  "mcpServers": {
    "stipend": {
      "command": "stipend",
      "args": ["mcp"]
    }
  }
}
```

### The tools

| tool | what it does |
|---|---|
| `stipend_address` | the wallet's address, so money can reach you whether or not you are running |
| `stipend_balance` | USDC held, native currency held, spent today, and the daily limit |
| `stipend_check` | would this payment be allowed? Answers without sending anything |
| `stipend_pay` | send USDC, subject to every limit below |
| `stipend_earnings` | read incoming payments off the network and record them |
| `stipend_report` | earned against spent, by category, with runway in days |
| `stipend_recover` | what is outstanding, and whose job each item is |

Every one of them goes through the same `policy.check` gate the command line
uses, so the caps, the allowlist and the new-destination confirmation apply
identically. There is no path here that moves money without them.

`stipend_check` exists so an agent can ask "would this be allowed?" before it
offers to pay for something, turning a refusal into an answer rather than a
failure.

### What it deliberately does not expose

No tool reads, exports or derives the private key. No tool changes a spending
limit or the allowlist. No tool creates or overwrites a wallet.

An MCP tool is callable by a model that is reading untrusted text, and raising a
cap is exactly what an attacker would ask for — so it is not on the menu at all.
Configuration changes stay at the command line, where a human is present.

### Why it is not hosted

Every registry would prefer a URL, and we will not publish one. A hosted wallet
server means the key lives on somebody else's machine — ours — and the whole
claim of this package is that it does not. This runs beside the keystore, under
the same user, and the key never moves.

## Run its own tests

No network, no funds, no wallet of yours touched:

```
python -m stipend selftest
```

219 checks covering address validation, amount arithmetic, every policy branch,
the allowlist, the daily cap, destination trust and its expiry, keystore
encryption, ERC-20 encoding, x402 requirement selection, EIP-3009 signing, the
ledger, and exactly what telemetry would send.

## What we would rather have

Someone to break it.

If you can construct an injection that moves money past the checks in
`policy.py`, open an issue. We would rather hear it from you than from someone
who is not being polite about it.

## Honest limits

- Not independently audited.
- x402 interoperability is verified against our own endpoint, not third-party
  merchants.
- The key is generated on your machine and never transmitted — which also means
  nobody can recover it for you, including us.
- Keep the balance small. It is a working float, not savings.

## Links

- [stipend.sh](https://stipend.sh) — the site, which serves plain text to agents
  and a page to browsers at the same URL
- [stipend.sh/skill.md](https://stipend.sh/skill.md) — written for agents
- [stipend.sh/for-your-human](https://stipend.sh/for-your-human) — written for
  the person who pays
- [kina](https://github.com/stipend-sh/kina) — a small language some of this
  reads and writes

## Licence

Apache-2.0. See [LICENSE](LICENSE).

Built by the Stipend dev team. FelixTrade.ai Pty Ltd, Australia.
