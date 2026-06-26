---
name: git-get-notification
description: Check GitHub notifications and recent Issues/PRs for monitored repos
allowed-tools:
  - Bash
---

# Git Get Notification

Check GitHub notifications, recent Issues, and recent PRs for a set of monitored repositories.

## Trigger

When the user asks to check notifications, see what's new, or check updates on monitored repos.

## Monitored Repos

- `zilliztech/claude-context`
- `zilliztech/memsearch`
- `zilliztech/mcp-server-milvus`
- `langchain-ai/langchain-milvus`
- `milvus-io/milvus-haystack`
- `zilliztech/milvus-marketplace`
- `zilliztech/vector-graph-rag`

## Execution Steps

### Step 1: Determine Target Repos

- If the user specifies a particular repo (e.g., "check mcp-server-milvus"), only query that repo. Match by partial name against the monitored list.
- If no repo is specified, query all monitored repos.

### Step 2: Fetch GitHub Notifications

For each target repo, fetch unread notifications:

```bash
gh api notifications --jq '[.[] | select(.repository.full_name == "REPO_NAME")] | sort_by(.updated_at) | reverse'
```

Classify notifications by reason into two priority tiers:

**High Priority (show first, with details):**
- `mention` - Someone @you
- `review_requested` - Review request
- `assign` - Assigned to you

**Medium Priority (show after high priority):**
- `author` - Updates on your PR/Issue
- `state_change` - Status changes (merged/closed)
- `comment` - New comments on your threads

Skip `subscribed` and `CheckSuite` notifications — these are noise.

### Step 3: Fetch Recent Issues

For each target repo, fetch issues created in the last 7 days:

```bash
gh api "repos/REPO_NAME/issues?state=all&sort=created&direction=desc&per_page=20&since=SEVEN_DAYS_AGO_ISO" --jq '[.[] | select(.pull_request == null)]'
```

- Use `date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ` to compute the since date.
- If a repo has more than 10 recent issues, show only the 10 most recent and note how many were omitted.
- **Skip closed issues** — only show open issues.

### Step 4: Fetch Recent PRs

For each target repo, fetch PRs updated in the last 7 days:

```bash
gh api "repos/REPO_NAME/pulls?state=all&sort=updated&direction=desc&per_page=20" --jq '[.[] | select(.updated_at >= "SEVEN_DAYS_AGO_ISO")]'
```

- If a repo has more than 10 recent PRs, show only the 10 most recent and note how many were omitted.
- **Skip merged and closed PRs** — only show open PRs.

### Step 5: Output Format

Output in Chinese. Group results by repo. Within each repo, display in this order:

```
## 📋 通知概览

### zilliztech/mcp-server-milvus

#### 🔴 高优先级通知
- [review_requested] PR #42: Add new endpoint - @someone 请求你 review (2h ago)
- [mention] Issue #38: Bug report - @someone 在评论中提到了你 (5h ago)

#### 🟡 中优先级通知
- [author] PR #40: Your PR title - 已合并 (1d ago)
- [comment] Issue #35: Discussion title - 3 条新评论 (3h ago)

#### 📝 最近 Issues (近 7 天，共 N 条)
- #50 [open] Issue title (2h ago) by @user
- #49 [closed] Issue title (1d ago) by @user

#### 🔀 最近 PRs (近 7 天，共 N 条)
- #48 [open] PR title (3h ago) by @user
- #47 [merged] PR title (2d ago) by @user

---
### next repo...
```

- Show relative time (e.g., "2h ago", "3d ago") for readability.
- If a repo has zero notifications, zero issues, and zero PRs in the last 7 days, show "✅ 暂无新动态" and move on.
- At the end, show a summary line: "共 X 条高优先级通知，Y 条中优先级通知，Z 条新 Issue，W 条新 PR"

## Notes

- All queries use `gh api` which requires `gh` CLI to be authenticated.
- Do NOT mark any notifications as read.
- The 7-day window is the default. If the user asks for a different time range (e.g., "this month"), adjust accordingly.
- Keep output concise. If data is overwhelming, prioritize recency and importance.
