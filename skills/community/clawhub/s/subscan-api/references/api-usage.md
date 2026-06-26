# Subscan API Usage Reference

## Basic Information

- **Documentation**: https://support.subscan.io
- **Pro Account**: https://pro.subscan.io
- **API Endpoint Format**: `https://<network>.api.subscan.io<path>`

## Authentication

All requests require the following headers:
```
X-API-Key: <your_api_key>
Content-Type: application/json
X-Refer: subscan-api-skill
```

Free users have rate limits; Pro users have higher quotas.

## Common Network Names

| Chain                    | network Parameter       |
|--------------------------|-------------------------|
| Acala                    | acala                   |
| agung (Testnet)          | agung-testnet           |
| Altair                   | altair                  |
| AssetHub Kusama          | assethub-kusama         |
| AssetHub Paseo           | assethub-paseo          |
| AssetHub Polkadot        | assethub-polkadot       |
| AssetHub Westend         | assethub-westend        |
| Astar                    | astar                   |
| Autonomys                | autonomys               |
| Autonomys Chronos        | autonomys-chronos       |
| Avail                    | avail                   |
| Avail Turing             | avail-turing            |
| Basilisk                 | basilisk                |
| Bifrost                  | bifrost                 |
| Bifrost Kusama           | bifrost-kusama          |
| BridgeHub Kusama         | bridgehub-kusama        |
| BridgeHub Paseo          | bridgehub-paseo         |
| BridgeHub Polkadot       | bridgehub-polkadot      |
| BridgeHub Westend        | bridgehub-westend       |
| Canary Matrix            | canary-matrix           |
| Canary Relay             | canary                  |
| CC Enterprise            | cc-enterprise           |
| CC Enterprise Testnet    | cc-enterprise-testnet   |
| Centrifuge               | centrifuge              |
| Collectives Polkadot     | collectives-polkadot    |
| Coretime Kusama          | coretime-kusama         |
| Coretime Paseo           | coretime-paseo          |
| Coretime Polkadot        | coretime-polkadot       |
| Coretime Westend         | coretime-westend        |
| Creditcoin               | creditcoin              |
| Creditcoin3 Testnet      | creditcoin3-testnet     |
| Crust                    | crust                   |
| Crust Parachain          | crust-parachain         |
| Dancelight               | dancelight              |
| Darwinia                 | darwinia                |
| Energy Web X             | energywebx              |
| Energy Web X Paseo       | energywebx-testnet      |
| Enjin Matrix             | matrix                  |
| Enjin Relay              | enjin                   |
| Heima                    | heima                   |
| Humanode                 | humanode                |
| Hydration                | hydration               |
| Karura                   | karura                  |
| Khala (Archived)         | khala                   |
| krest                    | krest                   |
| Kusama                   | kusama                  |
| Manta Atlantic           | manta                   |
| Midnight Mainnet         | midnight                |
| Midnight Preprod         | midnight-preprod        |
| Midnight Preview         | midnight-preview        |
| Moonbase                 | moonbase                |
| Moonbeam                 | moonbeam                |
| Moonriver                | moonriver               |
| Mythos                   | mythos                  |
| NeuroWeb                 | neuroweb                |
| NeuroWeb Testnet         | neuroweb-testnet        |
| Paseo                    | paseo                   |
| peaq                     | peaq                    |
| Pendulum                 | pendulum                |
| People Kusama            | people-kusama           |
| People Paseo             | people-paseo            |
| People Polkadot          | people-polkadot         |
| People Westend           | people-westend          |
| Phala (Archived)         | phala                   |
| Polkadot                 | polkadot                |
| Polymesh                 | polymesh                |
| Polymesh Testnet         | polymesh-testnet        |
| Reef                     | reef                    |
| Robonomics               | robonomics              |
| Shibuya                  | shibuya                 |
| Shiden                   | shiden                  |
| Space and Time           | sxt                     |
| Tanssi                   | tanssi                  |
| VFlow                    | vflow                   |
| VFlow Testnet            | vflow-testnet           |
| Vara                     | vara                    |
| Westend                  | westend                 |
| zkVerify                 | zkverify                |
| zkVerify Testnet         | zkverify-testnet        |

## Common Endpoints Quick Reference

### Block Queries
- `POST /api/scan/block` — Query block details by block number, hash, or timestamp
  - params: `block_num` (int) or `block_hash` (string)
- `POST /api/scan/blocks` — Block list

### Account Queries
- `POST /api/scan/account/tokens` — Account token balances
  - params: `address` (string, required)
- `POST /api/scan/account/balance_history` — Balance history

### Transaction / Extrinsic Queries
- `POST /api/scan/extrinsics` — Extrinsic list
  - params: `address`, `module`, `call`, `page`, `row`
- `POST /api/scan/extrinsic` — Extrinsic details
  - params: `extrinsic_index` or `hash`

### Staking Queries
- `POST /api/scan/staking/validator` — Validator details
- `POST /api/scan/staking/nominators` — Nominator list

### Governance
- `POST /api/scan/referenda_v2/referendums` — OpenGov referendum list
- `POST /api/scan/democracy/referendums` — Legacy referendums

### EVM / Contracts
- `POST /api/scan/evm/transactions` — EVM transaction list
- `POST /api/scan/evm/tokens` — EVM token list

## Response Structure

Standard response format:
```json
{
  "code": 0,
  "message": "Success",
  "generated_at": 1234567890,
  "data": { ... }
}
```

- `code == 0`: success
- `code != 0`: failure, check `message` for details

## Pagination Parameters

List endpoints typically support:
- `page`: page number (starts at 0)
- `row`: items per page (default 20, max 100)
- `order`: sort direction (`"desc"` or `"asc"`)

## Common Errors

| code  | Meaning              | Action                              |
|-------|----------------------|-------------------------------------|
| 10001 | Invalid parameter    | Check request body parameters       |
| 10004 | Invalid address      | Verify address format               |
| 20001 | Invalid API Key      | Check if the key is correct         |
| 40001 | Rate limit exceeded  | Reduce request frequency or upgrade |
