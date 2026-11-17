---
name: code-reviewer
description: >
  Use this skill to review code. It supports both local changes (staged or working tree)
  and remote Pull Requests (by ID or URL). It focuses on correctness, maintainability,
  and adherence to project standards. Covers Rust, Go, Python, TypeScript, JavaScript,
  Java, NestJS, React, Vue, Svelte with language-specific review guides.
  When called as a sub-skill of review-workflow, receives [CHANGE_PURPOSE] and [CODE_INPUT]
  from the orchestrator and outputs a structured [REVIEW_REPORT] for downstream steps.
version: 1.0.0
allowed-tools: Bash, Read
---

# Code Reviewer

将代码审查从"守门"转变为"知识共享"——通过建设性反馈、系统分析和协作改进来提升代码质量。

## 何时加载子 Reference

本 Skill 会根据代码变更的语言/框架，按需查阅对应的语言专项审查指南。所有指南位于当前 Skill 同级 `references/` 目录下。

| 语言/框架     | Reference 文件                                 | 何时查阅     |
|---------------|-----------------------------------------------|-------------|
| Rust          | [references/rust.md](references/rust.md)       | diff 含 `.rs` 文件 |
| Go            | [references/go.md](references/go.md)           | diff 含 `.go` 文件 |
| Python        | [references/python.md](references/python.md)   | diff 含 `.py` 文件 |
| TypeScript    | [references/typescript.md](references/typescript.md) | diff 含 `.ts`/`.tsx` |
| JavaScript    | [references/typescript.md](references/typescript.md) | diff 含 `.js`/`.jsx`（TS 规则也适用） |
| Java          | [references/java.md](references/java.md)       | diff 含 `.java` 文件 |
| NestJS        | [references/nestjs.md](references/nestjs.md)   | 项目含 `@nestjs/` 依赖 |
| React         | [references/react.md](references/react.md)     | diff 含 `.tsx`/`.jsx` 且含 React import |
| Vue           | [references/vue.md](references/vue.md)         | diff 含 `.vue` 文件 |
| Svelte        | [references/svelte.md](references/svelte.md)   | diff 含 `.svelte` 文件 |

跨语言通用指南（始终参考）：

| 主题           | Reference 文件                                                   |
|---------------|------------------------------------------------------------------|
| 通用代码质量   | [references/code-quality-universal.md](references/code-quality-universal.md) |
| 常见 Bug 清单  | [references/common-bugs-checklist.md](references/common-bugs-checklist.md)   |
| 安全审查       | [references/security-review-guide.md](references/security-review-guide.md)    |
| 审查最佳实践   | [references/code-review-best-practices.md](references/code-review-best-practices.md) |

> **查阅策略**：审查阶段根据变更文件类型，先并行加载对应的语言专项指南和通用指南，
> 再逐文件对照指南中的 Checklist 逐项检查。

---

## 核心原则

### 审查心态

**代码审查的目标：**
- 在合入前发现 Bug 和边界情况
- 确保代码可维护性和可读性
- 在团队中分享知识
- 强制执行编码标准
- 改进设计和架构

**不是代码审查的目标：**
- 炫耀知识
- 纠结格式化（交给 linter）
- 不必要地阻塞进度
- 按个人偏好重写代码

### 有效反馈

**好的反馈是：**
- 具体且可执行
- 教育性而非评判性
- 聚焦代码而非个人
- 平衡（也要表扬好的工作）
- 有优先级（关键 vs 锦上添花）

```
不好的反馈："这样写是错的。"
好的反馈："当多个用户并发访问时这里存在竞态条件，考虑用互斥锁保护这段临界区。"

不好的反馈："为什么不用 X 模式？"
好的反馈："考虑过用 Repository 模式吗？能让这段逻辑更容易测试。参考：[链接]"

不好的反馈："这个变量名改一下。"
好的反馈："[nit] 建议用 `userCount` 代替 `uc` 以提高可读性。不改也不阻塞合入。"
```

### 审查范围

**应该审查的：**
- 逻辑正确性和边界情况
- 安全漏洞
- 性能影响
- 测试覆盖率和质量
- 错误处理
- API 设计和命名
- 架构适配性

**不应该手动审查的：**
- 代码格式化（交给 Prettier、Black、gofmt 等）
- Import 排序
- Lint 违规
- 简单的拼写错误

---

## 审查流程

### Phase 1: 上下文收集（2-3 分钟）

在深入代码之前，理解以下内容：

**当作为 review-workflow 子 Skill 调用时**：
- `[CHANGE_PURPOSE]` 和 `[PROPOSAL_INFO]` 已由编排层收集，直接使用即可
- 如果信息缺失，按以下优先级处理：
  - 有 `[CHANGE_PURPOSE]` → 记录为审查锚点，进入 Phase 2
  - 无 `[CHANGE_PURPOSE]` 但用户刚提供过背景 → 向用户确认一次
  - 没有背景 → 审查结论标注"仅基于代码规范"

**当独立使用时**（如审查远程 PR）：
1. **读取 PR 描述和关联 Issue**（如有）
2. **检查变更规模**：超过 400 行？建议拆分
3. **审查 CI/CD 状态**：测试是否通过？
4. **理解业务需求**
5. **注意相关架构决策**

### Phase 2: 高层审查（5-10 分钟）

1. **架构与设计** — 方案是否适合问题？
   - 检查：SOLID 原则、耦合/内聚、反模式
2. **性能评估** — 是否有性能隐患？
   - 检查：算法复杂度、N+1 查询、内存使用
3. **文件组织** — 新文件是否在正确的位置？
4. **测试策略** — 是否有覆盖边界情况的测试？

### Phase 3: 逐行审查（10-20 分钟）

对每个文件对照以下维度检查：

- **逻辑与正确性** — 边界情况、off-by-one、null 检查、竞态条件
- **安全性** — 输入校验、注入风险、XSS、敏感数据
- **性能** — N+1 查询、不必要的循环、内存泄漏
- **可维护性** — 清晰的命名、单一职责、必要的注释
- **代码复用** — 接受新代码前，先搜索已有工具函数/helpers 是否能替代

> **关键**：根据变更文件的语言/框架，加载对应的 Reference 指南（见顶部表格），
> 逐项对照指南中的 Checklist 检查。

### Phase 4: 总结与决策（2-3 分钟）

1. 总结关键关注点
2. 突出做得好的地方
3. 明确决策：
   - ✅ 批准 (Approve)
   - 💬 评论 (Comment) — 小建议
   - 🔄 请求修改 (Request Changes) — 必须处理
4. 复杂情况可提议结对编程

---

## 审查技巧

### 技巧 1: 提问式审查

不要直接陈述问题，用提问引导思考：

```
不好的："列表为空时会崩溃。"
好的："如果 `items` 是空数组会发生什么？"

不好的："这里需要错误处理。"
好的："如果 API 调用失败，这里应该怎么处理？"
```

### 技巧 2: 建议而非命令

使用协作式语言：

```
不好的："你必须改成 async/await"
好的："建议：async/await 可能让这段代码更易读。你觉得呢？"

不好的："把这个提取成函数"
好的："这段逻辑在 3 个地方出现了。考虑提取成函数怎么样？"
```

### 技巧 3: 区分严重程度

使用标签指示优先级：

| 标签 | 含义 | 处理 |
|------|------|------|
| 🔴 `[blocking]` | 必须在合入前修复 | 阻塞合入 |
| 🟡 `[important]` | 应该修复，如有异议可讨论 | 建议修复 |
| 🟢 `[nit]` | 锦上添花，不阻塞 | 可选 |
| 💡 `[suggestion]` | 替代方案供参考 | 可选 |
| 📚 `[learning]` | 教育性评论，无需处理 | 无需操作 |
| 🎉 `[praise]` | 做得好的地方 | 无需操作 |

---

## 个人审查习惯（所有审查必须遵守）

### 函数长度（分级提醒）

- **≤ 50 行**：正常，无需提示
- **50–80 行**：提醒审查者关注是否职责单一；若逻辑清晰、无深层嵌套则放过
- **80–150 行**：警告，建议拆分或重构，必须在 review 中给出理由
- **> 150 行**：阻塞项，必须拆分后才能合并

**豁免条件**：同时满足以下所有条件时，即使超过 80 行也不警告：
- 函数为纯数据处理/配置映射（如大 match/switch、路由表、配置字典）
- 无明显嵌套（缩进层级 ≤ 2）
- 无副作用（不修改外部状态、不发起 I/O）

### 代码质量底线

- 检查是否缺少边界条件和空值处理。
- 变量命名须清晰表达意图，禁止使用单字母变量（循环索引 `i`、`j`、`k` 除外）。
- 任何 `TODO` 或 `FIXME` 注释必须标记为阻塞项，要求附上修复计划或关联 issue。
- 新增逻辑必须建议补充单元测试。
- 禁止在循环内进行数据库查询或网络请求（性能硬伤）。
- PR 超过 400 行时建议拆分，使审查更聚焦。

---

## 输出格式（与 review-workflow 对接）

当作为 review-workflow 子 Skill 调用时，输出以下结构化报告作为 `[REVIEW_REPORT]`：

```
### 审查报告

**变更背景确认**
- 目的：<复述 [CHANGE_PURPOSE]，确认理解正确>
- 关联提案：<[PROPOSAL_INFO] 或"无">

**意图层问题（逻辑/需求偏差）**
- [#I01] 问题描述 | 位置：<文件名>:<行号> | 严重程度：🔴 blocking / 🟡 important
- [#I02] ...

**规范层问题**
- [#C01] 问题描述 | 位置：<文件名>:<行号> | 违反规则：<具体规则> | 严重程度：🟡 important / 🟢 nit
- [#C02] ...

**改进建议**
- [#S01] 建议描述 | 位置：<文件名>:<行号> | 类型：💡 suggestion
- [#S02] ...

**函数长度提醒**
- <函数名>：XX 行 | 状态：✅ 正常 / 👀 关注 / ⚠️ 警告 / 🔴 阻塞

**安全审查要点**（对照 security-review-guide.md）
- <涉及安全的检查项及结果>

**测试补充建议**
- 针对新增逻辑，列出建议补充的单元测试（至少 1 个正向 + 1 个边界）

**习惯符合度评分：X / 5**
（5 = 完全符合所有规则且无改进空间；1 = 存在多个严重问题）

**决策**
- ✅ 批准 / 💬 评论（小建议）/ 🔄 请求修改（必须处理）

**下一步操作**
- 无严重问题 → 自动进入调试修复阶段
- 有严重问题 → 等待用户决策
```

---

## 门控规则

- 若存在 🔴 `[blocking]` 问题（意图层或规范层），必须暂停，询问：
  > "发现以上阻塞问题，是否忽略并继续后续步骤？"
- 用户确认后，或无阻塞问题时，返回报告供 review-workflow 进入下一阶段。
- 将完整报告记录为 `[REVIEW_REPORT]`。