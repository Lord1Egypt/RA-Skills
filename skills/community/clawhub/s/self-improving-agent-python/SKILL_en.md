# Self-Improvement Agent Skill

Activate this skill when an Agent needs to learn from task execution and self-optimize.

---

## Activation Conditions

This skill activates when users mention:
- "self-improvement", "self-optimization", "learning experience"
- "task evaluation", "performance analysis"
- "optimize workflow", "improve efficiency"
- Any scenario where the Agent needs to learn from mistakes

---

## Core Concepts

An Agent should not only execute tasks, but also learn from execution and continuously optimize its performance.

Three-layer self-improvement mechanism:
1. **Layer 1: Real-time Feedback Loop** - Immediate evaluation after each task execution
2. **Layer 2: Periodic Deep Reflection** - Regular in-depth analysis
3. **Layer 3: Cross-Agent Experience Sharing** - Shared learning outcomes

---

## Task Evaluation Standards

### Scoring Formula

Total Score = Completion(30%) + Efficiency(20%) + Quality(30%) + Satisfaction(20%)

### Score Levels

| Score | Level | Action |
|-------|-------|--------|
| ≥90 | Excellent | Document best practices |
| 80-89 | Good | Continue current approach |
| 70-79 | Adequate | Identify areas for improvement |
| <70 | Needs Work | Trigger deep reflection |

---

## Usage

### Python Version (Recommended)

```bash
# Evaluate task
python scripts/evaluate_task.py \
    --agent-id "my-agent" \
    --task-id "task-001" \
    --task-type "content-creation" \
    --completion 90 \
    --efficiency 85 \
    --quality 80 \
    --satisfaction 85

# Record lesson
python scripts/learn_lesson.py \
    --agent-id "my-agent" \
    --lesson "Validate link effectiveness" \
    --impact high \
    --category quality

# Optimization analysis
python scripts/optimize_agent.py --agent-id "my-agent"

# Cross-Agent sync
python scripts/sync_learning.py
```

### Parameter Reference

**evaluate_task.py**
| Parameter | Description | Required |
|-----------|-------------|----------|
| --agent-id | Agent identifier | Yes |
| --task-id | Task identifier | Yes |
| --task-type | Task type | Yes |
| --completion | Completion (0-100) | Yes |
| --efficiency | Efficiency (0-100) | Yes |
| --quality | Quality (0-100) | Yes |
| --satisfaction | Satisfaction (0-100) | Yes |

**learn_lesson.py**
| Parameter | Description | Required | Options |
|-----------|-------------|----------|---------|
| --agent-id | Agent identifier | Yes | |
| --lesson | Lesson description | Yes | |
| --impact | Impact level | Yes | high/medium/low |
| --category | Category | Yes | quality/efficiency/tools/knowledge |

---

## Data Storage Location

```
{workspace}/
├── self-improvement/
│   ├── evaluations.json        # Evaluation records
│   ├── lessons-learned.json   # Lesson library
│   └── optimization-plan.json # Optimization plan
└── shared-context/
    └── self-improvement/
        └── collective-wisdom.json  # Shared knowledge base
```

---

## Best Practices

### When to Evaluate
- After completing important tasks
- After completing complex tasks
- After task failure or rework
- Optional for simple repetitive tasks

### How to Record Lessons
- Record specific failure scenarios
- Record key success factors
- Record tool usage注意事项

### How to Apply Learning
- Regularly review the lesson library
- Proactively apply validated best practices
- Share with other Agents

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Cannot find workspace | Check path configuration in config.py |
| Lessons not syncing | Manually run sync_learning.py |
| Optimization plan generation fails | Ensure sufficient historical evaluation data |

---

*Let every Agent become a lifelong learner!*

*Version: 1.1.0 (Python Edition)*
*Tags: agent, self-improvement, learning, optimization*
