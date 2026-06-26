---
name: git-commit-pr
description: Commit changes and create a pull request to the official upstream repo
allowed-tools:
  - Bash
---

# Git Commit & PR

提交改动并向 official（上游）仓库创建 Pull Request。

## 触发条件

当用户要求提交改动并给原始仓库（official）提 PR 时使用此 skill。

## 执行步骤

1. **创建新分支**：`git checkout -b <branch-name>`，分支名由用户指定或根据改动内容自动生成。

2. **Review 改动**：先用 `git status` 和 `git diff` 自行检查所有改动，确保没有把临时文件、调试代码或不相关的文件混进来。

3. **暂存文件**：`git add` 相关改动文件。不要使用 `git add -A` 或 `git add .`，而是逐个添加相关文件。

4. **提交改动**：
   ```bash
   git commit --signoff --author="Cheney Zhang <chen.zhang@zilliz.com>" -m "<commit message>"
   ```
   - commit message 用英文编写，简洁描述改动内容。
   - **绝对不要**在 commit message 中提及 AI、Claude、LLM 或任何自动生成相关的字样。

5. **推送分支**：`git push origin <branch-name>`。

6. **创建 PR**：
   ```bash
   gh pr create --repo <official-owner/repo> --title "<PR title>" --body "<PR description>"
   ```
   - PR 标题和描述用英文编写。
   - **绝对不要**在 PR 标题或描述中提及 AI、Claude、LLM 或任何自动生成相关的字样。
   - 不要添加 `Co-Authored-By` 之类的 AI 相关标记。

7. **如果用户有合并权限且要求合并**：
   - Review PR 并合并。
   - 切回主分支（main 或 master）。
   - 同步上游：`git fetch official && git reset --hard official/<main-branch>`。
   - 删除本地临时分支：`git branch -d <branch-name>`。
   - 删除远端临时分支：`git push origin --delete <branch-name>`。

## 注意事项

- 先确认 `official` remote 存在，如果不存在则提示用户先配置。
- 提交前检查是否有未暂存的改动需要处理。
- 所有对外可见的文本（commit message、PR 标题/描述）都不能出现任何 AI 相关字样。
