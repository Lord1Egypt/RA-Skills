# Zrise Connect

**Zrise Connect** - Tự động hóa tasks trên Zrise bằng AI workflows.

## 🎯 Features

- ✅ **Workflow Management** — Tạo, sửa, xóa workflows qua Web UI
- ✅ **AI-Powered** — Xử lý tasks bằng OpenClaw Agent
- ✅ **8-Step Flow** — Poll → Analyze → Execute → Review → Writeback
- ✅ **Session Management** — Mỗi task có session riêng
- ✅ **Clarification Flow** — Tự động request info khi thiếu
- ✅ **HTML Comments** — Format đẹp trên Zrise
- ✅ **Permission Control** — Private/Team/Public workflows
- ✅ **10+ Templates** — Ready-to-use workflow templates

---

## 🚀 Quick Start

### 1. Start Web UI

```bash
cd skills/zrise-connect/scripts
python3 workflow_manager_ui.py --port 8888
```

**Access:** http://localhost:8888

### 2. Test Simple Workflow

```bash
python3 test_simple_workflow.py --task-id 42174 --approve
```

### 3. View Result

```
https://zrise.app/web#id=42174
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│  Employee (Web UI / Telegram)               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Workflow Manager UI (port 8888)            │
│  - Create/Edit/Delete workflows             │
│  - Test workflows                           │
│  - Share with team                          │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Workflow Registry (registry.json)          │
│  - 10+ workflow templates                   │
│  - Categories: general, analysis, dev, qa   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  OpenClaw Agent (zrise-analyst/dev/qa/pm)   │
│  - Process tasks with AI                    │
│  - Generate structured output               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Zrise Integration                          │
│  - Post HTML comments                       │
│  - Update task stage                        │
│  - Save conversation history                │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
skills/zrise-connect/
├── scripts/                    # Core scripts (34 files)
│   ├── workflow_manager_ui.py  # Web UI
│   ├── workflow_manager.py     # CLI manager
│   ├── workflow_registry.py    # Registry
│   ├── invoke_agent_for_task.py # Agent wrapper
│   ├── test_simple_workflow.py # E2E test
│   ├── post_html_comment.py    # HTML comments
│   ├── configure_openclaw_agent.py # Agent setup
│   ├── analyze_task.py         # Task analysis
│   ├── execute_ai_task.py      # Task execution
│   ├── request_clarification.py # Clarification flow
│   ├── poll_employee_work.py   # Poll tasks
│   └── ... (more scripts)
│
├── workflows/                  # Lobster workflows
│   ├── general.lobster
│   ├── email-draft.lobster
│   ├── requirement-analysis.lobster
│   └── zrise-execute.lobster
│
├── docs/                       # Documentation
│   ├── WORKFLOW_TEMPLATES.md
│   ├── WORKFLOW_UI_COMPLETE.md
│   ├── TELEGRAM_INTEGRATION.md
│   ├── TEAM_ONBOARDING.md
│   └── WORKFLOW_UI_DESIGN.md
│
├── state/                      # Runtime state
│   ├── zrise/
│   │   ├── sessions/           # Session state
│   │   ├── poll-state/         # Poll state
│   │   ├── work-items/         # Work items
│   │   └── test-reports/       # Test results
│   └── approvals/              # Approval requests
│
├── config/                     # Configuration
│   └── zrise/
│       └── agent-routing.json  # Agent definitions
│
├── SKILL.md                    # Skill documentation
├── skill.json                  # Skill manifest
└── README.md                   # This file
```

---

## 📚 Available Workflows

| Workflow | Purpose | Category |
|----------|---------|----------|
| `general` | Xử lý task tổng quát | general |
| `email-draft` | Soạn email | communication |
| `requirement-analysis` | Phân tích requirement | analysis |
| `technical-design` | Thiết kế kỹ thuật | design |
| `implementation` | Implementation plan | development |
| `code-review` | Review code | review |
| `testing` | Test plan | qa |
| `documentation` | Tạo docs | docs |
| `pm-planning` | PM planning | pm |
| `clarification-request` | Request info | clarification |

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Zrise Connection
ZRISE_URL=https://zrise.app
ZRISE_DB=zrise
ZRISE_USERNAME=admin
ZRISE_API_KEY=your_api_key

# OpenClaw Agents (optional)
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-flash
```

### Agent Configuration

```bash
# Setup agents
python3 configure_openclaw_agent.py --setup

# Check configuration
python3 configure_openclaw_agent.py --check
```

---

## 🧪 Testing

### E2E Tests (48 tests, 91.7% pass)

```bash
# Run all E2E tests
python3 zrise_e2e_test.py --all --task-id 42174

# Run session tests
python3 zrise_session_e2e_test.py --task-id 42174

# Run simple workflow test
python3 test_simple_workflow.py --task-id 42174 --approve
```

### Test Results

```
Step E2E Tests:    32 tests, 29 passed (90.6%)
Session E2E Tests: 16 tests, 15 passed (93.8%)
Total:             48 tests, 44 passed (91.7%)
```

---

## 📖 Documentation

### For Users

- **[Team Onboarding](docs/TEAM_ONBOARDING.md)** — Hướng dẫn cho nhân viên mới
- **[Workflow Templates](docs/WORKFLOW_TEMPLATES.md)** — Library of templates
- **[Workflow UI Guide](docs/WORKFLOW_UI_COMPLETE.md)** — How to use Web UI

### For Developers

- **[Telegram Integration](docs/TELEGRAM_INTEGRATION.md)** — Setup Telegram bot
- **[Workflow Design](docs/WORKFLOW_UI_DESIGN.md)** — Architecture & design
- **[SKILL.md](SKILL.md)** — Technical documentation

---

## 🛠️ Common Tasks

### Create Custom Workflow

```bash
# Via CLI
python3 workflow_manager.py --create \
  --name "my-workflow" \
  --description "My custom workflow" \
  --category "custom" \
  --file my-workflow.yaml

# Via Web UI
open http://localhost:8888
# Click "+ New Workflow"
```

### Post HTML Comment

```bash
python3 post_html_comment.py \
  --task-id 42174 \
  --title "Analysis Result" \
  --content "**Bold** and *italic* text"
```

### List Workflows

```bash
python3 workflow_registry.py --list
```

---

## 🐛 Troubleshooting

### Workflow không chạy?

```bash
# Check workflow exists
python3 workflow_registry.py --search "workflow-name"

# Check task exists
python3 fetch_task_data.py 42174

# Check logs
tail -f state/zrise/logs/*.log
```

### Comment không hiện?

```bash
# Test HTML format
python3 post_html_comment.py --task-id 42174 --title "Test" --content "Test" --test

# Check Zrise connection
python3 -c "from zrise_utils import connect_zrise; print(connect_zrise())"
```

### Agent không work?

```bash
# Check agent config
python3 configure_openclaw_agent.py --check

# Re-setup agents
python3 configure_openclaw_agent.py --setup
```

---

## 📊 Stats

- **Scripts:** 34 files
- **Workflows:** 10+ templates
- **Tests:** 48 tests, 91.7% pass
- **UI Port:** 8888
- **Agents:** 4 (analyst, dev, qa, pm)

---

## 🤝 Contributing

### Add New Workflow

1. Create `.lobster` file in `workflows/`
2. Add prompt to `invoke_agent_for_task.py`
3. Register: `python3 workflow_manager.py --create ...`
4. Test: `python3 test_simple_workflow.py --task-id X`
5. Document in `docs/WORKFLOW_TEMPLATES.md`

### Report Issues

1. Check existing docs
2. Run diagnostics
3. Create issue with:
   - Steps to reproduce
   - Expected vs actual
   - Logs/screenshots

---

## 📝 License

MIT License

---

## 🎉 Credits

- **OpenClaw** — Agent framework
- **Lobster** — Workflow orchestration
- **Zrise** — Task management
- **Gemini** — AI model (optional)

---

**Zrise Connect - Automate your tasks with AI!** 🚀
