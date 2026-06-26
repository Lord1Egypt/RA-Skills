# Agent Registry and Reputation (ERC-8004 / Solana-8004)

Use this reference when the user asks to register, discover, manage, or rate an ERC-8004/Solana-8004 agent.

## Registration

Script:

```bash
python {baseDir}/scripts/list_my_endpoints.py

python {baseDir}/scripts/register_agent.py \
  "Agent Name" \
  "Agent description" \
  --network baseSepolia \
  --image https://example.com/agent.png \
  --version 1.10.0 \
  --tag finance \
  --tag automation \
  --endpoint-id <ENDPOINT_UUID> \
  --custom-endpoint https://api.example.com/agent
```

Default behavior:

- wallet-first registration
- the agent wallet signs a challenge
- the same wallet sends the on-chain transaction
- worker finalize routes verify the transaction and index the agent
- registration can include:
  - `image`
  - `version`
  - repeated `--tag`
  - repeated `--endpoint-id`
  - repeated `--custom-endpoint`
- at least one service source is required:
  - positional `endpoint`
  - one or more `--endpoint-id`
  - one or more `--custom-endpoint`

Supported networks:

- `base`, `baseSepolia`
- `ethereum`, `ethereumSepolia`
- `polygon`, `polygonAmoy`
- `bsc`, `bscTestnet`
- `monad`, `monadTestnet`
- `solanaMainnet`, `solanaDevnet`

Registration variables:

- `PRIVATE_KEY` + `WALLET_ADDRESS` for EVM wallet-first registration
- `SOLANA_SECRET_KEY` (+ optional `SOLANA_WALLET_ADDRESS`) for Solana wallet-first registration
- `X402_API_BASE` (optional override)

## Discovery And Management

Owned-agent discovery:

```bash
python {baseDir}/scripts/list_agents.py --network baseSepolia
python {baseDir}/scripts/list_agents.py --network ethereum
python {baseDir}/scripts/list_agents.py --network polygon
python {baseDir}/scripts/list_agents.py --network bsc
python {baseDir}/scripts/list_agents.py --network monad
python {baseDir}/scripts/list_agents.py --network solanaDevnet
```

Owned-endpoint discovery:

```bash
python {baseDir}/scripts/list_my_endpoints.py
python {baseDir}/scripts/list_my_endpoints.py --chain solana
```

Update an EVM agent:

```bash
python {baseDir}/scripts/update_agent.py \
  --network baseSepolia \
  --agent-id 123 \
  --name "Agent Name v2" \
  --description "Updated description" \
  --image https://example.com/agent-v2.png \
  --version 1.4.1 \
  --tag finance \
  --tag automation \
  --endpoint-id <ENDPOINT_UUID> \
  --custom-endpoint https://api.example.com/fallback \
  --public
```

Use the same wallet-first EVM lifecycle with `--network ethereum`, `--network polygon`, `--network bsc`, or `--network monad` when the wallet and contract deployment exist on that chain.

Update a Solana agent:

```bash
python {baseDir}/scripts/update_agent.py \
  --network solanaDevnet \
  --asset-address <SOLANA_ASSET_ADDRESS> \
  --version 1.4.1 \
  --clear-tags \
  --private
```

Notes:

- `list_agents.py` uses wallet-authenticated `GET /agent/erc8004/mine`
- `list_my_endpoints.py` uses wallet-authenticated `GET /agent/erc8004/endpoints/mine`
- `update_agent.py` uses `update/prepare` plus `update/finalize`
- when metadata changes, `update_agent.py` automatically sends `setAgentURI()` (EVM) or the prepared Solana URI update transaction before finalize
- `--prepare-only` is available on `update_agent.py` for inspection/debugging
- `--clear-endpoints` clears platform/custom endpoint bindings; provide `--endpoint` if you still want a fallback service URL
- linked platform endpoint ids must belong to the authenticated wallet or a linked dashboard user
- list and update routes accept wallet-first auth, not dashboard session cookies

## Reputation Feedback

EVM feedback example:

```bash
python {baseDir}/scripts/submit_feedback.py \
  --network base \
  --agent-id 123 \
  --rating 5 \
  --comment "High quality responses"
```

Solana feedback example:

```bash
python {baseDir}/scripts/submit_feedback.py \
  --network solanaMainnet \
  --asset-address <SOLANA_ASSET_ADDRESS> \
  --rating 4 \
  --comment "Reliable execution"
```

Auth variables:

- `WORKER_FEEDBACK_API_KEY`
- `X402_API_BASE` (optional override)

## Operational Notes

- Use the same network domain for registration and feedback whenever possible.
- Handle duplicate/exists responses gracefully for idempotent registration flows.
- Preserve on-chain identifiers (`agent_id` or `asset_address`) in your agent metadata store for future feedback calls.
- For dashboard parity, the preferred lifecycle is:
  1. list bindable endpoints
  2. register with full metadata
  3. list owned agents
  4. update visibility/tags/version/endpoints as needed
- AWAL is supported for x402 payments, but wallet-first ERC-8004 registration currently expects local signing keys.
