# Pattern 4: Inversion

## Core Purpose

**Interview first, then execute**, preventing Agent from guessing when requirements are unclear, forcing complete context collection.

## Use Cases

- Project planning with vague requirements
- Complex system design
- Personalized tasks (need user preferences)
- Multi-constraint tasks

## Directory Structure

```
skills/project-planner/
├── SKILL.md
└── assets/
    └── plan-template.md      # Final output template (optional)
```

## SKILL.md Template

```markdown
---
name: project-planner
description: Gather requirements through structured questioning, then generate project plan. Activates when users say "I want to build", "help me plan", "design a system", "start new project".
metadata:
  pattern: inversion
  interaction: multi-turn
  trigger-phrases: [I want to, help me plan, design a, build a, plan a, design a system]
---

You are conducting a structured requirements interview. **Strictly follow these rules**:

## ⛔ Prohibitions
- **Prohibit** starting design or writing code before interview completes
- **Prohibit** asking all questions at once (ask 1 at a time)
- **Prohibit** skipping any questions

## ✅ Requirements
- Ask only 1 question at a time, wait for user answer before next
- If user answer is vague, ask follow-up for clarification
- After interview completes, summarize requirements for user confirmation

---

## Phase 1 — Problem Discovery (ask one by one, wait for each answer)

Ask following questions in order, **do not skip any**:

**Q1**: "What problem does this project solve for users?"
→ Wait for user answer

**Q2**: "Who are the primary users? What is their technical level?"
→ Wait for user answer

**Q3**: "Expected scale? (daily active users, data volume, request frequency)"
→ Wait for user answer

---

## Phase 2 — Technical Constraints (starts only after all Phase 1 answered)

**Q4**: "What deployment environment? (local/cloud/edge)"
→ Wait for user answer

**Q5**: "Any technology stack preferences? (language/framework/database)"
→ Wait for user answer

**Q6**: "Non-negotiable requirements? (latency/availability/compliance/budget)"
→ Wait for user answer

---

## Phase 3 — Requirements Confirmation (after all questions answered)

1. Summarize all collected requirements
2. Ask user: "Is above requirements summary accurate? Any omissions or adjustments needed?"
3. Iterate based on user feedback until user confirms

---

## Phase 4 — Generate Plan (after user confirms requirements)

1. Load `assets/plan-template.md` to get output format
2. Fill each section with collected requirements
3. Present complete plan
4. Ask: "Does this plan meet your expectations? What needs adjustment?"
5. Iterate based on feedback until user confirms
```

## assets/plan-template.md Template

```markdown
# {{project_name}} - Project Plan

## 1. Project Overview
- **Problem Statement**: {{Q1 answer}}
- **Target Users**: {{Q2 answer}}
- **Expected Scale**: {{Q3 answer}}

## 2. Technical Architecture
- **Deployment Environment**: {{Q4 answer}}
- **Technology Stack**: {{Q5 answer}}
- **Architecture Diagram**: {{generate architecture diagram description}}

## 3. Core Features
- {{feature list}}

## 4. Constraints & Requirements
- **Performance Requirements**: {{Q6 answer}}
- **Compliance Requirements**: {{Q6 answer}}
- **Budget Constraints**: {{Q6 answer}}

## 5. Milestone Plan
| Phase | Deliverables | Estimated Time |
|-----|--------|---------|
| Phase 1 | ... | ... |
| Phase 2 | ... | ... |

## 6. Risks & Mitigation
- **Technical Risks**: ...
- **Resource Risks**: ...

## 7. Next Actions
1. ...
2. ...

---
*Generated: {{date}}*
```

## Variant: Simplified Inversion

For lightweight tasks:

```markdown
## Quick Interview (3 questions)

Before starting, I need to understand:

1. "What is your primary goal?"
2. "Any technical constraints or preferences?"
3. "How do you define success? (acceptance criteria)"

Please answer in order, then I'll provide a solution.
```

## Variant: Branching Interview

Dynamically adjust questions based on user answers:

```markdown
## Phase 1 — Problem Discovery

**Q1**: "What is the main problem with this project?"

→ If user answers "performance issues", enter performance optimization branch
→ If user answers "missing features", enter feature design branch
→ If user answers "too expensive", enter cost optimization branch
```

## Dialogue State Tracking

For complex interviews, recommend tracking state:

```markdown
## Current State
- Phase: 2/3
- Questions answered: Q1, Q2, Q3, Q4
- Questions pending: Q5, Q6
- Requirements confirmed: No
```

## Pros & Cons

| Pros | Cons |
|-----|------|
| Avoids understanding偏差 | Many dialogue turns, time-consuming |
| Strong user involvement | Users may get impatient |
| Output better matches expectations | Question design needs experience |

## Combination with Generator

```markdown
## Inversion → Generator Flow

Phase 1-3: Inversion gathers requirements
  ↓
Phase 4: Generator fills template
  ↓
Phase 5: User confirms → If not satisfied, return to Phase 1 to re-gather
```

## Example Dialogue

```
User: I want to build a blog system

Agent: Great! Let me ask a few questions to understand your needs.

**Q1**: What problem does this blog system primarily solve for users?
      Is it a personal blog, enterprise content platform, or other type?

User: Enterprise content platform for publishing technical articles and case studies

Agent: Understood!

**Q2**: Who are the primary users? What is their technical level?
      Are they internal employees, customers, or public readers?

User: Mainly potential customers, medium technical level

Agent: Got it!

**Q3**: Expected scale? Like daily visitors, number of articles?

User: Expected 1000 DAU, initially about 50 articles

Agent: ...(continues with Phase 2 technical constraint questions)
```

---

## Checklist

- [ ] Clearly prohibit premature execution ("DO NOT start until...")
- [ ] Questions organized in phases
- [ ] Ask only 1 question at a time
- [ ] Has requirements confirmation step
- [ ] Has final output template (optional)
- [ ] Supports iterative feedback
