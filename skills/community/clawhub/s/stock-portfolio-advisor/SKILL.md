---
name: stock-portfolio-advisor
description: 分析A股自选与持仓，获取行情、财报、风险与新闻，按行业计算价值评分和独立交易环境分，输出基本面情景估值、数据缺口及受用户风险政策约束的配置参考，并生成离线HTML报告。适用于股票诊断、持仓复盘、投资价值评分和组合配置请求；不自动下单。 English — Deterministic value scoring and allocation for China A-share watchlists and holdings; sector-routed scoring, separate trading-environment score, scenario-based fundamental valuation, explicit data-gap reporting and constrained allocation reference; renders an offline HTML report. Pure Python stdlib, 77 unit tests. Not investment advice.

# ===== SkillHub 发布字段（上架必需，顶层）=====
slug: stock-portfolio-advisor
version: 2.4.0
displayName: 股票投资价值评分
summary: 上传持仓截图，即可给自选与持仓股票做六维量化评分（0-100），自动输出评级、目标价、止损位、评分变化归因与资产配置建议，并生成可离线打开的 HTML 报告。
category: 金融分析
tags:
  - 股票
  - 自选股
  - 持仓
  - 投资价值评分
  - 资产配置
  - A股
  - 复盘
license: MIT

# ===== 本地兼容字段 + ClawHub 分类/标签（保留）=====
metadata:
  version: 2.4.0
  categories: ["finance"]
  tags:
    - stock
    - a-share
    - china-stocks
    - portfolio
    - valuation
    - fundamental-analysis
    - quant
    - investing
    - asset-allocation
    - stock-scoring
  display_name: 自选持仓投资价值评分
  display_name_en: Stock Portfolio Investment Scoring
  description_zh: 连接腾讯自选股，输出可追溯价值评分、分行业情景估值与组合配置参考
  description_en: Evidence-based watchlist and portfolio scoring with sector-specific scenario valuation
  visibility: public
  agent_created: true
---

# 自选持仓投资价值评分

自选/持仓 → 批量取数及来源记录 → 分行业指标 → 价值与交易环境分别评分 → 基本面情景估值 → 用户政策约束配置 → HTML报告与快照。

评分和估值由 `scripts/score_engine.py` 调用 `scripts/value_model.py` 确定性计算，禁止心算评分、编造输入或直接填目标价绕过公式。模型负责取数、证据支持的定性判断、合理经营假设及说明。
v2是规则与数据质量升级，未完成历史收益校准；不能宣称更赚钱或目标价必然兑现。

## 资源与适用边界

- 计算前读 [references/indicator-mapping.md](references/indicator-mapping.md)：**v2输入字段、来源日期、估值公式和单位**。
- 判断行业与规则时读 [references/scoring-model.md](references/scoring-model.md)：评分结构、缺失门槛、模型路由、风险与配置约束。
- 取数时读 [references/data-playbook.md](references/data-playbook.md)：westock-mcp连接器与westockdata CLI命令、降级路径。
- [references/valuation-review-2026-09-05.md](references/valuation-review-2026-09-05.md)是v1问题留档，不覆盖当前v2规范。
- 历史回测/自动调权读 [references/backtesting.md](references/backtesting.md)：数据格式、滚动分区、执行模拟、启用门槛和一键命令。

主通道为已连接的westock-mcp，以及 `npx -y westock-data-skillhub@1.0.5`。先检查实际可用能力；服务字段、披露频率与数据覆盖需验证，不能把供应商缺项理解为零。
本版本针对A股。港股、美股可以记录清单，但不未经适配就套用A股行业阈值、币种与配置规则。

## 工作流

### 1. 确定清单和持仓

自选优先使用连接器`portfolio_watchlist`，不可用则读`workspace/portfolio_ledger/watchlist.json`；都没有时向用户索取名称或代码。
持仓优先采用用户提供且核对过的记录，或明确标记的模拟盘`portfolio_paper_positions`；也可读取本地`positions.json`。模拟盘不能冒充真实券商资产。
只有`holding=true`进入配置，自选未持仓只作观察。

```powershell
python scripts/portfolio_ledger.py init --dir workspace/portfolio_ledger
```

截图识别名称、代码、股数、成本价、现价，回显表格供用户核对，并询问是否还有未截到的持仓。未经核对不进入配置计算；单票基本面分析可独立继续。
核对后用`portfolio_ledger.py save-positions`保存。摊薄成本、股数单位、融资负债等陷阱见data-playbook。

### 2. 批量取数与时点留痕

把标的代码以逗号拼接，独立读取可批量执行，不必逐股拆开。

```powershell
npx -y westock-data-skillhub@1.0.5 kline sh600519,sz000725 --period day --limit 1
npx -y westock-data-skillhub@1.0.5 kline sh600519,sz000725 --period day --limit 250
npx -y westock-data-skillhub@1.0.5 finance sh600519,sz000725 --num 8
npx -y westock-data-skillhub@1.0.5 risk sh600519,sz000725
npx -y westock-data-skillhub@1.0.5 consensus sh600519,sz000725
```

以上是命令示例，不是用户真实清单。按需补充公告、资金、行业和新闻；保留原始来源、数据日、财报期、公告日、抓取时间、单位和实际/预测属性。
250日K线用于技术指标，**不能生成5年估值历史**；8期财报也不保证足够3年年度盈利或完整周期。估值历史、年度盈利、周期正常化及金融指标需另取足够样本。
北向数据先核实披露机制与供应商时间粒度；v2不依赖北向20日净流入，不能换名伪装成机构资金。

### 3. 加工v2输入

```powershell
python scripts/score_engine.py --template --output metrics.json
```

填写模板null字段，未知保持null。每项指标的`indicator_meta`必须有来源与原始数据日期；财务指标还需报告期与公告日。现价为独立`price_meta`。
财报累计值拆单季，统一TTM与归母/扣非口径；百分数20表示20%，PEG辅助计算20/20=1。
亏损、非正净资产、缺失数据是不同状态；不能用当前EPS除历史股价得到历史PE。

`risk.status`区分checked/not_checked/failed。已核查无风险用events=[]，未核查用null；ST/退市/立案必须保留标准标签。
Q/G/V有效覆盖率不足70%、关键财务字段缺失、风险未查或无有效现价/估值，输出NR而不是中性分评级。已知硬风险仍优先D。
缺失字段处置优先级（v2.4.0）：**先补数据 → 能派生就派生 → 结构性缺失（`forecast`/`industry_boom`）按期望分插补 → 观测项缺失按中性默认分60兜底**；兜底与插补都不抬高覆盖率，NR门槛不受影响，哪些分是插补/兜底来的见 `data_quality.*.imputed`/`.neutral`。大盘温度 4 项里拿到 ≥3 项即出分、按可用项权重归一（不足 3 项才"数据不足"）。

### 4. 构造适用基本面情景

明确profile：default/growth/value/cyclical/bank/broker/insurance。旧financial必须拆为具体子行业。
按scoring-model的方法路由，选一种主模型并提交bear/base/bull完整输入与非空假设、来源。可用正常化PE、ROE驱动PB、适用EV倍数、内含价值或股利/现金流折现。
参数依据公开信息、行业可比与经营预测，不能为得到期望结论倒推倍数。周期公司须说明完整周期正常化和恢复路径。没有可信假设则暂不估值。
公允价值为**估值日当前价值**，不是未来12个月股价预测。券商目标价和技术压力位独立显示，不参与估值；不要求为了凑方法数量混入不适用模型。

### 5. 读取用户配置约束

没有完整持仓、总资产口径及风险政策时，先完成个股评分报告，配置显示“暂不生成”。不要把股票资产内部占比当全部资产权重。
需要用户提供或确认的事实：风险承受度、投资期限、可承受回撤、总资产、现金需求、权益预算、其他资产比例及持仓完整性。已有信息直接复用，不重复询问。
`current_weight=股票市值/总资产×100`。每只持仓需行业、产业链敞口分组、1日内有效可交易状态记录。融资负债账户不直接套当前配置器。
市场冰点不自动满仓；权益预算取自用户政策。输出仅是单票/行业/产业链/现金约束下的参考权重，不生成订单，也不保证回撤限额。

### 6. 计算、报告、归档

```powershell
python scripts/score_engine.py --input metrics.json --output result.json
python scripts/build_report.py --result result.json --output workspace/portfolio_ledger/report.html
```

有历史快照时可传`--prev`；不同模型版本、不同档位或NR不直接比较分差，重建基线。不要硬编码历史日期充当本次分析日。
使用当前环境的文件展示能力打开HTML。报告离线可用，内嵌当前Logo，展示情景、假设、来源、数据门槛和独立交易环境。

```powershell
python scripts/portfolio_ledger.py snapshot --result result.json --dir workspace/portfolio_ledger
```

## 对话输出

给出简明结论和表格：标的、价值分/评级、交易环境分、保守/基准/乐观公允价值、安全边际、数据覆盖和关键缺口。
有合格配置参考时显示目标权重；否则说明缺哪些事实。市场温度仅描述市场环境。不要把NR写成“回避评级”，不要把未知权重写成0或100%现金。
说明估值日、数据是否实时、情景条件与风险；涨/正面沿用红色，跌/负面沿用绿色。
风险提示：公开数据量化参考，不构成投资建议，不承诺收益。

## 维护验证

v2.1增加历史时点数据构建、逐日回测、滚动调权与日期感知的权重注册。默认读取`config/weights.json`，没有有效学习版本时使用内置权重。
用户要求回测/调权时运行`run_calibration.py`；真实历史数据尚未提供时只用标为synthetic的样本验证程序，不能据此启用正式权重。
自动调权只限Q/G/V，只有真实数据与全部检验门槛通过时`--apply`才会写本地权重注册表，次日生效，不涉及任何交易。结果显示weights_version，并把调权与数据变化造成的分数变化分开归因。

```powershell
python -B -m unittest discover -s scripts -p "test_*.py" -v
```

回归测试是人工构造数据，不能冒充真实取数或收益回测。历史校准需另有按公告可得时点的数据集，包含退市样本、分红复权及费用，之后才能校准阈值和权重。
修改规则时同步value_model、模板、指标说明、报告与版本；保留原始快照以便审计。
用户另行明确要求模拟盘下单时，使用相应连接器并按实际工具规则核对价格、数量与账户；本技能计算本身不授权任何交易。
