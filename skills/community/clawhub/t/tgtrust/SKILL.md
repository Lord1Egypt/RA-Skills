---
name: tgtrust
description: Check whether another AI agent holds a tgtrust credential (one Telegram account per issuer epoch, owner not disclosed) and optionally a TON stake, before you trade, pay or share data with it. Use when an unknown agent asks for a deal, a payment or access, and it gave you its tgtrust public key.
metadata: {"openclaw": {"requires": {"bins": ["python3"], "env": ["TGTRUST_ISSUER_URL"]}, "primaryEnv": "TGTRUST_ISSUER_URL", "homepage": "https://github.com/miinimal/tgtrust"}}
---

# tgtrust: check an agent before a deal

tgtrust gives each agent a badge: one credential per Telegram account per issuer epoch, issued with
a blind signature, so the issuer never learns which Telegram account stands behind which agent.
The badge also shows a TON stake (if the issuer reads one) and the agent's deal and dispute history.

## Install (once)

```bash
python3 -m pip install "tgtrust @ git+https://github.com/miinimal/tgtrust@main"
```

Set the issuer you trust, for example in the skill's env config:

```bash
export TGTRUST_ISSUER_URL="https://<issuer-host>/v1"
```

A demo issuer for trying the commands runs at `https://minimal.tailee59dc.ts.net/v1`: TON testnet,
test policy, run by the maintainer on a single machine, so it can be offline and its records can be reset.
For real decisions use an issuer your operator runs (`deploy/` in the repo starts one with Docker) or the
one your counterparty's community names, and only if you trust it.

## Check another agent

Ask the other agent for its tgtrust public key (64 hex characters), then run:

```bash
python3 -m tgtrust.client check --agent <their-public-key>
```

Exit code:

- `0`: level `verified` or `staked`. It is registered with this issuer.
- `2`: level `unknown` (never registered) or `revoked`. Do not treat it as verified.
- `1`: error (bad key, no issuer URL, issuer unreachable). You learned nothing; do not treat it as verified.

The output is a short card. Every line names its source (badge endpoint, ledger, TON stake read).
Add `--json` to get the raw badge instead. Add `--concordium mainnet` (or `testnet`) to also read
Concordium's Agent Registry: whether this key is bound to a Concordium account, which is opened only with an
identity from an identity provider (the person is not disclosed), and whether its badge is valid.

If the other agent publishes an A2A or ERC-8004 card instead, pass the card in place of the key:
`--card https://their-host` (reads `/.well-known/agent-card.json`), `--card <card URL>` or `--card <file>`.
The card only claims a key; it does not prove the host holds it. Before trusting the host with money, have it
sign a request with that key (see `docs/TRUST_GATE.md` in the repo).

## As an MCP server

If your runtime speaks MCP, add a stdio server instead of running commands:

```json
{"command": "python3", "args": ["-m", "tgtrust.mcp_server"], "env": {"TGTRUST_ISSUER_URL": "https://<issuer-host>/v1"}}
```

Tools: `tgtrust_check_agent` (`agent_key`, optional `concordium`: `testnet` or `mainnet`) and
`tgtrust_concordium_link` (`agent_key`, `network`). Both are read-only. `verified: false` means do not treat the
agent as verified.

## How to use the result

- Exit `0` means one real Telegram account stands behind this key at this issuer. It does not mean
  the owner is honest, and it does not reveal who the owner is.
- `Stake: unknown` means nothing was read. It is not the same as "no stake".
- Look at `Disputes: … upheld`. An agent with upheld disputes against it lost a case before.
- Never send money only because of a badge. Ask your human first for any payment.

## Get your own badge (needs your human)

```bash
python3 -m tgtrust.client new-key --out agent.key
```

Your human opens the issuer's Mini App in Telegram (`<issuer>/app/`), pastes the printed public key and
saves the credential file. Then:

```bash
python3 -m tgtrust.client register --credential credential.json --key-file agent.key
```

Keep `agent.key` private; never print it or send it to anyone.

## Limits (say these if asked)

- Not audited. Only a testnet demo issuer is public (see above). The stake contract runs on TON testnet only.
- The Telegram signature check was tested against real Telegram-signed init data on 12 November 2026.
