# Boris Tane 方法论精要

> 来源：Boris Tane, *How I Use Claude Code* (2026-02-10)
> Boris 是 Cloudflare Workers 可观测性团队工程经理，之前创建了 Baselime（红杉投资，2024 年被 Cloudflare 收购）。

## 核心洞察

**AI 编程最贵的失败不是写错了，是放错了位置。**

AI 看得到局部，看不到全局。它可能写出完美的函数，但如果不理解模块间的职责边界、不知道哪些该复用、不清楚设计决策背后的约束，代码就是定时炸弹。

> "This is the most expensive failure mode with AI-assisted coding, and it's not wrong syntax or bad logic. It's implementations that work in isolation but break the surrounding system." — Boris Tane

## 解法

与其指望 AI 理解你的架构，不如建一套流程，把架构决策显式注入进去。

## Research 阶段要点

- 反复使用：**deeply, in great details, intricacies, go through everything**
- 不这么写 → Claude 走马观花，看函数签名就跳过
- research.md 不是让 AI 交作业，是你的审查面（review surface）
- 调研如果错了，方案一定错，实现也一定错

## Plan 阶段要点

- 不是"优化性能"这种愿景，要写到具体文件路径、代码片段、取舍
- 不用 Claude 内置 Plan 模式 — 自定义 markdown 可编辑、可持久
- 给参考实现 >> 从零设计

## Annotate 循环要点（最有价值的部分）

- 在文档中直接加行内批注，不是在聊天里解释
- markdown 充当共享可变状态（shared mutable state）
- "先不要实现"五个字至关重要 — 不写的话 AI 会擅自动手
- 1-6 轮循环：泛泛方案 → 精准规格
- 按自己的节奏思考，精确定位标注

## Implement 阶段要点

- 到这一步，所有决策已完成
- 实现应该是无聊的（boring）— 创造性工作在批注循环中已结束
- "全部实现 + 不要停下 + 标记完成 + 持续 typecheck"

## Feedback 阶段要点

- 短、准、狠
- 贴截图比三段描述清楚
- 引用已有代码当参照
- 方向走偏 → 不修补，直接回滚 + 收窄范围重来

## 会话管理

- 单长会话，不拆分
- plan.md 是外部文件，context 压缩不影响它
- 与其纠结会话续不续，不如把决策写进文档

## 一句话总结

> "Read deeply, write a plan, annotate the plan until it's right, then let Claude execute the whole thing without stopping, checking types along the way." — Boris Tane
