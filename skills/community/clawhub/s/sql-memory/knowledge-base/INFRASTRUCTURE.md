# Infrastructure & Application Framework
_Oblio System Architecture — Documented 2026-03-09_

---

## Core Principles

### 1. Task Decomposition Pattern
**Never execute tasks blindly.** Understand the goal first, then break into recursive subtasks.

**Pattern:**
```
GOAL (macro understanding)
  ↓
SUBTASK 1 (macro+micro context) → Agent chooses decomposition level
SUBTASK 2 (macro+micro context) → Agent executes or breaks down further
SUBTASK 3 (macro+micro context) → Recursive until atomic
```

**Example:**
- GOAL: "Enable dashboard reporting"
- MACRO: Users need to see system state (reports, queue, logs)
- SUBTASKS:
  - Backend 1: Cache layer (SQL data + TTL)
  - Backend 2: REST endpoints (/api/report, /api/queue, /api/logs)
  - Frontend 1: Report view rendering
  - Frontend 2: Queue view rendering
  - Frontend 3: Logs view rendering
  - QA: Integration tests

**Benefits:**
- Agents see the big picture → smarter decisions
- Parallel execution → efficiency
- Recursive decomposition → handles complexity naturally
- No "what do I do next?" bottleneck

---

## Architecture Layers

### Layer 1: Data (SQL Memory)

**Primary Backend:** Cloud (SQL5112.site4now.net)
```
Database: db_99ba1f_memory4oblio
Schema: memory.*
```

**Tables:**
- `memory.Memories` — Facts, decisions, learnings (domain, key, content)
- `memory.Sessions` — Session snapshots for continuity
- `memory.TaskQueue` — Work queue (agent, task_type, status, priority)
- `memory.KnowledgeIndex` — Knowledge base (domain, topic, summary)
- `memory.ActivityLog` — Agent activity (agent, event_type, description)

**Module:** `infrastructure/sql_memory.py`
- Dual-backend support (local fallback, cloud primary)
- 15+ methods: remember, recall, queue_task, complete_task, log_event, etc.
- Automatic retry + graceful degradation

**Configuration:**
```python
# All agents default to cloud
db = SQLMemory('cloud')
```

---

### Layer 2: Agent Framework

**Base Class:** `infrastructure/agent_base.py` → `OblioAgent`

**Features:**
- SQL memory integration (auto-logging to ActivityLog)
- Model selection via model_router.py
- Structured logging (file + DB)
- Graceful error handling with retry (3 attempts default)
- Ollama inference (text, chat, vision, embeddings)
- Reporting framework (per-agent metrics)

**Standard Methods:**
```python
class MyAgent(OblioAgent):
    agent_name = "my_agent"
    task_types = ["my_task_type"]
    backend = "cloud"  # MUST be "cloud"
    
    def run_task(self, task: dict) -> str:
        # Run one task, return summary
        pass

# Usage
agent = MyAgent()
agent.run_once()  # Process all pending tasks once
agent.run_loop(interval=60)  # Loop continuously
```

**Logging:**
```python
# Automatic to logs/my_agent.log
self.log.info("message")

# Automatic to memory.ActivityLog via
self.log_activity("event_type", "description", "metadata")
```

---

### Layer 3: Task Queue & Dispatch

**Queue System:** `infrastructure/sql_memory.py` + `agents/agent_dispatcher.py`

**Task Structure:**
```json
{
  "id": 47,
  "agent": "backend",
  "task_type": "dashboard_cache_layer",
  "payload": {
    "macro": "Agents need reliable, cached access to SQL data",
    "component": "util/dashboard_cache.py",
    "methods": ["get_latest_report", "get_queue_status", "get_recent_logs"],
    "ttl_seconds": 30,
    "tests_required": true
  },
  "priority": 9,
  "status": "pending",
  "created_at": "2026-03-09T06:40:00Z"
}
```

**Task Lifecycle:**
1. Queue → Pending
2. Agent claims → Processing
3. Agent executes → Completed (with result) OR Failed (with error)

**Dispatcher:** Routes tasks by type to specialized agents or handles directly
- Handles: github_setup, github_clone, github_checkin, ui_fix, security_test
- Scheduled: Every 3 hours (cron: `0 */3 * * *`)

---

### Layer 4: AI Models

**Primary:** Ollama (local to DEAUS 10.0.0.110:11434)

**Available Models:**
- `gemma3:4b` — Text generation (default, free)
- `codellama:7b` — Code analysis + generation
- `mistral:7b` — General purpose LLM
- `llava` — Vision (images)
- `moondream` — Lightweight vision
- `nomic-embed-text` — Embeddings

**Model Router:** `infrastructure/model_router.py`
- Selects model by task_type + budget tier
- Routing logic: `select_model(task_type, budget, **kwargs)`
- Falls back to cloud APIs (with approval) if needed

**Usage:**
```python
# Agent automatically selects model
result = self.ollama_generate(prompt="...", model="gemma3:4b")

# Or let router choose
model = self.get_model(task_type="code_analysis", budget="free")
result = self.ollama_generate(prompt, model)
```

---

### Layer 5: Specialized Agents

**Current Agents:**

| Agent | Purpose | Cron | Type |
|-------|---------|------|------|
| `agent_stamps.py` | Stamp identification + cataloging | 0 */2 * * * | Background |
| `agent_facs.py` | FACS micro-expression training | 0 2 * * * | Background |
| `agent_nlp.py` | NLP document processing | 30 2 * * * | Background |
| `agent_security.py` | Security audits (11 checks) | 30 3 * * * | Background |
| `agent_dispatcher.py` | General task router | 0 */3 * * * | Background |
| `agent_idle.py` | Background task scheduling | */15 * * * * | Background |
| `agent_reporter.py` | Daily reports (4:20 AM/PM) | 20 4,16 * * * | Reporting |

---

## Development Standards

### Solid Design Paradigm

**Requirements:**
1. **Every function MUST have a unit test**
   - Write test first (TDD)
   - Test covers happy path + error cases
   - Never ship untested code

2. **No silent failures**
   - All errors logged with severity (INFO, WARN, ERROR, CRITICAL)
   - Errors surface in dashboard alerts
   - Retry logic for transient failures

3. **SOLID Principles**
   - Single Responsibility: One job per class/function
   - Open/Closed: Open for extension, closed for modification
   - Liskov Substitution: Agents interchangeable
   - Interface Segregation: Minimal required interfaces
   - Dependency Inversion: Depend on abstractions (sql_memory), not concrete

4. **DRY (Don't Repeat Yourself)**
   - Shared code → `infrastructure/` modules
   - Agents inherit from OblioAgent base class
   - Configuration in `.env` (not hardcoded)

5. **Composition over Inheritance**
   - Agents compose behaviors (memory, models, logging)
   - Not deep inheritance hierarchies
   - Mixins for orthogonal concerns

### GitHub Workflow

**Repositories:**
- `VeXHarbinger/AI-UI` — Dashboard application
- `VeXHarbinger/sequel-memory-skill` — SQL memory skill
- `VeXHarbinger/clawbot-sql-memory` — Memory infrastructure
- `Oblio-Falootin/*` — Infrastructure/tooling (not for sharing)

**Branch Strategy:**
```
main (stable, tagged releases)
  ↑
development (next release, PR-based)
  ↑
feature/* (individual features, merged via PR)
```

**PR Requirements:**
- [ ] Tests pass (100% of changed code)
- [ ] Code review approved
- [ ] CI pipeline green
- [ ] Documentation updated

**Initial Checkin Checklist:**
- [ ] README.md (what, how, why)
- [ ] ARCHITECTURE.md (design decisions, module breakdown)
- [ ] tests/README.md (how to run tests)
- [ ] tests/test_*.py (unit tests for all functions)
- [ ] .gitignore (Python: .pyc, __pycache__, .env, venv/)
- [ ] .github/workflows/test.yml (CI: run pytest on push)

---

## Cron Schedule

**Execution Times:**

```
*/5 min   → inbox_monitor (file watcher keepalive)
*/15 min  → agent_idle (background scheduling when CPU < 15%)
*/30 min  → task-monitor.sh (check for stuck tasks)

0 1 * * * → agent_github (GitHub monitoring)
15 1 * * * → agent_git_sync (repo sync)
0 2 * * * → agent_facs (FACS training)
30 2 * * * → agent_nlp (NLP training)
0 3 * * * → agent_lightsound (background task)
30 3 * * * → agent_security (security audit)
0 3,15 * * * → db_backup (SQL backup + rotate)
0 */2 * * * → agent_stamps (stamp processing)
20 4,16 * * * → agent_reporter (daily report)
0 */3 * * * → agent_dispatcher (task dispatch)
```

---

## Testing Framework

**Structure:**
```
tests/
  __init__.py
  conftest.py              # Pytest fixtures (mock DB, etc.)
  test_dispatcher.py       # Task dispatcher tests
  test_agent_base.py       # Base agent tests
  test_sql_memory.py       # Memory module tests
  test_model_router.py     # Model selection tests
  test_ui_endpoints.py     # Dashboard API tests
  test_dashboard_*.py      # UI component tests
```

**Requirements:**
- **Coverage:** ≥ 80% of production code
- **Test types:**
  - Unit: Test functions in isolation (mock dependencies)
  - Integration: Test components together
  - End-to-end: Test full workflows
- **Naming:** `test_<function>_<scenario>.py`
- **Assertions:** Clear, specific (not just `assertTrue`)

**Run Tests:**
```bash
python -m unittest discover tests/ -v
# or
python -m pytest tests/ -v --cov=.
```

---

## Quality Gates

**Before merging to main:**

1. [ ] All tests pass (100% of changed code)
2. [ ] No new warnings/errors in logs
3. [ ] Code review approved (peer or lead)
4. [ ] Documentation updated
5. [ ] Commit messages clear + descriptive

**Before deploying:**

1. [ ] Tag release (v0.1.0, v1.2.3, etc.)
2. [ ] Update CHANGELOG.md
3. [ ] CI pipeline green
4. [ ] Manual testing in staging
5. [ ] Rollback plan documented

---

## Monitoring & Debugging

**Logs Location:** `/home/oblio/.openclaw/workspace/logs/`
- `agent_*.log` — Per-agent logs
- `sql_memory.log` — SQL query log
- `dispatcher.log` — Task dispatcher
- `report-*.md` — Daily reports

**Memory Location:** SQL `memory.*` tables
- Query agent activity: `SELECT * FROM memory.ActivityLog ORDER BY timestamp DESC`
- Query task queue: `SELECT * FROM memory.TaskQueue WHERE status='pending'`
- Query memories: `SELECT * FROM memory.Memories WHERE domain='....'`

**Dashboard:** http://localhost:3000
- Report: Latest 4:20 AM/PM summary
- Queue: Pending + in-progress tasks
- Logs: Recent agent activity

---

## Deployment Checklist

**First Time Setup:**

```bash
# 1. Clone repo
git clone https://github.com/VeXHarbinger/clawbot-sql-memory.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env
cp .env.example .env
# Edit .env with cloud DB credentials

# 4. Run tests
python -m unittest discover tests/ -v

# 5. Start agents
crontab -e  # Add cron jobs
# or manually: python agents/agent_dispatcher.py
```

**Verification:**

```bash
# Check cloud DB connection
python -c "from sql_memory import SQLMemory; db = SQLMemory('cloud'); print(db.execute('SELECT COUNT(*) FROM memory.TaskQueue'))"

# Start UI
cd ui && npm start

# Monitor logs
tail -f logs/*.log
```

---

## Troubleshooting

**Problem:** "No pending tasks"
- Check: `SELECT * FROM memory.TaskQueue WHERE status='pending'`
- Check agent filter: `agent='dispatcher'` and task_type matches

**Problem:** "Cloud DB connection timeout"
- Check `.env` credentials
- Check firewall (site4now accessible from your network)
- Try local backend as fallback

**Problem:** "Ollama not responding"
- Check DEAUS is reachable: `curl http://10.0.0.110:11434`
- Check model available: `ollama list`
- Pull model: `ollama pull gemma3:4b`

**Problem:** "Tests failing with SQL errors"
- Mock DB in tests (don't hit cloud during tests)
- Use `infrastructure/agent_base.py` test fixtures
- Check `.env` not loaded in test environment

---

## Next Steps & Continuous Improvement

1. **Monitor queue** — Periodically check pending tasks
2. **Review logs** — Look for WARN/ERROR patterns
3. **Optimize bottlenecks** — Profile slow tasks
4. **Add tests** — If test coverage < 80%, add tests
5. **Refactor** — Clean up tech debt before new features
6. **Document decisions** — Update ARCHITECTURE.md as design evolves

---

_Last updated: 2026-03-09 | Framework version: 1.0_
