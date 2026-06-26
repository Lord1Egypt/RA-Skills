# Advanced Flows Reference

## Stuck Task Recovery

Run both checks every cron cycle alongside normal task polling.

### Check 1 — Tasks stuck in "working" with a PR deliverable

```bash
curl -sL "${SC_API_URL}/api/tasks/list?status=working" -H "x-api-key: ${SC_API_KEY}"
```

For each working task where:
- `deliverables` contains a PR entry
- `startedAt` exists and is more than 30 minutes ago
- No recent activity signal

→ Auto-rescue by moving to review.

**Idempotency guards:**
1. Skip if task already has an `autoRescuedAt` marker in metadata
2. Skip if thread already contains an auto-rescue message for this task
3. After successful rescue, write `autoRescuedAt=<now>` marker to prevent duplicates

```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/set-review" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${ASSIGNED_AGENT_ID}\", \
      \"result\": \"Auto-rescued: sub-agent completed work but did not transition status.\", \
      \"deliverables\": ${EXISTING_DELIVERABLES}}"
```

Only post thread message if `set-review` actually changed task state to `review`:  
*"Auto-moved to review — sub-agent completed PR but didn't call set-review."*

---

### Check 2 — Tasks marked "done" with an unmerged/open PR

```bash
curl -sL "${SC_API_URL}/api/tasks/list?status=done" -H "x-api-key: ${SC_API_KEY}"
# Filter: completed in last 2 hours AND has a PR deliverable
```

Verify PR is merged:
```bash
# Extract owner/repo from workspace.repoUrl
# Extract PR number from deliverable URL (e.g. https://github.com/org/repo/pull/123 → 123)
curl -sL -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${owner}/${repo}/pulls/${PR_NUMBER}" | grep -o '"merged":[^,]*'
```

If `"merged":false` → the agent skipped review. Re-open for Hawk.

**Idempotency guard:** Search for existing review task referencing this PR in `review|assigned|working` state before creating a new one.

```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/create" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"title\": \"Review PR #${PR_NUMBER}: ${TASK_TITLE}\", \
      \"description\": \"Agent marked task done but PR is still open and unmerged. Please review and merge if approved.\\n\\nPR: ${PR_URL}\", \
      \"assignedAgentId\": \"${REVIEWER_AGENT_ID}\", \
      \"workspaceId\": \"${WORKSPACE_ID}\", \
      \"priority\": \"high\"}"
```

Post to original task thread only when a new review task is created:  
*"⚠️ Task was marked done but PR #N is unmerged. Created review task for Hawk."*

---

## Squad Lead Tasks — Merge & Complete

When the assigned agent has role containing "Lead" or "Orchestrator" AND the task has a PR deliverable, merge the PR to main BEFORE marking complete.

```bash
# 1. Pick up the task
curl -sL -X POST "${SC_API_URL}/api/tasks/pickup" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\"}"

# 2. Detect PR deliverable
# Priority: type === "pr" first, then url containing "/pull/"
# NEVER complete as done if any deliverable has type="pr" OR url containing "/pull/"

# 3. Clone and merge
DEFAULT_BRANCH="${SC_DEFAULT_BRANCH:-${WORKSPACE_DEFAULT_BRANCH:-main}}"
if [ -n "$GITHUB_TOKEN" ]; then
  git -c "credential.helper=!f() { echo username=x-access-token; echo password=${GITHUB_TOKEN}; }; f" clone "$REPO_URL" /tmp/merge-repo
else
  git clone "$REPO_URL" /tmp/merge-repo
fi
cd /tmp/merge-repo
git fetch origin
git checkout "$DEFAULT_BRANCH" && git pull origin "$DEFAULT_BRANCH"
git merge --no-ff origin/task/${TASK_ID} -m "Merge PR #${PR_NUMBER}: ${TASK_TITLE}"
git push origin "$DEFAULT_BRANCH"

# 4. Post to thread
curl -sL -X POST "${SC_API_URL}/api/threads/send" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\", \"content\": \"Merged PR #${PR_NUMBER} to main.\"}"

# 5. Complete
curl -sL -X POST "${SC_API_URL}/api/tasks/complete" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\", \"result\": \"Merged PR #${PR_NUMBER} to main.\", \"status\": \"done\"}"
```

**If merge fails** (conflicts): call `/api/tasks/fail` with the error. Post conflict details to thread. Do NOT force-merge.  
**If no PR deliverable**: complete the task directly without merging.

---

## Creating Tasks Programmatically

Useful for breaking down large tasks into sub-tasks, or creating review tasks:

```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/create" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"title": "...", "description": "...", "assignedAgentId": "...", "workspaceId": "...", "priority": "medium"}'
```

---

## Full Common Mistakes Reference

1. **Marking done without doing work** — Always post results to thread and create a PR (code tasks) before marking complete.
2. **Sub-agent calling /complete instead of /set-review after PR** — Most common violation. PR opened → `set-review` only. Stuck task recovery now auto-catches "done" tasks with open PRs.
3. **Squad Lead skipping merge** — When task assigned to Squad Lead with PR deliverable, merge to main BEFORE marking complete.
4. **Not passing SC_API_URL/SC_API_KEY into spawn prompt** — Sub-agents can't call back without these. Always include.
5. **Ignoring `task.workspace`** — Account-scoped keys embed workspace config per task. Use `task.workspace` when present; only fall back to top-level when absent.
6. **Forgetting to report failure** — Call `/api/tasks/fail`. Tasks stuck in "working" block the queue.
7. **Embedding token in git clone URL** — Use credential helper; never embed token in URL (leaks via process lists, git remotes, logs).
8. **Not pulling latest before branching** — Creates PRs against stale main, causing merge conflicts.
9. **Global concurrency instead of per-workspace** — With account-scoped keys, each workspace has its own limit. Don't count workspace A agents against workspace B's limit.
10. **Posting duplicate blocked status updates** — Check thread before posting; if last message is already a blocked update with no new messages since, do NOT post another.
11. **Loading full thread history unnecessarily** — Use `?limit=N` and `&after=<lastMessageId>` for incremental fetches.

---

## Poll Script Tests

```bash
~/.openclaw/skills/squad-control/scripts/run-tests.sh
```

`POLL_RESULT` envelope schema: `references/poll-result.schema.json`
