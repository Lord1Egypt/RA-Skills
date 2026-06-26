# Wallet Address Detection Rules

## Detection Patterns

### EVM Addresses
- **Pattern**: `0x` followed by exactly 40 hexadecimal characters (0-9, a-f, A-F)
- **Regex**: `^0x[0-9a-fA-F]{40}$`
- **Chains**: Ethereum (1), Arbitrum (42161), Base (8453), BSC (56), Polygon (137)
- **Action**: ALWAYS ask which chain — never assume from address alone
- **Payout chains**: Ethereum, Arbitrum, Base, BSC, Polygon

### Solana Addresses
- **Pattern**: Base58 encoded, 32-44 characters, does NOT start with `0x`
- **Regex**: `^[1-9A-HJ-NP-Za-km-z]{32,44}$`
- **Chain ID**: 900
- **Action**: Auto-detect as Solana

### Stellar G-Wallet (Private Key Wallet)
- **Pattern**: Starts with `G`, followed by 55 uppercase alphanumeric characters (Base32)
- **Regex**: `^G[A-Z2-7]{55}$`
- **Chain ID**: 1500
- **Action**: Auto-detect as Stellar
- **Trustline check**: Run `node scripts/dist/check-stellar-trustline.js --address <G_wallet>` (defaults to USDC, use `--asset EURC` for EURC). Block payment if trustline is missing.

### Stellar C-Wallet (Smart Contract Wallet)
- **Pattern**: Starts with `C`, followed by 55 uppercase alphanumeric characters (Base32)
- **Regex**: `^C[A-Z2-7]{55}$`
- **Chain ID**: 1500
- **Action**: Auto-detect as Stellar, use `stellar_payin_contracts` intent
- **Flow**:
  1. API returns Soroban contract address (`receiverAddressContract`) and memo (`receiverMemoContract`)
  2. User invokes the contract's `pay()` function with the amount and memo
  3. System monitors and triggers payout upon detection

## Decision Tree

```
Address starts with "0x" and length is 42?
├── Yes → EVM address
│   └── Ask user which chain (Ethereum, Arbitrum, Base, BSC, Polygon for payouts)
│
Address is Base58, 32-44 chars?
├── Yes → Solana (chain 900)
│
Address starts with "G" and length is 56?
├── Yes → Stellar G-wallet (chain 1500)
│   └── Warn about USDC trustline if sending USDC
│
Address starts with "C" and length is 56?
├── Yes → Stellar C-wallet (chain 1500)
│   └── Use stellar_payin_contracts intent
│
└── None matched → Ask user to verify the address format
```
