---
name: study-plan-maker
description: >
  Use this skill when creating personalized study plans, learning roadmaps,
  or skill acquisition schedules. Activates on requests like "make a study
  plan for X", "how do I learn Y in Z weeks", "create a learning roadmap for
  [skill/exam/topic]", or "help me prepare for [certification/exam]".
---

# Study Plan Maker

A structured framework for creating personalized, realistic, and effective
study plans optimized for knowledge retention and goal achievement.

## When to Use
- Preparing for exams (certifications, college entrance, professional exams)
- Learning a new skill from scratch (coding, language, instrument, etc.)
- Building a structured reading/learning curriculum
- Returning to a subject after a long break
- Cramming efficiently for an upcoming deadline

## Core Framework: SOLAR Method

```
S — Scope: Define exactly what needs to be learned
O — Objective: Set measurable outcomes and deadlines  
L — Layout: Map the content into phases and milestones
A — Allocate: Assign time blocks to each topic
R — Review: Build in spaced repetition and checkpoints
```

## Step-by-Step Workflow

### Step 1 — Intake Assessment
Ask the user:
- **Goal**: What are you trying to learn or achieve?
- **Deadline**: When do you need to be ready? (or is this open-ended?)
- **Current level**: Complete beginner / some experience / intermediate / advanced
- **Daily time available**: How many hours/minutes per day can you study?
- **Learning style**: Visual / reading-writing / hands-on / auditory
- **Resources available**: Books, courses, tutors, online platforms?
- **Constraints**: Exam format? Required syllabus? Company training?

### Step 2 — Scope the Curriculum

Break the subject into major domains:
```
Subject: [Name]
Total estimated hours: X–Y hours to proficiency

Domain 1: [Name] — ~X hours (X% of total)
  - Topic 1.1: ...
  - Topic 1.2: ...
  - Topic 1.3: ...

Domain 2: [Name] — ~X hours
  ...
```

Reference official syllabi, popular courses, or established learning paths
when available (e.g., for certifications, programming languages, languages).

### Step 3 — Set SMART Milestones

```
SMART = Specific, Measurable, Achievable, Relevant, Time-bound

❌ Vague: "Understand JavaScript well"
✅ SMART: "Complete Modules 1–5, pass practice quiz with 80%+ by Day 21"

Milestone 1 (Week X): [Specific achievement]
Milestone 2 (Week X): [Specific achievement]
Final Goal (Day X): [Pass exam / Complete project / Reach level X]
```

### Step 4 — Design the Weekly Schedule

**Phase structure** (for most learning goals):
```
Phase 1 (Weeks 1–X): Foundation
  — Core concepts, vocabulary, fundamentals
  — Priority: breadth over depth
  
Phase 2 (Weeks X–X): Building
  — Applied knowledge, practice problems
  — Priority: depth + skill-building

Phase 3 (Weeks X–X): Consolidation
  — Review, practice tests, weak area drilling
  — Priority: retention + exam readiness
```

**Weekly time template**:
```
Monday: [Topic A] — X min
Tuesday: [Topic B] — X min  
Wednesday: Review + practice — X min
Thursday: [Topic C] — X min
Friday: [Topic D] — X min
Saturday: Mock test / project work — X min
Sunday: Light review / rest
```

### Step 5 — Apply Learning Science Principles

| Principle | How to Apply |
|-----------|-------------|
| **Spaced repetition** | Review material at increasing intervals (Day 1, Day 3, Day 7, Day 14) |
| **Active recall** | Test yourself before re-reading (flashcards, practice questions) |
| **Interleaving** | Mix topics in each session rather than blocking one topic per day |
| **The Pomodoro method** | 25 min focused study + 5 min break, every 4 cycles take 30 min break |
| **Feynman technique** | Explain the concept in simple words to check understanding |
| **Deliberate practice** | Focus on weakest areas, not comfortable topics |

### Step 6 — Build in Checkpoints

```
Weekly check-in questions:
□ Did I complete this week's planned sessions?
□ Which topics felt unclear or need more time?
□ What was my practice test score this week?
□ Do I need to adjust next week's plan?

Adjustment rules:
- If >20% behind: cut 1 topic, add weekend catch-up
- If consistently ahead: add depth or advance timeline
- If exam is 2 weeks away: switch to 100% review + practice tests
```

## Output Format

Deliver a complete study plan with:

```
## 📚 Study Plan: [Subject/Goal]
**Goal**: | **Deadline**: | **Daily Time**: | **Level**:

### Curriculum Overview
[Domain map with estimated hours]

### Phase Breakdown
[3-phase structure with weeks]

### Week-by-Week Schedule
[Detailed weekly tables]

### Milestone Checklist
[SMART milestones]

### Recommended Resources
- Primary: [Book/Course name + URL if known]
- Practice: [Platform or resource]
- Reference: [Quick reference card or docs]

### Review Schedule (Spaced Repetition)
[What to review and when]
```

## Study Pace Guidelines

| Hours/Day | Goal type | Realistic timeline |
|-----------|-----------|-------------------|
| 0.5h/day | Light skill building | Long-term, months |
| 1h/day | Language / instrument | 6–12 months to conversational |
| 2h/day | Professional certification | 2–4 months |
| 3–4h/day | Intensive exam prep | 4–8 weeks |
| 6+h/day | Full-time bootcamp mode | 2–6 weeks for focused topic |

## Quality Standards
- Always validate the plan is achievable given user's time budget
- Flag if the goal is unrealistic for the timeline (offer alternatives)
- Prioritize high-yield topics (80/20 rule — 20% of topics cover 80% of exams)
- Include at least one practice/application activity per phase
