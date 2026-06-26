---
name: sentry-ai
description: Solana/Base Multi-Chain Meme Scanner & Auditor (Anti-Rug)
metadata:
  {
    "openclaw": {
      "emoji": "🛡️",
      "requires": { "env": [], "bins": [], "skills": [] },
      "install": []
    }
  }
---

# Sentry-AI: Multi-Chain Meme Scanner & Auditor

赋予你的 OpenClaw 顶级"科学家"的嗅觉。

## 简介

本插件专为一级市场玩家设计，集成全自动合约静态审计与链上动态监控。通过 LLM 逻辑判断，秒级识别"貔貅盘"与"老鼠仓"。

## 核心功能

### Auto-Scan
- 毫秒级接入 DexScreener/Raydium 新池子流
- 实时监控 Solana/Base 链新代币

### Risk Score
- 基于代码安全性加权评分
- 流动性占比分析
- 社交媒体增长率监测

### One-Click Execute
- 支持配置止盈止损逻辑
- 智能 Gas 优化

## 支持链

- Solana
- Base
- Ethereum (Coming Soon)

## 使用方法

```bash
# 扫描新池子
python scripts/scan.py

# 检查特定代币
python scripts/audit.py <TOKEN_ADDRESS>
```

## 定价

- 免费版：基础扫描
- Pro版 ($19.9/月)：完整审计 + 实时推送

---
*Powered by OpenClaw*
