# WBS Task Ledger Template

Create at `docs/spm/ledger.md` before starting substantive execution.

## Task Summary

- Assignment:
- Requested outcome:
- Deliverables:
- Success criteria:
- Constraints:
- Assumptions:
- External dependencies:
- Risks:

## WBS

| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|-----------|---------------|---------------|----------|--------|
| 1 | [init] | - | [self-contained context for cold-start execution] | [how we know it's done] | [file/command output] | todo |

### Context Brief 编写规范

每个任务的 Context Brief 必须包含以下信息（确保新 agent 无需读前置任务即可冷启动执行）：

1. **本任务目标**：一句话说明做什么
2. **前置产物**：依赖任务完成后产出了什么文件/接口（如"Task 1 已生成 `src/models/user.ts`"）
3. **涉及文件**：需要创建/修改的精确文件路径
4. **关键约束**：架构决策、命名规范、技术选型等本任务必须遵守的约束
5. **验收要点**：从 exit_criteria 中摘取最关键的 1-2 条

示例：
```
Context Brief: 实现 JWT token 签发中间件。
前置: Task 1 已完成 User 模型 (`src/models/user.ts`)。
涉及: `src/middleware/auth.ts` (新建), `src/routes/auth.ts` (新建)。
约束: 使用 HS256 算法，token 有效期 24h，密钥从 `process.env.JWT_SECRET` 读取。
验收: `POST /auth/login` 返回有效 token，`GET /me` 携带 token 返回用户信息。
```

Allowed statuses: `todo`, `doing`, `done`, `blocked`, `skipped`

## Active State

- Current item:
- Last completed item:
- Last safe checkpoint:
- Resume from here:
- Next exact action:
- Current blocker:

## Heartbeat Log

> ⚠️ SPM Integrity: Protected by `bash scripts/verify-wbs.sh`
> Run `bash scripts/attest-wbs.sh` after each WBS update.

| Time | Active item | Last completed | Evidence added | Resume point |
|------|-----------|---------------|----------------|-------------|
| YYYY-MM-DD HH:MM | | | | |

## Recovery Log

| Time | Interruption point | Verification | Recovery decision |
|------|-------------------|-------------|------------------|
| YYYY-MM-DD HH:MM | | | | |

## Mutation Log

计划变更的审计轨迹。任何对 WBS 的修改（拆分/插入/跳过/重排/废弃）必须在此记录。

| Time | Mutation Type | Affected IDs | Reason | New IDs (if split/insert) |
|------|--------------|-------------|--------|--------------------------|
| YYYY-MM-DD HH:MM | split / insert / skip / reorder / abandon | 3 | 任务太大需拆分 | 3.1, 3.2 |

### 允许的突变类型

| 类型 | 说明 | 规则 |
|------|------|------|
| **split** | 拆分任务为更小单元 | 原任务标记 `skipped`，子任务用 `X.1, X.2` 编号 |
| **insert** | 在已有任务之间插入新任务 | 新任务用小数字编号（如 `2.5` 插入在 2 和 3 之间） |
| **skip** | 跳过不需要的任务 | 标记 `skipped` + 注明原因 |
| **reorder** | 重排任务顺序 | 更新 Dependencies 列，验证无循环依赖 |
| **abandon** | 废弃任务（方向错误） | 标记 `skipped` + 注明"废弃：原因"，不移除行 |

**铁律：所有突变必须在 Mutation Log 留痕。计划审查通过后的突变需要重新触发对抗性审查。**

## Delivery Summary

- Completed work:
- Evidence package:
- Remaining blockers/skipped:
- Residual risks:
- Final handoff note:
