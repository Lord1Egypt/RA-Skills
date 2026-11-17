# Custom config (smart-commit.host-agent.json)

This skill's review threshold, commit rules, Git behavior, PR/MR platform, and comment policy are all decided by smart-commit.host-agent.json colocated with SKILL.md.
Edit the config to fit different teams / repos / habits; do not change the skill flow.

Path example: smart-commit.host-agent.json next to SKILL.md (for example ~/.cursor/skills/smart-git/smart-commit.host-agent.json, or the same-named directory under another AI tool's skills root). The skill copy actually loaded this turn wins; it is not limited to a specific product.

After editing, self-check with config resolve --config pointing at that JSON. No error means it is valid.

Keep the token as env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN. Do not put a plaintext token in the JSON.

---

## One-time overrides by saying it

You do not have to edit the JSON for a single run. State the value in the request and the skill passes it to the CLI as --set=path=value for that run only; the file is not changed and the next request uses the file again.

| You say (examples) | Applied as |
|--------------------|------------|
| review this MR but don't auto-merge this time | pullRequestReview.autoMerge=false |
| don't auto-approve | pullRequestReview.autoApprove=false |
| local review with threshold 8 | review.threshold=8 |
| review this MR with threshold 8 | pullRequestReview.threshold=8 |
| review in English | review.language=en |
| commit message in English, with body | commitMessage.language=en, commitMessage.structure=subjectBody |
| create MR as draft, reviewers alice and bob, label bug | pullRequestCreation.draft=true, reviewers=alice,bob, labels=bug |
| don't push this time | git.autoPush=false |
| use GitHub for this one | pullRequest.provider=github |
| require a commit scope | commitMessage.scope=required |

Rules:

- Any field documented below can be overridden except pullRequest.authToken and the two configFilePath fields
- Overrides beat the colocated JSON and repo overlays; the mode's dedicated flags (dry-run, commit message, list kinds, commit range, remote host, target branch) still work as before
- Give a concrete value; for a vague wish ("stricter review") the skill asks for the number
- Every summary lists the overrides it applied
- To make a value permanent, edit the JSON field

---

## This skill's defaults (out of the box)

The fields below are the ones the six modes actually use, with out-of-the-box values.
(If the JSON also has passHistory / reporting / output, this skill flow ignores them; they are not covered below.)

### Shared by local review / Create PR/MR

| Field | Default | One-line meaning |
|-------|---------|------------------|
| review.threshold | 6 | Only local Code Review / the bridge review before Create PR/MR: score must be strictly greater than this value to pass |
| review.language | "zh-cn" | Natural language used for review comments |
| review.maxDiffChars | 500000 | Max diff characters sent for review; too large may truncate |
| review.skill.id | "code-review" | Built-in review skill; used when path is empty. See review.skill below for ids |
| review.skill.path | "" | Custom review rules file; absolute paths used as-is, relative paths relative to the reviewed repo root. Non-empty ignores id |
| review.skill.promptTuning | "" | Short extra instructions appended to the review turn; PR/MR review may be overridden by pullRequestReview.skillPromptTuning |

Two thresholds are easy to mix up: review.threshold only covers local review / Create PR/MR; pullRequestReview.threshold only covers review of an existing PR/MR / batch-review. They do not affect each other. Both default to 6, but changing one does not sync the other. Pass condition is always score > threshold (equal does not pass).

### Create PR/MR (commit / push / create MR)

| Field | Default | One-line meaning |
|-------|---------|------------------|
| commitMessage.language | "zh-cn" | Language for auto-generated commit messages |
| commitMessage.input | "" | Prefill commit message; empty means the Agent generates it |
| commitMessage.maxDiffChars | 150000 | Diff cap sent to the model when generating a commit message |
| commitMessage.structure | "subjectOnly" | Generated structure: subjectOnly / subjectBody / subjectBodyFooter |
| commitMessage.scope | "forbidden" | typed subject (type: / type!:) (scope): auto optional, required mandatory, forbidden banned (CLI strips it). Gitmoji unaffected. Do not confuse with myPullRequest.listScope |
| commitMessage.autoGenerate | true | Whether to auto-generate a commit message when input is empty |
| commitMessage.hybridGenerate | false | When input is non-empty: false uses it and validates; true sends the draft to a refinement turn |
| commitMessage.skill.id | "conventional" | Built-in generate skill (conventional / semantic / gitmoji); not the same as the validation protocol |
| commitMessage.skill.path | "" | Custom commit-spec file; absolute as-is, relative to repo root. Non-empty ignores id |
| commitMessage.skill.promptTuning | "" | Short extra instructions appended to the commit-message turn |
| commitMessage.validation.protocol | "none" | Validation protocol: none / conventional / semantic / gitmoji (empty string treated as none) |
| commitMessage.validation.pattern | "" | Extra subject regex, independent of protocol; empty adds no extra constraint |
| commitMessage.validation.extractTicketIdFromBranch | true | Whether to extract a ticket id from the branch name into the commit message |
| commitMessage.validation.requireTicketIdInMessage | false | Whether the commit message must contain a ticket id |
| git.autoStageWhenNothingStaged | true | If the index is empty, whether to git add related changes automatically |
| git.autoCommit | true | Whether to auto-commit after a passing review |
| git.autoPush | true | Whether to auto-push after commit |
| git.pushTimeoutMs | 180000 | Push timeout (milliseconds) |
| pullRequestCreation.autoCreateAfterPush | true | Whether to auto-create a PR/MR after a successful push |
| pullRequestCreation.configFilePath | "" | Repo-level creation overlay (comma-separated, first existing file; mix absolute/relative). Empty means do not load |
| pullRequestCreation.targetBranch | "" | Merge target branch; usually left empty and temporarily overridden by conversation "create MR to xxx" |
| pullRequestCreation.titlePrompt | "" | Short title-generation instructions; when non-empty, a single commit subject is no longer used to overwrite title |
| pullRequestCreation.descriptionPrompt | "" | Short description-generation instructions (e.g. team MR template points) |
| pullRequestCreation.maxDiffChars | 300000 | Diff cap used when generating the PR/MR description |
| pullRequestCreation.assignees | [] | Default assignees at create time (usernames) |
| pullRequestCreation.reviewers | [] | Default reviewers at create time (usernames; GitHub teams may use org/team) |
| pullRequestCreation.labels | [] | Default labels at create time |
| pullRequestCreation.milestone | "" | Milestone title or numeric id; empty means unset |
| pullRequestCreation.draft | false | Whether to create as a draft PR/MR |
| pullRequestCreation.removeSourceBranch | true | Whether to delete the source branch after merge |
| pullRequestCreation.skipBranches | ["main","master","develop"] | If the current branch matches, auto-create PR/MR is forbidden |

### Platform (shared by Create / Review / List / Batch-review / List my commits; local review does not need it)

| Field | Default | One-line meaning |
|-------|---------|------------------|
| pullRequest.provider | "auto" | Platform: gitlab / github / auto |
| pullRequest.apiBaseUrl | "" | API root for self-hosted GitLab/GitHub; public hosts may leave empty |
| pullRequest.authToken | "env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN" | Token reference; keep env:..., no plaintext. Only create/review/list/batch-review/my-commit list need it; local bridge --review-only and config resolve resolve a missing env to empty and do not error |
| pullRequest.remoteHost | "" | Git host for account-scope List / Batch-review / List my commits; empty out of the box — fill in for self-hosted GitLab (and set provider explicitly) |

### Review existing PR/MR / batch-review

| Field | Default | One-line meaning |
|-------|---------|------------------|
| pullRequestReview.threshold | 6 | Only existing PR/MR (including batch) review: score must be strictly greater than this; does not affect local / Create PR/MR |
| pullRequestReview.autoApprove | true | Whether to auto-approve after a passing review |
| pullRequestReview.autoMerge | true | Whether to auto-merge after a passing review (risky) |
| pullRequestReview.summarySeverities | ["P0","P1"] | Which severities are written into the summary comment |
| pullRequestReview.commentSeverities | ["P0","P1"] | Which severities are posted as inline comments |
| pullRequestReview.skillPromptTuning | "" | Only existing PR/MR / batch-review: overrides review.skill.promptTuning; does not affect local / Create PR/MR bridge |
| pullRequestReview.skipSummaryOnPass | true | Whether to skip the summary comment when the review passes |
| pullRequestReview.skipCommentOnPass | true | Whether to skip inline comments when the review passes |
| pullRequestReview.configFilePath | "" | Repo-level review overlay (comma-separated, first existing file; mix absolute/relative). Empty means do not load |

### List my PRs/MRs / Batch-review my PRs/MRs

| Field | Default | One-line meaning |
|-------|---------|------------------|
| myPullRequest.listScope | "account" | List/batch scope: account (by account) or workspace (by workspace repos) |
| myPullRequest.listKinds | ["created","assigned","reviewer"] | List my PRs/MRs only: filter by role |
| myPullRequest.batchReviewKinds | ["reviewer","assigned"] | Batch-review only: role filter before serial review (default pending) |

The account-scope host now lives in pullRequest.remoteHost. myPullRequest.remoteHost is a deprecated fallback (read only when pullRequest.remoteHost is empty) and is no longer in the colocated JSON; an old config that still sets it keeps working.

### List my commits

| Field | Default | One-line meaning |
|-------|---------|------------------|
| myCommit.scope | "account" | account (repos the token account is a member of) or workspace (only --repo / current repo remotes). Independent of myPullRequest.listScope |
| myCommit.range | "today" | Default range when the utterance gives no time: today / yesterday / thisWeek / lastWeek / thisMonth / lastMonth / custom |
| myCommit.authorAliases | [] | Extra author names or emails to match besides the token login and profile email |
| myCommit.concurrency | 2 | Worker count (1-10) |
| myCommit.requestDelayMs | 100 | Minimum delay between API requests in ms (0-5000; 0 disables pacing) |
| myCommit.includeMergeCommits | false | Whether merge commits appear in the list |
| myCommit.outputFormat | "compact" | Summary style: compact (summary line plus commit messages only) or full (table with repo, SHA, time, branches, link). This skill's default is compact; the CLI built-in default is full |

---

## Common needs: what to change

| You want... | Change |
|-------------|--------|
| Local / Create PR/MR review stricter or looser | review.threshold (score > to pass; default 6) |
| Existing PR/MR / batch-review stricter or looser | pullRequestReview.threshold (same rule; independent of review.threshold) |
| Review/commit messages in English | review.language, commitMessage.language (e.g. en) |
| Switch review skill (frontend/Go/Java etc.) | review.skill.id; custom file via review.skill.path |
| Use GitHub / auto-detect | pullRequest.provider: github or auto |
| Self-hosted GitLab API URL | pullRequest.apiBaseUrl |
| List my PRs/MRs / my commits against a Git host | pullRequest.remoteHost (for a self-hosted host also set pullRequest.provider to gitlab / github) |
| List only ones I created | myPullRequest.listKinds: ["created"] |
| List only pending | myPullRequest.listKinds: ["reviewer","assigned"] (utterances with pending also one-shot override) |
| List only where I am reviewer | myPullRequest.listKinds: ["reviewer"] (utterance must say I am reviewer, not merely pending) |
| List / batch-review by workspace repos | myPullRequest.listScope: "workspace" |
| Batch-review only pending | myPullRequest.batchReviewKinds: ["reviewer","assigned"] (already the default) |
| Batch-review only ones I created | myPullRequest.batchReviewKinds: ["created"] |
| List my commits for this week by default | myCommit.range: "thisWeek" (utterances like yesterday / last month also one-shot override) |
| List my commits only from workspace repos | myCommit.scope: "workspace" |
| Match commits made under another name or email | myCommit.authorAliases: ["Alice Smith","alice@corp.com"] |
| Include merge commits in my commit list | myCommit.includeMergeCommits: true |
| My commit list as a full table (SHA, time, link) by default | myCommit.outputFormat: "full" (default compact shows messages only; saying details in the request also switches for one turn) |
| My commit list stops early (complete: false) | raise myCommit.requestDelayMs or lower myCommit.concurrency |
| Default assignees, reviewers, labels on create | pullRequestCreation.assignees, reviewers, labels |
| Create as a draft MR | pullRequestCreation.draft: true |
| Attach a milestone on create | pullRequestCreation.milestone (title or numeric id) |
| Repo-level create/review overlay | pullRequestCreation.configFilePath / pullRequestReview.configFilePath (see overlay rules) |
| Customize MR title/description generation | pullRequestCreation.titlePrompt, descriptionPrompt |
| Delete source branch after merge | pullRequestCreation.removeSourceBranch |
| Forbid auto-create on some branches | pullRequestCreation.skipBranches |
| Do not auto-create MR after push | pullRequestCreation.autoCreateAfterPush: false |
| Disable auto-approve after review | pullRequestReview.autoApprove: false |
| Disable auto-merge after review | pullRequestReview.autoMerge: false |
| Include P2 in summary comments | pullRequestReview.summarySeverities: ["P0","P1","P2"] |
| Still post a summary comment on pass | pullRequestReview.skipSummaryOnPass: false |
| Inline comments only for P0 | pullRequestReview.commentSeverities: ["P0"] |
| Extra short instructions for PR/MR review only | pullRequestReview.skillPromptTuning |
| Do not auto commit / push | git.autoCommit / git.autoPush: false |
| Commit must include a ticket id | commitMessage.validation.requireTicketIdInMessage: true |
| Conventional / Semantic must include (scope) | commitMessage.scope: "required" (typed subject must be type(scope):; missing fails immediately, no correction turn) |
| Conventional / Semantic forbid (scope) | commitMessage.scope: "forbidden" (feat(auth): becomes feat:; no second turn) |
| Turn off commit protocol validation | commitMessage.validation.protocol: "none" |
| Switch to Semantic / Gitmoji validation | protocol: semantic / gitmoji (and matching commitMessage.skill.id) |
| Extra subject constraint beyond protocol | commitMessage.validation.pattern (independent stack on protocol) |
| Let the model refine a draft | commitMessage.input non-empty and hybridGenerate: true |
| Switch review/commit skill or custom file | review.skill / commitMessage.skill id or path |

A one-shot Create PR/MR merge branch prefers conversation "create MR to xxx"; the skill uses a temporary overlay and does not rewrite targetBranch in the JSON.

---

## How to write paths (absolute / relative)

The CLI supports absolute paths. Relative paths are not relative to the config JSON directory.

| Field | Absolute path | Relative path is relative to |
|-------|---------------|------------------------------|
| review.skill.path | Read as-is (path.normalize) | Reviewed repo root repositoryPath (--repo / current repo) |
| commitMessage.skill.path | Same | Same (Git root for Create PR/MR) |
| pullRequestCreation.configFilePath | Each list item that is absolute is probed as-is | With --repo, relative to that repo root, else cwd. Comma-separated, first existing file |
| pullRequestReview.configFilePath | Same | Same |

A non-empty skill path ignores the matching id; missing or empty file errors. A non-empty overlay list where none exist is CONFIG_ERROR. Absolute overlay paths resolve without --repo; relative paths must pass --repo at the matching Git root (this skill's Create PR/MR / Review pass it by default).

---

## Field reference

Per config block: what it does, allowed values, how to change it. Paths are relative to root object smartCommitHostAgent.

### review — local Code Review / bridge review before Create PR/MR

Applies to: local code review, Create PR/MR (bridge before commit). Does not apply to review of an existing PR/MR.

| Field | Type / values | Notes |
|-------|---------------|-------|
| threshold | number, e.g. 6 | Pass when score > threshold (equal does not pass). Larger is stricter. Independent of pullRequestReview.threshold. |
| language | string, e.g. zh-cn / en | Natural language for review summary and details. |
| maxDiffChars | positive integer | Max diff characters sent to the model. Raise if truncated / context too long, or split the change. |
| skill.id | built-in ids below | When path is empty, load the CLI built-in review skill. This skill's default is code-review. |
| skill.path | path or "" | When non-empty, read only that file, ignore id, domain classified as generic. Absolute as-is; relative to reviewed repositoryPath (not the config directory). File must not be empty. |
| skill.promptTuning | string | Short instructions appended to the review turn. Put a full handbook in path, not this field. |

Built-in review.skill.id: code-review, frontend-code-review, mobile-code-review, python-code-review, golang-code-review, java-code-review, c-code-review, cpp-code-review, csharp-code-review, rust-code-review, php-code-review.

The CLI classifies the diff domain and writes it into the request (Detected diff domain). When filling the code-review turn: follow Review skill guidance in the request; if it says fallback to generic, do not complain about a skill mismatch — review for general correctness/safety/maintainability. Line-number annotations and per-line findings appear only in pull-request review / batch-review; local bridge does not have them.

### commitMessage — commit message when creating a PR/MR

| Field | Type / values | Notes |
|-------|---------------|-------|
| language | string, e.g. zh-cn / en | Language used when auto-generating the commit message. When zh-cn, protocol validation usually requires the subject to contain Chinese characters. |
| input | string | If non-empty: hybridGenerate=false validates and uses it; true uses it as User draft in the turn. Usually leave empty. |
| maxDiffChars | positive integer | Diff cap when generating a commit message. Must be >= 1000. |
| structure | subjectOnly / subjectBody / subjectBodyFooter | Max structure for generate and validate. Out-of-box subjectOnly: one-line subject only. |
| scope | auto / required / forbidden | Parenthesized scope policy for typed subjects (type: / type!:). Out-of-box forbidden: no parenthesized scope; CLI strips it; no second turn. auto: optional. required: must be type(scope):; missing fails immediately (no correction turn). forbidden: strips (scope) (feat(auth): becomes feat:, feat(api)!: becomes feat!:), no second turn. Gitmoji / non-typed (WIP, ordinary parentheses in a summary) unchanged. Overrides conflicting scope preference in the skill. Under required / forbidden, Conventional and Semantic subject shapes match; only auto still follows skill examples. No dedicated CLI flag or env override; one-time via --set=commitMessage.scope=... when stated in the request. Do not confuse with myPullRequest.listScope. |
| autoGenerate | true / false | When input is empty: true generates via a turn; false errors (no message source). |
| hybridGenerate | true / false | Only meaningful when input (or --commit-message) is non-empty. false: skip the commit-message turn; true: still issue the turn, request includes User draft, refine the draft rather than discard it. |
| skill.id | conventional / semantic / gitmoji | Built-in generate guidance when path is empty. Guides generation; what actually blocks is validation.protocol. They may differ. |
| skill.path | path or "" | When non-empty, read only that file, ignore id. Absolute as-is; relative to repo root. File must not be empty. |
| skill.promptTuning | string | Short instructions appended to the commit-message turn. |
| validation.protocol | none / conventional / semantic / gitmoji | Validation after generation. none skips protocol; conventional restricts type allowlist; semantic allows type: subject without restricting type; gitmoji requires emoji + space + text. Case-insensitive; empty string treated as none. |
| validation.pattern | JS regex or "" | Extra regex on the subject, stacked independently on protocol (e.g. protocol=conventional and pattern=^feat:\\s also fails fix:). Empty adds no extra layer. Invalid regex is CONFIG_ERROR. |
| validation.extractTicketIdFromBranch | true / false | true tries to parse a ticket id from the branch name (e.g. bugfix/xxx-PROJ-123) and write it into the commit message. |
| validation.requireTicketIdInMessage | true / false | true requires a ticket id in the commit message or validation fails. |

hybridGenerate actual paths:

- input non-empty and hybridGenerate=false: no turn, validate and use
- input non-empty and hybridGenerate=true: issue commit-message turn (request includes User draft)
- input empty and autoGenerate=true: generate from the diff
- input empty and autoGenerate=false: error (no message source)

When filling the commit-message turn: follow language / structure / protocol / scope / bundled skill in the request; if User draft is present, refine it, do not replace with an unrelated message; subjectOnly outputs one line. A scope overlay in the request beats skill examples: required must write type(scope): (short kebab-case from the changed area; bare type: is forbidden); forbidden uses only type: / type!:. hybrid: required may add scope to a draft that has none; a non-empty (scope) already on the draft must be kept as-is; forbidden strips parenthesized scope from the draft. required missing scope is COMMIT_MESSAGE_INVALID immediately; do not expect a second turn.

### git — Git actions in the Create PR/MR flow

| Field | Type / values | Notes |
|-------|---------------|-------|
| autoStageWhenNothingStaged | true / false | Whether to auto-stage related changes when the index is empty. If false, git add yourself first. |
| autoCommit | true / false | Whether to auto-create a commit after a passing review. false means review only, no commit in this flow. |
| autoPush | true / false | Whether to auto-push after commit. false can stop at a local commit. |
| pushTimeoutMs | positive integer (ms) | Push timeout; raise for slow networks or large repos. |

### pullRequest — platform connection (all PR/MR modes)

| Field | Type / values | Notes |
|-------|---------------|-------|
| provider | gitlab / github / auto | Platform used for create, review, list, batch-review, my-commit list. This skill defaults to auto (detect GitLab / GitHub from remotes). |
| apiBaseUrl | URL string | API root for a self-hosted instance (e.g. https://git.example.com/api/v4). Official public instances may leave empty. |
| authToken | "env:VARNAME" | Read the token from an env var. Keep env:SMART_COMMIT_PULL_REQUEST_AUTH_TOKEN; no plaintext. Local Code Review does not use this field; a missing env resolves to empty, and only commands that actually call the platform API will say the token is required. |
| remoteHost | hostname or URL with scheme, or "" | Git host for account scope of List my PRs/MRs, Batch-review, and List my commits. CLI normalizes to a hostname. Non-empty lets those modes skip reading local remotes. Resolution: pullRequest.remoteHost, then the deprecated myPullRequest.remoteHost, then local remotes. With provider=auto only github.com / gitlab.com are accepted; any other host is CONFIG_ERROR until provider is set to gitlab / github. workspace scope ignores it. Empty out of the box; for self-hosted GitLab, set it or ask first — do not silently list against the public internet. |

### pullRequestCreation — creating a PR/MR

| Field | Type / values | Notes |
|-------|---------------|-------|
| autoCreateAfterPush | true / false | Whether to open a PR/MR after a successful push. Set false to push without opening one. |
| configFilePath | path, comma-separated list, or "" | Repo-level creation overlay. Absolute, relative, or mixed (e.g. /etc/team/pr.creation.json, .smart-commit-pr.creation.json). The CLI / with-target-branch.sh take the first existing file and merge only smartCommitHostAgent.pullRequestCreation. Absolute probed as-is; relative with --repo relative to repo root, else cwd. Overlay must not contain configFilePath / autoCreateAfterPush. Shared pullRequest.* cannot go in the overlay. On Create PR/MR the script merges that overlay first, then writes the conversation targetBranch, then clears configFilePath in the temp config, so the conversation target beats overlay targetBranch. |
| targetBranch | branch name or "" | Merge target. Daily use: leave empty and let conversation "create MR to develop" override temporarily; do not rely on a dangerous fallback when empty. Empty target: bridge records a create error after push; pull-request create fails outright; neither guesses main. |
| titlePrompt | string | Short title instructions written into the pr-content turn. Non-empty skips "single commit subject overwrites title" and uses the turn-generated title. Do not put tokens / reviewer lists here. |
| descriptionPrompt | string | Short description instructions written into the pr-content turn (template points). Do not ask to invent tests, links, or approvals. |
| maxDiffChars | positive integer | Diff cap when generating title/description. Both bridge and pull-request create use this diff for the Host-Agent pr-content turn. |
| assignees | string array | Default assignees (platform usernames). Empty array means do not auto-assign. |
| reviewers | string array | Default reviewers. GitLab: usernames; GitHub: usernames, or org/team for a team. Missing accounts may warn or fail create. |
| labels | string array | Default labels. Empty array means no labels. Labels that do not exist on the platform are not auto-created. |
| milestone | string | Milestone. Numeric string treated as id; otherwise looked up by title. Missing milestone fails create. |
| draft | true / false | true creates a draft PR/MR (GitHub / GitLab behavior is not identical). |
| removeSourceBranch | true / false | Whether to delete the source branch after merge (GitLab; GitHub has no such field). |
| skipBranches | branch-name array | If the current branch is in the list, skip auto-creating a PR/MR (protects trunk, etc.). |

MR title is decided by the CLI (the turn must still provide a non-empty title):

- titlePrompt non-empty: use this turn's title (even if there is only 1 commit relative to target)
- titlePrompt empty and exactly 1 commit relative to target: use that commit subject (turn title is fallback only if subject is empty)
- multiple commits relative to target: use this turn's title
- both --title and --description provided: skip this turn
- description always uses this turn's generated body; do not paste the commit message as the description

### pullRequestReview — review an existing PR/MR (including each item in batch-review)

Applies to: Review existing PR/MR, Batch-review my PRs/MRs. Does not apply to local review / Create PR/MR.

| Field | Type / values | Notes |
|-------|---------------|-------|
| threshold | number, e.g. 6 | Pass when score > threshold. Only remote PR/MR review; changing it does not change review.threshold used by local / Create PR/MR. |
| autoApprove | true / false | Whether to approve on the platform after pass. Set false if you do not want auto-approve. |
| autoMerge | true / false | Whether to auto-merge after pass. Default true is risky; use dry-run for a trial, or set false. |
| summarySeverities | array of P0 / P1 / P2 / P3 | Severities written into the MR summary comment. Default excludes P2. |
| commentSeverities | array of P0 / P1 / P2 / P3 | Severities posted as inline comments. |
| skillPromptTuning | string | Only pull-request review / batch-review: overrides review.skill.promptTuning. Empty keeps review.skill.promptTuning. Does not change local bridge review. |
| skipSummaryOnPass | true / false | true: no summary comment on pass; false: still post. |
| skipCommentOnPass | true / false | true: no inline comments on pass; false: still post. |
| configFilePath | path, comma-separated list, or "" | Repo-level review overlay. Absolute / relative / mixed rules match creation overlay. CLI takes the first existing file and merges only smartCommitHostAgent.pullRequestReview. Overlay must not contain configFilePath. Shared pullRequest.* cannot go in the overlay. |

Requests for an existing PR/MR include line-number annotations and per-line findings: when filling the turn, copy visible lineNumber values; split the same root cause on multiple lines into multiple details. Local bridge / --review-only does not have these rules.

### myPullRequest — List my PRs/MRs and Batch-review my PRs/MRs

| Field | Type / values | Notes |
|-------|---------------|-------|
| listScope | account / workspace | account: list open MRs for the current token account on the given host; workspace: list from --repo / current workspace remotes. List and batch-review share this field. |
| listKinds | array of created / assigned / reviewer | List only: created = I created; assigned = assigned to me; reviewer = I am reviewer. Multi-select. Independent of batchReviewKinds. |
| batchReviewKinds | same | Batch-review only: role filter before serial review. Out-of-box reviewer+assigned (pending); does not default to reviewing ones I created. |
| remoteHost | hostname or URL with scheme | Deprecated. Fallback used only when pullRequest.remoteHost is empty. Move the value to pullRequest.remoteHost; setting both to different hosts means pullRequest.remoteHost wins. |

One-shot CLI overrides (the skill appends them from utterances; you need not edit JSON):

- List: --my-pull-request-list-scope, --my-pull-request-list-kinds, --pull-request-remote-host
- Batch-review: --my-pull-request-list-scope, --my-pull-request-batch-review-kinds, --pull-request-remote-host (batch uses batch-review-kinds, not list-kinds)
- The legacy --my-pull-request-remote-host still works in the CLI but this skill does not use it

### myCommit — List my commits

Applies to: List my commits (my-commit list) only. Reuses pullRequest.provider / apiBaseUrl / authToken / remoteHost. No Host-Agent turn.

| Field | Type / values | Notes |
|-------|---------------|-------|
| scope | account / workspace | account: enumerate repositories the token account is a member of, skip ones with no activity since the range start, and query each. workspace: only repositories resolved from --repo paths (or cwd); ignores remoteHost. Independent of myPullRequest.listScope. |
| range | today / yesterday / thisWeek / lastWeek / thisMonth / lastMonth / custom | Default range when the utterance gives none. Local calendar days of the machine running the CLI; weeks start on Monday. custom needs --start-date and --end-date (YYYY-MM-DD, inclusive, at most 31 days); the skill passes them only together with --my-commit-range custom, so leaving custom in the JSON without an utterance date is a CONFIG_ERROR. |
| authorAliases | string array | Extra author names / emails. Commits are matched by the token login, profile email, and these aliases; the profile display name is not used. Trimmed and de-duplicated case-insensitively. GitLab's substring author filter is re-checked locally for exact matches. |
| concurrency | integer 1-10 | Parallel repository workers. Higher is faster but burns rate limit. |
| requestDelayMs | integer 0-5000 | Minimum delay between API requests. Raise it when the provider throttles you. |
| includeMergeCommits | true / false | false hides merge commits. |
| outputFormat | full / compact | Summary style. compact (this skill's default): one summary line (range, total, repositories scanned, complete) plus a list of commit message first lines. full: adds CLI version / provider / account and a table with repo, short SHA, message, local time, branches, link. The skill always calls the CLI with --output json and renders this style itself; saying details / full or brief / only messages in the request overrides it for that turn. In the CLI's own --output text it picks the same two layouts. |

When the provider reports 5 or fewer remaining rate-limit requests, or returns a rate-limit error, the CLI stops early, keeps the records already collected, and reports complete: false (exit code still 0). GitHub records list the branches the commit was found on; GitLab records have no branch attribution.

One-shot CLI overrides (the skill appends them from utterances): --my-commit-scope, --my-commit-range, --start-date / --end-date (custom only), --my-commit-author-aliases, --my-commit-include-merge-commits, --pull-request-remote-host. There are no SMART_COMMIT_MY_COMMIT_* environment variables.

Print the full schema with: smart-commit-host-agent schema print --target config-file

---

## Multiple environments / multiple configs

| Approach | Notes |
|----------|-------|
| Edit the colocated default file | Personal global habits; simplest |
| SMART_GIT_CONFIG=/absolute/path/to/some.json | Temporarily or in CI point at another set; does not change files in the skill directory |
| Repo overlay (configFilePath) | Main config lists comma-separated paths, absolute / relative mixable. Review overlay is loaded automatically by the CLI; Create PR/MR creation overlay is merged by with-target-branch.sh. Relative paths are relative to --repo / repo root |
| One skill copy per tool | Different directories may hold different JSON; each uses its own (whichever copy was loaded this turn). Scripts do not switch copies across tools. To temporarily use another set, set SMART_GIT_CONFIG |

---

## Notes

- The Agent does not edit this business config during Create PR/MR / Review / List / Batch-review / List my commits (except the target temporary overlay). Personalize it locally, or state a value in the request for a one-time --set override.
- Default autoMerge: true: a live Review PR/MR or Batch-review my PRs/MRs may merge immediately; if unsure, say dry-run / trial first, or set autoMerge to false.
- List my PRs/MRs / Batch-review / List my commits ship with empty pullRequest.remoteHost and provider=auto; the CLI may fall back to public gitlab.com / github.com. For self-hosted GitLab, set pullRequest.remoteHost plus pullRequest.provider: "gitlab" (provider=auto rejects non-public hosts), or ask first; do not silently list against the public internet.
- This skill requires smart-commit-host-agent >= 0.1.7. Older CLIs silently ignore pullRequest.remoteHost and myCommit, may lack my-commit list and --set, and require --repo for pull-request review.
- List my commits custom ranges are at most 31 days; for longer periods the skill asks you to narrow the range (or use thisMonth / lastMonth).
- Batch-review filters with batchReviewKinds (default pending), independent of listKinds (default all three).
- If a diff is truncated or context is too long: raise review.maxDiffChars, or split into smaller MRs.
- review.threshold and pullRequestReview.threshold belong to different modes (local/Create PR/MR vs existing PR/MR) and do not override each other; both use score > threshold.
- commitMessage.validation.pattern is an extra subject regex stacked on protocol; they are independent.
- commitMessage.skill.id only guides generation; what blocks is validation.protocol. This skill's defaults: skill.id conventional, validation.protocol none.
- commitMessage.scope only governs typed-subject (scope), unrelated to myPullRequest.listScope; no dedicated CLI flag (one-time via --set). required failure does not open another commit-message turn; forbidden is stripped by the CLI with no second turn. Gitmoji does not grow a typed scope from this.
- hybridGenerate only issues a refinement turn when input / --commit-message is already present; empty input still follows autoGenerate.
- review.skill.path / commitMessage.skill.path / *.configFilePath all support absolute paths; relative paths are not relative to the JSON directory (skill files relative to repo root, overlays relative to --repo or cwd). See How to write paths above.
- A configured path whose files do not exist errors. On Create PR/MR the creation overlay is merged into the temp config by with-target-branch.sh (conversation targetBranch written last); review overlay is still loaded automatically by the CLI. The Agent must not merge overlay files by hand.
- If config resolve fails, fix the reported field and re-trigger the skill.
- The platform token still comes from the env var and is not replaced by JSON personalization. Local Code Review does not require that token; Create PR/MR / Review / List / Batch-review / List my commits do enforce it.

review.skill / commitMessage.skill are host-agent built-in templates, not other agent skills.
