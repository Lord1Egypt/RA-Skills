# Simple Workflow Guide

## 🎯 Mục tiêu

Đơn giản hóa workflow để team dễ triển khai:
- **1 workflow** thay vì 3 phases
- **1 agent call** cho mỗi task
- **Agent tự spawn subagents** nếu cần

---

## 📋 Architecture

### Trước (Phức tạp)
```
Plan → Execute → Approve
(3 phases, 3 agent calls)
```

### Sau (Đơn giản)
```
Execute
(1 phase, 1 agent call)
     ↓
Agent tự xử lý:
  - Phân tích task
  - Spawn subagents (nếu cần)
  - Aggregate results
  - Writeback to Zrise
```

---

## 🚀 Sử dụng

### 1. Chạy task với simple workflow

```bash
# Cách 1: Qua UI
# Mở http://localhost:8080
# Click vào task → Click "Execute"

# Cách 2: Command line
python3 scripts/execute_task.py --task-id 42174 --workflow simple

# Cách 3: Qua lobster
lobster run workflows/simple.lobster --argsJson '{"task_id": 42174}'
```

### 2. Agent sẽ tự động

```python
# Agent zrise-worker nhận task
# Tự quyết định:

if task.is_simple():
    # Tự xử lý
    result = process_task(task)
else:
    # Spawn subagents
    subagent1 = spawn("demo-be", "Implement backend")
    subagent2 = spawn("demo-fe", "Implement UI")
    result = aggregate(subagent1, subagent2)

# Writeback to Zrise
writeback(result)
```

---

## 👥 Cho Team Members

### Để triển khai, team chỉ cần:

1. **Tạo agent config** trong `openclaw.json`:
```json
{
  "id": "your-agent",
  "name": "Your Agent",
  "workspace": "/path/to/workspace",
  "skills": ["zrise-connect", "coding-agent", "github"],
  "model": {"primary": "zai/glm-5-turbo"}
}
```

2. **Agent sẽ tự động:**
   - Nhận task từ Zrise
   - Quyết định tự xử lý hay spawn subagents
   - Xử lý task
   - Writeback kết quả

3. **Không cần:**
   - Tạo workflow phức tạp
   - Quản lý 3 phases
   - Coordinate giữa nhiều agents

---

## 🔧 Workflow Types

### Simple (Recommended)
```yaml
# 1 step
steps:
  - execute → agent handles everything
```

**Use for:** Hầu hết tasks

### General (Deprecated)
```yaml
# 3 phases
steps:
  - plan
  - execute
  - approve
```

**Use for:** Legacy compatibility only

---

## 📊 Comparison

| Aspect | Simple | General (Old) |
|--------|--------|---------------|
| Phases | 1 | 3 |
| Agent calls | 1 | 3 |
| Complexity | Low | High |
| Flexibility | High (agent decides) | Low (fixed flow) |
| Recommended | ✅ Yes | ❌ No |

---

## 🎓 Examples

### Example 1: Simple Task
```
Task: "Tạo API endpoint để fetch users"

Agent zrise-worker:
1. Phân tích: Simple backend task
2. Tự xử lý:
   - Fetch task details
   - Generate code
   - Write to file
3. Writeback to Zrise
```

### Example 2: Complex Task
```
Task: "Xây dựng tính năng đăng nhập"

Agent zrise-worker:
1. Phân tích: Complex, needs multiple skills
2. Spawn subagents:
   - demo-be: Implement backend auth
   - demo-fe: Implement login UI
   - demo-qc: Write tests
3. Aggregate results
4. Writeback to Zrise
```

---

## 📁 Files

```
skills/zrise-connect/
├── workflows/
│   ├── simple.lobster          # ✅ Simple workflow (1 step)
│   ├── general.lobster         # ❌ Old workflow (3 phases)
│   └── ...
├── scripts/
│   ├── execute_task.py         # Main entry point
│   └── ...
└── skill.json                  # Config
```

---

## 🔄 Migration

### Từ General → Simple

**Trước:**
```bash
python3 run_workflow.py --task-id 42174 --phase plan
python3 run_workflow.py --task-id 42174 --phase execute
python3 run_workflow.py --task-id 42174 --phase approve
```

**Sau:**
```bash
python3 execute_task.py --task-id 42174 --workflow simple
```

---

## 💡 Tips

1. **Luôn dùng `simple` workflow** cho tasks mới
2. **Agent tự quyết định** - không cần specify phases
3. **Subagents được spawn tự động** - không cần manual coordination
4. **Writeback tự động** - không cần call riêng

---

## 🆘 Troubleshooting

### Task không chạy?
```bash
# Check agent config
cat ~/.openclaw/openclaw.json | grep -A 5 '"zrise"'

# Check session logs
tail -f ~/.openclaw/agents/zrise/sessions/*.jsonl
```

### Agent không spawn subagents?
- Check `subagents.allowAgents` trong openclaw.json
- Agent sẽ log decision trong session

---

## 📚 Related Docs

- `ARCHITECTURE.md` - System architecture
- `TEAM.md` - Team structure
- `skill.json` - Workflow configs
