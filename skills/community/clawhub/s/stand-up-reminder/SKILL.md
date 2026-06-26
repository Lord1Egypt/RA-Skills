---
name: stand-up-reminder
description: 创建「站起来活动」久坐提醒。当用户说"提醒我站起来"、"久坐提醒"、"每小时提醒活动"、"设置站立提醒"、"stand up reminder"、"站立提醒"等时触发。自动创建工作日（周一至周五）定时提醒的 cron 任务，支持自定义开始/结束时间、提醒间隔、多语言（中/英/日）、文案风格（活泼/简洁/严肃/励志）、节假日跳过。
---

# Stand-Up Reminder Skill

通过 cron 任务在工作日定时提醒用户站起来活动，避免久坐伤身。

## 快速创建流程

### 1. 收集参数（未提供时使用默认值，无需逐一询问）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 开始时间 | 8:30 | 每天第一次提醒 |
| 结束时间 | 17:30 | 每天最后一次提醒 |
| 间隔 | 60 分钟 | 提醒频率 |
| 语言 | zh（中文） | zh / en / ja |
| 文案风格 | fun（活泼） | fun / minimal / formal / motivational |
| 节假日跳过 | 否 | 是否跳过中国法定节假日 |
| 时区 | Asia/Shanghai | 按用户实际时区调整 |

### 2. 构造 cron 表达式

- 默认（8:30 起，每小时）：`30 8-17 * * 1-5`
- 整点提醒（9:00 起）：`0 9-17 * * 1-5`
- 每 90 分钟（9:00 起）：`0 9,10,12,13,15,16 * * 1-5`（手动列举时间点）

### 3. 选择提醒文案

从 `references/messages.md` 中按语言和风格选取一条文案填入 `payload.message`。
若用户未指定，默认使用中文活泼风格，随机选一条。

### 4. 节假日跳过（可选）

若用户需要节假日跳过，参考 `references/holidays.md` 修改 `payload.message`，
让 isolated agent 在执行时先判断当天是否为节假日，是则 NO_REPLY。

### 5. 调用 cron 工具创建任务

```json
{
  "name": "站起来活动提醒",
  "schedule": {
    "kind": "cron",
    "expr": "30 8-17 * * 1-5",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "⏰ 久坐提醒：已经坐了一个小时啦！站起来活动一下吧 🚶 伸个懒腰、走几步、喝杯水，对身体好！"
  },
  "delivery": { "mode": "announce" },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### 6. 回复用户

告知：任务名称、每天提醒次数、首次触发时间、任务 ID（供后续管理用）。

---

## 管理已有提醒

| 操作 | 方法 |
|------|------|
| 查看所有提醒 | `cron list` |
| 暂停 | `cron update` → `enabled: false` |
| 恢复 | `cron update` → `enabled: true` |
| 修改时间 | `cron update` → 更新 `schedule.expr` |
| 删除 | `cron remove` + 任务 ID |

---

## 参考文件

- **文案库**：`references/messages.md` — 中/英/日多语言、四种风格的提醒文案
- **节假日跳过**：`references/holidays.md` — 节假日感知实现方式与完整 payload 示例
