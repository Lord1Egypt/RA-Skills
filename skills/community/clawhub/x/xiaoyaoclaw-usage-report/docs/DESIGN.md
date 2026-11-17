# DESIGN.md — xiaoyaoclaw-usage-report 设计文档

> 项目：OpenClaw Usage Report（用量报告）
> 日期：2026-08-31 | 状态：已确认（指挥官拍板）
> 来源：调研 `tasks/openclaw-observability-research/`（FINAL_调研报告 + 事实卡片 + 校验记录）

## 1. 定位

OpenClaw 用量与性能查询工具：读取本地 session JSONL（`state/agents/*/sessions/*.jsonl`），
回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」——**零依赖、
纯本地、数据不出机器**。

背景：OpenClaw 没有内置 per-task 性能面板，但 session JSONL 已完整记录每次任务/工具/模型
调用的时间戳与 token 消耗（调研结论 C1/C2）。本工具直接消费这份数据，无需任何额外采集。

## 2. 命名

| 维度 | 值 |
|------|-----|
| 项目 slug | `xiaoyaoclaw-usage-report` |
| README 英文标题 | OpenClaw Usage Report |
| 中文名 | 用量报告 |
| GitHub | dtsola/xiaoyaoclaw-usage-report（public, main, MIT） |
| ClawHub | slug `xiaoyaoclaw-usage-report` @dtsola |

## 3. 核心决策（指挥官拍板）

1. **不做成本估算**：脚本**不读取、不计算、不输出任何 cost 字段**（文档 / 报告 / JSON 口径完全一致）；
   各模型供应商定价不同，token 是通用主指标；需要成本请按 token × 单价自行换算。
2. **cron 每日日报为可选项**：工具支持 `--today --json`，挂定时任务由用户自行决定；
   README 与 SKILL 中均有说明。
3. **只做第一层（数据底座）+ 第二层（轻量查询）**：砍掉可视化看板（claw-lens）与
   全链路 Trace（Opik）——第一二层已覆盖核心需求。

## 4. 数据模型与统计口径

数据源：session JSONL version 3，事件类型 session / message / model_change /
thinking_level_change / custom（model-snapshot、openclaw:prompt-error）。

| 指标 | 口径 | 备注 |
|------|------|------|
| token 真实消耗 | input + output | ⚠️ totalTokens 含 cacheRead 每轮重复计数（实测虚高 1.3x~14x+，单条最高 568x） |
| 工具耗时 | toolResult.ts − assistant(toolCall).ts | 含模型生成 toolCall 的决策时间 |
| 模型耗时 | assistant 事件 ts − 前一条事件 ts（cap 10min） | 近似值；⚠️ 不能用 message.timestamp（批量写入时间戳）；精确 duration 在 diagnostics-otel 事件层 |
| 任务窗口耗时 | session 首条用户消息 → 末条消息 | 含用户思考间隔 |
| 任务活跃耗时 | 相邻事件间隔 <5min 累计 | 近似值，可能含 heartbeat |
| skills 使用 | read 工具 arguments.file_path 含 /skills/<name>/SKILL.md | 仅统计被 read 加载过的技能 |
| 时间窗 | 窗口 = **硬边界**：所有指标只聚合窗口内事件（默认窗口 = 今天） | ⚠️ 窗口外历史数据不参与任何聚合；全历史须显式 `--all` |
| MCP 工具 | 与普通工具同构（toolCall/toolResult） | 天然覆盖 |

## 5. 输出维度

1. 总览：任务数、总 token(input+output)、总耗时
2. 按 agent/模型：调用次数、输入/输出 token、模型总耗时/平均（近似）
3. 按工具：次数、失败数、总耗时、平均、最慢
4. Skills 使用：技能名、读取次数、使用 agent
5. 任务排行：按活跃耗时（排除用户思考间隔）
6. 每日趋势：每日输入/输出 token、调用数

CLI：`--today / --week / --all / --agent <name> / --by-tool / --skills / --by-session / --daily / --json / --include-sessions / --include-paths / --state <path>`。
时间窗：**窗口即硬边界**——不传 `--today/--week/--all` 时默认「今天」（不扫全历史）；选定窗口后所有维度只统计窗口内事件，跨窗口长会话按窗口内部分截断；三者互斥。
数据目录解析顺序：`--state` 参数 → `OPENCLAW_STATE` 环境变量（唯一读取的环境变量）→ 桌面版（小遥Claw）默认路径；报告首部打印实际使用的目录，**默认脱敏为末两级**（`--include-paths` 才显示完整路径）。
输出最小化：默认只输出聚合统计（不含会话内容原文、不含 session id、不含本机绝对路径）；`--include-sessions` 才输出 session 级明细（字段：agent/id/start/end/duration_ms/active_ms/model_ms/models/tokens/tools/msgs），`--include-paths` 才输出完整本机路径。

## 6. 仓库结构

```
xiaoyaoclaw-usage-report/
├── scripts/usage-report.py   # 主工具（零依赖纯标准库）
├── README.md                 # 项目说明（含 cron 日报可选项）
├── README.en.md              # 英文版
├── SKILL.md                  # 技能形态（含 cron 日报可选项）
├── docs/DESIGN.md            # 本文档
├── PROGRESS.md               # 进度卡（.gitignore 排除，不随仓库发布）
├── manifest.json             # ClawHub 元数据
├── LICENSE                   # MIT
└── assets/readme/            # hero.svg / community-qr.png（发布资产）
```

## 7. 语言策略

本技能**不对任何语言或地区设限**：报告与文档默认中文，用户用英文或其它语言提问则跟随；
文档与示例中的中文属**示例与品牌双语素材**（`README.md` 中文主体 / `README.en.md` 英文版 / 头图中英双语），
不构成使用限制；头图（`assets/readme/hero.svg`）内已用可见文案与 `<desc>` **显式声明**该双语标注为「有意为之且可选」的品牌素材、
本体英文优先，工具本体与语言/地区无关；脚本内文案可按需替换为任意语言。

## 8. 已知限制

- 任务活跃耗时为近似值（可能含 heartbeat/后台事件）
- 仅支持 JSONL version 3 会话
- 仅统计本机数据（多机需各自运行）
- 模型耗时为近似估算，精确值需接 diagnostics-otel
