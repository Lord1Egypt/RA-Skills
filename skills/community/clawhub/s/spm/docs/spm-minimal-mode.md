# SPM Minimal Mode — 5 Rules

> 适用场景：< 10 个任务，单人项目，快速迭代
> 升级到完整模式：`/spm:mode full`（当任务数 > 10 或多人协作时）

## Core Rules

### 1. WBS Ledger Must Exist
创建 `docs/spm/ledger.md`，包含 Exit Criteria（退出标准）。
没有 Ledger 不执行任何任务。

### 2. Verify Before Completing
每个任务标记 `done` 前，必须运行至少一次验证：
- **最低要求**：编译通过（`npm run build` / `tsc --noEmit`）
- **推荐**：运行相关测试 + 手动冒烟

### 3. One Review Minimum
代码合入前至少经过一人审查：
- 可以是自己隔天审查（对于单人项目）
- 多人项目：必须他人审查
- 审查焦点：逻辑正确性 + 安全 + 性能

### 4. Evidence Required for done
任务标记 `done` 时必须附带证据：
- `git diff` 输出
- 测试通过截图/输出
- 验证命令的输出

### 5. Heartbeat After Each Task
每个任务完成后，更新 Heartbeat Log：
- Active（当前任务）
- Completed（已完成）
- Evidence（证据）
- Resume Point（恢复指引）

## 升级条件

满足以下任一条件时，建议切换到完整模式（`/spm:mode full`）：
- 任务数超过 10
- 开始多人协作
- 需要 TDD（测试驱动开发）
- 需要三级质量门控
- 需要子代理并行执行

## 完整模式新增功能

升级后可获得：
- 5 阶段生命周期
- 三级质量门控（Always / Ask / Never）
- 13 个 Superpowers 工作流
- 子代理调度并行执行
- Git Worktree 物理隔离
- 代码审查（3 阶段）
- 系统调试工作流
- 交付总结模板
