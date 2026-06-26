# 🛡️ Sentry-AI

Multi-Chain Meme Scanner & Auditor (Anti-Rug)

## 概述

Sentry-AI 赋予你的 OpenClaw 顶级"科学家"的嗅觉。本插件专为一级市场玩家设计，集成全自动合约静态审计与链上动态监控。

## 功能

### 🔍 Auto-Scan
- 毫秒级接入 DexScreener 新池子流
- 实时监控 Solana/Base 链新代币

### 📊 Risk Score
- 基于代码安全性加权评分
- 流动性占比分析
- 社交媒体增长率监测

### ⚡ One-Click Execute
- 支持配置止盈止损逻辑
- 智能 Gas 优化

## 支持链

- ✅ Solana
- ✅ Base
- 🔜 Ethereum

## 安装

```bash
clawhub install sentry-ai
```

## 使用方法

### 扫描新池子
```bash
python scripts/scan.py
```

### 审计代币
```bash
python scripts/audit.py <TOKEN_ADDRESS>
```

## 输出示例

```
[SENTRY-AI] Starting scan...
Found 15 pools

[SAFE] PEPE - Risk Score: 85/100
  Liquidity: $250,000
  URL: https://dexscreener.com/...
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| Free | $0 | 基础扫描 |
| Pro | $19.9/月 | 完整审计 + 实时推送 |

## 注意

本插件仅供教育和研究目的。使用前请自行承担风险。

---
*Powered by OpenClaw* 🦞
