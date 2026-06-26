# 久坐提醒 Heartbeat 模板

这份模板用于把 sedentary-reminder skill 接到 OpenClaw 的 heartbeat。

目标：
- heartbeat 负责周期检查
- 不是每次 heartbeat 都发提醒
- 只有满足条件时才输出一条合适的提醒
- 其余时候保持安静

## 设计原则

1. 先判断是否真的该提醒
2. 再决定提醒强度和文案
3. 如果现在不适合打断，就延后
4. 如果人不在，直接跳过
5. 如果刚提醒过，进入冷却

## 推荐检查频率

建议 heartbeat 大约每 10 到 15 分钟触发一次检查。

不要把 heartbeat 当成“每次都要说话”的定时器。

## 建议状态文件

建议在 `memory/heartbeat-state.json` 中至少维护这些字段：

```json
{
  "sedentary": {
    "enabled": true,
    "profile": "balanced",
    "lastReminderAt": 0,
    "lastBreakAt": 0,
    "estimatedSittingStartAt": 0,
    "lastEscalationLevel": "soft",
    "presence": "uncertain",
    "workState": "normal"
  }
}
```

可选扩展：

```json
{
  "sedentary": {
    "lastNaturalBoundaryAt": 0,
    "lastFocusBlockEndAt": 0,
    "lastMeetingEndAt": 0,
    "lastUserActivityAt": 0,
    "suppressedUntil": 0
  }
}
```

## 推荐 profile 默认值

### balanced
- firstReminderMin: 50
- followupMin: 25
- cooldownMin: 15
- strongerNudgeMin: 100

### focus-friendly
- firstReminderMin: 70
- followupMin: 30
- cooldownMin: 20
- strongerNudgeMin: 110

### study
- firstReminderMin: 45
- followupMin: 20
- cooldownMin: 15
- strongerNudgeMin: 100

### gentle
- firstReminderMin: 35
- followupMin: 20
- cooldownMin: 15
- strongerNudgeMin: 90

## Heartbeat 判断顺序

每次 heartbeat 到来时，按下面顺序判断：

1. 如果 `enabled != true`，结束
2. 如果当前时间早于 `suppressedUntil`，结束
3. 如果 `presence = away`，结束
4. 如果 `workState = meeting`，结束或延后
5. 计算连续久坐时长
6. 判断是否处于冷却期
7. 判断是否达到当前 profile 的提醒阈值
8. 如果没有达到阈值，结束
9. 如果达到阈值，再判断当前是否适合打断
10. 决定提醒强度：轻提醒 / 正常提醒 / 久坐加强提醒
11. 选一条不重复的中文文案输出
12. 更新 `lastReminderAt`

## 推荐提醒逻辑

### 轻提醒
触发条件示例：
- 刚达到首次提醒阈值
- 当前 workState = focus
- 当前没有自然断点但也不该继续拖太久

### 正常提醒
触发条件示例：
- 已达到标准阈值
- 当前 workState = normal / study / casual
- 距上次提醒已超过 cooldown

### 久坐加强提醒
触发条件示例：
- 连续久坐 >= strongerNudgeMin
- 人仍在电脑前
- 过去一段时间没有实际起身休息

## 自然断点优先

如果 heartbeat 能拿到这些信号，优先在这些时机提醒：
- 刚发完消息
- 刚结束一段任务
- 切换窗口或任务
- build / 上传 / 导出结束
- focus block 结束
- meeting 结束

如果拿不到，就按时长保守判断。

## 不该提醒的情况

满足任一情况，通常应直接跳过本轮：
- 正在 meeting
- `presence = away`
- 距离上次提醒还不到 cooldown
- 当前明显是高打断成本场景
- 用户刚回来，还没重新坐满一段时间

## 推荐输出风格

- 默认只输出一条短提醒
- 不要每次都解释规则
- 不要过度说教
- 不要连续多轮重复同一句

## 可直接放进 HEARTBEAT.md 的提示词模板

你可以把下面这段改成适合自己环境的 heartbeat 指令。

```markdown
# Sedentary reminder check

检查是否需要发送一条久坐提醒。

规则：
- 不是每次 heartbeat 都提醒
- 先看 sedentary 是否启用
- 读取 memory/heartbeat-state.json 中的 sedentary 状态
- 优先判断：presence、workState、lastReminderAt、lastBreakAt、estimatedSittingStartAt
- 如果人在离开状态，直接不提醒
- 如果正在 meeting，延后
- 如果还在 cooldown 内，不提醒
- 如果连续久坐未达到当前 profile 阈值，不提醒
- 如果达到阈值，再决定输出：轻提醒 / 正常提醒 / 久坐加强提醒
- 文案优先从 skills/sedentary-reminder/references/reminder-copy-zh.md 选，避免和上次过于重复
- 如果当前不适合打断，但又快到需要提醒的时候，可只更新状态，不发消息

如果不需要提醒，回复：HEARTBEAT_OK
如果需要提醒，只输出一条中文提醒，不要额外解释。
```

## 推荐最小可用方案

如果暂时没有完整状态来源，可以先用下面这套保守版：

- 默认 profile = balanced
- 每次 heartbeat 检查一次
- 如果距离上次提醒 < 15 分钟，不提醒
- 如果估算连续久坐 >= 50 分钟，发一条轻提醒
- 如果估算连续久坐 >= 100 分钟，发一条更明确的提醒
- 如果用户离开或锁屏，跳过
- 如果无法判断状态，宁可少提醒，不要乱提醒

## 实用建议

最容易做坏的地方有两个：

1. heartbeat 一来就发消息
2. 不做 cooldown，导致提醒太密

把这两个避开，体验就已经会好很多。
