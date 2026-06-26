# 📊 Stock Realtime Brief

> **A股实时分析与可执行操作建议生成器** — 把"凭感觉看盘"升级为"按规则执行"的纪律工具。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Market: A-Share](https://img.shields.io/badge/Market-A--Share-red.svg)]()
[![Skill: OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-brightgreen.svg)](https://clawhub.ai)
[![Tests](https://github.com/Michaelliugh/stock-realtime-brief/actions/workflows/test.yml/badge.svg)](https://github.com/Michaelliugh/stock-realtime-brief/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/Michaelliugh/stock-realtime-brief/branch/main/graph/badge.svg)](https://codecov.io/gh/Michaelliugh/stock-realtime-brief)

中文 | [English](./README_EN.md)

![demo](./docs/images/demo.gif)

---

## ✨ 它能做什么

针对 A 股市场，**根据用户输入的不同形态自动切换三种分析模式**：

| 模式 | 触发场景 | 输出 |
|:---:|---------|------|
| 📦 **Portfolio** | 给定持仓文件 | 完整盘前简报：实时态势 + 关键均线 + 三档硬止损 + 融资风险体检 + 重要公告告警 + 优先级操作清单 |
| 🔍 **Single** | 单只股票 | 单股深度分析：态势速判 + 技术面 + 5 档操作位（介入/加仓/止损/短线止盈/波段止盈） |
| 📊 **Multi** | 多只股票 | 横向对比表：综合评分排序 + 关键差异点 + ⭐/🟡/⚠️ 标签 |

**自动模式**：根据输入数量自动选择 — 1 只走 Single，多只走 Multi，有 portfolio 文件走 Portfolio。

## 📸 输出示例

<table>
<tr>
<td width="33%"><b>🔍 单股深度分析</b><br><img src="./docs/images/sample_single.png" alt="Single mode sample"></td>
<td width="33%"><b>📊 多股对比分析</b><br><img src="./docs/images/sample_multi.png" alt="Multi mode sample"></td>
<td width="33%"><b>📦 持仓简报</b><br><img src="./docs/images/sample_portfolio.png" alt="Portfolio mode sample"></td>
</tr>
</table>

---

## 🚀 30 秒快速开始

### 1. 安装

```bash
git clone https://github.com/<你的用户名>/stock-realtime-brief.git
cd stock-realtime-brief
pip install -r requirements.txt
```

### 2. 单股分析（最简单）

```bash
python -m stock_realtime_brief --code 300750
```

输出示例：
```
🔍 宁德时代 300750 实时分析 — 2026-05-06 14:30

## 一、态势速判
**📈 多头排列，趋势向上**

## 二、技术面
- 现价: **256.78** | 涨跌幅: **+2.31%** | 换手: 1.85% | 成交额: 8.93 亿
- 均线: MA5=251.20 MA10=247.45 MA20=240.12 MA30=235.67
- 近 N 日: 高 **268.50** / 低 **210.30**
- 40 日涨幅: **+18.45%**
...
```

### 3. 多股对比

```bash
python -m stock_realtime_brief --codes 600519,300750,600036
```

### 4. 持仓简报

```bash
# 复制示例配置
cp examples/portfolio_demo.json my_portfolio.json
# 编辑成你自己的持仓
vim my_portfolio.json
# 跑简报
python -m stock_realtime_brief --portfolio my_portfolio.json
```

---

## 🎯 核心特性

### ⭐ 三档硬止损纪律

不是"建议关注"那种空话，而是**写进券商条件单就能直接执行**的具体价位：

| 档位 | 价位逻辑 | 动作 |
|:---:|---------|------|
| **预警线** | MA5（一般）/ MA10（重仓）+ 利润保护位 | 减 1/3 |
| **风控线** | MA10（一般）/ MA20（重仓）/ max(MA20, 成本-15%) | 再减 1/3 |
| **清仓线** | MA20 / 成本-25%（亏损） | 全清 |

### ⭐ 数据源容错策略

A 股数据源时不时抽风。本工具按**实战验证的可靠性顺序**降级：

```
腾讯财经（最稳）→ 新浪财经批量 → AKShare（带 timeout）
```

> **踩过的坑**：AKShare 主源 `82.push2.eastmoney.com` 在交易日早盘经常超时（实测可达 50 分钟无响应）。本工具默认**先腾讯**，避开这个深坑。

### ⭐ 重要公告自动检测

跑持仓简报时自动并行拉取 **近 14 日重要公告**，识别 **HIGH / MED 两级利空**：

- 🔴 **HIGH**：减持公告 / 立案调查 / 业绩预减 / 处罚警示 / 诉讼...
- 🟡 **MED**：解禁 / 收购 / 重组 / 股东大会 / 业绩预告...

公告输出会**置顶展示**，提醒"在技术面分析之上调整出手节奏"。

### ⭐ 融资融券风险体检（A 股专属）

A 股融资融券是普通组合工具普遍忽视的重大风险。本工具：

- 自动算 **担保比例**（基于持仓 + 融资余额）
- 五档预警：✅ 安全 / 🟡 可控 / ⚠️ 警戒 / 🚨 强警告 / 🚨🚨🚨 接近强平
- 提供**还款顺序建议**

### ⭐ 多股综合评分

模式 M 的轻量打分系统，**让"哪个更值得关注"有明确依据**：

```
score = 当日涨跌幅 ÷ 2
       + MA5 偏离度 × 1.5  （短期强弱）
       + MA20 偏离度 × 1   （中期趋势）
       + 量价共振分（放量涨 +2 / 放量跌 -2）
```

---

## 📚 设计理念

### "规则比感觉重要"

这个工具的核心信念：**散户最大的敌人不是市场，是自己的情绪。**

- ❌ "建议谨慎操作" → ✅ "跌破 500 减 1/2"
- ❌ "情绪面不佳" → ✅ "成交 4.79 亿，量比 0.62（早盘缩量）"
- ❌ "目标价 600" → ✅ "止损 482 / 止盈 1: 539 / 止盈 2: 588"

每一条建议**都带触发条件**，让"白天忙、情绪波动、错过最佳点"的散户也能稳定执行。

### 7 步法

```
Step 1  解析输入 → 识别模式 + 提取股票代码
Step 2  拉实时行情 → 优先腾讯接口（最稳）
Step 3  拉历史 K 线 → AKShare stock_zh_a_hist (qfq, 近 60 日)
Step 4  计算关键位 → MA5/10/20/30 + 近 N 日高低 + 量能
Step 5  判断态势 → 杀跌 / 冲高 / 震荡 / 趋势上行 / 趋势下行
Step 6  生成操作位 → 止损位（P/S）或 排序推荐（M）
Step 7  模式专属动作 → P:融资体检 + 公告 / S:深度分析 / M:横向对比
```

详见 [docs/methodology.md](./docs/methodology.md)。

---

## 🛠 配置

### 三层路径优先级

`portfolio.json` 路径按以下顺序解析：

1. **命令行参数** `--portfolio path/to/file.json`
2. **环境变量** `STOCK_BRIEF_PORTFOLIO`
3. **当前目录** `./portfolio.json`

### 持仓文件格式

```json
{
  "margin_debt": 0,
  "positions": [
    {
      "symbol": "300750",
      "name": "宁德时代",
      "buy_price": 220.0,
      "amount": 500,
      "account": "普通",
      "sector": "新能源"
    }
  ]
}
```

完整示例见 [`examples/portfolio_demo.json`](./examples/portfolio_demo.json)，模板见 [`examples/portfolio_template.json`](./examples/portfolio_template.json)。

---

## 📁 项目结构

```
stock-realtime-brief/
├── src/stock_realtime_brief/
│   ├── cli.py              # 主入口
│   ├── data_sources.py     # 数据源策略
│   ├── indicators.py       # 均线/止损位计算
│   ├── analyzers.py        # 三种模式分析
│   ├── announcements.py    # 公告拉取
│   ├── renderers.py        # Markdown 输出
│   └── portfolio.py        # 持仓加载
├── examples/               # 示例配置
├── tests/                  # 单元测试
├── docs/                   # 详细文档
└── SKILL.md                # OpenClaw skill 主文档
```

---

## 🔌 集成

### 作为 Python 库

```python
from stock_realtime_brief import analyze_single, analyze_multi, analyze_portfolio

# 单股
result = analyze_single('300750')
print(result.markdown)

# 多股
result = analyze_multi(['600519', '300750', '600036'])
print(result.markdown)

# 持仓
result = analyze_portfolio('my_portfolio.json')
print(result.markdown)
```

### 作为 OpenClaw Skill

把 `SKILL.md` 与 `src/` 复制到你的 OpenClaw skills 目录即可：

```bash
cp -r . ~/.openclaw/workspace/skills/stock-realtime-brief/
```

详见 [SKILL.md](./SKILL.md)。

### 作为 Hermes Agent Skill

```bash
cp -r . ~/.hermes/skills/stock-realtime-brief/
```

---

## 🗓 路线图

- [x] v2.2 — 三模式 + 数据源容错 + 公告检测 + 融资体检
- [ ] v2.3 — 板块比较模式（自动识别 CPO / 半导体 / 新能源板块）
- [ ] v2.4 — 历史回测模块（验证三档止损规则的有效性）
- [ ] v2.5 — 港美股支持
- [ ] v3.0 — Web Dashboard（可视化）

---

## 🤝 贡献

欢迎 PR！请先看 [CONTRIBUTING.md](./CONTRIBUTING.md)。

特别欢迎以下贡献：
- 新数据源适配（如东方财富 / 同花顺）
- 新指标（KDJ / MACD / RSI 等）
- 多语言文档翻译
- Bug 修复 + 测试用例

---

## ⚠️ 免责声明

**本工具仅用于辅助分析，不构成任何投资建议。**

- 输出内容基于公开数据 + 既定算法，**不代表任何专业意见**
- 股票市场有风险，投资需谨慎
- 使用本工具产生的任何盈亏与作者无关
- 详见 [DISCLAIMER.md](./DISCLAIMER.md)

---

## 📜 License

[MIT](./LICENSE) © 2026

---

## 🌟 Star History

如果这个工具帮到了你，请给个 ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=Michaelliugh/stock-realtime-brief&type=Date)](https://star-history.com/#Michaelliugh/stock-realtime-brief&Date)
