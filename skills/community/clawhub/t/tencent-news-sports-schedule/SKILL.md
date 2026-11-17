---
name: tencent-news-sports-schedule
display_name: 体育赛事查询助手
display_name_en: Tencent Sports Schedule
description: 当用户查询某项体育赛事或某支球队的赛程、下一场比赛、比赛时间、对阵、比分、直播链接或支持的赛事列表时使用。通过腾讯新闻 CLI 查询已接入的中超、英超、西甲、欧冠、NBA、苏超等赛事；实际覆盖范围以当次赛事列表为准。不用于体育新闻、积分榜、球员统计或比赛集锦。
description_zh: 查询体育赛事和球队的赛程、对阵、比分与直播链接，支持按日期和球队筛选。
description_en: Query sports schedules, fixtures, scores and live links by competition, team and date using Tencent News. Coverage follows the current competition list.
version: 1.0.5
shared_resources: ["tencent-news-cli", "tencent-sports"]
author: TencentNews
tags: [sports, schedule, fixtures, scores, tencent]
examples_zh: ["本周英超赛事有哪些比赛？", "nba今日比赛结果如何？", "北京国安最近有哪些比赛？"]
examples_en: ["What Premier League matches are on this week?", "How did today's NBA games finish?", "What are Beijing Guoan's recent and upcoming matches?"]
---

# 体育赛事查询助手

当用户需要体育赛程或比赛结果时，按以下步骤执行：

1. 检查环境；缺少 CLI 或 Key 时完成诊断，输出「环境失败结果」及恢复步骤。
2. 环境就绪后，读取 [`references/sport.md`](references/sport.md)，通过 `run-cli` 获取当前体育命令帮助和赛事列表。
3. 按用户的赛事、球队与时间范围查询；需要时翻页、筛选球队、合并多项赛事并去重。
4. 仅整理实际取得的比赛数据，明确查询范围和未完成部分；不能把失败或部分结果解释成“没有比赛”。

本 skill 可独立安装，不依赖 `tencent-news` skill。所有 CLI 调用均通过本包的 `run-cli`，由脚本注入当前 skill 名称和版本；`cli-state` 是环境检查入口。

## 对话用例

| 用户问题 | 执行方式与回答要求 |
|---|---|
| 本周英超赛事有哪些比赛？ | 从当次赛事列表解析英超 ID，按北京时间本周区间查询并翻页，按日期展示对阵和已返回的直播链接。 |
| nba今日比赛结果如何？ | 从当次赛事列表解析 NBA ID，查询北京时间当天区间并翻页，只展示已开赛且返回了比分的比赛，未开赛或没有比分时不补占位比分。 |
| 北京国安最近有哪些比赛？ | 查询当前支持且可能相关的赛事，在实际返回中按国安别名筛选、去重，合并后按时间升序展示。 |

这些是调用示例，不是预置赛程。日期、对阵、比分和直播链接均以当次 CLI 返回为准；不得使用样例或模型记忆补齐比赛。

## 平台与脚本入口

先进入安装后的 skill 根目录（包含 `SKILL.md`），或将脚本路径解析为该目录下的绝对路径，不假定用户当前工作目录就是 skill 目录。

| 平台 | 状态检查 | 业务调用 |
|---|---|---|
| macOS / Linux | `sh scripts/cli-state.sh status` | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/cli-state.ps1 status` | `powershell scripts/run-cli.ps1 <command> [args]` |

后续示例使用 macOS / Linux；Windows 用 `powershell` 与对应 `.ps1` 文件。

- `run-cli` 无参数、`-h`、`--help` 显示本地用法并退出 0，无需 CLI 或 Key。
- `run-cli help` 优先返回当前 CLI 帮助；未安装时返回本地用法。不要把本地用法当作体育命令帮助。
- `cli-state` 无参数或 `status` 返回 JSON；`help`、`-h`、`--help` 显示帮助。
- 状态检查退出 0 只代表诊断已执行；必须读取 `success`、`status` 和 `error.code`。`ready` 只证明本地检测到 CLI 与 Key，不证明远端鉴权成功。
- 业务调用保留真实退出码，未知参数和缺少 CLI 的业务调用仍失败。

## Phase 1：环境就绪与失败处理

**执行业务前必须读取并遵守 [CLI 环境与失败处理](references/cli-environment.md)**，完成状态检查、安装/更新、shell 配置核实与脱敏恢复。它是环境处理的统一入口；不要重新实现 Key 检测或读取明文 Key。环境失败优先于下文业务输出格式及通用错误话术；本轮无法恢复时返回其中的结构化「环境失败结果」，不得用其他数据源补结果。

本 Skill 的失败结果 `capability` 填 `sport`；`query` 使用脱敏后的实际问题。环境就绪后按开头的赛程流程继续查询。

其他业务失败按赛程说明中的失败规则处理；没有成功数据时不附来源标识。

## References

以下安装、更新和 Key 指南中的直接 CLI 命令供用户在本地手动操作；智能体仍以本文件为准，通过 `run-cli` 执行业务与更新，通过 `cli-state` 检查 Key，不执行手动指南中的明文 Key 验证或循环重装。

- 查询、球队筛选、分页、时间与比分规则：[`references/sport.md`](references/sport.md)
- 手动安装：[`references/installation-guide.md`](references/installation-guide.md)
- 手动更新：[`references/update-guide.md`](references/update-guide.md)
- 本地 Key 配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
- 打包与评测环境：[`references/packaging.md`](references/packaging.md)
