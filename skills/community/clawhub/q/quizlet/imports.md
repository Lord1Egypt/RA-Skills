# Quizlet Import and Cleanup Workflows

## Pre-Import Checklist

- Remove duplicate lines and blank rows.
- Ensure each line maps to one prompt-answer pair.
- Keep source terminology consistent across the file.
- Tag entries by topic before first study session.

## Recommended Import Format

Use one card per line with a tab separator:

```text
Prompt<TAB>Answer
```

Example:

```text
What phase follows G1 in the cell cycle?	S phase
What does EBITDA exclude?	Interest, taxes, depreciation, and amortization
```

## Cleanup Pass After Import

1. Scan for duplicated prompts with different answers.
2. Normalize capitalization for key terms.
3. Add topic tags for grouped review.
4. Delete filler cards that do not map to exam outcomes.

## Bulk Rewrite Strategy

When imported cards are low quality:

- Keep only cards directly linked to learning outcomes.
- Rewrite top-priority cards first using atomic prompts.
- Split large imports into multiple focused sets.
- Run a short Learn session to validate readability and ambiguity.

## Import Traps

- Copying dense lecture bullets directly -> prompts become unreadable.
- Mixing languages in one set without markers -> recall confusion.
- Importing long answers as paragraphs -> weak active recall.
- Leaving answer synonyms undefined -> inconsistent scoring.
