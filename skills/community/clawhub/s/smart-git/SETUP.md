# smart-git setup

Place the entire smart-git/ directory under the skills root where the current AI tool loads SKILL.md (the directory name must be smart-git). The config file `smart-commit.host-agent.json` must sit next to SKILL.md. Config resolve uses the copy actually loaded this turn; the host does not have to be one of the products in the table below.

This skill is named **`smart-git`**; the underlying CLI is **`smart-commit-host-agent`** (do not confuse the two).

Package page: https://www.npmjs.com/package/smart-commit-host-agent

## Install paths

Common paths (examples, not an allowlist; other Coding Agents work the same — install under the skills root documented by that tool):

| Tool | Personal skills (example) | Project skills (example) |
|------|---------------------------|--------------------------|
| Cursor | ~/.cursor/skills/smart-git/ | <repo>/.cursor/skills/smart-git/ |
| Claude Code | ~/.claude/skills/smart-git/ | <repo>/.claude/skills/smart-git/ |
| Codex CLI | ~/.codex/skills/smart-git/ | <repo>/.codex/skills/smart-git/ or <repo>/.agents/skills/smart-git/ |
| Other Coding Agent | smart-git/ under that tool's personal / global skills root | smart-git/ under that tool's project skills root |

On Windows, ~ is the user home (for example %USERPROFILE%\.cursor\skills\smart-git\). scripts/*.sh need bash (Git Bash or WSL on Windows).

The same machine may install one copy per tool (each copy may have a different JSON). Scripts always use the copy actually loaded this turn and will not switch copies across tools. To temporarily use a different config, set SMART_GIT_CONFIG.

The directory must contain at least:

- SKILL.md
- HOST_AGENT_LOOP.md
- CONFIG.md
- smart-commit.host-agent.json
- scripts/discover-resolve-script.sh
- scripts/resolve-config.sh
- scripts/with-target-branch.sh

## Install the CLI

Prefer an existing install (need not be global). Use a global binary on PATH, a project-local node_modules binary, an explicit path via SMART_COMMIT_CLI, or a source build. Only when none of those is usable does the skill automatically globally install the package. Requires Node.js >= 20 and smart-commit-host-agent >= 0.1.7. An older install is treated as unusable and gets upgraded by the global install. If that install fails, the skill skips the business flow and will not pretend the CLI is installed.

## Environment variables

Create PR/MR, Review PR/MR, List my PRs/MRs, Batch-review my PRs/MRs, and List my commits need a platform token. If those modes are unconfigured, the Agent stops and guides you to set SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN.
Local Code Review (bridge with --review-only) and config resolve do not need a token; they can run without it.

Set SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN in an environment loaded at shell startup (macOS / Linux: ~/.zshrc or ~/.bashrc then source; Windows: system env var or the current shell). The shell used by the current AI tool must be able to read it.
Do not send the token in the conversation.

GitLab: api scope (create/comment/merge MRs). GitHub: repo or the PR permissions required (set provider to github / auto). Default provider is auto.

## Personal config (diverse needs)

Recommended: edit smart-commit.host-agent.json next to this skill.
Stricter review, switch to GitHub, default assignees/reviewers, a different review skill, disable auto-approve/merge, disable auto-push, etc. all live in that file; you do not need to change SKILL.md.
For a single run, just say the value in the request (e.g. "review this MR, don't auto-merge this time"); the skill passes it as a one-time --set override and leaves the file unchanged. See "One-time overrides by saying it" in CONFIG.md.

Out-of-box defaults (see CONFIG.md):

| Field | Default |
|-------|---------|
| pullRequest.provider | auto |
| commitMessage.validation.protocol | none |
| commitMessage.scope | forbidden |
| pullRequestReview.autoApprove | true |
| pullRequestReview.autoMerge | true |
| pullRequestReview.summarySeverities | ["P0","P1"] |
| myPullRequest.listScope | account |
| pullRequest.remoteHost | empty string |
| myCommit.scope | account |
| myCommit.range | today |
| myCommit.outputFormat | compact |

For a fuller need-to-field map and caveats see CONFIG.md.

Quick lookup:

| Need | Field |
|------|-------|
| Local / Create-PR/MR review threshold | review.threshold (score > to pass; independent of the one below) |
| Existing PR/MR / batch-review threshold | pullRequestReview.threshold |
| Review / commit language | review.language, commitMessage.language |
| Review skill (built-in id / custom file) | review.skill.id, review.skill.path (absolute or relative to repo root), review.skill.promptTuning |
| Commit protocol / extra subject regex | commitMessage.validation.protocol (none/conventional/semantic/gitmoji), pattern (independent of protocol) |
| Require/forbid (scope) on the commit subject | commitMessage.scope (auto/required/forbidden; do not confuse with myPullRequest.listScope; no dedicated CLI flag) |
| Commit skill / draft refinement | commitMessage.skill (path supports absolute or relative to repo root), hybridGenerate (also needs input) |
| Platform (default auto) / self-hosted | pullRequest.provider, apiBaseUrl |
| Account-scope Git host (List / Batch-review / List my commits) | pullRequest.remoteHost (self-hosted also needs pullRequest.provider gitlab / github); myPullRequest.remoteHost is a deprecated fallback |
| List my PRs/MRs (scope / roles) | myPullRequest.listScope, listKinds |
| List my commits (default range / scope / extra author identities / merge commits) | myCommit.range, scope, authorAliases, includeMergeCommits |
| Batch-review my PRs/MRs (role filter) | myPullRequest.batchReviewKinds (default reviewer+assigned; independent of listKinds) |
| MR assignees, reviewers, labels, milestone, draft | pullRequestCreation.assignees, reviewers, labels, milestone, draft |
| MR title/description generation guidance | pullRequestCreation.titlePrompt, descriptionPrompt (non-empty titlePrompt stops overwriting title with a single commit subject) |
| Repo-level create/review overlay | pullRequestCreation.configFilePath, pullRequestReview.configFilePath (absolute / relative, comma-mixable) |
| Extra short instructions for PR/MR review only | pullRequestReview.skillPromptTuning (overrides review.skill.promptTuning) |
| Whether to create an MR after push | pullRequestCreation.autoCreateAfterPush |
| Disable auto-approve / merge | pullRequestReview.autoApprove / autoMerge to false |
| Include P2 in summaries | add P2 to pullRequestReview.summarySeverities |
| Whether to auto commit/push | git.autoCommit, git.autoPush |

The root key must be smartCommitHostAgent.
Do not put a plaintext token in the file; use env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN.

The merge-into branch for Create PR/MR is produced by the skill calling scripts/with-target-branch.sh <config> <target> <Git root> to generate an ephemeral config: it first merges that repo's creation overlay, then writes targetBranch (the CLI has no target-branch flag) and does not rewrite the JSON you maintain long-term.

Temporarily use a different config file by setting SMART_GIT_CONFIG to an absolute path.

## Verify

Run discover-resolve-script.sh, then resolve-config.sh, then config resolve with --config pointing at the resolved file.
Optional: probe the turn protocol with host-agent probe using --session-base and --output json.
On Windows with no TMPDIR, use %TEMP% or Git Bash /tmp.

config resolve succeeding is enough (authToken may be empty). The first probe should return needs_host_agent. Platform modes also need the token already exported.

## Troubleshooting

If config is missing, confirm smart-commit.host-agent.json sits next to SKILL.md in a complete smart-git directory.
Missing SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN: only Create PR/MR, Review, List, Batch-review, and List my commits stop and guide you; Local Code Review continues.
"Could not infer GitHub/GitLab from pullRequest.remoteHost": provider is auto with a self-hosted host; set pullRequest.provider to gitlab or github.
List my commits returns nothing you expected: add the author name / email those commits used to myCommit.authorAliases. complete: false means it stopped early on the rate limit; retry later or raise myCommit.requestDelayMs. Do not send the token in chat.
Stuck on needs_host_agent: write a response JSON with the correct turnId and resume with --session.
Create PR/MR with no target branch: stop and ask (hard gate). Do not run with-target-branch.sh with an empty target, and do not guess main/master/develop.
discover/resolve cannot find the skill: directory name must be smart-git/ with scripts present.
If a diff is truncated or context is too long, raise review.maxDiffChars or split the MR.
Without Node 20+, skip the skill and install a current Node first.
