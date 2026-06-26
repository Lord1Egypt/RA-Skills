# Example: Focus Activation

## User request

`帮我看看这个知识库问题下一步怎么做，先别展开。`

## Correct focus

- primary focus: `ask-diagnose`
- secondary focus: `ima-lite`

## Why

- the user wants next-step advice, not a full report
- the user explicitly says not to expand
- this is likely happening in a lightweight knowledge conversation

## What should be loaded

- `references/ask_mode.md`
- `references/ima_copilot_runtime_protocol.md`

## What should not be loaded yet

- full Plan Mode details
- full Expert Mode details
- full file-safety workflow
- artifact-generation templates

## Sample response

```markdown
我先按 Ask Mode 处理，只看你当前这个问题，先给你极简结果。

判断：现在更适合先确认问题范围。
下一步：先锁定最相关的 3 条材料，再决定要不要展开。
```
