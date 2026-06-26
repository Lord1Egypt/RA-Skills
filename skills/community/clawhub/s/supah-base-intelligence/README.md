# SUPAH Base Intelligence

**OpenClaw skill for professional-grade token intelligence on Base blockchain.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Base](https://img.shields.io/badge/chain-Base-0052FF)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 What It Does

SUPAH provides **5-gate risk scoring** for Base tokens:
- **SIG** (Signals): Market momentum, volume, holder trends
- **TA** (Technical Analysis): Price action, indicators, patterns  
- **SEC** (Security): Honeypot detection, deployer profiling, liquidity safety
- **PRED** (Prediction): ML-based price predictions, confidence scores
- **NARR** (Narrative): Social sentiment, community strength, media coverage

**Each gate scores 0-100. Final score = weighted average.**

---

## 🚀 Quick Start

### Installation

```bash
# Via OpenClaw CLI
openclaw skills install supah-base-intelligence

# Or manually clone to skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/supahonbase/supah-openclaw-skill supah-base-intelligence
```

### Usage

**In your OpenClaw agent chat:**

```
scan token 0x52ba04de312cc160381a56b6b3b7fd482ae71d31
```

**Output:**
```
🦸 SUPAH Token Intelligence Report

Token: SUPH (SUPAH)
Address: 0x52ba04de312cc160381a56b6b3b7fd482ae71d31
Chain: Base

📊 Overall Score: 87/100 (SAFE)

Gate Breakdown:
• SIG (Signals):     92/100 ✅
• TA (Technical):    84/100 ✅
• SEC (Security):    95/100 ✅
• PRED (Prediction): 78/100 ⚠️
• NARR (Narrative):  88/100 ✅

Risk Level: LOW
Recommendation: Safe to trade with standard position sizing
```

---

## 📖 Commands

### Market Context ($0.03)

```bash
# Get ETH market regime (context for Base trading)
eth market
# Returns: HYPED/BULL/NEUTRAL/BEAR/DEEP_BEAR + momentum data
```

### Token Analysis

```bash
# Full 5-gate scan ($0.002)
scan token 0x52ba04de312cc160381a56b6b3b7fd482ae71d31

# Security scan only - faster ($0.001)
check safety 0x52ba04de312cc160381a56b6b3b7fd482ae71d31

# Portfolio analysis ($0.01)
analyze wallet 0xYourWalletAddress
```

### Premium Signal Feeds

```bash
# High-conviction signals - score ≥85 ($0.50)
get base signals

# Degen Top 5 - high-risk/high-reward ($1.00 - exclusive)
get degen tokens

# Swing Top 5 - swing trading picks ($1.00 - exclusive)
get swing picks
```

### Whale Tracking

```bash
# Monitor whale movements ($0.005)
track whales 0x52ba04de312cc160381a56b6b3b7fd482ae71d31

# Recent whale alerts ($0.002)
whale alerts
```

---

## 🔧 Configuration

### Requirements

- **`curl`** and **`node`** (pre-installed on most systems)
- **USDC on Base** — Your agent wallet must hold USDC on Base for x402 micropayments
- **x402-compatible HTTP client** — Payments happen automatically per call

Optional: Set `SUPAH_API_BASE` environment variable to override the default API endpoint (default: `https://api.supah.ai`).

### Pricing (x402 USDC per call)

**Token Intelligence**:
- Token scan: $0.08
- Safety scan: $0.08
- Market regime: $0.03

**Portfolio & Whales**:
- Portfolio scan: $0.05
- Whale tracking: $0.15
- Whale alerts: $0.15

**Premium Alpha**:
- Signal feed (score ≥85): $0.15
- Degen Top 5: $0.15
- Swing Top 5: $0.15

---

## 💡 Use Cases

### 1. Pre-Trade Risk Assessment

```bash
# Before buying any Base token
scan token 0x...

# Check for honeypots/scams
check safety 0x...
```

### 2. Portfolio Monitoring

```bash
# Scan your entire portfolio
analyze wallet 0xYourWallet

# Get alerts on risky holdings
```

### 3. Signal Trading

```bash
# Daily signal check
get base signals

# High-conviction opportunities only (score ≥85)
```

### 4. Whale Tracking

```bash
# Monitor smart money
track whales 0x...

# Follow whale movements
whale alerts
```

---

## 🎨 Integration Examples

### Basic Integration

```javascript
// In your OpenClaw agent code
const supah = require('./skills/supah-base-intelligence');

async function checkToken(address) {
  const result = await supah.scanToken(address);
  
  if (result.score >= 85) {
    console.log('✅ Safe to trade');
  } else if (result.score >= 60) {
    console.log('⚠️ Moderate risk');
  } else {
    console.log('🚫 High risk - avoid');
  }
}
```

### Automated Trading Bot

```javascript
// Get signals and auto-execute
const signals = await supah.getSignals({ minScore: 85 });

for (const signal of signals) {
  if (signal.gates.sec >= 90) {  // High security only
    await executeTrade(signal.address);
  }
}
```

### Portfolio Monitor

```javascript
// Daily portfolio health check
const portfolio = await supah.analyzeWallet(myWallet);

const risky = portfolio.tokens.filter(t => t.score < 60);
if (risky.length > 0) {
  await sendAlert(`⚠️ ${risky.length} risky tokens in portfolio`);
}
```

---

## 🔒 Security & Privacy

- **No private keys required** — read-only API calls
- **x402 USDC payments** — on-chain, transparent
- **No data storage** — requests processed and discarded
- **Rate limiting** — prevents abuse
- **Open source** — audit the code yourself

---

## 📊 API Endpoints (Behind the Scenes)

This skill uses SUPAH API endpoints:

```
GET  /agent/v1/token/:address          # Token risk score
GET  /agent/v1/safety/:address         # Safety scan only
GET  /agent/v1/portfolio/:wallet       # Portfolio analysis
GET  /agent/v1/signals                 # High-conviction signals
GET  /agent/v1/whale-alerts/:address   # Whale tracking
POST /agent/v1/batch/risk-scores       # Batch scanning
```

**All endpoints support x402 micropayments.**

---

## 🤝 Support

- **Docs**: https://docs.supah.ai
- **API**: https://api.supah.ai
- **Telegram**: https://t.me/SUPAH_Based
- **X**: https://x.com/SUPAH_AI_
- **GitHub Issues**: https://github.com/supahonbase/supah-openclaw-skill/issues

---

## 📜 License

MIT License - see LICENSE file

---

## 🦸 About SUPAH

SUPAH is the leading AI-powered token intelligence platform on Base blockchain. We provide institutional-grade risk analysis through our 5-gate scoring system, protecting traders from rugs, honeypots, and high-risk tokens.

**Features**:
- 5-gate risk scoring (SIG/TA/SEC/PRED/NARR)
- Real-time whale tracking
- Portfolio analysis
- High-conviction signal feeds
- x402 USDC micropayments
- Multi-platform (Web, API, MCP, OpenClaw, MetaMask)

**Built for**:
- Retail traders (app.supah.ai)
- Developers (api.supah.ai)
- AI agents (MCP, OpenClaw, x402)
- DeFi protocols (API integrations)

---

**Get started**: https://app.supah.ai  
**API docs**: https://api.supah.ai

🦸 **SUPAH — King of Snipes, Slayer of Rugs, Protector of Degens.**
