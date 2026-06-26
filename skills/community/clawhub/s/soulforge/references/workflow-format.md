# Workflow YAML Format

Workflows live in `workflows/<name>/workflow.yml` inside the Soulforge install directory.

## Security / trust model

Soulforge workflows are a trusted-operator orchestration surface, not a safe sandbox for arbitrary user input.

Important boundaries:
- `{{task}}` and custom `--var` values should be treated as untrusted text unless the operator explicitly trusts the source.
- Workflow `input` is executor prompt content, not a shell command template.
- Do not construct shell commands by concatenating untrusted `{{task}}` / `--var` values.
- External CLIs such as Codex, Claude Code, and OpenClaw may have powerful execution capabilities; workflow authors are responsible for using them in trusted, operator-controlled contexts.
- Callback commands are delivery wrappers. Prefer passing through `{{callback_message}}` unchanged rather than inventing callback bodies in shell snippets.

## Schema

```yaml
id: my-workflow           # unique identifier
name: My Workflow         # display name
version: 1
description: |
  What this workflow does.

defaults:                 # applied to all steps unless overridden
  executor: claude-code   # claude-code | codex | codex-cli | openclaw | manual
  model: opus             # model passed to executor CLI when relevant
  timeout: 600            # seconds per step
  max_retries: 2

steps:
  - id: step-name
    executor: claude-code        # override default executor
    model: opus                  # override default model
    workdir: "{{workdir}}"       # working directory for this step
    type: single                 # single | loop | switch
    timeout: 300                 # override default timeout
    max_retries: 1
    input: |                     # prompt/instructions sent to executor
      Instructions with {{template_variables}}.
      Reply with structured output.
    output_schema:               # required for manual steps and recommended for typed completion
      type: object
      properties:
        status:
          type: string
    expects: "STATUS: done"      # optional string the output must contain
    callback_message: "{{run_id}} {{step_id}} {{step_status}}: {{task}}"
    on_fail:                     # optional failure handling
      retry_step: step-name      # which step to retry
      max_retries: 3
      escalate_to: review-step   # manual step on exhaustion
```

## Executor Types

| Executor | What it does |
|----------|-------------|
| `claude-code` | Runs Claude Code CLI (`claude`) with the step's input as prompt. |
| `codex` / `codex-cli` | Runs Codex CLI with the step's input as prompt. |
| `openclaw` | Sends work to an OpenClaw agent via the OpenClaw CLI. |
| `manual` | Human/operator completion point. The step waits for `soulforge complete ...` with structured output. |

## Template Variables

Steps can use `{{variable}}` placeholders. Built-in variables include:

| Variable | Source |
|----------|--------|
| `{{task}}` | The task string passed to `soulforge run` |
| `{{workdir}}` | The working directory for this run |
| `{{branch}}` | The git branch name |
| `{{build_cmd}}` | From `--var build_cmd=…` |
| `{{test_cmd}}` | From `--var test_cmd=…` |
| `{{run_id}}` | The unique run ID |
| `{{rejection_feedback}}` | Feedback from a rejected/manual retry loop |

Custom variables are passed via `--var key=value` flags.

Step outputs are also available as variables in subsequent steps. For example, if the `plan` step outputs structured `stories`, later steps can reference `{{stories_json}}` and related derived fields when provided by the runtime.

## Loop Steps

For iterating over a list (for example, implementing multiple stories):

```yaml
- id: implement
  type: loop
  over: stories
  as: story
  steps:
    - id: implement-story
      type: single
      executor: codex-cli
      input: |
        CURRENT STORY: {{story.title}}
        ACCEPTANCE: {{story.acceptance}}
```

## Switch Steps

Use `type: switch` for explicit routing decisions:

```yaml
- id: review-plan-branch
  type: switch
  switch:
    decision_var: plan.status
    routes:
      approved: implement
      retry: plan
```

## Manual Steps

Manual steps are typically `type: single` with `executor: manual`.

```yaml
- id: review-plan
  type: single
  executor: manual
  input: |
    Review the proposed plan and choose approved or retry.
  output_schema:
    type: object
    properties:
      status:
        type: string
        enum: [approved, retry]
      notes:
        type: string
```

Manual steps without `output_schema` are invalid workflow authoring.

## Example: Feature Development

The built-in `feature-dev` workflow implements a full development pipeline:

1. **plan** — decompose task into ordered user stories
2. **review-plan** (`executor: manual`) — human reviews the plan with structured output
3. **implement** (`type: loop`) — implement each story or work item
4. **verify** — verify acceptance criteria
5. **test** — run broader tests
6. **pr** — create pull request with `gh pr create`
7. **review-loop** / **final-review** (`executor: manual`) — operator review before merge

All executor prompts should be treated as trusted/operator-authored workflow content, not arbitrary shell templates.
