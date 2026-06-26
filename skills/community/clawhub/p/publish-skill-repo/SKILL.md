---
name: publish-skill
description: 将当前项目中的 Skill 发布到 GitHub 并同步到 ClawHub。新项目自动走完流程，已有仓库的项目会总结变更、确认提交信息和建议版本号。
triggers:
  - 发布skill
  - 上线skill
  - 发布技能
  - 上线技能
  - publish skill
  - deploy skill
---

# Publish Skill

将当前项目中的 Skill 发布到 GitHub 仓库并同步到 ClawHub。

## 前置条件

在执行之前，先检查以下条件是否满足：

1. **当前目录包含 `SKILL.md`** — 如果没有，提示用户这不是一个 skill 项目
2. **gh CLI 已安装且已登录** — 运行 `gh auth status` 验证
3. **ClawHub Token 已配置** — 检查 `~/.clawhub/secret_token` 文件是否存在（如果仓库已有 CLAWHUB_TOKEN secret 则不需要）

如果前置条件不满足，给出具体提示并停止。

## 判断项目类型

检查当前项目状态，判断是 **新项目** 还是 **已有项目**：

- 如果当前目录没有 `.git`，或 git remote 没有指向 GitHub → **新项目**
- 如果当前目录有 `.git` 且 remote 指向 GitHub 仓库 → **已有项目**

## 新项目流程

对于新项目，按以下步骤自动执行：

1. 运行脚本 `scripts/publish-skill-repo.sh <当前目录>` 走完整个流程
2. 脚本会自动完成：git init、创建 LICENSE、创建 workflow、创建 GitHub 仓库、设置 secret、提交推送、创建 v1.0.0 tag
3. 完成后向用户汇报结果

## 已有项目流程

对于已有项目，需要用户确认后再执行：

### 步骤 1：总结变更

检查自上次 tag 以来的变更：

```bash
LATEST_TAG="$(git describe --tags --abbrev=0 2>/dev/null || echo '')"
if [[ -n "$LATEST_TAG" ]]; then
  git log "${LATEST_TAG}..HEAD" --oneline
  git diff "${LATEST_TAG}..HEAD" --stat
else
  git log --oneline -20
  git diff --stat
fi
```

也检查当前是否有未提交的变更：

```bash
git status --short
git diff --stat
```

将变更整理为简洁的中文总结，包含：
- 提交历史摘要
- 修改的文件和主要改动
- 是否有未提交的变更

### 步骤 2：确认提交信息

基于变更内容，生成建议的 commit message。使用 AskUserQuestion 让用户确认或修改：

- 展示建议的 commit message
- 用户可以直接确认，也可以修改

### 步骤 3：确认版本号

基于变更内容判断版本号升级类型：

| 变更类型 | 版本升级 | 示例 |
|---------|---------|------|
| 新功能 / feat | minor | v1.0.0 → v1.1.0 |
| Bug 修复 / fix | patch | v1.1.0 → v1.1.1 |
| 破坏性变更 | major | v1.1.0 → v2.0.0 |
| 仅文档 / chore | patch | v1.1.0 → v1.1.1 |

使用 AskUserQuestion 让用户确认版本号：

- 展示建议的版本号
- 用户可以直接确认，也可以输入自己想要的版本号

### 步骤 4：执行发布

确认完成后，执行以下操作：

1. 如果有未提交的变更，用用户确认的 commit message 提交
2. 如果当前不在主分支，合并当前分支到主分支（主分支通过 `git symbolic-ref refs/remotes/origin/HEAD` 自动检测，兼容 main 和 master）
3. 推送到远程主分支
4. 创建用户确认的 tag 并推送到远程
5. 向用户汇报完成结果

如果是已有仓库但缺少 LICENSE、workflow 或 secret，运行 `scripts/publish-skill-repo.sh <当前目录>` 补齐这些文件，然后再执行发布。

## 脚本说明

`scripts/publish-skill-repo.sh` 是底层自动化脚本，也可以由用户直接运行：

```bash
./scripts/publish-skill-repo.sh /path/to/your-skill [github-owner] [public|private]
```

脚本会自动处理幂等性（跳过已存在的文件和配置），可安全重复运行。
