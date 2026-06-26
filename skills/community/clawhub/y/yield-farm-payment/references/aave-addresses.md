# Aave V3 Addresses - Base Network

## Main Contracts (YieldFarmPayment)

### Aave V3 Pool
- **Address**: `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5`
- **Description**: Main pool contract for deposits, withdrawals, and borrowing
- **Source**: Aave V3 Base Mainnet

### Pool Addresses Provider
- **Address**: `0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D`
- **Description**: Provides addresses of all Aave V3 contracts

### Pool Data Provider
- **Address**: `0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac`
- **Description**: Provides user account data including health factor

### Oracle
- **Address**: `0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156`
- **Description**: Price oracle for Aave V3 on Base

### Pool Addresses Provider
- **Address**: `0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D`
- **Description**: Provides addresses of all Aave V3 contracts

## Token Addresses

### USDC (Circle)
- **Address**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Decimals**: 6
- **aToken**: `0x4e65fE4DbA92790696d040ac24Aa414708F5c0AB` (aBaseUSDC)

### WETH
- **Address**: `0x4200000000000000000000000000000000000006`
- **Decimals**: 18
- **aToken**: `0xD4a0e0b9149BCbE3D8C5b0F0B5cAeB8c8C9C8F8c` (aBaseWETH)

### cbETH
- **Address**: `0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22`
- **Decimals**: 18
- **aToken**: `0x...` (aBasecbETH)

## Important Notes

### Health Factor
- Minimum safe health factor: **1.1**
- Liquidation threshold varies by asset
- Monitor health factor regularly

### Interest Rates
- USDC supply APY: ~2-3% (conservative estimate)
- Rates update based on pool utilization

### Network Details
- **Chain ID**: 8453
- **RPC URL**: `https://mainnet.base.org`
- **Block Explorer**: `https://basescan.org`

## Usage Examples

### Supply USDC to Aave
```javascript
const poolAddress = '0xA238Dd80C259a72e81d7e4664a9801593F98d1c5';
const usdcAddress = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

// Supply 100 USDC
await poolContract.supply(
  usdcAddress,
  parseUnits('100', 6),
  userAddress,
  0 // referralCode
);
```

### Check User Data
```javascript
const userData = await poolContract.getUserAccountData(userAddress);
// Returns: [totalCollateralBase, totalDebtBase, availableBorrowsBase, 
//           currentLiquidationThreshold, ltv, healthFactor]
```

## Safety Considerations

1. Always maintain health factor > 1.1
2. Use buffers for price volatility
3. Test on testnet first (Base Sepolia)
4. Implement emergency withdrawal procedures
5. Monitor Aave governance for parameter changes

## Testnet (Base Sepolia)

- **Pool Address**: `0x...` (check Aave docs for latest)
- **Test USDC**: Get from Base faucet
- **RPC URL**: `https://sepolia.base.org`
