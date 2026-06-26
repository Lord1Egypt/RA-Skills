# Example: Pairing with Installed Khazix Skills

## Context

The following local skills are installed:

- `hv-analysis`
- `khazix-writer`
- `neat-freak`

## Recommended pairing logic

### 1. Deep research first, then route

When the user wants a real deep research report, let `token-efficient-task-router` decide whether the task truly needs full depth first.

If yes, pair with:

- `hv-analysis` for systematic deep research

Good entry prompt:

```text
先用 token-efficient-task-router 判断这个研究任务值不值得做成完整深度报告。如果值得，再进入 hv-analysis。
```

### 2. Long-form writing after scope lock

When the user wants a public article or long-form write-up, first use the router to confirm:

- whether a full draft is needed
- whether a sample opening is enough
- whether the scope is already stable

Then pair with:

- `khazix-writer` for article drafting

Good entry prompt:

```text
先用 token-efficient-task-router 判断我现在需要的是文章提纲、样本段落，还是完整长文。确认后再进入 khazix-writer。
```

### 3. Session cleanup at the end

When a milestone is complete, pair with:

- `neat-freak` for cleanup and knowledge reconciliation

Good entry prompt:

```text
这个阶段做完了。先用 token-efficient-task-router 判断需要同步哪些文档和记忆，再按 neat-freak 的方式收尾。
```

## Why this pairing works

The router prevents the downstream skill from triggering too deep, too broad, or too early.

In practice:

- `token-efficient-task-router` decides whether depth is justified
- the installed Khazix skill does the specialized work
- the result is lower token waste and cleaner execution boundaries

## Note

Newly installed skills usually require a Codex restart before they are reliably available in fresh sessions.
