---
name: smart-git
description: >-
  Use the smart-commit-host-agent CLI for local code review, creating a PR/MR, reviewing an existing PR/MR, listing my open PRs/MRs, batch-reviewing my PRs/MRs, or listing my own commits for a date range. Triggers: create MR / create PR / create pull request / open a PR / submit and create MR; review MR / review PR plus a PR/MR URL; list my MRs / list my open PRs / my MR list / my-pull-request list; batch review my MRs / batch-review my PRs / my-pull-request batch-review; list my commits / my commits today / my commits this week / what did I commit / my-commit list; local code review / local review of changes / local review diff / smart-git local review. Do not use for ordinary code review / review code without the word local. Must read this SKILL.md first. CLI task flow plus Host-Agent turn loop only; do not use gh for GitLab; no manual commit/push/API; do not edit business source based on review.
---

# smart-git

Via the CLI **`smart-commit-host-agent`** (>= 0.1.7), six mutually exclusive modes are supported. After entering, route the mode first; do not mix commands.

| Mode | CLI | Purpose |
|------|-----|---------|
| **Local Code Review** | bridge --review-only | Review local changes; no commit / push / create PR/MR |
| **Create PR/MR** | bridge / pull-request create | Review then commit, push, create PR/MR (or resume from a breakpoint) |
| **Review PR/MR** | pull-request review url | Review an existing GitHub PR / GitLab MR |
| **List my PRs/MRs** | my-pull-request list | List open PRs/MRs for the current account/workspace; no review, no commit |
| **Batch-review my PRs/MRs** | my-pull-request batch-review | List open PRs/MRs by batchReviewKinds, then review them serially (includes platform publish actions; requires Host-Agent turns) |
| **List my commits** | my-commit list | List commits I authored on GitHub/GitLab for a date range; no review, no commit, no turn |

This CLI obtains model text via Host-Agent turns: when it returns status "needs_host_agent" (exit 10), this Agent must write the turn response file and resume with --session. See [HOST_AGENT_LOOP.md](HOST_AGENT_LOOP.md).
Exception: my-pull-request list and my-commit list have no turn and do not need the Host-Agent loop. my-pull-request batch-review has turns (same path as a single pull-request review).

Do not: edit business source based on review comments; switch Git branches; manually git commit / git push / fall back to platform APIs; silently turn a list-my-MRs result into batch-review (the user must explicitly trigger batch review); silently turn a list-my-commits result into a report, review, or MR.

This skill runs independently: it does not call or hand off to other skills.

Behavior is configurable: review threshold, review skill, commit message, Git auto-commit/push, PR/MR platform, assignees/reviewers/labels/milestone/draft, review comments and approve/merge, etc. are all controlled by the colocated smart-commit.host-agent.json. Out-of-box defaults: pullRequest.provider=auto; commitMessage.scope is forbidden; commitMessage.validation.protocol is none; pullRequestReview.autoApprove / autoMerge are true; summarySeverities is ["P0","P1"]; myPullRequest.listScope=account; myCommit.scope=account; myCommit.range=today; pullRequest.remoteHost="" (empty; shared by List / Batch-review / List my commits; if empty, ask before listing against public gitlab.com/github.com for self-hosted GitLab; myPullRequest.remoteHost is a deprecated fallback). Users adapt by editing that file; no skill changes required. A value stated in the request itself ("no auto-merge this time", "threshold 8") overrides the file for that run only (shared prerequisite 4.1). review.skill / commitMessage.skill are host-agent built-in templates, not other agent skills. See [CONFIG.md](CONFIG.md) and [SETUP.md](SETUP.md).

At these times, the Agent should remind the user in one or two sentences that they can edit this config (do not paste the full JSON, do not restate the token):

- This turn skipped / CONFIG_ERROR for a config-related reason (when it is not a missing token, you may point at the specific field docs)
- The user asks whether they can change the threshold / disable auto-merge / set assignees / switch to GitHub / require commit scope, etc. (also mention they can just say it in the request for a one-time override)
- After a successful Create PR/MR / Review / List my PRs/MRs / Batch-review my PRs/MRs / List my commits summary (optional one-liner)

When showing that reminder, write it as a clickable Markdown link using the absolute path of the effective skill directory (SKILL_DIR comes from config resolve / the skill copy read this turn), for example:

    Tip: edit [smart-commit.host-agent.json]({SKILL_DIR}/smart-commit.host-agent.json) to adjust the review threshold, review skill, commit message, Git flow (auto-stage/commit/push), auto-approve/merge, assignees/reviewers, and more. See [CONFIG.md]({SKILL_DIR}/CONFIG.md) for field docs.

Keep the [filename]({SKILL_DIR}/...) structure at the end of each mode summary so the files are clickable; do not use a bare filename or a backtick-wrapped filename only.

## Mode routing (highest priority)

| User message | Mode |
|--------------|------|
| Hits keywords for more than one mode at once (local / review MR / create MR / list my MRs / batch-review / list my commits). A batch-review phrase is not also Review PR/MR just because it contains "review" | Stop and ask |
| Local Code Review keywords | Local Code Review |
| Batch-review my PRs/MRs keywords | Batch-review my PRs/MRs (will serial-review and may approve/merge) |
| List my PRs/MRs keywords | List my PRs/MRs (does not review) |
| List my commits keywords | List my commits (does not review, commit, or create MRs) |
| Review MR keywords plus URL | Review PR/MR |
| Create MR keywords only | Create PR/MR |
| Only cites this skill, semantics unclear | Ask |

Local keywords (any one): `local\s*code\s*review`, `local\s*review\s*(of\s*)?(changes|diff)`, `smart-git.*local\s*review`.

Batch-review my PRs/MRs keywords (any one): `batch[\s-]*review\s*(my\s+)?(open\s+|pending\s+)?(MRs?|PRs?|pull\s*requests?)`, `my-pull-request\s*batch-review` (case-insensitive).
Must include batch or batch-review semantics; do not treat list my MRs / my pending MRs alone as batch review; do not treat review MR plus a single URL as this mode (that is single-item review).

List my PRs/MRs keywords (any one): `list\s*my\s*(open\s+|pending\s+)?(MRs?|PRs?|pull\s*requests?|merge\s*requests?)`, `my-pull-request\s*list`, `my\s*(open\s+|pending\s+)?(MR|PR)\s*list`, `list\s*(open\s+|pending\s+|created\s+|assigned\s+)?(MRs?|PRs?)`, `list\s*(MRs?|PRs?)\s+I\s+created` (case-insensitive).
Do not treat a message that only contains review MR plus a URL as list; list mode does not publish comments/approve/merge.
If the same message hits both list and batch-review, or contains both list and batch-review wording (e.g. list and batch-review my MRs), stop and ask.

List my commits keywords (any one): `list\s*my\s*(own\s+)?(recent\s+)?commits?`, `my-commit\s*list`, `my\s+(own\s+)?commits?\s+(for\s+|from\s+|in\s+|since\s+)?(today|yesterday|this\s+week|last\s+week|this\s+month|last\s+month|the\s+last\s+\d+\s+days)`, `what\s+(did|have)\s+I\s+commit(ted)?`, `show\s+(me\s+)?my\s+commits?` (case-insensitive).
Must refer to commits I authored (my commits); the bare word commit / commit message does not trigger this mode (Create PR/MR commits as a step). Do not treat list my MRs / list my PRs as this mode. If the same message also hits list my MRs / batch-review / create MR, or asks to list commits together with MRs/PRs (e.g. list my commits and MRs, which the list-my-MRs regex alone misses), stop and ask.

Review MR keywords (any one): `review\s+(my\s+|an?\s+|the\s+|this\s+)?(open\s+)?(MR|PR)`, `MR\s*review`, `PR\s*review`, `review\s+(an?\s+|the\s+|this\s+)?(merge\s*request|pull\s*request)` (case-insensitive) plus a parseable URL.
Do not treat a message that already matches batch-review keywords as this mode, even if it contains the word review and pull request / merge request (that is Batch-review my PRs/MRs).

Create MR keywords (any one): `create\s*(a\s+|an\s+|new\s+)?(MR|PR)`, `create\s+(a\s+|an\s+|new\s+)?(merge\s*request|pull\s*request)`, `open\s+(a\s+|an\s+|new\s+)(MR|PR)`, `open\s+(a\s+|an\s+|new\s+)?pull\s*request\b`, `submit\s*(and\s*)?(create\s*)?(MR|PR)`.
Do not treat adjective "open" as Create (list my open MRs / review my open PR / batch-review my open PRs are not Create).

Ordinary code review / review code (without local) does not trigger this skill. "review MR" / "review PR" plus a URL still is Review PR/MR.

---

## Host-Agent turn loop (mandatory for all AI commands)

For commands that issue turns — bridge / pull-request create / pull-request review / my-pull-request batch-review (not my-pull-request list / my-commit list):

loop:
  run {CLI prefix} cmd ... --output json
  if status == "needs_host_agent" (exit 10):
    1. Read requestPath (turns/NNNN.request.json)
    2. Produce this turn's content from messages + responseSchema + purpose
    3. Write sessionPath/turns/{turnId}.response.json
       shape: turnId same as request, content is always a string. code-review / pr-content: JSON.stringify into content. commit-message: plain text, not a JSON object
    4. Resume the same command: drop --session-base, pass --session sessionPath instead (never pass both). Do not start a new first-run command without a session
  else finish (passed | blocked | error | created | ok | ...)

| purpose (common) | content shape |
|------------------|---------------|
| code-review or code-review:<url> | JSON string: score, decision, summary, details[]. batch-review often suffixes each MR's purpose with the URL. Follow Review skill guidance and Detected diff domain in the request; when PR/MR review includes line-number annotations, lineNumber must copy the visible number |
| commit-message | Commit message as plain text. Follow the request language / structure / protocol / scope / skill; when User draft is present (hybridGenerate), refine the draft, do not discard it. subjectOnly outputs a single line. Typed subject: scope=required must be type(scope): (missing scope fails immediately, no correction turn); forbidden must not include (scope) (CLI strips it, no second turn); auto is optional. Gitmoji / non-typed are unchanged. Do not confuse with myPullRequest.listScope. |
| pr-content | JSON string: title, description (bridge issues this turn after push, before creating the MR; do not paste the commit message as the description). Follow Title/Description prompt tuning in the request. When titlePrompt is non-empty, the CLI will not overwrite title with a single commit subject; only when titlePrompt is empty and there is exactly 1 commit relative to target does the CLI overwrite with that commit subject |

Allowed: read the request, write the session response file, parse CLI JSON.
Forbidden: Write/StrReplace business source based on this; use gh prefetch instead of pull-request review; skip the turn and pretend it passed.

Default --session-base: ${TMPDIR:-/tmp}/scha-sessions (on Windows with no TMPDIR, use %TEMP% or Git Bash /tmp).

---

## Shared prerequisites (all six modes)

### 1. Config resolve

smart-commit.host-agent.json is colocated with SKILL.md. The bash resolve-config.sh path lookup may run immediately. The CLI command config resolve waits until Node and the CLI prefix are ready (section 2); do not run the CLI before that.

    SKILL_DIR="<directory of the smart-git/SKILL.md read this turn>"
    DISCOVER="${SKILL_DIR}/scripts/discover-resolve-script.sh"
    RESOLVE_SCRIPT="$(bash "${DISCOVER}")" || exit
    SMART_GIT_CONFIG="$(bash "${RESOLVE_SCRIPT}")" || exit
    test -f "$SMART_GIT_CONFIG"

SMART_GIT_CONFIG may override explicitly. The summary must record the config source (absolute path, no secrets). Installation: [SETUP.md](SETUP.md).
The resolve scripts require bash; on Windows run them in Git Bash / WSL or an Agent shell that already provides bash.
Always use the config from the skill directory read this turn; do not switch to a copy in another tool's directory. To use a different JSON, set SMART_GIT_CONFIG.

### 2. Node and CLI

Use an existing usable install if present. Auto-install globally only when none is found.
Order is fixed: ensure Node >= 20, resolve a usable CLI by priority, globally install the package only if every probe fails, then run business commands.
The summary must record Node version, chosen CLI prefix and source (PATH / project-local / explicit path / global install this turn), and version output.
If a global install, a project dependency, or a locally built binary already runs with the required subcommands, use it as-is and do not install.

#### 2.1 Node >= 20

Check node -v; major version must be >= 20.
If not, in the same shell session switch to an installed 20+ (nvm / fnm / asdf / mise / volta; prefer project .nvmrc / .node-version if already >= 20), then re-check.
If this machine has no Node >= 20 at all, skip the whole skill. Summary: skipped, did not run bridge / pull-request. Reason: Node.js >= 20 not found. Do not run the CLI with Node below 20.

#### 2.2 Probe existing installs (high to low, stop on first hit)

After Node is ready, probe in this order and stop on first usable prefix whose help includes the current mode's subcommands:
1. SMART_COMMIT_CLI if set and executable.
2. smart-commit-host-agent on PATH.
3. node_modules/.bin/smart-commit-host-agent under the Git root or cwd (project-local, not global).
4. An executable path given in the user message (local checkout build).

Any candidate succeeds: freeze that CLI prefix, record the source, do not run 2.3.
All fail: go to 2.3.

Mode help requirements: Local needs bridge and --review-only. Create PR/MR needs bridge; breakpoint resume also needs pull-request create. Review PR/MR needs pull-request review. List needs my-pull-request list. Batch-review needs my-pull-request batch-review. List my commits needs my-commit list.
Every mode also requires CLI >= 0.1.7: --version must print 0.1.7 or later. Older CLIs silently ignore pullRequest.remoteHost and myCommit in the JSON (a self-hosted host would quietly fall back to the public host), may lack --set, and require --repo for pull-request review, so an older candidate counts as a miss; the global install in 2.3 then upgrades to the latest package.

#### 2.3 When nothing is found: default automatic global install

Run only when 2.2 missed all candidates (do not ask the user whether to install): globally install package smart-commit-host-agent.
After install, re-check the global command on PATH (exists, version, help). If recheck passes and subcommands are complete, prefix is smart-commit-host-agent; note auto global install this turn, then continue. Recheck fails: go to 2.4.

Forbidden: forcing a global install when 2.2 already found a usable CLI; forging an unverified path after a failed install; hiding an install failure; using elevated privileges for global install unless the user explicitly asked this turn.

#### 2.4 Install or environment failure: skip

Skip the whole skill (do not enter config resolve / bridge / pull-request) if: no Node >= 20; 2.2 all missed and registry/network failed; 2.2 all missed and permission failed; command still unavailable after global install.
Summary must say skipped, what was probed (SMART_COMMIT_CLI / PATH / project node_modules), what was tried, and that the skill did not pretend it is installed.

### 3. Environment probes

| Check | Requirement |
|-------|-------------|
| Node | Major version >= 20 (see 2.1; may auto-switch) |
| CLI | 2.2 resolved a usable prefix, or automatic global install this turn succeeded |
| Platform token | Only Create PR/MR / Review PR/MR / List / Batch-review / List my commits need it (see 3.1). Local Code Review does not |
| Config | resolve-config.sh plus config resolve succeeded |

#### 3.1 Platform token (validate by mode)

| Mode | Needs pullRequest.authToken? |
|------|------------------------------|
| Local Code Review (bridge --review-only) | No. Even if SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN is unset, continue config resolve and the business CLI |
| config resolve (prerequisite of any mode) | No. The CLI resolves missing env: refs to empty and does not CONFIG_ERROR for that |
| Create PR/MR, Review PR/MR, List my PRs/MRs, Batch-review my PRs/MRs, List my commits | Yes. Calls GitHub/GitLab APIs |

The colocated config still writes pullRequest.authToken: "env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN".

Modes that do not need a token: skip the env check below and go straight to config resolve / the business CLI.

Modes that need a token: before config resolve / the business CLI, if SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN is unset or empty: stop immediately; do not guess a token, copy secrets from files/chat, or ask the user to paste a token into the conversation; guide the user to configure SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN (GitHub PAT or GitLab Personal Access Token) so the shell used by the current AI tool can read it. Local Code Review does not need this token.

Permission suggestions (default provider is auto): GitLab api (or enough to create/comment/merge MRs; read_api is enough for List my commits alone); GitHub repo (private repos) or the PR permissions needed for public repos.
After configuring, the user can say create MR / review MR / list my MRs / batch-review my MRs / list my commits again. Do not send the token in the conversation.

Summary must say Skipped (waiting for SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN); do not phrase it as a CLI/review failure.
If config resolve still reports CONFIG_ERROR because of other env refs, guide by field and stop. Treat every authToken in output as sensitive; do not paste it to the user (including redacted).
If JSON points authToken at a variable name that does not exist in the current shell, and this turn is a token-required mode: offer two options — change authToken back to env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN, or write that variable into the shell config so the current AI tool's shell can read it, then re-trigger.

Run: {CLI prefix} config resolve --config "$SMART_GIT_CONFIG" optionally --repo Git-root, plus the same --set flags this turn will use (shared prerequisite 4.1), so invalid overrides fail early and the resolved values reflect them.

When this mode later runs bridge / pull-request at a Git root, config resolve must pass the same --repo (relative configFilePath overlays resolve relative to the repo root; absolute paths are probed as-is). Account-scoped List my PRs/MRs / List my commits that does not read a local repo may omit --repo.

### 4. Config takes precedence / targetBranch

host-agent has no target-branch flag. For Create PR/MR, generate a temporary config with the script:

    RUNTIME_CONFIG="$(bash "${SKILL_DIR}/scripts/with-target-branch.sh" "$SMART_GIT_CONFIG" "<MR target branch>" "<Git root>")"
    then --config "$RUNTIME_CONFIG"

The script merges that repo's pullRequestCreation.configFilePath overlay using CLI rules, then writes the conversation-specified targetBranch, and clears configFilePath in the temp config (so the CLI does not load the overlay a second time and overwrite the target). One RUNTIME_CONFIG per Git root.

Except --repo, --config, --session / --session-base, --review-only, breakpoint resume --no-commit / --no-push, --output, user-explicit dry-run, a --commit-message the user clearly gave this turn, the --my-pull-request-* overrides allowed for List / Batch-review, the --my-commit-* and --start-date / --end-date overrides allowed for List my commits, --pull-request-remote-host for a host the user named this turn (List / Batch-review / List my commits only), and --set overrides derived from the user's words (4.1), do not pass flags that would override config such as --provider / --pull-request-provider / --pull-request-api-base-url / --pull-request-auth-token (the token only goes through the env var plus config env: ref; a platform switch the user asks for goes through --set=pullRequest.provider=...).

### 4.1 One-shot config overrides from the user's words

When the user's message this turn states a config value in natural language, apply it to this run only with the CLI's generic --set flag. Never edit smart-commit.host-agent.json for this; the next request goes back to the file unless the user restates the value. If the user wants it permanent, point them at the JSON field instead.

Form: one token per field, --set=path=value, where path is the dotted field under smartCommitHostAgent (same names as CONFIG.md). Quote the whole token when the value has spaces or JSON, e.g. '--set=pullRequestCreation.titlePrompt=Use a Chinese title'. Values: numbers; true / false; plain text; arrays as a comma list (--set=pullRequestCreation.reviewers=alice,bob) or JSON; an empty value clears an array.

Rules:
- Only translate explicit values or unambiguous switches ("no auto-merge this time", "threshold 8", "review in English", "create as draft", "reviewers alice and bob", "use GitHub"). A vague wish without a value ("review more strictly") -> ask once for the value; do not invent one
- Map by mode when a word is shared: threshold -> review.threshold in Local Code Review / Create PR/MR, pullRequestReview.threshold in Review PR/MR / Batch-review; language of the review -> review.language; language of the commit message -> commitMessage.language
- Prefer the dedicated flag where this skill already uses one: --dry-run, --commit-message, --my-pull-request-*, --my-commit-*, --start-date / --end-date, --pull-request-remote-host. Create PR/MR target branch still goes through with-target-branch.sh. List my commits summary style (outputFormat) is chosen from the user's words directly. Everything else uses --set
- Forbidden: pullRequest.authToken and any *.configFilePath (the CLI rejects them); never put a token on the command line
- Skip fields the mode cannot use (e.g. git.autoPush in Local Code Review, which never commits) and say so in the summary instead of passing them
- Pass the same --set flags to config resolve, the first run, and every --session resume of that command
- Where this skill itself reads a config value to decide what to do (pullRequestCreation.skipBranches, autoCreateAfterPush, targetBranch, myPullRequest kinds, myCommit fields), use the overridden value
- Dedicated CLI flags beat --set for the same field, and --set beats repo overlays and the JSON file
- Every summary lists the overrides applied this run (field = value), or says none

CLI support: --set is part of the >= 0.1.7 requirement in 2.2. Never drop overrides silently.

pullRequestReview.configFilePath is loaded automatically by the CLI in config resolve / pull-request review / batch-review (comma-separated, first existing file; absolute paths as-is, relative paths relative to the repo root when --repo is present). The Agent must not manually read/merge overlay files. Review overlays must not contain configFilePath. Creation-overlay merge only goes through with-target-branch.sh; do not hand-edit the temp JSON afterwards.

If pullRequestReview.configFilePath is a relative path: CLI config resolve, pull-request review, and batch-review must pass --repo, otherwise it resolves against cwd and the file is not found (CONFIG_ERROR). List / account-scoped batch-review / List my commits that would otherwise omit --repo must still pass --repo of a relevant Git root when that overlay path is relative (List and List my commits do not use the overlay content, but the CLI still loads it). Pure absolute paths need not depend on --repo.

### 5. Do not switch branches / edit business source

- MR source branch = git branch --show-current at trigger time; do not git switch / git checkout
- Current branch = target: skip that repo, tell the user to switch to the source branch themselves and re-trigger
- Current branch is in pullRequestCreation.skipBranches from the colocated JSON (default main, master, develop): skip that repo's Create PR/MR. Do not run bridge / pull-request create just so the CLI can refuse auto-create. Tell the user they are on a protected branch. This is not REVIEW_BLOCKED
- Do not Write/StrReplace/Delete business source (session response files excepted)
- Do not manually commit / push / call platform APIs; do not use gh in place of the GitLab flow

### 6. Issues table (local review / Create PR/MR)

Local Code Review and Create PR/MR share the same table for reviewDetails (review of an existing MR / batch-review do not make local jumps):

| Severity | Description | Location |
|----------|-------------|----------|
| P1 | ... | [src/main.js#L101]({repositoryPath}/src/main.js#L101) |

Location: show filePath relative to the repo root (may include #L line); href must be that item's {repositoryPath}/{filePath} absolute path (use filePath directly if it is already absolute). No path: write an em dash. Multi-repo: one table per repo, do not mix repos; do not use a relative path only (workspaces often have same-named files).

Review PR/MR / batch-review still do not make local jumps.

---

## Create PR/MR mode

### When to use

Run when any of the following holds:

- create MR / create PR / create pull request / open a PR / submit and create MR
- May include a target branch: create MR to feature/x, --target-branch "feature/x"
- Cites this skill and has MR semantics

Do not trigger: the user is still writing code and has not asked to create a PR/MR (dirty porcelain after they did ask is the main Create path: run bridge); review/local-review keywords only; workspace is clean, no commits relative to target, and breakpoint resume does not apply.

### targetBranch resolution (high to low)

1. Explicit branch name in the user message (e.g. create MR to feature/x, --target-branch "feature/x")
2. Merge-into branch the user clearly gave in this conversation
3. After CLI config resolve of the colocated JSON (not the creation overlay), pullRequestCreation.targetBranch is already non-empty (only when the above are absent and the config value is unique). The creation overlay is merged later by with-target-branch.sh and cannot supply the unique target for this gate; the script requires a non-empty target argument
4. Still cannot uniquely determine: hard gate, stop and ask (see below)

Strip quotes and the origin/ prefix.

### target-branch not configured / not given in time (hard gate)

Before calling with-target-branch.sh, bridge, or pull-request create, a unique target must already be resolved. If the user only said create MR and context has no base branch:

1. Stop immediately this skill's Git/CLI steps
2. Do not guess main/master/develop, use the current branch as target, or run the CLI with an empty targetBranch (with an empty target, bridge records a create failure after commit/push, and pull-request create fails outright; neither guesses a default branch)
3. Ask the user to reply with create MR to feature/2.0.2.SP6 or --target-branch feature/2.0.2.SP6. Once an explicit branch name is given, continue commit / push / create MR.
4. After the user's next message gives a branch: resume from config resolve / with-target-branch
5. If the summary skipped for a missing target: write Skipped (waiting for the user to specify target-branch); do not phrase it as a CLI/review failure

### Breakpoint resume (pull-request create)

Run only when all of the following hold:

1. git status --porcelain is empty
2. Current branch is not target and is not in skipBranches
3. There are commits to merge relative to target (git rev-list --count origin/<target>..HEAD > 0 or equivalent)
4. The entry was already clean, or after bridge you got NO_CHANGES / committed but no MR yet
5. pullRequestCreation.autoCreateAfterPush is true. If the user set it false, "committed but no MR" is the intended stop; do not run pull-request create

porcelain non-empty: must bridge first. REVIEW_BLOCKED: do not bypass with create.

No upstream and not pushed: do not push manually; tell the user to git push -u origin <branch> and re-trigger.

### Per-repo flow

cd to the Git root. Record porcelain and current branch. Generate RUNTIME_CONFIG with with-target-branch.sh using SMART_GIT_CONFIG, the MR target branch, and pwd.

| porcelain | commits relative to target | Action |
|-----------|----------------------------|--------|
| non-empty | any | bridge plus Host-Agent loop |
| empty | yes | pull-request create plus loop |
| empty | no | skip |

bridge (main path): cd Git root, set SESSION_BASE to ${TMPDIR:-/tmp}/scha-sessions, run {CLI prefix} bridge --repo . --config RUNTIME_CONFIG --session-base SESSION_BASE optional --commit-message if the user clearly gave one this turn, optional --set=... overrides (4.1), --output json. On needs_host_agent, write the response and resume with the same args except replace --session-base with --session sessionPath (never pass both).

Typical purpose order: commit-message (when autoGenerate is true and input is empty, or hybridGenerate is true with a draft), then code-review, then (after push) pr-content, then create MR.
Add --commit-message only when the user clearly gave a commit message this turn (equivalent to commitMessage.input).
hybridGenerate=true plus a non-empty input / --commit-message: refinement turn (request includes User draft). hybridGenerate=false plus a non-empty input: no commit-message turn (validate and use the draft). Default hybridGenerate=false and autoGenerate=true with empty input: the CLI still issues a commit-message turn to generate from the diff; do not skip it.
commit-message: follow structure/protocol/scope/skill; if User draft is present, refine.
  required: type(scope): kebab-case from the changed area; missing scope fails immediately, do not expect a correction turn
  forbidden: type: / type!: no parenthesized scope; CLI strips it, no second turn
  auto: (scope) optional; Gitmoji / non-typed unaffected by scope
  hybrid: required may add scope to a draft that has none; an existing scope must be kept as-is; forbidden strips parenthesized scope from the draft
code-review: follow Review skill guidance; local bridge has no line-number annotations
pr-content must be a JSON string of title and description; do not paste the commit message as the description
title: titlePrompt non-empty uses this turn's title; titlePrompt empty and exactly 1 commit relative to target: CLI overwrites with that commit subject
reviewers / milestone / draft are sent to the platform API from config; do not fill them in the turn JSON

pull-request create (breakpoint): {CLI prefix} pull-request create --repo . --config RUNTIME_CONFIG --session-base SESSION_BASE --no-commit optional --no-push, optional --set=... overrides (4.1), --output json.

| relative to @{u} | flags |
|------------------|-------|
| ahead = 0 | --no-commit --no-push |
| ahead > 0 | --no-commit (let the CLI push only if git.autoPush is true; if autoPush is false, also pass --no-push) |
| no upstream | do not run; tell the user to push |

### Parse bridge results

| Result | Behavior |
|--------|----------|
| needs_host_agent | continue the turn loop (not a failure) |
| passed plus push plus MR created/existing | success |
| NO_CHANGES / committed but no MR, and breakpoint applies | pull-request create only if autoCreateAfterPush is true; if false, stop as success without an MR |
| REVIEW_BLOCKED / blocked plus review block | stop the whole skill; output the review only; do not edit code or resume create |
| other error | skip that repo (continue if multi-repo) |

Every bridge must write into the summary: score, threshold, reviewDecision, reviewSummary, reviewDetails (table format: shared prerequisite 6).

### Output summary (Create PR/MR)

Heading: Git / MR summary — branch name.
Include: MR target branch and source (user-specified / conversation / config); temporary overrides applied (4.1) or none; CLI smart-commit-host-agent version and all-succeeded / partial / all-failed / skipped; a table of repo, source branch, target, path (bridge / pull-request create), result, score, commit, push, MR, link; Code Review per repo with score / threshold / decision / summary / details table.
End with the clickable config reminder: [smart-commit.host-agent.json]({SKILL_DIR}/smart-commit.host-agent.json) and [CONFIG.md]({SKILL_DIR}/CONFIG.md).

---

## Review PR/MR mode

Must have at least one PR/MR URL (GitHub .../pull/N or GitLab .../merge_requests/N). No URL: ask.

Default-config impact (know this before a live review): in the colocated smart-commit.host-agent.json, pullRequest.provider defaults to auto; pullRequestReview.autoApprove / autoMerge default to true; summarySeverities defaults to ["P0","P1"]. So a live pull-request review may auto-approve and merge after a passing review. When the user has not changed the config:

- Add --dry-run only if the user explicitly asks for dry-run / a trial / no publish / no merge
- If the user clearly does not want auto-merge / auto-approve this time: pass --set=pullRequestReview.autoMerge=false and/or --set=pullRequestReview.autoApprove=false (4.1); for a permanent change point them at the JSON
- The summary must truthfully report approve / merge attempted / performed (or skip under dry-run)

Run: {CLI prefix} pull-request review URL --config $SMART_GIT_CONFIG --session-base ${TMPDIR:-/tmp}/scha-sessions optional --repo path, optional --dry-run, optional --set=... overrides (4.1), --output json. Keep the URL right after "pull-request review" and use the single-token --set= form.

--repo is optional. Platform, project, number, and diff all come from the URL, so no local checkout is needed; without --repo the CLI uses the current directory (Git or not) and never writes into it. Pass --repo only when pullRequestReview.configFilePath or review.skill is a relative path that lives in a specific repo (point it at that repo's Git root), or when the user is already working in that PR/MR's local clone.

Do not pass --provider / --pull-request-provider (default auto; a platform switch the user asks for this turn uses --set=pullRequest.provider=..., a permanent one goes in the JSON). Multiple URLs are reviewed one by one; a single URL failure does not stop the rest (except a global CONFIG failure).

pullRequestReview.configFilePath is loaded automatically by the CLI (rules: shared prerequisite 4). A non-empty skillPromptTuning overrides review.skill.promptTuning and only affects this mode / batch-review, not local bridge. When filling the code-review turn, follow Review skill guidance; when the request has line-number annotations, copy the visible lineNumber.

The summary must include: score, threshold, details, summary, platform action fields (including approve/merge), temporary overrides applied (or none). On blocked, do not edit code and should not merge.

Do not use gh pr view prefetch in place of the CLI.

---

## List my PRs/MRs mode

### When to use

Run when any of the following holds (no URL needed, no local changes needed):

- list my MRs / my MR list / my pending MRs / list my PRs / my-pull-request list
- list pending MRs / list MRs I created / list MRs assigned to me (you may narrow listKinds from this)
- Cites this skill with the meaning show my open PRs/MRs

Do not trigger: review MR with a parseable URL (Review mode); create MR; local code review; wording that includes batch / batch-review (Batch-review my PRs/MRs).

### Behavior

- No Host-Agent turn; a single CLI run is terminal (status ok / error)
- Does not commit / push / create MR / post comments / approve / merge
- Does not need targetBranch / with-target-branch.sh
- Needs a platform token (same as shared prerequisite 3.1)
- Defaults from config: myPullRequest.listScope (default account), myPullRequest.listKinds (default created,assigned,reviewer), pullRequest.remoteHost (default empty; deprecated myPullRequest.remoteHost is the fallback)
- After a successful list, do not automatically switch to my-pull-request batch-review; if the user wants a batch review they must separately say batch-review my MRs

### scope / host / kinds resolution (high to low)

listScope:
1. Explicit in the user message: account / my account -> account; workspace / current repo -> workspace
2. Config myPullRequest.listScope

remoteHost (commonly used for account; strongly recommended for self-hosted GitLab; shared with Batch-review and List my commits):
1. A hostname in the user message (e.g. gitlab.example.com, list my MRs on xxx) -> pass --pull-request-remote-host
2. Config pullRequest.remoteHost
3. Config myPullRequest.remoteHost (deprecated fallback, read by the CLI only when pullRequest.remoteHost is empty)
4. Still empty and scope=account: the CLI may fall back to local remotes, then public gitlab.com / github.com (driven by pullRequest.provider). Out of the box remoteHost is empty; when the team uses self-hosted GitLab, ask first for the hostname or prompt them to edit the config; do not silently list against the public internet without confirmation

With pullRequest.provider=auto, a remoteHost other than github.com / gitlab.com is CONFIG_ERROR ("Could not infer GitHub/GitLab from ..."). Guide the user to set pullRequest.provider to gitlab or github (and pullRequest.apiBaseUrl if needed) in the JSON, or, if they state the platform in the request, pass --set=pullRequest.provider=gitlab for this run (4.1); do not pass --pull-request-provider and do not edit the config yourself.

listKinds (multi-select: created / assigned / reviewer):
1. User-semantics mapping:
   - Only I created / created -> created
   - Only assigned to me / assigned -> assigned
   - Only I am reviewer -> reviewer
   - pending (e.g. list pending MRs, my pending MRs) -> reviewer,assigned (MRs I need to review/handle; matches the default batchReviewKinds in config)
   - Unspecified -> use config listKinds
2. Config myPullRequest.listKinds

--repo:
- workspace: pass --repo path for each relevant Git root (if omitted the CLI uses cwd)
- account plus non-empty remoteHost: --repo may be omitted (skip reading remotes)
- account plus empty remoteHost: current-repo --repo . may help infer host from origin (still prefer guiding them to set pullRequest.remoteHost)

### CLI

{CLI prefix} my-pull-request list --config $SMART_GIT_CONFIG optional --repo paths, --my-pull-request-list-scope account|workspace, --my-pull-request-list-kinds created,assigned,reviewer, --pull-request-remote-host host, --output json.

Allowed one-shot overrides: only the --my-pull-request-* flags above, --pull-request-remote-host, --set=... for other fields the user stated (4.1, e.g. pullRequest.provider), plus --repo / --config / --output. Do not use the deprecated --my-pull-request-remote-host.
Forbidden: --pull-request-auth-token (keeps the token out of command-line history), --provider / --pull-request-provider overriding config, hand-written gh / platform REST lists.

### Parse results

Per-repo failure warnings: with status ok the CLI downgrades a single repo's listing error to a warnings entry (mostly workspace scope), e.g. HTTP 401/403, Bad credentials, token rejected, request failed. Check warnings before treating status ok as success.

| Result | Behavior |
|--------|----------|
| status ok, items non-empty, no per-repo failure warnings | success; render the summary table |
| status ok, items empty, no per-repo failure warnings | success but no matches; record summary / warnings as-is |
| status ok, items empty, per-repo failure warnings | listing failed, not "no matches": name the failed repos; for 401/403 guide the user to fix SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN (shared prerequisite 3.1) |
| status ok, items non-empty, per-repo failure warnings | partial results: render the items, then name the failed repos and say their MRs/PRs are missing; for 401/403 guide the token fix as above |
| CONFIG_ERROR / Token | guide per shared prerequisites; stop |
| other error | skip/failure summary (do not pretend success in multi-repo) |

Take from JSON: scope, kinds, items[] (at least title, url, repoName/projectPath, roles, sourceBranch, targetBranch, draft, author, updatedAt), warnings, summary.

### Output summary (List my PRs/MRs)

Heading: List my PRs/MRs. Include CLI version; query scope/kinds/remoteHost/repos; temporary overrides applied (if any); results summary; a table of repo, title, roles, source->target, draft, updated, link; warnings.
End with the clickable reminder pointing at smart-commit.host-agent.json for myPullRequest.listScope / listKinds and pullRequest.remoteHost, and CONFIG.md.
Do not paste the token / authToken. After listing, if the user wants to review one item they must separately say review MR plus URL; if they want a batch review they must separately say batch-review my MRs. Do not automatically switch to pull-request review / batch-review.

---

## Batch-review my PRs/MRs mode

### When to use

Run when any of the following holds (no need to paste URLs, no local changes needed):

- batch review my MRs / batch-review MRs / batch review my PRs / my-pull-request batch-review
- batch-review pending MRs (you may narrow batchReviewKinds from this)
- Cites this skill with the meaning automatically review my related open PRs/MRs one by one

Do not trigger: only list my MRs / my pending MRs (List mode, does not review); review MR plus one or more URLs (single pull-request review); create MR; local code review.

### Behavior

- First list open PRs/MRs by myPullRequest.batchReviewKinds (default reviewer,assigned), then serially run the same review plus platform-publish path as pull-request review on each
- Has Host-Agent turns: on needs_host_agent write the response and resume with --session; the CLI records batch progress in the session directory itself and automatically skips completed URLs on resume
- Does not commit / push / create MR; does post comments / approve / merge per pullRequestReview (same as single-item review)
- Does not need targetBranch / with-target-branch.sh
- Needs a platform token (same as shared prerequisite 3.1)
- Defaults from config: myPullRequest.listScope, myPullRequest.batchReviewKinds, pullRequest.remoteHost (do not use listKinds as the batch filter)

Default-config impact (know this before a live batch review): in the colocated config, pullRequestReview.autoApprove / autoMerge default to true. Batch items that pass may also be auto-approved and merged. When the user has not changed the config:

- Add --dry-run only if the user explicitly asks for dry-run / a trial / no publish / no merge
- If the user clearly does not want auto-merge / auto-approve this time: pass --set=pullRequestReview.autoMerge=false and/or --set=pullRequestReview.autoApprove=false (4.1) on the first run and every resume
- The summary must truthfully report each outcome and the overall summary; when any item is not_passed the CLI exit is often 2 (blocked). Still write completed outcomes into the summary; do not edit business source because of blocked

### scope / host / kinds resolution (high to low)

listScope / remoteHost: same as List my PRs/MRs (user explicit then pullRequest.remoteHost then deprecated myPullRequest.remoteHost; for account plus empty remoteHost on self-hosted GitLab, ask first; provider=auto with a self-hosted host is CONFIG_ERROR).

batchReviewKinds (multi-select: created / assigned / reviewer) — not listKinds

1. User-semantics mapping:
   - Only I created -> created
   - Only assigned to me -> assigned
   - Only I am reviewer -> reviewer
   - pending / role unspecified -> use config batchReviewKinds (default reviewer,assigned)
2. Config myPullRequest.batchReviewKinds

--repo: same as list mode (workspace passes each Git root; account plus non-empty remoteHost may omit).

### CLI

{CLI prefix} my-pull-request batch-review --config $SMART_GIT_CONFIG optional --repo paths, --my-pull-request-list-scope, --my-pull-request-batch-review-kinds, --pull-request-remote-host, --session-base ${TMPDIR:-/tmp}/scha-sessions, optional --dry-run, optional --set=... overrides (4.1), --output json.
On needs_host_agent, write the response and resume with the same args except replace --session-base with --session sessionPath (never pass both). On resume do not list again; the CLI skips completed URLs from session progress.

Allowed one-shot overrides: the --my-pull-request-* flags above, --pull-request-remote-host, --set=... (4.1), --repo / --config / --session / --session-base / --dry-run / --output. Do not use the deprecated --my-pull-request-remote-host.
Forbidden: --pull-request-auth-token, --provider / --pull-request-provider override, gh / hand-written platform APIs, using multiple pull-request review calls instead of this command (unless the user only wants a few specific URLs), chaining batch-review after list mode on your own.

### Parse results

| Result | Behavior |
|--------|----------|
| needs_host_agent | continue the turn loop (not a failure); keep sessionPath |
| status ok, totalListed 0, no per-repo failure warnings (defined under List my PRs/MRs parse results) | success but no matches; record summary / warnings as-is |
| status ok, totalListed 0, per-repo failure warnings | same as the List my PRs/MRs row "items empty, per-repo failure warnings": listing failed, not "no matches" |
| status ok plus outcomes, no per-repo failure warnings | terminal success path; combine with exit: 0 all passed; 2 some not_passed; 4 some error / cancelledRemaining |
| status ok plus outcomes, per-repo failure warnings | report the outcomes per exit code as in the row above, then apply the List my PRs/MRs row "items non-empty, per-repo failure warnings": name the failed repos and say their MRs/PRs were neither listed nor reviewed |
| CONFIG_ERROR / Token | guide per shared prerequisites; stop |
| other error | failure summary (do not edit business source) |

Take from JSON: scope, kinds, totalListed, outcomes[] (status passed / not_passed / error / skipped; plus title/url/score/threshold or errorMessage), cancelledRemaining, warnings, summary, dryRun, sessionPath.

### Output summary (Batch-review my PRs/MRs)

Heading: Batch-review my PRs/MRs. Include CLI version and succeeded / some not passed / failed / skipped / dry-run; query scope, batchReviewKinds, remoteHost, dryRun, repos; temporary overrides applied (or none); overview summary, totalListed, cancelledRemaining; a table of status, title, score, threshold, link/error; warnings.
End with the clickable reminder for myPullRequest.batchReviewKinds / listScope, pullRequest.remoteHost, and pullRequestReview.autoApprove/autoMerge.
Do not paste the token / authToken. Any item not passed or error: do not Write/StrReplace business source based on it.

---

## List my commits mode

### When to use

Run when any of the following holds (no URL needed, no local changes needed):

- list my commits / my commits today / my commits this week / show my commits / my-commit list
- what did I commit yesterday / last week / this month / between 2026-10-01 and 2026-10-07
- Cites this skill with the meaning show the commits I authored for some period (stand-up, weekly report, timesheet)

Do not trigger: create MR / commit my changes (Create PR/MR); list my MRs (List my PRs/MRs); local code review; a request to write a report (this mode only lists commits; summarizing them is a separate request).

### Behavior

- No Host-Agent turn; a single CLI run is terminal (status ok / error)
- Does not commit / push / create MR / post comments / approve / merge; does not read or change the local working tree beyond resolving remotes
- Does not need targetBranch / with-target-branch.sh
- Needs a platform token (same as shared prerequisite 3.1)
- Defaults from config myCommit: scope (default account), range (default today), authorAliases (default []), includeMergeCommits (default false), outputFormat (default compact; decides the summary style below); host from pullRequest.remoteHost (same rules as List my PRs/MRs)
- Matches commits by the token account's login, profile email, and myCommit.authorAliases; the profile display name is not used. Results are de-duplicated and sorted newest first
- After a successful list, do not automatically generate a report, review, or MR from the records

### scope / host / range / author resolution (high to low)

scope:
1. Explicit in the user message: account / all my repos -> account; workspace / current repo / this repo -> workspace
2. Config myCommit.scope

remoteHost: same as List my PRs/MRs (user hostname -> --pull-request-remote-host, then pullRequest.remoteHost, then deprecated myPullRequest.remoteHost; account plus empty host on self-hosted GitLab: ask first; provider=auto with a self-hosted host is CONFIG_ERROR). workspace scope ignores remoteHost and scans the --repo remotes.

range (dates are local calendar days of this machine; weeks start on Monday):

| User says | Flags |
|-----------|-------|
| today | --my-commit-range today |
| yesterday | --my-commit-range yesterday |
| this week | --my-commit-range thisWeek |
| last week | --my-commit-range lastWeek |
| this month | --my-commit-range thisMonth |
| last month | --my-commit-range lastMonth |
| last N days, since a date, a specific date, or a date span | --my-commit-range custom --start-date YYYY-MM-DD --end-date YYYY-MM-DD (inclusive; compute from today's local date; "last 3 days" = today and the 2 days before) |
| nothing about time | omit; use config myCommit.range |

- custom spans at most 31 days. If the requested range is longer (e.g. this quarter, the last 60 days), stop before running the CLI: tell the user the 31-day limit and ask them to narrow it, or suggest thisMonth / lastMonth. Do not split it into multiple runs yourself
- Never pass --start-date / --end-date without --my-commit-range custom (the CLI rejects it with CONFIG_ERROR); even if config myCommit.range is custom, pass --my-commit-range custom explicitly together with both dates
- Start must not be after end; ask if the user's dates are ambiguous (e.g. a month/day with no clear year near a year boundary)

authorAliases / merge commits:
- The user names extra author identities this turn (e.g. also match alice@corp.com, my old name Alice Smith) -> --my-commit-author-aliases "Alice Smith,alice@corp.com" (one-shot; for a permanent change point them at myCommit.authorAliases)
- The user asks to include merge commits -> --my-commit-include-merge-commits; asks to exclude them -> --my-commit-include-merge-commits=false
- Otherwise use config

--repo:
- workspace: pass --repo path for each relevant Git root (if omitted the CLI uses cwd)
- account plus non-empty remoteHost: --repo may be omitted (skip reading remotes)
- account plus empty remoteHost: current-repo --repo . may help infer host from origin (still prefer guiding them to set pullRequest.remoteHost)

### CLI

{CLI prefix} my-commit list --config $SMART_GIT_CONFIG optional --repo paths, --my-commit-scope account|workspace, --my-commit-range preset, --start-date / --end-date (custom only), --my-commit-author-aliases list, --my-commit-include-merge-commits[=false], --pull-request-remote-host host, --output json.

Allowed one-shot overrides: only the flags above, --set=... for other fields the user stated (4.1, e.g. pullRequest.provider), plus --repo / --config / --output. Leave --my-commit-concurrency / --my-commit-request-delay-ms to config unless the user explicitly asks this turn. Always use --output json; do not pass --my-commit-output-format (it only changes CLI text output). The summary style is chosen by the skill, see Output summary below.
Forbidden: --pull-request-auth-token, --provider / --pull-request-provider / --pull-request-api-base-url overriding config, the deprecated --my-pull-request-remote-host, git log on local clones or hand-written gh / platform REST calls in place of this command.

### Parse results

| Result | Behavior |
|--------|----------|
| status ok plus records | success; render the summary in the chosen style (compact or full) |
| status ok plus records empty | success but no matches; record summary / warnings as-is; if the user expected commits, mention myCommit.authorAliases (commits authored under another name or email are not matched) |
| complete false | still exit 0; results are partial (query stopped early, usually a low rate limit). Say so explicitly, show warnings, suggest retrying later or raising myCommit.requestDelayMs / lowering myCommit.concurrency |
| CONFIG_ERROR (exit 3) | token missing -> guide per shared prerequisite 3.1; invalid range / dates / myCommit.* / provider-host mismatch -> report the field and stop |
| RUNTIME_ERROR (exit 4) | e.g. rejected token or invalid repository path; failure summary, do not pretend success |

Take from JSON: scope, dateRange (preset, label, since, until, dayCount), provider (kind, host), account.login, records[] (projectPath, sha, message, authoredAt, branches, url, isMergeCommit), complete, repositoryCount, scannedRepositoryCount, warnings, summary, config.myCommit.outputFormat.

### Output summary (List my commits)

Style (high to low):
1. Explicit in the user message: details / full / table / with links / with SHA -> full; brief / concise / only messages / for stand-up -> compact
2. config.myCommit.outputFormat from the CLI JSON (default compact)

compact (default): heading List my commits, then one line with range label (local since / until), total commits, repositories scanned (scannedRepositoryCount / repositoryCount), complete yes/no; then a plain bullet list of each commit message's first line, newest first (no SHA / time / link); then warnings. No CLI version / provider / account lines unless something failed.

full: heading List my commits. Include CLI version; provider and host; account login; scope; range label with local since / until; total commits, repositories scanned, complete yes/no; then a table of repo (projectPath), short SHA (first 8 chars), message (first line), authored at (local time), branches (empty for GitLab), link; warnings.

Both styles: complete false must be stated as partial results; empty results say no commits matched; temporary overrides applied this run (4.1) get one line when there are any.
End with the clickable reminder pointing at smart-commit.host-agent.json for myCommit.outputFormat / range / scope / authorAliases / includeMergeCommits and pullRequest.remoteHost, and CONFIG.md.
Do not paste the token / authToken, and do not paste authorEmail values beyond what the user asked for.

---

## Local Code Review mode

cd to the Git root. Run {CLI prefix} bridge --repo . --config $SMART_GIT_CONFIG --review-only --session-base ${TMPDIR:-/tmp}/scha-sessions optional --set=... overrides (4.1; review.* fields such as threshold / language / skill are the useful ones here) --output json. The summary lists the overrides applied (or none).

- Do not use --no-commit/--no-push in place of --review-only
- Do not pass target / provider / create-MR parameters
- Does not need pullRequest.authToken / SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN; even if unset, must not stop per 3.1
- Confirm the result: commitMessageSource=review-only, didCommit=false, didPush=false
- With git.autoStageWhenNothingStaged true (default) and nothing staged, the CLI stages the working-tree changes to review them and leaves them staged. Mention this in the summary; do not unstage or reset on your own
- reviewDetails table format: shared prerequisite 6

---

## Intent routing

This skill runs independently; it does not call or hand off to other skills. Route only among this skill's six modes based on the user message:

| User input | Mode |
|------------|------|
| local code review / local review of changes etc. | Local Code Review |
| batch-review my MRs / batch-review etc. | Batch-review my PRs/MRs |
| list my MRs / my MR list / list my PRs etc. | List my PRs/MRs |
| list my commits / my commits this week / what did I commit yesterday etc. | List my commits |
| review MR / review PR plus URL | Review PR/MR |
| create MR / open a PR / create PR | Create PR/MR |
| local review plus create MR / review MR / list / batch-review / list my commits (multiple modes in one message) | Stop and ask |
| ordinary code review / review code (without local) | Do not trigger this skill |

Resolution priority:

1. Multiple mode keywords in the same message (local / review MR / create MR / list my MRs / batch-review / list my commits) -> ask. Do not count batch-review keywords as Review PR/MR
2. Local Code Review keywords -> local mode
3. Batch-review my PRs/MRs keywords -> batch-review mode
4. List my PRs/MRs keywords -> list mode (does not review)
5. List my commits keywords -> List my commits mode
6. Review MR keywords plus URL -> review mode
7. Create MR keywords -> Create PR/MR

---

## Quick checklist

- Mode routed and commands not mixed
- Config values stated in the request went through --set=path=value (or the mode's dedicated flag) on config resolve, the first run, and every resume; nothing was written to the JSON; no authToken / configFilePath override; vague wishes without a value were asked about; the summary lists the overrides
- discover then resolve done; platform modes have a token (or already guided and skipped); Local Code Review was not stopped for a missing token; config resolve passed
- Node >= 20; CLI from PATH / project node_modules / SMART_COMMIT_CLI / a global install this turn (source recorded in the summary); the CLI is >= 0.1.7 (--version)
- Did not extra-run a global install when a local or PATH install already existed; automatic global install only when nothing found
- Did not forge an unverified path after a failed global install
- On needs_host_agent, wrote the response and resumed with --session to a terminal state (list mode and List my commits have no turn, skip this item; batch-review has turns and must resume). commit-message follows the request structure/protocol/scope/skill (refine if User draft is present; required must be type(scope):, forbidden must not include parenthesized scope; neither has a second turn). code-review follows Review skill guidance; PR/MR review with line-number annotations must copy the visible lineNumber. The pr-content turn before bridge creates the MR must fill title and description JSON; do not paste the commit message as the description. Only when titlePrompt is empty and there is exactly 1 commit relative to target does the CLI overwrite title with that commit subject; when titlePrompt is non-empty, this turn's title is used
- Create PR/MR: unique target resolved (or missing target already asked and CLI skipped); used with-target-branch.sh config target Git-root; did not git switch; did not edit business source
- Did not run bridge / pull-request create with an empty target (empty target fails create and will not guess main)
- List: used my-pull-request list; self-hosted GitLab confirmed remoteHost (or already asked); host override used --pull-request-remote-host, not the deprecated --my-pull-request-remote-host; did not automatically switch to review/batch-review; did not pass --pull-request-auth-token; checked warnings before calling status ok a success: per-repo HTTP/token failures with empty results were reported as a failed listing, not "no matches", and with non-empty results as partial results naming the failed repos (same for batch-review)
- List my commits: used my-commit list (not git log / gh / hand-written APIs); range mapped to a preset or custom with both dates (custom only, at most 31 days; longer ranges were sent back to the user to narrow); self-hosted GitLab confirmed remoteHost (or already asked); complete false reported as partial; did not chain into a report / review / MR
- Batch-review: used my-pull-request batch-review (not multiple hand-written pull-request review); kinds from batchReviewKinds / --my-pull-request-batch-review-kinds; resume used the same --session; autoApprove/autoMerge risk was called out or dry-run was honored; did not edit business source because of not_passed
- Did not manually commit/push/API; did not misuse gh in place of review/list/batch-review/my-commit list
- REVIEW_BLOCKED / batch not_passed summarized truthfully and code was not auto-fixed
- Summary has no token / authToken
- Local review / Create PR/MR details are Severity | Description | Location; href uses that repo's {repositoryPath}/{filePath} absolute path (do not mix multi-repo); Review PR/MR / batch-review do not make local jumps
