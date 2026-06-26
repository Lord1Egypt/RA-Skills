# Style Extraction Guide

## Input
- Document content (from Feishu or other sources)
- Author name (optional)
- Document type (requirements/technical/meeting/other)

## Analysis Dimensions

### 1. Title Hierarchy
- How # ## ### are used
- Fixed structures like "Background", "Solution", "Todo"

### 2. Paragraph Organization
- Background → Solution → Todo
- Problem → Analysis → Conclusion
- List-based

### 3. Code Block Preferences
- Common languages: cpp / json / python / plaintext
- Code block ratio

### 4. Table Usage
- Frequency of tables
- Table purposes (comparison? parameters? interfaces?)

### 5. Tone
- Casual vs formal
- Level of colloquialism

### 6. High-Frequency Vocabulary
- Technical terms
- Personal catchphrases

### 7. Layout Habits
- Whitespace
- List styles
- Quote patterns

### 8. Collaboration Elements
- @mention style
- Document references
- Todo markers

## Batch Learning Mode

When learning from multiple documents:

1. **Extract** - Analyze each document individually
2. **Compare** - Find similarities and differences
3. **Summarize** - Focus on common patterns (especially format-related)
4. **Generate** - Create unified style guide

### Common Pattern Types (Priority)
- Document structure
- Title hierarchy
- Code block formats
- Table layouts
- List styles

## Output Format

```markdown
## Style Profile: [Author Name]

### Core Characteristics
- Characteristic 1
- Characteristic 2

### Structural Features
- Title hierarchy: xxx
- Paragraph organization: xxx

### Format Preferences
- Code blocks: xxx
- Tables: xxx

### Vocabulary
- High-frequency words: xxx
- Tone: xxx

### Collaboration Habits
- @mentions: xxx
- References: xxx
```

## Storage

After extraction, save to:
- Personal: MEMORY.md
- Team: Specified knowledge base
