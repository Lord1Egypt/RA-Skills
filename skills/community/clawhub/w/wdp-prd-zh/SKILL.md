---
name: wdp-prd-zh
description: Use when the user runs /wdp-prd-zh to discuss/record new requirements, view the backlog, or dispatch confirmed requirements to background subagents for parallel implementation. 中文版需求管理。子命令：new, list, update, confirm, dispatch, accept
disable-model-invocation: true
---

# wdp-prd-zh — 需求管理

基于 superpowers 的需求管理：**讨论与实现解耦**。随时 brainstorm 新需求存为卡片；确认后通过后台子代理并行实现，主会话不被阻塞。

## 何时使用
- 讨论/记录新需求（不立即实现）→ `/wdp-prd-new`
- 查看 backlog / 调度状态 → `/wdp-prd` 或 `/wdp-prd-list`
- 确认需求可派发 → `/wdp-prd-confirm <id>`
- 派发实现 → `/wdp-prd-dispatch`
- 验收完成的需求 → `/wdp-prd-accept <id>`
- 修改卡片 → `/wdp-prd-update <id>`

## 存储模型
- 全局根：`~/.wdp/prd/`（可用环境变量 `PRD_ROOT` 覆盖）。
- 项目子目录：`<PRD_ROOT>/<project-slug>/`，内含：
  - `backlog/R-###.md` 需求卡片
  - `execution-plan.md` 调度视图
  - `plans/` 实现计划存档
- 桥接：项目根 `.wdp-prd` 文件，内容为该项目的全局根绝对路径（即 `<PRD_ROOT>/<slug>/`）。每次命令操作前先读它。

### 初始化
若 `<cwd>/.wdp-prd` 不存在：
1. 询问项目名（slug，小写连字符）。
2. 创建 `<PRD_ROOT>/<slug>/`（含 `backlog/`、`plans/`）与空 `execution-plan.md`，并在项目内创建 `docs/superpowers/specs/`。
3. 写 `.wdp-prd`，内容为全局根绝对路径。
4. 报告初始化完成。

## 状态机
`draft → confirmed → in-progress → needs-review → accepted → done`
另有 `blocked`（依赖未满足 / 子代理失败）、`cancelled`。

## 调度规则
对全部卡片计算状态报告，两条规则（MVP 不做拓扑排序）：
1. `depends_on` 中仍有非 done 状态 → `⏳ 等 R-00X 完成`（被 `cancelled` 的依赖视为已满足，不阻塞）。
2. `conflicts_with` 中有 in-progress → `⚠ 与 R-00X(开发中) 冲突，需等它完成或用户裁定`。

计算前先检查 depends_on 关系：成环则报告环（R-003↔R-004）并标记相关卡片 blocked，不派发；引用不存在的依赖 id 则报告『依赖 R-999 不存在，检查 depends_on』，不派发。依赖不存在的卡片归入 ⏳ 阻塞并在括号注明『依赖不存在』。

阻塞提示括号内显示依赖卡片当前的实际状态（如 confirmed / in-progress / cancelled）。

**可立即派发** = status==confirmed + 依赖全满足 + 与 in-progress 无冲突 + in-progress 数量 < 并发上限。
**并发上限** 默认 2，可配置（环境变量 `PRD_MAX_CONCURRENT`）。超出报「已达并发上限，先验收手头的」。
**同批约束**：用户挑选的一批必须两两无冲突；选了互相 conflicts_with 的一对时，强制只挑一个；每批最多 `PRD_MAX_CONCURRENT − 当前 in-progress` 张。

报告格式：
```
▶ 现在就能并行派发      [R-001, R-002]
⏳ 依赖阻塞，等任务完成  R-005 → 等 R-002(开发中)
⚠ 与执行中任务冲突      R-003 ↔ R-004(开发中)
```

## execution-plan.md
每次状态变更/派发/验收后由 Claude 重写（以**全部卡片的当前状态**为准：needs-review/accepted/done 的卡片自然离开 in-progress/可立即派发/阻塞/冲突 列表，不再出现）：
````markdown
# 执行计划（自动生成，勿手改）
更新时间: YYYY-MM-DD
in-progress: [R-001, R-002]
可立即派发: []
阻塞: R-005 → 等 R-002
冲突: []
````

## 命令

### /wdp-prd —— 主入口
1. 读所有卡片，输出 backlog 摘要表格（id/title/status/priority/依赖）。
2. 按「调度规则」计算并输出当前调度状态报告（可立即派发 / 依赖阻塞 / 冲突 / 并发上限提示，格式见报告格式）。
3. 提示可用的 `/wdp-prd-*` 命令。

### /wdp-prd-list —— 列表
输出 backlog 摘要表格，按 priority 从 high 到 low、同 priority 再按 created 升序排序。若卡片为空，明确说明。

### /wdp-prd-update <id> —— 修改卡片
1. 定位卡片（不存在则报错并列出最近 id）。
2. 询问要改的字段（status/priority/depends_on/conflicts_with/title）。
3. 校验取值：status 必须属于状态机集合；priority 必须 high/medium/low。
4. 更新字段，`updated` 置为当天，`created` 保持不变。
5. 重写 `execution-plan.md`（如受影响）。

### /wdp-prd-confirm <id> —— 确认需求
1. 卡片存在且 status==draft；卡片不存在或非 draft → 报错并说明当前状态。
2. 确认后 status→confirmed，`updated` 更新。
3. 重写 `execution-plan.md`。

### /wdp-prd-dispatch —— 派发
1. 出调度状态报告（规则见「调度规则」）。
2. 用户挑选一批「立即派发」（同批两两无冲突；并发超上限时提示先验收）。
3. 每需求 spawn 一个**后台子代理**，在 **git worktree 隔离分支**中执行：
   `superpowers:writing-plans` → `superpowers:test-driven-development` → 开发 → `superpowers:verification-before-completion`；
   派发时同步把卡片 → in-progress、`updated` 更新、重写 execution-plan.md（保证子代理整个运行期间该卡片都算 in-progress）；
   子代理产出实现计划后，归档到 `<pointer>/plans/<id>.md`。
4. 子代理返回报告：改了什么文件、跑了哪些测试、结果、遗留问题。
5. 子代理完成后：卡片 → needs-review，提示用户 `/wdp-prd-accept <id>`。

**非 git 降级**：检测不到 git 仓库时，明确警告无法 worktree 隔离，询问用户仍要串行派发还是放弃；不得静默继续。

### /wdp-prd-accept <id> —— 验收
1. 卡片 status==needs-review，否则提示先派发。
2. 合并子代理的 worktree 分支到当前工作分支。
3. 跑**全量集成测试**；失败 → 卡片留 needs-review，记录失败原因，提示修复或回滚。
4. 走 **code review**（复用 `superpowers:requesting-code-review`）。
5. 呈现变更摘要 + review 结论给用户 → 用户确认。
6. 确认 → status→accepted→done，填「验收记录」，重写 execution-plan.md。
7. 验收通过后清掉已合并的 worktree（复用 `superpowers:using-git-worktrees` 的清理流程）。

### /wdp-prd-new —— 讨论并新建需求
1. 确认本项目的 `.wdp-prd` 指针存在（缺失则先走「初始化」）。
2. 调用 `superpowers:brainstorming` 与用户讨论需求，产出设计文档（存到项目 `docs/superpowers/specs/`）。
3. 按 `references/card-template.md` 创建新卡片 `backlog/R-###.md`：
   - id 自增（当前最大 +1）；status=draft；priority 由用户定或默认 medium。
   - created/updated = 当天。
   - 「设计文档」段写入 spec 路径。
4. 重写 `execution-plan.md`。

## 需求卡片
格式见 `references/card-template.md`。创建时复制模板。

## 错误处理
| 情况 | 处理 |
|------|------|
| 非 git 仓库 | 无法 worktree 隔离 → 明确警告，降级串行/非隔离（见派发流程） |
| 子代理失败 | 卡片 → blocked，报告原因，更新 execution-plan |
| 依赖成环 | 检测并报告环，不派发 |
| 依赖不存在 | 报告依赖 id 不存在，提示检查 depends_on |
| 同批冲突 | 强制只挑一个 |
| review 未过 | 卡片留 needs-review，记录结论 |
| 用户未确认 | 卡片留 needs-review |
| 无 Agent 工具 | 降级为手动引导流程 |
| `.wdp-prd` 缺失 | 触发初始化 |

## 验证
按 `references/test-scenarios.md` 干跑全部场景（S1–S6）。全部 Expected 满足才算 skill 验证通过。
