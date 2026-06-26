# 久坐提醒 Break 识别规则

这份说明定义系统如何把 `away / idle / lock / sleep / 明确离开` 识别为一次真实休息或自然中断。

目标：
- 不让提醒系统把“人已经离开去活动了”还继续算作连续久坐
- 自动把明显的离开行为当作 break
- 让回来后的提醒从更合理的时间重新计算

## 核心原则

1. 真实 break 比提醒更重要
2. 人离开后，连续久坐计时应尽量停止
3. 回来后不要立刻按离开前的旧时长催促
4. 无法确定时，宁可保守，不乱认定

## 什么算 break

### 强 break 信号
以下情况通常可以直接当作一次 break：
- 屏幕锁定
- 设备休眠
- 用户明确离开电脑
- presence 持续为 `away` 达到阈值
- 用户手动说自己已经起来活动了

### 弱 break 信号
以下情况不一定直接算 break，但可作为候选：
- 长时间 idle
- presence 从 `present` 变成 `uncertain` 并持续较久
- 应用切换减少、操作明显中断

## 推荐 break 判定阈值

### 明确 away
- `presence = away` 且持续 **5 到 10 分钟**
- 推荐直接认定为一次 break

### uncertain
- `presence = uncertain` 时先不要立刻认定
- 若 uncertain 持续 **10 到 15 分钟**，可以保守视为 break 候选

### lock / sleep
- 一旦确认锁屏或休眠，通常可直接认定为 break

### 短暂离开
- 少于 **3 到 5 分钟** 的短离开，不一定算 break
- 更适合作为“自然中断”而不是正式 break

## 推荐新增状态字段

建议在 `memory/heartbeat-state.json` 的 `sedentary` 中新增：

```json
{
  "lastAwayStartedAt": 0,
  "lastIdleStartedAt": 0,
  "lastBreakDetectedAt": 0,
  "lastBreakSource": "",
  "breakMinSeconds": 300
}
```

### 字段说明
- `lastAwayStartedAt`
  - 最近一次进入 away 的开始时间
- `lastIdleStartedAt`
  - 最近一次进入 idle / uncertain 的开始时间
- `lastBreakDetectedAt`
  - 最近一次系统自动识别到 break 的时间
- `lastBreakSource`
  - break 来源，比如 `away`、`lock`、`sleep`、`manual`
- `breakMinSeconds`
  - 最短 break 时长阈值，默认 300 秒

## 状态更新规则

### 当 presence 从 present 变成 away
- 如果 `lastAwayStartedAt = 0`，写入当前时间
- 更新 `lastPresenceChangeAt`
- 不要立刻把它算成 break，先等是否持续

### 当 away 持续超过阈值
认定 break，并更新：
- `lastBreakAt = now`
- `lastBreakDetectedAt = now`
- `lastBreakSource = "away"`
- `estimatedSittingStartAt = 0`
- `lastEscalationLevel = "soft"`
- `lastSkippedReason = "away"`

### 当检测到 lock / sleep
可直接认定 break，并更新：
- `lastBreakAt = now`
- `lastBreakDetectedAt = now`
- `lastBreakSource = "lock"` 或 `"sleep"`
- `estimatedSittingStartAt = 0`
- `lastEscalationLevel = "soft"`

### 当 presence 从 present 变成 uncertain
- 如果 `lastIdleStartedAt = 0`，写入当前时间
- 暂不直接认定 break

### 当 uncertain 持续超过阈值
可保守认定为一次 break 候选，尤其当同时满足：
- 最近没有明显活动
- 没有会议迹象
- 没有持续输入迹象

若认定，则更新：
- `lastBreakAt = now`
- `lastBreakDetectedAt = now`
- `lastBreakSource = "idle"`
- `estimatedSittingStartAt = 0`

### 当用户回来 present
- 清理 `lastAwayStartedAt` 和 `lastIdleStartedAt`
- 如果当前 `estimatedSittingStartAt = 0`，可把现在作为新的潜在坐下起点
- 不要立刻按之前的连续久坐时长补发提醒

## break 与自然中断的区别

### break
意味着：
- 可以重置连续久坐时间
- 下次提醒从新的 sittingStart 重新算

### 自然中断
意味着：
- 当前不提醒
- 但不一定足够长到视为 break

简化建议：
- **离开很短** -> 自然中断
- **离开够久** -> break

## Heartbeat 推荐判断顺序

每次 heartbeat 可按下面顺序处理：

1. 更新当前时间戳
2. 判断 presence
3. 如果进入 away，记录 `lastAwayStartedAt`
4. 如果进入 uncertain，记录 `lastIdleStartedAt`
5. 如果 away / idle 持续超过阈值，认定 break
6. 如果已认定 break，重置 sittingStart
7. 如果用户重新 present，从当前时间重新开始保守计时
8. 再判断本轮要不要提醒

## 推荐默认参数

- `breakMinSeconds = 300`，也就是 5 分钟
- `uncertainBreakSeconds = 600`，也就是 10 分钟
- `shortAwayIgnoreSeconds = 180`，也就是 3 分钟

## 与用户控制的配合

如果用户手动说：
- 我已经活动过了
- 我刚起来走过了

优先直接认定 break，不需要再等自动识别。

推荐更新：
- `lastBreakSource = "manual"`
- `lastBreakAt = now`
- `estimatedSittingStartAt = 0`

## 推荐输出行为

Break 被自动识别时，通常**不需要主动发消息**。

它应该主要用于：
- 重置计时
- 降低误报
- 避免回来后马上被催

## 最重要的一句

好的 break 识别不是“抓到用户离开”，而是：

**别把已经起身活动过的人，还当成一直坐着。**
