---
name: telegram-todolist
description: Telegram bot Todo List manager. Three commands: /todo query (show tasks), /todo organize (add/delete/edit tasks), /todo execute (complete tasks). Uses TODO.md file. Perfect for task tracking in Telegram. Supports statistics, progress tracking, and organized task management.
---

# Telegram Todo List

Manage a Todo List stored in TODO.md through Telegram bot commands.

## Commands

### 1. 查询 (query)
**Usage**: `/todo query`

**Description**: Display current todo list with status

**Behavior**:
- Read TODO.md file
- Parse tasks (both completed [x] and pending [ ])
- Format and display in clean table/list
- Show statistics (total tasks, completed, pending)

**Example Output**:
```
📋 待办事项列表

今日任务 (2026-02-12)

- [ ] 学习并掌握 skill-creator 技能介绍
  - 理解技能创建的核心原则

待办总数：6 项未完成
已完成：1 项
```

### 2. 整理 (organize)
**Usage**: `/todo organize`

**Description**: Update, optimize, or restructure the todo list

**Behavior Options**:
- **Add new task**: User specifies task content
- **Delete task**: User specifies task number to remove
- **Move task**: Change task priority/order
- **Edit task**: Modify task content or check/uncheck status
- **Batch operations**: Add multiple tasks at once

**Input Format**:
``/todo organize <action> <details>
```

**Actions**:
- `add`: Add new task(s)
- `delete`: Remove task by number
- `move`: Move task to different position
- `edit`: Modify task content
- `check`: Mark task as completed
- `uncheck`: Mark task as uncompleted

**Example**:
``/todo organize add 学习Markdown语法
/todo organize delete 3
/todo organize move 1 to top
```

### 3. 执行 (execute)
**Description**: Complete a specific task

**Behavior**:
- Mark task as completed [x]
- Update timestamp
- Remove from active list
- Move to completed section
- Show confirmation

**Input Format**:
``/todo execute <task_number>
```

**Example**:
``/todo execute 1
```

## File Structure

**Storage**: TODO.md in workspace root
```
/root/.openclaw/workspace/TODO.md
```

**File Format**:
```markdown
# TODO List

## 今日任务 (2026-02-12)

- [ ] **Task 1**
  - Subtask 1
  - Subtask 2

- [ ] **Task 2**

---

## 待完成任务

### Category
- [ ] **Task 3**

---

## 已完成任务

- [x] **Completed Task**
  - 记录时间：2026-02-12 07:55 UTC
  - 内容：Task description
```

## Implementation Details

### Parsing Tasks

**Regular Expression**:
```regex
- \[([ x])\]\s*\*\*(.+?)\*\*.*?$         # Main task
  - (.+)$                                 # Subtasks
```

**Status**:
- `[x]` = completed
- `[ ]` = pending

### Display Format

**Clean Table**:
```
📋 待办事项

今日任务 (2026-02-12)
1. [ ] Task 1
2. [ ] Task 2

待办总数：2 项未完成
已完成：0 项
```

### Error Handling

**Task Not Found**:
- "未找到任务 #N"
- Ask user to verify task number

**Invalid Format**:
- "格式错误，请使用正确的命令格式"
- Show usage example

**File Read Error**:
- "无法读取 TODO.md，请检查文件权限"
- Try to recreate default template

### User Experience

**Confirmation Messages**:
- Task completed: "✅ 已完成任务 #N"
- Task deleted: "🗑️ 已删除任务 #N"
- Task added: "➕ 已添加任务"

**Progress Indicators**:
- Show real-time count updates
- Calculate completion percentage
- Highlight pending vs completed

## Tips

1. **Task Numbers**: Always reference task by number in organize/execute commands
2. **Indentation**: Keep consistent spacing for subtasks
3. **Comments**: Lines starting with `#` are ignored
4. **Status Updates**: Execute updates both visual status and file content

## Examples

### User: /todo query
Bot shows full todo list

### User: /todo organize add 学习CSS
Bot adds task and shows confirmation

### User: /todo execute 2
Bot marks task #2 as completed and updates list

### User: /todo organize delete 5
Bot removes task #5 from list
