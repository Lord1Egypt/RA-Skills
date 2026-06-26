# 久坐提醒状态自更新规则

这份说明定义 heartbeat 在每次运行后，应该如何维护 `memory/heartbeat-state.json` 中的久坐状态。

目标：
- 让 heartbeat 不只是会判断，还会持续积累状态
- 下次判断时有连续上下文
- 避免每一轮都像第一次运行

## 核心原则

1. 能更新状态时就更新，但不要伪造精确信号
2. 无法确认时，宁可保守
3. 提醒是否发送，和状态是否更新，是两件事
4. 即使本轮不发消息，也可能需要更新状态

## 建议维护字段

```json
{
  "lastChecks": {
    "sedentary": 0
  },
  "sedentary": {
    "enabled": true,
    "profile": "balanced",
    "lastReminderAt": 0,
    "lastBreakAt": 0,
    "estimatedSittingStartAt": 0,
    "lastEscalationLevel": "soft",
    "presence": "uncertain",
    "workState": "normal",
    "suppressedUntil": 0,
    "lastNaturalBoundaryAt": 0,
    "lastFocusBlockEndAt": 0,
    "lastMeetingEndAt": 0,
    "lastUserActivityAt": 0,
    "lastPresenceChangeAt": 0,
    "lastWorkStateChangeAt": 0,
    "lastSuggestedBreakAt": 0,
    "lastSkippedReason": "",
    "lastReminderText": ""
  }
}
```

## 每轮 heartbeat 都该更新的字段

### 1. lastChecks.sedentary
每次运行都更新为当前时间戳。

### 2. presence
如果本轮能判断 presence，就写回最新值。

### 3. workState
如果本轮能判断 workState，就写回最新值。

### 4. lastUserActivityAt
如果看到近期活跃迹象，就更新。

## presence 更新规则

### 当 presence 变成 present
- 更新 `presence = present`
- 如果之前是 `away`，更新 `lastPresenceChangeAt`
- 如果 `estimatedSittingStartAt = 0`，可把当前时间视为新的潜在坐下起点
- 不要因为刚回来就立刻提醒

### 当 presence 变成 uncertain
- 更新 `presence = uncertain`
- 更新 `lastPresenceChangeAt`
- 保留现有 `estimatedSittingStartAt`，但后续判断更保守

### 当 presence 变成 away
- 更新 `presence = away`
- 更新 `lastPresenceChangeAt`
- 可视为一次自然中断
- 将 `estimatedSittingStartAt` 重置为 0
- 如果 away 持续明显成立，也可以把这次视为 break，并更新 `lastBreakAt`

## workState 更新规则

### 当 workState 发生变化
- 更新 `lastWorkStateChangeAt`
- 写回新的 `workState`

### 如果进入 meeting
- 可设置 `suppressedUntil` 为一个短期未来时间，避免会中频繁判断
- 更新 `lastSkippedReason = meeting`

### 如果 meeting 结束
- 更新 `lastMeetingEndAt`
- 清理过期的 meeting 抑制状态
- 不要自动马上提醒，除非也满足久坐阈值

### 如果 focus 结束
- 更新 `lastFocusBlockEndAt`
- 这是一个较好的自然断点

## sittingStart 更新规则

### 什么时候设置 estimatedSittingStartAt
在这些情况可以设置或重置：
- 从 away -> present，且重新开始电脑活动
- 明确发生 break 后重新进入工作
- 原值为 0，且用户当前明显在持续工作

### 什么时候不要乱改
不要因为一次 heartbeat 没拿到完整信息，就重置 `estimatedSittingStartAt`。

### 什么时候清零
这些情况可以清零：
- 用户 away
- 明确发生 break
- 用户手动标记已起身活动

## reminder 更新规则

### 如果本轮发出了提醒
更新：
- `lastReminderAt = now`
- `lastSuggestedBreakAt = now`
- `lastReminderText = 本轮提醒文案`
- `lastSkippedReason = ""`

同时根据提醒强度更新：
- 轻提醒 -> `lastEscalationLevel = soft`
- 正常提醒 -> `lastEscalationLevel = standard`
- 久坐加强提醒 -> `lastEscalationLevel = firm`

### 如果本轮没有发提醒
不要改 `lastReminderAt`。
但可以更新：
- `lastSkippedReason`
- `presence`
- `workState`
- `lastChecks.sedentary`

## skippedReason 建议值

可用这些短值：
- `disabled`
- `away`
- `meeting`
- `cooldown`
- `below-threshold`
- `focus-deferral`
- `uncertain-presence`
- `suppressed`
- `manual-pause`

## break 更新规则

### 可以认定为一次 break 的情况
- presence 明确进入 away 并持续了一段时间
- 用户显式说自己去活动了
- 外部自动化明确写入了 break 事件

### 认定为 break 后
更新：
- `lastBreakAt = now`
- `estimatedSittingStartAt = 0`
- `lastEscalationLevel = soft`

## 冷却与抑制更新规则

### cooldown
cooldown 不一定单独存字段，只要通过 `lastReminderAt` 计算即可。

### suppressedUntil
适合用于：
- meeting 中临时静默
- 用户手动要求暂停提醒
- 某个高打断场景临时跳过

如果当前时间已超过 `suppressedUntil`，后续可恢复正常判断。

## 推荐自更新顺序

每次 heartbeat 执行时，推荐顺序：

1. 记录 `lastChecks.sedentary = now`
2. 读取现有 sedentary 状态
3. 判断并更新 presence
4. 判断并更新 workState
5. 必要时更新 `estimatedSittingStartAt`
6. 判断本轮是否需要提醒
7. 如果提醒，更新 reminder 相关字段
8. 如果不提醒，更新 `lastSkippedReason`
9. 将新状态写回 `memory/heartbeat-state.json`

## 最小可用自更新策略

如果暂时拿不到复杂状态，也至少做到：

- 每轮更新 `lastChecks.sedentary`
- 发提醒时更新 `lastReminderAt`
- 用户离开时清掉 `estimatedSittingStartAt`
- 识别跳过原因并写入 `lastSkippedReason`

## 最重要的一句

自更新逻辑的目标不是“记录得很华丽”，而是：

**让下一次 heartbeat 能基于上一次结果做更稳的判断。**
