---
name: smart-reminder
description: "智能定时提醒助手，支持：1) 多人格提醒风格（可爱/元气/认真/毒舌/温柔），2) 多频次任务进度追踪（本周已完成训练 1/3），3) 上下文感知的鼓励/反馈（上次没完成则下次鼓励）。集成 cron 调度。触发词：'提醒我' '定个提醒' '定时提醒' 'remind me' '帮我记着' '设置提醒' '设定提醒'"
---

# Smart Reminder - 智能定时提醒助手

## 核心能力

本技能提供四个维度的提醒能力：

1. **人格化提醒** — 固定 5 种人格风格，提醒消息完全按该人格的语调、用词、表情符号输出
2. **昵称个性化** — 用户可设置自己的昵称，全局应用于所有提醒消息
3. **游戏化进度追踪** — 多频次任务（如"每周一三五运动"）显示进度条，风格化呈现
4. **延续性反馈** — 记录每次提醒的完成状态，影响到下一次提醒的措辞

## 快速使用

### 用户触发句式示例

| 场景 | 用户说 | 你应该 |
|------|--------|--------|
| 单次提醒 | "提醒我 30 分钟后喝水" | 创建 cron at 任务，存储 config，带上人格发送提醒 |
| 单次指定时间 | "明天下午 3 点提醒我开会" | 同上 |
| 多频次任务+人格 | "设定每周一三五晚 8 点运动，要可爱的提醒风格" | 创建 3 个 cron 任务（或一个 cron 表达式），存储 task config，包含 progress |
| 指定人格（5种任选） | "元气风格提醒我每天早上跑步" | 同上，人格设为 "energetic" |
| 无指定人格 | "提醒我多喝水" | 默认用 "gentle" 风格 |
| 设置昵称 | "叫我小可爱" / "别叫我名字了" | 更新 `config.nickname`，后续所有提醒使用该昵称 |

### 5 种人格一览（详见 personalities.md）

| 名称 | key | 特点 | 颜文字风格 |
|------|-----|------|-----------|
| 🎀 可爱 | cute | 软萌、撒娇、使用大量颜文字 | (｡>ω<｡) ♡～ |
| ⚡ 元气 | energetic | 热血、干劲满满、感叹号多 | 💪🔥✨ |
| 📋 认真 | formal | 正经、简洁、称呼礼貌 | 少用emoji |
| 🗡️ 毒舌 | sarcastic | 傲娇、调侃、激将法 | 😒～哼 |
| 🌸 温柔 | gentle | 暖心、体贴、知心大姐姐/哥哥 | ☺️💗 |

## 工作流程

### Step 1: 用户提出提醒需求

解析用户的自然语言请求，提取：
- **任务名称**（如"运动"、"喝水"）
- **时间/频率**（如"30分钟后"、"每天早8点"、"周一三五"）
- **人格偏好**（如"可爱风格"、"元气一点"——未指定则默认温柔）
- **总频次**（仅多频次任务需要，如"每周运动3次"→totalSessions=3）
- **昵称设置**（如"叫我小可爱"→更新全局昵称；"别叫昵称"→清空）

### Step 2: 存储任务配置

将任务写入状态文件：`memory/smart-reminder-tasks.json`

**文件结构：**

```json
{
  "config": {
    "nickname": "小可爱"
  },
  "tasks": {
    "task_<shortId>": {
      "id": "task_abc123",
      "name": "运动训练",
      "schedule": {
        "type": "cron",
        "expression": "0 20 * * 1,3,5",
        "tz": "Asia/Shanghai"
      },
      "personality": "cute",
      "delivery": {
        "channel": "openclaw-weixin",
        "sessionKey": "agent:main:openclaw-weixin:direct:...@im.wechat"
      },
      "tracking": {
        "totalSessions": 3,
        "completedSessions": 0,
        "weekStart": "2026-05-11",
        "history": [],
        "sinceLastCompletion": 0
      },
      "createdAt": "2026-05-11T12:00:00+08:00",
      "enabled": true
    }
  }
}
```

- `config.nickname` — 用户昵称，所有提醒消息的 `{nickname}` 占位符替换为此值
- 未设置时各人格使用默认称呼（见 personalities.md 末尾）

**字段说明：**
- `schedule.type` — `"at"`（单次）或 `"cron"`（重复）
- `personality` — 人格 key
- **`delivery`** — **必需字段！**
  - `channel` — 目标频道 ID（如 `"openclaw-weixin"`、`"telegram"`、`"main"` 表示当前会话）
  - `sessionKey` — 目标会话 key（从 `openclaw sessions` 获取，用于 `sessions_send`）
  - 跨频道提醒（如从 Control UI 设定但发到微信）必须设置此字段
- `tracking.totalSessions` — 每周目标次数（仅多频次）
- `tracking.completedSessions` — 本周已完成次数
- `tracking.weekStart` — 当前追踪周的周一 YYYY-MM-DD
- `tracking.history` — 数组，每项 `{date, completed, feedback?}`
- `tracking.sinceLastCompletion` — 连续未完成次数（用于鞭策）

### Step 3: 创建 cron 任务

**⚠️ 警告：存储 task 配置后必须同时创建 cron 任务！** 光存 config 不会触发任何提醒。

**必须使用 `cron` 工具创建任务（不是 CLI！CLI 有设备范围限制）。**

调用 `cron(add)` 工具：
- 单次提醒 → `schedule: {kind: "at", at: "ISO-8601 with offset"}`
- 重复提醒 → `schedule: {kind: "cron", expr: "...", tz: "Asia/Shanghai"}`
- 所有提醒 → `payload: {kind: "systemEvent", text: "SMART_REMINDER task_id"}`
- 单次自动清理 → `deleteAfterRun: true`

**cron 的 systemEvent 文本格式：** cron 触发后发送 `systemEvent` 给主 session，文本必须包含 task ID。

```
SMART_REMINDER task_abc123
```

**cron 调用示例（工具调用）：**
```json
{
  "action": "add",
  "job": {
    "name": "SMART_REMINDER_task_abc123",
    "schedule": {
      "kind": "at",
      "at": "2026-05-12T20:00:00+08:00"
    },
    "payload": {
      "kind": "systemEvent",
      "text": "SMART_REMINDER task_abc123"
    },
    "sessionTarget": "main",
    "deleteAfterRun": true
  }
}
```

**重要：**
- 不要使用 `openclaw cron add` CLI 命令
- 使用 `cron` 函数工具（tool），它是 OpenClaw Gateway 原生支持的
- cron job 的 name 设为对应 task ID 方便管理

### Step 4: cron 触发 → 生成提醒消息

当收到 `SMART_REMINDER task_xxx` 系统事件时（同频道提醒）：

1. **读取任务配置** — 从 `skills/memory/smart-reminder-tasks.json` 加载该 task
2. **读取昵称** — 从 `config.nickname` 获取；若无则按人格使用默认称呼
3. **读取进度上下文** — 检查 `tracking.history` 和 `sinceLastCompletion`
4. **生成个性化提醒** — 将 personalities.md 模板中的 `{nickname}` 替换为用户昵称
5. **直接在当前 session 回复** — 提醒消息 + 询问完成状态

### Step 4b: 跨频道投递（从网页端发到微信）

**⚠️ 只有需要跨频道投递时用此方式！** 同频道提醒用 Step 4 的 systemEvent 方式。

如果用户通过 Control UI（网页）设定提醒但想在微信接收，需要使用 cron 的 `delivery` 机制。

**不需要 systemEvent！** 直接创建 `agentTurn` 类型的 cron job，通过 delivery 投递到微信：

**cron 调用示例：**
```json
{
  "action": "add",
  "job": {
    "name": "SMART_REMINDER_task_xxx",
    "schedule": {"kind": "at", "at": "ISO-8601"},
    "payload": {
      "kind": "agentTurn",
      "message": "用温柔风格告诉昵称该喝糖水了，发完就结束",
      "timeoutSeconds": 120,
      "lightContext": true
    },
    "sessionTarget": "isolated",
    "deleteAfterRun": true,
    "delivery": {
      "mode": "announce",
      "channel": "openclaw-weixin",
      "to": "用户的xxx@im.wechat",
      "accountId": "微信bot的AccountId"
    }
  }
}
```

**关键参数：**
- `sessionTarget: "isolated"` — 必须用孤立 session
- `timeoutSeconds: 120` — agent 启动可能需要一些时间，给充足超时
- `lightContext: true` — 轻量标记，减少加载时间
- `delivery.mode: "announce"` — 投递模式
- `delivery.channel: "openclaw-weixin"` — 目标频道
- `delivery.to: "用户@im.wechat"` — 微信用户的 ID（从微信 session key 获取）
- `delivery.accountId: "bot的AccountId"` — 微信 bot 的 account ID（从 channels status 获取）

**注意：** 
- `delivery.to` 和 `delivery.accountId` 缺一不可
- `sessions_send` 不可行（受 visibility=tree 限制），必须用 delivery 机制
- 同频道提醒（用户在哪设在哪收）直接用 systemEvent 方式即可

**提醒消息结构模板：**

```
[人格化问候/开场]
[提醒主题 + 时间/周期]
[进度显示（仅多频次任务）]
[上下文延续（上次没完成则鼓励）]
[询问完成状态]
```

### Step 5: 处理用户反馈

用户回复完成状态后：
- **完成（✅）** → `completedSessions++`，添加 `{date, completed:true}` 到 history，`sinceLastCompletion = 0`，发送风格化祝贺
- **未完成（❌）** → `sinceLastCompletion++`，添加 `{date, completed:false}` 到 history，发送风格化鼓励
- **取消任务** → `enabled = false`

**特殊逻辑 — 周重置：**
- 每次任务触发时，检查当前时间是否已进入新的一周
- 如果是 → `weekStart = 当前周一`, `completedSessions = 0`, `history = []`
- 如果某任务在旧周从未触发过 → 也正常重置

### Step 6: 用户查询进度

用户可随时问：
- "我的训练进度怎么样了" → 读取任务配置，呈现当前进度
- "取消这个提醒" → `enabled = false`
- "改成元气风格" → 更新 `personality`

## 状态文件路径

```
skills/memory/smart-reminder-tasks.json
```

不存在时自动创建。所有任务共享这一个文件。

**注意：** 脚本自动解析路径相对于脚本所在目录，最终路径为 `skills/memory/smart-reminder-tasks.json`。不要手动在其他目录创建同名文件。

**获取真实路径的命令：**
```bash
python -c "import os; from manage_tasks import _ensure_state; print(os.path.abspath(STATE_FILE))"
```

## 重要规则

1. **必须创建 cron 任务！** — 光存 task 配置不会触发提醒，必须调用 `openclaw cron add` 创建实际调度
2. **必须存储 delivery！** — 每次创建提醒时记录当前 session 的 channel 和 sessionKey，否则跨频道发不出去
3. **获取 sessionKey 的方法：** 使用 `openclaw sessions --agent main --active 60 --json` 查看最近的 session
4. **人格一致性** — 同一任务的所有提醒、反馈、查询回复，必须用同一人格
5. **不要过度设计** — 用户说"提醒我喝水"就是简单提醒，不需要确认太多参数
6. **时间解析** — 使用当前 session 时区（Asia/Shanghai）解析用户时间
7. **cron 表达式写本地时间** — 如在 Asia/Shanghai，周一三五晚 8 点 = `0 20 * * 1,3,5`
8. **单次 vs 重复** — 单次提醒没有 tracking（或 tracking 留空），不要显示进度
9. **进度仅在多频次任务显示** — 用户说"每天提醒我一次"这种固定单次，不显示进度
10. **默认人格** — 用户未指定时使用 `gentle`（温柔）
11. **消息长度** — 提醒消息不要太长，人格化体现在关键措辞和表情上，不是堆砌文字
12. **cron 触发勿回复过长** — systemEvent 触发时生成的提醒要精炼，后续对话在主 session 继续

## 脚本工具

### scripts/manage_tasks.py
确定性任务状态管理脚本，支持 CRUD 和进度更新。可在 SKILL.md 逻辑中直接调用，避免手动编辑 JSON。

**Windows 注意：** 调用时需设置环境变量 `$env:PYTHONIOENCODING='utf-8'` 否则中文会报错。

```powershell
# 创建（带追踪，带微信投递）
python scripts/manage_tasks.py create "运动训练" "0 20 * * 1,3,5" "cute" 3 "openclaw-weixin" "agent:main:openclaw-weixin:direct:xxx@im.wechat"

# 标记完成
python scripts/manage_tasks.py complete task_xxx true

# 标记未完成
python scripts/manage_tasks.py complete task_xxx false

# 列出所有
python scripts/manage_tasks.py list

# 更新人格
python scripts/manage_tasks.py update task_xxx personality energetic

# 删除
python scripts/manage_tasks.py delete task_xxx

# 设置昵称
python scripts/manage_tasks.py set-nickname "小可爱"

# 查看昵称
python scripts/manage_tasks.py get-nickname

# 查看完整配置
python scripts/manage_tasks.py config
```

## 参考文件

- **[personalities.md](references/personalities.md)** — 各人格的详细用语、模板、颜文字库、进度显示模板和反馈句式
- 查看此文件以获取具体人格的措辞库和消息模板
