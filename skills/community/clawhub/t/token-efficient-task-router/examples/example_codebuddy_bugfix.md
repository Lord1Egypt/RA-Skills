# Example: CodeBuddy Bugfix

## User request

`这个报错帮我修一下。`

## Recommended route

- primary focus: `ask-diagnose`
- secondary focus: `codebuddy-code`

## Why

- the context is incomplete
- a full repo scan would waste tokens
- the safest first step is to narrow the scope to the most relevant files

## Sample response

```markdown
这个代码任务先确认范围：

[1 只诊断]
[2 只读 1-3 文件]
[3 只改一个点]
[4 分阶段重构]

默认建议：`2` 或 `3`
```
