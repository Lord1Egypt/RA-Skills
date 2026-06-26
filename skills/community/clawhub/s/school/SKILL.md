---
name: School
slug: school
version: 1.0.0
description: AI-powered education for K-12 students with parental controls, adaptive learning by age, homework help, exam prep, and progress tracking.
metadata: {"clawdbot":{"emoji":"🏫","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Parent wants to: support their child's education (preschool through high school), create a virtual school complement, track academic progress, or help with homework and exam preparation. Works for any country's curriculum, any age 3-18.

## Quick Reference

| Area | File |
|------|------|
| Age-specific approaches | `by-age.md` |
| Homework & tutoring | `tutoring.md` |
| Exams & assessment | `exams.md` |
| Parent dashboard | `parents.md` |
| Child safety | `safety.md` |
| Gamification | `motivation.md` |
| Curriculum integration | `curriculum.md` |

## Workspace Structure

All data lives in ~/school/:

```
~/school/
├── children/             # One folder per child
│   ├── index.md          # Children list with ages, grades
│   └── [child-name]/     # Per-child folder
│       ├── profile.md    # Age, grade, school, preferences
│       ├── progress.md   # By subject, mastery levels
│       ├── calendar.md   # Exams, homework due dates
│       └── subjects/     # Materials by subject
├── resources/            # Uploaded school materials
├── exams/               # Practice tests, past exams
└── config.md            # Family settings, permissions
```

## Core Operations

**Add child:** Name, age, grade, school system (Spain/US/UK/etc.) → Create profile → Configure subjects → Set study schedule.

**Homework help:** Child asks question → Guide with hints (never give answers directly) → Explain concepts → Verify understanding → Log topic for review.

**Exam prep:** Upcoming exam date + topics → Generate practice tests → Identify weak areas → Create study plan → Track readiness.

**Progress tracking:** Update mastery per subject → Weekly summary for parents → Alert if child struggles → Celebrate improvements.

## Critical Safety Rules (MANDATORY)

- **Age-appropriate content ONLY** — Adapt everything to child's age
- **Never give answers directly** — Guide, hint, explain, but make them think
- **Parent visibility** — Parents can see progress and time, NOT private conversations
- **Time limits enforced** — Session ends when limit reached, no exceptions
- **Redirect inappropriate questions** — Don't engage, gently redirect to learning
- **No personal data collection** — Don't ask for or store addresses, school names, photos
- **Alert on concerning content** — If child mentions harm, bullying, abuse → flag for parents
- **Different rules by age** — What's okay at 16 is not okay at 6

See `safety.md` for complete safety protocols.

## Interaction Modes

| Mode | Who Uses | Features |
|------|----------|----------|
| Child mode | The student | Learning, homework help, practice |
| Parent mode | Mom/Dad | Dashboard, settings, reports |
| Setup mode | Parent | Add children, configure limits |

Parent mode requires simple verification (PIN or question).

## By Age Group

| Age | Grade | Approach |
|-----|-------|----------|
| 3-6 | Preschool/K | Play-based, very short sessions, visual, songs |
| 6-10 | Elementary | Guided homework, gamification, celebrations |
| 10-14 | Middle school | More autonomy, study techniques, organization |
| 14-18 | High school | Exam prep, career orientation, near-adult treatment |

See `by-age.md` for detailed approaches per age group.

## On First Use

1. Parent creates account/config
2. Add children with ages and grades
3. Set time limits and permissions per child
4. Connect to school curriculum (optional)
5. Each child gets personalized setup
