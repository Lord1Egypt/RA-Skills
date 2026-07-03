# Urufu Agent API (OpenAPI)

Machine-readable contract for AI agents and MCP codegen.

## Spec

- [`openapi.yaml`](./openapi.yaml) — indexer reads, gasless claim + free mint relay, meadow REST

## Hermes tarball

From [urufu-agent](https://github.com/urufu-labs/urufu-agent):

```bash
git clone https://github.com/urufu-labs/urufu-agent.git
cd urufu-agent
npm run pack-hermes
hermes skills install ./scripts/dist/urufu-steward-hermes.tgz
cd scripts/dist/urufu-steward-hermes && node install.mjs
```

## MCP codegen

Generate a typed client (example with OpenAPI Generator):

```bash
npx @openapitools/openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g typescript-fetch \
  -o /tmp/urufu-agent-client
```

For MCP servers, expose read tools from indexer paths first (`getStats`, `getChibisByOwner`).
Write tools should wrap `scripts/urufu-steward.mjs` so claim timers stay enforced.

## Runnable steward (recommended)

Prefer the repo CLI over raw POST spam:

```bash
cd scripts
npm install
export URUFU_WALLET=0x...
export URUFU_PRIVATE_KEY=0x...   # claim only; use session key in prod

node urufu-steward.mjs check
node urufu-steward.mjs claim      # respects 6h timer
node urufu-steward.mjs claim --force  # user override only
node urufu-steward.mjs mint-preview
node urufu-steward.mjs mint       # gasless free phase, 24h cooldown
```

## EIP-712 MintIntent

| Field | Type |
|---|---|
| domain.name | `UrufuRandomness` |
| domain.version | `1` |
| domain.chainId | `8453` |
| domain.verifyingContract | minter address |
| message.user | wallet |
| message.phaseId | open free phase id |
| message.quantity | mint count |
| message.nonce | `mintNonce(user)` |
| message.deadline | unix sec |
| message.paramsHash | `mintParamsHash(phaseId, qty, 0)` |

Reference: `scripts/mint.mjs`

## EIP-712 ClaimIntent

| Field | Type |
|---|---|
| domain.name | `UrufuClaims` |
| domain.version | `1` |
| domain.chainId | `8453` |
| domain.verifyingContract | vault address |
| message.user | wallet |
| message.nonce | `claimNonce(user)` |
| message.deadline | unix sec, ≤ 5 min ahead |
| message.tokenIdsHash | hash of sorted token id list |

Reference: `scripts/chain.mjs`, `scripts/claim.mjs`

## Related

- `SKILL.md`
- `hermes/SKILL.md`
- `scripts/README.md`
