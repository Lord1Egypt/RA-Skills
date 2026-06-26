---
name: git-fork-clone
description: Fork a GitHub repo and clone it locally with proper remote setup
allowed-tools:
  - Bash
---

# Git Fork & Clone

Fork 别人的 GitHub 仓库并 clone 到本地，自动配置 official remote。

## 触发条件

当用户要求 fork 别人的仓库并 clone 到本地时使用此 skill。

## 输入

用户需要提供目标仓库，格式为 `owner/repo`。

## 执行步骤

1. **Fork 仓库**：使用 `gh repo fork <owner/repo> --clone=false` 将仓库 fork 到 `zc277584121` 账号下。
2. **Clone 仓库**：使用 `gh repo clone zc277584121/<repo>` 将 fork 后的仓库 clone 到本地。
3. **进入项目目录**：`cd <repo>`。
4. **添加 official remote**：`git remote add official https://github.com/<original-owner>/<repo>.git`，用于跟踪上游仓库。
5. **验证 remote 配置**：`git remote -v`，确认 origin 指向自己的 fork，official 指向原始仓库。

## 注意事项

- 如果 fork 已存在，`gh repo fork` 会自动跳过 fork 步骤。
- 始终使用 `official` 作为上游 remote 名称（而非 `upstream`），以保持一致性。
- Clone 完成后向用户报告 remote 配置结果。
