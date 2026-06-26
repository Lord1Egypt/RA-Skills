# Course Workspace Structure

Organize your course production with this folder structure.

## Directory Layout

```
~/udemy/
├── index.md                    # Portfolio overview
├── _templates/                 # Reusable templates
│   ├── script-template.md
│   ├── slide-template.pptx
│   ├── quiz-template.md
│   └── checklist-launch.md
│
├── [course-slug]/              # One folder per course
│   ├── README.md               # Course overview & status
│   ├── planning/
│   │   ├── research.md         # Niche & competitor analysis
│   │   ├── outline.md          # Full curriculum
│   │   └── objectives.md       # Learning objectives per section
│   │
│   ├── scripts/
│   │   ├── section-01/
│   │   │   ├── lecture-01.md
│   │   │   ├── lecture-02.md
│   │   │   └── quiz.md
│   │   └── section-02/
│   │       └── ...
│   │
│   ├── slides/
│   │   ├── section-01.pptx
│   │   └── section-02.pptx
│   │
│   ├── assets/
│   │   ├── images/
│   │   ├── code/
│   │   └── downloads/          # Student resources
│   │
│   ├── marketing/
│   │   ├── description.md
│   │   ├── title-options.md
│   │   └── promo-script.md
│   │
│   └── tracking/
│       ├── qa-log.md           # Student questions & responses
│       ├── reviews.md          # Notable reviews & responses
│       └── updates.md          # Change log
│
└── ideas/                      # Future course ideas
    ├── validated/
    └── research-needed/
```

## Status Tracking

In each course's `README.md`:

```markdown
# [Course Name]

**Status:** [Planning | Production | Published | Updating]
**Udemy URL:** [link when published]
**Published:** [date]
**Last Updated:** [date]

## Metrics
- Students: X
- Rating: X.X (N reviews)
- Revenue (30d): $X

## Current Tasks
- [ ] Task 1
- [ ] Task 2

## Notes
[Any important context]
```

## Portfolio Index

In `~/udemy/index.md`:

```markdown
# Udemy Course Portfolio

## Published
| Course | Status | Students | Rating | Revenue/mo |
|--------|--------|----------|--------|------------|
| [Name](./course-slug/) | Active | 1,234 | 4.7 | $XXX |

## In Production
| Course | Phase | Target Launch |
|--------|-------|---------------|
| [Name](./course-slug/) | Scripts | 2026-03-01 |

## Ideas Pipeline
| Idea | Validated? | Priority |
|------|------------|----------|
| Topic X | Yes | High |
| Topic Y | Needs research | Medium |
```

## File Naming Conventions

- Use lowercase with hyphens: `section-01-lecture-03.md`
- Number sections and lectures for sorting: `01-intro.md`, `02-setup.md`
- Version drafts if needed: `script-v1.md`, `script-v2.md`
- Final files: no version suffix

## Workflow Tips

1. **Start in planning/** — Don't produce until research is complete
2. **Scripts before slides** — Write what you'll say, then visualize it
3. **Batch similar tasks** — Write all scripts, then all slides, then record
4. **Track everything** — Future-you will thank present-you
5. **Archive, don't delete** — Move old versions to `_archive/`
