# Supported Tokens and Chains

## Direction glossary

- **Pay-In** = the SOURCE side: the chain/token the payer sends FROM.
- **Pay-Out** = the DESTINATION side: the chain/token the recipient gets.
- A chain can appear in one direction and not the other. Solana appears under
  USDT **Pay-In** (you can pay FROM Solana in USDT) but not under USDT
  **Pay-Out** (a recipient cannot receive USDT on Solana).

## Pay-In Tokens (source — what you can pay FROM)

### USDC Pay-In

| Chain | Chain ID | Token Address | Decimals |
|-------|----------|--------------|----------|
| Ethereum | 1 | 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 | 6 |
| Arbitrum | 42161 | 0xaf88d065e77c8cc2239327c5edb3a432268e5831 | 6 |
| Base | 8453 | 0x833589fcd6edb6e08f4c7c32d4f71b54bda02913 | 6 |
| BSC | 56 | 0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d | 18 |
| Polygon | 137 | 0x3c499c542cef5e3811e1192ce70d8cc03d5c3359 | 6 |
| Solana | 900 | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | 6 |
| Stellar | 1500 | USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN | 7 |

### USDT Pay-In (source; NOT Base — Base is USDC-only in BOTH directions)

| Chain | Chain ID | Token Address | Decimals |
|-------|----------|--------------|----------|
| Ethereum | 1 | 0xdac17f958d2ee523a2206206994597c13d831ec7 | 6 |
| Arbitrum | 42161 | 0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9 | 6 |
| BSC | 56 | 0x55d398326f99059ff775485246999027b3197955 | 18 |
| Polygon | 137 | 0xc2132d05d31c914a87c6611c10748aeb04b58e8f | 6 |
| Solana | 900 | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB | 6 |

## Pay-Out Tokens (destination — what the recipient gets)

### USDC Pay-Out

| Chain | Chain ID | Token Address | Decimals |
|-------|----------|--------------|----------|
| Ethereum | 1 | 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 | 6 |
| Arbitrum | 42161 | 0xaf88d065e77c8cc2239327c5edb3a432268e5831 | 6 |
| Base | 8453 | 0x833589fcd6edb6e08f4c7c32d4f71b54bda02913 | 6 |
| BSC | 56 | 0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d | 18 |
| Polygon | 137 | 0x3c499c542cef5e3811e1192ce70d8cc03d5c3359 | 6 |
| Solana | 900 | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | 6 |
| Stellar | 1500 | USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN | 7 |

### USDT Pay-Out (destination — EVM chains only; NOT Solana, NOT Stellar, NOT Base)

| Chain | Chain ID | Token Address | Decimals |
|-------|----------|--------------|----------|
| Ethereum | 1 | 0xdac17f958d2ee523a2206206994597c13d831ec7 | 6 |
| Arbitrum | 42161 | 0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9 | 6 |
| BSC | 56 | 0x55d398326f99059ff775485246999027b3197955 | 18 |
| Polygon | 137 | 0xc2132d05d31c914a87c6611c10748aeb04b58e8f | 6 |

## Important Notes

- **USDT payout supported on EVM chains** — Ethereum, Arbitrum, BSC, Polygon
- **Base is USDC-only** — USDT is not supported on Base for pay-in or pay-out
- **USDT payout NOT supported on Solana or Stellar**
- **BSC uses 18 decimals** for both USDC and USDT (different from other chains)
- **Stellar uses 7 decimals** for USDC
