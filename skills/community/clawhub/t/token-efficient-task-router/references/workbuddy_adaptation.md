# WorkBuddy Adaptation

## Default stance

WorkBuddy often touches local documents, folders, knowledge bases, and automation. Be conservative by default.

Recommended defaults:

- Ask or Plan first
- Craft only for clear low-risk tasks
- file modification requires Plan
- batch operations require confirmation
- knowledge-base organization requires a plan first
- file-scope budget should be confirmed before broad reads
- batch tasks should default to a sample batch before full rollout

## WorkBuddy scope budget

When a folder or document-library task appears large, ask the user to choose scope first:

- `先看 3 个文件`
- `先看 10 个文件`
- `先看一个子文件夹`
- `全目录处理`

Default recommendation: start with the smallest representative scope.

## Interactive routing in WorkBuddy

When local files or folders are involved, add a file-safety confirmation:

1. 只读分析，不改文件
2. 先生成修改计划
3. 新建副本，不覆盖原文件
4. 允许修改指定文件，但需先列清单

Default recommendation: `2` or `3`.

## Batch and knowledge-base handling

For large WorkBuddy tasks, prefer this sequence:

1. list the materials or files first
2. group them
3. identify risk points
4. process one sample batch
5. expand only after confirmation

Do not default to whole-folder execution on the first turn.

## WorkBuddy prompt examples

- `请用 token-efficient-task-router 判断这个任务应进入什么模式。`
- `请按 Plan Mode 先给我整理方案，不要直接改文件。`
- `这个报错先用 Ask Mode 诊断，不要修改代码。`
- `这是明确的小任务，请用 Craft Mode 直接生成结果。`
