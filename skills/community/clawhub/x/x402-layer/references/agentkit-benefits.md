# World AgentKit Benefits

Use this reference when the endpoint advertises a benefit for **verified human-backed agent wallets**.

## What this is

AgentKit helps the worker distinguish:
- normal wallets and scripts
- wallets that are registered as **human-backed agent wallets**

In Studio today, sellers can enable AgentKit benefits on **direct endpoints**:
- `free`
- `free-trial`
- `discount`

## Important scope

- This is **not** the same thing as plain seller World verification.
- This is **not** a generic discount for every browser wallet.
- This is specifically for the wallet that signs agent requests.

## Discovery

Use:

```bash
python {baseDir}/scripts/discover_marketplace.py details <slug>
```

If the listing is an endpoint and it has an AgentKit benefit, the script will surface it.

## Payment flow

Use:

```bash
python {baseDir}/scripts/pay_base.py <endpoint_url> --agentkit auto
```

Modes:
- `off`: do not attempt AgentKit
- `auto`: attempt AgentKit if the endpoint advertises it, otherwise continue normally
- `required`: fail if the wallet does not qualify for the advertised AgentKit benefit

## What the script does

1. Makes the normal request
2. Reads the `402 Payment Required` challenge
3. Checks whether the challenge includes an AgentKit extension
4. If yes, signs the AgentKit message locally with the agent wallet
5. Retries with the `agentkit` header
6. If qualified:
   - free/free-trial may return access immediately
   - discount may return a cheaper payment challenge
7. Then continues the x402 payment flow if payment is still required

## Registration guidance

To qualify, the wallet that signs agent requests must be registered in AgentBook:

```bash
npx @worldcoin/agentkit-cli register <wallet-address>
```

That registration requires a human to complete the World App verification flow.

So the correct agent behavior is:
- explain why the benefit is available
- tell the human which wallet must be registered
- ask them to complete the World flow
- retry the request after registration succeeds

## Current limitation

The Python skill supports AgentKit signing in **private-key mode**.

AWAL mode can still pay endpoints, but this skill does not currently use AWAL to generate the AgentKit proof header.

## Expected agent wording

Good:
- `This endpoint offers 20% off for verified human-backed agent wallets.`
- `Your current wallet does not appear to qualify yet. Register the signing wallet in AgentBook, complete the World App verification step, then retry.`

Bad:
- `This is free for all humans.`
- `Your browser wallet is automatically verified with World.`
