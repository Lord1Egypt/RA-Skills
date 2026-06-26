# Token Research Skill - Usage Examples

## Quick Start

### Example 1: Shallow Dive on PEPE (Ethereum)
```bash
# Use the helper script
./fetch_token_data.sh shallow 0x6982508145454ce325ddbe47a25d4ec3d2311933 ethereum

# Manual research for social sentiment
web_search("PEPE meme token narrative crypto twitter")
web_search("PEPE holders whale wallets movement")
```

**Expected Output:**
- Price, volume, liquidity from DexScreener
- Security analysis from GoPlus 
- Top 3 token holders from Etherscan
- Social narrative from web search

### Example 2: Deep Research on a Base Token
```bash
# Use helper script for data collection
./fetch_token_data.sh deep 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 base

# Additional manual research
web_search("Base USDC official Circle announcement")
web_search("Base chain adoption USDC usage statistics")
web_search("Circle team founders background USDC")
```

## Complete Research Workflow

### Step 1: Data Collection
```bash
# Set variables
TOKEN_ADDRESS="0x6982508145454ce325ddbe47a25d4ec3d2311933"
CHAIN="ethereum"

# Run automated data fetch
./fetch_token_data.sh deep $TOKEN_ADDRESS $CHAIN
```

### Step 2: Data Analysis
```bash
# Navigate to results folder
cd research_*_69825081

# Check data quality
cat research_summary.txt

# Analyze key files
cat dexscreener.json | jq '.pairs[0] | {price: .priceUsd, volume: .volume.h24, liquidity: .liquidity.usd}'
cat security.json | jq '.result | to_entries[0].value | {honeypot: .is_honeypot, mintable: .is_mintable, buy_tax: .buy_tax}'
cat holders.json | jq '.result[:3] | .[] | {address: .TokenHolderAddress, balance: .TokenHolderQuantity}'
```

### Step 3: Social Research
```bash
# Project fundamentals
web_search("PEPE official website social media")
web_search("PEPE meme token what is purpose utility")

# Team research
web_search("PEPE founder team anonymous doxxed")
web_search("PEPE development team background")

# Community sentiment
web_search("PEPE crypto twitter bullish bearish sentiment")
web_search("PEPE telegram discord community size")
web_search("PEPE KOL influencer mentions analysis")

# Recent activity
web_search("PEPE news announcement partnership 2024")
web_search("PEPE price pump dump reason why")
```

### Step 4: Risk Assessment
```bash
# Security deep dive
web_search("PEPE contract audit security report")
web_search("PEPE rug pull scam honeypot warning")
web_search("PEPE liquidity locked team tokens")

# Market risks
web_search("PEPE meme token risks volatility")
web_search("PEPE whale wallets large holders")
```

## Advanced Research Techniques

### Holder Analysis Deep Dive
```bash
# Get full holder list
curl "https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress=$TOKEN_ADDRESS&page=1&offset=1000&sort=desc"

# Check if top holders are known entities
web_search("0x... ethereum address label who owns")

# Calculate concentration metrics
# Top 10 holders percentage
# Gini coefficient for distribution
# Number of holders vs supply
```

### Cross-Chain Analysis
```bash
# Check if token exists on multiple chains
web_search("TOKEN_NAME multi-chain ethereum polygon BSC")

# Compare liquidity across chains
curl "https://api.dexscreener.com/latest/dex/search?q=TOKEN_SYMBOL" | jq '.pairs[] | select(.chainId != null) | {chain: .chainId, liquidity: .liquidity.usd}'
```

### Time-Series Analysis
```bash
# Historical price data (if available)
web_search("TOKEN_NAME price history chart coingecko dextools")

# Launch analysis
web_search("TOKEN_NAME launch date first trade stealth fair launch")
```

## Red Flags Checklist

During research, watch for these warning signs:

### 🚨 HIGH RISK
- [ ] Honeypot detected by GoPlus
- [ ] >50% supply held by top 10 wallets
- [ ] Anonymous team with no previous projects
- [ ] No verified contract
- [ ] Unlimited mint authority
- [ ] >5% buy/sell tax

### ⚠️ MEDIUM RISK
- [ ] 20-50% top holder concentration
- [ ] High volatility without clear catalysts
- [ ] New project (<30 days)
- [ ] Limited social presence

### ✅ POSITIVE INDICATORS
- [ ] Team fully doxxed with track record
- [ ] Liquidity locked long-term
- [ ] Active development and community
- [ ] Clear utility/value proposition
- [ ] Distributed holder base

## Sample Research Reports

### Shallow Dive Output
```
🔍 SHALLOW DIVE: Pepe (PEPE)

💰 BASICS
• Price: $0.000008 (24h: +12.5%)
• Market Cap: $3.2B | Liquidity: $45M
• Age: 287 days | Chain: Ethereum
• Contract: 0x6982508145454ce325ddbe47a25d4ec3d2311933

🛡️ SECURITY
• Honeypot: ✅ | Ownership: Renounced
• Risk Level: LOW

📱 NARRATIVE
• Project: Meme token inspired by Pepe the Frog
• Narrative: Community-driven meme coin with no utility

👥 TOP HOLDERS
1. 0x41...62f - 7.2% (Binance Hot Wallet)
2. 0x28...891 - 3.8% (Unknown)
3. 0x77...123 - 2.1% (Uniswap V3 Pool)

⚠️ QUICK ASSESSMENT: Established meme token with reasonable distribution. Standard meme coin risks apply.
```

## Automation Tips

### Batch Analysis
```bash
# Research multiple tokens
TOKENS=("0x6982..." "0xA0b86..." "0xdAC17...")
for token in "${TOKENS[@]}"; do
    ./fetch_token_data.sh shallow "$token" ethereum
    sleep 30  # Respect rate limits
done
```

### Monitoring Setup
```bash
# Create monitoring script for price alerts
echo '#!/bin/bash
TOKEN="0x6982508145454ce325ddbe47a25d4ec3d2311933"
CURRENT_PRICE=$(curl -s "https://api.dexscreener.com/latest/dex/tokens/ethereum/$TOKEN" | jq -r ".pairs[0].priceUsd")
echo "PEPE: $CURRENT_PRICE"
' > monitor_price.sh
chmod +x monitor_price.sh
```

Remember: Always verify critical information through multiple sources and never rely solely on automated analysis for investment decisions.