---
name: superpowers-finishing-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - presents structured options for merge, PR, or cleanup; adapted for OpenClaw git workflow without worktrees
---

# Superpowers Finishing Branch（OpenClaw 适配版）

## 概述

通过清晰的选项指导完成开发工作：验证测试 → 展示选项 → 执行选择 → 清理。

**开始时宣布：** "我正在用 finishing-a-development-branch 技能完成这项工作。"

## OpenClaw 适配说明

Superpowers 原版使用 git worktree 做隔离工作区，结束时清理 worktree。OpenClaw 环境下：
- 使用 git branch 做隔离
- 结束时清理特性分支或保留供将来使用
- 工作目录即隔离环境，无需额外清理

## 流程

### 步骤 1：验证测试

**展示选项前，验证测试通过：**

```bash
# 运行项目测试套件
npm test / pytest / cargo test / go test ./...
```

**如果测试失败：**
```
测试失败（<N> 个失败）。必须修复才能继续：

[显示失败]

测试通过前不能继续 merge/PR。
```

停止。不要继续到步骤 2。

**如果测试通过：** 继续步骤 2。

### 步骤 2：确定基准分支

```bash
# 尝试常见基准分支
git merge-base HEAD main
git merge-base HEAD master
```

或问："这个分支从 main 分叉——正确吗？"

### 步骤 3：展示选项

展示这 4 个选项：

```
实现完成。你想做什么？

1. Merge 回本地 <base-branch>
2. Push 并创建 Pull Request
3. 保留分支（稍后处理）
4. 丢弃这个工作

哪个选项？
```

**不要加解释**——保持选项简洁。

### 步骤 4：执行选择

#### 选项 1：本地 Merge

```bash
# 切换到基准分支
git checkout <base-branch>

# Pull 最新
git pull

# Merge 特性分支
git merge <feature-branch>

# 验证合并后测试
<test command>

# 如果测试通过
git branch -d <feature-branch>
```

#### 选项 2：Push 并创建 PR

```bash
# Push 分支
git push -u origin <feature-branch>

# 创建 PR
gh pr create --title "<title>" --body "..."
# 或手动创建并提供 URL
```

#### 选项 3：保留

报告：`保留分支 <name>。工作区保持在 <path>。`

**不要做额外清理。**

#### 选项 4：丢弃

**先确认：**
```
这将永久删除：
- 分支 <name>
- 所有 commits：<commit-list>

输入 'discard' 确认。
```

等精确确认。

如果确认：
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## 快速参考

| 选项 | Merge | Push | 保留分支 | 清理 |
|------|-------|------|---------|------|
| 1. 本地 merge | ✅ | - | - | ✅ |
| 2. 创建 PR | - | ✅ | ✅ | - |
| 3. 保留 | - | - | ✅ | - |
| 4. 丢弃 | - | - | - | ✅（强制） |

## 常见错误

**跳过测试验证**
- 问题：Merge 坏代码，创建失败 PR
- 修复：展示选项前总是验证测试

**开放式问题**
- 问题："接下来做什么？" → 模糊
- 修复：展示确切的 4 个结构化选项

**选项 4 无确认**
- 问题：意外删除工作
- 修复：对选项 4 要求输入"discard"确认
