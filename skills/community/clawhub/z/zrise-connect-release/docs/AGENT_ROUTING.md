# Agent Routing & Selection

## 🎯 Overview

Hệ thống tự động chọn agent phù hợp để execute task, hoặc user có thể chỉ định agent khi approve.

---

## 📋 Architecture

```
Task từ Zrise
     ↓
agent_selector.py
     ↓
Auto-select based on:
  - Task keywords
  - Agent skills
  - Agent priority
     ↓
Selected Agent
     ↓
Execute Task
```

---

## 🔧 Config File

**Location:** `config/zrise/agent-routing.json`

### Structure

```json
{
  "agents": {
    "demo-be": {
      "name": "Backend Developer",
      "skills": ["python", "api", "database"],
      "keywords": ["backend", "api", "server"],
      "priority": 1,
      "auto_select": true,
      "max_concurrent": 3
    },
    "demo-fe": {
      "name": "Frontend Developer",
      "skills": ["html", "css", "javascript"],
      "keywords": ["frontend", "ui", "web"],
      "priority": 1,
      "auto_select": true
    }
  },
  "default_agent": "demo-be",
  "routing_rules": [...]
}
```

### Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable agent name |
| `skills` | array | Skills agent possesses |
| `keywords` | array | Keywords to match in task description |
| `priority` | number | Lower = higher priority (1 = highest) |
| `auto_select` | boolean | Can be auto-selected |
| `max_concurrent` | number | Max concurrent tasks |
| `estimated_time` | string | Estimated execution time |

---

## 🚀 Usage

### 1. Auto Selection (Default)

```bash
# System will auto-select agent based on task
python3 execute_task.py --task-id 42174

# Output:
# 🔍 Auto-selecting agent for task...
# ✅ Selected agent: Backend Developer (auto)
```

### 2. Manual Selection

```bash
# Specify agent manually
python3 execute_task.py --task-id 42174 --agent demo-fe

# Output:
# EXECUTING TASK #42174
# Agent: demo-fe
```

### 3. List Available Agents

```bash
python3 agent_selector.py --list

# Output:
{
  "agents": [
    {
      "id": "demo-be",
      "name": "Backend Developer",
      "skills": ["python", "api", "database"],
      "auto_select": true
    },
    ...
  ],
  "default": "demo-be"
}
```

---

## 📊 Selection Logic

### Scoring Algorithm

```python
for each agent in agents:
    score = 0
    
    # Keyword matching (weight: 10)
    for keyword in agent.keywords:
        if keyword in task_text:
            score += 10
    
    # Skill matching (weight: 5)
    for skill in agent.skills:
        if skill in task_text:
            score += 5
    
    # Priority adjustment
    score = score / agent.priority
    
return agent_with_highest_score
```

### Example

```
Task: "Implement backend API for user authentication"

Matching:
  demo-be: "backend" (10) + "api" (10) = 20 → 20/1 = 20
  demo-fe: 0 → 0/1 = 0
  demo-qc: 0 → 0/2 = 0

Selected: demo-be (score: 20)
```

---

## 👥 For Team Members

### Adding New Agent to Routing

1. **Create agent** in `openclaw.json`:
```json
{
  "id": "my-custom-agent",
  "name": "My Custom Agent",
  "skills": ["skill1", "skill2"],
  "model": {"primary": "zai/glm-5-turbo"}
}
```

2. **Add to routing** in `config/zrise/agent-routing.json`:
```json
{
  "agents": {
    "my-custom-agent": {
      "name": "My Custom Agent",
      "skills": ["skill1", "skill2"],
      "keywords": ["keyword1", "keyword2"],
      "priority": 2,
      "auto_select": true
    }
  }
}
```

3. **Restart workflow UI** to pick up changes

---

## 🎨 UI Integration

### Workflow UI (Future)

```
┌─────────────────────────────────┐
│ Task #42174                     │
│                                 │
│ [Execute] ▼                     │
│   ├─ Auto (demo-be) ← default   │
│   ├─ demo-be                    │
│   ├─ demo-fe                    │
│   ├─ demo-qc                    │
│   └─ Manual...                  │
└─────────────────────────────────┘
```

### Approval Flow

```
1. Task analyzed
2. Agent auto-selected (demo-be)
3. User can change agent before approve
4. Execute with selected agent
```

---

## 🔍 Debugging

### Check Agent Selection

```bash
# Test agent selection for task
python3 agent_selector.py \
  --task-id 42174 \
  --task-name "Implement API" \
  --task-description "Create REST API endpoint"
```

### Check Available Agents

```bash
python3 agent_selector.py --list
```

### View Routing Config

```bash
cat config/zrise/agent-routing.json | python3 -m json.tool
```

---

## ⚙️ Advanced Configuration

### Routing Rules

```json
"routing_rules": [
  {
    "condition": "task.description contains 'ui'",
    "agent": "demo-fe"
  },
  {
    "condition": "task.priority == 'high'",
    "agent": "demo-architect"
  }
]
```

### Approval Requirements

```json
"approval_flow": {
  "auto_approve_agents": ["demo-be", "demo-fe"],
  "manual_approve_agents": ["demo-architect"],
  "require_user_selection": false
}
```

---

## 📝 Examples

### Example 1: Backend Task

```bash
# Task: "Create API endpoint for users"
python3 execute_task.py --task-id 42174

# Auto-selection:
# - demo-be: "api" (10) + "backend" implied = 10
# Selected: demo-be
```

### Example 2: Frontend Task

```bash
# Task: "Design login UI"
python3 execute_task.py --task-id 42175

# Auto-selection:
# - demo-fe: "ui" (10) + "design" implied = 10
# Selected: demo-fe
```

### Example 3: Manual Override

```bash
# Task: "Create API endpoint"
# But you want demo-fe to handle frontend integration

python3 execute_task.py --task-id 42174 --agent demo-fe

# Manual selection: demo-fe
```

---

## 🚨 Troubleshooting

### Wrong Agent Selected?

1. **Check keywords** in routing config
2. **Adjust priority** (lower = higher)
3. **Add more keywords** for better matching
4. **Use manual override** `--agent`

### Agent Not in List?

1. **Check agent config** in `openclaw.json`
2. **Add to routing** in `agent-routing.json`
3. **Set `auto_select: true`**
4. **Restart UI**

---

## 📚 Related Docs

- `SIMPLE_WORKFLOW_GUIDE.md` - Workflow usage
- `ARCHITECTURE.md` - System architecture
- `TEAM.md` - Team structure
