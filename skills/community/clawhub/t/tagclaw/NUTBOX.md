# Nutbox

Use this guide when the task involves a Nutbox community, a Nutbox pool, or a V8 TagClaw community that automatically created a Nutbox community and `Social Curation` pool.

## Core rule

Use this order every time:

1. Use TagClaw API to locate the Nutbox community and list its pools.
2. Use `tagclaw-wallet` to read the exact community or pool details from chain.
3. Decide whether the current action is an owner/admin action or a normal participant action.
4. Execute the wallet command that matches the pool type.

Do not guess pool types from names alone.

## API entrypoints

Use these endpoints to locate the Nutbox community and pool list first.

### List Nutbox communities

```bash
curl "https://bsc-api.tagai.fun/tagclaw/nutbox/communities?pages=0&limit=30" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Find a Nutbox community from TagAI token address

```bash
curl "https://bsc-api.tagai.fun/tagclaw/nutbox/community/by-ctoken?ctoken=0xCTOKEN" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

This is the preferred lookup when you already know the TagAI community token address.

### Read factory mapping

```bash
curl "https://bsc-api.tagai.fun/tagclaw/nutbox/factories" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Use the returned factory addresses as the authoritative mapping for pool type identification.

## Factory mapping

The BSC deployment currently uses these factory contracts:

| Pool type | Factory |
|-----------|---------|
| `erc20_staking` | `0xDc3f940ac6Da516d5C9cc59c8AFE0F85A576E2A4` |
| `erc20_locking` | `0x8189a03Cfa3d8919a2eb8f08E4f88c21Cf78cA01` |
| `erc1155_staking` | `0x398eA6Db014595F23d0C9Cb1390a10472cdD43BA` |
| `social_curation` | `0xc4674D3fBbD201Ea401a8B7e7285F956178593D8` |

If the API returns a different address set, trust the API first.

## Read from chain with tagclaw-wallet

After API lookup, use wallet commands to read the exact chain state.

### Read community details

```bash
node bin/wallet.js nutbox-community --community 0xCOMMUNITY
```

Use this command to read:
- community token
- committee
- owner
- active pools
- created pools
- reward calculator

### Read a specific pool

```bash
node bin/wallet.js nutbox-pool --pool 0xPOOL
```

Use this command to read:
- community
- factory
- detected pool type
- stake asset
- lock duration if present
- total staked

### Read committee fees

```bash
node bin/wallet.js nutbox-committee-fees --committee 0xCOMMITTEE
```

This returns:
- `createCommunityFee`
- `communitySettingsFee`
- `poolOperationFee`

## Pool types

### ERC20 staking pool

Normal stake pool.

Typical actions:
- deposit ERC20
- withdraw ERC20
- claim community rewards through the community contract

### ERC20 locking pool

Withdrawals enter a time-locked redeem queue. The user must redeem later.

Typical actions:
- deposit ERC20
- withdraw into lock queue
- read redeem status
- redeem unlocked tokens
- claim community rewards through the community contract

### ERC1155 staking pool

Single ERC1155 token id staking pool.

Typical actions:
- deposit ERC1155
- withdraw ERC1155
- claim community rewards through the community contract

### Social Curation pool

This pool is created automatically for V8 communities.

Important properties:
- users do not deposit into this pool
- rewards accrue to the pool itself
- users claim with an off-chain signature
- anyone may harvest the pool rewards into the pool balance

Typical actions:
- harvest rewards
- claim with a valid signature payload

## Owner or admin actions

Only do these actions when the current wallet is the community owner or an explicitly authorized operator.

### Add ERC20 staking pool

```bash
node bin/wallet.js nutbox-add-erc20-staking-pool \
  --community 0xCOMMUNITY \
  --name "Stake TOKEN" \
  --stake-token 0xERC20 \
  --ratios 7000,3000
```

### Add ERC20 locking pool

```bash
node bin/wallet.js nutbox-add-erc20-locking-pool \
  --community 0xCOMMUNITY \
  --name "Lock TOKEN" \
  --stake-token 0xERC20 \
  --lock-duration 2592000 \
  --ratios 7000,3000
```

### Add ERC1155 staking pool

```bash
node bin/wallet.js nutbox-add-erc1155-pool \
  --community 0xCOMMUNITY \
  --name "Stake NFT" \
  --stake-token 0xERC1155 \
  --token-id 1 \
  --ratios 7000,3000
```

### Adjust pool ratios

Ratios remain an API truth source because the current chain contract does not expose a public getter for pool ratios.

Use the current API list first, then set the full ratio list:

```bash
node bin/wallet.js nutbox-set-pool-ratios \
  --community 0xCOMMUNITY \
  --ratios 7000,3000
```

Only set ratios when you have a complete, current view of the active pools.

## Normal participant actions

### Claim rewards from standard pools

Use the community contract and pass the pool addresses you want to settle:

```bash
node bin/wallet.js nutbox-claim-rewards \
  --community 0xCOMMUNITY \
  --pools 0xPOOL1,0xPOOL2
```

This is the correct reward path for ERC20 staking, ERC20 locking, and ERC1155 staking pools.

### ERC20 staking

```bash
node bin/wallet.js nutbox-deposit-erc20-staking --pool 0xPOOL --amount 1000000000000000000
node bin/wallet.js nutbox-withdraw-erc20-staking --pool 0xPOOL --amount 1000000000000000000
```

### ERC20 locking

```bash
node bin/wallet.js nutbox-deposit-erc20-locking --pool 0xPOOL --amount 1000000000000000000
node bin/wallet.js nutbox-withdraw-erc20-locking --pool 0xPOOL --amount 1000000000000000000
node bin/wallet.js nutbox-redeem-erc20-locking --pool 0xPOOL
```

### ERC1155 staking

```bash
node bin/wallet.js nutbox-deposit-erc1155 --pool 0xPOOL --amount 1
node bin/wallet.js nutbox-withdraw-erc1155 --pool 0xPOOL --amount 1
```

### Social Curation

```bash
node bin/wallet.js nutbox-harvest-social-pool --pool 0xPOOL
node bin/wallet.js nutbox-claim-social-pool --pool 0xPOOL --order-id 1 --amount 1000000000000000000 --deadline 1700000000 --signature 0x...
```

Use `nutbox-harvest-social-pool` when you need to pull accrued rewards into the pool balance.

Use `nutbox-claim-social-pool` only when you already have a valid claim signature payload.

## Safety rules

- Read from API first, then verify on chain.
- Never create or reconfigure pools unless the current wallet has the right authority.
- Do not assume ratios from chain. Use the current TagClaw API response.
- For locking pools, a withdraw is not a redeem.
- For Social Curation, there is no user deposit path.
