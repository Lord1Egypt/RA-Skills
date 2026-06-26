# 🌾 YieldFarmPayment v1.0

**Recover Payment amount to recipient (any seller) with Aave v3 automatic investment.** 
Our high-efficiency logic on Base L2 offsets network fees by pairing payments with low-risk, stablecoin-based yield investments. Achieve professional-grade automated cost recovery.

Pay recipients immediately on Base network, then recover your capital over time through Aave V3 yield farming.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Base Network](https://img.shields.io/badge/Network-Base-0052FF)](https://base.org)
[![Aave V3](https://img.shields.io/badge/Integration-Aave%20V3-1B5AE3)](https://aave.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ⚠️ v1.0 — Upfront Mode Only

v1.0 supports **Upfront Mode** only (immediate payment to recipient + capital recovery).
Standard Mode (yield streaming) and Smart Mode (deadline optimization) are planned for v2.0.

## 🎯 What Problem Does This Solve?

Traditional payments require upfront capital that's gone forever. YieldFarmPayment allows you to:
- **Pay immediately** — Recipient gets paid right away
- **Recover your capital** — Collateral deposited in Aave V3 generates yield
- **Flexible collateral** — 3x to 20x multiplier (default 20x for ~1 year recovery)
- **DeFi-powered** — Earn yield on Aave V3 while recovering payment costs

## 🚀 Quick Demo

```bash
# Clone and setup
git clone https://github.com/yourusername/yield-farm-payment.git
cd yield-farm-payment
npm install
cp .env.example .env
# Edit .env with your RPC and private key

# Pay 0.1 USDC with default 20x collateral (~1 year recovery)
node scripts/cli.js --amount 0.1 --recipient 0x... --buffer 8
```

## 📊 How Upfront Mode Works

```
1. You want to pay 0.1 USDC to a seller
2. System calculates total required: 0.1 + 0.2 fee + (0.1 × 20x × 1.08 buffer) = 2.46 USDC
3. 0.1 USDC is transferred IMMEDIATELY to seller
4. 0.2 USDC fee is transferred to developer (only after successful steps 3+5)
5. 2.16 USDC is deposited in Aave V3 for recovery
6. Aave generates ~3% APY = 0.0648 USDC/year on the deposit
7. You recover the 0.1 USDC payment in ~565 days (~1.55 years)
8. After recovery, the 2.16 USDC collateral is still yours in Aave
```

### ⚡ Key Insight: Recovery = Payment Amount, NOT Collateral

The amount you need to recover is the **payment sent to the seller** (0.1 USDC), not the total collateral (2.16 USDC). The collateral stays in your Aave position and continues earning yield.

### 📊 Recovery Times by Collateral Multiplier

For a 0.1 USDC payment at 3% APY (conservative estimate):

| Multiplier | Aave Deposit | Annual Yield | Recovery Time |
|------------|-------------|--------------|---------------|
| 3×         | 0.224 USDC  | 0.0067 USDC  | ~15 years     |
| 5×         | 0.440 USDC  | 0.0132 USDC  | ~7.5 years    |
| 10×        | 0.980 USDC  | 0.0294 USDC  | ~3.4 years    |
| **20× (default)** | **2.060 USDC** | **0.0618 USDC** | **~1.6 years** |

**Higher collateral = faster recovery** because more capital in Aave generates more yield.

**Note:** 3% APY is a conservative estimate. Actual Aave V3 rates may vary.

## ✨ Key Features

- **Immediate Payment**: Seller gets paid right away
- **Capital Recovery**: Recover payment cost through Aave yield
- **Flexible Collateral**: 3x to 20x multiplier with configurable buffer
- **Aave V3 Integration**: Deposit USDC to earn yield on Base
- **Robust Transaction Handling**: Automatic retry, gas optimization
- **Professional CLI**: Full-featured command line interface

## 💰 Fee Structure

YieldFarmPayment charges a **fixed 0.2 USDC fee** per successful payment execution:

- **Fixed Amount**: 0.2 USDC (not configurable)
- **Developer Address**: `0x785cF69cEd4E20A7e975A3391d51321b1528Fdfe` (Base Mainnet)
- **Payment Timing**: Fee is transferred **ONLY AFTER** both:
  1. ✅ Payment to recipient succeeds
  2. ✅ Collateral deposit to Aave succeeds
- **Risk-Free**: If any step fails, no fee is charged
- **Transparent**: Fee amount visible in transaction preview before signing

**Why this model?**
- Aligns incentives: Developer gets paid only for successful work
- Reduces risk: User doesn't pay if transaction fails
- Professional: Pay-for-performance model

## 🛠️ Installation

### Prerequisites
- Node.js 18+
- Base network wallet with ETH for gas
- USDC tokens for collateral

### Setup
```bash
npm install
cp .env.example .env
# Edit .env with your configuration
node scripts/check-configuration.js
```

## 📖 Usage

### 🧪 Recommended Testing Workflow
1. **Start with simulation (no funds):**
   ```bash
   node scripts/test-realistic-payment.js
   ```

2. **Validate configuration:**
   ```bash
   node scripts/check-configuration.js
   ```

3. **Test on Base Sepolia (testnet) first:**
   ```bash
   # Update .env with testnet settings:
   # BASE_RPC_URL=https://sepolia.base.org
   # Get test ETH: https://sepolia-faucet.pk910.de/
   # Get test USDC: https://faucet.circle.com/ (select Base Sepolia)
   node scripts/cli.js --amount 0.01 --recipient 0x... --collateral 5 --buffer 8
   ```

4. **Move to Base Mainnet:**
   ```bash
   # Update .env with mainnet settings:
   # BASE_RPC_URL=https://mainnet.base.org
   # Use REAL funds (start small)
   node scripts/cli.js --amount 0.1 --recipient 0x... --buffer 8
   ```

### Default (20x collateral, ~1.6 year recovery)
```bash
node scripts/cli.js --amount 0.1 --recipient 0x... --buffer 8
```

### Custom collateral
```bash
node scripts/cli.js --amount 0.5 --recipient 0x... --collateral 10 --buffer 5
```

### Check configuration
```bash
node scripts/check-configuration.js
```

### Simulation testing (safe - no transactions)
```bash
# Run realistic payment calculations without executing
# Shows recovery times, collateral comparisons, and ready-to-use commands
node scripts/test-realistic-payment.js
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
PRIVATE_KEY=0x...                    # Your wallet private key
BASE_RPC_URL=https://mainnet.base.org  # Base network RPC

# Aave V3 Contracts (Base)
AAVE_V3_POOL_ADDRESS=0xA238Dd80C259a72e81d7e4664a9801593F98d1c5
USDC_ADDRESS=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
AAVE_USDC_TOKEN_ADDRESS=0x4e65fE4DbA92790696d040ac24Aa414708F5c0AB

# Settings
SKILL_FEE_USDC=0.2                   # Fixed 0.2 USDC fee to developer 
DEFAULT_COLLATERAL_MULTIPLIER=20     # 20x for ~1.6 year recovery
DEFAULT_BUFFER_PERCENTAGE=8          # 8% safety buffer
ESTIMATED_APY=0.03                   # 3% conservative APY estimate
```

## 🔒 Security

### ⚠️ CRITICAL SECURITY WARNINGS
- **NEVER use your main wallet**: Create a dedicated wallet with minimal funds
- **Verify all contract addresses** against official Aave/Base documentation
- **Test on Base Sepolia (testnet) first** before using mainnet
- **Audit all scripts locally** before running with real funds
- **Monitor transactions** on [basescan.org](https://basescan.org)

### Technical Protections
- **Balance Verification**: Pre-transaction checks
- **Gas Limit Monitoring**: Prevents excessive fees
- **Transaction Retry**: 3 attempts with gas price escalation
- **Collateral Limits**: 3x minimum, 20x maximum
- **Health Factor Monitoring**: Minimum 2.0 safety margin

## 📈 Roadmap

### v2.0 Planned
- **Standard Mode**: Yield streaming via x402 protocol
- **Smart Mode**: Deadline optimization
- **x402 Integration**: Trustless automatic yield distribution
- **Multi-token Support**: USDT, wETH, etc.

## 📄 License

MIT License

## 🙏 Acknowledgments

- **Aave Protocol** for yield farming infrastructure
- **Base Network** for low-cost L2 execution
- **OpenClaw Community** for skill development framework

---

**YieldFarmPayment v1.0** — Immediate payments with capital recovery on Base network. 🚀

*Built with ❤️ for the OpenClaw community*
