# Example: Token Safety Check

## User Prompt

```
Is this token safe? TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE
```

## Expected Workflow

1. **Token Metadata** → `getTrc20Info("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → Name, symbol
2. **Contract Info** → `getContractInfo("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → Deployer, settings
3. **Contract ABI** → `getContract("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE")` → ABI check
4. **Holders** → `getTrc20TokenHolders("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", limit=20)` → Concentration
5. **Transactions** → `getContractTransactions("TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", limit=50)` → Activity
6. **Deployer Account** → `getAccount(deployerAddress)` → Deployer profile
7. **Web Search** → "TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE token scam" → Community reports

## Expected Output (Sample)

```
## Token Report: MoonToken (MOON)

### Basic Info
- Contract: TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE
- Standard: TRC-20
- Decimals: 18
- Issuer: TJZuV6A9QRdtVeJBvewCF9fLF2qnRSEv3y
- Issue Date: March 1, 2026

### Supply & Market
- Total Supply: 1,000,000,000,000 MOON
- Price: No exchange listings found
- Market Cap: Unknown

### Holder Analysis
- Total Holders: 23
- Top 10 Concentration: 99.2% ⚠️
- Largest Holder: Deployer wallet (92% of supply) ⚠️

### Activity Metrics
- Total Transactions: 47
- Daily Active Addresses: ~3
- 7-day Trend: Declining

### Safety Score: High Risk ⛔

**Critical Risk Factors:**
1. Deployer holds 92% of total supply
2. Only 23 holders — extremely low adoption
3. No ABI available (closed source)
4. Deployed only 10 days ago
5. No exchange listings or liquidity pools found
6. Extremely low activity (47 total transactions)
7. 100% user energy cost (consume_user_resource_percent = 100)

**Recommendation:**
Do NOT interact with this token. It shows all classic signs of a potential
rug pull: extreme concentration, no transparency, no liquidity, and minimal
organic activity.
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getTrc20Info` | 1 | Token metadata |
| `getContractInfo` | 1 | Contract settings |
| `getContract` | 1 | ABI availability |
| `getTrc20TokenHolders` | 1 | Concentration |
| `getContractTransactions` | 1 | Activity |
| `getAccount` | 1 | Deployer profile |
