# VIGIL Contract Addresses

## Base Mainnet

| Contract | Address | Status |
|----------|---------|--------|
| $VIGIL Token (ERC-20) | [`0xC751afAdD6fde251Ac624A279ECB9ac85AA27bA3`](https://basescan.org/token/0xC751afAdD6fde251Ac624A279ECB9ac85AA27bA3) | ✅ Live on Base |
| Fee Recipient | [`0x9f6697155bbfc4c87fe9499ceb233a3dda4ce708`](https://basescan.org/address/0x9f6697155bbfc4c87fe9499ceb233a3dda4ce708) | ✅ Active |
| VIGIL Staking | `0xPENDING` | Planned |
| VIGIL Governance | TBD | Planned |
| VIGIL Treasury (Multi-sig) | TBD | Planned |

## Deployment Checklist

- [ ] Deploy `VigilToken.sol` with treasury address
- [ ] Deploy `VigilStaking.sol` with token address
- [ ] Grant `MINTER_ROLE` to staking contract (for bounty payouts)
- [ ] Fund staking reward pool with initial VIGIL allocation
- [ ] Add initial liquidity on Aerodrome (VIGIL/USDC pair)
- [ ] Lock LP tokens for 12 months
- [ ] Verify all contracts on BaseScan
- [ ] Transfer admin to multi-sig treasury

## Verification Commands

```bash
# Verify token contract
npx hardhat verify --network base <TOKEN_ADDRESS> "<TREASURY_ADDRESS>"

# Verify staking contract
npx hardhat verify --network base <STAKING_ADDRESS> "<TOKEN_ADDRESS>" "<OWNER_ADDRESS>"
```

## Dependencies

- OpenZeppelin Contracts v5.x
- Solidity ^0.8.20
- Base chain (Coinbase L2)
