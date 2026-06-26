---
name: study-buddy
description: Interactive study assistant that creates flashcards, quizzes, and spaced repetition reviews from any source material (notes, PDFs, photos, text, URLs). Use when the user wants to study, memorize, review, prepare for exams, create flashcards, take a quiz, practice questions, or learn any topic. Triggers on phrases like "study", "quiz me", "flashcards", "review", "exam prep", "test me", "help me memorize", "spaced repetition", "study session".
metadata:
  { "openclaw": { "emoji": "📚", "requires": { "bins": ["python3"] } } }
---

# Study Buddy

AI-powered study assistant that turns any material into interactive learning sessions with flashcards, quizzes, and spaced repetition — delivered through chat.

## Core Workflow

### 1. Create Flashcards from Material

When the user provides study material (text, image, PDF, URL):

1. Extract and analyze the content
2. Identify key concepts, definitions, formulas, dates, and relationships
3. Generate flashcards as Q&A pairs
4. Store them using `scripts/deck_manager.py`

```bash
# Create a new deck
python3 scripts/deck_manager.py create "Biology Exam" --cards '[
  {"q": "What is mitosis?", "a": "Cell division producing two identical daughter cells"},
  {"q": "What are the phases of mitosis?", "a": "Prophase, Metaphase, Anaphase, Telophase (PMAT)"}
]'

# Add cards to existing deck
python3 scripts/deck_manager.py add "Biology Exam" --cards '[
  {"q": "What is meiosis?", "a": "Cell division producing four genetically different gametes"}
]'
```

**Card generation guidelines:**
- One concept per card
- Questions should test understanding, not just recall
- Include mnemonics when helpful (e.g., PMAT for mitosis phases)
- For math/science: include both formula cards and application cards
- For languages: include context sentences, not just word translations
- Aim for 10-20 cards per topic section

### 2. Quiz Session

When the user asks to be quizzed:

```bash
# Get cards due for review (spaced repetition)
python3 scripts/deck_manager.py review "Biology Exam"

# Get random quiz (all cards)
python3 scripts/deck_manager.py quiz "Biology Exam" --count 10
```

**Quiz delivery format:**

Present one question at a time:

> **Question 3/10**
> What are the phases of mitosis?

Wait for the user's answer, then reveal:

> **Answer:** Prophase, Metaphase, Anaphase, Telophase (PMAT)
>
> How did you do?
> Got it | Partially | Missed it

Record the result:

```bash
python3 scripts/deck_manager.py record "Biology Exam" --card-id 2 --result "correct"
```

Results affect spaced repetition scheduling:
- correct: review interval increases (1d, 3d, 7d, 14d, 30d)
- partial: interval stays the same
- missed: interval resets to 1 day

### 3. Spaced Repetition Review

When the user starts a study session or asks "what should I review?":

```bash
# Check what's due across all decks
python3 scripts/deck_manager.py due

# Review specific deck
python3 scripts/deck_manager.py review "Biology Exam"
```

Only show cards that are due based on the SM-2 algorithm intervals. After each session, show a summary:

> **Session complete!**
> Reviewed: 12 cards
> Correct: 9 | Partial: 2 | Missed: 1
> Next review: 3 cards due tomorrow

### 4. Generate Practice Exam

When the user asks for an exam or test:

```bash
python3 scripts/deck_manager.py exam "Biology Exam" --questions 20 --types "multiple_choice,short_answer,true_false"
```

Generate a mix of question types from the deck:
- **Multiple choice** (4 options, one correct) -- use other cards' answers as distractors
- **True/False** -- modify real answers slightly for false statements
- **Short answer** -- direct questions from flashcards
- **Fill in the blank** -- remove key terms from answers

### 5. Deck Management

```bash
# List all decks
python3 scripts/deck_manager.py list

# Show deck stats
python3 scripts/deck_manager.py stats "Biology Exam"

# Export deck (share with others)
python3 scripts/deck_manager.py export "Biology Exam"

# Import deck
python3 scripts/deck_manager.py import deck_file.json

# Delete deck
python3 scripts/deck_manager.py delete "Biology Exam"
```

For guidance on handling different input types (text, photos, PDFs, URLs) and tips for creating effective cards, see [references/guidelines.md](references/guidelines.md).

## Storage

All decks are stored as JSON in `~/.openclaw/study-buddy/decks/`. Each deck file contains cards, review history, and scheduling metadata. See [references/data_format.md](references/data_format.md) for the schema.

## Multilingual Support

Study Buddy works in any language. Detect the user's language from their message and:
- Generate cards in the same language
- Quiz prompts in the user's language
- Support mixed-language decks (useful for language learning)
