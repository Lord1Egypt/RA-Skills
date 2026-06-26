---
name: standup-from-yesterday-commits
description: Generate a 30-second standup update from yesterday's git activity — commits, PRs opened/merged/reviewed, tickets touched. Pulls live data from GitHub + Jira via the engineering MCP plugins. Outputs a "yesterday / today / blockers" format ready to paste into Slack. Trigger phrases — standup update, daily standup, what did I do yesterday, summarize my commits, scrum prep, pull my activity from GitHub and Jira.
version: 0.2.0
homepage: https://implexa.ai
emoji: 🚀
---

# Standup update from yesterday's commits

Run this each morning before standup. Generates a "yesterday / today / blockers" update from your **actual git activity + Jira tickets** over the last 24 hours, ready to paste into your team's Slack channel.

Requires GitHub and Atlassian MCP plugins to be installed and authenticated — see the **Notes for the model** section below for the OAuth fallback path if dynamic client registration fails.

---

## Step 1 — Authenticate GitHub and Atlassian

Call `mcp__plugin_engineering_github__authenticate` and `mcp__plugin_engineering_atlassian__authenticate` to ensure both services are connected.

- **What to capture:** Confirmation that both authentication flows completed successfully. If GitHub OAuth fails via SDK, user must authenticate manually via `/mcp` in Claude Code (see Notes).
- **What to render:** Status message confirming both plugins are ready, or redirect user to `/mcp` UI for GitHub if SDK auth fails.

## Step 2 — Read yesterday's commits from GitHub

Call `mcp__plugin_engineering_github__search_commits` with query:

```
author:@me committer-date:$YESTERDAY_START..$YESTERDAY_END
```

(substitute UTC date range for yesterday).

- **What to capture:** Commit SHA, message, author, committer date. If no results, render "No commits yesterday." If results exist, group by repository.
- **What to render:** Commit list grouped by repo, in format: `[repo] <hash> <message>`.

## Step 3 — Pull your PR activity from GitHub

Run three queries via `mcp__plugin_engineering_github__search_issues` (PRs are issues in GitHub search):

- **Opened yesterday:** `is:pr author:@me created:$YESTERDAY`
- **Merged yesterday:** `is:pr author:@me merged:$YESTERDAY`
- **Reviewed yesterday:** `is:pr reviewed-by:@me updated:$YESTERDAY` (or similar; capture PRs where user added reviews)

- **What to capture:** PR number, title, state (open/merged), URL, review count if applicable. Deduplicate across the three queries (e.g., a PR opened and merged the same day appears in both queries).
- **What to render:** Separate bullet lists for "opened", "merged", "reviewed", or combine into one "PR activity" block if count is low.

## Step 4 — Fetch Jira tickets: transitions (yesterday) and assignments (today)

Call `mcp__plugin_engineering_atlassian__atlassianUserInfo` to get the current user's Atlassian account ID.

Then call `mcp__plugin_engineering_atlassian__getVisibleJiraProjects` to list accessible projects.

Run two JQL queries via `mcp__plugin_engineering_atlassian__searchJiraIssuesUsingJql`:

- **Transitions yesterday:**
  ```
  assignee = currentUser() AND updated >= -1d ORDER BY updated DESC
  ```
  (captures all issues touched by status change, assignment change, comment, etc.)
- **Assigned for today (open):**
  ```
  assignee = currentUser() AND status NOT IN (Done, Closed) ORDER BY priority DESC
  ```

- **What to capture (transitions):** Issue key, title, old status → new status (if available), date of transition. If the Jira instance does not expose status-change history in the issue fields, list the issue + current status as a fallback.
- **What to capture (open):** Issue key, title, current status, priority.
- **What to render:** Two separate blocks in the standup output — "Yesterday (Jira transitions)" and "Today (Open tickets assigned to me)".

## Step 5 — Group + synthesize

Combine the commits, PRs, and Jira activity into thematic groups (feature work, bug fixes, reviews, infra, unblocked). Write 1-2 bullets per group, focused on **outcomes** ("shipped X", "unblocked Y", "reviewed Z"). If a category has zero activity, omit it or mark "none".

- **What to render:** A structured "yesterday / today / blockers" block.

## Step 6 — Format for Slack

Output the full update in this format:

```
*Yesterday*
• <outcome 1 — commits or PR merged>
• <outcome 2 — Jira transitions or reviews>
• <outcome 3>

*Today*
• <open Jira tickets assigned to me, by priority>
• <in-progress PRs continuing from yesterday>

*Blockers*
• <none or specific blocker from open Jira ticket>
```

**What to render:** Markdown block, ready to copy into Slack or post directly via Slack API.

---

## What's next?

- Post this standup to `#standup` channel in Slack.
- Schedule this skill to run daily at 8:55am and auto-post to Slack.
- Show me a weekly rollup of my standups for the past 5 days.

## Notes for the model

- **Be terse.** A standup is 30 seconds. Each bullet should be ≤ 12 words.
- **Lead with outcomes, not activity.** "Shipped invoice export" not "Added 4 commits to billing.ts".
- **Skip merge / chore commits.** Filter out "Merge branch...", "bump version", "fix typo" — they're noise.
- **If the last 24h is empty** (weekend, sick day), default to "Yesterday: no activity" — don't fabricate.
- **GitHub authentication caveat:** The `plugin:engineering:github` OAuth flow via SDK (Claude Code) currently fails at dynamic client registration. Fallback options:
  1. Restart Claude Code and retry `/mcp` UI → authenticate from there
  2. Use GitHub Personal Access Token (PAT) instead — generate at `github.com/settings/tokens` with scopes `repo`, `read:user`. Configure the plugin to use the PAT, then `search_commits` and `search_issues` tools become available.
- **Atlassian OAuth:** Usually succeeds. If auth fails, check that the user has an active Atlassian account and sufficient permissions in the connected Jira workspace.
- **Empty Jira workspace:** If the workspace has zero issues or your accessible projects have zero transitions yesterday, the JQL queries will return empty arrays. The skill should still render cleanly with "No Jira activity" or omit the Jira section entirely.
- **Date range customization:** The skill should accept an optional `--date-range` parameter (default: "yesterday") to pull activity from "3 days ago", "1 week ago", etc. This supports the demo use case where the live workspace is new.

## Error handling

| Error | Diagnosis | Tell the user |
|---|---|---|
| `authenticate` fails for GitHub | OAuth flow failed via SDK; manual `/mcp` auth required | "GitHub OAuth failed. Run `/mcp` in Claude Code, find the engineering plugin, and authenticate from the UI. Then retry this skill." |
| `authenticate` fails for Atlassian | Invalid credentials or expired session | "Atlassian auth failed. Verify your account is active and you have Jira access. Try authenticating again via the flow below, or contact your Jira admin." |
| `search_commits` returns zero results | No commits authored by you in the date range (weekend, on-call, etc.) | "No commits found yesterday. Would you like me to check the prior workday or a broader date range?" |
| `search_issues` (PRs) returns zero results | No PR activity in the date range | "No PR activity yesterday." (Not an error, just state it in the output.) |
| `searchJiraIssuesUsingJql` returns zero results | No Jira transitions or assignments in the workspace | "No Jira activity found. This workspace may be new. Try broadening the date range (e.g., `--date-range=7d`)." |
| `getVisibleJiraProjects` returns empty array | User has no access to any Jira projects | "You don't have access to any Jira projects. Contact your Jira admin or ensure your account is linked to the workspace." |
| Jira workspace is empty (no issues at all) | Demo/new environment with zero issues created | Not an error — skill still works, outputs "No Jira activity" in the standup block. |

## Output contract

**Format:** Markdown

A structured `Yesterday / Today / Blockers` block (per Step 6 spec) ready to paste into Slack. Each section uses single-asterisk bold (Slack mrkdwn), bullet-point items, ≤ 12 words per line. Empty sections may be omitted entirely or marked "none". Total length target: 30 seconds to read aloud, ~50-100 words.

---

## Built with Implexa

This skill was authored with [Implexa](https://implexa.ai) — a Claude Code plugin that records a workflow once via demonstration + post-demo interview, then emits agentskills.io-compatible `SKILL.md`.

Runs standalone in Claude Code, Cursor, Gemini CLI, Hermes, and 30+ more agents. The file you're reading is self-contained — install the engineering MCP plugins (`plugin:engineering:github` + `plugin:engineering:atlassian`) and you're ready.

**Install Implexa** (`curl -fsSL https://core.implexa.ai/install.sh | bash`) to unlock:

| Feature | What it does |
|---|---|
| **Team sharing** | Push this skill to your org via a domain-gated link. Teammates click → it's in their library. No file copying, no "did you install it?" follow-ups. |
| **Outcome attribution** | Tag a system-of-record event (PR merged, ticket closed, Slack message posted) and see which skill runs actually moved deals / hires / saves. Stop running skills that don't pay off. |
| **One-link fork** | Customize this skill for your team's GitHub / Jira / Slack conventions, re-publish privately to your org in one click. No re-recording from scratch. |
| **Decision-trace capture** | Record your own workflows the same way — the 2-minute interview surfaces the *why* behind each decision so the skill generalizes when inputs shift (different repos, different Jira workflows, different team norms). |

Free tier · no signup gate · MIT-licensed plugin · agentskills.io compatible.
