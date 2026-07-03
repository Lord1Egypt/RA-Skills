# Urufu agent scripts

Support for AI agents (Hermes, OpenClaw, Cursor) playing urufu gēmu safely.

## One-command Hermes install

```bash
# from repo root
npm run pack-hermes
npm run install-hermes
hermes skills install ./scripts/dist/urufu-steward-hermes.tgz
```

## Quick start (dev)

```bash
cd scripts
npm install

export URUFU_WALLET=0xYourWallet
export URUFU_PRIVATE_KEY=0xYourSessionKey   # claim/mint only

node urufu-steward.mjs check
node urufu-steward.mjs claim                 # respects 6h timer
node urufu-steward.mjs claim --force         # user override
node urufu-steward.mjs mint-preview          # free phase + allowlist
node urufu-steward.mjs mint                  # respects 24h timer
node urufu-steward.mjs mint --force
```

## Docs

- Skill: `SKILL.md`
- Hermes: `hermes/SKILL.md`
- Bootstrap prompt: `references/BOOTSTRAP.md`
- OpenAPI: `docs/api/openapi.yaml`

## Policy

| Guard | Default |
|---|---|
| Min time between claims | **6 hours** |
| Min time between mints | **24 hours** |
| Min URU to claim | **0.001 URU** |
| Max ids per claim batch | **25** (prod server may allow 100) |
| Gasless mint | **free phase only** |
| Auto-mint / auto-swap | **off** |

## Env

| Variable | Purpose |
|---|---|
| `URUFU_WALLET` | Wallet address (required) |
| `URUFU_PRIVATE_KEY` | Signing key (claim/mint) |
| `URUFU_MINTER` | ChibiMinter override |
| `URUFU_RPC_URL` | Base RPC |
| `URUFU_INDEXER` | Indexer base URL |
| `URUFU_SITE_URL` | Site for gasless relay + allowlists |
| `URUFU_AGENT_STATE` | State file (default `~/.urufu-agent/state.json`) |
| `URUFU_CLAIM_INTERVAL_MS` | Claim cooldown override |
| `URUFU_MINT_INTERVAL_MS` | Mint cooldown override |

## Tests

```bash
npm test
npm run pack-hermes
```
