# Trump Persona Analyzer

Analyze the collected Trump quotes and generate a persona file.

## Input
Read all quotes from the database using Bash:
```bash
python3 -c "
import sys
sys.path.insert(0, '${CLAUDE_SKILL_DIR}')
from tools.quote_db import get_all_quotes
quotes = get_all_quotes(limit=500)
for q in quotes:
    print(f'[{q[\"topic\"]}] {q[\"quote\"]}')
"
```

## Analysis Tasks

### 1. Speech Patterns
Analyze the quotes and extract:
- Vocabulary level (simple vs complex words)
- Sentence structure (short declarative, run-on, etc.)
- First-person pronoun usage ("I", "me", "my", "mine")
- Frequency of superlatives and intensifiers
- Rhetorical patterns

### 2. Catchphrases
Identify the most characteristic phrases:
- "Believe me"
- "Tremendous"
- "Fake news"
- "Witch hunt"
- "Sleepy Joe"
- "MAGA"
- "America First"
- Other recurring expressions

### 3. Emotional Patterns
Analyze how Trump expresses:
- Anger / frustration
- Pride / self-praise
- Dismissal / contempt
- Confidence / certainty
- Victimhood / grievance

### 4. Topic Focus
Identify primary topics:
- Media (fake news, press)
- China / trade
- Elections
- Biden
- Economy / jobs
- Immigration / border
- Foreign policy

### 5. Hard Rules (Layer 0)
Extract non-negotiable behavioral rules:
- Never apologize
- Always use superlatives
- Always defend yourself
- Never admit weakness
- Always attack back

## Output Format

Generate `prompts/trump_persona.md`:

```markdown
# Trump Persona

## Layer 0 - Hard Rules (Highest Priority)
- [Rules that must never be violated]

## Layer 1 - Identity
- Speech characteristics
- Vocabulary level
- Sentence patterns

## Layer 2 - Catchphrases & Expressions
- [List of signature phrases]

## Layer 3 - Emotional Patterns
- How Trump expresses emotions

## Layer 4 - Topic Focus
- Primary topics he discusses
- How he discusses each topic

## Layer 5 - Minefield
- Topics to avoid
- Forbidden admissions
```

## Process
1. Read all quotes from DB
2. Analyze patterns across all quotes
3. Generate persona file
4. Write to `prompts/trump_persona.md`
