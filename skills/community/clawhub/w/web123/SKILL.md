---
name: web123
version: 1.1.0
description: "Web3 Skill Navigator / Web3 技能导航站. Describe your need in plain language to get matched AntalphaAI skill recommendations with install commands. Triggers: web123, recommend skill, I want to trade tokens, check wallet balance, Web3 beginner, invest RWA, whale tracking, airdrop, meme token analysis, payment link, what Web3 skills are there, CEX trade, OKX Binance, technical analysis, KOL signal, contract security / 触发词：web123、推荐技能、我想交易代币、查余额、Web3新手、投资理财、聪明钱追踪、空投、meme币分析、收款链接、Web3技能有哪些、CEX交易、OKX、Binance、技术分析、KOL信号、合约安全扫描"
author: Antalpha AI
---

# web123 — Web3 Skill Navigator / Web3 技能导航站

> **"Web3 不会用，就上 web123" / "New to Web3? Start with web123."**
>
> AntalphaAI 官方 18 个 Skill 导航，自然语言匹配推荐
> Official navigator for 18 AntalphaAI skills — match by natural language

---

## Data Source / 数据来源

Skill metadata is stored in `references/skills.json`.
Only skills from the official [AntalphaAI GitHub org](https://github.com/AntalphaAI) are included.

技能元数据存储于 `references/skills.json`，仅收录 AntalphaAI GitHub org 真实发布的仓库。

**18 Skills / 18 个技能（v1.1 新增 5 个）：**

```
🔄 交易 (3)：web3-trader · cex-trader [NEW] · poly-master
💰 投资 (2)：antalpha-rwa-skill · web3-investor
📊 数据 (6)：wallet-balance · transaction-receipt · smart-money · defillama-data-aggregator · ta-radar [NEW] · crypto-social-intel [NEW]
🛡️ 安全 (4)：wallet-guard · anti-rug [NEW] · meme-token-analyzer · airdrop-hunter
💳 支付 (2)：eth-payment · walletconnect-requester
🔧 工具 (2)：antalpha-ai-setup [NEW] · antalpha-ai-docs [NEW]
```

### v1.1 新增技能 / What's New in v1.1

| Skill | 分类 | 亮点 |
|-------|------|------|
| `cex-trader` | 交易 | OKX + Binance 现货/合约，内置风控，API Key 引导配置 |
| `ta-radar` | 数据 | EMA/RSI/MACD/布林带多维技术分析，支持链上合约地址 |
| `crypto-social-intel` | 数据 | KOL 信号、情绪评分、提及量骤增预警、Fear & Greed 指数 |
| `anti-rug` | 安全 | 合约风险深度扫描，蜜罐/Rug Pull 检测，支持 ETH/BSC/Polygon |
| `antalpha-ai-setup` | 工具 | 60+ Web3 工具一键初始化配置向导 |
| `antalpha-ai-docs` | 工具 | 源码驱动 MCP 文档生成，自动对齐最新 API |

同时，`smart-money` 已更新至 v1.2，新增自定义地址订阅（最多 5 个）和 LP 池鲸鱼追踪。

---

## Trigger Conditions / 触发条件

Activate this skill when: / 以下情况触发本 skill：

- User mentions `web123`
- User describes a Web3 need in natural language (e.g. "I want to trade tokens", "check wallet balance")
- User says "Web3 beginner", "starter", "recommend a skill"
- User asks "what Web3 tools are there", "what skills does AntalphaAI have"
- User browses by category (e.g. "safety skills", "trading tools", "CEX trading")

---

## Recommendation Algorithm / 推荐算法 (MVP)

### Weights / 权重

```
tags match      → +3 per match / 每次匹配 +3
scenarios match → +2 per match / 每次匹配 +2
description     → +1 per match / 每次匹配 +1
beginner keyword → +5 bonus / 新手关键词额外 +5
```

### Steps / 步骤

1. Tokenize user input / 将用户输入分词
2. Score all skills by weight + priority / 按权重 + 优先级打分
3. Return Top 3 / 返回 Top 3
4. If beginner keyword detected → return starter pack / 检测到新手词 → 返回新手套装

### Edge Cases / 边界处理

| Situation / 情况 | Action / 处理 |
|-----------------|--------------|
| No match / 无匹配 | Return `hot_skills` Top 3 / 返回热门 Top 3 |
| >3 matches | Sort by score × priority, Top 3 |
| "新手" / "beginner" | Return 新手入门套装 |
| Category browse / 分类浏览 | List all skills in that category / 列出该分类所有技能 |
| "CEX" / "OKX" / "Binance" | Prioritize cex-trader |
| "技术分析" / "TA" / "K线" | Prioritize ta-radar |
| "KOL" / "情绪" / "社交" | Prioritize crypto-social-intel |
| "rug" / "蜜罐" / "合约安全" | Prioritize anti-rug |

---

## Execution Flow / 执行流程

### Step 1: Load Data / 加载数据

Load `references/skills.json` (relative to SKILL.md directory).
读取 `references/skills.json`（相对于 SKILL.md 目录）。

### Step 2: Detect Intent / 意图识别

| Intent / 意图 | Example / 示例 | Action / 处理 |
|--------------|---------------|--------------|
| Need match / 需求匹配 | "I want to trade" / "我想交易" | Keyword match → Top 3 |
| Beginner / 新手入门 | "Web3 beginner" / "新手入门" | Return starter pack / 返回新手套装 |
| Category browse / 分类浏览 | "Safety skills" / "安全类技能" | List category / 列出分类 |
| Exact lookup / 精确查找 | "How to install web3-trader" | Return skill detail / 返回详情 |
| Full list / 全览 | "What skills are there" / "有哪些技能" | Full matrix / 全景矩阵 |

### Step 3: Output / 输出

Use the templates below. / 按下方模板输出。

---

## Output Templates / 输出模板

### Single Skill / 单个推荐

```
🎯 Recommended / 推荐技能：{name}
📝 {description}
💡 Use cases / 使用场景：
- {example_1}
- {example_2}
📦 Install / 安装：{install}
🔗 GitHub：{github}
```

### Top 3 List / Top 3 推荐

```
🔍 Based on your need / 根据你的需求，推荐以下技能：

━━━━━━━━━━━━━━━━━━━
🥇 {name_1} — {description_1}
   💡 {scenario_1}
   📦 {install_1}

🥈 {name_2} — {description_2}
   💡 {scenario_2}
   📦 {install_2}

🥉 {name_3} — {description_3}
   💡 {scenario_3}
   📦 {install_3}
━━━━━━━━━━━━━━━━━━━
💡 Batch install / 批量安装：
openclaw skill install {github_1} {github_2} {github_3}
```

### Starter Pack / 新手套装

```
🎒 {pack_label}
{pack_description}

Includes / 包含 {count} skills:
- {skill_1} — {desc_1}
- {skill_2} — {desc_2}
- {skill_3} — {desc_3}

One-click install / 一键安装：
{install_command}
```

### Full Matrix / 全景产品矩阵

```
🌐 AntalphaAI Skills (18 total / 共 18 个)

🔄 Trading / 交易
  • web3-trader — DEX swap + Hyperliquid perpetuals / DEX聚合交易+合约
  • cex-trader — OKX/Binance spot & futures / CEX现货合约（NEW）
  • poly-master — Polymarket prediction market / 预测市场+套利

💰 Investment / 投资
  • antalpha-rwa — RWA on-chain yield / RWA链上理财
  • web3-investor — DeFi portfolio / DeFi投资组合

📊 Data / 数据
  • wallet-balance — Multi-chain balance / 多链钱包余额
  • transaction-receipt — On-chain tx decoder / 链上交易解析
  • smart-money — Whale tracking + custom watch v1.2 / 聪明钱+自定义监控
  • defillama-data-aggregator — DeFi TVL data / DeFi数据
  • ta-radar — Multi-dim TA: EMA/RSI/MACD / 技术分析雷达（NEW）
  • crypto-social-intel — KOL signals + sentiment / KOL信号+情绪指数（NEW）

🛡️ Safety / 安全
  • wallet-guard — Wallet approval scan / 钱包授权扫描
  • anti-rug — Contract risk scanner / 合约安全深度扫描（NEW）
  • meme-token-analyzer — Meme token analysis / Meme币财富基因
  • airdrop-hunter — Daily airdrop intel / 空投情报日报

💳 Payment / 支付
  • eth-payment — EIP-681 payment links / 收款链接生成
  • walletconnect-requester — WalletConnect v2 / 钱包连接

🔧 Tools / 工具
  • antalpha-ai-setup — 60+ tools setup guide / MCP一键配置向导（NEW）
  • antalpha-ai-docs — Auto MCP docs generator / MCP文档自动生成（NEW）

💬 Tell me what you want to do, I'll recommend the best skill.
   告诉我你想做什么，我来推荐最合适的技能！
```

---

## Quick Reference / 验收速查

| User says / 用户说 | Returns / 推荐 |
|-------------------|--------------|
| "I want to trade tokens" / "我想交易代币" | web3-trader |
| "OKX/Binance 下单" / "CEX 交易" | cex-trader |
| "Check wallet balance" / "查钱包余额" | wallet-balance |
| "Invest in RWA" / "投资RWA" | antalpha-rwa |
| "What are whales buying" / "聪明钱在买什么" | smart-money |
| "BTC 技术分析" / "K 线趋势" | ta-radar |
| "KOL 在讨论什么" / "市场情绪" | crypto-social-intel |
| "Check for rug pull" / "合约风险扫描" | anti-rug |
| "Check for rug pull" / "检测 honeypot" | wallet-guard + anti-rug |
| "Meme 币分析" / "财富基因" | meme-token-analyzer |
| "Airdrop tasks" / "空投任务" | airdrop-hunter |
| "Generate payment link" / "生成收款链接" | eth-payment |
| "配置 Antalpha MCP" / "快速接入" | antalpha-ai-setup |
| "Web3 beginner" / "Web3新手入门" | Starter pack / 新手套装 |
| "Safety skills" / "有哪些安全工具" | Safety category / 安全分类 |
| "All skills" / "有哪些技能" | Full matrix / 全景矩阵 |
| No match / 无匹配 | Hot Top 3 |

---

## Install / 安装

```bash
# Install web123 itself / 安装 web123
openclaw skill install https://github.com/AntalphaAI/web123

# Single skill / 安装单个
openclaw skill install https://github.com/AntalphaAI/web3-trader

# 新手包 / Beginner pack
openclaw skill install https://github.com/AntalphaAI/wallet-balance https://github.com/AntalphaAI/web3-trader https://github.com/AntalphaAI/transaction-receipt

# 交易套装 / Trading pack (v1.1 new)
openclaw skill install https://github.com/AntalphaAI/web3-trader https://github.com/AntalphaAI/cex-trader https://github.com/AntalphaAI/TA-Radar

# 数据情报套装 / Data intel pack (v1.1 new)
openclaw skill install https://github.com/AntalphaAI/smart-money https://github.com/AntalphaAI/crypto-social-intel https://github.com/AntalphaAI/TA-Radar
```

---

*Powered by Antalpha AI · web123 v1.1.0 · github.com/AntalphaAI*
