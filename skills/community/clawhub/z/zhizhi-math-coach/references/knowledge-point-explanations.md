# Knowledge Point Explanations

## Purpose

Create reusable knowledge-point cards that help a parent explain, a student reread, and the coach decide whether the knowledge is actually mastered.

## Card Location

Store reusable cards in:

```text
knowledge-points/<topic-slug>.md
```

## Required Sections

Each card should include:

- Applicable grade and textbook scope.
- Core concept in parent-facing language.
- Parent explanation script.
- Student short version.
- Doing tips.
- Common errors and why they happen.
- Quick verification questions.
- Mastery evidence.

## Mastery Evidence

Use evidence layers instead of correctness alone:

1. The child can explain the rule in plain language.
2. The child can solve same-structure items.
3. The child can solve variants with changed wording, scenario, or condition order.
4. The child can still solve after spaced review.

## Output Style

- Parent version: concrete, short, and directly usable while explaining.
- Student version: shorter, no diagnosis jargon.
- Avoid large copied textbook passages.
- Link explanation to the observed cause, not just the topic name.

## After Explanation

Generate a `post_explanation_check` set of 3 to 6 items. Use it to decide whether the issue is still weak, consolidating, or ready for spaced review.
