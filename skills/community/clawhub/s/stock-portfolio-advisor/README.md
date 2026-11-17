# stock-portfolio-advisor · 自选持仓投资价值评分与配置顾问

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.4.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-77%20passed-brightgreen.svg)](#测试)
[![Deps](https://img.shields.io/badge/dependencies-stdlib%20only-orange.svg)](#安装)

> 分析 A 股自选与持仓，**按行业路由**计算价值评分与**独立的**交易环境分，输出基本面情景估值、数据缺口、受风险政策约束的配置参考，并生成可离线打开的 HTML 报告。
>
> A WorkBuddy Skill. 所有分数由脚本**确定性计算**，禁止模型心算。

**English TL;DR** — Deterministic, rule-based scoring for A-share watchlists and holdings: sector-routed value score + separate trading-environment score, scenario-based fundamental valuation, explicit data-gap reporting, constrained allocation reference, offline HTML report. Pure Python stdlib, 77 unit tests. Not investment advice.

---

## 为什么又做了一个

v1 的问题在于把"交易热度"混进了"价值判断"——资金、技术、新闻的噪音会盖过基本面信号。
v2 做的一件核心事：**把价值分和交易环境分彻底拆开**，各自独立打分、独立展示，不再合成一个"总分"糊弄过去。

| | v1 | v2.4.0 |
|---|---|---|
| 评分 | 六维合成一个总分 | **价值分（Q/G/V，按行业路由）+ 独立的交易环境分（F/T/N）** |
| 估值 | 目标价三法取中位数 | 分行业主模型 + bear/base/bull 三情景公允价值 |
| 缺失数据 | 中性兜底 | **先补数据 → 能派生就派生 → 最后才兜底**；有效覆盖率 <70% 该维度直接为 `null`，资料不足输出 NR |
| 结构性缺失 | 计 0 分 | **第三方来源缺失的前瞻/行业项按总体期望分插补**（`IMPUTE` 白名单） |
| 观测项缺失 | 计 0 分 | **按中性默认分 60 兜底**（`MISSING_FILL='neutral'`），仍留在分母，不会把少量可得数据放大成高分 |
| 大盘温度 | 4 项全齐才出分 | **拿到 ≥3 项即出分，按可用项权重归一**，缺一两项不再让温度变"数据不足" |
| 配置 | 固定约束 | 单票 ≤15% / 行业 ≤30% / 产业链分组 ≤30% / 现金 ≥ max(5%, 现金需求) |
| 可追溯性 | 无 | 每只股票每项指标带 `weights_version`，结果带 `model_version` |

---

## 四条设计原则

1. **不许心算** —— 分数与估值由 `scripts/score_engine.py` 调用 `scripts/value_model.py` 计算，禁止模型凭感觉估分或直接填目标价绕过公式。
2. **不许编造** —— 取不到的数据标缺失，**绝不编造**。缺失项按固定优先级处置：**先尽力补数据 → 能派生就派生 → 结构性缺失按期望分插补 → 观测项缺失按中性默认分 60 兜底**；兜底/插补**都不抬高覆盖率**，所以不会把"少量可得数据"放大成高分，也过不了 NR 门槛。
3. **硬风险不被缺失掩盖** —— 已知 ST / 退市 / 立案 → 强制评级 D、仓位上限 0；资料不足 → NR（暂不评级），总分 `null`。
4. **不承诺收益** —— v2 阈值尚未完成历史收益校准，README 与报告都写明这一点。

---

## 安装

```bash
git clone https://github.com/<你的用户名>/stock-portfolio-advisor.git
cd stock-portfolio-advisor
```

**零依赖**：只用 Python 标准库，Python 3.13+ 直接跑，不需要 `pip install` 任何东西。

作为 WorkBuddy 技能使用时，把整个目录放到 `~/.workbuddy/skills/` 下即可。

---

## 快速开始

仓库自带**合成数据示例**（不联网、不用真实行情），可以直接跑通整条链路：

```bash
# 1) 评分：metrics.json -> result.json
python scripts/score_engine.py \
  --input  examples/metrics.example.json \
  --output examples/result.example.json

# 2) 出报告：result.json -> HTML
python scripts/build_report.py \
  --result examples/result.example.json \
  --output examples/report.example.html

# 3) 查看输入字段模板
python scripts/score_engine.py --template
```

打开 `examples/report.example.html` 即可看到完整报告（内联 SVG，断网可看）。

---

## 使用示例

以下是**仓库示例真实跑出的结果**，不是示意：

### 输入

`examples/metrics.example.json` 是 6 只标的的指标输入：1 只带股息数据的红利样本、1 只数据齐全、1 只无机构覆盖（`forecast` / `industry_boom` 结构性缺失）、1 只缺个别观测项、1 只银行、1 只故意留空的 `missing`。大盘用的是**原始时间序列**（沪深300 收盘、全市场成交额、涨家占比）外加一个标量，**故意只给 3/4 项**，用来演示 v2.4.0 的"≥3 项即可出分、按权重归一"。

### 输出 · 个股

| code | 价值分 | 交易环境分 | 评级 | 动作 | 上行空间 | 仓位上限 | 参考目标权重 |
|---|---|---|---|---|---|---|---|
| `dividend` | 88.3 | 80.1 | A+ | 价值评分很高 | +33.3% | 15% | —（未持仓） |
| `ordinary` | 87.0 | 80.1 | A+ | 价值评分很高 | +33.3% | 15% | 11.39% |
| `no_coverage` | 86.0 | 80.1 | A+ | 价值评分很高 | +33.3% | 15% | 11.12% |
| `partial_data` | 85.2 | 80.1 | A+ | 价值评分很高 | +33.3% | 15% | —（未持仓） |
| `bank` | 72.6 | 80.1 | A | 价值评分较高 | −16.7% | 12% | 7.48% |
| `missing` | `null` | `null` | **NR** | 暂不评级 | — | — | — |

- `missing` 就是"数据不足不硬凑"的演示：**不给分、不定级、不给仓位上限**。
- `dividend` 演示 v2.3.0 的股息子项：股息率 3.83%、对无风险利率利差 +2.03 个百分点（利差分 93.7），分红覆盖净利 1.89 倍（覆盖分 80.9）→ V = 84.3，比同参数的 `ordinary`（V = 82.0）高。**这是"持有理由"第一次被引擎量化**。
- `ordinary` 的行业景气度改由申万行业财报派生（净利同比 12.0%、营收同比 8.0%）→ G = 80.3，**不再是所有标的等额 50**；`np_yoy` 也由净利润 TTM 与去年同期利润自算。
- `no_coverage` 演示 v2.3.0 的插补与"派生优先"：既无机构覆盖、也无行业财报 → `forecast` 按期望分 60、`industry_boom` 按 50 计价，G = 76.9（旧口径直接计 0 时只有 59.9），覆盖率仍为 70%，**插补不抬高覆盖率**。
- `partial_data` 演示 **v2.4.0 的中性兜底**：它是 `ordinary` 去掉 `qoq_trend`（G 权重 15、原分 100）后的副本，G 覆盖率跌到 85%、缺项按**中性 60** 计价 → G = 74.3（不再是旧口径的 65.3），价值分 85.2。**兜底值取中位，既不给缺失加分，也不把缺失当"差"来重罚**；覆盖率 85% 仍高于 70% 门槛，所以照常出评级。

### 输出 · 六维与数据质量

```json
// ordinary —— 数据齐全，行业景气度由申万财报派生
"dims": {"Q": 96.4, "G": 80.3, "V": 82.0, "F": 79.2, "T": 87.4, "N": 74.0},
// no_coverage —— 结构性缺失走 IMPUTE 白名单插补
"G": {"score": 76.9, "coverage": 70.0, "imputed_weight": 30, "neutral_weight": 0,
      "missing": [], "imputed": ["forecast", "industry_boom"], "neutral": []}
// partial_data —— 观测项缺失按中性 60 兜底
"G": {"score": 74.3, "coverage": 85.0, "imputed_weight": 0, "neutral_weight": 15,
      "missing": [], "imputed": [], "neutral": ["qoq_trend"]}
```

每个维度都带 `coverage`（有效覆盖率）、`imputed`（按期望分插补的项）和 `neutral`（按中性 60 兜底的项）——**分数、它的可信度、以及哪些分是插补/兜底来的，一起给**。`missing` 只在显式切换到 `renorm` 策略时才会非空（默认 `neutral` 下缺项进 `neutral` 而非 `missing`）。

### 输出 · 大盘与配置

```json
"market":     {"temperature": 70.0, "state": "偏热", "coverage": 82.4, "min_items": 3,
               "used": ["hs300_ma250_dev", "volume_ratio_5_250", "up_ratio_20d"],
               "missing": ["broken_net_ratio"],
               "derived": {"volume_ratio_5_250": "turnover_series", "up_ratio_20d": "advance_ratio_series"}}
"allocation": {"equity_pct": 29.99, "cash_pct": 55.01, "status": "reference"}
```

温度分不再是"4 项全齐才敢给"：本示例只提供了 3 项（`broken_net_ratio` 缺），引擎按**可用项权重占比 82.4% 归一**照常给出 70.0 分，`notes` 写明"温度分由 3/4 项按权重归一得出"。同时 `turnover_series`（量能比 5/250）与 `advance_ratio_series`（20 日上涨占比）是引擎**自算**的，`derived` 会点名；若外部直接给了标量值，则以外部值为准。

配置的 `status` 是 `reference`（参考），不是指令。配套 warning 会明说：

> 仅为约束预算参考，未生成买卖订单；交易费用、最小交易单位、实际可成交性需另行核实。

---

## 评分模型

**价值分** = `(Q×wQ + G×wG + V×wV) / (wQ+wG+wV)`，权重按标的画像路由：

| profile | Q : G : V | 适用 |
|---|---|---|
| `default` | 25 : 20 : 20 | 通用盈利企业 |
| `growth` | 20 : 30 : 15 | 成长 |
| `value` | 30 : 10 : 30 | 成熟红利 |
| `cyclical` | 25 : 15 : 25 | 周期资源 |
| `bank` / `broker` / `insurance` | 30 : 10 : 25 | 分别适配（银行看不良率与资本缓冲，券商看风险覆盖率，保险看偿付能力） |

**交易环境分** = `(15F + 10T + 10N) / 35` —— 与价值分**并列展示，不混入**。

**缺失值按固定优先级处置**：① **先补数据**（按取数手册把字段取回来）→ ② **能派生就派生**（`ocf_to_np` / `np_yoy` / 股息子项 / 行业景气度 / 温度自算）→ ③ **结构性缺失**（`forecast` 无机构覆盖、`industry_boom` 无行业数据）按**总体期望分**插补（`IMPUTE` 白名单）→ ④ **观测项缺失**（ROE、负债率、资金流、波动率…）按**中性默认分 60** 兜底（`MISSING_FILL='neutral'`），仍留在分母里。三者都不抬高 `coverage`，所以不会把少量可得数据放大成高分，也过不了 NR 门槛；哪些分是插补/兜底来的，`data_quality.*.imputed` 与 `data_quality.*.neutral` 会点名。

**发布门槛**：Q/G/V 均有分 + 关键财务齐全 + 有效现价 + 完整情景估值 + 风险已核查，才发布总分与评级。

**大盘温度**：均线 / 成交额 / 涨跌广度 / 破净比例 4 项，权重 30:20:20:15；**拿到 ≥3 项即出分，按可用项权重归一**（不足 3 项才"数据不足"），缺一两项不再让温度消失。

完整口径见 [`references/scoring-model.md`](references/scoring-model.md) 与 [`references/indicator-mapping.md`](references/indicator-mapping.md)。

---

## 估值与配置

- 每次选**一种**适用的行业主模型，输出 bear / base / bull 三套公允价值。行业不适配、输入不完整、情景顺序错误 → **不出公允价值，不做技术位兜底**。
- 配置硬约束：单票 ≤15%、单一行业 ≤30%、产业链分组 ≤30%、现金 ≥ max(5%, 现金需求)。
- 目标权重按 merit（总分−45）比例填充：**同一轮内同步提交增量**，分组额度不足时先按 merit 比例压缩该组额度、再套用单票上限，因此结果不依赖股票代码顺序。
- 结果带 `model_version` 与每只股票的 `weights_version`，跨版本/跨 profile 的快照**不直接计算分差**。

---

## 回测与校准

`scripts/backtest.py` 是一个日频、只做多、次日开盘成交的模拟器，含现金分红、拆股、成本与停牌不可成交处理。

```bash
python scripts/make_demo_data.py --folder workspace/demo --years 12 --count 12   # 合成数据
python scripts/backtest.py --dataset workspace/demo --output bt.json \
  --start 2015-01-01 --end 2024-12-31
```

⚠️ **必须说清楚**：仓库里的 77 个单元测试验证的是**公式正确性、缺失值处理、行业路由、风险判定、仓位约束与报告兼容性**，**不是历史收益回测**。
v2 的阈值**尚未完成历史收益校准**，因此本项目不宣称"更赚钱"，也不承诺目标价会兑现。

---

## 测试

```bash
cd scripts
python test_value_model.py   # 54 tests
python test_backtest.py      # 23 tests
```

共 **77 个测试全部通过**，无需联网、无需真实数据。

---

## 项目结构

```
.
├── SKILL.md                          # 技能元数据与完整工作流
├── scripts/
│   ├── score_engine.py               # 评分 CLI 入口
│   ├── value_model.py                # 估值与评分核心（确定性计算）
│   ├── build_report.py               # HTML 报告渲染（内联 SVG）
│   ├── portfolio_ledger.py           # 持仓台账与快照
│   ├── backtest.py                   # 日频回测模拟器
│   ├── build_backtest_dataset.py     # 回测数据集构建
│   ├── calibrate_weights.py          # 权重校准
│   ├── weight_registry.py            # 权重注册表（版本化）
│   ├── run_calibration.py            # 校准一键执行
│   ├── make_demo_data.py             # 合成示例数据生成
│   ├── package_skill.py              # 打包
│   └── test_*.py                     # 单元测试（77 个）
├── references/
│   ├── scoring-model.md              # 评分结构、行业路由、门槛、约束
│   ├── indicator-mapping.md          # v2 输入字段、单位、来源日期、估值公式
│   ├── data-playbook.md              # 取数命令与降级路径
│   ├── backtesting.md                # 回测数据格式与启用门槛
│   └── valuation-review-2026-09-05.md# v1 问题留档
├── config/                           # 权重、校准、回测策略配置
├── assets/                           # 报告样式与图标
└── examples/                         # 可跑通的输入 / 输出 / 报告示例
```

---

## 数据源

主通道为腾讯自选股（`westock-mcp` 连接器 + `westockdata` CLI）。连接器未连接时有降级路径，但**禁止编造自选或持仓数据**。

针对 A 股。港股 / 美股可记录清单，但**不套用** A 股行业阈值、币种与配置规则。
K 线为收盘级别，非盘中实时。

---

## 能力边界

**不做**：盘中实时盯盘 · 个股深度尽调 · 自动下单（仅模拟盘且须人工确认价格与数量）。

---

## 免责声明

本项目输出的是**评分、条件估值与配置参考**，**不构成投资建议**，不含任何收益承诺，不保证目标价兑现或回撤上限。
v2 阈值尚未完成历史收益校准。市场有风险，投资决策及其后果由使用者自行承担。

---

## License

[MIT](LICENSE)
