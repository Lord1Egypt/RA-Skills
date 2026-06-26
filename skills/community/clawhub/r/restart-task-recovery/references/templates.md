# Templates

## Checkpoint entry template

```md
### <sessionKey>
- Agent: <agent>
- Goal: <goal>
- Last done: <done>
- Next: <next>
- Blockers: <none|...>
- Resume message: Continue where you left off. Last completed: <done>. Next: <next>.
```

## User update template

```md
重启已完成，已开始恢复任务：
- 已恢复：<list>
- 待确认：<list>
- 需人工处理：<list>
```

## Manual confirmation template (V5)

```md
以下恢复动作存在潜在非幂等风险，需你确认后再执行：
- <sessionKey>: <reason>
- <sessionKey>: <reason>

回复“确认执行全部”或逐条确认。
```

## Resume message variants

### Generic
Continue where you left off. The previous model attempt may have failed or timed out. Resume from the next unfinished step.

### Tool-call retry
Continue where you left off. Last completed: <done>. Retry the failed tool call and continue with <next>.

### Validation-first
Continue where you left off. First verify current state/results, then proceed with <next> to avoid duplicate writes.
