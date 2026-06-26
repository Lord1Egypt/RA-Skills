---
name: zetachain-helper
description: ZetaChain全链助手：支持全链资产查询、CCTX跨链追踪、zEVM合约部署指南及技术文档索引。
version: 1.0.0
---

# 🚀 ZetaChain Omnichain Helper

这是由 **mango (ZetaChain Technical Ambassador)** 开发的专属技能，旨在让 AI Agent 能够深度理解并操作 ZetaChain 全链生态。

## 🌟 核心功能

1. **Omnichain Status (全链状态)**: 实时查询 ZetaChain 及连接链（ETH, BSC, BTC）的资产平衡。
2. **CCTX Tracker (跨链追踪)**: 输入 Hash 即可追踪全链消息 (CCTX) 的实时进度。
3. **Dev Mentor (技术指导)**: 索引最新 zEVM 开发文档，一键生成部署脚本示例。
4. **Network Watch (网络监控)**: 监控 ZetaChain 主网及测试网的最新升级与提案。

## 🛠 快速开始

### 1. 查询地址全链资产
```bash
python scripts/zeta_tool.py balance <wallet_address>
```

### 2. 追踪跨链交易 (CCTX)
```bash
python scripts/zeta_tool.py track <cctx_hash>
```

## 📅 项目规划 (Roadmap)
- [ ] Phase 1: 基础全链查询逻辑实现
- [ ] Phase 2: 集成 OpenRouter LLM 实现智能技术答疑
- [ ] Phase 3: 发布至 ClawHub 并开源至 GitHub

---
*Created by mango - ZetaChain Technical Ambassador 2026*
