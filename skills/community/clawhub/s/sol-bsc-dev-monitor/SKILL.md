---
name: unified-dev-monitor
description: Unified Dev Wallet Monitor for BSC and Solana - Monitor only, manual buy only, no private keys
version: "1.0.0"
author: Your Name
tags: [bsc, solana, monitor, research, crypto, blockchain, multi-chain]
payment:
  provider: skillpay.me
  api_key: sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5
  price: 0.005
  currency: USDT
  billing_mode: per_call
---
# Unified Dev Monitor

## 🎯 Overview

Multi-chain developer wallet monitor for BSC and Solana. Monitor token transfers from developer addresses and get real-time notifications of new token deployments.

## 🔒 Security First - No Private Keys Required

**Important:** This is a **monitor-only tool** with **manual buy only**. No private keys are required and no auto-buy functionality is included.

**Benefits:**
- ✅ No private keys needed
- ✅ Zero risk of accidental transactions
- ✅ Safe to run on any machine
- ✅ Perfect for research and information gathering

---

## 💰 Pricing & Billing

### Pricing Model

- **Per Call**: 0.005 USDT (1/2 token)
- **1 USDT = 200 tokens**
- **1 call = 0.5 tokens**
- **Minimum deposit: 8 USDT (1600 tokens)**

### Platform Fees

- **Handling fee:** 5%
- **Withdrawal:** Automatic to your wallet
- **Configuration:** No payment setup required

---

## 🔒 Manual Buy Only

### How It Works

1. **Monitor detects token transfer**
   - Scans blockchain blocks/slots
   - Filters transactions from monitored address
   - Detects new token transfers

2. **System provides buy links**
   - Solana: Jupiter Aggregator (https://jup.ag)
   - BSC: PancakeSwap (https://pancakeswap.finance/swap)

3. **User decides whether to buy**
   - User reviews token information
   - User clicks buy link
   - User authorizes transaction in their wallet
   - User confirms transaction

4. **System continues monitoring**
   - Transaction completes, system continues monitoring
   - Logs all detections

---

## 🚀 Quick Start

### Installation

```bash
npm install
```

### Test Run

```bash
# Test environment
npm test

# Test BSC monitoring
node index-bsc.js test

# Test Solana monitoring
node index-sol-safe.js test
```

---

## 📖 Usage

### Monitor Solana Address

```bash
node index-sol-safe.js monitor <ADDRESS> SOL <DURATION>
```

### Monitor BSC Address

```bash
node index-bsc.js monitor <ADDRESS> BSC <DURATION>
```

### Check Balance

```bash
node index.js '{"action":"balance","userId":"your-user-id"}'
```

---

## 📊 Supported Chains

### 1. BSC (Binance Smart Chain)

- **Native Token**: BNB
- **Block Time**: ~3 seconds
- **Address Format**: 0x... (42 hex characters)
- **DEX**: PancakeSwap
- **Router Address**: 0x10ED43C718714eb63d5aA57B78B54704E256024E

### 2. Solana

- **Native Token**: SOL
- **Block Time**: ~400ms
- **Address Format**: Base58 (32-44 characters)
- **DEX**: Jupiter Aggregator
- **API**: https://quote-api.jup.ag/v6

---

## 📝 Manual Buy Links

### Solana

After detecting a token, users can buy via:
- **Jupiter Aggregator**: https://jup.ag
- **Raydium**: https://raydium.io
- **Orca**: https://www.orca.so
- **1inch**: https://app.1inch.io
- **其他 DEX**

### BSC

After detecting a token, users can buy via:
- **PancakeSwap**: https://pancakeswap.finance/swap
- **1inch**: https://app.1inch.io
- **其他 DEX**

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

## 💰 Billing Guide

### Check Balance

```bash
node index.js '{"action":"balance","userId":"your-user-id"}'
```

**Response:**
```json
{
  "success": true,
  "action": "balance",
  "userId": "your-user-id",
  "balance": 1000,
  "tokens": 1000,
  "usdt": "5.000"
}
```

### Get Payment Link

```bash
node index.js '{"action":"payment-link","userId":"your-user-id","amount":8}'
```

### Monitor with Auto-Charge

```bash
# Solana
node index.js '{"action":"monitor","chain":"SOL","address":"...","duration":3600,"userId":"your-user-id"}'

# BSC
node index.js '{"action":"monitor","chain":"BSC","address":"...","duration":3600,"userId":"your-user-id"}'
```

**Insufficient Balance:**
```json
{
  "success": false,
  "action": "billing",
  "error": "Insufficient balance",
  "balance": 0,
  "paymentUrl": "https://skillpay.me/payment/...",
  "message": "余额不足。最低充值: 8 USDT (1600 tokens)\n充值链接: https://..."
}
```

---

## 💳 Billing Flow

### Complete Flow

```
用户请求监控
    ↓
检查余额 (0.5 tokens)
    ↓
余额 >= 0.5? 
  是 → 扣除 0.5 token → 开始监控
  ↓
检测到代币 → 提供购买链接
  ↓
用户决定是否购买
    ↓
交易完成
  ↓
继续监控
    ↓
返回检测结果
    ↓
  No → 返回充值链接
```

---

## 📊 Configuration

### Solana

```javascript
{
  SOLANA_RPC: 'https://api.mainnet-beta.solana.com',
  JUPITER_API: 'https://quote-api.jup.ag/v6',
  MONITOR_INTERVAL: 10000,  // 10 seconds
  DEFAULT_DURATION: 3600,      // 1 hour
  WSOL_MINT: 'So11111111111111111111111111111111111112'
}
```

### BSC

```javascript
{
  BSC_RPC: 'https://bsc-dataseed.binance.org',
  PANKCAKESWAP_ROUTER: '0x10ED43C718714eb63d5aA57B78B54704E256024E',
  WBNB_ADDRESS: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
  MONITOR_INTERVAL: 3000,   // 3 seconds
  DEFAULT_DURATION: 3600,      // 1 hour
}
```

---

## 📝 Output

### Detection Example

When a token transfer is detected:

**Solana:**
```
💰 Token transfer detected from <ADDRESS>
✅ Detection logged for token: TOKEN_SYMBOL
💰 User can buy at: https://jup.ag
```

**BSC:**
```
💰 Token transfer detected from <ADDRESS> to <TOKEN_ADDRESS>
✅ Detection logged for token: <TOKEN_ADDRESS>
💰 User can buy at: https://pancakeswap.finance/swap
```

### Summary

After monitoring completes, you'll get a summary:

```json
{
  "success": true,
  "chain": "SOL",
  "monitoring": {
    "address": "<ADDRESS>",
    "startTime": "2026-03-06T10:00:00.000Z",
    "endTime": "2026-03-06T11:00:00.000Z",
    "duration": 3600,
    "actualDuration": "3600.12",
    "slotsScanned": 1234,
    "detections": [
      {
        "chain": "SOL",
        "slot": 123456789,
        "signature": "...",
        "timestamp": "2026-03-06T10:30:00.000Z",
        "from": "<ADDRESS>",
        "to": "<TOKEN_ADDRESS>",
        "tokenMint": "...",
        "tokenSymbol": "TOKEN",
        "amount": "1000",
        "decimals": 9
      }
    ]
  }
}
```

---

## 📊 What Gets Detected

- Token transfers from monitored address
- Token mint addresses
- Token symbols (when available)
- Transfer amounts
- Timestamps
- Transaction signatures/hashes

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

## 🔒 Security & Privacy

### Data Collected

- Blockchain data (public)
- Token transfer information (public)
- Detection timestamps
- Log files for monitoring
- User ID (for billing)

### Data Stored Locally

- `logs-sol/sol-monitor.log` - Solana monitoring logs
- `logs-bsc/bsc-monitor.log` - BSC monitoring logs
- `detections-sol/detections.json` - Solana detection history
- `detections-bsc/detections.json` - BSC detection history

### Data NOT Collected

- ❌ No private keys
- ❌ No wallet information
- ❌ No personal data
- ❌ No transaction signing keys
- ❌ No sensitive financial information

---

## 💳 Billing SDK (billing-final.js)

### Core Functions

```javascript
// 查询余额
const balance = await checkBalance(userId);

// 扣费（每次调用 0.5 token = 0.005 USDT）
const charge = await chargeUser(userId, 0.005);

// 获取充值链接（最低 8 USDT = 1600 tokens）
const paymentUrl = await getPaymentLink(userId, 8);

// 检查并自动扣费
const result = await checkAndCharge(userId);
```

### Billing Flow

```
监控请求
    ↓
检查余额（0.005 token）
    ↓
余额 >= 0.005? 
  是 → 扣除 0.005 token → 开始监控
  ↓
检测到代币 → 提供购买链接
  ↓
用户决定是否购买
  ↓
交易完成
  ↓
继续监控
  ↓
返回检测结果
    ↓
  否 → 返回充值链接
```

---

## 🔒 Trading Safety

### What This Tool Does

- ✅ Monitors blockchain for token transfers
- ✅ Records detections with timestamps
- ✅ Saves detection history
- ✅ Provides buy links for manual trading
- ✅ Integrates with billing system

### What This Tool Does NOT Do

- ❌ No auto-buy functionality
- ❌ No private keys required
- ❌ No transactions executed
- ❌ No wallet interactions
- ❌ No spending of funds
- ❌ No transaction signing

---

## 💡 Platform Fees

- **Handling fee:** 5%
- **Withdrawal:** Automatic to your wallet
- **Configuration:** No payment setup required

---

## ⚠️ Important Notes

### This Tool Does
- ✅ Monitors blockchain for token transfers
- ✅ Records detections with timestamps
- ✅ Saves detection history
- ✅ Provides manual buy links (Jupiter, PancakeSwap, etc.)
- ✅ Integrates with billing system

### This Tool Does NOT Do
- ❌ No auto-buy functionality
- ❌ No private keys required
- ❌ No transactions executed
- ❌ No wallet interactions
- ❌ No spending of funds
- ❌ No transaction signing
- ❌ No sensitive financial information

---

## ⚖️ Disclaimer

This tool is provided for educational and research purposes only. The user assumes all risks associated with trading cryptocurrency.

**Always:**
- Always verify transactions independently
- Use only for legitimate monitoring purposes
- Check your balance before monitoring
- Manual trading should be done through verified DEX platforms
- This is a monitor-only tool - no transactions are executed

---

## 📦 Dependencies

- `@solana/web3.js` (^1.98.4) - Solana blockchain interaction
- `axios` (^1.13.6) - HTTP requests (Billing API)
- `ethers` (^5.0.0) - EVM blockchain interaction (BSC)

---

## 📄 License

MIT

---

**Version**: 1.0.0
**Node.js**: >=14.0.0
**Security Model**: Monitor only, no private keys, manual buy only
