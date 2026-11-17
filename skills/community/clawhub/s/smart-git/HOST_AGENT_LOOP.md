# Host-Agent turn loop

`smart-commit-host-agent` does not call an external LLM HTTP API. When it needs model output the process exits **`needs_host_agent` (exit code 10)**; the host AI Agent writes the response and then resumes.

## Session directory

The files below are written by the CLI at runtime under --session / --session-base (default temp scha-sessions dir). They are not files inside the skill package; the Agent must not look for or bundle them from the skill directory.

```text
<sessionDir>/
  session.json
  bridge-state.json
  batch-review-state.json
  turns/
    0001.request.json
    0001.response.json
```

The first command uses --session-base plus a directory (prefer ${TMPDIR:-/tmp}/scha-sessions; on Windows with no TMPDIR, use %TEMP% or Git Bash /tmp).
Resume must use the same --session plus sessionPath from JSON.
On batch-review resume the CLI reads the batch progress file it wrote, skips completed URLs, and continues from the next one. The Agent only fills turn responses and resumes with --session; do not hand-edit that progress file.

## Request file (CLI to Agent)

Main fields of turns/NNNN.request.json:

| Field | Meaning |
|-------|---------|
| turnId | e.g. 0001; the response must echo it as-is |
| kind | complete or review |
| purpose | see table below |
| messages | role/content array; generate the answer as a conversation |
| responseSchema | description of the expected output shape (string) |
| attempt | attempt count |

## Response file (Agent to CLI)

Path: turns/{turnId}.response.json

    {
      "turnId": "0001",
      "content": "..."
    }

- turnId must match the request
- content is always a string
- If the schema wants a JSON object, JSON.stringify the object into content (do not put the object as sibling fields on the JSON root)

### purpose to content contract

| purpose | content |
|---------|---------|
| code-review or code-review:<url> | JSON.stringify of score, decision, summary, details. decision is pass or block. details has severity/message, optional filePath/lineNumber. For batch-review each MR's purpose is often code-review:<that MR URL> with the same shape. Must follow Review skill guidance and Detected diff domain in the request. When PR/MR review includes line-number annotations and per-line findings: copy the visible number into lineNumber; split the same root cause on multiple lines into multiple details. Local bridge has no line-number annotations |
| commit-message | Single-line or structure-allowed commit message as plain text. Follow the request language / structure / protocol / scope / bundled skill / promptTuning. If User draft is present (hybridGenerate=true), refine the draft; do not discard its intent. subjectOnly outputs a single line. protocol is none / conventional / semantic / gitmoji; pattern is validated by the CLI after the turn. commitMessage.scope (auto / required / forbidden) only governs typed-subject (scope): a scope overlay in the request beats skill examples; required must be type(scope): (kebab-case, derived from the changed area) and missing scope fails validation immediately with no correction turn; forbidden uses only type: / type!: (feat(auth): becomes feat:, feat(api)!: becomes feat!:); the CLI strips parenthesized scope with no second turn; auto may include it or not. Gitmoji / non-typed (e.g. WIP) are unchanged. hybrid: required may add scope to a draft that has none; a draft that already has scope must keep it as-is; forbidden strips parenthesized scope from the draft. Do not confuse with myPullRequest.listScope; no CLI flag |
| pr-content | JSON.stringify of title and description, both non-empty. bridge issues this turn after push, before creating the MR/PR; pull-request create issues it as well. Follow Title/Description prompt tuning. Do not paste the commit message as the description. The MR title is decided by the CLI (see below); this turn must still provide a non-empty title |
| probe | any probe text (diagnostics only) |
| report | report body (if AI report is enabled) |

Review language follows Review language in the request messages (config is often zh-cn).

Commands with no turn: my-pull-request list, my-commit list (and locally rendered report generate) never return needs_host_agent and do not use this loop.
Commands with turns (must use this section): bridge, pull-request create, pull-request review, my-pull-request batch-review, etc.

### code-review example

    {
      "turnId": "0001",
      "content": "{\"score\":8.5,\"decision\":\"pass\",\"summary\":\"Changes are clear; risk is manageable.\",\"details\":[]}"
    }

Score is relative to config review.threshold (or pullRequestReview.threshold for an existing PR/MR review): usually score > threshold is pass (same as the CLI gate; follow the request text). The request may include Review skill guidance; review against that checklist and domain hint, and do not invent a different output format.

### pr-content example

The turn response must still provide non-empty title and description. The title actually written to the MR/PR is decided by the CLI after the turn:

- titlePrompt non-empty: use this turn's generated title (even if there is only 1 commit relative to target)
- titlePrompt empty and exactly 1 commit relative to target: use that commit's subject as the MR title (this turn's title is a fallback only if the subject is empty)
- titlePrompt empty and multiple commits relative to target: use this turn's generated title
- Both --title and --description provided: skip this turn; do not overwrite the caller's title
- description always uses this turn's generated body; do not paste the commit message as the description

When there are multiple commits (generated title is used):

    {
      "turnId": "0003",
      "content": "{\"title\":\"Wire up tenant-tokens and remove mocks\",\"description\":\"## Summary\\n- ...\"}"
    }

## Agent loop pseudocode

First run:

    {CLI prefix} bridge --repo . --config "$CFG" --review-only --session-base "$SESSION_BASE" --output json

On needs_host_agent, read the request, write turns/{turnId}.response.json, then resume:

    {CLI prefix} bridge --repo . --config "$CFG" --review-only --session "$SESSION" --output json

Repeat until a terminal status. Same idea for pull-request create / pull-request review / my-pull-request batch-review: keep equivalent args except session, and replace --session-base with --session.

The CLI re-resolves config from the arguments on every resume (the session does not store it), so one-shot --set=path=value overrides must be passed again on each resume exactly as on the first run.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | success |
| 2 | blocked (review did not pass, etc.; any batch-review item not_passed is also 2) |
| 3 | config / input error |
| 4 | runtime error (batch-review includes an item error or cancelledRemaining > 0) |
| 10 | needs_host_agent — continue the loop, not a terminal failure |

## Safety boundary

- Do: read the request, write the response, generate content per schema, resume the CLI
- Do not: treat review details as a to-do list to auto-edit business code this turn
- Do not write authToken / tokens from env vars into replies or summaries
