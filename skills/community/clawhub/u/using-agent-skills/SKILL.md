---
name: using-agent-skills
version: 1.0.0
description: "Check for applicable skills before responding to any task"
tags: [coding, backend, iterative, browser, visual]
---

# Using Agent Skills �?开发技能路�?v1.0

> **定位**：被 `coding-framework` �?Step 0 调用的开发技能路由表
> 
> **调用关系**：`coding-framework` �?`using-agent-skills` �?24 �?Anthropic 开发技�?
## 核心理念

Agent Skills 是按开发阶段组织的工程工作流技能集合。每个技能编码高级工程师遵循的特定流程。本 skill 提供**开发阶段决策树**，帮�?routing 到正确的技能�?
## 技能发�?
当任务到达时，识别开发阶段并应用相应的技能：

```
任务到达
    �?    ├── 还不知道想要什么？ ──────�?interview-me
    ├── 有粗略概念，需要变体？ �?idea-refine
    ├── 新项�?功能/变更�?──�?spec-driven-development
    ├── 有规格，需要任务？ ──────�?planning-and-task-breakdown
    ├── 实现代码�?────────────�?incremental-implementation
    �?  ├── UI 工作�?─────────────────�?frontend-ui-engineering
    �?  ├── API 工作�?────────────────�?api-and-interface-design
    �?  ├── 需要更好的上下文？ ─────�?context-engineering
    �?  ├── 需要文档验证的代码�?───�?source-driven-development
    �?  └── 高风�?不熟悉的代码�?──�?doubt-driven-development
    ├── 编写/运行测试�?────────�?test-driven-development
    �?  └── 基于浏览器？ ───────────�?browser-testing-with-devtools
    ├── 出问题了�?──────────────�?debugging-and-error-recovery
    ├── 审查代码�?───────────────�?code-review-and-quality
    �?  ├── 太复杂？ ─────────────�?code-simplification
    �?  ├── 安全问题�?───────�?security-and-hardening
    �?  └── 性能问题�?───�?performance-optimization
    ├── 提交/分支�?─────────�?git-workflow-and-versioning
    ├── CI/CD 管道工作�?──────────�?ci-cd-and-automation
    ├── 弃用/迁移�?────────�?deprecation-and-migration
    ├── 写文�?ADR�?───────────�?documentation-and-adrs
    ├── 添加日志/指标/告警�?───�?observability-and-instrumentation
    └── 部署/发布�?─────────�?shipping-and-launch
```

---

## 核心操作行为

这些行为始终适用，跨所有技能。它们是不可协商的�?
### 1. 浮出假设

在实现任何非平凡的事情之前，明确说明你的假设�?
```
我的假设�?1. [关于需求的假设]
2. [关于架构的假设]
3. [关于范围的假设]
�?现在纠正我，否则我将按这些假设继续�?```

不要默默填充模糊的需求。最常见的失败模式是做出错误的假设并 unchecked 地运行。尽早浮出不确定性——它比返工更便宜�?
### 2. 主动管理困惑

当你遇到不一致、冲突的需求或不清晰的规格时：

1. **停止�?* 不要带着猜测继续�?2. 命名具体的困惑�?3. 呈现权衡或提出澄清问题�?4. 等待解决后再继续�?
**差：** 默默选择一个解释并希望它是对的�?**好：** "我在规格中看�?X，但在现有代码中看到 Y。哪个优先？"

### 3. 在合理时推回

你不�?yes-machine。当方法有明显问题时�?
- 直接指出问题
- 解释具体的缺点（尽可能量化—�?这增加约 200ms 延迟"而不�?这可能更�?�?- 提出替代方案
- 如果人类在充分信息下覆盖，接受人类的决定

谄媚是失败模式�?当然�?然后实现一个坏主意对谁都没帮助。诚实的技术分歧比虚假的同意更有价值�?
### 4. 强制简�?
你的自然倾向是过度复杂化。主动抵抗它�?
在完成任何实现之前，问：
- 能用更少行完成吗�?- 这些抽象值得其复杂性吗�?- 资深工程师会看这个说"为什么不直接…�?吗？

如果你构建了 1000 行�?100 行就够，你失败了。偏好无聊、明显的解决方案。聪明是昂贵的�?
### 5. 维护范围纪律

只碰你被要求碰的东西�?
不要�?- 删除你不理解的注�?- "清理"与任务正交的代码
- 作为副作用重构相邻系�?- 删除看起来未使用的代码而没有明确批�?- 添加规格�?看起来有�?的功�?
你的工作是手术精度，不是主动翻新�?
### 6. 验证，而非假设

每个技能都包括验证步骤。任务在验证通过前不算完成�?看起来对"永远不够——必须有证据（通过的测试、构建输出、运行时数据）�?
每技能验证是本地检查。适用�?每个*变更的项目级标准，无论哪个技能活跃，�?Definition of Done：测试通过、无回归、行为在运行时验证、文档更新。它补充每个任务的验收标准而非替代它们�?
---

## 要避免的失败模式

这些是看起来像生产力但创造问题的微妙错误�?
1. 做出错误的假设而不检�?2. 不管理自己的困惑——迷失时继续前进
3. 不浮出你注意到的不一�?4. 不在非显而易见的决策上呈现权�?5. 对有明确问题的方法谄媚（"当然�?�?6. 过度复杂化代码和 API
7. 修改与任务正交的代码或注�?8. 删除你不完全理解的东�?9. 在没有规格的情况下构建因�?显然要构建什�?
10. 跳过验证因为"看起来对"

---

## 技能规�?
1. **在开始工作前检查适用的技能�?* 技能编码防止常见错误的流程�?
2. **技能是工作流，不是建议�?* 按顺序跟随步骤。不要跳过验证步骤�?
3. **多个技能可以适用�?* 功能实现可能按顺序涉�?`idea-refine` �?`spec-driven-development` �?`planning-and-task-breakdown` �?`incremental-implementation` �?`test-driven-development` �?`code-review-and-quality` �?`code-simplification` �?`shipping-and-launch`�?
4. **有疑问时，从规格开始�?* 如果任务非平凡且没有规格，从 `spec-driven-development` 开始�?
---

## 生命周期序列

对于完整功能，典型的技能序列是�?
```
1.  interview-me                �?提取用户实际想要什�?2.  idea-refine                 �?精炼模糊想法
3.  spec-driven-development     �?定义我们在构建什�?4.  planning-and-task-breakdown �?分解为可验证�?5.  context-engineering         �?加载正确上下�?6.  source-driven-development   �?对照官方文档验证
7.  incremental-implementation  �?逐片构建
8.  observability-and-instrumentation �?构建时插桩（�?7-9 并行运行，不是之后）
9.  doubt-driven-development    �?交叉审查非平凡决�?10. test-driven-development     �?证明每片工作
11. code-review-and-quality     �?合并前审�?12. code-simplification         �?在保留行为的同时减少不必要的复杂�?13. git-workflow-and-versioning �?清晰的提交历�?14. documentation-and-adrs      �?文档化决�?15. deprecation-and-migration   �?在需要时退役旧系统并安全迁移用�?16. shipping-and-launch         �?安全部署
```

不是每个任务都需要每个技能。Bug 修复可能只需要：`debugging-and-error-recovery` �?`test-driven-development` �?`code-review-and-quality`�?
---

## 快速参�?
| 阶段 | 技�?| 一行总结 |
|------|------|----------|
| 定义 | interview-me | 在任何计划、规格或代码存在之前，浮出用户实际想要什�?|
| 定义 | idea-refine | 通过结构化发散和收敛思维精炼想法 |
| 定义 | spec-driven-development | 代码之前的需求和验收标准 |
| 计划 | planning-and-task-breakdown | 分解为小的、可验证的任�?|
| 构建 | incremental-implementation | 薄垂直切片，每片在扩展前测试 |
| 构建 | source-driven-development | 实现前对照官方文档验�?|
| 构建 | doubt-driven-development | 对每个非平凡决策的对抗性新鲜上下文审查 |
| 构建 | context-engineering | 正确的时间正确的上下�?|
| 构建 | frontend-ui-engineering | 带可访问性的生产质量 UI |
| 构建 | api-and-interface-design | 带清晰契约的稳定接口 |
| 验证 | test-driven-development | 先失败测试，然后让它通过 |
| 验证 | browser-testing-with-devtools | Chrome DevTools MCP 用于运行时验�?|
| 验证 | debugging-and-error-recovery | 复现 �?定位 �?修复 �?防护 |
| 审查 | code-review-and-quality | 五轴审查带质量门 |
| 审查 | code-simplification | 保留行为的同时减少不必要的复杂�?|
| 审查 | security-and-hardening | OWASP 防护、输入验证、最小权�?|
| 审查 | performance-optimization | 先测量，只优化重要的 |
| 发布 | git-workflow-and-versioning | 原子提交、清晰历�?|
| 发布 | ci-cd-and-automation | 每次变更的自动化质量�?|
| 发布 | deprecation-and-migration | 移除旧系统并安全迁移用户 |
| 发布 | documentation-and-adrs | 文档化为什么，不只是什�?|
| 发布 | observability-and-instrumentation | 结构化日志、RED 指标、追踪、基于症状的告警 |
| 发布 | shipping-and-launch | 发布前检查清单、监控、回滚计�?|

---

## 与其他技能的关系

| 技�?| 关系 |
|------|------|
| **daily-agent** | 通用任务调度，using-agent-skills 专注开发工作流技能路�?|
| **所有其他技�?* | using-agent-skills 是发现和调用它们的元技�?|

---

## 约束

- **技能优�?*：开始工作前检查适用的技�?- **顺序跟随**：按顺序跟随步骤，不跳过验证
- **多技能组�?*：复杂任务可以按顺序应用多个技�?- **核心行为**：浮出假设、管理困惑、推回、强制简单、范围纪律、验�?- **失败模式警觉**：避�?10 个常见微妙错�?
---

*Version 1.0.0 �?来源：Anthropic 官方 using-agent-skills skill*
