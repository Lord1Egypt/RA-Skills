---
name: stock-factor
description: >
  股票因子（Stock Factor）技能 —— 当前已收录 **1101 个因子（18 个因子族）**，为 AI 提供一套已收集、已转写、可由 QuantAll（全A解析）直接运行的
  A 股因子清单（含 IC / IR / time_potential 等评估指标）。既可直接读取因子清单（scripts/output/*.xlsx），
  也可通过 run_task_file 执行 scripts/task/*.json 用 QuantAll 实时重算/更新因子参数。
  已汇总 Qlib Alpha158、Qlib Alpha360、国泰君安 GTJA Alpha191、WorldQuant Alpha101（已全量转写），
  并补充 stock_daily（量价/估值/市值/换手等）、stock_report（财务质量/成长/偿债）两类基础因子，
  以及 TA-Lib 技术指标 + 常用指标（KDJ/BIAS）共 84 个。
  内置 gen_report.py 报告生成器：一键汇总全部因子族的 IC/IR 统计并生成可视化 HTML 报告。
  触发：用户提到"股票因子""因子清单""因子库""因子分析""IC分析""Alpha158/360/191/101""选股因子"
  "更新因子""跑因子""因子报告"等量化关键词时。
  不主动在普通股市聊天中触发，仅在用户有明确因子研究/选股需求时使用。
  本技能依赖 QuantAll（全A解析）MCP 计算引擎，使用前需先安装并启动它。
agent_created: true
license: MIT
version: 1.3.0
---

# 股票因子（Stock Factor）技能

---

## 1. 这是什么 / 技能定位

> **📊 当前已收录因子：共 1101 个（18 个因子族）** —— 已入库 `task/` **1087 个（16 族，可直接 QuantAll 运行）**；参考区 **14 个（2 族：会计质量 4 + Beneish 10，因本地 DB 数据缺口 / 信号弱留参考区未入库）**。

本技能为 AI 提供一份**已收集、已转写、可直接在 QuantAll（全A解析）引擎上运行**的 A 股因子清单。

- **因子指标**：每个因子都带 IC、IR、time_potential、top10%_IC、top10%_IR、top10%_time_potential、bottom10%_IC、bottom10%_IR、bottom10%_time_potential。
  - `time_potential = daily_IC.MA5.STD / daily_IC.STD`（近期 IC 波动相对长期 IC 波动的比值，衡量因子信号的时效性/稳定性）。
- **因子代码**：已制作成 QuantAll 可直接执行的 JSON 文件（`scripts/task/*.json`），后续可用 QuantAll 实时更新因子参数。
- **因子来源**：主要来自网络收集汇总，由 AI 辅助完成转写。目前已汇总 `Qlib_Alpha158`、`Qlib_Alpha360`、`GTJA_Alpha191`、`Alpha101`，并持续扩充。

> ⚠️ **指标口径注意**：top10% / bottom10% 的判别，是把因子值按 0~1 排序后取 `<0.1` 或 `>0.9` 的极端档位。
> **某些因子头尾数据可能大量重复**（如常数因子、或大量股票同一数值），导致排序后极端档位不存在合适样本，
> 此时其 top10%_IC / bottom10%_IC 会缺失（NaN）。这是数据特性，不是代码错误。

**本技能与上下游技能的关系**：

| 技能 | 定位 | 关系 |
|------|------|------|
| `quantall-mcp` | QuantAll 计算引擎：安装、配置、工具总览（**含数据库建库与更新**） | **上游依赖**：本技能所有计算都跑在它上面；数据准备也由它 / `update-stock-mcp` 负责 |
| `update-stock-mcp` | A 股 DuckDB 数据库管理：建库、全量/增量更新行情与财报、查询 | **上游依赖（数据）**：本技能所需的底层数据由它准备 |
| `stock-factor`（本技能） | 因子清单的收集、转写、提供、更新 | **下游应用** |

> **定位边界**：本技能当前是**因子清单（字典 + 初筛）**，提供"有哪些因子、各自怎么算、初步 IC/IR 表现"。**尚未做精选有效因子、因子去冗余、因子合成与策略挖掘**——这些后续可由 AI 基于 `output/*.xlsx` 继续深入（见 §4.3 边界说明）。如果想做因子精选，不妨参考factor-prune技能。

---

## 2. 技能已内置的因子清单（收集成果）

| 因子家族 | 因子数 | 转写状态 | 清单(xlsx) | 代码(task json) | 参考源 |
|----------|--------|----------|------------|------------------|--------|
| Qlib Alpha158 | 158 | ✅ 已转写+已跑 | `facotr-Qlib_alpha158.xlsx` | `facotr-Qlib_alpha158.json` | `Alpha158_因子参考.md` |
| Qlib Alpha360 | 360 | ✅ 已转写+已跑 | `facotr-Qlib_alpha360.xlsx` | `factor-Qlib-Alpha360.json` | `Alpha360_因子参考.md` |
| 国泰君安 GTJA Alpha191 | 191 | ✅ 已转写+已跑(全 191 验证) | `factor-GTJA_Alpha191.xlsx` | `GTJA_Alpha191.json` | `国泰君安Alpha191.txt` / `GTJA_Alpha191-30.txt` |
| WorldQuant Alpha101 | 101 | ✅ **已全量转写 101/101**（`scripts/task/factor-Alpha101.json`，含 `scale`/`indneutralize`/`Ts_ArgMax` 等全部算子） | `factor-Alpha101.xlsx`（待跑） | `factor-Alpha101.json` | `Alpha101.txt` |
| stock_daily 基础因子 | 12 | ✅ 已转写+已跑 | `factor-stock_daily.xlsx` | `factor-stock_daily.json` | （估值/市值/换手/量比等） |
| stock_report 财务因子 | 多 | ✅ 已转写+已跑 | `factor-stock_report.xlsx` | `factor-stock_report.json` | `db_translate.json` 字段 |
| TA-Lib 技术指标 + 常用指标(KDJ/BIAS) | 84 | ✅ 已转写+真实引擎验证(0 异常)；v1.2.0 已优化命名 | `factor-Indicators.xlsx` | `task/factor-TA_Indicators.json` | `TA-Lib指标参考.md` / `TA_Indicators_跳过汇总.txt` |
| Barra CNE5 风格因子 | 10 | ✅ 已转写+已跑(0 异常) | `factor-BarraCNE5.xlsx` | `task/factor-BarraCNE5.json` | 华安/中银证券《CNE5 十大风格因子》研报（MSCI Barra CNE5 风险模型） |
| Piotroski F-Score | 10 | ✅ 已转写+已跑(0 异常) | `factor-Piotroski.xlsx` | `task/factor-Piotroski.json` | Piotroski(2000) 9 条二元会计标准（质量改善选股） |
| Altman Z-Score | 6 | ✅ 已转写+已跑(0 异常)，**已入库** `task/` | `factor-AltmanZ.xlsx` | `task/factor-AltmanZ.json` | Altman(1968) 5 变量破产预警（困境质量因子） |
| Beneish M-Score | 10 | 🟡 已转写+已跑，**6 可行子项+6变量近似版通过；DSRI/DEPI/完整MScore 因缺数据报错** — 留 `因子初始参考文件/`（**数据缺口不补**：本地DB创建/下载麻烦，且近似版信号弱，不入库） | `factor-BeneishM.xlsx` | `因子初始参考文件/factor-BeneishM.json` | Beneish(1999) 8 变量盈余操纵检测 |
| 经典学术异象 | 9 | ✅ 已转写+已跑(9/9 通过)，**已入库** `task/`；含 4 个强有效反转/波动因子（INTRADAY/MAX20/REVERSAL_M1/IDIOVOL |IR|>0.3） | `factor-ClassicAnomalies.xlsx` | `task/factor-ClassicAnomalies.json` | Sloan 应计 / Bali 彩票偏好 / Ang 特质波动 / Amihud 非流动性 / Jegadeesh 反转 / HXZ 资产增长代理 |
| Fama-French / HXZ 风格 | 7 | ✅ 手写转写+已跑(7/7 通过，0 异常)，**已入库** `task/` | `factor-FF_HXZ.xlsx` | `task/factor-FF_HXZ.json` | FF3/FF5(1993/2015)+HXZ q-factor(2015)：Size/Value(BM,EP)/Profitability/Investment/Momentum/ROE |
| 中信/申万 风格因子 | 12 | ✅ 手写转写+已跑(12/12 通过，0 异常)，**已入库** `task/` | `factor-CITIC_Shenwan.xlsx` | `task/factor-CITIC_Shenwan.json` | 中信 7 大类 + 申万 10 大类（规模/估值/成长/动量/反转/波动/流动性/杠杆/盈利/非线性规模） |
| WorldQuant 公式化 alpha 扩展批 | 10 | ✅ 手写转写+已跑(10/10 通过，0 异常)，**已入库** `task/`（基础 101 已入 `task/`，本批为扩展样本，非官方 201/212） | `factor-WorldQuant_formulaic.xlsx` | `task/factor-WorldQuant_formulaic.json` | WorldQuant《101 Formulaic Alphas》扩展族（算子 rank/ts_rank/correlation/decay 等） |
| 收益高阶矩 / 52 周高异象 | 7 | ✅ 手写转写+已跑(7/7 通过，0 异常)，**已入库** `task/` | `factor-ReturnMoment.xlsx` | `task/factor-ReturnMoment.json` | 52周高价距离/β/β²/下行半离差/收益偏度/峰度/特质偏度（ANOM_SKEW IR −0.55、ANOM_DOWNSIDE_VOL −0.26、ANOM_52WK top10% −0.47 强有效） |
| 违约距离 / 现金流收益率 | 5 | ✅ 手写转写+已跑(5/5 通过，0 异常)，**已入库** `task/` | `factor-Merton_CashFlow.xlsx` | `task/factor-Merton_CashFlow.json` | Merton(1974) 违约距离/经营现金流收益率/企业自由现金流收益率/EBITDA收益率/股息率（MERTON_DD IR −0.25、CF_DIV_YIELD +0.12） |
| 会计质量 / 困境预警 | 4 | 🟡 手写转写+已跑(4/4 通过，0 异常)，留 `因子初始参考文件/`（**不补折旧**：本地DB创建/下载麻烦，且 4 因子 |IR|≈0.02~0.07 均无效，不入库）— Mohanram G-Score 现 6/7 变量近似 | `factor-AccountingQuality.xlsx` | `因子初始参考文件/factor-AccountingQuality.json` | Ohlson O-Score / Mohanram G-Score / Novy-Marx 毛利率质量 / Sloan 应计 |

> **说明**：Alpha101 是 WorldQuant 发布的 101 个高难度量价因子（含 `SignedPower`、`IndNeutralize`、`scale`、`Ts_ArgMax` 等算子）。
> 公式见 `Alpha101.txt`，**全量转写已落地于 `scripts/task/factor-Alpha101.json`**（2026-08-08 由用户手写逐个完成，已做复权、直接调用内置 `row_scale`/`row_indneutralize`）。
> 旧文件 `因子初始参考文件/Alpha101_QuantAll.json`（仅 78 个、未复权、脚本生成可读性差）与 `Alpha101_跳过汇总.txt` 已**被本版取代**，可删除。

> **关于 "WorldQuant 201 / 212"**：经核查，WorldQuant 官方**没有**独立的 "Alpha 201 / 212" 论文或公式集。其经典公开出处是《101 Formulaic Alphas》(Tulchinsky et al., 2015)，**全集已转写收录于 `task/factor-Alpha101.json`（#1–#101）**。社区所谓的 "201/212" 是对「公式化 alpha 扩展家族（量价算子型，200+ 个）」的统称。本技能已交付：① 算子语义映射表（见 `因子收集_WorldQuant公式化alpha.md`）；② 手写一批代表性扩展样本 `因子初始参考文件/factor-WorldQuant_formulaic.json`（与已有 101 互补、不重复）。如需真正 200+ 全集，需另行获取社区扩展公式源。

> **TA-Lib 技术指标说明**：共 84 个因子，覆盖 Overlap Studies（均线类）、Momentum（动量）、Volume（成交量）、Volatility（波动率）、Price Transform（价格变换）、Statistic Functions（统计）、Directional Movement（ADX 族）、K 线形态（3 个代表）以及常用指标 KDJ（K/D/J）和 BIAS（6/12/24）。
> **命名规则**（v1.2.0 优化）：采用业界通用标准名，无 `TA_` 前缀——均线类 `SMA5/EMA12/WMA20/DEMA20/TEMA20/HMA20/VWMA20/TRIMA20`；布林带 `BOLL_MID20/BOLL_UP20/BOLL_LOW20/BOLL_WID20/BOLL_PCTB20`；MACD 用中文通用的 `MACD_DIF/MACD_DEA/MACD_HIST`；加速带 `ACCBANDS_MID20/UP/LOW`；形态 `CDL_ENGULFING/CDL_HAMMER/CDL_DOJI`；线性回归 `LINEARREG20/LINEARREG_SLOPE20/LINEARREG_INTERCEPT20/TSF20`。
> 跳过项详见 `scripts/因子初始参考文件/TA_Indicators_跳过汇总.txt`（SAR/KAMA/NVI/PVI/MAVP 等需状态迭代或 Hilbert 变换的指标）。

---

## 3. 依赖：QuantAll（全A解析）的安装与使用

本技能所有因子计算都依赖 QuantAll 引擎（本地 HTTP 服务 `localhost:8686`）。下面是给 AI 和用户速查的最小化安装/使用要点；完整细节见 `quantall-mcp` 技能的 `SKILL.md`。

> ### ⭐ 优先推荐：直接安装 `quantall`（全A解析）技能
> **数据库怎么建、怎么更新，已经在 `quantall` 技能（及其配套的 `update-stock-mcp` 技能）里讲全了**——包括用 tushare/baostock 拉行情、指数、分红、业绩预告、财报，以及 DuckDB 建库与增量更新。
> 👉 **强烈建议先安装并阅读 `quantall` 技能的 SKILL.md**，按其指引完成「引擎安装 → 建库 → 数据更新」三步，再回来用本技能的因子清单。
> 本技能只负责"因子清单 + 转写方法论"，**底层数据准备请交给 `quantall` / `update-stock-mcp`，不要在本技能里重复维护建库/更新脚本**（本技能原内置的 `Create_DuckDB.py`、`UpdateStock_script.py` 已移除，统一由上述技能接管）。

### 3.1 安装

```
□ 1. 创建 venv（约 300MB+，依赖 PySide6/pandas 等大包）：
   <Python路径> -m venv <skill-dir>/scripts/.venv

□ 2. pip 安装（务必用清华源，否则超时）：
   <skill-dir>/scripts/.venv/Scripts/python.exe -m pip install quantall -i https://pypi.tuna.tsinghua.edu.cn/simple

□ 3. 在 scripts 目录下编写启动文件 Start_QuantAll.py：
   import os
   from QuantAll import Start_main
   Start_main(os.path.dirname(__file__))

□ 4. 建议用户制作 bat 启动脚本并发送桌面快捷方式：
   @echo off
   cd /d "%~dp0"
   start "" .venv\Scripts\pythonw.exe Start_QuantAll.py %*
   （注意：不要在桌面直接放 .bat，Windows cmd 以 GBK 读 .bat 会乱码；应放 scripts/ 下再建 .lnk）

□ 5. 首次启动会自动创建 DB_setting.json（默认用测试库，仅沪深300近两年基础行情）。
□ 6. 配置数据库：修改 DB_setting.json 的 db_path 指向本地完整 DuckDB（正式分析必需）。
□ 7. **本地无数据库或需更新数据时，请用 `quantall` / `update-stock-mcp` 技能**（不要再在本技能里找建库/更新脚本）：
   - 建库、增量/全量更新行情与财报、字段翻译等，完整步骤见 `quantall` 技能的 SKILL.md。
   - 简言之：tushare 免费渠道约 120 积分可更新基础行情；财报等深度数据需 ≥2000 积分。
□ 8. 数据库字段名难懂时，用 data/db_translate.json 翻译成中文名（如 'symbol'→'股票代码'），
	常用的'close','open','high','low','vol','amount'不受翻译文件影响。
   供 AI 用 available_data 查询时看到的是易懂中文。注意翻译名不要重复映射。
```

### 3.2 使用（启动、连接、协议、ping）

1. 启动 QuantAll（bat 或 `python Start_QuantAll.py`）。
2. **首次弹用户协议窗口，需用户确认**；确认后即永久激活，后续不再弹窗。
3. AI 通过 MCP 连接 `http://127.0.0.1:8686/mcp`（`~/.workbuddy/mcp.json` 中 `"全A解析": {"url": "http://127.0.0.1:8686/mcp", "disabled": false}`）。
4. 部分智能体首次需用户在「连接器-自定义连接器」确认许可；且**建议先启动 QuantAll 再启动智能体**，否则需在智能体内「重新连接」。
5. 用 `ping` 工具测试连接是否成功（注意：`ping` 通 ≠ 分析工具可用，必须确认协议窗口已确认）。

### 3.3 本技能用到的关键内置工具

| 工具 | 用途 |
|------|------|
| `ping` | 健康检查 |
| `available_data` | 查看当前可用数据字段（受本地库 + db_translate.json 影响） |
| `how_code` | 查看代码执行环境说明（内置变量/函数/禁写规则） |
| `factor_analysis` | 单因子 IC 分析（测试单个因子能否跑通、深入分析） |
| `batch_factor_analysis` | 批量因子 IC 分析（效率与流程稳定性优先） |
| `run_task_file` | **读取本地 JSON 任务文件并执行**（本技能把收集的因子汇总成 `scripts/task/*.json`，用它来跑 `batch_factor_analysis`，简化任务流程、确保稳定性） |

> 所有 QuantAll 工具调用**必须串行**（一个返回后再发下一个），不支持并行。

---

## 4. 技能使用流程

### 4.1 AI 读取因子清单（了解已有因子）

直接用 `Read` / 表格读取 `scripts/output/*.xlsx`，即可了解各因子的 IC / IR / time_potential 等指标，无需启动引擎。

- `scripts/output/facotr-Qlib_alpha158.xlsx`（158 维技术面）
- `scripts/output/facotr-Qlib_alpha360.xlsx`（360 维原始价量）
- `scripts/output/factor-GTJA_Alpha191.xlsx`（191 维国泰君安）
- `scripts/output/factor-Alpha101.xlsx`（101 维 WorldQuant）
- `scripts/output/factor-Indicators.xlsx`（84 个技术指标）
- `scripts/output/factor-stock_daily.xlsx`（量价/估值/市值/换手等基础因子）
- `scripts/output/factor-stock_report.xlsx`（财务质量/成长/偿债因子）

### 4.2 因子数据更新（重算因子参数）

用 `Start_QuantAll.py` 启动引擎后，调用 `run_task_file` 执行 `scripts/task/*.json`：

- 每个 task JSON 结构：`{"tool_name": "batch_factor_analysis", "feature_days": 5, "factor_dict": {因子名: "out = 代码"}, "save_path": "output\\因子名.xlsx"}`
- **默认 `feature_days=5`**：用「5 日后收益」评估因子预测力。
- 结果**保存到启动脚本同目录的 `output/` 文件夹**（由 `save_path` 指定）。更新时注意 `save_path` 相对路径是否正确，避免覆盖或写错位置。

### 4.3 如何解读与使用输出结果（因子清单的用途）

每个 `output/*.xlsx` 是**逐因子 IC 分析**的结果表，一行一个因子。默认 `feature_days=5`（用未来 5 日收益评估预测力），样本区间约 2024-08 至 2026-07，股票池为全市场约 5588 只。列含义如下：

| 列 | 含义 |
|----|------|
| `name` | 因子名 |
| `code` | 该因子的 QuantAll 代码（可直接复制到 `run_task_file` / `factor_analysis` 复用） |
| `feature_days` | 评估所用的未来收益天数（默认 5） |
| `start_date` / `end_date` | 回测样本区间 |
| `universe` / `stock_count` | 股票池 / 样本内股票数（全市场约 5588） |
| `IC` | 因子值与未来收益的 Spearman 秩相关均值（绝对值越大预测力越强） |
| `IR` | IC 均值 / IC 标准差（信息比率；\|IR\|>0.3 通常视为有效） |
| `time_potential` | `daily_IC.MA5.STD / daily_IC.STD`（近期 IC 波动相对长期的比值，越接近 1 越稳定/时效一致） |
| `top10%_IC / _IR / _time_potential` | 因子值最高 10% 档位（排序 >0.9）内的 IC / IR / time_potential |
| `bottom10%_IC / _IR / _time_potential` | 因子值最低 10% 档位（排序 <0.1）内的对应指标 |

> 首列 `Unnamed: 0` 只是行索引，无业务含义，可忽略。

**怎么用这些结果**（本技能当前定位 = 因子清单 / 字典 + 初筛）：

1. **当因子字典查**：想知道"有哪些因子、各自怎么算"，直接看 `name` + `code` 两列。`code` 列就是可运行的 QuantAll 代码，可原样复制去跑单因子深入分析，或接入自己的研究 / 回测。
2. **快速初筛有效因子**：在 Excel 按 `IR` 降序排列，挑 `|IR| > 0.3` 的作为候选（如 GTJA_Alpha1 IR≈0.54、Alpha158 的 KLEN IR≈-0.43）。IC 的**正负号**代表因子方向（正 = 因子值越大未来收益越高，负则相反）。
3. **看多空区分度**：对比 `top10%_IR` 与 `bottom10%_IR`。若一头显著正、另一头显著负（如换手率 top10%_IR≈-1.19、bottom10%_IR≈0.10），说明因子在头/尾档位区分度强、选股信号更可靠；若两头都接近 0，可能只是中间段在起作用或信号弱。
4. **按家族横向比较**：同一套因子（如 GTJA 的 191 个、stock_report 的 105 个财务因子）放在一起看 IC/IR 分布，能快速判断"哪类因子在当前样本更管用"，为后续研究指方向。
5. **检查数据健康度**：`stock_count` 是否覆盖全市场、`time_potential` 是否异常（极端值可能意味着因子近期失效或样本有问题）。

> ⚠️ **头尾档位可能缺失**：部分因子值大量重复（常数因子或大量同值），排序后极端档位无合适样本，其 `top10%_*` / `bottom10%_*` 会为空（NaN），属数据特性非代码错误（见第 1 节口径说明）。

**⚠️ 本技能的边界（重要）**：当前产出是**因子清单 + 初筛指标**，本质是"因子字典 / 候选池"，**尚未做进一步精选、去冗余、因子合成与策略挖掘**。尚未覆盖：① 在 `|IR|>0.3` 基础上**精选有效因子**并给有效性评级；② 因子间**去冗余**（`batch_factor_corr`，|IC|>0.8 视为冗余）；③ 多因子**正交 / 合成**；④ 与**策略回测**衔接验证（`quantall-mcp` 的 `strategy_backtest`）；⑤ 随时间**更新 IC** 做版本管理。这些"精选与挖掘"步骤，AI 可在拿到 xlsx 后**继续深入**（例如按 IR 排序筛 Top 因子 → 用 `batch_factor_corr` 去冗余 → 把精选因子接入回测）。本技能先把"有哪些因子、各自表现如何"这层地基打牢。

### 4.4 因子分析报告生成（gen_report.py）

`scripts/gen_report.py` 是内置的**一键报告生成器**：自动读取 `scripts/output/*.xlsx` 全部因子族数据，统计分析并生成可视化 HTML 报告。

**使用方法**：
```bash
# 需安装 pandas / matplotlib / openpyxl
python scripts/gen_report.py
```

**输出**：`scripts/因子分析报告.html`（自包含 HTML，图表以 base64 内嵌，无需外部依赖）。

**报告内容**：
1. **分析总览**：KPI 卡片（因子总数、有效因子数、强有效因子数、平均 |IR|、平均 IC）+ 各因子族汇总表
2. **因子有效性分布**：IR 直方图、time_potential 分布图
3. **IC-IR 关系**：跨因子族散点图
4. **有效因子排行榜**：Top 30 by |IR|（含因子代码可展开查看）+ Top 20 横向条形图
5. **各因子族明细**：每族 Top 10 by |IR|
6. **数据健康度**：样本覆盖、口径说明、注意事项
7. **后续建议**：精选、去冗余、合成、回测的路径指引

> 报告中的图表使用 matplotlib 生成，需系统安装微软雅黑字体（`C:\Windows\Fonts\msyh.ttc`）。报告输出位置为 `scripts/` 目录（非 `scripts/output/`）。

---

## 5. ★ 经验一：如何收集因子

> 本技能因子信息主要从网络收集汇总、AI 辅助完成，下面是可复用的收集方法论。

> 📄 完整的「收集 + 转写」经验已单独立档：**`scripts/因子收集与转写经验.md`**（字段名坑、量纲/复权、指数基准、逐人手写约定、数据缺口处理、版本脉络等）。本节能直接套用的核心规则，深度细节见该文档。

### 5.1 收集来源（按"可直接计算性"分级）

| 来源 | 特点 | 收集难度 | 推荐做法 |
|------|------|----------|----------|
| **Qlib Alpha158** | 官方硬编码表达式（kbar/price/rolling 三类，158 维） | 低，可直接提取 | 从 Qlib 源码 `loader.py → Alpha158DL.get_feature_config()` 提取，无需运行 Qlib |
| **Qlib Alpha360** | 近 60 日 6 字段归一的原始特征（360 维） | 低 | 同上提取；注意它是"原始特征"非"构造因子"，转写后用来观察历史窗口含多少信号 |
| **GTJA 国泰君安 Alpha191** | 券商研报公开 191 个量价因子 | 中 | 收集原始公式文本（`国泰君安Alpha191.txt`），逐个转写为 QuantAll 代码 |
| **WorldQuant Alpha101** | WorldQuant 发布的 101 个"地狱难度"量价因子 | 高 | 收集公式（`Alpha101.txt`）；大量算子（`SignedPower`/`IndNeutralize`/`scale`/`Ts_ArgMax`）需自写 helper，转写成本高 |
| **技术指标 / 经典量价 / 基本面** | RSI/MACD/KDJ/BOLL/估值/成长/质量/规模 | 低 | 业界标准定义，整理为初始表达式（`因子表达式初始收集.md`） |
| **FamaFrench 五因子** | 市值/账面比/盈利/投资分组 | 中 | 组合层 + 单股票特征两层表达，A 股逐股计算用单股票特征做截面 rank |

### 5.2 收集与整理流程（推荐）

```
1. 选来源 → 2. 抓原始表达式（类 Qlib / WorldQuant 记号）→ 3. 整理成"初始收集"基线文档
   （统一记号：open/high/low/close/volume/vwap/ret/cap…，算子 MA/STD/REF/SUM/RANK…，防除零 +1e-12）
   → 4. 分类框架（技术面/估值/市值/动量/波动/财务/复合）→ 5. 转写为 QuantAll 代码（见第 6 节）
   → 6. 跑 batch_factor_analysis 验证 → 7. 落盘 xlsx / 汇总
```

- **初始收集文档**示例：`scripts/因子初始参考文件/因子表达式初始收集.md` —— 用**类 Qlib 算子记号**记录表达式（不是 QuantAll 代码），作为转写基线；覆盖 Alpha158 + 技术指标 + 经典量价/基本面 + FamaFrench。
- **记号约定**务必统一（见该文档第 0 节）：字段 `open/high/low/close/volume/vwap/ret/cap/float_cap/equity/ni/rev/ocf`；算子 `MA/EMA/WMA/STD/HHV/LLV/REF/SUM/ABS/RANK/PCTILE/LOG/COV/CORR`；防除零统一 `+1e-12`。

### 5.3 分类框架（供收集时归类）

| 大类 | 代表因子 | 数据来源 |
|------|----------|----------|
| 估值 | PE/PB/PS/股息率 | stock_factor |
| 市值 | 总市值/流通市值 | stock_factor |
| 换手/量价 | 换手率/量比/成交量均线比 | stock_factor |
| 动量 | N 日收益率 | close × adj_factor |
| 波动率 | N 日收益率 std | close × adj_factor |
| 技术指标 | RSI/KDJ/MACD/BOLL/ATR | OHLCV |
| 财务质量 | ROE/ROA/毛利率 | stock_report |
| 成长 | 净利同比/营收同比 | stock_report |
| 偿债 | 资产负债率/流动比率 | stock_report |
| 复合 | 低换手+小市值 | 多表组合（先 row_rank 再相加） |

---

## 6. ★ 经验二：如何转写因子代码（到 QuantAll）

> 核心：把"源表达式"（Qlib/WorldQuant/券商研报/自定义）翻译成 QuantAll 的 **Python exec 向量化代码片段**，
> 封装进 `scripts/task/*.json` 的 `factor_dict`，由 `batch_factor_analysis` 全市场运行。

### 6.1 转写目标格式（task JSON）

```json
{
  "tool_name": "batch_factor_analysis",
  "feature_days": 5,
  "factor_dict": {
    "因子名": "out = 代码片段",
    "GTJA_Alpha1": "out = -1*row_rank(d['vol']/d['vol'].shift(1)).rolling(6).corr(row_rank((d['close'] - d['open']) / d['open']))"
  },
  "save_path": "output\\因子名.xlsx"
}
```

- 每个 `factor_dict` 的值是**以 `out =` 结尾**的 Python exec 代码串。
- 单因子直接 `out = 原始值`，引擎内部自动截面排名，**不要手动 row_rank**；复合因子各子项先 `row_rank` 再组合。

### 6.2 QuantAll 代码铁律（必读，违反即报错）

1. **禁止**：`import` / `for`/`while` 循环 / `df.apply()` / `lambda` / 递归 / `axis=1` / `df.loc`/`df.iloc`。
2. 各股票停牌时间不对齐，**一律按列方向**（pandas 默认），禁止行方向计算。
3. **代码最后一行必须** `out = ...`。
4. **复权价格手动算**：`adj_close = d['close'] * d['adj_factor']`。
5. 条件分支优先用 pandas 向量化（如 `np.where`、`Series.where`、布尔索引），不要写 if/else 循环。
6. 所有 QuantAll 工具调用必须串行。

### 6.3 字段映射（源 → QuantAll）

| 源记号 | QuantAll 写法 | 备注 |
|--------|---------------|------|
| `close` | `d['close']` | **实际用复权价 `adj_cl = d['close']*d['adj_factor']`** |
| `open` | `d['open']` | 实际用 `adj_op` |
| `high` | `d['high']` | 实际用 `adj_hi` |
| `low` | `d['low']` | 实际用 `adj_lo` |
| `volume` | `d['vol']` | ⚠️ 字段名是 `vol` 不是 `volume` |
| `vwap` | `d['amount']/d['vol']` | 数据库无 vwap 字段，用 成交额/成交量 还原（分母 `.replace(0, np.nan)` 防零） |
| `cap` 总市值 | `d['总市值']` | 依 db_translate.json 中文名 |
| `adv{d}` 平均日成交额 | `d['amount'].rolling(d).mean()` | ⚠️ **是"成交额(amount)"不是"成交量(vol)"**；WorldQuant 定义 adv{d}=平均日*美元*成交量 = amount 滚动均值。极易误写成 `vol.rolling(d).mean()`（见 §6.8 坑 2） |
| `ret` 收益率 | `ac/ac.shift(1)-1`（ac=复权收盘） | 不要用未复权 close 直接算 |
| 指数收益(mkt) | `get_stock_index('000001','close', out_type='Series')` → 再 `.pct_change()` | 详见 §6.6；旧名 `get_index_matrix` 已改名，`out_type='Series'` 返回序列（Alpha30 用 `'serie'` 亦可）；基准常用 `'000001'`(上证综指) |

> 数据库字段名最终以 `db_translate.json` 翻译后的中文为准；写代码前用 `available_data` 确认，不要假设字段名。

### 6.4 复权价约定（重要）

价格类字段统一用复权价（原始价 × `adj_factor`），成交量/成交额/VWAP 不是价格类，不参与复权：

```python
ac = d['close'] * d['adj_factor']   # 复权收盘价
op = d['open']  * d['adj_factor']    # 复权开盘价
hi = d['high']  * d['adj_factor']    # 复权最高价
lo = d['low']   * d['adj_factor']    # 复权最低价
vwap = d['amount'] / d['vol'].replace(0, np.nan)   # VWAP，防零
```

### 6.5 算子映射表（源算子 → QuantAll / pandas）

| 源算子 | QuantAll / pandas 写法 |
|--------|------------------------|
| `REF(x, N)` / `DELAY(x, N)` | `x.shift(N)` |
| `MA(x, N)` / `Mean` | `x.rolling(N).mean()` |
| `STD(x, N)` | `x.rolling(N).std()` |
| `SUM(x, N)` | `x.rolling(N).sum()` |
| `MAX/MIN(x, N)` / `HHV/LLV` | `x.rolling(N).max()` / `.min()` |
| `Abs` | `abs(...)` 或 `np.abs` |
| `Log` | `np.log(...)` |
| `Greater/Less` | `np.maximum` / `np.minimum` |
| `Corr(x, y, N)` | `x.rolling(N).corr(y)` |
| `Cov(x, y, N)` | `x.rolling(N).cov(y)` |
| `Quantile(x, N, p)` | `x.rolling(N).quantile(p)` |
| `Rank(x)` 截面 | `row_rank(x)` → 0~1 百分位 |
| `Rank(x)` 时序 | `x.rolling(N).rank(pct=True, method='max')` |
| `IdxMax/IdxMin` | `x.rolling(N).apply(np.argmax/argmin, raw=True)`（窗口内 0 基位置；非 lambda，已验证可用） |
| `TS_ARGMAX/TS_ARGMIN(x,N)` | `rolling_imax(x,N)*N` / `rolling_imin(x,N)*N`（WorldQuant 语义="距今日天数"） |
| `PROD(x, N)` 时序乘积 | `x.rolling(N).apply(np.prod, raw=True)`（Alpha#29/#81 用到） |
| `Slope/Resi/Rsqr` | `rolling_slope(x,N)` / `rolling_resi(x,N)` / `rolling_rsquare(x,N)`。**⚠️ slope/resi 返回原始值（量纲=元/天、元），不含÷价格**；要无量纲须调用方 `/ac`（如 `rolling_slope(ac,n)/ac`、`rolling_resi(ac,n)/ac`）。rsquare 本身 0~1 无量纲 |
| `EMA/SMA(N)` | `ewm(alpha=2/(N+1), adjust=False)`（`SMA(N,m)` 用此近似） |
| `WMA/衰减线性` | `rolling_decay_linear(x, N)`（别名 `rolling_wma`） |
| `TSMAX/TSMIN` | `x.rolling(N).max()` / `.min()` |
| `TSRANK` | `x.rolling(N).rank(pct=True, method='max')` |
| `SignedPower(x, a)` | 实践用 `np.sign(x) * (np.abs(x) ** a)`（稳健，避免负底+非整数指数 `x**a` 出 NaN）；文档字面 `x**a`，取舍见 §6.8 坑 5 |
| `scale(x, a=1)` | `row_scale(x, a)`（**已内置**）：令每行 `|x|` 之和 = a（默认 1），即 `x.div(x.abs().sum(axis=1).replace(0,nan), axis=0)*a`。**注意：不是 z-score，旧文档写成 `(x-x.mean())/x.std()` 是错的** |
| `IndNeutralize(x, g)` | `row_indneutralize(x, g)`（**已内置**，g 为分组 Series 如 `col_attrs['所属行业']`）：截面行业中性化，每个元素减其所在组在该时间截面的均值。无需再注入 helper |
| `RegBeta/RegResi` | `rolling_regbeta(Y, X, n)`（单自变量 β）/ `rolling_regresi(df, [X1,X2,...], window)`（多自变量回归残差，如 3 因子 MKT+SMB+HML） |

### 6.6 内置函数速查（详见 `scripts/因子初始参考文件/how_code.txt`，以最新版为准）

> ✅ **环境已更新（重要）**：最新 `how_code.txt` 已把 `row_scale` / `row_indneutralize` / `get_stock_index` / `rolling_regresi` / `row_mean` 列入**内置函数**。**无需再自己注入 helper**——直接调用即可（旧文档"须前置注入"的说法已作废）。

- `d`：dict[str, DataFrame]，key=字段名（中文），value=面板（行=时间，列=股票）
- `col_attrs`：dict[str, Series]，股票属性（行业/市值/上市日期等）
- `np`, `pd`：已内置
- **截面函数**：`row_rank(df, split=[])`（截面排名→0~1 百分位，split 可按代码切分板块独立排名）、`row_top_n(df, n)` / `row_bottom_n(df, n)`（截面 Top/Bottom N）、`row_mean(df)`（按日期求均值→Series）、`row_scale(df, a=1)`（每行 |x| 之和缩放为 a）、`row_indneutralize(df, group_series)`（组内中性化，group_series 如 `col_attrs['所属行业']`）
- **时序回归/位置**：`rolling_slope/rsquare/resi/imax/imin/rank/decay_linear`（imax/imin 已含 /n 归一化）、`rolling_regbeta(Y, X, n)`（单自变量 β）、`rolling_regresi(df, factors_list, window)`（多自变量回归残差，factors_list 为 Series 列表，如 `[mkt, smb, hml]`）
- **指数**：`get_stock_index(index_code, field='close', out_type='DataFrame')`：获取指数数据并拷贝成与 `d['close']` 同结构的矩阵。基准常用 `'000001'`（上证综指）；指数 symbol 通常 6 位纯数字；`out_type='Series'` 返回 Series（旧名 `get_index_matrix` 已改名）。**指数是否有数据取决于本地库是否加载该指数**
- **回测**：`hold_until(buy, sell)` / `entry_check(...)`：持仓矩阵
- **时间函数**：`get_time()` / `get_time_id()` / `time_at()` / `time_between()` / `time_in()`


### 6.7 常见转写坑（血泪经验）

| 坑 | 原因 | 解决 |
|----|------|------|
| `df.loc/iloc` 或 `axis=1` 报错 | 停牌时间不对齐，行方向计算非法 | 全部改列方向向量化 |
| 因子 IC 偏弱/方向反 | 直接用 `d['close']` 未复权 | 先乘 `adj_factor` 得复权价 |
| `np.where` 导致运行失败 | 返回 numpy array，`out` 非 DataFrame | 用 `pd.DataFrame(...)` 包一层，或尽量用 `.where`/布尔索引 |
| `vwap` 算出来全 NaN | 数据库无 vwap 字段 / 除零 | 用 `d['amount']/d['vol'].replace(0, np.nan)` |
| 指数收益全 NaN | 该指数 symbol 未加载进本地库 | 用确定已入库的指数（如 `'000001'`），6 位纯数字 key |
| `rolling.apply` 疑似不支持 | 误以为需要 lambda | 用**命名辅助函数** `raw=True`（已验证可用） |
| 头尾档位指标缺失 | 因子值大量重复，排序后极端档位无样本 | 正常现象，非代码错（见第 1 节口径说明） |
| 单因子又手动 `row_rank` | `factor_analysis` 内部已自动排名 | 单因子直接 `out = d['字段']` |
| 字段名不存在 | 假设了字段名 | 先 `available_data` 确认（受 db_translate 影响） |
| `CLOSE0` 等常量因子 IC 异常 | `out = adj_cl/adj_cl` 恒等于 1 | 属正常，跳过即可 |

---

### 6.8 ★ Alpha101 全量对照经验（2026-08-08）

2026-08-08 用户手写逐个完成 Alpha101 全量 101 个因子（`scripts/task/factor-Alpha101.json`），
并对照源公式 `Alpha101.txt` 逐条复核。以下是从这次对照中新沉淀的经验，供后续转写其它家族（Alpha360 剩余、研报因子等）复用。

**A. 转写方式：手写逐个，不要脚本批量生成**
- Alpha101 这类「一次性、需逐个核对语义」的转写，**务必手写**，不要写脚本批量生成。
- 脚本生成的代码可读性差、易漏复权/adv 细节（早期 `Alpha101_QuantAll.json` 即因脚本生成、漏复权被弃用）。
- 跑测验证后再固化：用 QuantAll 实跑 `batch_factor_analysis` 确认无 `error_code`，比"看起来对"可靠。

**B. 复权是底线**
- 所有价格类字段（`close/open/high/low`）一律 `× adj_factor` 得复权价（`ac/ao/ah/al`），再参与运算；`returns` 用复权收盘算。
- 漏复权会导致因子值系统性偏移（前版教训）。

**C. `adv{d}` 必须用语义（最易系统性踩坑）**
- 定义：`adv{d} = average daily dollar volume` = 平均日**成交额** = `d['amount'].rolling(d).mean()`。
- **绝不能用 `vol.rolling(d).mean()`（那是平均成交量，量纲/数值都不同）**。本次对照发现 Alpha101 手写版里除 #71/#81 用了 `d['amount']` 外，其余 adv 仍误用了 `vol`，属需全局修正的系统性偏差（详见 §6.3 字段映射）。

**D. `scale` / `indneutralize` 现在已是内置函数，直接调用即可**
- 最新 `how_code.txt` 已内置 `row_scale(x, a=1)` 与 `row_indneutralize(x, group_series)`，无需再注入 helper（旧版"须前置注入"的写法已作废）。
- `row_scale(x, a=1)`：令每行 `|x|` 之和 = a（默认 1），即 `x.div(x.abs().sum(axis=1).replace(0,nan), axis=0)*a`；**不是 z-score**。
- `row_indneutralize(x, g)`（g 为分组 Series，如 `col_attrs['所属行业']`）：每个元素减其所在组在该时间截面的均值；内部用 `x.T.groupby(g).transform('mean').T` 绕开 axis=1 禁令。

**E. 算子语义细节（逐个核对，勿想当然）**
1. **`min(x, d)` / `max(x, d)` 是时序算子**（= `x.rolling(d).min()/max()`），**不是逐元素**；`np.minimum/np.maximum` 只用于 `min(A,B)/max(A,B)` 两序列形式。
   - 反例：Alpha#29 的 `min(x, 5)` 若写成 `np.minimum(x, 5)` 会变成"封顶 5"，正确是 `x.rolling(5).min()`。
2. **`Ts_ArgMax(x,N)` = `rolling_imax(x,N)*N`**（距今日天数），不是窗口内 0 基位置。
3. **`rank` 嵌套层数必须和源公式逐层对齐**：WorldQuant 里 `rank(rank(rank(x)))` 与 `rank(x)` 数值不同。
   - 反例：Alpha#31 源为 `rank(rank(rank(decay_linear(-1*rank(delta(close,10)),10))))`——decay 内 1 个 rank、外 3 个 rank；若写成 decay 内 2 个 + 外 1 个，数值就错。
   - 反例：Alpha#97 第二项源是 `Ts_Rank(...)`（仅时序 rank），手写误多包一层 `row_rank`，应去掉。
4. **`SignedPower(x,a)`**：文档字面 `x**a`，但负底 + 非整数指数会出 NaN/复数；实践用 `np.sign(x)*np.abs(x)**a`（与 WorldQuant 实际 `signedpower` 一致），需与文档取舍确认。
5. **`correlation(x,y,d)` 是时序相关** = `x.rolling(d).corr(y)`；若 x/y 本身已是截面 rank 序列，rank 在 corr **之前**先算（逐层核对括号）。

**G. 复权简化规则（用户确认，非偷懒）**
- 若因子公式**不含 shift、仅做同一天内的价格比较**（如 GTJA Alpha1/2/7/9 的 `(close-open)/open`、高低价差等），
  同一公式内所有价格项都乘同一个"当天对单只股票为常数"的 `adj_factor`，乘不乘会相消，故可直接用未复权 `d['close']`。
- **这类因子省略 `adj_factor` 是正确设计，不是"复权口径不统一"的 bug**——复查时不要误报。
- 但凡含 shift 且是比值类（如 `ac/ac.shift(N)`），必须复权，否则含义会变。
- 另：`rolling_slope`/`rolling_resi` 返回原始斜率/残差（不含 ÷价格），要无量纲须调用方 `/ac`（见 §6.5 / §6.6 标注）。

**F. 验证手段（无需 MCP 也可本地冒烟）**
- 造一份合成面板（行=时间、列=股票），用 stub 版 `row_rank/rolling_*`（含 `row_scale`/`row_indneutralize`，`row_rank`=截面 `df.rank(axis=1,pct=True)`）模拟引擎环境，
  逐个 `exec` 因子代码串，统计哪些能跑出 DataFrame、哪些抛异常。
- 本次用此法验证：注入 helper 后 **101 个中 100 个可跑通**，唯一失败是 Alpha#56 因测试数据缺 `d['总市值']` 列（`cap` 属真实 DB 字段依赖，需在 `available_data` 确认该列存在）。
- 冒烟只能验证"能否跑通/形状对"，**逻辑正确性（如上面 C/E 的数值偏差）仍需人工逐公式核对**。

### 6.9 ★ 数据缺口与入库决策约定（2026-08-13 沉淀）

转写/验证过程中常遇到"字段不在本地库"导致的 `error_code.loss_d` 报错（如 Beneish 需应收账款/营业收入/折旧绝对值、Mohanram 需折旧绝对值）。处理约定：

- **先判定信号强度**：若缺口因子已用可行近似版跑出 `|IR|≪0.3`（弱信号），**直接放弃该因子、留 `因子初始参考文件/` 不入库，不补数**——因为补库（建本地 DuckDB、用 tushare/baostock 拉数据入库）成本高、且补完也无实质价值。用户原话："需要本地数据库，创建和下载起来还比较麻烦，效果不咋样就算了。"
- **仅当信号强（|IR|>0.3）且缺口可低成本补**时才考虑走 `update-stock-mcp` 补库。
- **入库铁律**：新因子先暂存 `因子初始参考文件/` → 用 QuantAll 实跑 `batch_factor_analysis`/`run_task_file` 确认 `error_code.names=[]`（0 异常、0 缺失字段）→ 收集齐 + 验证无误才移入 `task/`；有缺失则备注交用户定夺，不擅自入库。
- **`save_path` 必须用 `output\`**（scripts/output 可写）；用 `因子初始参考文件\` 作 save_path 时引擎建目录失败、结果落不了盘。

---

## 7. 文件结构

```
stock-factor/
├── skill.md                        # 本文件（技能主文件）
├── skill_md制作.txt                # 原始起草笔记（本技能的来源草稿）
└── scripts/
    ├── Start_QuantAll.py          # 引擎启动入口
    ├── gen_report.py              # ★ 因子分析报告生成器（输出 HTML 到 scripts/）
    ├── 因子分析报告.html            # ★ gen_report.py 生成的可视化报告（自包含 HTML）
    ├── 因子收集与转写经验.md        # ★ 独立经验文档（收集+转写方法论、坑、约定、版本脉络，详见 §5 指引）
    # 注：建库/数据更新脚本（Create_DuckDB.py、UpdateStock_script.py）已移除，
    #     改由 quantall / update-stock-mcp 技能统一负责，见 §3「优先推荐」。
    ├── data/
    │   └── db_translate.json      # 数据库字段→中文名映射
    ├── task/                       # ★ 转写后的因子代码（run_task_file 执行）
    │   ├── facotr-Qlib_alpha158.json
    │   ├── factor-Qlib-Alpha360.json
    │   ├── GTJA_Alpha191.json
    │   ├── factor-Alpha101.json
    │   ├── factor-TA_Indicators.json   # 技术指标 84 个（v1.2.0 优化命名）
    │   ├── factor-stock_daily.json
    │   ├── factor-stock_report.json
    │   ├── factor-BarraCNE5.json        # Barra CNE5 十大风格因子（10 个）
    │   ├── factor-Piotroski.json        # Piotroski F-Score（9 子项+1 合成，10 个）
    │   ├── factor-AltmanZ.json          # Altman Z-Score（6 个，困境质量）
    │   └── factor-ClassicAnomalies.json # 经典学术异象（9 个，含 4 强有效反转/波动）
    ├── output/                     # ★ 因子评估结果（xlsx）
    │   ├── facotr-Qlib_alpha158.xlsx
    │   ├── facotr-Qlib_alpha360.xlsx
    │   ├── factor-GTJA_Alpha191.xlsx
    │   ├── factor-Alpha101.xlsx
    │   ├── factor-Indicators.xlsx
    │   ├── factor-stock_daily.xlsx
    │   ├── factor-stock_report.xlsx
    │   ├── factor-BarraCNE5.xlsx
    │   ├── factor-Piotroski.xlsx
    │   ├── factor-FF_HXZ.xlsx
    │   ├── factor-CITIC_Shenwan.xlsx
    │   ├── factor-WorldQuant_formulaic.xlsx
    │   ├── factor-ReturnMoment.xlsx
    │   ├── factor-Merton_CashFlow.xlsx
    │   └── factor-AccountingQuality.xlsx
    └── 因子初始参考文件/             # 收集阶段的原始表达式与转写规范（新因子先暂存此处，确认后再移入 task/）
        ├── Alpha158_因子参考.md
        ├── Alpha360_因子参考.md
        ├── 国泰君安Alpha191.txt / GTJA_Alpha191-30.txt
        ├── Alpha101.txt / Alpha101_QuantAll.json
        ├── TA-Lib指标参考.md / TA_Indicators_跳过汇总.txt
        ├── 因子表达式初始收集.md
        ├── how_code.txt            # QuantAll 代码执行环境权威说明
        ├── factor-BeneishM.json         # Beneish M-Score（10，DSRI/DEPI 缺数据，待补）
        ├── 因子收集_财务质量与学术异象.md  # 上轮来源/公式/数据缺口说明
        ├── 因子收集_FamaFrench_HXZ.md      # FF/HXZ 公式与 A 股适配说明
        ├── 因子收集_中信申万风格.md         # 中信/申万 风格因子定义与转写映射
        └── 因子收集_WorldQuant公式化alpha.md # 算子语义映射 + 公式目录 + 201/212 澄清
```

---

## 8. AI 行为规范 / 注意事项

- ✅ 本技能**依赖 QuantAll 已启动并连接**；跑更新前先确认协议窗口已确认（`ping` 通 ≠ 分析工具可用）。
- ✅ 读取因子清单直接用 `scripts/output/*.xlsx`，无需启动引擎；更新因子用 `run_task_file` 执行 `scripts/task/*.json`。
- ✅ 更新时注意 `save_path` 相对路径，确保写入 `scripts/output/`，避免覆盖或写错位置。
- ✅ 新增/转写因子时严格遵守第 6 节铁律与字段映射；写完用 `factor_analysis` 先测单因子能否跑通，再批量。
- ⚠️ 遇到"服务器忙/有其它任务在执行"先查杀残留 `python` 进程，不要反复盲目重试（QuantAll 单任务锁）。
- ⚠️ 全量评估耗时较长（单文件 60~360 因子可能数分钟~十分钟级），建议后台串行运行。
- 📁 关键文件：`scripts/task/*.json`（可执行因子代码）、`scripts/output/*.xlsx`（结果）、`scripts/gen_report.py`（报告生成器）、`scripts/因子分析报告.html`（可视化报告）、`scripts/因子初始参考文件/how_code.txt`（代码环境权威说明）、`scripts/因子初始参考文件/因子表达式初始收集.md`（收集基线）、`data/db_translate.json`（字段映射）。

---

## 9. 版本说明

### v1.3.0
**方法论定位**：本版起用户使用 WorkBuddy，由 AI 自行检索主流来源、收集公式并逐个人手写转写因子，技能进入「AI 辅助自动扩充」阶段。本版扩充两套主流因子源（均由 QuantAll 实跑验证，error_code 0 异常）：

- **新增 Barra CNE5 风格因子（10 个）**：MSCI Barra CNE5 风险模型十大风格因子（机构量化标配），含 Size/Beta/Momentum/ResidualVol/NLSIZE/BookToPrice/Liquidity/EarningsYield/Growth/Leverage。转写要点：Beta 用 `get_stock_index('000001','close')` 取上证综指作市场收益 + `rolling_regbeta(ret,mkt,252)`；NLSIZE 用 `-(row_rank(ln市值)-0.5)^2` 逆 U 代理捕捉中盘暴露。
- **新增 Piotroski F-Score（9 子项 + 1 合成 = 10 个）**：Piotroski(2000) 9 条二元会计标准（盈利 4 + 杠杆/流动性 3 + 运营效率 2），0~9 分选质量改善股。转写要点：财务数据按日向前填充，故「同比」用 `shift(252)`（≈1 年交易日）；F4 应计 `OCF/TA>ROA` ⟺ `每股OCF>每股收益`。
- **IC 说明**：两套因子在 feature_days=5 下 |IR| 均 < 0.3（Barra 最佳 Liquidity IR≈-0.29、Piotroski_FScore IR≈0.06），属「风格/质量描述符」在短周期下的常态（Barra 为风险模型暴露、Piotroski 为年度质量信号），已按技能「因子字典/候选池」定位入库，不强行以 |IR|>0.3 裁剪。

> **同一范式下的持续扩充**：在上述「AI 自行检索 + 逐人手写转写」范式下，因子库逐步扩至当前规模（**共 1101 个因子 / 18 个因子族**，详见 §1、§2）。后续陆续补充的因子族：Altman Z-Score(6)、Beneish M-Score(10，DSRI/DEPI 缺数据留参考区)、经典学术异象(9)、Fama-French/HXZ(7)、中信申万风格(12)、WorldQuant 公式化 alpha 扩展批(10)、收益高阶矩/52 周高异象(7)、Merton 违约距离/现金流收益率(5)；会计质量/困境预警(4，Ohlson/Mohanram/Novy-Marx/Sloan，信号弱留参考区)。所有新因子均手写转写 + 实跑验证（`error_code.names=[]`）。配套新建独立经验文档 `scripts/因子收集与转写经验.md`（作为 §5/§6 的扩展参考）。

### v1.2.0
本版新增技术指标因子优化、报告生成器与指数相关能力：

- **指数相关能力确立**：以 `get_stock_index` 获取指数行情（如 `'000001'` 上证综指）作为市场基准，支撑 Beta / IDIOVOL / 市场调整类因子的指数基准计算（详见 §6.3、§6.6）；指数 symbol 须 6 位纯数字，是否含数据取决于本地库是否加载该指数。
- **技术指标命名优化**：`scripts/task/factor-TA_Indicators.json` 全部 84 个因子名称改为业界通用标准命名。主要变更：① 去掉 `TA_` 前缀（如 `TA_RSI14` → `RSI14`）；② `BB_` → `BOLL_`（布林带，中文市场通用写法，如 `TA_BB_MID20` → `BOLL_MID20`）；③ `MACD` → `MACD_DIF`、`MACD_SIG` → `MACD_DEA`（中文 MACD 标准命名：DIF 快线 / DEA 慢线）；④ `ACCB_` → `ACCBANDS_`（完整 TA-Lib 函数名）；⑤ `CDLENGULFING` → `CDL_ENGULFING`（统一下划线分隔）；⑥ `LINREG` → `LINEARREG`（完整 TA-Lib 函数名）；⑦ 删除与 `TR` 完全重复的 `TA_TR_DM`（85 → 84 个）。命名对照详见 §2 TA-Lib 技术指标说明。

- **新增 gen_report.py 报告生成器**：`scripts/gen_report.py` 一键读取 `output/*.xlsx` 全部因子族数据，自动统计分析并生成可视化 HTML 报告（`scripts/因子分析报告.html`）。报告包含 KPI 总览、IR 分布、IC-IR 散点、Top 30 排行榜（含代码展开）、各因子族 Top 10 明细、数据健康度检查与后续研究建议。报告输出位置为 `scripts/` 目录（非 `output/`），图表以 base64 内嵌为自包含 HTML。详见 §4.4。

- **SKILL.md 同步更新**：§2 因子清单表更新 TA 指标行（84 个 + v1.2.0 命名优化标注）、新增 TA-Lib 技术指标命名规则说明；§4.4 新增「因子分析报告生成」使用指南；§7 文件结构补全 `gen_report.py`、`因子分析报告.html`、`factor-Alpha101.json/xlsx`、`factor-TA_Indicators.json/xlsx` 等遗漏文件。

### v1.1.0
本版为因子清单技能的一次集中修订，合并了以下改动：

- **移除建库/更新脚本**：删除 `scripts/Create_DuckDB.py` 与 `scripts/UpdateStock_script.py`，不再在本技能内维护本地 DuckDB 建库与数据更新逻辑（原因：该数据管道超出"因子清单"定位、与对外描述不匹配；底层数据准备统一改由 `quantall` / `update-stock-mcp` 技能负责，见 §3 优先推荐）。对应 §1 关系表补 `update-stock-mcp`、§3 新增"优先安装 quantall 技能"横幅、§3.1 第 7 步与 §7 文件结构同步指向上述技能。

- **Alpha101 全量转写落地**：`scripts/task/factor-Alpha101.json` 完成 101/101 手写逐个转写（含 `scale`/`indneutralize`/`Ts_ArgMax` 等全部算子、已做复权）；旧文件 `因子初始参考文件/Alpha101_QuantAll.json`、`Alpha101_跳过汇总.txt` 已被取代，可删除。

- **同步最新 QuantAll 代码环境（how_code.txt 已更新）**：`row_scale` / `row_indneutralize` / `get_stock_index`(旧名 get_index_matrix) / `rolling_regresi` / `row_mean` 现均为**内置函数**，删除全文中"须前置注入 helper""函数不存在"等过时说法，改为"直接调用"（此前 Alpha101 对照里"row_scale/row_indneutralize 须注入 helper"、GTJA"get_stock_index 函数不存在"两条疑点随环境更新自动消除）。

- **转写经验沉淀（§6.x）**：新增 §6.8「Alpha101 全量对照经验」——手写逐个转写优于脚本批量、复权底线、`adv{d}` 必须用语义 amount、rank 嵌套/ts_argmax/min(x,d) 等语义坑、本地冒烟验证法；§6.5 补 `RegBeta/RegResi` 多因子回归、修正 `scale` 旧文档误写的 z-score（应为 `sum(|x|)=a`）、补 `adv{d}`/`Ts_ArgMax`/`PROD` 算子映射、强化 `rolling_slope/rolling_resi` 不含÷价格须 `/ac` 的标注；§6.3 指数基准改 `out_type='Series'` 写法；§6.8 新增 **G. 复权简化规则**（无 shift 同日比价因子省略 adj 属正确设计、非 bug）。

