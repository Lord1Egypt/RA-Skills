---
name: team-code
description: Coordinate multiple AI agents as a development team to tackle complex coding projects faster and more accurately. Like having a team of engineers working in parallel on different parts of your codebase—each in their own isolated branch, with automatic integration and verification. Use for multi-file features, complex refactors, or any project where parallel development beats solo coding. Works like pair programming, but with as many agents as your task needs (2-4 recommended, max 8).
---

# Team Code - Multi-Agent Development

**Team Code** implements the **CAID (Centralized Asynchronous Isolated Delegation)** research paradigm for coordinating multiple AI agents as a development team.

Think of it like this: instead of one developer working alone on a complex feature, you have a team of specialists working in parallel—each in their own isolated workspace, with a tech lead (manager) coordinating who works on what and when.

> ⚠️ **CRITICAL WARNINGS:**
> - **Use Team Code from the start** — Don't try solo first. Sequential attempts cost nearly 2x with minimal gain.
> - **Physical branch isolation is mandatory** — Shared workspaces cause silent conflicts that break everything.
> - **Team size matters** — 2 agents for research tasks, 4 for clear codebases, never exceed 8.
> - **Higher cost, better results** — Team Code improves accuracy (+26%), not speed. Worth it for important code.

## The Analogy: Human Dev Team

| Human Team | Team Code |
|------------|-----------|
| Tech lead assigns tasks | Manager builds dependency graph |
| Developers work in branches | Agents work in git worktrees |
| Pull requests for review | Self-verification before commit |
| Merge conflicts resolved by author | Agent resolves their own conflicts |
| Code review before shipping | Manager final review |

## When to Use Team Code

**Perfect for:**
- 🏗️ **Building features** that touch multiple files (auth, API, database)
- 🔄 **Complex refactors** with clear dependency chains
- 📚 **Implementing libraries** from scratch with test suites
- 🔬 **Research reproductions** (paper implementations)

**Skip for:**
- 🔧 One-line fixes or single-file changes
- 🧪 Pure exploration without clear structure
- ⏱️ Quick prototypes where "good enough" is fine

## The Workflow

### Phase 0: Setup (Manager = You)

Before the team starts, prepare the environment:

```bash
cd your-project

# Ensure dependencies work
pip install -r requirements.txt  # or npm install, etc.

# Create minimal stubs so imports don't fail
mkdir -p src/feature
touch src/feature/__init__.py src/feature/module_a.py src/feature/module_b.py

# Commit so team starts from known state
git add .
git commit -m "setup: initial feature structure"
```

### Phase 1: Plan (Dependency Graph)

Analyze what needs to be built and in what order:

```
Your Task: "Add user authentication"

Dependencies:
  database.py ─→ models.py ─→ auth.py ─→ api.py
     (none)      (needs db)   (needs    (needs
                               models)   auth)

Round 1: database.py (foundation)
Round 2: models.py (depends on db)
Round 3: auth.py (depends on models)
Round 4: api.py (depends on auth)
```

### Phase 2: Delegate to Agents

```javascript
// Agent 1: Database (no dependencies)
await sessions_spawn({
  runtime: "subagent",
  task: `
    Implement database connection in src/feature/database.py
    - connect() function
    - Connection pooling
    - Error handling
    
    VERIFY: pytest tests/test_database.py -v
    RESTRICTED: src/feature/__init__.py
  `,
  agentId: "coding-agent",
  mode: "run",
  runTimeoutSeconds: 400
});
```

```javascript
// Agent 2: Models (after database completes)
await sessions_spawn({
  runtime: "subagent",
  task: `
    Implement User model in src/feature/models.py
    - User class with SQLAlchemy
    - Fields: id, username, email, password_hash
    - Methods: set_password(), check_password()
    
    DEPENDS ON: database module (completed)
    VERIFY: pytest tests/test_models.py -v
    RESTRICTED: src/feature/__init__.py, src/feature/database.py
  `,
  agentId: "coding-agent",
  mode: "run",
  runTimeoutSeconds: 400
});
```

### Phase 3: Integrate

```bash
# When agent signals completion
git checkout main
git merge feature/database

# If conflict - agent who created it resolves:
cd ../workspace-database
git pull origin main
# fix conflicts
pytest tests/test_database.py -v
git commit --amend
```

### Phase 4: Final Review

```bash
# After all rounds complete
git checkout main
pytest tests/ -v                    # Full test suite
python -c "from src.feature import auth; print('OK')"  # Smoke test
```

## Team Size Guide

| Task Type | Team Size | Why |
|-----------|-----------|-----|
| Research/paper reproduction | 2 | Complex dependencies, manager heavy |
| Library implementation | 4 | Clear file structure, parallelizable |
| API + frontend feature | 2-3 | Frontend/backend parallel |
| Simple multi-file refactor | 2 | Limited parallelism |
| **Never exceed** | 8 | Coordination tax exceeds gains |

## Key Principles

### 1. **Branch Isolation is Mandatory**

```bash
# CORRECT: Physical isolation
git worktree add ../workspace-agent-1 feature/task-1
git worktree add ../workspace-agent-2 feature/task-2

# WRONG: Soft isolation (leads to conflicts)
# All agents in same directory with "don't touch each other's files"
```

### 2. **Self-Verification Before Commit**

Agent must run tests and fix failures BEFORE submitting:

```bash
pytest tests/test_my_module.py -v  # Must pass
git commit -m "implement: feature X"  # Only then
```

### 3. **Structured Communication Only**

Use JSON task specs, not conversation:

```json
{
  "task_id": "implement-auth",
  "description": "JWT authentication",
  "files": ["src/auth/jwt.py"],
  "verify": "pytest tests/test_jwt.py -v",
  "restricted": ["src/auth/__init__.py"]
}
```

### 4. **Agent Resolves Their Own Conflicts**

If merge fails, the agent who wrote the code fixes it—not the manager.

## Common Patterns

### Pattern: Sequential Dependencies
```
A ─→ B ─→ C ─→ D
```
Start 1 agent, when done start next. Not parallel but structured.

### Pattern: Parallel Foundation
```
  ┌──→ A ──→ C ─┐
  │              ├──→ E
  └──→ B ──→ D ─┘
```
A and B parallel, then C and D parallel, then E.

### Pattern: Star (Common API Structure)
```
    ┌──→ Endpoint A
    │
DB ─┼──→ Endpoint B
    │
    └──→ Endpoint C
```
Database first, then all endpoints in parallel.

## Trade-offs

| Aspect | Solo Agent | Team Code |
|--------|-----------|-----------|
| Speed | Faster wall-clock | Similar/slower |
| Accuracy | 42-57% | 59-68% (+14-26%) |
| Cost | Lower | Higher |
| Best for | Quick fixes | Important code |

**Rule of thumb:** If you'd assign this to a human team, use Team Code.

## Quick Start Template

```javascript
// 1. Setup your project
cd my-project
git checkout -b feature/xyz

// 2. Create stubs
touch src/module.py
git add . && git commit -m "setup: stubs"

// 3. Plan dependencies
// Draw: what depends on what?

// 4. Spawn first agent (foundation)
const agent1 = await sessions_spawn({
  runtime: "subagent",
  task: "Implement foundation: src/core.py with...",
  mode: "run",
  timeoutSeconds: 400
});

// 5. Wait, integrate, repeat
await waitFor(agent1);
git merge feature/core;

// 6. Spawn dependent agents...

// 7. Final review
git checkout main
pytest tests/ -v
```

## References

- Research paper: "Effective Strategies for Asynchronous Software Engineering Agents" (arXiv:2603.21489v1)
- Original name: CAID (Centralized Asynchronous Isolated Delegation)
- GitHub: https://github.com/JiayiGeng/async-swe-agents

See [references/examples.md](references/examples.md) for detailed implementation examples.