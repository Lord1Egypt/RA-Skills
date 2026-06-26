# Study Tutor Skill

**Study Tutor** is a compact, science-based tutoring skill for helping students and self-learners study systematically. It supports diagnosis, guided teaching, practice, review, spaced repetition, mistake analysis, and learning-profile tracking.

## What Changed in This Version

This version compresses the original long skill into a smaller execution-oriented `SKILL.md`. Long examples and repeated templates were removed or merged to reduce token usage. The skill name is standardized as **Study Tutor**.

## Core Features

- Pre-learning diagnosis: goal, baseline, materials, deadline, available time.
- Teacher preparation: read user materials before teaching when available.
- Four learning modes: Guided, Batch, Question-driven, Hybrid.
- Teaching loop: explain → check → feedback → practice → record → review.
- Active recall and spaced repetition.
- Mistake analysis and weak-point repair.
- Learning profile stored separately to support cross-session continuity.

## Trigger Examples

Use this skill when the user says things like:

- “I want to learn Data Structures.”
- “I don’t understand this concept.”
- “Help me solve this homework problem.”
- “I have an exam soon; help me review.”
- “Help me organize my mistakes.”
- “Make me a study plan.”

## File Structure

```text
Study Tutor/
├── SKILL.md       # Main skill definition, English only
├── README.md      # English documentation
└── README-CN.md   # Chinese documentation
```

`SKILL-CN.md` is intentionally removed in this compact version because the skill itself is required to be English only.

## Recommended Workflow

1. Diagnose the learner’s goal, baseline, materials, and time.
2. Prepare from user-provided textbooks, notes, slides, or problems.
3. Choose a learning mode.
4. Teach one unit with intuition, details, example, common mistakes, and a check question.
5. Give feedback based on the user’s answer.
6. Record progress, mistakes, weak points, and next review.
7. Use active recall and spaced repetition to consolidate learning.

## Learning Modes

| Mode | Best For | Style |
|---|---|---|
| Guided | Beginners, weak foundation, high-score goals | One concept at a time with checks. |
| Batch | Review, limited time, existing baseline | Several related points, then a combined test. |
| Question-driven | Specific confusion or homework | Solve the question and expose the underlying concept. |
| Hybrid | Most learning sessions | Flexible mix of the other three modes. |

## Learning Profile

For long-term study, create a separate file:

```text
memory/{subject}-study.md
```

It should track:

- basic goal and baseline;
- progress by topic;
- weak points;
- mistake records;
- next review and practice plan.

## Scientific Basis

The skill is inspired by:

- Active Recall
- Spaced Repetition
- Testing Effect
- Elaboration
- Feynman Technique
- Cornell Note-taking

## Design Principle

`SKILL.md` should stay short. Put only behavior rules, compact templates, and required workflows there. Keep long examples, explanations, and promotional content in README files or external docs.

## License

Proprietary

## Version

- Version: 1.0.2 compact-security
- Updated: 2026-05-03
- Author: Jiang Kaiqi