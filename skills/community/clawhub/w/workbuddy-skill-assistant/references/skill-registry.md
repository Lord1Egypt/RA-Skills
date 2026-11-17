# 积木注册表（skill registry）

> **名册 vs 目录**：`skill-catalog/` 是**外部候选发现**（还没装、值得考虑的）；本文件是**自己人名册**（已装或自建、可直接调用的积木）。
> 选择 skill 方案时的顺序：**先查名册，再查目录**。名册里的积木都经过真实任务验证或明确登记，可信度高于目录候选。

## 注册动作

1. 教授说「把 X 注册进来」；
2. 读取 X 的 SKILL.md frontmatter，按下方字段生成条目草稿；
3. 按 [基础分类标准](skill-taxonomy.md) 判定**主分类**（七类或扩展类之一）；
4. 教授确认后写入本文件，并在 `state.md` 记一条采纳。

**规则**：

- 上限 **30 块**。超员时先淘汰「上次验证」最旧且低频者（淘汰 = 状态改 `retired`，不删除条目）；
- 每次真实任务用到某块积木，顺手更新该条目的「上次验证」；
- 状态只有三种：`active`（可调用）/ `retired`（停用，仅留档）/ `draft`（刚登记、未经真实任务验证）；
- 注册、停用、移除均需教授确认。

## 名册（首批 9 块）

| 积木 | 分类 | 来源 | 场景（何时想起它） | 输入 → 输出 | 调用方式 | 状态 | 上次验证 |
|------|------|------|--------------------|-------------|----------|------|----------|
| skill-designer | meta | 自建 @user_4894573e | 要设计新 skill 或改造设计蓝图 | 任务需求 + 边界 → 设计蓝图（积木链 B01-B10 + references 选型） | 话术「积木设计师」或 `Skill: skill-designer` | active | 2026-09 |
| skill-rebuild | meta | 已装 | 已装 skill 需要把脉改造（性能/功能/适配） | skill 名 + 改造意图 → 改造清单 | `Skill: skill-rebuild` | active | 2026-09 |
| skill-md-refactor | meta | 已装 | SKILL.md 臃肿、结构混乱，要重构为精简路由器 | 超长 SKILL.md → 精简 + 积木式有序版本 | `Skill: skill-md-refactor` | active | 2026-09 |
| skill-check-pro | meta | 已装 | skill 生态体检、修复、升级、仪表板 | 体检范围 → 分级问题清单 + 修复方案 | `Skill: Workbuddy_skill_check` | active | 2026-09 |
| skill-publish-audit | meta | 已装 | skill 发布前的就绪度审查（合规/格式/文档） | skill 目录 → 10 维审查报告 | `Skill: skill-publish-audit` | active | 2026-09 |
| Work_skill_router | meta | 已装 | 任务→skill 的实时路由参考（三层分类 + 组合模式） | 任务描述 → 推荐 skill 序列 | `Skill: Work_skill_router` | active | 2026-09 |
| Work_skill_workflow | meta | 已装 | 投资场景工作流卡片库（晨报→复盘等）的运行时参考 | 场景 → 推荐 skill 序列与预期产出 | `Skill: Work_skill_workflow` | active | 2026-09 |
| Work_skill_manager | meta | 已装 | skill 系统总枢纽、管理面板运营 | — | `Skill: Work_skill_manager` | active | 2026-08 |
| stock-volume-12step-analysis | finance | 自建 | 个股量能 12 步深度分析（12 步 SOP + 5 维量能评分） | 股票代码 → 量能 HTML 报告（5 图可视化） | `Skill: stock-volume-12step-analysis` | active | 2026-09 |

## 与其他模块的分工

| 模块 | 职责 | 边界 |
|------|------|------|
| 本注册表 | 「自己人」的事实名册：场景、接口、状态 | 只登记，不评分、不排等级 |
| skill-catalog/ | 外部候选发现，找装什么 | 目录条目验证后才进名册 |
| references/workflows/ | 积木组合的接力定义（工作流卡片） | 卡片里的每块积木应已在本名册注册 |
| Work_skill_router | 实时任务路由 | 名册是路由的事实源之一 |
| Work_skill_manager | 面板运营 | 名册变更经教授确认后此处登记即可 |
