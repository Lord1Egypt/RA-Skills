# Token Research API Quick Reference

## Quick Commands

### DexScreener API
```bash
# Search for token by name/symbol
curl "https://api.dexscreener.com/latest/dex/search?q=PEPE"

# Get token pairs (Base)
curl "https://api.dexscreener.com/latest/dex/tokens/base/0x6982508145454ce325ddbe47a25d4ec3d2311933"

# Get token pairs (Solana)
curl "https://api.dexscreener.com/latest/dex/tokens/solana/So11111111111111111111111111111111111111112"

# Get specific pair info
curl "https://api.dexscreener.com/latest/dex/pairs/base/0x...pairaddress"
```

### GoPlus Security API
```bash
# EVM token security check
curl "https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=0x6982508145454ce325ddbe47a25d4ec3d2311933"

# Solana token security check  
curl "https://api.gopluslabs.io/api/v2/token_security/So11111111111111111111111111111111111111112?chain_id=solana"

# Malicious address check
curl "https://api.gopluslabs.io/api/v1/address_security/0x...address?chain_id=1"
```

### Etherscan/Basescan APIs
```bash
# Token info
curl "https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress=0x...&apikey=YourApiKey"

# Top token holders
curl "https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=0x...&page=1&offset=100&apikey=YourApiKey"

# Address balance  
curl "https://api.etherscan.io/api?module=account&action=balance&address=0x...&apikey=YourApiKey"

# Base chain (same format, different URL)
curl "https://api.basescan.org/api?module=token&action=tokeninfo&contractaddress=0x..."
```

## Common Token Addresses for Testing

### Ethereum Mainnet
- **USDC**: `0xA0b86a33E6441085693a5a8b6633b0f21d73f5dd`
- **USDT**: `0xdAC17F958D2ee523a2206206994597C13D831ec7`
- **WETH**: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- **PEPE**: `0x6982508145454ce325ddbe47a25d4ec3d2311933`

### Base Chain
- **USDC**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **WETH**: `0x4200000000000000000000000000000000000006`

### Solana
- **SOL**: `So11111111111111111111111111111111111111112`
- **USDC**: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- **BONK**: `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263`

## Chain IDs & API Endpoints

| Chain | ID | DexScreener | GoPlus | Block Explorer |
|-------|----|---------|---------| --------------|
| Ethereum | 1 | ethereum | 1 | api.etherscan.io |
| Base | 8453 | base | 8453 | api.basescan.org |
| BSC | 56 | bsc | 56 | api.bscscan.com |
| Arbitrum | 42161 | arbitrum | 42161 | api.arbiscan.io |
| Polygon | 137 | polygon | 137 | api.polygonscan.com |
| Solana | - | solana | solana | - |

## Web Search Queries for Social Research

### Project Information
```bash
web_search("TOKEN_NAME official website")
web_search("TOKEN_NAME whitepaper documentation")
web_search("TOKEN_NAME what does project do")
```

### Team Research
```bash
web_search("TOKEN_NAME founder CEO team doxxed")
web_search("TOKEN_NAME team linkedin background")
web_search("TOKEN_NAME previous projects experience")
```

### Social Sentiment
```bash
web_search("TOKEN_NAME twitter OR x.com bullish bearish")
web_search("TOKEN_NAME crypto twitter KOL mentions")
web_search("TOKEN_NAME telegram discord community")
web_search("TOKEN_NAME reddit discussion sentiment")
```

### News & Events
```bash
web_search("TOKEN_NAME news announcement partnership")
web_search("TOKEN_NAME listing exchange binance")
web_search("TOKEN_NAME pump dump reason why")
```

### Risk Research
```bash
web_search("TOKEN_NAME scam rug pull warning")
web_search("TOKEN_NAME audit report security")
web_search("TOKEN_NAME honeypot contract risk")
```

## Rate Limit Guidelines

- **DexScreener**: 300 req/min for pairs, 60 req/min for others
- **GoPlus**: No published limits - be respectful
- **Etherscan**: 5 req/sec (free), 100 req/sec (pro)
- **Web Search**: Use sparingly, combine queries

## Common JSON Response Fields

### DexScreener Response
```json
{
  "pairs": [{
    "baseToken": {"address", "name", "symbol"},
    "quoteToken": {"address", "name", "symbol"},
    "priceUsd": "0.00001",
    "volume": {"h24": "1000000"},
    "liquidity": {"usd": "500000"},
    "fdv": "1000000",
    "pairCreatedAt": "timestamp"
  }]
}
```

### GoPlus Security Response
```json
{
  "result": {
    "TOKEN_ADDRESS": {
      "is_honeypot": "0",
      "is_mintable": "0", 
      "is_proxy": "0",
      "buy_tax": "0.01",
      "sell_tax": "0.01",
      "owner_address": "0x000...000",
      "creator_address": "0x...",
      "lp_holders": [...]
    }
  }
}
```

### Etherscan Holders Response
```json
{
  "result": [{
    "TokenHolderAddress": "0x...",
    "TokenHolderQuantity": "1000000000000000000000"
  }]
}
```