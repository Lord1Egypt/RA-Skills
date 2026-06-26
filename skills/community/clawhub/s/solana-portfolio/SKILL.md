---
name: solana-portfolio
description: 管理 Solana 投资组合 — 追踪多钱包余额、代币分布和资产估值。当用户想查看持仓、添加钱包或了解资产状况时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: ["SOLANA_NETWORK"]
      bins: ["node"]
    emoji: "💼"
---

# Solana 投资组合管理

## When to Use

- 用户想查看投资组合、余额、持仓
- 用户想添加或移除 Solana 钱包地址
- 用户想了解资产分布和总价值
- 用户提到"组合"、"余额"、"持仓"、"钱包"

## Workflow

### 用户想查看投资组合

1. 获取用户的 Telegram User ID
2. 运行 `node skills/solana-portfolio/scripts/get-portfolio.js <user_id>`
3. **如果输出包含 "没有连接的钱包"**：
   - 友善地告知用户还没有连接钱包
   - 主动引导："请发送你的 Solana 钱包地址，我帮你添加"
4. **如果成功返回数据**：
   - 用友善的语气展示结果（总价值、持仓明细）
   - 主动提问："需要设置价格警报吗？" 或 "要看看更详细的行情吗？"

### 用户想添加钱包

1. 如果用户没有提供地址，主动询问："请发送你的 Solana 钱包地址"
2. 验证地址格式（32-44 个字符的 base58 编码）
3. 运行 `node skills/solana-portfolio/scripts/add-wallet.js <user_id> <address>`
4. 确认添加成功后，建议用户查看投资组合

### 用户想列出已连接的钱包

1. 运行 `node skills/solana-portfolio/scripts/list-wallets.js <user_id>`
2. 如果没有钱包，引导添加

### 用户想移除钱包

1. 如果用户没有指定地址，先列出所有钱包让用户选择
2. 确认用户的选择："确定要移除这个钱包吗？"
3. 运行 `node skills/solana-portfolio/scripts/remove-wallet.js <user_id> <address>`

## Guardrails

- **只读操作** — 查看余额不需要私钥，绝不要求用户提供
- **最多 5 个钱包** — 超出时友善提示限制
- **地址验证** — 添加前验证格式，无效时提示正确格式而非报错
- **不评价持仓** — 不说"你的 XXX 持仓太多/太少"，只展示数据

## Available Scripts

| 脚本 | 用途 | 参数 |
|------|------|------|
| `get-portfolio.js` | 查看组合 | `<user_id> [--lang en]` |
| `add-wallet.js` | 添加钱包 | `<user_id> <address>` |
| `list-wallets.js` | 列出钱包 | `<user_id>` |
| `remove-wallet.js` | 移除钱包 | `<user_id> <address>` |
