---
name: session-sync
version: 1.0.0
description: Cross-session memory sync protocol. Ensures memory consistency across Feishu, webchat, and any other channels.
author: Stitch
keywords:
  - memory
  - session
  - sync
  - cross-channel
  - feishu
  - webchat
  - persistence
  - ai-agent
  - memory-management
  - continuity
---

# Session Sync — 跨 Session 记忆同步

## 问题

每个 session（飞书、webchat、新建 session）的对话上下文是独立的。
如果不主动同步，切换通道后会"失忆"。

## 解决方案

**共享文件是唯一的跨 session 记忆桥梁。**

### 📥 Session 启动时（必做）

1. 读取 `memory/YYYY-MM-DD.md`（今天和昨天的）
2. 读取 `MEMORY.md` 获取长期记忆
3. 读取 `memory/SESSION-STATE.md` 获取最新任务状态
4. 检查是否有其他活跃 session：

```
sessions_list(activeMinutes=120, messageLimit=3)
```

如果有其他 session 有近期活动，读取其历史了解上下文：
```
sessions_history(sessionKey="<key>", limit=10)
```

### 📤 Session 运行中（必做）

**每当你做了以下事情，立即写入 memory 文件：**
- 开始了一个新任务
- 做了一个重要决定
- 获得了新信息
- 完成了一个任务
- 切换话题

写入位置：
- `memory/YYYY-MM-DD.md` — 当天日志（原始记录）
- `memory/SESSION-STATE.md` — 当前活跃任务状态（覆盖更新）

### 📤 Session 结束前 / 对话间隙（必做）

更新 `memory/SESSION-STATE.md`：

```markdown
# Session State

## 最后更新
- 时间：YYYY-MM-DD HH:MM
- 通道：feishu / webchat
- session key：xxx

## 当前进行中的任务
- [任务名]：简述状态、下一步

## 最近重要决定
- [决定]：理由

## 待跟进
- [事项]：什么时候跟进
```

### 🔄 定期整理（建议每天一次）

把 `memory/YYYY-MM-DD.md` 中值得长期保留的内容提炼到 `MEMORY.md`。

---

## ⚠️ 关键规则

1. **不要假设另一个 session 知道你在做什么** — 写下来
2. **不要假设你自己记得之前聊了什么** — 读文件
3. **SESSION-STATE.md 是"热状态"** — 随时覆盖更新
4. **MEMORY.md 是"长期记忆"** — 定期整理，不要频繁改
5. **memory/YYYY-MM-DD.md 是"日志"** — 只追加，不删除

---

## 🧹 日志清理（自动执行）

**规则**：超过 7 天的 `memory/YYYY-MM-DD.md` 自动归档到 `memory/archive/`

**触发时机**：
- 每次 session 启动时检查一次
- 执行清理脚本：`skills/session-sync/scripts/cleanup-memory.sh`

**操作**：
```bash
bash skills/session-sync/scripts/cleanup-memory.sh
```

归档前确保有价值的内容已提炼到 MEMORY.md。

---

## 快速命令（给老板用）

- "同步记忆" → 执行完整的跨 session 同步检查
- "更新状态" → 更新 SESSION-STATE.md
- "整理记忆" → 把日志整理到 MEMORY.md
- "清理日志" → 执行 7 天归档脚本
