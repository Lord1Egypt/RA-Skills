---
name: structured-dev
description: >
  结构化开发流水线：Research → Plan → Annotate → Implement。
  基于 Boris Tane (Cloudflare) 的 Claude Code 工作流，确保 AI 在架构审查通过前不写一行代码。
  触发词："结构化开发", "structured dev", "走流水线", "RPAI流程",
  "先调研再写代码", "深度开发", "Boris 流程", "research plan implement"。
---

# Structured Dev — 结构化开发流水线

**核心原则：在你审查并批准书面方案之前，不让 AI 写一行代码。**

## 流水线总览

```
Research → Plan → Annotate (1-6轮) → Todo List → Implement → Feedback
```

每一步都有明确产物和审查点。所有产物写入项目根目录的 `.dev/` 文件夹。

---

## Phase 1: Research（深度调研）

### 触发
用户给出开发任务时，**不直接写代码**。

### 执行步骤
1. 在项目根目录创建 `.dev/` 目录（如不存在）
2. 深度阅读相关代码。使用以下关键词引导自己：**deeply, in great details, intricacies, go through everything**。浅层阅读不可接受。
3. 输出 `.dev/research.md`，必须包含：
   - **架构理解**：模块关系、调用链、数据流
   - **相关文件清单**：每个文件的职责说明
   - **现有约定**：ORM 用法、缓存层、API 风格、命名规范
   - **潜在风险**：边界条件、已知 bug、需要注意的耦合点
4. **停下来，等待用户确认**

### 产物
- `.dev/research.md`

### 审查标准
用户通读 research.md，验证 AI 是否真正理解了系统。调研如果错了，方案一定错。

---

## Phase 2: Plan（详细方案）

### 触发
用户确认调研无误后。

### 执行步骤
1. 输出 `.dev/plan.md`，必须包含：
   - **实现思路**：整体方案描述
   - **文件路径**：将修改哪些文件，每个文件改什么
   - **关键代码片段**：不是伪代码，是实际可运行的代码
   - **取舍说明**：为什么选 A 不选 B
   - **影响评估**：对现有模块的影响
   - **排除项**：明确说明不做什么
2. 如果用户提供了参考实现，优先基于参考实现设计
3. **停下来，等待用户审查**

### 产物
- `.dev/plan.md`

### 关键原则
> Claude works dramatically better when it has a concrete reference implementation to work from rather than designing from scratch.

给参考实现 > 从零设计。

---

## Phase 3: Annotate Loop（批注循环）

### 这是整套方法最有价值的部分

用户在 `.dev/plan.md` 中直接添加行内批注。批注类型：

- **纠正假设**："不对，这里应该用 PATCH，不是 PUT"
- **否决方案**："这一节整个删掉，不需要缓存"
- **补充约束**："用 drizzle:generate 生成迁移，不要写原始 SQL"
- **注入上下文**："队列消费者已有重试机制，这段多余，删掉"
- **调整方向**："visibility 字段应在 list 层级，不是 item 上"

### 执行步骤
1. 用户说"处理批注"时，打开 `.dev/plan.md`
2. 逐条处理所有批注
3. **原地更新** plan.md（不新建文件）
4. 明确标注每条批注的处理方式
5. **停下来，等待用户再次审查**
6. 重复 1-6 轮，直到用户说"方案确认"

### 关键约束
- **绝不在批注循环中写实现代码**
- 用户说"先不要实现"时严格遵守
- plan.md 是共享可变状态（shared mutable state），不是一次性输出

---

## Phase 4: Todo List（任务拆分）

### 触发
用户说"方案确认"或"生成 todo list"。

### 执行步骤
1. 在 plan.md 末尾追加 `## 实施清单` 章节
2. 按阶段拆分为细粒度任务，每个任务一行 checkbox：
   ```markdown
   ## 实施清单
   
   ### 阶段一：数据层
   - [ ] 创建 migrations/xxx.sql
   - [ ] 修改 src/models/user.ts 添加 role 字段
   
   ### 阶段二：业务层
   - [ ] 修改 src/services/auth.ts 添加权限检查
   ```
3. 任务粒度：一个函数、一个文件修改、一个测试用例
4. **停下来，等待用户确认任务拆分**

### 产物
- plan.md 中的实施清单章节

---

## Phase 5: Implement（执行实现）

### 触发
用户说"开始实现"。

### 标准实现指令
```
全部实现。每完成一个任务，在 .dev/plan.md 中标记为已完成 [x]。
在所有任务全部完成之前不要停下。
不要添加不必要的注释，保持代码风格与项目一致。
持续运行类型检查/lint，确保不引入新问题。
```

### 执行原则
- 所有决策已在批注循环中完成，实现是机械性执行
- 实现过程中遇到方案没覆盖的问题，暂停并询问
- 不擅自做架构决策
- plan.md 是进度的唯一来源

> I want implementation to be boring. — Boris Tane

---

## Phase 6: Feedback（反馈修正）

### 反馈类型

**简短修正**（直接执行）：
- "你漏了 xxx 函数"
- "挪到 X 文件"
- "用 Y 代替 Z"
- "宽一点" / "有 2px 间隙"

**参照修正**（指向已有代码）：
- "这个表格应该跟用户列表完全一样"

**回滚重来**（方向走偏时）：
- "回滚所有改动，只做 X，别的不动"
- 回滚 + 收窄范围，几乎总是比渐进式修补更好

### 四种方向盘操作
1. **逐项挑选**："第一个用 Promise.all，第三个提取函数，第四五个忽略"
2. **裁剪范围**："删掉下载功能，现在不做"
3. **保护接口**："这三个函数签名不能改"
4. **覆盖选型**："用这个库的内置方法"

---

## 与 Coding Agent 的集成

### 大型任务：spawn coding agent 执行实现

当项目较大或需要长时间运行时，Phase 5 可以 spawn coding agent：

```
用法：
1. 完成 Phase 1-4（Research → Plan → Annotate → Todo List）
2. 用户确认后，spawn coding agent 进入项目目录
3. 把 .dev/plan.md 的内容作为 agent 的 task
4. Agent 按 plan 执行，在 plan.md 中标记进度
```

### 实现完成后

可触发 code-review skill 进行代码审查，或自动创建 GitLab/GitHub MR。

---

## 会话管理

### 默认：单长会话
- 调研 → 实现保持 context 连续
- AI 在整个会话中积累了对系统的理解
- 换新会话 = 理解归零

### 会话中断恢复
- 通过 `.dev/plan.md` 恢复上下文
- 指令："读取 .dev/research.md 和 .dev/plan.md，恢复上下文，继续从 todo list 中未完成的任务开始"

### 文档 > 记忆
- 关键决策写进文档，不依赖 context window
- plan.md 不会被压缩、不会被遗忘

---

## 快速参考

| 阶段 | 产物 | 审查点 | 关键词 |
|------|------|--------|--------|
| Research | `.dev/research.md` | 用户确认理解 | "调研完成" |
| Plan | `.dev/plan.md` | 用户审查方案 | "方案已输出" |
| Annotate | plan.md 更新 | 用户再次审查 | "处理批注" |
| Todo | plan.md 追加清单 | 用户确认拆分 | "方案确认" |
| Implement | 代码 + plan.md ✅ | 持续 typecheck | "开始实现" |
| Feedback | 代码修正 | 用户验收 | 简短指令 |
