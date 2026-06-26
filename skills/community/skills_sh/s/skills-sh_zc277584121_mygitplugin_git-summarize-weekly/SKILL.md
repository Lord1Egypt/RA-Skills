---
name: git-summarize-weekly
description: Summarize weekly GitHub contributions for writing weekly reports
allowed-tools:
  - Bash
---

# Git Summarize Weekly

总结本周的 GitHub 贡献，输出适合写入周报的英文摘要。

## 触发条件

当用户要求总结本周 GitHub 贡献、写周报或查看本周工作时使用此 skill。

## 执行步骤

1. **计算日期范围**：计算本周一的日期到今天。使用 `date` 命令计算。

2. **拉取 GitHub events**：
   ```bash
   gh api users/zc277584121/events --paginate --jq '.[]'
   ```
   获取用户近期的 GitHub 活动事件。

3. **过滤和分析**：
   - 过滤出本周时间范围内的事件。
   - **默认排除** `zc277584121` 自己账号下的仓库，只保留对他人仓库的贡献。
   - 如果用户明确要求包含自己的仓库，则不排除。
   - 关注以下事件类型：
     - `PushEvent`：代码推送
     - `PullRequestEvent`：PR 创建/合并
     - `PullRequestReviewEvent`：PR Review
     - `IssuesEvent`：Issue 创建/关闭
     - `IssueCommentEvent`：Issue 评论
     - `CreateEvent`：分支/标签创建

4. **输出格式**：
   - **必须用英文输出**，适合直接抄写到周报中。
   - 大的 feature 或重要 PR 单独一条列出，简要说明做了什么。
   - 小的修复、review、评论等可以合并为一条。
   - 按仓库分组，格式简洁清晰。
   - 示例格式：
     ```
     ## Weekly Contributions (2025-01-20 ~ 2025-01-24)

     ### milvus-io/pymilvus
     - Implemented hybrid search API with support for multiple vector fields (#xxx)
     - Fixed connection pool timeout issue (#xxx)
     - Reviewed 3 PRs related to batch insert optimization

     ### milvus-io/milvus
     - Minor: commented on 2 issues about memory management
     ```

## 注意事项

- GitHub Events API 最多返回最近 90 天、300 个事件的数据。
- 如果某一周活动特别少，如实报告即可。
- 输出要简洁实用，直接可以粘贴到周报中。
