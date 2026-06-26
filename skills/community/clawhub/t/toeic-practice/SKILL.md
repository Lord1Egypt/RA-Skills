---
name: toeic-practice
description: Daily TOEIC practice coach for a user scoring 600+. Delivers one focused session daily for Parts 5, 6, and 7, explains answers with grammar and vocabulary notes, and targets improvement toward 700+. Use when Hana should deliver TOEIC homework, drill Parts 5 to 7, or explain why an answer is correct.
---

# TOEIC Practice Coach

User level: 600+ (intermediate). Target: 700+.

## User profile

- Handles basic vocabulary and common business English well.
- Main focus areas: Part 6 (text completion) and Part 7 (reading comprehension, double/triple passages).
- Grammar gaps: relative clauses, conditionals, passive voice, preposition collocations.
- Vocabulary: knows common words but misses less frequent business/formal vocabulary.

## Daily homework format

Rotate across TOEIC Parts 5, 6, and 7 only: Part 5 → Part 6 → Part 7 → repeat.

### Part 5 — Incomplete Sentences (Grammar & Vocabulary)

- Present 5 sentence completion questions.
- Cover grammar (tense, voice, relative clauses, conditionals, prepositions) or vocabulary (collocations, word form).
- Do NOT give answers upfront.
- After user answers: explain the grammar rule or vocabulary logic for each question.
- Give 1–2 similar sentences to reinforce the pattern.

### Part 6 — Text Completion

- Write ONE original short text (email, notice, or memo, 80–120 words) with 4 blanks and 4-option choices.
- Ask user to choose the best option for each blank.
- After user answers: explain context-based reasoning for each answer.
- Point out discourse markers and cohesion signals.

### Part 7 — Reading Comprehension

- Write ONE original single passage (email, advertisement, article, 150–200 words) with 3–4 questions.
- Question types: detail, inference, vocabulary in context, NOT TRUE.
- Do NOT give answers upfront.
- After user answers: explain where in the text the answer is located and why distractors are wrong.

## State tracking

Rotation order: Part 5 → Part 6 → Part 7 → (repeat)

Before each session:

1. Read `memory/toeic-state.md`. Look for the line: `last_part: <value>`
2. Pick the NEXT part in the rotation order above.
3. If the file does not exist, is empty, or contains a part outside this rotation, start with Part 5.

After delivering the homework (before waiting for user response):

- Overwrite `memory/toeic-state.md` with exactly one line: `last_part: <current part>`
- Example: `last_part: Part 6`

## Coaching rules

- Always explain WHY an option is correct AND why the others are wrong.
- For grammar questions: state the rule name clearly (e.g., "subject-verb agreement", "gerund vs. infinitive").
- For vocabulary questions: give the word's meaning + 1 example sentence.
- After each session, identify 1 pattern the user is consistently missing.
- Keep all practice content in English.

## Scheduled Delivery Contract

For the cron-triggered daily homework:

- Use the built-in Part 5 to Part 7 rotation and state tracking in this skill.
- Generate all practice content yourself.
- Wait for the user's response before giving answers or feedback.
- No markdown tables.
- Do not generate Part 1, 2, 3, or 4 content.

Use this delivery wrapper:

```
PART
[Today's part number and name]
HOMEWORK
[Original practice content in English]
```
