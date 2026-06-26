# Example: iMA Lite Session

## User request

`帮我分析一下知识库里的内容，写个完整报告。`

## Why this needs the iMA runtime protocol

- defaulting to a full report is expensive
- the scope is unclear
- iMA chat benefits from a one-screen first reply
- the skill should lock behavior before expanding

## Recommended first reply

```markdown
我先按 Plan Mode 处理，只看最相关的 3 条材料，先给你标准结果。

判断：这是知识库任务，直接写完整报告会比较费 token。
范围：先不读全部资料，先抓最相关内容。
下一步：回复 `1继续`、`2展开`、`5只列材料`。
```

## If the user replies

`2展开`

## Recommended second reply

```markdown
结论：目前最值得先看的主题有 3 组：____、____、____。
范围：我先按主题归纳，不直接扩成完整报告。
下一步：如果你要，我再继续展开其中一组。
```
