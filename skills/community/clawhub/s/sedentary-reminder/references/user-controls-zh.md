# 久坐提醒用户控制说明

这份说明定义用户可以如何直接控制久坐提醒系统。

目标：
- 让用户能随时暂停、恢复、切换提醒风格和场景
- 让 heartbeat 和提醒逻辑尊重用户当前意图
- 尽量用少量、自然的中文指令就能完成控制

## 核心原则

1. 用户明确说停，就停
2. 用户明确说改模式，就立刻改
3. 用户明确说今天别提醒，就静默到当天结束或指定时间
4. 用户恢复提醒后，不要立刻补发一堆旧提醒
5. 用户控制优先级高于自动推断

## 推荐支持的控制动作

### 1. 暂停提醒
适用表达示例：
- 暂停久坐提醒
- 先别提醒我
- 关掉久坐提醒
- 今天先静音

推荐状态更新：
- `enabled = false`，或
- 保持 `enabled = true` 但设置较长的 `suppressedUntil`

推荐做法：
- **长期关闭**：`enabled = false`
- **临时静默**：保留 `enabled = true`，改 `suppressedUntil`

### 2. 恢复提醒
适用表达示例：
- 恢复久坐提醒
- 可以继续提醒我了
- 打开久坐提醒

推荐状态更新：
- `enabled = true`
- 如果 `suppressedUntil` 已设置，清零或清为过期值
- `lastSkippedReason = ""`

恢复后建议：
- 不要立即补发提醒
- 从当前时刻重新保守判断
- 必要时把 `estimatedSittingStartAt` 设为当前时间，避免一恢复就因旧时长触发

### 3. 暂停一段时间
适用表达示例：
- 一小时内别提醒我
- 下午三点前别提醒
- 今天别提醒了
- 两小时内静音

推荐状态更新：
- `enabled = true`
- 设置 `suppressedUntil = 指定时间戳`
- `lastSkippedReason = "manual-pause"`

### 4. 切换 profile
适用表达示例：
- 改成专注模式
- 改成温和一点
- 提醒勤一点
- 切到学习模式
- 用 balanced

推荐 profile：
- `balanced`
- `focus-friendly`
- `study`
- `gentle`

推荐状态更新：
- `profile = 对应值`
- `lastSkippedReason = ""`

### 5. 切换 workState
适用表达示例：
- 我现在在开会
- 我接下来要专注
- 我现在在学习
- 我只是随便刷刷

推荐状态更新：
- `workState = meeting | focus | study | casual | normal`
- `lastWorkStateChangeAt = now`

### 6. 手动标记已休息
适用表达示例：
- 我刚起来走过了
- 我已经活动完了
- 刚休息过了

推荐状态更新：
- `lastBreakAt = now`
- `estimatedSittingStartAt = 0`
- `lastEscalationLevel = "soft"`
- `lastSkippedReason = ""`

## 推荐新增状态字段

建议在 `memory/heartbeat-state.json` 的 `sedentary` 对象中新增：

```json
{
  "controlMode": "auto",
  "manualPauseReason": "",
  "lastUserControlAt": 0,
  "lastUserControlText": ""
}
```

### 字段说明
- `controlMode`
  - `auto`：自动判断
  - `paused`：用户明确关闭
  - `suppressed`：用户临时静默
- `manualPauseReason`
  - 记录原因，比如 `today-off`、`one-hour-pause`
- `lastUserControlAt`
  - 最近一次用户控制时间
- `lastUserControlText`
  - 最近一次用户控制原话或简化摘要

## 控制优先级

按这个优先级处理：
1. 用户明确控制
2. 当前安全 / 可打断性约束
3. 自动推断的 state
4. 默认 profile 规则

也就是说：
- 用户说停，自动逻辑不能偷偷继续提醒
- 用户说切 focus，自动逻辑不能继续按 casual 提醒

## Heartbeat 配合规则

Heartbeat 每次运行时，先检查：

1. `controlMode`
2. `enabled`
3. `suppressedUntil`

推荐行为：
- 如果 `controlMode = paused`，直接跳过
- 如果 `controlMode = suppressed` 且现在还没到时间，直接跳过
- 如果用户刚恢复提醒，不要立刻用历史坐姿时长轰炸式补发

## 推荐回复风格

用户发出控制指令后，回复应简短确认，不讲大段规则。

### 示例
- 已暂停久坐提醒。
- 好，先静音一小时。
- 行，切到专注模式了。
- 已恢复提醒，我会走保守策略，不会立刻连发。
- 收到，这次算你刚休息过，重新计时。

## 推荐实现策略

如果后续要把它做成真正可执行的聊天控制逻辑，建议：

1. 识别用户控制意图
2. 修改 `memory/heartbeat-state.json`
3. 返回一条简短确认
4. 让 heartbeat 在后续轮次自动读取最新状态

## 最实用的一组最小控制能力

如果先做 MVP，至少支持：
- 暂停提醒
- 恢复提醒
- 今天别提醒
- 一小时内别提醒
- 改成专注模式
- 改成学习模式
- 我刚休息过了

## 最重要的一句

好的久坐提醒，不只是“会提醒”，还要：

**用户一句话就能管住它。**
