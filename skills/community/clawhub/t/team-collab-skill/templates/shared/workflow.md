# 团队协作工作流

## 任务流转

```
用户提需求
    ↓
主 Agent 判断类型 → 分发给产品/研发/运营
    ↓
Agent 执行 → 输出结果
    ↓
更新状态文件 → 汇报给用户
```

## 状态同步

每个任务完成后：
1. 更新 `memory/agents/{角色}-agent.md`
2. 重要发现写入 `memory/lessons.md`
3. 决策写入 `memory/shared/decisions.md`
