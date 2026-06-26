---
name: daily-market-report
description: Generate automated daily market reports for Chinese futures markets. Summarize sector performance, top movers, volume/OI changes, and produce formatted end-of-day summaries for distribution or PDF conversion.
emoji: 📰
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars: []
    dependencies:
      skills:
        - china-commodity-quotes
---

# Daily Market Report — 期货市场每日行情日报

Generate structured, professional daily reports covering Chinese commodity futures, financial index futures, and shipping index markets.

**Use this skill when:**
- User asks for "日报", "收盘总结", "日盘回顾", "每日行情汇总"
- End of trading day (15:00 CST or night session close)
- User wants a formatted market summary to share or distribute
- User asks "今天哪些品种涨得最好" or "今天的大跌是什么原因"

## Report Workflow

### Step 1: Gather Data

Use `china-commodity-quotes` skill to fetch all major contracts. Recommended data points per contract:

| Field | Source |
|:------|:-------|
| Current price | Sina Finance API / browser snapshot |
| Open | Sina Finance API |
| High / Low | Sina Finance API |
| Previous settlement | Sina Finance API |
| Volume | Sina Finance API |
| Open interest | Sina Finance API |
| Change % | Calculated: (current - prev_settlement) / prev_settlement × 100 |

**Primary contracts to cover:**

| Sector | Contracts | Exchange |
|:-------|:----------|:---------|
| Financials | IF, IC, IH, IM (main month) | CFFEX |
| Metals | CU, AL, AU, AG (main month) | SHFE |
| Ferrous | I, RB, HC (main month) | DCE / SHFE |
| Energy | SC, LU (main month) | INE |
| Chemical | MA, TA, SA, EG (main month) | ZCE / DCE |
| Agricultural | C, M, Y, P, SR, CF (main month) | DCE / ZCE |
| Shipping | EC (main month) | INE |

**Bulk data fetch (quick method):**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,CU0,AL0,AU0,AG0,I0,RB0,HC0,SC0,LU0,MA0,TA0,SA0,EG0,C0,M0,Y0,P0,SR0,CF0,EC0"
```

### Step 2: Calculate Statistics

For each contract, compute:
- **涨跌幅 (Change %):** (current - prev_settle) / prev_settle × 100
- **振幅 (Range %):** (high - low) / prev_settle × 100
- **成交额 (Turnover):** volume × price × contract_multiplier
- **持仓变化 (OI Change):** current_OI - prev_OI (requires 2 data points)
- **涨跌比 (Advance/Decline):** Across all tracked contracts

### Step 3: Structure the Report

### Step 4: Output Format

## Report Template

```
═══════════════════════════════════════════
  📰 中国期货市场日报
  China Futures Daily Market Report
═══════════════════════════════════════════
  📅 YYYY-MM-DD (周X)
  🕐 日盘 + 夜盘收盘
───────────────────────────────────────────

━━━ 1. 市场概况 ━━━

📊 今日总览
  ● 跟踪品种:  40个
  ● 上涨品种:  25个 (62.5%) 🟢
  ● 下跌品种:  12个 (30.0%) 🔴
  ● 持平品种:   3个 (7.5%)  ⚪
  ● 涨跌比:    2.08:1

📈 涨幅TOP5
  1. EC (集运欧线)  +3.85%  — 即期运价反弹
  2. J  (焦炭)       +2.50%  — 焦化厂提涨
  3. AG (白银)       +2.30%  — 外盘贵金属走强
  4. CU (铜)         +1.85%  — LME铜库存下降
  5. I  (铁矿石)     +1.60%  — 钢厂补库

📉 跌幅TOP5
  1. SA (纯碱)       -3.20%  — 累库压力
  2. MA (甲醇)       -2.40%  — 港口库存偏高
  3. C  (玉米)       -1.80%  — 新粮上市预期
  4. RM (菜粕)       -1.50%  — 需求疲弱
  5. EG (乙二醇)     -1.30%  — 装置重启

━━━ 2. 板块表现 ━━━

🏦 金融股指 | 涨跌: +0.85% | 成交额: ¥2850亿
  ● IF (沪深300):  +0.95% → 3840.2
  ● IC (中证500):  +0.72% → 5620.0
  ● IH (上证50):   +0.88% → 2550.5
  ● IM (中证1000): +0.65% → 6180.0

🥇 贵金属 | 涨跌: +1.85% | 成交额: ¥420亿
  ● AU (黄金):  +1.20% → 580.30
  ● AG (白银):  +2.30% → 7850.0

🛢️ 能源化工 | 涨跌: -0.65% | 成交额: ¥850亿
  ● SC (原油):      -0.80% → 520.0
  ● MA (甲醇):      -2.40% → 2450.0
  ● TA (PTA):       -0.30% → 5820.0
  ● SA (纯碱):      -3.20% → 1550.0
  ● EG (乙二醇):    -1.30% → 4620.0

⚙️ 黑色系 | 涨跌: +0.75% | 成交额: ¥620亿
  ● I (铁矿石):    +1.60% → 780.0
  ● RB (螺纹钢):    +0.40% → 3720.0
  ● J (焦炭):      +2.50% → 2350.0
  ● JM (焦煤):      +1.80% → 1450.0
  ● HC (热卷):      +0.50% → 3850.0

🌾 农产品 | 涨跌: +0.30% | 成交额: ¥380亿
  ● C (玉米):       -1.80% → 2450.0
  ● M (豆粕):       +0.60% → 3020.0
  ● Y (豆油):       +0.80% → 8250.0
  ● P (棕榈油):     +1.20% → 7650.0
  ● SR (白糖):      -0.20% → 5950.0
  ● CF (棉花):      -0.40% → 14200.0

🚢 航运 | 涨跌: +3.85% | 成交额: ¥95亿
  ● EC (集运欧线): +3.85% → 3850.0

━━━ 3. 市场异动 ⚡ ━━━

🔺 异动上涨:
  ● EC 集运欧线 +3.85% — 即期运价指数反弹，船公司提价
  ● AG 白银 +2.30% — 外盘突破，避险情绪升温
  ● J 焦炭 +2.50% — 焦化厂开启第二轮提涨

🔻 异动下跌:
  ● SA 纯碱 -3.20% — 库存连续3周累积创新高
  ● MA 甲醇 -2.40% — 港口到港增加
  ● C 玉米 -1.80% — 新粮上市预期施压

━━━ 4. 资金流向 ━━━

💰 资金流入TOP3 (持仓量增加):
  1. CU铜:  +12,500 手
  2. IF沪深300: +8,200 手
  3. SC原油: +6,500 手

💸 资金流出TOP3 (持仓量减少):
  1. SA纯碱: -18,000 手
  2. RB螺纹钢: -9,500 手
  3. MA甲醇: -7,000 手

━━━ 5. 明日关注 ━━━

📅 重要事件:
  1. 09:30 中国公布5月PMI数据
  2. 20:30 美国初请失业金人数
  3. LME铜库存数据更新

🔮 技术面提示:
  ● IF2606: MACD金叉延续，关注3850压力位
  ● SA2609: 超卖区域，关注1500整数关口支撑
  ● EC2608: 强势突破，顺势偏多

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 报告生成时间: YYYY-MM-DD HH:MM
⚡ 数据来源: 新浪财经 / 各交易所
```

## Scripts

### `scripts/report_generator.py`
Daily report generation helper:
- `fetch_all_quotes()` — Bulk fetch all major contracts
- `calc_sector_averages(contracts)` — Calculate sector-level aggregates
- `rank_by_change(contracts)` — Top gainers/losers ranking
- `detect_anomalies(contracts)` — Spot unusual volume/price moves
- `generate_markdown_report(data)` — Build the full report template
- `export_pdf(markdown_path)` — Convert markdown to PDF (via pandoc/weasyprint)

## Export Options

### Simple Markdown (Default)
Output as structured markdown, ready for:
- Copy-paste to WeChat/Flying book
- Save as `.md` file
- Future conversion

### PDF Conversion (if available)
```bash
# Using pandoc + wkhtmltopdf
pandoc report.md -o report.pdf --pdf-engine=wkhtmltopdf

# Using python with weasyprint
python -c "
from weasyprint import HTML
HTML(string=open('report.md').read()).write_pdf('report.pdf')
"
```

## Notes

- Best generated after 15:30 CST (日盘 close + data settling)
- Include night session data if report is generated the next morning
- Use `approx` for turnover: volume × price × contract_multiplier (simplified)
- OI change requires comparing to previous day; for first run, mark as "N/A"
- For WeChat/Discord delivery, use the AGENTS.md formatting rules (bullet lists, no tables)
