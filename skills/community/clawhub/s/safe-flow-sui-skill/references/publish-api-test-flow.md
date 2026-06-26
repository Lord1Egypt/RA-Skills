# Publish API Test Flow (Intent Producer + Agent Consumer)

This skill treats Publish API integration as a test harness for full E2E:

1. create intent from producer side,
2. let agent poll and execute once,
3. report result with `txDigest` + `walrusBlobId`.

## Required Inputs

- `publish-api-base-url` (real URL provided later by owner/operator)
- `recipient` address
- `walletId` + `sessionCapId` + `agentAddress` (from owner handoff flow)

## One Command E2E

```bash
cd .claude/skills/safe-flow-sui-skill/scripts
./test_publish_api_flow.sh \
  --publish-api-base-url <PUBLISH_API_BASE_URL> \
  --recipient <RECIPIENT_ADDRESS>
```

## What It Does Internally

1. `curl <base>/health`
2. `agent_scripts/create_intent.ts` with:
- `--agent-address`
- `--wallet-id`
- `--session-cap-id`
- `--recipient`
- `--amount-mist`
3. `agent_scripts/e2e_runner.ts --once`
4. `curl /v1/intents/<intentId>` and print final state.

## Walrus Upload Behavior

- Walrus upload is performed by SDK `executePaymentWithEvidence`.
- Successful upload stores real blob id.
- If degrade is enabled and upload fails, `fallback:<sha256>` is reported.

## Optional Auth

If your API enforces key-based write auth:

```bash
./test_publish_api_flow.sh \
  --publish-api-base-url <URL> \
  --recipient <RECIPIENT_ADDRESS> \
  --api-key <X_API_KEY>
```
