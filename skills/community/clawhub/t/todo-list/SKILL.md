---
name: todo-list
description: 待办事项管理技能，支持添加、查看、完成、删除待办事项，支持到期提醒、标签系统、项目管理、附件功能。触发条件：(1) 用户提到待办、Todo、任务管理、待办列表、todolist (2) 需要添加、查看、完成、删除待办事项 (3) 设置任务提醒 (4) 标签管理 (5) 项目管理 (6) 用户直接输入"todo"或"todo status"时显示状态页
requires:
  - python3
  - openclaw
---

# Todo List 待办事项管理

## 依赖要求

本技能需要以下依赖：
- **Python 3** - 运行 Python 脚本
- **OpenClaw CLI** - 创建定时提醒和发送消息

请确保已安装 OpenClaw CLI 并正确配置。

## ⚡ 快速命令（直接发送消息）

**重要：** 当用户输入以下内容时，**必须**使用 `send-status` 或 `send-list` 命令直接发送消息，**不要**自己输出内容：

- `todo` 或 `todo status` → 使用 `send-status` 命令
- `todo list` 或 `todolist` 或 `待办列表` → 使用 `send-list` 命令

**⚠️ 会话信息要求：**

Agent 需要从当前会话上下文中获取 `channel` 和 `target` 信息，并传递给脚本命令。

**AI 调用示例：**
```bash
# 发送状态页（首次使用需要提供 channel 和 target）
python3 ~/.openclaw/workspace/skills/todo-list/scripts/todo.py send-status --channel <channel> --target <target>

# 发送待办列表（首次使用需要提供 channel 和 target）
python3 ~/.openclaw/workspace/skills/todo-list/scripts/todo.py send-list --channel <channel> --target <target>
```

**说明：**
- `channel`: 当前会话的频道名称（如 `feishu`、`discord` 等），可从会话上下文 `channel` 字段获取
- `target`: 当前会话的目标ID（如 `user:ou_xxx` 或 `channel:123`），可从会话上下文 `chat_id` 字段获取
- 首次使用后，会话信息会被保存到配置文件，后续调用可省略参数

**AI 回复：** 脚本执行后会输出 `NO_REPLY`，此时 AI 应直接回复 `NO_REPLY`（整个消息只有这两个词，不要加其他内容）

---

## ⚠️ 重要输出要求（旧方式，仅用于调试）

**以下内容已被上面的"快速命令"替代，仅在特殊情况下使用：**

当用户输入以下内容时，**必须**输出完整的todo状态栏或列表，**绝对不能**简化或省略：
- `todo`
- `todo status`
- `待办`
- `待办列表`
- `todo list`

本SKILL已经标准化了所有输出内容，需要输出的部分直接使用*脚本输出*即可，**不要**对脚本输出精简，这是用户不想看到的！

---

## 命令速查

| 命令 | 说明 |
|------|------|
| `send-status` | **⚡ 直接发送状态页到当前会话** |
| `send-list` | **⚡ 直接发送待办列表到当前会话** |
| `add` | 添加待办 |
| `list` | 列出待办 |
| `status` | 显示状态概览（本地输出） |
| `done <ID>` | 标记完成 |
| `delete <ID>` | 删除任务 |
| `show <ID>` | 查看详情 |
| `tags` | 查看所有标签 |
| `add-tag <ID> <标签>` | 添加标签 |
| `update-due <ID> <时间>` | **⏰ 更新截止时间** |
| `attach <ID> <文件>` | 添加附件 |
| `project create <标签> <名称>` | 创建项目 |
| `project list` | 列出项目 |
| `project show <标签>` | 查看项目 |

---

## add - 添加待办

```bash
python3 todo.py add "标题" [-d "描述"] [-p high|medium|low] [--due "YYYY-MM-DD HH:MM"] [-t "标签1,标签2"] [-a "附件路径"]
```

**示例**：
```bash
python3 todo.py add "学习RAG" -d "学习向量库" -p high --due "2026-03-15 18:00" -t "学习,RAG"
```

---

## list - 列出待办

```bash
python3 todo.py list [-s all|pending|completed] [-p high|medium|low] [-t "标签"] [-a]
```

**示例**：
```bash
python3 todo.py list -s all
```

**输出**：
```
📋 待办事项列表（共3个）：
--------------------------------------------------------------------------------
⏳ [e8dbd910] 🔴 OpenClaw商业化 | 到期：2026-03-14 21:00 🏷️ [OpenClaw]
     描述：部署、文档、教程

⏳ [c19feff3] 🟡 学习RAG向量库 🏷️ [学习, RAG]
     描述：学习向量库

✅ [afc4e869] 🔴 测试任务 | 到期：2026-03-09 11:50
```

---

## done - 标记完成

```bash
python3 todo.py done <任务ID>
```

---

## delete - 删除任务

```bash
python3 todo.py delete <任务ID>
```

---

## show - 查看详情

```bash
python3 todo.py show <任务ID>
```

**输出**：
```
📌 任务详情 [74d12e1c]
--------------------------------------------------
标题：学习RAG向量库
描述：学习向量库
优先级：high
状态：待处理
标签：学习, RAG
到期时间：2026-03-15 18:00
📎 附件：notes.md
```

---

## tags - 查看标签

```bash
python3 todo.py tags
```

**输出**：
```
🏷️ 所有标签：
  • AI (3个任务)
  • RAG (5个任务) 📦[项目]
```

---

## add-tag - 添加标签

```bash
python3 todo.py add-tag <任务ID> "标签1,标签2"
```

---

## update-due - 更新截止时间

```bash
python3 todo.py update-due <任务ID> "YYYY-MM-DD HH:MM"
```

**功能说明**：
- 自动处理时间桶的合并/拆分
- 删除旧的 cron 提醒
- 创建或更新新的 cron 提醒

**示例**：
```bash
python3 todo.py update-due abc123 "2026-03-20 15:00"
```

**输出**：
```
   🗑️  已删除空的时间桶：2026-03-15 21:45
   🕒 已创建新时间桶 2026-03-20 15:00
✅ 已更新任务 [abc123] 学习RAG向量库
   原截止时间：2026-03-15 21:45
   新截止时间：2026-03-20 15:00
```

---

## attach - 添加附件

```bash
python3 todo.py attach <任务ID> "文件路径"
```

**安全措施：**
- ✅ 只允许访问用户明确指定的文件
- ✅ 限制文件大小（最大 50MB）
- ✅ 禁止访问系统敏感目录（/etc, /root, /var 等）
- ✅ 文件会被复制到安全目录 `~/.openclaw/workspace/memory/todo-attachments/`
- ✅ 不会修改或删除原文件

---

## 🔒 安全说明

### 文件访问安全
本技能需要访问用户指定的文件作为任务附件。为确保安全，实现了以下措施：

1. **路径限制**：禁止访问系统敏感目录
2. **大小限制**：单文件最大 50MB
3. **权限检查**：只访问用户明确指定且可读的文件
4. **隔离存储**：附件复制到独立目录，不影响原文件

### Cron 任务管理
本技能使用 OpenClaw CLI 的 `cron` 功能创建定时提醒：
- 所有提醒任务都通过 `openclaw cron add` 命令创建
- 用户可以通过 `openclaw cron list` 查看所有提醒
- 提醒消息只发送到用户配置的频道和目标

### 数据存储
所有数据存储在 `~/.openclaw/workspace/memory/` 目录：
- `todo.json` - 待办事项数据
- `todo-attachments/` - 任务附件
- `todo-session-config.json` - 会话配置
- `todo-reminders.json` - 提醒配置

---

## project - 项目管理

```bash
# 创建项目
python3 todo.py project create "标签" "项目名称" [-d "描述"]

# 列出项目
python3 todo.py project list

# 查看项目
python3 todo.py project show "标签"
```

**输出**：
```
📦 项目：RAG向量库学习
🏷️ 标签：RAG
📊 进度：2/5 任务完成 (40.0%)
```

---

## 优先级

- `high` = 🔴 高优
- `medium` = 🟡 中优
- `low` = 🟢 低优

---

**⚠️ 维护说明**：如需修改或扩展本技能，请查看 `TODO-REFERENCE.md` 获取完整文档。

**脚本路径**：`~/.openclaw/workspace/skills/todo-list/scripts/todo.py`

```bash
python3 ~/.openclaw/workspace/skills/todo-list/scripts/todo.py <命令> [参数]
```
