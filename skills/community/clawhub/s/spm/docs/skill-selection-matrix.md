# SPM 技能选型矩阵

> 三个源技能（Superpowers、PM、WBS Executor）逐功能比对，决定 SPM 的融合方案。

## 比对规则

- **✅ 采用** = 直接采用该来源版本
- **🔀 融合** = 融合多个来源的优点的综合版本
- **❌ 排除** = 不纳入 SPM（不适用于 SPM 场景或被其他技能覆盖）
- **🆕 新增** = 三个源技能均无，SPM 新创

---

## 一、需求定义阶段 (Requirement)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 设计讨论/脑暴 | ✅ `brainstorming` - 轮番提问、多方案对比、可视化辅助 | ✅ `/spec` - Idea refinement, PRD, architecture | ❌ 无 | ✅ 采用 Superpowers | Superpowers 的 brainstorming 更成熟，有完整的对话流程、视觉伴侣、设计文档自动生成。PM 的 spec-driven 偏向模板化。 |
| 设计文档规范 | ✅ 自动写 `docs/superpowers/specs/YYYY-MM-DD-xxx-design.md` 并提交 | ✅ 输出 `PRD.md` + `architecture.md` | ❌ 无 | 🔀 融合 | 采用 Superpowers 的自动文档机制，但输出格式融合 PM 的 PRD+架构分离结构。 |
| 假设显式化 | ❌ 隐含在讨论中 | ✅ `/spec` 中强制列出「我正在做的假设」清单 | ❌ 无 | ✅ 采用 PM | PM 这一步非常好——写 spec 前先列出假设，预防隐含假设导致的设计偏离。 |
| 灵魂拷问 (Soul-Searching) | ❌ 隐含在讨论中 | ✅ `spec-driven.md` Phase 1 中的「3 个致命问题」 | ❌ 无 | ✅ 采用 PM | PM 的"3 个致命问题"协议是独特亮点。 |

---

## 二、任务规划阶段 (Planning)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 实施计划编写 | ✅ `writing-plans` - 精确到每步代码、每步命令、2-5 分钟粒度的任务 | ✅ `/plan` - 任务分解、依赖分析、验收标准 | ✅ 创建 WBS 工作包 | 🔀 融合 | Superpowers 的粒度更精细（每步给代码+命令），但其计划格式是 Freeform markdown。SPM 要融合 WBS 台账结构（含 ID、状态、验收标准、证据）和 Superpowers 的精细化实现步骤。 |
| 计划保存位置 | ✅ `docs/superpowers/plans/` | ✅ `docs/task-breakdown.md` + `wbs.json` | ✅ 独立 ledger 文件 | 🔀 融合 | 计划正文用 Superpowers 的精细 markdown 格式，但创建时自动同步到 WBS 台账（含任务 ID、状态、依赖）。 |
| WBS 任务台账 | ❌ 无结构化台账 | ✅ 有 `wbs.json` 但格式偏阶段式 | ✅ 完整台账系统（ID、状态、退出条件、证据、心跳日志） | ✅ 采用 WBS Executor | WBS Executor 的台账模板最完整：WBS 表格 + 活跃状态 + 心跳日志 + 恢复日志 + 交付摘要。PM 的 wbs.json 缺少证据列和恢复机制。 |
| 计划自助审查 | ✅ `writing-plans` 内置的 self-review（占位符扫描、类型一致性、范围匹配） | ❌ 无 | ❌ 无 | ✅ 采用 Superpowers | Superpowers 的 self-review 三步扫描很实用。 |
| 执行方式选择 | ✅ `writing-plans` 末尾给用户 2 选 1 | ❌ 无 | ❌ 无 | ✅ 采用 Superpowers | 「Subagent-Driven vs Inline Execution」选择机制好。 |

---

## 三、执行阶段 (Execution)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| Git Worktree 隔离 | ✅ `using-git-worktrees` - 智能目录选择、gitignore 验证、基线测试验证 | ✅ `using-git-worktrees` 同款（拷贝版） | ❌ 无 | ✅ 采用 Superpowers（最新版） | Superpowers 的版本更成熟（新增 CLAUDE.md 配置检查、全局目录支持），PM 是早期拷贝版。 |
| TDD 铁律 | ✅ `test-driven-development` - RED-GREEN-REFACTOR 完整循环 | ✅ `incremental-build.md` 同款 | ❌ 无 | ✅ 采用 Superpowers | Superpowers 的 TDD skill 更完整（含 Verify RED/GREEN 强制步骤、反模式表、常见合理化借口表、当卡住时的解决方案表）。PM 版内容相似但缺少表格形式。 |
| 逐任务 subagent 执行 | ✅ `subagent-driven-development` - 每任务新 subagent + 两阶段审查 | ✅ `subagent-driven-dev workflow` 同概念但更简单 | ❌ 无 | 🔀 融合 | 核心流程相同，但 Superpowers 有更完善的 prompt 模板和执行流程图。SPM 要叠加 WBS 台账绑定——subagent 处理任务时要同步更新台账状态。 |
| 批量执行（线内） | ✅ `executing-plans` - 批量执行 + 检查点 | ✅ `/build` 阶段概念 | ✅ 逐工作包执行 | 🔀 融合 | Superpowers 的 executing-plans 最轻量好用，融合 WBS 的检查点概念。 |
| 并行 subagent | ✅ `dispatching-parallel-agents` - 独立问题的并行调查 | ❌ 无 | ❌ 无 | ✅ 采用 Superpowers + 🆕 WBS 绑定 | OpenClaw 实测支持并行 subagent。需要新增：并行 subagent 的任务必须关联 WBS 任务 ID，完成后更新台账状态。 |
| 冻结/沙箱保护 | ❌ 无 | ✅ `/freeze & /guard` - 声明沙箱边界、只读外部文件、破坏性操作保护 | ❌ 无 | ✅ 采用 PM | PM 的 safe sandbox protocol 是独特功能。 |

---

## 四、质量保障阶段 (Quality)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 验证铁律 | ✅ `verification-before-completion` - Gate Function | ✅ 同款（拷贝版） | ❌ 无 | ✅ 采用 Superpowers（最新版） | 版本更新，内容更完善（含失败记忆引用、更多反模式）。 |
| 代码审查 | ✅ `requesting-code-review` - 每任务后派 reviewer subagent | ✅ `code-review.md` + `two-stage-review.md` - 两阶段审查（spec + 质量） | ❌ 无 | 🔀 融合 | Superpowers 有 reviewer subagent 模板和 SHAs 获取机制；PM 有 spec 合规审查与工程质量审查的两阶段拆解。合并为三阶段审查：Spec 合规 → 工程质量 → 最终确认。 |
| 接收审查反馈 | ✅ `receiving-code-review` - 如何专业地回应审查意见 | ❌ 无 | ❌ 无 | ✅ 采用 Superpowers | 独特且必要的人力协作技能。 |
| 系统性调试 | ✅ `systematic-debugging` - 4 阶段 + 铁律 + 多组件证据收集 | ✅ `systematic-debugging.md` 同概念 | ❌ 无 | ✅ 采用 Superpowers（最新版） | Superpowers 版更完整（含多组件诊断策略、根因追溯技术、失败记忆参考）。 |
| 质量门控 | ❌ 有隐含的质量要求但无结构化门控 | ✅ 三层质量门系统（Always / Ask / Never） | ❌ 无 | ✅ 采用 PM | PM 的三层质量门控是独特优势。Superpowers 靠 skill 纪律来保证质量，PM 有明确的闸门。 |

---

## 五、交付阶段 (Delivery)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 完成开发分支 | ✅ `finishing-a-development-branch` - 4 选项（合并/PR/保留/丢弃） | ✅ `/ship` 阶段 | ❌ 无 | ✅ 采用 Superpowers | 更完整的流程（测试验证→展示选项→执行选择→清理 worktree）。PM 的 shipping 偏生产部署，不适合所有项目场景。 |
| 部署上线 | ❌ 无 | ✅ 发布计划、回滚计划、监控配置、部署清单 | ❌ 无 | ✅ 采用 PM | 对于需要部署的项目，PM 的 shipping 流程不可替代。作为 SPM 的可选阶段。 |
| 交付摘要 | ❌ 无 | ❌ 无 | ✅ 交付摘要映射回原始需求 | ✅ 采用 WBS Executor | 独特功能：将完成工作映射回原始需求，产出证据包。 |

---

## 六、追踪与恢复 (Tracking & Recovery)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 心跳/检查点 | ❌ 隐含在 subagent 流程中 | ✅ 10 分钟间隔，逐阶段检查点 | ✅ 10 分钟心跳日志 | ✅ 采用 WBS Executor | WBS 的心跳日志格式最合适（含时间戳、活跃项、证据、恢复点）。 |
| 项目状态追踪 | ❌ 无 | ✅ `project-state.json`（阶段、切片、质量指标） | ❌ 无 | ✅ 采用 PM | project-state.json 提供完整的宏观状态视图。 |
| 中断恢复 | ❌ 无（worktree 提供了隐式恢复） | ✅ 检查 project-state → 恢复检查点 → 更新台账 → 继续 | ✅ 完整的恢复决策规则 | 🔀 融合 | WBS 的恢复模式最完整（含恢复决策规则表），但需读取 PM 的 project-state.json。合并为：读取台账 → 验证状态 → 选择恢复边界 → 继续。 |
| 常见合理化借口表 | ✅ 各 skill 内自带 | ✅ 部分 skill 有 | ✅ WBS 有独立表 | ✅ 采用 Superpowers（各 skill 内） | Superpowers 在每个 skill 内嵌了 Rationalization 表，这是关键的反自我欺骗机制。 |
| 红旗列表 | ✅ 各 skill 内自带 | ✅ 部分 skill 有 | ✅ WBS 有独立表 | ✅ 采用 Superpowers（各 skill 内） | 同上的反自我欺骗机制。 |
| 证据驱动完成 | ❌ 有 verification 但无台账证据 | ❌ 隐式（测试通过=完成） | ✅ 每个 done 必须有证据 | ✅ 采用 WBS Executor | WBS 的「无证据不标记 done」原则应贯穿 SPM 全程。 |

---

## 七、技能元层 (Meta)

| 功能点 | Superpowers | PM | WBS Executor | SPM 决策 | 理由 |
|--------|------------|-----|-------------|---------|------|
| 技能发现/调用 | ✅ `using-superpowers` - 1%可能就调用 | ❌ 无 | ❌ 无 | ✅ 采用 Superpowers | 技能发现和自动调用机制是 Superpowers 的核心理念。 |
| 指令优先级 | ✅ 用户指令 > 技能规则 > 系统提示 | ✅ 同概念 | ❌ 无 | ✅ 采用 Superpowers | 更清晰的优先级声明。 |
| 编写技能 | ✅ `writing-skills` - TDD 应用于文档 | ❌ 无 | ❌ 无 | ❌ 排除 | 元技能，不适用于 SPM 工作流本身。 |
| 脚手架/初始化 | ❌ 仅在 brainstorming 中间接涉及 | ✅ `init-project.sh` 完整脚手架 | ❌ 无 | ✅ 采用 PM | 对新项目快速启动很有价值。 |

---

## 八、WBS Executor 独有功能汇总

以下 WBS Executor 功能在 Superpowers 和 PM 中均无直接对应：

| 功能点 | 纳入 SPM？ | 说明 |
|--------|-----------|------|
| ✅ 结构化任务台账（WBS 表） | ✅ 核心 | 作为 SPM 的追踪中枢 |
| ✅ 任务 ID 稳定性 | ✅ 核心 | WBS 项用稳定 ID (`1`, `1.1`, `1.2`) |
| ✅ 退出条件 + 证据列 | ✅ 核心 | 每个任务必须有退出条件和预计证据 |
| ✅ 多区域心跳日志 | ✅ 核心 | 时间、活跃项、最近完成、证据、恢复点 |
| ✅ 恢复日志 | ✅ 核心 | 中断点、验证动作、恢复决策 |
| ✅ 交付摘要映射 | ✅ 核心 | 输出时映射回原始需求 |
| ✅ 活跃状态追踪 | ✅ 核心 | 当前项、最后完成项、最后安全检查点、从哪恢复 |

---

## 九、汇总统计

| 来源 | 技能/功能点数 | 最终纳入 SPM |
|------|-------------|------------|
| **Superpowers** | 14 个完整技能 | 12 个技能直接采用 + 2 个融合 |
| **PM** | ~17 个功能/工作流 | 5 个功能直接采用 + 6 个融合 |
| **WBS Executor** | ~8 个核心功能 | 7 个功能直接采用 + 2 个融合 |
| **SPM 新增** | - | 并行 subagent + WBS 台账绑定 |

### 采用方式分布

- 直接采用 Superpowers: 12 个技能
- 直接采用 PM: 5 个功能
- 直接采用 WBS: 7 个功能
- 融合版本: 8 个功能点
- SPM 新增: 1 个功能（并行 subagent 台账绑定）
- 排除: 1 个（writing-skills）

---

*本文档为 SPM 技能的设计依据，2026-05-04 创建。*
