# Unified Dev Monitor - Monitor Only Version

## 🎯 Overview

Multi-chain developer wallet monitor for BSC and Solana. Monitor token transfers from developer addresses and get real-time notifications of new token deployments.

## 🔒 Security First - No Private Keys Required

**Important:** This is a **monitor-only tool**. No private keys are required and no auto-buy functionality is included.

**Benefits:**
- ✅ No private keys needed
- ✅ Zero risk of accidental transactions
- ✅ Safe to run on any machine
- ✅ Perfect for research and information gathering

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Monitoring

**Solana:**
```bash
node index-sol-safe.js monitor <ADDRESS> SOL 3600
```

**BSC:**
```bash
node index-bsc.js monitor <ADDRESS> BSC  60
```

**Example:**
```bash
node index-sol-safe.js monitor 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU SOL 3600
```

---

## 📊 Supported Chains

### 1. BSC (Binance Smart Chain)

- **Native Token**: BNB
- **DEX**: PancakeSwap
- **Router Address**: 0x10ED43C718714eb63d5aA57B78B54704E256024E

### 2. Solana

- **Native Token**: SOL
- **DEX**: Jupiter Aggregator
- **API**: https://quote-api.jup.ag/v6

---

## 📖 Usage

### Monitor with Manual Buy

**Solana:**
```bash
node index-sol-safe.js monitor <ADDRESS> SOL 3600
```

**BSC:**
```bash
node index-bsc.js monitor <ADDRESS> BSC 3600
```

### Monitor Only (No Buy)

```javascript
const { monitorSOL } = require('./index-sol-safe.js');

await monitorSOL({
  address: 'YourAddress',
  duration: 3600
});
```

---

## 📝 Output

### Detection Example

When a token transfer is detected:

**Solana:**
```
💰 New token detected!
✅ Detection logged for token: TOKEN_SYMBOL
💰 User can buy at: https://jup.ag
```

**BSC:**
```
💰 Transaction from 0x... to 0x...
✅ Detection logged for token: 0x...
💰 User can buy at: https://exchange.pancakeswap.finance/#/swap
```

---

## 🔍 Viewing Results

### View Logs

```bash
# Solana
tail -f logs-sol/sol-monitor.log

# BSC
tail -f logs-bsc/bsc-monitor.log
```

### View Detections

```bash
# Solana
cat detections-sol/detections.json

# BSC
cat detections-bsc/detections.json
```

---

## ⚙️ Configuration

### Solana

```javascript
{
  SOLANA_RPC: 'https://api.mainnet-beta.solana.com',
  MONITOR_INTERVAL: 10000,  // 10 seconds
  DEFAULT_DURATION: 3600      // 1 hour
}
```

### BSC

```javascript
{
  BSC_RPC: 'https://bsc-dataseed.binance.org',
  MONITOR_INTERVAL: 3000,   // 3 seconds
  DEFAULT_DURATION: 3600      // 1 hour
}
```

---

## 🔒 Privacy & Security

### What This Tool Does

- ✅ Monitors blockchain for token transfers
- ✅ Records detections with timestamps
- ✅ Saves detection history
- ✅ Provides detailed logs
- ✅ Offers manual buy links (Jupiter, PancakeSwap)

### What This Tool Does NOT Do

- ❌ No auto-buy functionality
- ❌ No private keys required
- ❌ No transactions executed
- ❌ No wallet interactions
- ❌ No spending of funds

---

## 📝 Logging

Logs are written to:
- `logs-sol/sol-monitor.log` - Solana monitoring logs
- `logs-bsc/ ⚠️ No private keys are logged

---

## 🔍 Transaction Verification

### Solana

**Explorer:** https://explorer.solana.com/
- **Check:** Transaction signatures in logs

### BSC

**Explorer:** https://bscscan.com/
- **Check:** Transaction hashes in logs

---

## 💡 Manual Buy Links

After detection, users can manually buy tokens:

### Solana
- **Jupiter:** https://jup.ag
- **Raydium:** https://raydium.io/
- **Orca:** https://www.orca.so/

### BSC
- **PancakeSwap:** https://exchange.pancakeswap.finance/#/swap
- **1inch:** https://app.1inch.io/

---

## 📦 Dependencies

- `@solana/web3.js` (^1.98.4) - Solana blockchain interaction
- `axios` (^1.13.6) - HTTP requests (Jupiter API)
- `ethers` (^5.0.0) - EVM blockchain interaction (BSC)

---

## 💰 Billing Integration

### Pricing

- **1 call = 1 token = 0.005 USDT**
- **1 USDT = 200 tokens**
- **Minimum deposit: 8 USDT = 1600 tokens**

### Check Balance

```bash
node index.js '{"action":"balance","userId":"your-id"}'
```

### Get Payment Link

```bash
node index.js '{"action":"payment-link","userId":"your-id","amount":8}'
```

---

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. The user assumes all risks associated with trading cryptocurrency.

**Important:**
- Always verify transactions independently
- Use only for legitimate monitoring purposes
- This is a monitor-only tool - no transactions are executed
- Manual buying should be done through verified DEX platforms

---

**Version**: 1.0.0
**Node.js**: >=14.0.0
**Mode**: Monitor only, no private keys, no auto-buy
