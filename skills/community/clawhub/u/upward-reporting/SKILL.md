---
name: upward-reporting
description: 职场汇报文档写作的总入口与路由。当用户说"写汇报"、"写文档"、"帮我写材料"但未明确场景时触发，帮助识别场景并路由到对应子skill。也提供所有汇报场景通用的风格规范和汇报对象适配指南。子skill：report-planning（规划汇报）、report-postmortem（故障复盘）、report-review（年终述职）、report-kickoff（横向协作KO）、report-okr（OKR制定/进展汇报/复盘）。
metadata:
  author: archon
  version: "3.0"
---

# upward-reporting — 汇报写作总入口

本 skill 是所有职场汇报写作场景的**路由入口**，同时承载所有子场景共用的风格规范和范式选择指引。

## 场景路由

当用户描述写作需求时，先判断场景，再加载对应子 skill（子 skill 文件位于本目录下）：

| 用户说了什么 | 路由到 | 子 skill 路径 |
|------------|-------|-------------|
| 写规划、写方向、技术规划、团队规划、年度规划、部门汇报 | `report-planning` | [report-planning/SKILL.md](report-planning/SKILL.md) |
| 故障复盘、事故总结、障碍分析、写改革计划、P0/P1复盘 | `report-postmortem` | [report-postmortem/SKILL.md](report-postmortem/SKILL.md) |
| 年终述职、写述职、个人总结、晋升材料、绩效总结 | `report-review` | [report-review/SKILL.md](report-review/SKILL.md) |
| 晋升谈话、晋升面谈、1v1述职准备、向老板介绍自己、年终1on1 | `report-review` + 口头策略 | [report-review/SKILL.md](report-review/SKILL.md) + [口头汇报策略](references/oral-presentation-guide.md) |
| 横向协作、KO文档、拉通、项目启动会、跨团队对齐 | `report-kickoff` | [report-kickoff/SKILL.md](report-kickoff/SKILL.md) |
| 写OKR、制定OKR、OKR进展、双周进展汇报、月度OKR、OKR复盘、KR拆解、写季度OKR | `report-okr` | [report-okr/SKILL.md](report-okr/SKILL.md) |

## 路由冲突解决

当多个子场景的触发词重叠时，按以下优先级判断：

1. **故障/事故关键词**：提到"P0/P1/故障/事故/线上异常" → `report-postmortem`（优先级最高，故障复盘有紧迫性）
2. **OKR专用 vs 通用**：提到"OKR/KR/O"且语境为制定/进展/复盘 → `report-okr`（即使语境模糊也优先OKR子skill）
3. **晋升谈话 vs 常规述职**：提到"晋升谈话/1v1/面谈准备/年终1on1" → `report-review` + `oral-presentation-guide` 组合（第一步加载 `report-review` 整理内容，第二步加载口头汇报策略准备表达）
4. **个人 vs 团队**：提到"我/个人/晋升/绩效/述职" → `report-review`；提到"团队/部门/方向/规划" → `report-planning`
5. **横向协作关键词**：提到"跨团队/拉通/对齐/KO/协作启动" → `report-kickoff`
6. **无法判断**：回到入口问题

**如果场景不明确，先问以下问题再路由：**

1. 这份材料是给谁看的？（高层/大老板 / 直属上级 / 平级协作方 / 风控/财务等专业角色）
2. 是什么场合？（例行规划 / 战略评审 / 事后复盘 / 述职评审 / 项目启动）
3. 读者进来时的情绪预设是什么？（需要被说服 / 需要被安抚 / 在做评估 / 需要被拉动 / 需要核对数据）

## 核心原则：受众决定范式

不同受众的**信息需求和信任机制**完全不同，这决定了写作范式选择：

- **高层/大老板**：缺时间，要结论和方案 → 命题驱动（"我认为选A方案，因为ROI最高。详细分析见附录"）
- **直属上级/导师**：需要理解你的思路 → 信息驱动（展示分析过程，末尾给出倾向判断，邀请讨论）
- **平级/协作方**：视目的而定 → 同步进度用信息驱动，请求配合用命题驱动
- **风控/财务等专业审核**：需要核对数据源头 → 信息驱动（必须展示完整推导链路）

> 详细决策矩阵见 [受众→范式映射](references/audience-guide.md)

## 范式选择提示

**路由到 report-planning 时**，提醒用户：

> 规划汇报有两种写作范式：
> - **信息驱动**：现状→问题→根因→趋势→目标→打法（适合需要展示推导过程的场景）
> - **命题驱动**：核心命题→命题拆解→解决思路→关键问题与解法（适合需要快速给出判断的场景）
> 
> 请确认你的汇报对象是谁，我来帮你选择最合适的范式。参考 [受众适配指南](references/audience-guide.md)

**路由到 report-okr 时**，先问以下问题再展开：

> 请确认是哪种OKR场景：
> - **OKR制定**：新周期开始，需要制定O/KR/KA
> - **OKR进展汇报**：周期中，反映双周/月度执行状态
> - **OKR复盘**：周期结束，总结达成和经验

**路由到其他子 skill 时**，不强制选择范式，但提醒用户考虑受众适配。

**路由到 report-review + oral-presentation-guide（晋升谈话场景）时**：

> 晋升谈话是述职内容和口头表达的双重准备。建议分两步：
> 1. 先用 `report-review` 梳理内容——你要讲什么、判断是什么、成长是什么
> 2. 再用 [口头汇报策略](references/oral-presentation-guide.md) 设计表达方式——15分钟版/开场30秒/Q&A准备

## 公共参考文件

所有子场景均适用，但在不必要的情况下不要加载全部——参考**条件化加载指引**，按需读取对应文件：

- [风格规范](references/style-guide.md) — 语气、用词、禁用词、高级表达技法库、图表使用（写作全程可用，但不需要一次性读完）
- [汇报对象适配](references/audience-guide.md) — 范式选择决策矩阵 + 不同层级/背景受众的适配策略（在 Step 1 确认受众后加载对应部分）
- [口头汇报策略](references/oral-presentation-guide.md) — 不同时长内容适配、开场30秒、Q&A准备、讲述节奏、受众口头适配（仅在用户需要准备口头汇报时加载）
- [技法适配参考](references/technique-adaptation.md) — 各子场景技法适配方式（仅在你帮用户撰写某章并需要决定技法使用方式时，按场景读取对应部分）
- [技法详解](report-planning/references/techniques.md) — 11种高级表达技法的完整说明（含示例、适用受众、常见陷阱）；通过技法适配参考确认需要某技法后，按编号按需读取