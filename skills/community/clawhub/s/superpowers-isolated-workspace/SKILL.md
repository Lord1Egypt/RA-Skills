---
name: superpowers-isolated-workspace
description: Use when starting feature work that needs isolation from current workspace - creates isolated git branches with clean setup and safety verification, adapted for OpenClaw environments
---

# Superpowers Isolated Workspace（OpenClaw 适配版）

## 概述

为新功能工作创建隔离的 git 分支环境。在 OpenClaw 环境中，用 git branch 做隔离比 worktree 更稳定可靠。

**核心原则：** 系统化目录选择 + 安全验证 = 可靠隔离。

**开始时宣布：** "我正在用 isolated-workspace 技能设置隔离工作环境。"

## 目录选择流程

按优先级检查：

### 1. 检查现有目录

```bash
# 按优先级检查
ls -d .isolated 2>/dev/null || ls -d worktrees 2>/dev/null || ls -d .worktrees 2>/dev/null
```

**如果找到：** 使用该目录。

### 2. 检查 AGENTS.md 或项目文档

```bash
grep -i "workspace.*director\|worktree.*director\|isolated.*path" AGENTS.md 2>/dev/null
```

**如果指定了偏好：** 无需询问直接使用。

### 3. 询问主人

如果没有目录且无偏好指定：

```
没有找到隔离工作区目录。在哪里创建？

1. .isolated/ (项目内，隐藏)
2. ~/.openclaw/workspace-<project-name>/ (全局位置)

选择哪个？
```

## 安全验证

### 对于项目内目录

**创建分支前必须验证目录未被跟踪：**

```bash
# 检查目录是否被 git 忽略
git check-ignore -q .isolated 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果没有被忽略：**

立刻修复：
1. 添加到 .gitignore
2. Commit 变更
3. 继续创建隔离分支

## 创建步骤

### 1. 检测项目名

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建特性分支

```bash
# 确定分支名
BRANCH_NAME="feature/<feature-name>"

# 从当前分支创建新分支
git checkout -b "$BRANCH_NAME"

# 确认在正确分支上
git branch --show-current
```

### 3. 运行项目设置

自动检测并运行适当的设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then pip install -e .; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证干净基线

运行测试确保起点干净：

```bash
# 使用项目对应的测试命令
npm test / pytest / cargo test / go test ./...
```

**如果测试失败：** 报告失败，询问是继续还是调查。

**如果测试通过：** 报告就绪。

### 5. 报告位置

```
隔离分支 ready: $BRANCH_NAME
测试通过 (<N> 测试，0 失败)
准备实现 <feature-name>
```

## 快速参考

| 情况 | 行动 |
|------|------|
| `.isolated/` 存在 | 使用它（验证被忽略） |
| `worktrees/` 存在 | 使用它（验证被忽略） |
| 都存在 | 使用 `.isolated/` |
| 都不存在 | 检查 AGENTS.md → 询问主人 |
| 目录未被忽略 | 添加到 .gitignore + commit |
| 基线测试失败 | 报告失败 + 询问 |
| 无 package.json | 跳过依赖安装 |

## 常见错误

**跳过忽略验证**
- 问题：工作区内容被跟踪，污染 git 状态
- 修复：创建项目内目录前总是用 `git check-ignore`

**假设目录位置**
- 问题：造成不一致，违反项目约定
- 修复：遵循优先级：现有 > AGENTS.md > 询问

**不确认就开始**
- 问题：无法区分新 bug 和已有问题
- 修复：报告失败，获得明确许可再继续

**硬编码设置命令**
- 问题：在使用不同工具的项目上失败
- 修复：从项目文件自动检测（package.json 等）

## 与 Brainstorming 的集成

```
用户请求新功能
  → brainstorming 技能（探索设计）
  → 主人批准设计
  → isolated-workspace（创建隔离分支）← 当前技能
  → writing-plans（写实现计划）
  → subagent-dev 或 顺序执行
  → finishing-branch（完成并清理）
```

## OpenClaw 环境说明

在 OpenClaw 环境中（WSL）：
- `git worktree` 命令可用，但与 OpenClaw session 模型不完全兼容
- 使用 `git branch` + 独立工作目录更稳定
- 分支命名约定：`feature/<name>` / `fix/<name>` / `refactor/<name>`
- 完成后通过 `finishing-branch` 技能处理 merge/PR/清理
