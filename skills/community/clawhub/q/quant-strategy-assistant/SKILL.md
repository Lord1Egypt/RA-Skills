---
name: quant-strategy-assistant
description: "量化策略助手：自然语言→策略生成→回测→优化→QMT模拟/实盘。三轮交互闭环。"
metadata:
  requires:
    bins: ["python3"]
  openclaw:
    requires:
      bins: ["python3"]
---

# 量化策略助手

> **兼容说明**：本文档既是 OpenClaw Skill，也可作为任意 AI Agent 的操作手册。只要 Agent 能读取文件、执行命令、生成代码，即可按下方协议使用。YAML 头部的 `metadata.openclaw` 为 OpenClaw 平台专用字段，其他 Agent 忽略即可。

回测三轮交互闭环 → 用户按需选择参数优化 / 模拟实盘。

## 能力分层

| 能力 | 引擎 | 依赖 | 说明 |
|------|------|------|------|
| **CTA回测** | vnpy_ctastrategy | python3 + qgdata | 单标的择时策略，任意平台 |
| **Portfolio回测** | vnpy_portfoliostrategy | python3 + qgdata | 多标的组合/轮动策略，任意平台 |
| **参数优化** | vnpy OptimizationSetting | 同回测 | 回测后由用户触发，穷举/遗传算法 |
| **模拟/实盘** | miniQMT + vnpy CTA引擎 | QMT 交易端 | `qmt-check` 检测 → `trade` 启动自动交易，含探针单验证 |

回测是核心能力，不依赖 QMT。用户请求模拟/实盘时才运行 `qmt-check`。

### CTA vs Portfolio 自动路由（强制）

| 条件 | 模式 | 策略基类 |
|------|------|----------|
| 单一标的 + 无组合关键词 | `cta` | `CtaTemplate` |
| 以下任一条件满足 | `portfolio` | `StrategyTemplate`（vnpy_portfoliostrategy） |

**portfolio 判定规则（分层，LLM 和 `parse_requirement()` 均遵循）**：
1. **强信号**（任一出现即 portfolio）：`轮动/组合/多标的/全市场/等权/仓位分配/前N名`
2. **弱信号 + 多标的上下文**（二者共现才 portfolio）：弱信号 `排序/筛选/选股/调仓/排列/持仓周期` 需同时存在多标的上下文（`板块/成分股/指数/行业/概念/股票池`）
3. **标的数量 > 1**：`--symbols` 含 2 只以上自动 portfolio

注意："多头排列"中的"排列"、"均线排序"在单标的场景不触发 portfolio。

路由由 `parse_requirement()` 自动判定并写入 `parsed["mode"]`，agent 生成策略代码时必须使用对应基类。

**Portfolio 引擎驱动约束**：Portfolio 回测引擎仅支持 DAILY 和分钟级驱动。周级策略用 `--interval DAILY`，在 `on_bars(bars)` 中按 `list(bars.values())[0].datetime.weekday()==0`（周一）判断调仓日；周线指标直接用 `pro.weekly()` 获取，无需从日线合成。

**股票池所有权契约（强制）**：股票池由 `--symbols` 参数唯一定义 → 引擎加载数据 → 策略通过 `self.vt_symbols` 接收。策略代码 `__init__` 中**禁止覆盖 `vt_symbols`**，必须使用引擎传入的列表。所有标的代码使用 vnpy 格式（`600519.SSE`/`000858.SZSE`），不可使用 qgdata 格式（`.SH/.SZ`）。选股逻辑在 `on_bars(bars)` 中基于 `self.vt_symbols` 遍历和筛选。

**板块/指数成分股由引擎自动解析（强制）**：用户说"人工智能板块"/"沪深300成分股"/"银行行业"等时，引擎会自动解析出完整成分股列表到 `--symbols`。策略代码中**禁止**自行调用 `pro.ths_member()`/`pro.ths_index()`/`pro.dc_member()` 等板块 API。

**回测日期约束（强制）**：用户的回测日期意图必须由你转换为标准 `--start YYYYMMDD --end YYYYMMDD` 参数。例如用户说"最近1年"则根据当天日期计算 today-365 输出对应日期。用户未提及任何日期时，**不传** `--start/--end`（引擎默认最近1年，即 today-365 ~ today）。第1轮确认摘要中日期栏必须写"引擎默认最近1年"而非自行编造"近2年"等。**禁止**编造与用户意图不符的固定日期。

### 模拟/实盘交易（独立流程，不走三轮协议）

用户提及 `模拟`/`实盘`/`模拟交易`/`开始交易`/`QMT` 时触发。**前提：至少有一次成功的回测（status=completed）。**

**第 1 步：环境检测**（自动发现 QMT 路径，无需用户手动配置路径）

```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" qmt-check
```

输出 JSON 含 `ready`（布尔）和 `hint`（状态说明）：
- `platform != Windows` → 提示用户在 Windows + QMT 环境运行
- QMT 路径自动扫描失败 → 提示确认 QMT 已安装
- QMT 终端未运行 → 提示"请先打开 QMT 并以极简模式登录"
- 缺少资金账号 → 提示通过 `--account-id` 或 `QMT_ACCOUNT_ID` 提供
- `ready=true` → 进入第 2 步

**第 2 步：启动交易**（内含自动探针验证：100股跌停价挂单→确认→撤单，可选单独跑 `probe --symbol {代码} --account-id {账号}`）

```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" trade \
  --run-id "{最近成功回测的 run_id}"
```

返回 JSON 分流：
- `status=trading_started` → 告知用户：✅ 交易已启动，附带日志路径
- `status=platform_redirect` → 告知用户：需在 Windows + QMT 环境运行，给出命令
- `status=error` → 告知具体错误

**第 3 步：停止交易**（用户说「停止交易」时）

```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" trade-stop --run-id "{run_id}"
```

仅需用户提供 **资金账号**（`--account-id` 或 `QMT_ACCOUNT_ID`）；QMT 路径自动扫描各盘符下 `userdata_mini` 目录（可通过 `QMT_PATH` 覆盖）。

## 环境

| 项目 | 值 |
|------|---|
| 项目根目录 | `QUANTCLAW_ROOT`（兼容 `QMT_PROJECT_ROOT`） |
| vnpy_qmt源码 | `$QUANTCLAW_ROOT/vnpy_qmt` |
| 策略输出 | `$QUANTCLAW_ROOT/strategies/` |
| 回测输出 | `$QUANTCLAW_ROOT/backtests/` |
| 回测数据源 | qgdata（建议预先配置 `QGDATA_TOKEN`） |
| 实盘交易 | miniQMT (xt_gateway.py)，需 QMT 交易端已启动 |
| Python解释器 | `PYTHON_BIN`（默认 `python3`） |

回测默认参数：`capital=1000000 / rate=0.0003 / slippage=0.01 / size=1 / pricetick=0.01`

配置指南: https://gitee.com/GuojinQuant/quant-claw#第四步配置环境变量 （仓库自带 `.env.example`）

关键变量（优先从 `.env` / 环境变量自动推导，不需要写死）：
- `QUANTCLAW_ROOT`：项目根目录（兼容 `QMT_PROJECT_ROOT`）
- `MONITOR_PUBLIC_BASE`：监控公网基址（可留空；OpenClaw 环境下可由 `OPENCLAW_CONTROL_URL` 自动推导）
- `ORCH_MONITOR_PORT_CANDIDATES`：白名单端口（默认 `8767`，必须在防火墙放通）
- `QGDATA_TOKEN`：数据 Token（可选；未配置时自动使用内置共享试用Token，有每日额度限制）

**Token 自动提取规则（强制）**：若用户对话中出现 60~70 位连续字母数字串（如"我的token是 Mj9mN2xP..."），自动提取并通过 `--token` 参数传给 submit 命令。日志和回复中只显示前 6 位+`***`，**绝不回显完整 Token**。提取到个人 Token 后提示用户：`已使用您的个人Token，不消耗共享试用额度`。

---

## 核心原则（强制）

- 回测请求走三轮交互协议（见下方工作流）。
- 编排器路径：`"${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py"`。
- 严禁读取或引用历史报告文件（`.html`/`.png`/`.json`），只使用 orchestrator 的 `status` 命令输出获取结果。
- 策略代码由 agent 在第 2 轮使用 LLM 生成，写入 `${QUANTCLAW_ROOT}/strategies/` 目录。
- 禁止在首条回复前做长轮询。
- 监控页是透明主通道，聊天页只给里程碑与结论。
- 失败时必须回复 `status` + `error` + `next_action`，禁止只说"失败了"不给下一步。
- 实盘能力保留，默认不进入实盘；用户请求模拟/实盘时执行 `qmt-check` 检测。
- 触发词分四类：
  - **回测第1轮**：`回测`、`策略`、`自动编排`、`均线`、`上穿`、`下穿`、`买入`、`卖出` → 进入三轮交互协议
  - **回测第2轮**：`开始生成`、`生成策略`、`好`、`开始`、`继续`、`1`（或任何第1轮确认后的用户消息）；若同条消息同时包含完整需求+第2轮触发词，直接视为已确认并进入第2轮
  - **参数优化**：`优化`、`调参`、`参数优化`、`网格搜索` → 执行 `optimize`（回测完成后触发）
  - **模拟/实盘**：`模拟`、`模拟盘`、`模拟交易`、`开始交易`、`实盘`、`实盘交易`、`QMT` → 执行 `qmt-check` + `trade`（独立流程，不走三轮协议）

---

## 第 0 步：环境预检（每次会话首次触发时执行一次）

运行 Skill 内置预检脚本（`scripts/preflight.py`，相对于本 Skill 目录）。脚本内部使用 `sys.executable` 自适应解释器，直接调用即可：

Linux/macOS：
```bash
python3 "<本Skill目录>/scripts/preflight.py"
```
Windows PowerShell：
```powershell
python "<本Skill目录>\scripts\preflight.py"
```

输出 JSON，按字段消费：
- `ready=true` → 取 `engine_root` 作为 `QUANTCLAW_ROOT`，进入第 1 轮
- `ready=false` + `engine_found=true` → 依赖缺失，向用户展示 `blockers` 和 `fix_cmd`
- `ready=false` + `engine_found=false` → 引擎未找到，返回 `status=config_missing` + 配置指南链接。**禁止降级为手动脚本。**
- `hints` 非空 → 非阻塞提示（如 Token 状态），向用户如实展示
- 预检通过后可选执行 `doctor_cmd` 做深度配置诊断（端口/Token/公网等）

退出码：`0`=就绪　`1`=引擎未找到　`2`=依赖缺失可修复

编排器脚本内置路径回退（`Path(__file__).parents[1]`），即使环境变量未设置，只要找到脚本就能正常运行。

---

## 三轮交互协议

### 第 1 轮：需求确认

**目标**：理解用户意图，确认关键参数，引导进入代码生成轮。

1. **解析需求**：提取标的、周期、信号（仓位/风控缺失时使用默认并说明）
2. **做数据能力检查**：
```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/data_capability_guard.py" \
  --requirement "{用户原始需求}"
```
3. **确认并引导**：回复至少包含：
   - 已理解的参数摘要（标的/周期/信号/方向）
   - 若 `data_capability_guard` 输出含 `token_hint`（非空字符串），**必须**在确认摘要之后、引导词之前如实告知用户。这表示检测到 Portfolio 策略 +（未传 Token 将回退共享试用 Token / 正在使用共享试用 Token）的组合，数据调用量大可能触发频率限制。直接呈现 `token_hint` 内容即可，不要包装为广告
   - 明确引导用户触发下一轮：

```
需求已确认：{标的} / {模式cta或portfolio} / {日线/分钟线} / {做多/做空} / {回测区间或"引擎默认最近1年"}
{若有token_hint则在此呈现，无则省略此行}
请回复「开始生成」，我来为你生成策略代码并提交回测。
```

**第 1 轮禁止**：不做代码生成、不调用 submit、不创建文件。
**第 1 轮最多命令**：`data_capability_guard.py`（1条）。

### 第 2 轮：代码生成 + 提交（极速流程）

**触发**：第 1 轮确认后，用户发送任意消息（`开始生成`/`好`/`1` 等）；若同条消息同时包含完整需求+第2轮触发词，也可直通第2轮。

**直通首响（强制）**：直通第2轮时先立即回复一句 `已收到，开始生成中...`，再执行代码生成与提交，避免长时间无反馈。

**第 2 轮速度约束（强制）**：
- **禁止**重跑 `data_capability_guard`（第 1 轮已检查）
- **禁止**单独跑 `py_compile`（submit 内部已含编译+静态检查+冒烟测试）
- 理想路径 **2 次工具调用**：① 写策略文件 ② submit
- submit **同步等待预检**（compile→lint→dryrun，通常 10~60 秒）再返回结果：
  - 预检通过 → 返回 `status: "accepted"` + `monitor_url`（回测已在后台运行）
  - 预检失败 → 返回 `status: "lint_error"/"compile_error"/"dryrun_error"` + `error` + `strategy_file`（**不返回 monitor_url**）
- 预检失败时 **在 Round 2 内立即修复**：
  1. **先告知用户**当前情况（如"检测到 import 路径错误，正在自动修复..."），保持透明
  2. 读 `error` + `strategy_file` → 修复代码 → 重新 submit
  3. 最多 **6 轮**修复重试，超过交由用户决策
- submit 返回 `accepted` 后若回测运行时/超时/数据失败 → 已有 `monitor_url`，在第 3 轮处理

1. **生成策略代码**（agent 使用 LLM 能力，直接写入文件）：
   - 根据 `parsed["mode"]` 选择正确模板：
     - `cta` → 继承 `CtaTemplate`，`on_bar(self, bar)`，`self.buy(price, vol)` / `self.sell(price, vol)`，`self.pos`，初始化用 `self.load_bar(N)`（**单数**，N=bar 数量）
     - `portfolio` → 继承 `StrategyTemplate`（vnpy_portfoliostrategy），`on_bars(self, bars: dict)`，`self.buy(vt_symbol, price, vol)` / `self.sell(vt_symbol, price, vol)`，`self.get_pos(vt_symbol)`，初始化用 `self.load_bars(days)`（**复数**，days=天数）
   - **严禁混用**：CTA 策略禁止用 `load_bars`，Portfolio 策略禁止用 `load_bar`
   - **仓位计算（强制——用户未指定时默认全仓）**：
     - 用户明确说了手数/股数/仓位比例 → 按用户要求
     - 用户未提仓位 → **默认全仓**（用 `self.available_cash` 动态计算最大可买手数）
     - **绝对禁止** `fixed_size = 100` 或任何硬编码固定股数作为默认仓位（这是 vnpy 教程示例值，不是真实交易逻辑）
     - CTA 全仓计算参考：
       ```python
       vol = int(self.available_cash / (bar.close_price * 1.0003)) // 100 * 100  # 主板100股整数倍
       if vol >= 100:
           self.buy(bar.close_price, vol)
       ```
     - Portfolio 等权全仓参考：
       ```python
       per_capital = self.available_cash / max(len(target_symbols), 1)
       vol = int(per_capital / (bar.close_price * 1.0003)) // 100 * 100
       if vol >= 100:
           self.buy(vt_symbol, bar.close_price, vol)
       ```
     - 引擎会自动管理资金扣减/回款，并在资金不足时自动调减到可买最大手数
   - **账户属性（引擎自动注入，策略直接用）**：
     - `self.available_cash` — 可用现金（买入扣减，卖出回款）
     - `self.total_value` — 账户总值（现金+持仓市值）
     - `self.closable_pos` — CTA可卖数量（T+1 自动扣减当日买入）
     - `self.closable_positions` — Portfolio per-symbol可卖量dict（`self.closable_positions.get(vt_symbol, 0)`）
     - `self.capital` — 等于 available_cash（兼容）
     - `self.trade_calendar` — 交易日历（set of "YYYYMMDD"），可用 `date_str in self.trade_calendar` 判断交易日
     - `self.last_order_status` — 最近一次下单结果（`{"ok":True/False,"reason":"...","symbol":"..."}`）
     - `self.order_reject_log` — 最近200条被拒订单记录（停牌/涨跌停/资金不足等）
   - **资金不足兜底**：引擎会自动调减买入量到可用现金能买的最大手数，无需策略手动检查
   - **停牌/涨跌停兜底**：引擎自动拦截停牌日下单和触及涨跌停价格的委托，返回空列表。**策略判断下单是否成功应优先检查 `buy()/sell()` 返回值**（空列表=被拒），而非假设一定成功
   - **交易所合规（强制）**：沪深主板/创业板 100 股整数倍，科创板(688xxx) 200 股起步+1 股递增（205 股合法）
   - **ArrayManager API**：均线用 `am.sma()`，禁止用 `am.ma()`（vnpy 不存在此方法）
   - **CTA 必须在 `on_bar` 开头调用 `am.update_bar(bar)`**：否则 ArrayManager 永远不会 `inited`，导致全程 0 交易。引擎有运行时兜底但不能依赖
   - 写入 `${QUANTCLAW_ROOT}/strategies/{module_name}.py`

**Portfolio 轮动策略速查**（减少生成思考时间）：
- 周轮动：`on_bars(self, bars)` 中 `list(bars.values())[0].datetime.weekday()==0` 判断周一调仓
- 排序选股：遍历 `self.vt_symbols` 计算因子 → `sorted()` → 取前N名
- 等权全仓：每只 `self.available_cash / N`，按交易所规则取整手
- 周线数据：`pro.weekly(ts_code=code, start_date=..., end_date=...)` 直取，无需从日线合成

2. **直接提交**（submit 内置编译+静态检查+预导入，无需单独 py_compile）：
```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" submit \
  --requirement "{用户原始需求}" \
  --strategy-file "${QUANTCLAW_ROOT}/strategies/{module_name}.py" \
  --strategy-module "{module_name}" \
  --strategy-class "{class_name}" \
  --symbols "{策略中所有vt_symbol逗号分隔}" \
  --monitor-public-base "${MONITOR_PUBLIC_BASE:-}" \
  --monitor-port-candidates "${ORCH_MONITOR_PORT_CANDIDATES:-8767}" \
  --timeout-sec 1200
```
   - submit 内部同步执行预检：py_compile → _lint_strategy → _preflight_import → dryrun
   - 预检通过后自动启动回测，返回 `status: "accepted"` + `monitor_url`
   - 预检失败返回 `status: "<error_type>"` + `error` + `strategy_file`，**不启动回测、不返回 monitor_url**
   - agent 判断 submit 输出：
     - `status == "accepted"` → 进入步骤 3（回复用户）
     - `status` 为 `compile_error`/`lint_error`/`dryrun_error` → **先输出一句话告知用户**（如"检测到 xxx 错误，正在修复第 N/6 次..."）→ 读 error + strategy_file → 修复代码 → 重新 submit（最多 6 轮）
     - 6 轮后仍失败 → 将最后一次错误信息告知用户，交由用户决策

3. **回复用户**（仅在 submit 返回 `accepted` 后）：
   - `run_id` + `monitor_url` + 当前状态
   - 引导词（必须覆盖两个语义点）：
     - A：打开监控页实时查看策略代码/曲线/交易
     - B：完成后发送「查看结果」获取摘要与报告链接

### 第 3 轮：查看结果 / 诊断修复

**触发词**：`查看结果`、`结果`、`status`、`重新生成`

1. **查询状态**：
```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" status --run-id "{run_id}"
```

2. **根据状态分流**：

| status | 处理 |
|--------|------|
| `running` | 告知当前进度，提示继续等待 |
| `completed` | 输出摘要 + 强制输出 `report_url`，不用 `monitor_url` 表述完整报告 |
| `failed` | 根据 `last_error.error_type` 分流处理（见下方错误分流表） |

3. **错误分流（agent 决策表）**：

| error_type | 含义 | agent 策略 |
|-----------|------|-----------:|
| `compile_error` | py_compile 失败 | 读 strategy_file + traceback → LLM 修复代码 → 重新提交 |
| `lint_error` | 静态检查 blocker（如 am.ma()、vnpy.trading 导入） | 同 compile_error 处理 |
| `dryrun_error` | 冒烟测试失败（50根K线采样回放运行时异常） | 同 compile_error 处理：读 strategy_file + traceback → LLM 修复 → 重新提交 |
| `runtime_error` | 回测运行时异常 | 读 strategy_file + traceback → LLM 分析修复 → 重新提交 |
| `compat_error` | 引擎兼容性（如 portfolio+WEEKLY 未降级） | 提示用户调整参数，通常不应出现（parse_requirement 已自动降级） |
| `data_error` | 数据加载失败/为空 | 提示用户检查标的代码/日期范围/token |
| `config_error` | 环境/配置问题 | 提示用户检查配置 |
| `timeout_error` | 超时 | 建议缩短日期范围或标的数量 |

- 只对 `compile_error`、`lint_error`、`dryrun_error` 和 `runtime_error` 尝试自动修复，其余直接报告用户。
- Round 2 预检失败（compile/lint/dryrun）自动修复最多 **6 轮**；Round 3 运行时修复最多 **3 轮**。超过交由用户决策。

3.5 **结果校验告警（status=completed 时优先检查）**：

`status` 输出中若包含 `result_warnings` 字段（非空列表），说明回测结果校验发现语义异常：
- 读 `result_warnings` + `strategy_file` → LLM 分析是否为策略 bug
  - 若判断为 bug → 修复策略代码 → 重新提交
  - 若判断为正常行为（如趋势策略在熊市期间无反向信号）→ 照常输出结果，附带告警说明

常见告警类型：零交易、单边信号（有买无卖/有卖无买）、胜率极端值（100%/0%）。

4. **完成后引导**（status=completed 时必须附带）：

```
回测已完成，{摘要}。您可以：
1. 回复「优化参数」对策略参数进行网格搜索
2. 回复「模拟交易」在 QMT 中启动自动交易（需 Windows + QMT 环境）
```

---

## 参数优化流程（回测完成后由用户触发）

**触发词**：`优化`、`调参`、`参数优化`、`网格搜索`

**前提**：已完成至少一次回测（数据已缓存在数据库中）。

1. **确认优化方案**：agent 分析当前策略的可调参数，向用户确认：
   - 优化目标（默认 `sharpe_ratio`，可选 `total_return`/`annual_return`/`max_ddpercent`）
   - 参数范围（`[起始, 终止, 步长]`）
   - 预估组合数

2. **执行优化**：
```bash
"${PYTHON_BIN}" "${QUANTCLAW_ROOT}/backtests/pipeline_orchestrator.py" optimize \
  --strategy-file "${QUANTCLAW_ROOT}/strategies/{module_name}.py" \
  --strategy-class "{class_name}" \
  --symbols "{vt_symbol}" \
  --start "{YYYYMMDD}" --end "{YYYYMMDD}" \
  --optimize-params '{"target":"sharpe_ratio","params":{"fast_window":[5,30,5],"slow_window":[10,60,10]}}'
```

支持 `"algorithm":"ga"` 使用遗传算法（大参数空间时推荐）。

3. **展示结果**：输出 JSON 含 `best`（最优参数+指标）和 `results`（Top N），agent 以表格形式呈现。

4. **后续选择**：用户可选择用最优参数重新回测验证，或继续调整参数范围。

---

## 绝对禁止清单（违反任何一条 = 严重事故）

### 链路禁止
- **禁止**在项目目录或工作目录下创建 `.html` 报告文件
- **禁止**读取、搜索、引用 `reports/` 目录下的历史文件
- **禁止**直接调用 `backtest_runner.py`、`monitor_server.py`、`/api/code`
- **禁止**使用 `python -m http.server` 或任何临时 HTTP 服务
- **禁止**生成临时回测脚本或手工拼接回测执行流程
- **禁止**在 submit 之前检查"策略是否已存在"
- **禁止**在编排器找不到时降级为手动脚本、akshare/yfinance 临时方案、或任何非编排器回测方式

### 输出禁止
- **禁止**寒暄/自我介绍/营销文案
- **禁止**承诺"完成后自动推送摘要"或"跨轮次自动再回复"
- **禁止**使用"模拟数据演示"口径替代真实回测
- **禁止**硬编码市场数据
- **禁止**繁琐状态输出 `[run_id][N/M][状态]`
- **禁止**发了"请确认"却自动继续
- **禁止**前台启动长驻进程

### 安全禁止
- **禁止**硬编码绝对路径（统一使用 `QUANTCLAW_ROOT`）
- **禁止**在 SKILL 或脚本中提交明文凭据
- **禁止**策略文件路径指向 `strategies/` 目录之外
