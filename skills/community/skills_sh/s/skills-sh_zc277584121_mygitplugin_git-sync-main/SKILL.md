---
name: git-sync-main
description: Sync local main branch with the latest code from official upstream or origin remote
allowed-tools:
  - Bash
---

# Git Sync Main

同步最新主分支代码到本地并切换到主分支。支持两种场景：fork 的项目从 official remote 同步，自己的项目从 origin 同步。

## 触发条件

当用户要求同步上游代码、更新主分支、或拉取最新主分支代码时使用此 skill。

## 执行步骤

1. **检查 remote 配置**：`git remote -v`，确认是否存在 `official` remote。

2. **根据是否存在 official remote 分两种情况执行**：

### 情况一：存在 official remote（fork 的项目）

3. **检测主分支名称**：通过 `git remote show official` 或查看本地分支，确定主分支名称（`main` 或 `master`）。

4. **拉取 official 最新代码**：`git fetch official`。

5. **切换到本地主分支**：`git checkout <main-branch>`。

6. **同步代码**：`git reset --hard official/<main-branch>`，将本地主分支重置到 official 最新状态。

7. **推送到 origin**：`git push origin <main-branch> --force-with-lease`，同步自己 fork 的远端主分支。

### 情况二：不存在 official remote（自己的项目）

3. **检测主分支名称**：通过查看本地分支，确定主分支名称（`main` 或 `master`）。

4. **拉取 origin 最新代码**：`git fetch origin`。

5. **切换到本地主分支**：`git checkout <main-branch>`。

6. **同步代码**：`git pull origin <main-branch>`，将本地主分支同步到 origin 最新状态。

### 共同步骤

8. **验证结果**：`git log --oneline -5`，展示最新的几条 commit 确认同步成功。

## 注意事项

- 始终使用 `official` 作为上游 remote 名称（而非 `upstream`），以保持一致性。
- 对于 fork 项目，推送到 origin 时使用 `--force-with-lease` 而非 `--force`，更安全地强制推送。
- 如果当前有未提交的改动，先提示用户处理（stash 或 commit），避免丢失工作。
