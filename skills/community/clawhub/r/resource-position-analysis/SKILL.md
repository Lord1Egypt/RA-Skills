---
name: resource-position-analysis
slug: resource-position-analysis
version: "1.0.0"
description: >-
  Analyze conversion funnel data for frontend resource positions (banners, cards, popups)
  from exposure, click, and business conversion dimensions. Decompose data fluctuations
  into factor contributions using Sequential Substitution method, generate key findings
  and actionable recommendations. Supports day-over-day, week-over-week, and custom
  period comparison with multi-position cross-analysis. Use when the user mentions
  resource position analysis, conversion funnel, exposure/click/conversion fluctuation,
  or 资源位分析、转化漏斗、波动归因、数据波动分析.
changelog: "Initial release with funnel decomposition, multi-period comparison, and multi-position analysis."
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"]},"os":["linux","darwin"],"configPaths":[]}}
---

# 资源位转化数据波动分析

对前端资源位（banner、卡片、弹窗等）的曝光→点击→业务转化漏斗进行波动归因分析，定位数据波动的主要驱动因素，输出结构化分析报告。

## 前置条件

- Python 3.8+
- 依赖会由脚本自动检测，缺失时提示安装命令

## 定位脚本路径

**重要**：分析脚本位于本 SKILL.md 同级目录的 `scripts/analyze.py`。

运行前先确定本 SKILL.md 的绝对路径，然后拼出脚本路径：

```bash
# 假设 SKILL.md 位于 /path/to/skills/resource-position-analysis/SKILL.md
# 则脚本路径为:
SCRIPT="/path/to/skills/resource-position-analysis/scripts/analyze.py"
python3 "$SCRIPT" <excel_file> --mode <mode> [options]
```

常见安装位置：
- ClawHub 安装: `./skills/resource-position-analysis/scripts/analyze.py`
- 个人技能: `~/.cursor/skills/resource-position-analysis/scripts/analyze.py`

## 数据格式

用户需提供 Excel 文件，包含以下字段（支持中英文列名）：

| 必需字段 | 中文别名 | 说明 |
|---------|---------|------|
| date | 日期 | 日期列 |
| resource_position | 资源位/资源位名称/位置 | 资源位标识 |
| exposure_uv | 曝光UV/曝光人数 | 曝光独立用户数 |
| click_uv | 点击UV/点击人数 | 点击独立用户数 |
| conversion_count | 转化量/业务转化量/转化数 | 业务转化绝对量 |

可选字段：`exposure_pv`, `click_pv`, `channel`, `segment`

## 分析流程

### Step 1: 确认数据和对比周期

支持三种对比模式：

| 模式 | 参数 | 说明 |
|------|------|------|
| 日环比 | `--mode dod --date YYYY-MM-DD` | 指定日期 vs 前一天 |
| 周同比 | `--mode wow --date YYYY-MM-DD` | 指定日期 vs 上周同天 |
| 自定义 | `--mode custom --base-start ... --base-end ... --compare-start ... --compare-end ...` | 任意两段时间 |

### Step 2: 运行分析

```bash
# 日环比
python3 "$SCRIPT" data.xlsx --mode dod --date 2026-03-25

# 周同比
python3 "$SCRIPT" data.xlsx --mode wow --date 2026-03-25

# 自定义区间
python3 "$SCRIPT" data.xlsx --mode custom \
  --base-start 2026-03-18 --base-end 2026-03-24 \
  --compare-start 2026-03-11 --compare-end 2026-03-17

# 指定资源位
python3 "$SCRIPT" data.xlsx --mode dod --date 2026-03-25 --position "头部banner,福利卡片"

# 输出到文件
python3 "$SCRIPT" data.xlsx --mode dod --date 2026-03-25 --output report.md
```

### Step 3: 解读报告

脚本输出 Markdown 报告包含：

1. **数据概览** — 本期/上期核心指标对比表
2. **波动归因** — 各因素（曝光/CTR/CVR）贡献量和占比
3. **多资源位对比** — 各资源位波动方向和主因横向对比
4. **关键发现** — 自动识别的重要信号
5. **后续建议** — 基于波动因素的针对性运营建议

## 核心方法论：连环替代法

漏斗公式：`业务转化量 = 曝光UV × CTR × CVR`

```
曝光贡献 = (Exp₁ - Exp₀) × CTR₀ × CVR₀
CTR贡献  = Exp₁ × (CTR₁ - CTR₀) × CVR₀
CVR贡献  = Exp₁ × CTR₁ × (CVR₁ - CVR₀)
贡献占比 = 贡献量 / 总变化量 × 100%
```

## 建议映射规则

| 主因 | 方向 | 建议 |
|------|------|------|
| 曝光UV | 下降 | 排查流量分配策略、资源位可见性、页面改版影响 |
| 曝光UV | 上升 | 关注新增流量质量，观察CTR/CVR是否同步变化 |
| CTR | 下降 | 检查素材创意、位置变化、用户疲劳度，建议AB测试 |
| CTR | 上升 | 沉淀有效素材策略，评估可复用性 |
| CVR | 下降 | 排查落地页体验、业务流程卡点、人群偏移 |
| CVR | 上升 | 分析转化提升原因，评估可规模化性 |

## 注意事项

- 总变化量接近0（|ΔConversion| < 1）时脚本提示"波动极小，无需归因"
- 连环替代法固定使用「曝光→CTR→CVR」替代顺序
- 数据缺失值会被自动跳过
- 报告模板参见 [report-template.md](report-template.md)
