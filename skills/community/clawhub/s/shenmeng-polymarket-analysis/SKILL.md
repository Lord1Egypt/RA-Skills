---
name: polymarket-analysis
description: |
  Polymarket 预测市场数据分析助手。自动抓取市场数据、热门榜单、赔率变化、情绪指标，生成结构化分析报告。

  激活场景：
  - "Polymarket 分析"、"分析 Polamrket"
  - "热门市场有哪些"、"最近什么市场最火"
  - "查看 Polymarket 排行榜"
  - "Polymarket 市场情绪"
  - "预测市场数据分析"
  - "帮我分析某个市场"
---

# Polymarket Analysis Skill

## 功能说明

通过 Polymarket API + 网页抓取，实时获取市场数据并生成分析报告。

## 数据来源

- 主 API：`https://gamma.polymarket.com`
- CLOB API：`https://clob.polymarket.com`
- 官方排行榜：`https://polymarket.com/leaderboard`
- 分类市场：`https://polymarket.com/predictions/{category}`

## 工具使用

**首选工具：`extract_content_from_websites`**
- 直接抓取市场页面结构化数据
- 支持所有 Polymarket 官方页面

**备用工具：`batch_web_search`**
- 搜索最新市场动态和新闻
- 查询特定市场赔率

## 工作流程

### 通用分析流程

1. **确定分析目标** — 用户是问热门市场、特定类别、还是单个市场深度分析？
2. **抓取数据** — 根据目标调用对应 URL
3. **解析关键指标** — 提取赔率(yes/no)、成交量、流动性、参与者数量
4. **生成分析** — 解读数据，给出见解

### 市场概览

使用 `extract_content_from_websites` 抓取：
- `https://polymarket.com/predictions` → 全部热门市场
- `https://polymarket.com/predictions/weekly` → 本周市场
- `https://polymarket.com/leaderboard/overall/weekly/volume` → 周榜

### 分类市场

- `/predictions/crypto` — 加密货币
- `/predictions/trump` — Trump 相关
- `/predictions/btc` — BTC 价格预测
- `/predictions/politics` — 政治
- `/predictions/sports` — 体育

### 单市场深度分析

抓取市场详情页：`https://polymarket.com/event/{slug}`

提取指标：
| 字段 | 含义 |
|------|------|
| yes price | 「是」的概率（0~1）|
| no price | 「否」的概率（0~1）|
| volume | 总成交量（USD）|
| liquidity | 流动池大小 |
| end date | 市场结束时间 |
| shares | 参与者数量 |

## 分析框架

### 热门市场判断标准

1. **成交量** — 越大说明市场越热
2. **流动性** — 决定价格深度和操纵难度
3. **参与者数量** — 参与的人越多，预测越接近群体智慧
4. **距离结算时间** — 越近不确定性越大

### 情绪判断

- **高赞成率（>80%）+ 低成交量** → 可能是庄家控盘，谨慎
- **赔率剧烈波动** → 市场不确定性强，机会与风险并存
- **长期低成交量 + 高流动性池** → 可能是预热市场

### 风险提示

- Polymarket 在中国大陆需要 VPN 访问
- 预测市场不构成投资建议
- 智能合约有清算风险，小额试探为主

## SkillPay 变现配置（可选）

本 Skill 支持接入 SkillPay 实现每次调用自动扣费。

### 配置步骤

1. **注册 SkillPay**：访问 [skillpay.me](https://skillpay.me)，使用钱包登录
2. **创建 Skill**：在 Dashboard 创建新技能，获取：
   - `SKILL_ID`（UUID 格式）
   - `BILLING_API_KEY`（sk_ 开头）
3. **编辑脚本配置**：打开 `scripts/skillpay.py`，替换以下两个值：

```python
BILLING_API_KEY = "sk_your_api_key_here"   # ← 替换这里
SKILL_ID = "your_skill_id_here"             # ← 替换这里
```

4. **重新打包发布**：
```bash
python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /workspace/skill-workspace/polymarket-analysis
# 发布
npx clawhub publish /workspace/skill-workspace/polymarket-analysis \
  --slug shenmeng-polymarket-analysis --version 1.1.0
```

### 扣费参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 单次扣费金额 | 0.001 USDT | 可在 `skillpay.py` 中修改 |
| 分成比例 | 开发者 95% | SkillPay 抽 5% |
| 到账方式 | 即时到钱包 | 无需提现 |

### 扣费流程

```
用户发起分析请求
    ↓
skillpay.py 检查余额
    ↓
余额充足 → 自动扣费 → 执行分析 → 返回结果
    ↓
余额不足 → 返回充值链接 → 用户充值后重试
```

## 输出格式

分析报告包含：
1. **市场概览** — 成交量、流动性、最热门市场
2. **分类亮点** — 各板块最值得关注的市场
3. **深度分析** — 用户指定市场的详细数据
4. **风险提示** — 注意事项
5. **操作建议** — 针对不同类型用户的参考意见
