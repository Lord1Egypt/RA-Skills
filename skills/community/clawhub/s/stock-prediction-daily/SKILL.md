---
name: stock-prediction-daily
description: "A股个股日线涨跌预测系统。七大能力：训练模型（XGBoost二分类+交叉验证+输出模型文件和报告）、优化模型（扩展特征+特征筛选）、模型预测（腾讯日线）、模型评估（日线T+1验证）、输出网页（Flask五页面仪表盘）、板块分析（直接调用stock-sector-research技能）、个股分析（直接调用stock-watchlist-briefing技能）。Use when: 股票预测, stock prediction, 训练模型, train model, 模型优化, optimize model, 模型预测, predict stock, 模型评估, evaluate model, 预测网页, prediction dashboard, 板块分析, sector research, 个股分析, watchlist briefing, XGBoost, A股, 沪深300, daily prediction, 日线预测"
argument-hint: "指定能力：训练/优化/预测/评估/网页/板块/个股，或一键全部执行"
---
# A股个股日线涨跌预测系统

基于沪深300成份股日线数据训练 XGBoost 二分类模型，预测个股下一个交易日的价格涨跌方向。预测与评估均统一使用腾讯财经日线数据，预测和评估两个步骤相互独立。除预测主流程外，本 skill 还提供两个研究入口：板块分析直接复用 `stock-sector-research`，个股分析直接复用 `stock-watchlist-briefing`。

## 使用约束

- 训练、优化、预测、评估、网页能力仅使用当前 skill 目录内的文件和子目录，不要读取、修改或依赖 skill 目录外的实现文件。
- 板块分析能力不在当前目录内重复实现，直接调用 `stock-sector-research` skill。
- 个股分析能力不在当前目录内重复实现，直接调用 `stock-watchlist-briefing` skill。
- 默认工作目录为 `.github/skills/stock-prediction-daily/scripts/`。
- 运行、修改、排查当前 skill 自带功能时，只使用 `scripts/` 和 `references/` 下的内容。

## 项目结构

```
.github/skills/stock-prediction-daily/
├── SKILL.md           # 技能说明
├── references/        # 参考说明与排障文档
└── scripts/
   ├── config.py          # 配置中心（路径、股票池、超参数）
   ├── features.py        # 特征工程（100+候选技术指标）
   ├── train.py           # 训练流水线（获取数据→特征→选择→交叉验证→保存）
   ├── predict.py         # 预测流水线（腾讯日线）
   ├── evaluate.py        # 评估流水线（日线T+1验证）
   ├── app.py             # Flask网页仪表盘
   └── main.py            # 一键执行入口
```

运行过程中生成的 `data/`、`models/`、`results/`、`templates/`、`static/` 目录都位于 `scripts/` 目录下，由 `scripts/config.py` 自动创建。
其中 `scripts/reports/` 用于保存板块分析和个股分析的文本报告，网页页面会直接读取该目录中的文件进行展示。

## 技术栈

- **数据源**: akshare Tencent日线 `stock_zh_a_hist_tx`
- **模型**: XGBoost `XGBClassifier` 二分类
- **序列化**: joblib（不用 xgboost 原生 `save_model`）
- **Python**: 使用 `python3`
- **Web**: Flask + Jinja2，端口 5000

## 能力一：训练模型

### 触发条件

用户要求训练模型、构建预测系统、或首次搭建项目时执行。

### 流程

1. **获取训练数据**

   - 获取沪深300成份股列表：`ak.index_stock_cons()` 或 `ak.index_stock_cons_csindex(symbol="000300")`
   - 逐只获取日线数据：`ak.stock_zh_a_hist_tx(symbol, start_date, end_date, adjust="qfq")`
   - 缓存到 `scripts/data/{code}_daily.csv`
   - 请求节流由 `scripts/config.py` 的 `FETCH_DELAY` 控制
2. **特征工程**

   - 调用 `features.add_technical_features(df)` 计算技术指标特征
   - 调用 `features.create_label(df)` 生成标签：下一期 `close > 当前 close` 则为 1
3. **特征选择**

   - 使用 XGBoost `feature_importances_` 排序
   - 取 `config.TOP_N_FEATURES` 个最重要特征
4. **交叉验证**

   - 10 折分层交叉验证 `StratifiedKFold`
   - 指标：Accuracy、Precision、Recall、F1、AUC
5. **保存模型和报告**

   - 模型：`scripts/models/xgb_stock_model.pkl`
   - 归一化器：`scripts/models/scaler.pkl`
   - 特征名：`scripts/models/feature_names.json`
   - 报告：`scripts/results/model_report.json`

### 关键代码模式

```python
df = ak.stock_zh_a_hist_tx(symbol="sh600436", start_date="20240101", end_date="20260315", adjust="qfq")

import joblib
joblib.dump(model, config.MODEL_PATH)
model = joblib.load(config.MODEL_PATH)
```

### 缓存策略

训练数据缓存在 `scripts/data/`，重新训练时可直接复用缓存 CSV。

## 能力二：优化模型效果

### 触发条件

用户要求提升准确率、增加特征、调参、或模型效果不理想时。

### 优化维度

1. **扩展候选特征**

   - 在 `scripts/features.py` 的 `add_technical_features()` 中添加新特征
   - 在 `scripts/features.py` 的 `get_all_feature_columns()` 中注册特征名
2. **调整特征数量**

   - 修改 `scripts/config.py` 中的 `TOP_N_FEATURES`
3. **调整 XGBoost 超参数**

   - 修改 `scripts/config.py` 中的 `XGB_PARAMS`
4. **重新训练**

   - 可直接复用缓存日线 CSV 重新训练，无需重新抓取数据

## 能力三：模型预测

### 触发条件

用户要求预测特定股票在特定日期的涨跌方向。

### 预测逻辑

- 只使用腾讯财经日线数据 `stock_zh_a_hist_tx`
- 对目标日期取不晚于该日期的最近一个交易日 bar
- 在该日线 bar 上计算与训练一致的特征
- 输出下一交易日涨跌方向概率

### 启动方式

```bash
cd .github/skills/stock-prediction-daily/scripts
python3 predict.py "2026-03-13"
```

### 输出格式

CSV 含字段：股票代码、股票名称、当前时间、预测生成时间、当前价格、预测结果、上涨概率、下跌概率、数据频率。

说明：

- `当前时间` 只精确到日期，例如 `2026-03-13`
- `预测生成时间` 精确到秒，用于区分同一交易日的多次预测批次
- `数据频率` 固定为腾讯日线
- `scripts/results/predictions.csv` 为去重后的主表，按 `股票代码 + 当前时间` 只保留最新一批预测结果
- 每次预测还会额外生成 `scripts/results/prediction_history/predictions_YYYYMMDD_HHMMSS.csv` 批次快照，用于保留完整历史

## 能力四：模型评估

### 触发条件

用户要求评估预测准确率、验证模型效果。

### 评估逻辑

- 独立读取 `scripts/results/predictions.csv`
- 对每条预测重新获取腾讯财经日线数据
- 取预测日期之后的下一个交易日收盘价进行评估
- 计算实际涨跌与预测是否一致

### 启动方式

```bash
cd .github/skills/stock-prediction-daily/scripts
python3 evaluate.py
```

### 输出格式

CSV 含字段：股票代码、股票名称、预测时间、预测生成时间、当时价格、预测结果、上涨概率、预测数据频率、一天后价格、评估数据频率、实际涨跌、预测是否准确。

说明：

- `一天后价格` 表示下一个可用交易日的收盘价
- 若预测后尚无新交易日数据，则该字段为 `N/A`
- 若同一支股票同一天存在多次预测，评估时以 `predictions.csv` 主表中的最新批次为准

## 能力五：输出网页

### 触发条件

用户要求启动网页、展示结果、或搭建仪表盘。

### Flask应用结构

- `/predictions` — 日线预测结果表格
- `/report` — 模型训练报告
- `/evaluation` — 日线 T+1 评估结果表格
- `/sector-analysis` — 板块分析报告浏览页，自动读取 `scripts/reports/sector_analysis/` 中的报告
- `/stock-analysis` — 个股分析报告浏览页，自动读取 `scripts/reports/stock_analysis/` 中的报告
- `/` — 重定向到 `/predictions`

说明：

- 板块分析和个股分析页面都以报告文件为唯一数据源，不再展示独立的介绍页内容。
- 页面左侧提供报告选择菜单，菜单项显示“报告主标题 + 创建时间”，可在多份历史报告之间切换。
- 页面正文会完整渲染报告内容，并自动格式化一级/二级标题、列表、表格。
- 页面会从 Markdown 报告中的表格自动提取结构化信息，生成摘要卡片与简单图表。
- 左侧章节导航只展示一级章节，不展示子章节，避免导航过长。

### 页面模板

- `base.html`：布局和导航
- `predictions.html`：预测表格与统计卡片
- `report.html`：报告 JSON 展示
- `evaluation.html`：评估表格与准确率统计
- `sector_analysis.html`：板块分析报告页
- `stock_analysis.html`：个股分析报告页

### 启动方式

```bash
cd .github/skills/stock-prediction-daily/scripts
python3 app.py
```

## 一键执行

```bash
cd .github/skills/stock-prediction-daily/scripts
python3 main.py
```

依次执行：训练 → 预测 → 评估 → 启动网页。

## 能力六：板块分析

### 触发条件

用户要求查看近阶段重点板块、板块排行、新闻催化、资金流向、龙头股或下周板块观察清单。

### 执行方式

- 不在当前 skill 内重复实现板块研究逻辑。
- 直接调用 `stock-sector-research` skill。
- 调用时沿用用户原始问题中的时间范围、主题范围和输出形式要求。
- 调用完成后，将最终输出保存到 `scripts/reports/sector_analysis/` 目录。
- 文件格式优先使用 Markdown，命名建议为 `sector_analysis_YYYYMMDD_HHMMSS.md`。

### 默认输出

- 重点板块排序
- 每个重点板块的催化、资金与交易逻辑
- 每个板块 2 到 3 只核心股
- 下周观察清单或盘前清单

### 保存要求

- 报告正文必须可直接阅读，不要只保存摘要。
- 报告开头必须包含统一头部，顺序如下：一级标题、单独一行的副标题、单独一行的报告时间。
- 主标题和副标题都必须直接体现报告结论，不能使用“板块分析报告”“个股分析报告”“近7天重点信息汇总”这类泛泛标题。
- 主标题必须简短，控制在一句短结论内，优先写成 6 到 16 个字，不要把全部判断塞进主标题。
- 主标题应概括最重要的结论，例如：`# 主线聚焦新能源`、`# 算力分化创新药走强`。
- 副标题再补充次级判断或执行结论，例如：`> 副标题：风电与锂电强度最高，算力分化加大，创新药更适合中线跟踪`。
- 头部格式仍保持三行结构：主标题、以 `> 副标题：` 开头的副标题、`报告时间：YYYY-MM-DD HH:MM:SS`。
- 优先使用分节标题、列表和表格，便于网页端自动格式化和提取图表数据。
- 主章节优先使用 `##`，例如“重点板块排序”“核心股对比表”“下周观察清单”“风险提示”。
- 若主章节下需要展开细分内容，可使用 `###` 子章节，但网页左侧导航默认只展示 `##` 主章节。
- 同一次分析如有补充说明，合并写入同一个报告文件，不拆成多个零散文件。

## 能力七：个股分析

### 触发条件

用户要求分析一组 A 股个股近 3 天、5 天、7 天或 1 个月的重要信息，或要求输出观察清单、优先执行标的和买点止损位。

### 执行方式

- 不在当前 skill 内重复实现多股票研究逻辑。
- 直接调用 `stock-watchlist-briefing` skill。
- 调用时保留用户给定的股票列表、时间范围和输出深度。
- 调用完成后，将最终输出保存到 `scripts/reports/stock_analysis/` 目录。
- 文件格式优先使用 Markdown，命名建议为 `stock_analysis_YYYYMMDD_HHMMSS.md`。
- 个股分析默认以 A 股为主；若用户给出的名单中包含港股，可保留该标的，但要在报告中单独标注“港股口径”。
- 港股行情或估值接口不稳定时，允许退回到稳定的公开港股报价页、公司业绩公告和主流财经媒体摘要；不要把港股强行套用 A 股接口，也不要伪造精确技术位。

### 默认输出

- 多股票概览表
- 下周观察清单
- 优先执行标的
- 买点、突破位、止损位、减仓位

### 保存要求

- 报告正文必须保留股票分组、结论和执行位信息。
- 报告开头必须包含统一头部，顺序如下：一级标题、单独一行的副标题、单独一行的报告时间。
- 主标题和副标题都必须直接体现报告结论，不能使用“个股分析报告”“股票观察清单”“多股汇总”这类泛泛标题。
- 主标题必须简短，控制在一句短结论内，优先写成 6 到 16 个字，不要把多只股票的全部判断都写进主标题。
- 主标题应先给出最核心的股票结论，例如：`# 宁德时代仍是首选`、`# 立讯精密暂不追高`。
- 副标题再补充组合判断、时间范围或执行优先级，例如：`> 副标题：片仔癀偏防守配置，未来7天执行优先级低于宁德时代`。
- 头部格式仍保持三行结构：主标题、以 `> 副标题：` 开头的副标题、`报告时间：YYYY-MM-DD HH:MM:SS`。
- 优先使用分节标题、列表和表格，便于网页端自动格式化和提取图表数据。
- `## 全名单概览表` 若使用 Markdown 表格，表头固定为：`股票 | 近 7 日涨跌幅 | 近 7 日成交额合计 | 最近正式财务口径 | 周内重点信息 | 一句话建议`。
- 不要把上述固定表头改成“近 7 日涨跌”“近 7 日涨跌/状态”等变体。
- 若个别标的无法稳定给出近 7 日涨跌幅，仍保留固定表头，并在对应单元格填写 `N/A`；口径说明写入“研究口径”或“周内重点信息”，不要通过修改列名表达。
- 主章节优先使用 `##`，例如“先看结论”“全名单概览表”“下周观察清单”“优先执行标的”“风险提示”。
- 若主章节下需要展开分组，可使用 `###` 子章节，但网页左侧导航默认只展示 `##` 主章节。
- 同一批股票的研究结果尽量输出为单文件，避免网页端阅读碎片化。
- 若报告包含港股标的，研究口径章节应明确区分 A 股与港股的数据来源；对于无法稳定获取 MA5、MA10、20 日高低点的港股，只写可核对的价格区间和事件驱动，不要硬补精确数值。

## API注意事项


| API         | 函数                 | 用途             | 注意         |
| ----------- | -------------------- | ---------------- | ------------ |
| Tencent日线 | `stock_zh_a_hist_tx` | 训练、预测、评估 | 稳定，不限频 |

## 常见问题

- **`python` 不可用**：macOS 使用 `python3`
- **模型加载报错**：必须用 `joblib.load()`，不用 `xgb.load_model()`
- **预测字段时间精度**：`当前时间` 只保留日期，不含时分秒
- **次日评估无数据**：如果下一交易日尚未收盘，`一天后价格` 会是 `N/A`
- **运行路径**：先进入 `.github/skills/stock-prediction-daily/scripts` 再执行脚本
