---
name: tonghuashun
description: 操作同花顺炒股软件，覆盖盯盘、选股、自选、下单前检查、复盘等个人炒股全流程
metadata:
  {"openclaw":{"emoji":"📈","homepage":"https://www.10jqka.com.cn","os":["darwin","win32"]}}
---

# 同花顺个人炒股全流程 Skill

当用户需要操作同花顺（THS）进行个人炒股时，优先使用 `exec` 工具自动化完成“开盘准备 -> 盯盘 -> 选股 -> 自选管理 -> 交易执行 -> 收盘复盘”的完整流程。

本 Skill 目标是覆盖绝大多数个人交易者常见操作，但资金安全相关动作（最终买入/卖出确认）必须由用户手工确认。

## 1. 平台与应用识别

- **macOS**：应用名通常为 `同花顺` 或 `同花顺炒股`
- **Windows**：通常使用桌面快捷方式或安装目录启动
- 若用户未明确应用名，默认 `同花顺`

## 2. 核心能力范围（覆盖个人炒股全流程）

1. **开盘准备**：启动软件、切换到大盘、自选页、刷新行情
2. **大盘监控**：上证/深证/涨跌家数/涨停跌停观察
3. **涨停体系**：涨停板、连板、涨幅榜、强势股跟踪
4. **板块轮动**：行业、概念、板块涨幅与资金流
5. **个股分析**：分时、K 线、成交明细、F10 资讯、盘口观察
6. **自选管理**：加入/删除自选、自选分组轮巡
7. **交易执行**：打开委托页面、按用户指令定位标的和方向
8. **风控流程**：仓位、止损、盈亏比检查与提醒
9. **收盘复盘**：导出观察清单、记录交易日志、次日计划

## 3. 高频快捷键（同花顺）

| 快捷键 | 功能 |
|---|---|
| F3 | 上证大盘 |
| F4 | 深证大盘 |
| F5 | 分时 / K 线切换 |
| F6 | 自选股 |
| F10 | 个股资讯（基本面/公告等） |
| F12 | 委托下单 |
| F1 | 成交明细 |
| F2 | 价量分布 |
| F7 | 个股全景 |
| Insert | 加入自选股 |
| Delete | 删除自选股 |
| Esc | 返回上一画面 |
| Ctrl+Z | 涨停板排行（常用） |
| 60 + Enter | 涨幅榜（快速看强势股） |
| 80 + Enter | 综合排行 |

## 4. 操作总原则

1. **先激活窗口再操作**：每次按键前先 `activate` 同花顺并 `delay 0.2-0.5s`
2. **分步执行**：优先“一步一结果”，避免连续长串指令导致 UI 漏触发
3. **关键动作二次确认**：涉及 F12、买卖方向、数量时必须复述并确认
4. **错误可恢复**：失败时先 `Esc` 回到上一级，再重试
5. **不盲下单**：本 Skill 可协助进入下单流程，但最终下单由用户手动确认

## 5. 标准流程模板

### A. 开盘前 5 分钟

1. 启动同花顺
2. 切大盘（F3/F4）
3. 看涨停板（Ctrl+Z）
4. 看涨幅榜（60）
5. 打开自选（F6）

### B. 盘中盯盘循环（每 10-15 分钟）

1. 刷新（F5）
2. 看涨停/连板
3. 看板块涨幅与资金流
4. 回到自选逐个检查分时与量能
5. 命中条件时提醒“观察/减仓/止盈/止损”

### C. 交易执行流程（半自动）

1. 用户说“准备买入/卖出 XXX”
2. Skill 先打开 F12
3. 复述关键信息：代码、方向、价格、数量、仓位占比
4. 用户确认后，仅执行“定位输入”与“界面操作辅助”
5. 最终提交由用户点击确认

### D. 收盘复盘

1. 汇总今日涨停、强势板块、自选异动
2. 记录交易日志（买卖点、理由、结果）
3. 生成次日观察清单

## 6. 交易风控规则（强制提醒）

当用户发起交易动作时，先做以下检查并提醒：

1. 单笔风险 <= 账户权益的 1%-2%
2. 单票仓位不超过用户预设上限
3. 明确止损位与止盈位
4. 盈亏比不低于用户设定阈值（如 1:1.5 或 1:2）
5. 若用户未给出这些参数，先询问再继续

## 7. 常见用户意图映射

| 用户意图 | 推荐动作 |
|---|---|
| 打开同花顺 | 启动 + 激活窗口 |
| 看大盘强弱 | F3/F4 + 60 + 80 |
| 看今天涨停 | Ctrl+Z（涨停板） |
| 看我自选 | F6 |
| 看某只股票基本面 | 搜索代码 + F10 |
| 看分时和成交 | F5 + F1 |
| 准备下单 | F12 + 风控确认流程 |
| 收盘复盘 | 汇总涨停/板块/交易记录 |

## 8. 平台命令模板

### 8.1 macOS（推荐模板）

启动应用：
```bash
open -a "同花顺"
```

激活应用：
```bash
osascript -e 'tell application "同花顺" to activate'
```

发送 F5（刷新）：
```bash
osascript -e 'tell application "同花顺" to activate' -e 'delay 0.3' -e 'tell application "System Events" to key code 96'
```

发送 F6（自选）：
```bash
osascript -e 'tell application "同花顺" to activate' -e 'delay 0.3' -e 'tell application "System Events" to key code 97'
```

发送 Ctrl+Z（涨停板）：
```bash
osascript -e 'tell application "同花顺" to activate' -e 'delay 0.3' -e 'tell application "System Events" to keystroke "z" using control down'
```

输入 `60` 回车（涨幅榜）：
```bash
osascript -e 'tell application "同花顺" to activate' -e 'delay 0.3' -e 'tell application "System Events" to keystroke "60"' -e 'tell application "System Events" to key code 36'
```

### 8.2 Windows 示例

启动应用（按实际路径调整）：
```powershell
Start-Process "同花顺"
```

或：
```powershell
Start-Process "C:\Program Files\同花顺\同花顺.exe"
```

> Windows 下按键自动化通过 `ths-hotkeys.mjs`（Node 调用系统 COM SendKeys）实现；若 COM 被禁用，可退化为手工快捷键。

## 9. macOS key code 速查

| 功能键 | key code |
|---|---|
| F1 | 122 |
| F2 | 120 |
| F3 | 99 |
| F4 | 118 |
| F5 | 96 |
| F6 | 97 |
| F7 | 98 |
| F10 | 109 |
| F12 | 111 |
| Delete | 51 |
| Return | 36 |

## 10. 执行策略（给 Agent）

1. 当用户给出目标（如“看涨停”、“看自选”、“准备买入”），先输出一句执行计划
2. 再调用一次 `exec` 执行最小动作
3. 读取执行结果并反馈成功/失败
4. 需要继续时再执行下一步
5. 涉及下单时，必须进入“确认-执行-再确认”模式

## 11. 工具调用格式

统一使用 `exec`，参数为 `command`。

```xml
<tool_call id="ths_001" name="exec">{"command":"open -a \"同花顺\""}</tool_call>
```

```xml
<tool_call id="ths_002" name="exec">{"command":"osascript -e 'tell application \"同花顺\" to activate' -e 'delay 0.3' -e 'tell application \"System Events\" to key code 97'"}</tool_call>
```

## 12. 安全边界

- 允许：行情查看、切页、自选管理、交易前准备、复盘记录
- 谨慎：交易界面录入（需用户确认关键参数）
- 禁止：未经用户确认的自动提交下单、自动转账、自动修改账户安全设置

## 13. 模板化交易指令（可直接理解并执行）

当用户使用以下“模板口令”时，按预定义流程执行。若用户未明确风格，默认执行“短线日内模板”。

### 13.1 短线日内模板

触发词示例：
- `执行短线开盘检查`
- `开始短线盯盘`
- `做一轮短线复盘`

流程：
1. 开盘检查：F3 -> F4 -> Ctrl+Z -> 60 -> F6
2. 盘中巡检：F5 -> 涨停/连板 -> 板块轮动 -> 自选逐票检查
3. 交易前确认：方向/仓位/止损/止盈/盈亏比
4. 收盘复盘：强势股、失败交易、次日观察池

### 13.2 波段模板

触发词示例：
- `执行波段检查`
- `做波段候选筛选`

流程：
1. 先看指数趋势（F3/F4）
2. 查看板块强弱与持续性（80、行业概念页面）
3. 个股检查：F5（日线/周线） + F10（基本面/公告）
4. 输出候选池：强趋势、回撤到位、风险收益比达标

### 13.3 仅复盘模板

触发词示例：
- `只做收盘复盘`
- `生成明日计划`

流程：
1. 统计涨停/跌停与市场情绪
2. 复盘自选表现与成交量变化
3. 记录交易错误（追高、止损不执行、仓位过重）
4. 输出次日计划（关注标的、触发条件、风控线）

## 14. Windows 自动按键落地（Node.js）

调用 `{baseDir}/scripts/ths-hotkeys.mjs` 即可执行同花顺 GUI 自动化。

### 14.1 单步动作

- `activate` 激活同花顺窗口
- `refresh` 发送 F5
- `watchlist` 发送 F6
- `limitup` 发送 Ctrl+Z（涨停板）
- `gainrank` 输入 60 + Enter
- `market_sh` 发送 F3
- `market_sz` 发送 F4
- `entrust` 发送 F12

### 14.2 组合动作（新增）

- `morning_check`：F3 -> F4 -> Ctrl+Z -> 60 -> F6
- `intraday_scan`：F5 -> Ctrl+Z -> 60 -> F6
- `after_close_review`：Ctrl+Z -> 60 -> F6
- `prep_buy`：F6 -> F12（买入前准备）
- `prep_sell`：F6 -> F12（卖出前准备）

### 14.3 参数化动作（带股票代码）

- `focus <code>`：定位到指定股票（6 位代码）
- `quote <code>`：定位并查看该股票报价/分时
- `kline <code>`：定位并切到 K 线（F5）
- `detail <code>`：定位并打开成交明细（F1）
- `fundamentals <code>`：定位并打开 F10 资料
- `prep_buy <code>`：自选 -> 定位股票 -> F12（买入前准备）
- `prep_sell <code>`：自选 -> 定位股票 -> F12（卖出前准备）

### 14.4 一键计划动作（新增）

- `plan_short`：短线计划（指数 + 涨停 + 涨幅 + 自选 + 刷新复查）
- `plan_swing`：波段计划（指数 + 综合排行 + 自选 + K 线）
- `plan_scalp`：超短计划（涨停与涨幅高频扫描）

### 14.5 批量巡检动作（新增）

- `batch_quote <csv>`：批量查看报价/分时
- `batch_kline <csv>`：批量切 K 线
- `batch_f10 <csv>`：批量查看 F10（看完自动返回）
- `batch_quote_file [path]`：从文件读取代码并批量查看报价
- `batch_kline_file [path]`：从文件读取代码并批量切 K 线
- `batch_f10_file [path]`：从文件读取代码并批量查看 F10

其中 `<csv>` 是逗号分隔的 6 位股票代码，如：
- `600519,300750,002594`

其中 `[path]` 是股票清单文件路径，省略时默认：
- `{baseDir}/scripts/watchlist.txt`

调用示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action limitup
```

组合动作示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action morning_check
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action prep_buy
```

参数化动作示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action focus --arg 600519
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action fundamentals --arg 300750
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action prep_buy --arg 002594
```

一键计划示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action plan_short
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action plan_swing
```

批量巡检示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action batch_kline --arg "600519,300750,002594"
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action batch_f10 --arg "000001,600036,601318"
```

文件批量巡检示例：
```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action batch_kline_file
```

```powershell
node "{baseDir}/scripts/ths-hotkeys.mjs" --action batch_f10_file --arg "D:\quant\watchlist.txt"
```

若 Windows 下 COM 被安全策略禁用，退化为手工快捷键。

### 14.6 模板口令与动作映射

| 模板口令 | 推荐脚本动作 |
|---|---|
| 执行短线开盘检查 | `morning_check` |
| 开始盘中巡检 | `intraday_scan` |
| 做收盘复盘 | `after_close_review` |
| 执行短线全流程计划 | `plan_short` |
| 执行波段计划 | `plan_swing` |
| 执行超短计划 | `plan_scalp` |
| 准备买入某股票 | `prep_buy <code>` |
| 准备卖出某股票 | `prep_sell <code>` |
| 打开某股票看 K 线 | `kline <code>` |
| 打开某股票看 F10 | `fundamentals <code>` |
| 批量看自选 K 线 | `batch_kline <csv>` |
| 批量看自选 F10 | `batch_f10 <csv>` |
| 从文件批量看 K 线 | `batch_kline_file [path]` |
| 从文件批量看 F10 | `batch_f10_file [path]` |

### 14.7 执行日志（新增）

`ths-hotkeys.mjs` 每次执行都会自动写日志到：
- `{baseDir}/scripts/logs/trading-YYYY-MM-DD.log`

日志格式：
- `时间 | 状态 | action=动作名 | arg=参数 | 详情`

示例：
```text
2026-03-17 10:12:03 | OK | action=plan_short | arg=- | 执行成功
2026-03-17 10:20:11 | ERROR | action=focus | arg=abc | 缺少或非法股票代码
```

## 15. 风控仓位计算脚本（新增）

新增脚本：`{baseDir}/scripts/risk-calc.mjs`

用途：
- 计算单笔最大可承受风险
- 计算建议股数（按 board lot，默认 100 股）
- 计算仓位占比、实际风险、盈亏比（可选 target）

调用示例（long）：
```bash
node "{baseDir}/scripts/risk-calc.mjs" --capital 200000 --riskPct 1 --entry 25.8 --stop 24.9 --target 28 --side long
```

调用示例（short）：
```bash
node "{baseDir}/scripts/risk-calc.mjs" --capital 200000 --riskPct 1 --entry 25.8 --stop 26.6 --target 24.2 --side short
```

输出为 JSON，可直接让 Agent 读取后总结为：
1. 建议股数
2. 预计风险金额
3. 预计仓位占比
4. 盈亏比是否达标

## 16. 标准应答模板（给 Agent）

当用户下达操作指令时，按如下结构回复并执行：

1. `收到目标`：一句话复述用户要做什么
2. `执行步骤`：说明本次只执行第 1 步（最小动作）
3. `工具调用`：执行一次 `exec`
4. `结果反馈`：成功/失败 + 下一步建议
5. `交易确认`：若涉及下单，要求用户明确确认后再继续

示例（用户：帮我看涨停）：
- 先回复：`我先打开同花顺并进入涨停板列表。`
- 再执行：激活 -> Ctrl+Z
- 最后回复：`已进入涨停板页面，是否继续按连板数筛选？`

## 17. 一体化编排入口（新增）

新增脚本：`{baseDir}/scripts/run-all.mjs`

作用：
- 按策略模板一键执行多个动作（短线/波段/超短）
- 可联动批量巡检（csv 或 watchlist 文件）
- 可联动风控参数计算（仓位、风险、RR）
- 自动输出 JSON 结果并写入运行日志

示例：
```bash
node "{baseDir}/scripts/run-all.mjs" --mode short --batch kline
```

```bash
node "{baseDir}/scripts/run-all.mjs" --mode swing --watchlist "{baseDir}/scripts/watchlist.txt" --batch f10
```

```bash
node "{baseDir}/scripts/run-all.mjs" --mode short --symbols 600519,300750 --batch quote --capital 200000 --riskPct 1 --entry 25.8 --stop 24.9 --target 28
```

说明：
- `run-all.mjs` 仅在 **Windows + Node** 场景下执行 GUI 动作
- 运行日志落盘：`{baseDir}/scripts/logs/run-all-*.json`

## 18. 自定义计划文件（新增）

新增示例：`{baseDir}/scripts/trading-plan.sample.json`

可自定义动作序列，然后执行：
```bash
node "{baseDir}/scripts/run-all.mjs" --plan-file "{baseDir}/scripts/trading-plan.sample.json"
```

计划文件规则：
- `actions` 为动作数组，动作必须是 `ths-hotkeys.mjs` 支持的名称
- 支持 `action:arg` 形式，例如：
  - `batch_kline_file:scripts/watchlist.txt`
  - `focus:600519`

## 19. 交易日志工具（新增）

新增脚本：`{baseDir}/scripts/trade-journal.mjs`

新增记录：
```bash
node "{baseDir}/scripts/trade-journal.mjs" add --symbol 600519 --side buy --entry 1688 --stop 1650 --target 1760 --shares 100 --strategy short --note "回踩均线"
```

查看最近记录：
```bash
node "{baseDir}/scripts/trade-journal.mjs" list --limit 20
```

日志文件：
- `{baseDir}/scripts/logs/trade-journal.jsonl`

## 20. 交付清单（当前版本）

- `scripts/ths-hotkeys.mjs`：单步、组合、参数化、计划、批量、日志落盘
- `scripts/watchlist.txt`：默认批量巡检清单
- `scripts/risk-calc.mjs`：风控仓位计算
- `scripts/run-all.mjs`：一体化流程编排
- `scripts/trading-plan.sample.json`：可编辑的策略计划模板
- `scripts/trade-journal.mjs`：交易日志增查工具
