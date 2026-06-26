---
name: tradingagents-cn-skill
version: 2.0.0
description: >
  股票多智能体分析报告生成。通过 6 个分析师串行分析 + 多空辩论 + 交易计划 + 风险评估，
  生成专业 PDF 报告。触发场景：用户要求分析股票、生成股票报告、提供截图或代码进行分析、
  询问买卖建议、要求技术分析或基本面分析或风险评估。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
---

# TradingAgents-CN Skill

多智能体股票分析框架。Agent 串行完成 12 步分析，每步调用 LLM 并通过脚本验证输出，最终生成 PDF 报告。

## 全局规则

### 重试协议

每次 LLM 调用后，**必须**通过 `validate_step.py` 验证输出：

```bash
echo '<LLM原始输出>' | python3 {baseDir}/scripts/validate_step.py --step <步骤名> --stock-code <股票代码> --attempt <次数>
```

**处理规则：**
- `exit 0` → stdout 是清洗后的 JSON，保存结果，进入下一步
- `exit 1` → stderr 是 JSON 错误信息（含 `hint` 字段），将 hint 追加到 prompt 重新调用 LLM
- 关键步骤（bull、bear、manager、trader、risk_manager）最多重试 **3 次**
- 次要步骤（tech、fundamentals、news、social、debate、risk_debate）最多重试 **2 次**
- 超过重试上限 → 获取默认值继续：
  ```bash
  python3 {baseDir}/scripts/validate_step.py --step <步骤名> --default
  ```

**重试时的 prompt 追加格式：**
```
注意：上次输出格式有误。{hint}。请严格按纯 JSON 格式返回，不要用 markdown 代码块包裹。
```

### 日志

分析开始前，设置日志环境变量，确保同一次分析的所有步骤写入同一日志文件：

```bash
export TRADINGAGENTS_LOG_FILE="{baseDir}/scripts/logs/{股票代码}_{YYYYMMDD}_{HHMMSS}.log"
mkdir -p {baseDir}/scripts/logs
```

分析结束后，告知用户日志文件路径。

### 语言要求

所有 LLM 调用的 system_prompt 和 user_message 使用**中文**。所有分析内容使用**中文**输出。

---

## 工作流程

```
Step 1A: 获取原始文本（截图 → OCR / 文字 → 直接使用）
Step 1B: 结构化提取 LLM → validate → stock_data JSON
Step 2:  web_search 获取新闻 → news_data
Step 3:  多头分析师 LLM → validate → bull_analyst
Step 4:  空头分析师 LLM → validate → bear_analyst
Step 5:  技术分析师 LLM → validate → tech_analyst
Step 6:  基本面分析师 LLM → validate → fundamentals_analyst
Step 7:  新闻分析师 LLM → validate → news_analyst
Step 8:  社交媒体分析师 LLM → validate → social_analyst
Step 9:  多空辩论 + 研究经理决策 LLM → validate → debate + manager_decision
Step 10: 交易员计划 LLM → validate → trading_plan
Step 11: 风险辩论 + 风险经理评估 LLM → validate → risk_debate + final_decision
Step 12: 组装 JSON → 生成 PDF
```

---

## Step 1A: 获取原始文本

根据用户输入类型，获取原始文本：

**情况 1：用户提供截图/图片**
- 调用 OCR MCP tool（如 `image-ocr`）或 Agent 内建的图片识别能力
- 将识别结果作为原始文本
- 截图可能包含：K 线图、技术指标面板、财报数据、交易软件截图等

**情况 2：用户提供文字描述**
- 直接使用用户提供的文字作为原始文本

**情况 3：用户只提供股票代码/名称**
- 将股票代码和名称作为原始文本，后续步骤会通过 web_search 补充数据

---

## Step 1B: 结构化数据提取

**LLM 调用：**
- system_prompt:
  ```
  你是股票数据提取专家。从用户提供的文本（可能来自截图OCR、交易软件、财报等）中，
  提取结构化的股票数据。只提取文本中明确存在的信息，缺失的字段设为 null。
  不要虚构或推测任何数据。以纯 JSON 格式返回。
  ```
- user_message:
  ```
  请从以下文本中提取股票数据，以纯 JSON 格式返回：

  {原始文本}

  要求返回的 JSON 格式：
  {
    "stock_code": "股票代码（如 PDD、600519、HK.00700）",
    "stock_name": "股票名称",
    "current_price": 数字或null,
    "change_pct": "涨跌幅字符串或null",
    "volume": "成交量或null",
    "turnover": "成交额或null",
    "technical_indicators": {
      "MA5": 数字或null,
      "MA10": 数字或null,
      "MA20": 数字或null,
      "MA60": 数字或null,
      "RSI": 数字或null,
      "MACD": "描述或null",
      "KDJ": "描述或null",
      "BOLL_upper": 数字或null,
      "BOLL_mid": 数字或null,
      "BOLL_lower": 数字或null
    },
    "fundamentals": {
      "PE": 数字或null,
      "PB": 数字或null,
      "ROE": "字符串或null",
      "market_cap": "字符串或null",
      "revenue": "字符串或null",
      "net_profit": "字符串或null"
    },
    "k_line_pattern": "K线形态描述或null（如：近5日缩量调整、均线多头排列等）",
    "other_info": "其他有价值的信息或null"
  }
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step parse_input --stock-code {股票代码} --attempt 1
```

**后处理：**
- 将验证通过的 JSON 保存为 `stock_data`
- 从 `stock_data` 中提取 `stock_code` 和 `stock_name` 供后续步骤使用
- 构建 `text_description`：将 `stock_data` 格式化为可读文本，包含所有非 null 字段：
  ```
  股票代码: {stock_code}
  股票名称: {stock_name}
  当前价格: ¥{current_price}
  涨跌幅: {change_pct}
  技术指标: MA5={MA5}, MA10={MA10}, RSI={RSI}, MACD={MACD} ...
  基本面: PE={PE}, PB={PB}, 市值={market_cap} ...
  K线形态: {k_line_pattern}
  ```
- 缺失字段标注"待获取"

---

## Step 2: 获取新闻数据

使用 web_search 搜索 4 次：

```
web_search: "{股票代码} {股票名称} 最新新闻"
web_search: "{股票代码} 财报 业绩"
web_search: "{股票名称} 分析师评级"
web_search: "{股票代码} 技术分析 走势"
```

**过滤规则**：只保留最近 **3 天内**（不含当天）的新闻。

构建 `news_data` 列表，每条必须包含：`title`、`date`（YYYY-MM-DD）、`source`、`summary`（≤50 字，基于 title+snippet 生成）、`sentiment`（偏多/偏空/中性）。

---

## Step 3: 多头分析师

**LLM 调用：**
- system_prompt: 读取 `references/bull_prompt.md` 的完整内容
- user_message:
  ```
  请分析以下股票，以纯 JSON 格式返回分析结果，不要用 markdown 代码块包裹。

  {text_description}

  近期新闻：
  {news_data 格式化列表}
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step bull_analyst --stock-code {股票代码} --attempt 1
```

**保存：** 将验证通过的 JSON 存为 `bull_analyst` 结果。

---

## Step 4: 空头分析师

**LLM 调用：**
- system_prompt: 读取 `references/bear_prompt.md`
- user_message: 同 Step 3 格式

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step bear_analyst --stock-code {股票代码} --attempt 1
```

---

## Step 5: 技术分析师

**LLM 调用：**
- system_prompt: 读取 `references/tech_prompt.md`
- user_message: 同 Step 3 格式

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step tech_analyst --stock-code {股票代码} --attempt 1
```

---

## Step 6: 基本面分析师

**LLM 调用：**
- system_prompt: 读取 `references/fundamentals_prompt.md`
- user_message: 同 Step 3 格式

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step fundamentals_analyst --stock-code {股票代码} --attempt 1
```

---

## Step 7: 新闻分析师

**LLM 调用：**
- system_prompt: 读取 `references/news_prompt.md`
- user_message: 同 Step 3 格式

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step news_analyst --stock-code {股票代码} --attempt 1
```

---

## Step 8: 社交媒体分析师

**LLM 调用：**
- system_prompt: 读取 `references/social_prompt.md`
- user_message: 同 Step 3 格式

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step social_analyst --stock-code {股票代码} --attempt 1
```

---

## Step 9: 多空辩论 + 研究经理决策

### 阶段 A: 多空辩论

**LLM 调用：**
- system_prompt: "你是一位专业的投资辩论主持人。"
- user_message:
  ```
  以下是多头和空头的观点：

  多头观点：
  {bull_analyst 的 analysis 部分，JSON 格式}

  空头观点：
  {bear_analyst 的 analysis 部分，JSON 格式}

  请进行 2 轮辩论，每轮让多头反驳空头、空头反驳多头。
  以纯 JSON 格式返回，不要用 markdown 代码块：
  {"rounds": [{"round": 1, "bull_points": ["论点1", "论点2"], "bear_points": ["论点1", "论点2"]}]}
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step debate --stock-code {股票代码} --attempt 1
```

### 阶段 B: 研究经理决策

**LLM 调用：**
- system_prompt: 读取 `references/manager_prompt.md`
- user_message:
  ```
  基于以下分析师观点，给出最终决策。

  {text_description + news_data 上下文}

  分析师汇总：
  {bull_analyst, bear_analyst, tech_analyst, fundamentals_analyst, news_analyst 的 analysis 和 sentiment 摘要，JSON 格式}

  辩论结果：
  {debate 结果 JSON}

  请以纯 JSON 格式返回：
  {"decision": "买入/卖出/持有", "rationale": "核心逻辑"}
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step manager --stock-code {股票代码} --attempt 1
```

---

## Step 10: 交易员计划

**LLM 调用：**
- system_prompt: 读取 `references/trader_prompt.md`
- user_message:
  ```
  研究经理决策: {manager_decision.decision}
  理由: {manager_decision.rationale}
  当前股价: {current_price} 港元

  请根据决策制定交易计划，以纯 JSON 格式返回：

  decision 为"买入"时：
  {"buy_price": 回调入场价（当前价×0.98）, "target_price": 目标价（buy_price×1.10~1.20）, "stop_loss": 止损价（buy_price×0.92~0.95）, "position_size": "15%-20%", "entry_criteria": "...", "exit_criteria": "..."}

  decision 为"持有/观望"时：
  {"buy_price": null, "target_price": null, "stop_loss": null, "position_size": "0%", "reference_price": 当前价, "reference_target": 当前价×1.10, "reference_stop": 当前价×0.95, "entry_criteria": "观望理由和入场条件", "exit_criteria": "不适用"}
  ```

**注意：**
- buy_price/target_price/stop_loss **仅在 decision="买入" 时必填数字**
- 持有/观望时这三个字段**允许为 null**
- 任何决策都必须包含 position_size（非 null）
- price 必须使用数字类型（如 1.37），不允许文字描述

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step trader --stock-code {股票代码} --attempt 1
```

**后处理：** 将 `manager_decision.decision` 写入 trading_plan 的 `decision` 字段。

---

## Step 11: 风险评估

### 阶段 A: 三方风险辩论

**LLM 调用：**
- system_prompt: 读取 `references/risk_debate_prompt.md`
- user_message:
  ```
  交易计划：
  {trading_plan JSON}

  {text_description + news_data 上下文}

  请从激进派、中性派、保守派三个角度辩论，以纯 JSON 格式返回：
  {"aggressive": {"stance": "...", "points": [...]}, "moderate": {"stance": "...", "points": [...]}, "conservative": {"stance": "...", "points": [...]}}
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step risk_debate --stock-code {股票代码} --attempt 1
```

### 阶段 B: 风险经理最终评估

**LLM 调用：**
- system_prompt: 读取 `references/risk_manager_prompt.md`
- user_message:
  ```
  交易计划：{trading_plan JSON}
  三方风险辩论观点：{risk_debate JSON}

  {text_description + news_data 上下文}

  请综合评估，以纯 JSON 格式返回：
  {"final_recommendation": "买入/卖出/持有", "risk_level": "低/中/高", "investment_horizon": "短期/中期",
   "risk_assessment": {"市场风险": "...", "流动性风险": "...", "波动性风险": "..."},
   "suitable_investors": ["稳健型"], "monitoring_points": ["..."]}
  ```

**验证：**
```bash
echo '<LLM输出>' | python3 {baseDir}/scripts/validate_step.py --step risk_manager --stock-code {股票代码} --attempt 1
```

---

## Step 12: 生成 PDF 报告

将所有结果组装为完整 JSON（格式详见 `references/data_schema.md`）：

```json
{
  "stock_code": "{股票代码}",
  "stock_name": "{股票名称}",
  "current_price": {当前价格},
  "timestamp": "{ISO 8601 时间戳}",
  "parallel_analysis": {
    "bull_analyst": {Step 3 结果},
    "bear_analyst": {Step 4 结果},
    "tech_analyst": {Step 5 结果},
    "fundamentals_analyst": {Step 6 结果},
    "news_analyst": {Step 7 结果},
    "social_analyst": {Step 8 结果}
  },
  "debate": {Step 9A 结果},
  "manager_decision": {Step 9B 结果},
  "trading_plan": {Step 10 结果},
  "risk_debate": {Step 11A 结果},
  "final_decision": {Step 11B 结果}
}
```

调用脚本生成 PDF：

```bash
echo '<完整JSON>' | python3 {baseDir}/scripts/generate_report.py --stdin
```

脚本输出 PDF 文件路径。

**重要：必须将 PDF 文件直接发送给用户，不要只显示文件路径。** 使用文件发送能力将 PDF 作为附件发给用户，让用户可以直接下载查看。

同时附上简要的分析摘要：
- 核心结论（买入/卖出/持有）
- 关键价格：买入价、目标价、止损价
- 风险等级和投资期限
- 一句话看多/看空逻辑

---

## 输出文件

PDF 保存到 `{baseDir}/scripts/reports/`，文件名格式：`{股票代码}_{YYYYMMDD}_{HHMMSS}.pdf`

---

## 调试方法

### CLI 直接触发
```bash
openclaw agent --message "分析一下 PDD" --verbose on --json
```

### 单步验证工具
```bash
# 测试某个 LLM 输出是否通过验证
echo '{"bull_detail":{"core_logic":"test","bull_case":["point1"]}}' | python3 {baseDir}/scripts/validate_step.py --step bull_analyst

# 获取某步骤的默认值
python3 {baseDir}/scripts/validate_step.py --step bull_analyst --default
```

### 日志查看
```bash
# 查看最新日志
cat {baseDir}/scripts/logs/latest.log

# 查看指定股票的日志
ls {baseDir}/scripts/logs/PDD_*.log
```
