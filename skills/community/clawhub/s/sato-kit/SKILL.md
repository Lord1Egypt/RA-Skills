---
name: sato-kit
description: Prepare and execute onchain agent actions (chain reads, swap quotes, swaps, x402 payments) through the Sato Kit CLI with a policy pre-flight, simulation and a receipt log. Use when an agent needs to read chain state, quote or build a swap, or prepare an x402 payment and hand it to a signer only after a person has seen the summary. Fork network by default.
version: 0.1.1
compatibility: Requires Node.js 20 or later and npx. Network access to an EVM RPC (fork by default) and to the swap venue the caller chooses.
metadata:
  version: "0.1.1"
  homepage: https://satohub.ai
  openclaw:
    requires:
      bins: ["node", "npx"]
      env: []
---

# Sato Kit

Sato Kit turns an onchain action into two steps: **prepare** builds an unsigned intent, runs the
policy pre-flight and simulates it; **execute** takes only that `intent_id` and hands it to the
configured signer. The pre-flight explains refusals. The signer is what enforces limits.

Every command below prints JSON with `--json`. Exit code 0 = ok, 2 = refused by policy, 1 = error.

## Rules for the agent

1. The network is **fork** unless `policy.json` says otherwise. Do not change it to mainnet on your
   own; mainnet needs the person's explicit opt-in in their policy file.
2. Always `prepare` first. Show the person the intent's `summary`, `fee_disclosure`,
   `simulation` and `policy` verbatim.
3. Run `execute` only after the person has approved that exact `intent_id`. Never execute an intent
   you did not just show them, and never invent or edit an intent id.
4. If `prepare` returns `policy.ok: false`, report each refusal (rule, limit, observed) and stop.
   Do not retry with changed numbers to get around a rule.
5. A USD value marked `unknown` stays unknown. Do not estimate one.

## Commands

Read (no signature, no funds move):

```bash
npx -y @satohub/kit@0.1 read chain.read --input '{"chain":"base-sepolia","kind":"native_balance","address":"0x..."}' --json
npx -y @satohub/kit@0.1 read swap.quote --input '{"chain":"base","sell_token":"0x...","buy_token":"0x...","sell_amount":"1000000"}' --json
```

Prepare (builds an intent; nothing is signed):

```bash
npx -y @satohub/kit@0.1 prepare swap.prepare --input '{"chain":"base","sell_token":"0x...","buy_token":"0x...","sell_amount":"1000000","taker":"0x..."}' --json
npx -y @satohub/kit@0.1 prepare x402.prepare --input '{"url":"https://...","max_amount_base_units":"10000"}' --json
```

Execute (only after approval; takes the intent id and nothing else):

```bash
npx -y @satohub/kit@0.1 execute --intent si_... --json
```

Check the setup:

```bash
npx -y @satohub/kit@0.1 doctor --json
```

Action names accept either the ODA id (`swap.prepare`) or the tool name (`swap_prepare`).

## Configuration

- `./policy.json` (or `--policy <file>`): the `sato.policy/v1` file the pre-flight reads.
- `./.sato/`: intents, the intent key and `receipts.jsonl`. Keep `.sato/` out of version control.
- RPC: `SATO_RPC_URL_<CHAIN>` (for example `SATO_RPC_URL_BASE_SEPOLIA`) or `--rpc <url>`. Optional;
  without one the kit uses the fork endpoint.

## Swaps

Any venue is accepted. `sato` is the labelled default and its fee sentence is returned verbatim in
`fee_disclosure`, with a quote carrying no Sato fee alongside. `venue: "direct"` never contacts Sato.

## As an MCP server

`npx -y @satohub/kit@0.1 mcp` starts a local stdio MCP server with the same tools.
