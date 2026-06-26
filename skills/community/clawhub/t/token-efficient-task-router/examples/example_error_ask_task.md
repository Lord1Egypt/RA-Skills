# Example: Error Ask Task

## User request

`为什么这个脚本报错？`

## Route

- clarity: medium
- complexity: medium
- risk: low to medium
- token budget: Standard
- mode: Ask Mode

## Sample response

```markdown
## 判断

当前任务适合使用 Ask Mode，因为你目前是在做报错诊断，还没有授权直接修改脚本。

## 诊断

1. 可能原因：参数缺失、路径错误、依赖环境不一致。
2. 影响范围：当前脚本运行失败，但未必影响其他模块。
3. 风险等级：低到中。

## 建议

1. 先提供报错信息和触发命令。
2. 确认脚本依赖是否已安装。
3. 如果涉及代码修改，我再给你一个最小修复方案。
```
