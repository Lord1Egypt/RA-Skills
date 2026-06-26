# Agent-to-Agent Architecture

## 🎯 Mục tiêu

Đơn giản hóa workflow bằng cách:
- ❌ Bỏ `execute_task.py` trung gian
- ❌ Bỏ `run_workflow.py` trung gian
- ✅ **Agent-to-agent trực tiếp**

---

## 📋 Architecture

### Trước (Phức tạp)

```
UI Approve
     ↓
execute_task.py
     ↓
run_workflow.py
     ↓
lobster workflow
     ↓
Agent zrise
     ↓
Subagents
```

### Sau (Đơn giản)

```
UI Approve
     ↓
POST /api/sessions/{task_id}/trigger
     ↓
Spawn agent `zrise` directly
     ↓
Agent analyzes task
     ↓
Agent spawns subagents if needed
     ↓
Writeback to Zrise
```

---

## 🔧 Implementation

### 1. UI Trigger Endpoint

**Update `/api/sessions/{task_id}/trigger`:**

```python
# Old (complex)
cmd = ['python3', 'run_workflow.py', '--task-id', str(task_id), ...]

# New (simple)
cmd = [
    'openclaw', 'agent',
    '--agent', selected_agent,  # From agent_selector
    '--local',
    '--session-id', f'zrise-{task_id}',
    '--message', f'''Execute task #{task_id}

Task: {task_name}
Description: {task_description}

Instructions:
1. Analyze task
2. Determine approach
3. Spawn subagents if needed
4. Execute
5. Writeback to Zrise
'''
]
```

### 2. Agent Behavior

**Agent `zrise` (or selected agent):**

```python
# On receive task message
1. Parse task ID from message
2. Fetch task from Zrise
3. Analyze task type
4. Decide approach:
   - Simple task → Process yourself
   - Complex task → Spawn subagents
5. Execute work
6. Writeback to Zrise
```

---

## 🚀 Benefits

### Đơn Giản

- ✅ 1 layer thay vì 3 layers
- ✅ Không cần maintain execute_task.py
- ✅ Không cần lobster workflows
- ✅ Agent-to-agent communication built-in

### Flexible

- ✅ Agent tự quyết định approach
- ✅ Easy to change behavior in agent code
- ✅ No workflow file changes needed

### Powerful

- ✅ Agents can spawn subagents natively
- ✅ Full agent capabilities available
- ✅ Built-in session management

---

## 📝 Code Changes

### workflow_manager_ui.py

```python
# Line ~642: Update trigger endpoint

match = re.match(r'^/api/sessions/(\d+)/trigger$', path)
if match:
    task_id = int(match.group(1))
    
    # Get task info
    task = fetch_task_from_zrise(task_id)
    
    # Select agent (auto or manual)
    selected_agent = body.get('agent') or auto_select_agent(task)
    
    # Build message
    message = f"""Execute task #{task_id}

Task: {task['name']}
Description: {task['description']}
Project: {task['project']}
Priority: {task['priority']}

Instructions:
1. Fetch full task details from Zrise
2. Analyze requirements
3. Determine approach (do yourself or spawn subagents)
4. Execute the work
5. Writeback results to Zrise
6. Update task stage to Done when complete
"""
    
    # Spawn agent directly
    cmd = [
        'openclaw', 'agent',
        '--agent', selected_agent,
        '--local',
        '--session-id', f'zrise-{task_id}',
        '--message', message
    ]
    
    proc = subprocess.Popen(cmd, cwd=str(ROOT))
    
    self.send_json({
        'ok': True,
        'task_id': task_id,
        'agent': selected_agent,
        'pid': proc.pid
    })
```

---

## 🎨 UI Updates

### Simplify Buttons

**Before:**
```
[Re-plan] [Resume] [Execute] [Approve]
```

**After:**
```
[Execute Task]  ← Single button
```

### Agent Selection

```
┌──────────────────────────┐
│ Task #42174              │
│                          │
│ Agent: demo-be (auto) ▼  │
│   ├─ demo-be (Backend)   │
│   ├─ demo-fe (Frontend)  │
│   └─ ...                 │
│                          │
│ [Execute Task]           │
└──────────────────────────┘
```

---

## 📊 Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Layers** | 3 (execute → run → agent) | 1 (agent direct) |
| **Scripts** | 2 intermediate scripts | 0 intermediate |
| **Workflow files** | Required (.lobster) | Not needed |
| **Flexibility** | Limited by workflow | Full agent freedom |
| **Maintenance** | High | Low |

---

## ✅ Summary

**Agent-to-agent architecture:**

1. ✅ **Đơn giản** - 1 layer thay vì 3
2. ✅ **Flexible** - Agent tự quyết định
3. ✅ **Powerful** - Full agent capabilities
4. ✅ **Maintainable** - Ít code hơn

**Không cần:**
- ❌ `execute_task.py`
- ❌ `run_workflow.py`
- ❌ `.lobster` workflows

**Chỉ cần:**
- ✅ Agent config trong `openclaw.json`
- ✅ Agent routing trong `agent-routing.json`
- ✅ Agent code xử lý task

---

## 🚀 Next Steps

1. Update `workflow_manager_ui.py` trigger endpoint
2. Simplify UI buttons
3. Test agent-to-agent execution
4. Document for team

**Giờ workflow cực kỳ đơn giản: UI → Agent → Done!** 🎉
