# Changelog

## v4.0.0 (2026-07-27) — 简化版 fork

**重大架构变更：** 移除所有多 agent / 多视角 / 多空辩论流水线代码，**只保留默认主 agent 简单模式**。

### 变更摘要

- ❌ 删除：5-subagent 多视角流水线（阶段 1-5，sessions_spawn 模板，subagent 角色定义）
- ❌ 删除：`mode: fast / mode: full / analysts: split / skip debate / budget` 等 override flags
- ❌ 删除：原 references/technical-indicators.md 中"选 8 项"的多 agent 专属选取原则
- ✅ 保留：默认主 agent 简单模式（数据采集 + 资讯 + 综合建议）
- ✅ 保留：🛡️ 「监管 / 处罚 / 政策」hard rule（v3.1 加入，v4 强化为必跑步骤）
- ✅ 保留：评级体系 + 操作建议规范
- ✅ 保留：三市场差异化（货币单位 / 交易时间）
- ✅ 新增：本 changelog.md

### 为什么只保留默认模式

来源笔记（2026-07-27）：

1. **Rate limit 教训（2026-07-24 腾讯翻车）**：6 subagent 并行在 MiniMax-M3 token plan 限额（2062）前全军覆没
2. **token 边际收益低**：v2 实测 5-subagent 流水线相对单 agent token 仅降 18%（vs 预估 47-60%）
3. **响应可预测性**：单 agent 出报告 < 1 分钟，token 占用稳定；多 agent 易截断
4. **日常复盘够用**：主 agent + westock-data + minimax__web_search 已覆盖 80% 决策需求

### 与上游 `stock-research-team` (charonling, 1.0.0) 的关系

- 本 skill 是上游的 **fork**，通过 clawhub `--fork-of` 元数据标记
- 上游版本：2026-05-11 更新，主打 4 分析师 + 2 研究员 + 1 CIO 七视角多 agent
- 本版本：移除多视角，仅保留主 agent 快速分析
- 适用人群：希望快速决策、不需要多 agent 抗辩的个人投资者

### 升级路径（适用从 v3.x 升级的用户）

1. 删除本地旧版本：`rm -rf skills/stock-research-team`
2. 安装 v4：`clawhub install tanteng-stock-research`
3. 触发关键字不变（"分析 X 股票"），但失去 `mode: full` 的多 agent 升级能力
4. 如确需多 agent 深度复盘，回到上游 `stock-research-team` 原版

### 资料来源

- 上游：https://clawhub.ai/skills/stock-research-team
- 本 fork 由 `tanteng` 在 2026-07-27 重构发布
- 数据源：`westock-data` skill（腾讯自选股接口）
- 资讯源：`minimax__web_search`（MiniMax MCP）
