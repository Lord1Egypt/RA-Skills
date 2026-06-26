---
name: Study
slug: study
version: 1.0.1
description: Structure study sessions, manage materials, and prepare for exams with active recall techniques.
changelog: Simplified structure, removed broken script references, explicit data storage
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Data Storage

```
~/study/
├── subjects/           # One folder per subject
│   └── {subject}/
│       ├── materials/     # PDFs, notes, resources
│       ├── flashcards.json
│       ├── schedule.md
│       └── progress.md
├── calendar/           # Exam dates, deadlines
│   └── deadlines.json
└── config.json         # Preferences
```

Create on first use: `mkdir -p ~/study/{subjects,calendar}`

## Scope

This skill:
- ✅ Creates study plans in ~/study/
- ✅ Manages materials and flashcards
- ✅ Tracks deadlines and exam dates
- ✅ Guides study sessions with active recall
- ❌ NEVER generates content student should create themselves
- ❌ NEVER stores data outside ~/study/

## Quick Reference

| Topic | File |
|-------|------|
| Study techniques | `techniques.md` |
| Subject strategies | `subjects.md` |
| Exam preparation | `exams.md` |

## Core Rules

### 1. Workflow
```
Plan Semester → Weekly Schedule → Daily Sessions → Review → Exam Prep
```

### 2. AI Scaffolds, Student Creates
- AI asks questions → student writes summaries
- AI structures sessions → student takes notes
- AI generates quiz → student answers
- NEVER generate the student's work

### 3. Adding a Subject
1. Create ~/study/subjects/{subject}/
2. Set exam date in deadlines.json
3. Estimate weekly hours needed
4. Generate initial schedule

### 4. Study Session Flow
1. **Start**: What topic? How long?
2. **Active recall**: Questions first, answers second
3. **Practice**: Problems, not just reading
4. **Summary**: Student writes key points
5. **Schedule**: Next session based on spaced repetition

### 5. Exam Preparation
When exam approaches (≤2 weeks):
1. Review all flashcards with SR
2. Practice past exams if available
3. Identify weak areas from progress.md
4. Create focused review plan

### 6. Configuration
In ~/study/config.json:
```json
{
  "level": "undergraduate",
  "technique": "pomodoro",
  "session_minutes": 25,
  "break_minutes": 5
}
```

### 7. Progress Tracking
In {subject}/progress.md:
```
## Topics
- [x] Chapter 1: Intro (mastered)
- [~] Chapter 2: Basics (in progress)
- [ ] Chapter 3: Advanced (not started)

## Weak Areas
- Integration techniques
- Proof by induction
```
