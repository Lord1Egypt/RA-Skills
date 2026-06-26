# Example: Need Calibration

## User request

`帮我把这个知识库全面整理好，并生成一份完整报告。`

## Why calibration is needed

- the user asks for a large final artifact
- the real need may only be a direction or a sample
- full expansion may waste many tokens

## Recommended response

```markdown
为了避免非必要消耗，我先确认你真正需要的是哪一种结果：

1. 只要判断和下一步
2. 先做一个样本 / 一小部分
3. 先给阶段方案，再逐步推进
4. 一次性完整处理

默认建议：2 或 3。
```

## Why this is more efficient

If the user chooses `2` or `3`, the agent can validate the direction before generating a large report or touching the full knowledge base.
