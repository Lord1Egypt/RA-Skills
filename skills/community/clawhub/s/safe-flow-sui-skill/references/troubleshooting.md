# Troubleshooting

## `sui CLI not found`

- Install Sui CLI: <https://docs.sui.io/guides/developer/getting-started/sui-install>
- Verify:

```bash
sui client envs
```

## `No active Sui address found`

Create one and set active:

```bash
sui client new-address ed25519
sui client active-address
```

## `Publish API URL is invalid or unreachable`

Default endpoint:

- `https://producer.safeflow.space`

If your deployment uses another domain, pass:

- `--publish-api-base-url <YOUR_API_URL>`

## `Walrus blob id is fallback:*`

This means upload degraded. Verify:

- `WALRUS_PUBLISHER_URL=https://publisher.walrus-testnet.walrus.space`
- `WALRUS_AGGREGATOR_URL=https://aggregator.walrus-testnet.walrus.space`
- network connectivity to both endpoints.

## `No pending intent found` in runner

Expected if queue is empty. Create one:

```bash
cd agent_scripts
npx tsx create_intent.ts --agent-address <AGENT> --wallet-id <WALLET> --session-cap-id <CAP> --recipient <RECIPIENT>
```

## `Cannot switch to agent address`

Agent key may be missing in local keystore. Re-bootstrap:

```bash
cd .claude/skills/safe-flow-sui-skill/scripts
./bootstrap_owner_handoff.sh --force-new-agent
```
