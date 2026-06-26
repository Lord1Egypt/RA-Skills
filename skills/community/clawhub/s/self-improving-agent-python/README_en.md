# Self-Improving Agent

Enables Agents with self-evaluation, learning, and iteration capabilities.

## Overview

An Agent should not only execute tasks, but also learn from execution and continuously optimize its performance.

Three-layer self-improvement mechanism:
1. **Real-time Feedback Loop** - Immediate evaluation after each task execution
2. **Periodic Deep Reflection** - Regular in-depth analysis to identify systemic issues
3. **Cross-Agent Experience Sharing** - All Agents share learning outcomes

## Scoring Formula

```
Total Score = Completion(30%) + Efficiency(20%) + Quality(30%) + Satisfaction(20%)
```

| Score | Level | Action |
|-------|-------|--------|
| ≥90 | Excellent | Document best practices |
| 80-89 | Good | Continue current approach |
| 70-79 | Adequate | Identify areas for improvement |
| <70 | Needs Work | Trigger deep reflection |

## Installation

```bash
# Clone to WorkBuddy skills directory
git clone https://github.com/Brandon114/self-improving-agent_python.git ~/.workbuddy/skills/self-improving-agent
```

Or manually copy to `~/.workbuddy/skills/self-improving-agent/`

## Usage

```bash
# 1. Evaluate task execution
python scripts/evaluate_task.py \
    --agent-id "my-agent" \
    --task-id "task-001" \
    --task-type "content-creation" \
    --completion 90 \
    --efficiency 85 \
    --quality 80 \
    --satisfaction 85

# 2. Record lessons learned
python scripts/learn_lesson.py \
    --agent-id "my-agent" \
    --lesson "Validate link effectiveness" \
    --impact "high" \
    --category "quality"

# 3. Analyze and generate optimization plan
python scripts/optimize_agent.py --agent-id "my-agent"

# 4. Cross-Agent learning sync
python scripts/sync_learning.py
```

## Data Storage

Data is stored in the workspace directory `{workspace}/self-improvement/`:

| File | Description |
|------|-------------|
| evaluations.json | Task evaluation records |
| lessons-learned.json | Lesson library |
| optimization-plan.json | Optimization plan |
| collective-wisdom.json | Shared knowledge base |

## Supported Platforms

- **Python Version**: macOS / Linux / Windows (WSL)
- **PowerShell Version**: Windows (OpenClaw)

---

MIT License
