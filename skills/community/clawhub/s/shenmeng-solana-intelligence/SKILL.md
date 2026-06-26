---
name: solana-intelligence
description: Solana 链上智能分析与机会检测工具。用于分析 Solana 生态项目、检测新兴机会、追踪 Meme币趋势、监控链上数据和提供投资建议。当用户需要分析 Solana 生态、发现新项目、追踪链上机会、获取 Solana 市场情报或进行链上数据分析时触发此 Skill。
---

# Solana 链上智能分析与机会检测

Solana 生态一站式情报中心，整合链上数据分析、新项目发现、Meme币追踪和投资机会识别。

## 核心能力

1. **生态全景分析** - Solana 整体生态健康度、TVL、交易量、活跃地址
2. **新项目发现** - Pump.fun 等发射平台新币监测、早期机会识别
3. **Meme币情报** - 热门 Meme币追踪、趋势分析、风险提示
4. **链上数据洞察** - 钱包行为分析、巨鲸动向、资金流向
5. **AI+Solana 融合** - AI Agent 项目、AI DEX 等新兴赛道追踪

## 快速开始

### 基础查询
- "Solana 生态最近怎么样"
- "分析 BONK/WIF 当前情况"
- "有什么新的 Solana 项目值得关注"

### 进阶分析
- "检测 Solana 上的新机会"
- "分析 Pump.fun 发射趋势"
- "追踪 Solana 巨鲸动向"

## 数据来源

- **链上数据**: DefiLlama, Dune Analytics, Solscan
- **市场数据**: CoinGecko, CoinMarketCap
- **发射平台**: Pump.fun, LetsBONK.fun, Boop.fun
- **社交情报**: Twitter/X, Discord 社区热度

## 分析框架

### ME2F 分析模型
用于评估 Meme币/新项目的风险与机会:
- **M**arket Cap - 市值大小与增长空间
- **E**ngagement - 社区活跃度与社交热度
- **E**fficiency - 资金效率与流动性质量
- **F**ounders - 团队背景与代币分配

### 机会检测信号
1. 🔥 **热点信号** - 社交媒体提及量激增、KOL 关注
2. 💰 **资金信号** - 巨鲸入场、大额交易、流动性增加
3. 🆕 **新币信号** - 新发射项目、创新机制、独特叙事
4. 🤖 **AI 融合** - AI Agent 集成、智能化功能

## 参考资源

### 生态系统参考
查看 [references/ecosystem.md](references/ecosystem.md) 了解:
- Solana 蓝筹 Meme币列表
- 主要 DeFi 协议数据
- 发射平台对比
- AI+Solana 项目

### API 与工具参考
查看 [references/api-reference.md](references/api-reference.md) 了解:
- 常用 API 端点和调用方法
- 链上数据分析脚本
- 代币健康度评分算法
- 风险等级评估方法

### 发射平台指南
查看 [references/launchpad-guide.md](references/launchpad-guide.md) 了解:
- Pump.fun Bonding Curve 机制详解
- 新币评估完整清单
- 风险信号识别
- 机会识别策略

## 分析脚本

### 代币分析器
`scripts/token_analyzer.py` - 全面分析 Solana 代币:
```bash
python3 scripts/token_analyzer.py
```
功能:
- 计算代币健康度评分 (0-100)
- 评估风险等级 (LOW/MEDIUM/HIGH/EXTREME)
- 识别风险因素
- 检测机会信号
- 生成投资建议

### 生态监控器
`scripts/ecosystem_monitor.py` - 监控 Solana 生态指标:
```bash
python3 scripts/ecosystem_monitor.py
```
功能:
- 获取 TVL 数据
- 列出顶级协议
- 生成市场概览报告

## 使用场景

### 场景1: 日常市场监控
用户想了解 Solana 生态整体状况:
→ 提供 TVL、交易量、活跃地址等核心指标
→ 总结当日/当周重大事件和趋势
→ 使用 `scripts/ecosystem_monitor.py` 获取数据

### 场景2: 新项目评估
用户询问某个新发射的代币:
→ 使用 ME2F 模型分析
→ 检查合约安全性、代币分配、团队背景
→ 给出风险提示和投资建议
→ 参考 `scripts/token_analyzer.py` 的分析框架

### 场景3: 机会挖掘
用户希望发现早期机会:
→ 扫描发射平台新项目
→ 识别异常交易模式
→ 推荐值得关注的标的
→ 查阅 `references/launchpad-guide.md` 的机会识别策略

### 场景4: 生态项目对比
用户想对比多个 Solana 项目:
→ 使用 `references/ecosystem.md` 中的项目数据
→ 对比 TVL、交易量、社区规模等指标
→ 提供差异化分析

## 风险提示

⚠️ **高风险警告**:
- 99% 的 Solana 新币在 3-7 天内归零
- 内幕钱包常控盘 30-50%
- Meme币无基本面支撑，纯情绪驱动
- 监管不确定性（SEC 2026年加强执法）

## 相关 Skill

- `crypto-trend-analyzer` - 虚拟币概念前瞻分析
- `dex-price-monitor` - DEX 价格监控与套利
- `whale-alert-monitor` - 鲸鱼钱包监控
- `social-sentiment-monitor` - 社交媒体情绪监控

## 更新记录

- v1.0.0 - 初始版本，基础 Solana 生态分析能力
  - 生态监控脚本
  - 代币分析框架
  - Pump.fun 发射指南
  - 完整项目参考数据库
