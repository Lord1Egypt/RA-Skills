---
name: sharkflow
description: ⚡ SharkFlow - 链上任务自动化，智能合约交互队列 + 多签工作流
version: 0.1.0
author: gztanht
license: MIT
tags: [task, workflow, multisig, defi, automation, shark]
pricing:
  free_tier: 5 tasks/day
  sponsorship: 0.5 USDT or 0.5 USDC for unlimited
  note: "Feel free to sponsor more if you find it useful!"
wallet:
  usdt_erc20: "0x33f943e71c7b7c4e88802a68e62cca91dab65ad9"
  usdc_erc20: "0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44"
metadata:
  clawdbot:
    emoji: ⚡
    requires:
      bins: [npm, node]
---

# ⚡ SharkFlow - 链上任务自动化

**Automate Your On-Chain Workflow** - 闪电般高效执行！

## Overview

SharkFlow 是专为 DeFi 用户设计的任务管理工具，支持智能合约交互队列、多签工作流、定时任务执行等功能。批量操作、自动化执行，解放你的双手。

## Features

- 📋 **任务队列** - 批量添加链上操作，一键执行
- 🔐 **多签支持** - 多签名钱包工作流管理
- ⏰ **定时任务** - 设定时间自动执行（如定投、复投）
- 📊 **历史追踪** - 完整的任务执行历史
- 🔔 **完成提醒** - Telegram/邮件通知
- 🔄 **模板系统** - 保存常用操作模板

## Installation

```bash
npx @gztanht/sharkflow
```

## Usage

### 创建任务

```bash
# 添加 USDT 存款任务
node scripts/flow.mjs add --action deposit --token USDT --amount 1000 --platform aave

# 添加 ETH 兑换任务
node scripts/flow.mjs add --action swap --from ETH --to USDC --amount 0.5

# 添加批量任务
node scripts/flow.mjs batch --file tasks.json
```

### 执行任务

```bash
# 执行队列中的任务
node scripts/flow.mjs execute

# 执行特定任务
node scripts/flow.mjs execute --id 123

# 模拟执行（不实际提交）
node scripts/flow.mjs execute --dry-run
```

### 多签工作流

```bash
# 创建多签任务
node scripts/flow.mjs multisig create --required 3 --signers 0x123,0x456,0x789

# 签名任务
node scripts/flow.mjs multisig sign --taskId 123

# 查看签名状态
node scripts/flow.mjs multisig status --taskId 123
```

### 定时任务

```bash
# 设置每周一定投
node scripts/flow.mjs schedule --action deposit --amount 100 --recur weekly --day monday

# 查看定时任务
node scripts/flow.mjs schedule --list
```

## Supported Actions

| 操作 | 描述 | 支持平台 |
|------|------|----------|
| deposit | 存款 | Aave, Compound, Spark |
| withdraw | 取款 | Aave, Compound, Spark |
| swap | 代币兑换 | Uniswap, Curve, 1inch |
| stake | 质押 | Lido, Rocket Pool |
| claim | 领取奖励 | 所有 yield 平台 |
| bridge | 跨链 | Stargate, Hop, Across |

## Configuration

编辑 `config/wallets.json` 添加钱包：

```json
{
  "wallets": [
    {"name": "Main", "address": "0x...", "type": "EOA"},
    {"name": "Safe", "address": "0x...", "type": "Safe", "required": 2, "signers": [...]}
  ]
}
```

## Safety

- ✅ 模拟执行 - 实际提交前预览结果
- ✅ 限额设置 - 单笔/每日交易限额
- ✅ 白名单 - 只允许预定义的合约交互
- ✅ 多签确认 - 大额交易需要多签

## Support

- 📧 Email: support@SharkFlow.shark
- 💬 Telegram: @SharkFlowBot
- 🦈 赞助：USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`

## License

MIT © 2026 gztanht
