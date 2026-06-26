# 久坐提醒直改状态方案

这份说明定义如何把用户的自然语言指令，直接映射成 `memory/heartbeat-state.json` 的状态修改。

目标：
- 用户说一句话，就能直接改提醒状态
- 不只写说明，而是形成稳定的状态编辑规则
- 让聊天控制和 heartbeat 共用同一份状态

## 核心原则

1. 用户明确控制，优先直接写状态
2. 状态修改要小而准，不要顺手改一堆无关字段
3. 改完后给一句简短确认
4. 能从当前时间安全重算的，就不要沿用旧状态强行推断

## 直改入口场景

适用于这类用户消息：
- 暂停久坐提醒
- 恢复久坐提醒
- 一小时别提醒
- 今天别提醒了
- 改成专注模式
- 改成学习模式
- 改成温和一点
- 我刚休息过了
- 我现在在开会
- 我回来了

## 推荐映射规则

### 1. 暂停提醒
示例：
- 暂停久坐提醒
- 关掉久坐提醒
- 先别提醒我

状态修改：
```json
{
  "enabled": false,
  "controlMode": "paused",
  "manualPauseReason": "manual-pause",
  "lastUserControlAt": now,
  "lastUserControlText": "暂停久坐提醒"
}
```

推荐回复：
- 已暂停久坐提醒。

### 2. 恢复提醒
示例：
- 恢复久坐提醒
- 打开久坐提醒
- 可以继续提醒我了

状态修改：
```json
{
  "enabled": true,
  "controlMode": "auto",
  "manualPauseReason": "",
  "suppressedUntil": 0,
  "lastUserControlAt": now,
  "lastUserControlText": "恢复久坐提醒",
  "lastSkippedReason": "",
  "estimatedSittingStartAt": now
}
```

推荐回复：
- 已恢复久坐提醒，我会从现在重新保守计时。

### 3. 一小时别提醒
示例：
- 一小时别提醒我
- 先静音一小时

状态修改：
```json
{
  "enabled": true,
  "controlMode": "suppressed",
  "manualPauseReason": "one-hour-pause",
  "suppressedUntil": now + 3600,
  "lastUserControlAt": now,
  "lastUserControlText": "一小时别提醒"
}
```

推荐回复：
- 好，先静音一小时。

### 4. 今天别提醒了
示例：
- 今天别提醒了
- 今天先别提醒我

状态修改：
```json
{
  "enabled": true,
  "controlMode": "suppressed",
  "manualPauseReason": "today-off",
  "suppressedUntil": endOfToday,
  "lastUserControlAt": now,
  "lastUserControlText": "今天别提醒了"
}
```

推荐回复：
- 好，今天先不提醒你了。

### 5. 切到专注模式
示例：
- 改成专注模式
- 我接下来要专注

状态修改：
```json
{
  "profile": "focus-friendly",
  "workState": "focus",
  "lastWorkStateChangeAt": now,
  "lastUserControlAt": now,
  "lastUserControlText": "切到专注模式"
}
```

推荐回复：
- 行，切到专注模式了。

### 6. 切到学习模式
示例：
- 改成学习模式
- 我现在在学习

状态修改：
```json
{
  "profile": "study",
  "workState": "study",
  "lastWorkStateChangeAt": now,
  "lastUserControlAt": now,
  "lastUserControlText": "切到学习模式"
}
```

推荐回复：
- 好，已经切到学习模式。

### 7. 改成温和一点
示例：
- 温和一点
- 提醒轻一点

状态修改：
```json
{
  "profile": "gentle",
  "lastUserControlAt": now,
  "lastUserControlText": "改成温和一点"
}
```

推荐回复：
- 好，我会用更温和的提醒节奏。

### 8. 我刚休息过了
示例：
- 我刚起来走过了
- 刚休息过了
- 我已经活动完了

状态修改：
```json
{
  "lastBreakAt": now,
  "lastBreakDetectedAt": now,
  "lastBreakSource": "manual",
  "estimatedSittingStartAt": 0,
  "lastEscalationLevel": "soft",
  "lastUserControlAt": now,
  "lastUserControlText": "我刚休息过了",
  "lastSkippedReason": ""
}
```

推荐回复：
- 收到，这次算你刚休息过，重新计时。

### 9. 我现在在开会
示例：
- 我现在在开会
- 接下来要开会

状态修改：
```json
{
  "workState": "meeting",
  "lastWorkStateChangeAt": now,
  "lastUserControlAt": now,
  "lastUserControlText": "我现在在开会"
}
```

可选：
- 根据需要设置一个短期 `suppressedUntil`

推荐回复：
- 好，我先按开会状态处理。

### 10. 我回来了
示例：
- 我回来了
- 回到电脑前了

状态修改：
```json
{
  "presence": "present",
  "lastPresenceChangeAt": now,
  "estimatedSittingStartAt": now,
  "lastUserControlAt": now,
  "lastUserControlText": "我回来了"
}
```

推荐回复：
- 收到，我从现在重新算。

## 状态修改安全规则

- 只改与当前指令直接相关的字段
- 不要因为切 profile 就重置所有提醒历史
- 不要因为恢复提醒就立刻发补偿提醒
- 涉及时间的字段，统一写 Unix 时间戳
- 对“今天别提醒了”这类语句，按用户时区计算当天结束

## 推荐实现流程

1. 识别用户指令意图
2. 读取 `memory/heartbeat-state.json`
3. 仅修改相关字段
4. 写回文件
5. 返回一条简短确认

## 常见冲突处理

### 用户说恢复提醒，但还在 suppressedUntil 内
- 用户明确恢复优先
- 直接清掉 `suppressedUntil`

### 用户说改成专注模式，但之前是 paused
- 只改 profile/workState 还不够
- 若用户语义明显要恢复使用，建议同时改 `enabled = true` 和 `controlMode = auto`
- 若语义只是预设模式，可只改 profile，不恢复提醒

### 用户说我刚休息过了，但当前 still paused
- 允许更新 break 状态
- 不必自动恢复提醒

## 最小可执行命令集

建议至少支持这 8 个：
- 暂停久坐提醒
- 恢复久坐提醒
- 一小时别提醒我
- 今天别提醒了
- 改成专注模式
- 改成学习模式
- 改成温和一点
- 我刚休息过了

## 最重要的一句

直改状态版的价值，不是多聪明，而是：

**用户说一句，状态就真的改了。**
