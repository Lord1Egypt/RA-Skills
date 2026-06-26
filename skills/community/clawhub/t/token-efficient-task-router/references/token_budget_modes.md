# Token Budget Modes

## Micro Mode

Use when the user says:

- `简单说`
- `一句话`
- `只给结论`
- `极简`

Target length: 50-200 Chinese characters.

## Standard Mode

Default mode for most tasks.

Target length: 300-1500 Chinese characters.

## Deep Mode

Use only when the user clearly asks for:

- `深度分析`
- `完整展开`
- `详细说明`
- `系统方案`

Target length: 1500-4000 Chinese characters.

## Artifact Mode

Use for files, templates, code, skills, or long documents.

Rules:

1. write the long artifact into files when possible
2. keep chat output short
3. do not duplicate the full file content in chat unless necessary
4. report path and usage
5. generate long artifacts in modules when appropriate

Do not choose Artifact as the first move when a decision-only answer or a sample would satisfy the real need.

## Reuse rule

If the user already selected a depth in the current session and the task type did not materially change, keep that depth by default instead of asking again.

## iMA note

In iMA Copilot, default to `Micro` or short `Standard` for the first turn unless the user explicitly asks for a full analysis.
