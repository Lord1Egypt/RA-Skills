---
name: study-planner
description: Create personalized study plans with time allocation, phased learning schedules, and review strategies. Use when users need help planning their learning journey for any subject or skill — exam preparation, self-study, career development, language learning, certification prep, or any structured learning goal. Triggers on phrases like "学习计划", "study plan", "怎么学", "备考规划", "学习规划", "复习安排", "learning schedule", "how to learn X", "prepare for exam".
---

# Study Planner — 学习规划智能体

Create structured, phased study plans tailored to the learner's goals, time, and subject difficulty.

## Workflow

### 1. Gather Context

Ask the learner (if not provided):

- **目标科目** — What to learn (e.g. Python, 英语六级, AWS认证)
- **当前水平** — Beginner / intermediate / advanced
- **可用时间** — Daily hours, deadline date
- **优先级** — Which subjects matter most (if multiple)
- **学习偏好** — Morning/night, reading/video/practice-heavy

Keep questions brief — 2-3 at a time, not an interrogation.

### 2. Generate Schedule

Run the schedule generator to produce a time allocation plan:

```bash
python3 scripts/generate_schedule.py '{"subjects":[{"name":"<科目>","priority":<1-5>,"difficulty":<1-5>}],"daily_hours":<小时数>,"deadline":"<YYYY-MM-DD>","start_date":"<YYYY-MM-DD>"}'
```

- **priority**: 1 (optional) → 5 (must-pass)
- **difficulty**: 1 (easy) → 5 (very hard)

Interpret the output and present it in a readable format — not raw JSON.

### 3. Design the Learning Path

Based on schedule output, create a phased plan for each subject:

**Phase 1 — 基础入门 (30%)**: Build conceptual framework
- Recommended: textbooks/videos + structured notes
- Output: concept map or summary notes

**Phase 2 — 深入理解 (40%)**: Master core principles
- Recommended: exercises, problem sets, mini-projects
- Output: completed exercises, working code/projects

**Phase 3 — 综合应用 (20%)**: Integrate and apply
- Recommended: cross-topic projects, teaching others, real-world tasks
- Output: portfolio project or teaching notes

**Phase 4 — 查漏补缺 (10%)**: Fill gaps, reinforce
- Recommended: mock tests, error analysis, weak-spot review
- Output: test results, improvement log

### 4. Add Review Strategy

Apply spaced repetition intervals: **1天 → 3天 → 7天 → 14天 → 30天**

For each major topic, mark review dates in the plan. See [learning-methods.md](references/learning-methods.md) for full strategy details.

### 5. Present the Plan

Format the final plan using templates from [templates.md](references/templates.md):
- Weekly overview
- Daily schedule with time blocks
- Review calendar
- Monthly复盘 checkpoints

**Presentation rules:**
- Use the learner's language (Chinese/English/etc.)
- Keep it actionable — specific tasks, not vague advice
- Include rest days — burnout prevention is part of good planning
- Add a "应急调整" section for when life interrupts

### 6. Follow-up

Offer to:
- Break any phase into weekly micro-plans
- Generate specific resource recommendations
- Create review flashcards
- Track progress with a simple log template

## Key Principles

- **Active > Passive**: Always recommend practice over reading
- **Small wins**: Break goals into daily achievable chunks
- **Energy matching**: Hard tasks in peak hours, review in low hours
- **Flexibility**: Plans must bend — include buffer days (10-15% of total)
- **Measure progress**: Define what "done" looks like for each phase

## Common Adjustments

| Situation | Adjustment |
|-----------|-----------|
| Working professional | Reduce daily hours, extend deadline, focus weekends |
| Exam deadline tight | Increase Phase 4 weight to 20%, compress Phase 1 |
| Multiple subjects | Weight by priority × difficulty, stagger start dates |
| Already intermediate | Skip or compress Phase 1, start at Phase 2 |
| Burnout risk | Mandatory rest days every 5-6 days, lighter review days |

## Resources

- **scripts/generate_schedule.py** — Auto-generate time allocation by subject weight
- **references/learning-methods.md** — Spaced repetition, Feynman technique, pomodoro, common traps
- **references/templates.md** — Weekly, daily, and monthly plan templates