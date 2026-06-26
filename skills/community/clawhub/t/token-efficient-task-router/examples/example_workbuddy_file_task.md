# Example: WorkBuddy File Task

## User request

`帮我处理一下这个文件夹。`

## Route

- clarity: low
- complexity: medium to complex
- risk: medium to high
- token budget: Standard
- mode: Interactive Routing Prompt with file-safety confirmation

## Sample response

```markdown
这个任务可能涉及文件操作。为了省 token，也避免误操作，我先请你选一个方式：

1. 只读分析，不改文件；
2. 先给计划，确认后再执行；
3. 新建副本，不覆盖原文件；
4. 允许修改指定文件，但需先列清单。

默认建议：2 或 3。
```
