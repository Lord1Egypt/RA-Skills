# Commands

Use explicit, chat-friendly commands first. Expand aliases only after the base set is stable.

## Switching

### Prefix switch + send

- `{agent} ...`

Examples:

- `技术助手 帮我看日志`
- `文案助手 改一下这段话`
- `AgentB 接手这个需求`

Use placeholders or sample names only as illustrations. Do not assume other users share the same naming system.

### Direct switch

- `切到{agent}`
- `切换到{agent}`
- `回到{defaultAgent}`

## Status

- `当前是谁`
- `现在是谁`
- `你是谁`
- `角色列表`
- `有哪些助手`

## Reset

### Current session

- `重置当前`
- `清空当前上下文`

### Target agent

- `清空{agent}`
- `只重置{agent}`

## Summary view

- `查看当前上下文摘要`
- `当前上下文摘要`
- `查看摘要`
- `查看{agent}上下文摘要`

## Handoff

- `转给{agent}`
- `交给{agent}`
- `让{agent}接手`
- `总结后交给{agent}`

## UX guidance

- keep direct router replies short
- allow trailing punctuation when practical
- prefer silent handoff: confirm transfer first, let the target agent answer on the next user turn
- do not overfit commands to one project's private role names if the system is meant to be shared publicly
