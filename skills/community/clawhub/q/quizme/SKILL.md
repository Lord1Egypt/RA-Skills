---
name: quizme
description: >-
  Adaptive tech quiz skill for OpenClaw. Asks one question at a time on any coding or CS topic:
  Python, JavaScript, SQL, system design, algorithms, networking, Git, Docker, APIs, and more.
  Includes code snippets where relevant. Difficulty adapts dynamically — harder after correct
  answers, easier after wrong ones. Uses a rolling question bank generated in batches (via
  GPT-4o-mini) so sessions are fast and token-efficient. Automatically graduates you to the next
  difficulty level when you hit 80% accuracy. Tracks your topics and progress across sessions.
  Trigger: /quizme, "quiz me on X", "teach me X", "test my knowledge of X", "I want to learn X", "start a quiz".
---

# QuizMe

## Overview

An adaptive, Socratic quiz skill for tech and coding topics. Asks one question at a time, confirms right/wrong after each answer with a brief explanation, and adjusts difficulty dynamically — harder after a correct answer, easier (or same) after a wrong one. Saves topics to `~/quizme/topics.json` for persistence across sessions.

## Supported Topic Areas

| Area | Subtopics |
|---|---|
| Python | basics, OOP, async/await, exceptions, decorators |
| JavaScript | closures, promises, async/await, event loop |
| SQL | joins, indexes, window functions, query optimization |
| System design | caching, load balancing, databases, CAP theorem |
| Algorithms & data structures | big-O, trees, graphs, sorting |
| Networking | HTTP, TCP/IP, DNS, websockets |
| Git | branching, rebasing, conflicts, workflows |
| Docker / Kubernetes | containers, images, pods, services |
| APIs | REST, GraphQL, auth patterns (OAuth, JWT) |
| General CS concepts | memory, OS basics, compilers, concurrency |

See `references/topics.md` for detailed per-topic concept lists and example questions at each difficulty level.

## Workflow

### Step 1 — Start every session by asking the topic

Always ask the user what they want to practice, even if a topic was passed inline. Show the saved list from `~/quizme/topics.json` if it exists:

> "What would you like to practice today?"
> [if topics exist] "Your saved topics: 1. Python async  2. SQL joins  (or type a new topic)"

After topic confirmed, ask difficulty OR load current difficulty from `~/quizme/progress.json` if the user has history with this topic:
> "Your last difficulty for Python was intermediate — continue there? (yes / pick another)"

If no prior history, default to **beginner** or ask: "What difficulty? (beginner / intermediate / advanced)"

### Step 2 — Initialize the bank if needed

Check `~/quizme/bank/{topic_slug}-{difficulty}.json` where `topic_slug` is the topic lowercased with spaces/special chars replaced by hyphens:

- If the file is **missing** or has **fewer than 3 unseen questions** (`"seen": false`): generate questions inline (no external API needed — you are the LLM).
  - First run (file missing): generate 20 questions
  - Refill (file exists but low on unseen): generate 10 more and append
- Tell the user: *"Generating questions for [topic] at [difficulty]..."* then generate and write the JSON file immediately.
- After generating, add the topic to `~/quizme/topics.json` if not already present.

**How to generate inline:** Produce a valid JSON array of question objects matching the bank format below, then write it to the bank file using the `write` tool. Do not call any external script or API.

Bank file format:
```json
{
  "topic": "system design",
  "difficulty": "beginner",
  "generated_at": "YYYY-MM-DD",
  "questions": [
    {
      "id": "{topic_slug}-{diff_prefix}-{3-digit-index}",
      "concept": "short concept name",
      "question": "The question text",
      "code": null,
      "language": null,
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "answer": "A",
      "explanation": "2-3 sentence explanation of why the answer is correct.",
      "seen": false,
      "correct_count": 0,
      "seen_count": 0
    }
  ]
}
```

For code topics: set `"code"` to a code snippet string (≤15 lines) and `"language"` to the language name.
For conceptual topics (networking, system design, algorithms theory): set both to `null`.

### Step 3 — Ask questions from bank

Pick a **random unseen** question (`"seen": false`) from the bank. After showing it, immediately set `"seen": true` on that question and save the bank file.

Question format rules:
- If `"code"` field is non-null: include the snippet in a fenced code block using the `"language"` value
- If `"code"` is null: plain question text only
- Always show all 4 options (A/B/C/D) from the `"options"` field
- One question per message — never show two at once

#### Question template (code topic)
```
**Question N** — [Topic] ([difficulty])

[question text]

```[language]
[code snippet]
```

A) ...
B) ...
C) ...
D) ...
```

#### Question template (conceptual topic)
```
**Question N** — [Topic] ([difficulty])

[question text]

A) ...
B) ...
C) ...
D) ...
```

### Step 4 — After each answer

1. Reveal correct/wrong + show the `"explanation"` from the bank question (2–3 sentences).
2. Update the bank question:
   - Increment `"seen_count"` by 1
   - If correct: increment `"correct_count"` by 1
3. Save the bank file.
4. **Check graduation:** Count all questions in this bank where `"seen_count" > 0`. If there are ≥ 15 such questions AND `(sum of correct_count / sum of seen_count) >= 0.80` → trigger graduation (Step 5).
5. **Check refill:** Count remaining unseen questions (`"seen": false`). If fewer than 5 remain → silently generate 10 more inline and append them to the bank file.
6. Ask the next question.

### Step 5 — Graduation

When graduation triggers:
- Announce: *"You've mastered [difficulty] [topic]! Moving up to [next level]."*
- Delete the old bank file (`~/quizme/bank/{slug}-{difficulty}.json`)
- Update `~/quizme/progress.json`: mark current difficulty as graduated with today's date, set `current_difficulty` to the next level
- Generate 20 new questions inline for the next difficulty and write the new bank file
- Continue the session at the new difficulty

Difficulty order: **beginner → intermediate → advanced**

At **advanced**: no graduation. Just keep refilling the bank when unseen questions run low.

### Step 6 — End session

When the user says "stop", "quit", "done", or similar:
- Show summary: topic, questions answered this session, correct count, accuracy %
- Save session stats to `~/quizme/progress.json` (increment answered/correct counts for this topic+difficulty)

## Storage Layout

```
~/quizme/
├── topics.json          # { "topics": ["python async", "SQL joins"] }
├── progress.json        # per-topic difficulty + stats
└── bank/
    ├── python-beginner.json
    ├── sql-joins-intermediate.json
    └── ...              # only current difficulty per topic lives here
```

### progress.json format

```json
{
  "python": {
    "current_difficulty": "intermediate",
    "beginner": { "answered": 17, "correct": 14, "graduated": true, "graduated_at": "2026-05-22" },
    "intermediate": { "answered": 4, "correct": 3, "graduated": false }
  }
}
```

### topics.json format

```json
{ "topics": ["python async", "SQL joins", "system design"] }
```

- On first run, create the file if it doesn't exist.
- When a new topic is introduced, append it to the list and save.
- When showing saved topics, display them as a numbered list.

## Hard Rules — Never Break These

1. **Never ask two questions at once.**
2. **Never add a code snippet to a non-code topic** (networking, algorithms theory, CS concepts).
3. **Never reveal the answer before the user responds.**
4. **This skill is tech-only.** If the user asks to be quizzed on a non-tech topic (history, cooking, etc.), politely decline and list the supported topic areas.
5. **Always provide 4 multiple-choice options** (A/B/C/D) — no open-ended questions.
6. **Always explain after every answer**, even when correct.

## Difficulty Levels

| Level | Description |
|---|---|
| Beginner | Core syntax, definitions, basic usage patterns |
| Intermediate | How things work under the hood, common patterns, tricky edge cases |
| Advanced | Performance, internals, architectural tradeoffs, subtle bugs |

## Resources

### references/
- `topics.md` — Detailed per-topic concept coverage at each difficulty level, with example question ideas. Load this when generating questions to ensure appropriate concept selection.
