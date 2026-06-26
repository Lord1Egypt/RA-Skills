---
name: todo-list
description: 待办事项管理技能，支持添加、查看、完成、删除待办事项，支持到期提醒、标签系统、项目管理、附件功能。触发条件：(1) 用户提到待办、Todo、任务管理、待办列表、todolist (2) 需要添加、查看、完成、删除待办事项 (3) 设置任务提醒 (4) 标签管理 (5) 项目管理 (6) 用户直接输入"todo"或"todo status"时显示状态页
---

# Todo List 待办事项管理技能

## 功能说明
- 📊 状态页：显示项目进度、待办概览、标签统计（用户输入"todo"或"todo status"时触发）
- 📝 添加待办事项：支持设置标题、详细描述、优先级、到期时间、标签、附件
- 👀 查看待办事项：支持按状态（全部/未完成/已完成）、优先级、时间、标签筛选
- ✅ 标记完成：将待办事项标记为已完成状态
- 🗑️ 删除待办事项：删除不需要的待办事项
- ⏰ 到期提醒：自动提醒即将到期的待办任务（提醒中包含附件路径）
- 🏷️ 标签系统：为任务添加标签，支持按标签筛选和查询
- 📦 项目管理：将标签升级为项目，追踪项目进度
- 📎 附件功能：为任务添加附件，支持文件存储
- 🔴 优先级说明：high=🔴高优，medium=🟡中优，low=🟢低优

## ⚠️ AI展示规则
**重要：** 当AI展示待办列表时，必须遵循以下规则：
1. **时间顺序排序**：所有任务必须按到期时间（dueAt）排序，最早到期的任务排在最前面
2. **不按类别分类**：不要按标签、优先级或项目分类展示，而是使用统一的时间线展示
3. **排序规则**：
   - 有到期时间的任务按到期时间升序排列（最近到期在前）
   - 没有到期时间的任务排在有到期时间的任务之后
   - 相同到期时间的任务按优先级排序（high > medium > low）
4. **展示格式**：统一展示所有未完成任务，使用时间线方式呈现

## 🎯 触发条件
当用户输入以下内容时，必须调用本技能：
- `todo` - 显示状态页概览
- `todo status` - 显示状态页概览
- `todolist` - 显示完整待办列表
- 其他包含"待办"、"任务"、"todo"的请求

## 使用方法

### 前置说明
本技能的命令行工具位于 `scripts/todo.py`，需要使用 Python 3 运行，执行时需要先进入技能目录或指定完整路径。

### 正确调用方式
```bash
# 方式1：先进入脚本目录
cd ~/.openclaw/workspace/skills/todo-list/scripts/
python3 todo.py <子命令> [参数]

# 方式2：直接指定完整路径
python3 ~/.openclaw/workspace/skills/todo-list/scripts/todo.py <子命令> [参数]
```

---

## 📊 状态页命令

### 显示状态概览
```bash
python3 todo.py status
```

**输出内容：**
1. **全局最近截止**：所有未完成任务中最近的一个截止时间
2. **项目进度**：显示所有未完成项目（进度<100%）及其最近截止时间
3. **待办概览**：已完成数量、未完成数量、最近3个待办
4. **标签统计**：所有标签的未完成/总数量

**示例输出：**
```
📊 Todo 状态概览
==================================================

⏰ 全局最近截止：2026-03-12 21:00 (约2小时)

📦 项目进度
--------------------------------------------------
├─ OpenClaw商业化项目 [商业化] 0/8 (0.0%) | ⏰ 21:00 (约2小时)
│  └─ 最近任务：操作手册编写、说明文件编写、速查表建立

📋 待办概览
--------------------------------------------------
├─ ✅ 已完成：11 个
└─ ⏳ 未完成：24 个

⏰ 最近待办：
   ├─ 🔴 OpenClaw文档：操作手册编写 (21:00)
   ├─ 🔴 OpenClaw文档：说明文件编写 (21:00)
   └─ 🔴 OpenClaw部署：部署文档编写 (21:00)

🏷️ 标签统计
--------------------------------------------------
├─ OpenClaw: 8/8  |  📦商业化: 8/8  |    学习: 7/12
├─ IEP: 5/5  |    AI: 4/7  |    文档: 4/4
...
```

---

## 📝 基础命令

### 添加待办
```bash
python3 todo.py add "任务标题" [参数]
```

**参数说明：**
| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--description` | `-d` | 任务详细描述 | `--description "详细说明"` |
| `--priority` | `-p` | 优先级（high/medium/low） | `--priority high` |
| `--due` | 无 | 到期时间 | `--due "2026-03-15 12:00"` |
| `--tags` | `-t` | 标签（逗号分隔） | `--tags "学习,RAG,AI"` |
| `--attach` | `-a` | 附件文件路径 | `--attach "/path/to/file.pdf"` |

**示例：**
```bash
# 基础添加
python3 todo.py add "英语辩论赛初赛"

# 完整参数
python3 todo.py add "学习RAG向量库" \
  --description "学习MiroFish的RAG实现" \
  --priority high \
  --due "2026-03-15 18:00" \
  --tags "学习,RAG,AI" \
  --attach "/home/user/notes.md"
```

---

### 查看待办
```bash
python3 todo.py list [参数]
```

**参数说明：**
| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--status` | `-s` | 状态过滤（all/pending/completed） | `--status all` |
| `--priority` | `-p` | 优先级过滤 | `--priority high` |
| `--all` | `-a` | 显示全部已完成任务 | `--all` |
| `--tag` | `-t` | 按标签筛选 | `--tag "学习"` |

**示例：**
```bash
# 查看所有待办（包含已完成和未完成，已完成只显示最近3个）
python3 todo.py list --status all

# 查看所有待办，显示全部已完成任务
python3 todo.py list --status all --all
# 或
python3 todo.py list --status all -a

# 只查看未完成的待办（默认）
python3 todo.py list

# 只查看高优先级待办
python3 todo.py list --priority high

# 按标签筛选任务
python3 todo.py list --tag "学习"
# 或
python3 todo.py list -t "RAG"

# 查看已完成的任务（只显示最近3个）
python3 todo.py list --status completed
```

**输出格式示例：**
```
📋 待办事项列表（共11个）：
--------------------------------------------------------------------------------
✅ 已完成（共1个）：
✅ [afc4e869] 🔴 测试Todo任务 | 到期：2026-03-09 11:50
     描述：这是一个测试待办事项，用于验证提醒功能

⏳ 未完成（共10个）：
⏳ [e8dbd910] 🔴 OpenClaw商业化 | 到期：2026-03-14 21:00 🏷️ [OpenClaw, 商业化]
     描述：以OpenClaw部署、文档编写、教程制作、一对一指导为核心赚钱模式

⏳ [c19feff3] 🟡 学习RAG向量库 🏷️ [学习, RAG]
     描述：学习Rag向量库以及嵌入大模型
```

---

### 标记完成
```bash
python3 todo.py done <任务ID>
```

**示例：**
```bash
python3 todo.py done 74d12e1c
```

**说明：** 标记完成时会显示该任务的附件信息，并自动取消相关的定时提醒。

---

### 删除待办
```bash
python3 todo.py delete <任务ID>
```

**示例：**
```bash
python3 todo.py delete 74d12e1c
```

**说明：** 删除任务时会同时删除该任务的所有附件文件。

---

### 为任务添加标签
```bash
python3 todo.py add-tag <任务ID> <标签>
```

**参数说明：**
| 参数 | 说明 | 示例 |
|------|------|------|
| `任务ID` | 要添加标签的任务ID | `e8dbd910` |
| `标签` | 要添加的标签，多个标签用逗号分隔 | `学习,AI` 或 `#RAG` |

**示例：**
```bash
# 添加单个标签
python3 todo.py add-tag e8dbd910 "OpenClaw"

# 添加多个标签
python3 todo.py add-tag e8dbd910 "OpenClaw,商业化"

# 使用#标签格式（#会被自动去除）
python3 todo.py add-tag e8dbd910 "#RAG,#AI"
```

**说明：**
- 标签会自动去重，重复添加不会创建重复标签
- 如果标签对应的项目已存在，任务会自动关联到该项目

---

### 查看详情
```bash
python3 todo.py show <任务ID>
```

**示例：**
```bash
python3 todo.py show 74d12e1c
```

**输出示例：**
```
📌 任务详情 [74d12e1c]
--------------------------------------------------
标题：学习RAG向量库
描述：学习Rag向量库以及嵌入大模型
优先级：high
状态：待处理
标签：学习, RAG, AI
所属项目：RAG向量库学习
创建时间：2026-03-12 12:00
到期时间：2026-03-15 18:00

📎 附件（1个）：
   • notes.md
     路径：/home/user/.openclaw/workspace/memory/todo-attachments/74d12e1c/notes.md
```

---

---

## 🏷️ 标签系统

### 自动提取标签
系统会自动从任务标题和描述中提取 `#标签` 格式的标签，无需手动指定。

**示例：**
```bash
# 在标题中使用标签
python3 todo.py add "学习RAG向量库 #RAG #学习"

# 在描述中使用标签
python3 todo.py add "完成任务" --description "这是一个重要任务 #重要 #紧急"

# 混合使用
python3 todo.py add "学习RAG #RAG" --tags "AI,开发"
# 最终标签：RAG, AI, 开发（自动合并）
```

**支持的标签格式：**
- 支持中文：`#学习` `#重要`
- 支持英文：`#RAG` `#AI`
- 支持数字：`#M1` `#IEP`
- 支持连字符：`#OpenClaw` `#to-do`

### 查看所有标签
```bash
python3 todo.py tags
```

**输出示例：**
```
🏷️  所有标签：
----------------------------------------
  • AI (3个任务)
  • OpenClaw (2个任务)
  • RAG (5个任务) 📦[项目]
  • 学习 (8个任务)
```

**说明：** 带 `📦[项目]` 标记的标签表示已被创建为项目。

### 按标签筛选任务
使用 `list` 命令的 `-t` / `--tag` 参数：
```bash
python3 todo.py list -t "学习"
python3 todo.py list --tag "RAG"
```

---

## 📦 项目管理

### 创建项目
```bash
python3 todo.py project create <标签> <项目名称> [--description "项目描述"]
```

**参数说明：**
| 参数 | 简写 | 说明 | 必填 |
|------|------|------|------|
| `标签` | 无 | 要升级为项目的标签 | ✅ 必填 |
| `项目名称` | 无 | 项目显示名称 | ✅ 必填 |
| `--description` | `-d` | 项目描述 | 可选 |

**示例：**
```bash
# 创建项目
python3 todo.py project create "RAG" "RAG向量库学习"

# 创建项目并添加描述
python3 todo.py project create "OpenClaw" "OpenClaw商业化项目" \
  --description "部署、文档、教程、一对一指导"
```

**说明：**
- 创建项目后，所有包含该标签的任务会自动关联到项目
- 后续添加的带该标签的任务也会自动关联

---

### 查看所有项目
```bash
python3 todo.py project list
```

**输出示例：**
```
📦 所有项目：
------------------------------------------------------------
  📦 RAG向量库学习
     标签：RAG
     进度：2/5 (40.0%)
     描述：学习Rag向量库和嵌入大模型

  📦 OpenClaw商业化项目
     标签：OpenClaw
     进度：0/3 (0.0%)
     描述：部署、文档、教程、一对一指导
```

---

### 查看项目详情
```bash
python3 todo.py project show <标签>
```

**示例：**
```bash
python3 todo.py project show "RAG"
```

**输出示例：**
```
📦 项目：RAG向量库学习
🏷️  标签：RAG
📊 进度：2/5 任务完成 (40.0%)
📝 描述：学习Rag向量库和嵌入大模型
--------------------------------------------------------------------------------
⏳ 未完成（共3个）：
⏳ [c19feff3] 🟡 学习RAG原理 🏷️ [学习, RAG]
     描述：理解向量库工作方式

⏳ [abc12345] 🟡 构建向量库 🏷️ [RAG, 实践]
     描述：参考MiroFish构建

✅ 已完成（共2个）：
✅ [def67890] 🟡 阅读文档 🏷️ [RAG]
     描述：阅读官方文档
```

---

## 📎 附件功能

### 添加任务时附带附件
使用 `add` 命令的 `--attach` / `-a` 参数：
```bash
python3 todo.py add "学习任务" --attach "/path/to/file.pdf"
```

### 为已有任务添加附件
```bash
python3 todo.py attach <任务ID> <文件路径>
```

**示例：**
```bash
python3 todo.py attach 74d12e1c "/home/user/notes.md"
```

**说明：**
- 附件会被复制到 `~/.openclaw/workspace/memory/todo-attachments/<任务ID>/` 目录
- 每个任务的附件独立存储，按任务ID分类
- 文件名冲突时会自动添加序号

### 查看任务附件
使用 `show` 命令查看任务详情时会显示附件信息：
```bash
python3 todo.py show 74d12e1c
```

### 提醒中的附件
- 定时提醒消息中会包含附件路径
- 当任务有附件时，完成或查看任务会提示附件位置
- 兰兰会在提及任务时询问是否需要发送附件

---

## 📊 数据存储

### 存储位置
- **数据文件**：`~/.openclaw/workspace/memory/todo.json`
- **附件目录**：`~/.openclaw/workspace/memory/todo-attachments/`

### 数据结构
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "任务标题",
      "description": "任务描述",
      "priority": "high",
      "status": "pending",
      "tags": ["学习", "RAG"],
      "attachments": [
        {
          "type": "file",
          "path": "uuid/filename.pdf",
          "name": "filename.pdf"
        }
      ],
      "projectName": "RAG向量库学习",
      "createdAt": "timestamp",
      "dueAt": "timestamp",
      "completedAt": "timestamp"
    }
  ],
  "projects": {
    "RAG": {
      "name": "RAG向量库学习",
      "tag": "RAG",
      "description": "项目描述",
      "createdAt": "timestamp"
    }
  },
  "tags": ["学习", "RAG", "AI"]
}
```

---

## ⏰ 提醒机制

### 自动合并提醒
**重要特性**：系统会自动将**同一时间段内**（15分钟内）到期的多个任务合并为一个提醒，避免提醒过于频繁。

**合并规则：**
- 时间桶对齐：将到期时间对齐到15分钟的整数倍（如21:00、21:15、21:30）
- 自动合并：同一时间桶内的所有任务会合并为一个提醒
- 智能排序：合并提醒中的任务按优先级（high > medium > low）和到期时间排序

**合并提醒示例：**
```
⏰ 待办提醒 - 以下任务即将到期：

🔴 [cd0d91a4] OpenClaw文档：操作手册编写
   到期：2026-03-12 21:00

🔴 [9df17ec5] OpenClaw文档：说明文件编写
   到期：2026-03-12 21:00

🟡 [9c8ac16d] OpenClaw文档：速查表建立
   到期：2026-03-12 21:15
```

### 自动提醒规则
- **高优先级任务**：桶时间前30分钟、15分钟、准点 三次提醒
- **普通/低优先级任务**：桶时间前15分钟、准点 两次提醒
- **提醒内容**：包含任务标题、优先级、到期时间

### 单任务提醒示例
```
⏰ 待办提醒：[c19feff3] 学习RAG向量库
优先级：high
到期时间：2026-03-15 18:00
⏱️ 还有15分钟到期！
```

### 提醒数据存储
- 提醒配置保存在：`~/.openclaw/workspace/memory/todo-reminders.json`
- 包含每个合并提醒的时间桶、任务ID列表、OpenClaw cron任务ID

---

## 🔧 常见问题

1. **提示 "todo: 未找到命令"**：说明没有在正确的路径执行，需要使用 `python3 todo.py` 的方式调用

2. **提示 "python: 未找到命令"**：请使用 `python3` 代替 `python`

3. **时间格式错误**：到期时间请使用 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM` 格式，例如 `2026-03-11 12:00`

4. **优先级设置错误**：优先级只能是 `high`、`medium`、`low` 三个选项

5. **标签分隔符**：多个标签使用英文逗号 `,` 分隔，例如 `--tags "学习,RAG,AI"`

6. **附件文件不存在**：添加附件前请确保文件路径正确，支持绝对路径和相对路径

7. **项目标签已存在**：一个标签只能创建一个项目，如果提示已存在，请先检查现有项目

---

## 📝 完整命令速查表

| 命令 | 说明 |
|------|------|
| `add` | 添加新待办 |
| `list` | 列出待办 |
| `done` | 标记完成 |
| `delete` | 删除任务 |
| `show` | 查看详情 |
| `tags` | 查看所有标签 |
| `add-tag` | 为任务添加标签 |
| `project create` | 创建项目 |
| `project list` | 查看所有项目 |
| `project show` | 查看项目详情 |
| `attach` | 添加附件 |
| `check-due` | 检查到期任务 |

---

## 🛠️ 维护工具

### 重新合并所有提醒
如果需要重新合并所有待办任务的提醒（例如升级系统后），可以使用：

```bash
cd ~/.openclaw/workspace/skills/todo-list/scripts/
python3 merge-reminders.py
```

**功能说明：**
- 自动删除所有旧的 todo-* 提醒
- 按时间桶重新分组所有待办任务
- 为每个时间桶创建合并提醒
- 保存提醒配置到 `~/.openclaw/workspace/memory/todo-reminders.json`

**使用场景：**
- 系统升级后重新整理提醒
- 手动修改了待办任务的到期时间
- 提醒系统出现异常需要重建
