---
name: Smart Teacher
description: "Expert education planning tool. Generate lesson plans, curriculum maps, study schedules, assessments, and learning objectives aligned to Bloom's taxonomy."
permissions: Bash
triggers:
  - lesson plan
  - curriculum planning
  - education planning
  - study schedule
  - assessment
  - learning objectives
  - smart teacher
---

# Smart Teacher

Expert education planning assistant. Generate structured lesson plans, curriculum maps, study schedules, rubrics, and assessments — all from a zero-dependency Python CLI.

## Quick Start

```bash
# Generate a lesson plan
python3 scripts/edu_planner.py lesson "Photosynthesis" --grade 8 --duration 45

# Create a curriculum map
python3 scripts/edu_planner.py curriculum "Biology" --grade 9 --weeks 12

# Build a study schedule
python3 scripts/edu_planner.py schedule --subjects "Math,Science,English" --hours 3 --days 5

# Generate learning objectives using Bloom's taxonomy
python3 scripts/edu_planner.py objectives "Fraction Operations" --grade 5 --levels "remember,understand,apply,analyze"

# Create a rubric
python3 scripts/edu_planner.py rubric "Persuasive Essay" --criteria 4 --levels 4

# Generate an assessment
python3 scripts/edu_planner.py assess "Cell Biology" --grade 10 --type quiz --questions 10
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `lesson <topic>` | Generate a structured lesson plan |
| `curriculum <subject>` | Create a multi-week curriculum map |
| `schedule` | Build a weekly study schedule |
| `objectives <topic>` | Generate learning objectives (Bloom's taxonomy) |
| `rubric <assignment>` | Create an assessment rubric |
| `assess <topic>` | Generate a quiz or test |

## Options

### Lesson Plan
- `--grade N` — Target grade level (K-12)
- `--duration N` — Duration in minutes
- `--standard <std>` — Align to standards (e.g., "CCSS", "NGSS", "Alberta")

### Curriculum Map
- `--grade N` — Grade level
- `--weeks N` — Number of weeks
- `--standard <std>` — Standards alignment

### Study Schedule
- `--subjects "A,B,C"` — Comma-separated subjects
- `--hours N` — Hours per day
- `--days N` — Days per week
- `--exam-date YYYY-MM-DD` — Target exam date for priority weighting

### Learning Objectives
- `--grade N` — Grade level
- `--levels "list"` — Bloom's levels: remember, understand, apply, analyze, evaluate, create

### Rubric
- `--criteria N` — Number of criteria (default: 4)
- `--levels N` — Performance levels (default: 4)

### Assessment
- `--type quiz|test|exam` — Assessment type
- `--questions N` — Number of questions
- `--grade N` — Grade level

## Bloom's Taxonomy

All objectives and assessments are aligned to Bloom's revised taxonomy:
1. **Remember** — Recall facts and basic concepts
2. **Understand** — Explain ideas or concepts
3. **Apply** — Use information in new situations
4. **Analyze** — Draw connections among ideas
5. **Evaluate** — Justify a stand or decision
6. **Create** — Produce new or original work
