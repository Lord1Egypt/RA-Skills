# Example: Button-guided Chat

## User request

`帮我把这个资料库都整理好。`

## Why a button-guided response is better

- the task is large
- the real need may still be unclear
- the user should be able to confirm with one tap or one short reply

## Recommended response

```markdown
为了避免误判和无效消耗，你先选一个：

[1 只要结论]
[2 先做样本]
[3 分阶段]
[4 一次做完]

默认建议：`2` 或 `3`
```

## Plain-text fallback

The user can also reply:

- `2`
- `先做样本`
- `分阶段`

## Safety behavior

If the user chooses full delivery for a high-risk file task, the skill should still route into Plan Mode before execution.
