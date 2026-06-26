---
name: token-approval-checker
description: 钱包授权管理工具，检查 ERC20/ERC721 代币授权风险，识别无限授权和高风险授权。每次调用收取 0.001 USDT。当用户提到"检查授权"、"撤销授权"、"Token Approval"、"高风险授权"、"MetaMask授权"时使用。Wallet authorization management tool for checking ERC20/ERC721 token approval risks. Charges 0.001 USDT per call.
metadata:
  openclaw:
    emoji: "🔐"
  pricing:
    amount: "0.001"
    currency: "USDT"
    chain: "BNB Chain"
    skill_id: "f6a281ea-7575-40f0-a6c3-25068de08bce"
---

# Token Approval Checker / 钱包授权检查器

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Overview

Check and manage your wallet's token approvals. Identify unlimited approvals and high-risk authorizations to protect your assets.

**Pricing**: 0.001 USDT per call

### Supported Blockchains

| Chain | Token Approval Checker |
|-------|------------------------|
| Ethereum | https://etherscan.io/tokenapprovalchecker |
| BSC | https://bscscan.com/tokenapprovalchecker |
| Polygon | https://polygonscan.com/tokenapprovalchecker |
| Arbitrum | https://arbiscan.io/tokenapprovalchecker |
| Optimism | https://optimistic.etherscan.io/tokenapprovalchecker |
| Avalanche | https://snowtrace.io/tokenapprovalchecker |
| Base | https://basescan.org/tokenapprovalchecker |

### Risk Levels

| Level | Icon | Condition | Action |
|-------|------|-----------|--------|
| Critical | 🔴 | Unlimited + Unverified Contract | Revoke Immediately |
| High | 🟠 | Unlimited + Low Liquidity Token | Revoke Recommended |
| Medium | 🟡 | Unlimited + Known Protocol | Consider Revoking |
| Low | 🟢 | Limited Amount + Known Protocol | Can Keep |

### How to Use

```
User: Check my wallet 0x1234...5678 for approval risks
Claude: [Charge 0.001 USDT] → [Analyze approvals] → [Generate risk report]
```

### Revoke Tools

| Tool | Link | Features |
|------|------|----------|
| Revoke.cash | https://revoke.cash | Multi-chain, Recommended |
| Unrekt | https://app.unrekt.net | Batch revoke |
| Etherscan | https://etherscan.io/tokenapprovalchecker | Official tool |

### Known Protocol Whitelist

- **DEX**: Uniswap, SushiSwap, PancakeSwap, 1inch
- **Lending**: Aave, Compound, MakerDAO
- **NFT**: OpenSea, Blur, Magic Eden
- **Staking**: Lido, Rocket Pool

---

<a name="中文"></a>
## 中文

### 概述

检查和管理你的钱包代币授权，识别无限授权和高风险授权，保护资产安全。

**费用**: 每次调用 0.001 USDT

### 支持的区块链

| 链 | Token Approval Checker |
|----|------------------------|
| Ethereum | https://etherscan.io/tokenapprovalchecker |
| BSC | https://bscscan.com/tokenapprovalchecker |
| Polygon | https://polygonscan.com/tokenapprovalchecker |
| Arbitrum | https://arbiscan.io/tokenapprovalchecker |
| Optimism | https://optimistic.etherscan.io/tokenapprovalchecker |
| Avalanche | https://snowtrace.io/tokenapprovalchecker |
| Base | https://basescan.org/tokenapprovalchecker |

### 风险评级标准

| 等级 | 图标 | 条件 | 建议 |
|------|------|------|------|
| 极高危 | 🔴 | 无限授权 + 未验证合约 | 立即撤销 |
| 高危 | 🟠 | 无限授权 + 低流动性代币 | 建议撤销 |
| 中危 | 🟡 | 无限授权 + 知名协议 | 可考虑撤销 |
| 低危 | 🟢 | 有限额度 + 知名协议 | 可保留 |

### 使用方法

```
用户: 检查我的钱包 0x1234...5678 的授权风险
Claude: [扣费 0.001 USDT] → [分析授权] → [生成风险报告]
```

### 撤销授权工具

| 工具 | 链接 | 特点 |
|-----|------|------|
| Revoke.cash | https://revoke.cash | 多链支持，推荐 |
| Unrekt | https://app.unrekt.net | 批量撤销 |
| Etherscan | https://etherscan.io/tokenapprovalchecker | 官方工具 |

### 知名协议白名单

以下协议的授权风险较低：
- **DEX**: Uniswap, SushiSwap, PancakeSwap, 1inch
- **借贷**: Aave, Compound, MakerDAO
- **NFT**: OpenSea, Blur, Magic Eden
- **质押**: Lido, Rocket Pool

---

## SkillPay Billing Integration / 计费接入

```javascript
// ═══════════════════════════════════════════════════
// SkillPay Billing Integration / 计费接入
// ═══════════════════════════════════════════════════

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = 'sk_b82c6ede30fbac400f2ccbaefc57a013270ab0af29e7cd06746511a51977a5aa';
const SKILL_ID = 'f6a281ea-7575-40f0-a6c3-25068de08bce';

// ① Check balance / 查余额
async function checkBalance(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`,
    { headers: { 'X-API-Key': BILLING_API_KEY } }
  );
  const data = await resp.json();
  return data.balance;  // USDT amount
}

// ② Charge per call / 每次调用扣费
async function chargeUser(userId) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: 0.001,  // USDT per call
    }),
  });
  const data = await resp.json();

  if (data.success) {
    return { ok: true, balance: data.balance };
  }

  // Insufficient balance → get payment link
  return { ok: false, balance: data.balance, paymentUrl: data.payment_url };
}

// ③ Generate payment link / 生成充值链接
async function getPaymentLink(userId, amount) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, amount }),
  });
  const data = await resp.json();
  return data.payment_url;  // BNB Chain USDT payment link
}

// ═══════ Usage example / 使用示例 ═══════
async function handleApprovalCheck(userId, walletAddress) {
  const result = await chargeUser(userId);
  if (result.ok) {
    // ✅ Execute skill logic - check approvals
    return await checkWalletApprovals(walletAddress);
  } else {
    // ❌ Insufficient balance, return payment link
    return {
      success: false,
      paymentUrl: result.paymentUrl,
      message: "Insufficient balance / 余额不足"
    };
  }
}
```

---

## Code Example: Manual Revoke / 手动撤销代码

```javascript
const { ethers } = require('ethers');

async function revokeApproval(wallet, tokenAddress, spenderAddress) {
  const ERC20_ABI = ['function approve(address, uint256) external returns (bool)'];
  const token = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);

  // Set allowance to 0 to revoke / 设置额度为 0 即撤销
  const tx = await token.approve(spenderAddress, 0);
  return await tx.wait();
}
```

---

## Important Notes / 注意事项

1. Revoking approvals requires gas fees / 撤销授权需要支付 Gas 费
2. Check approvals regularly (monthly recommended) / 定期检查授权（建议每月一次）
3. Revoke unnecessary approvals after transactions / 交易完成后及时撤销不必要的授权
4. Prefer limited approvals over unlimited / 优先使用有限额度授权而非无限授权
