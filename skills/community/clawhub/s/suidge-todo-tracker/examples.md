# Usage Examples

## Adding a Todo

```
User: 提醒我明天上午跟进那个插件更新问题
Agent: 好的，已添加到待跟进清单。明天上午我会提醒你。

[Agent writes to todo.json with follow_up_time set to tomorrow morning]
```

## Reminder Triggered

```
[Heartbeat detects follow_up_time reached]

Agent: 主人，你之前让我提醒你跟进插件更新问题，现在要处理吗？
```

## Completing a Todo

```
User: 已经完成了，不用跟进了
Agent: 好的，已标记为完成。

[Agent updates status to "completed" and sets completed_at]
```

## Viewing Todos

```
User: 查看待办事项
Agent: 你有 3 个待跟进事项：
1. [高优先级] 跟进插件更新问题 - 明天上午
2. [中优先级] 确认会议时间 - 下周一
3. [低优先级] 整理文档 - 无具体时间
```

## Cancelling a Todo

```
User: 取消那个文档整理的提醒
Agent: 好的，已取消。

[Agent updates status to "cancelled" and sets cancelled_at]
```

## Handling Ambiguous Time

```
User: 提醒我明天跟进
Agent: 好的，明天具体什么时间呢？

User: 上午吧
Agent: 好的，明天上午我会提醒你。

[Agent sets follow_up_time to tomorrow 09:00]
```
