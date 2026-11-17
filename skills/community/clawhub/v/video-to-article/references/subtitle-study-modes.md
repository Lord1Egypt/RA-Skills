# Subtitle Study Modes

## Mode selection

```text
User has a subtitle file or transcript -> what do they want?
  |- "summarize it" / "what is this about?" -> B1: Knowledge extraction
  |- "split it into chapters" / "what sections does it have?" -> B2: Chapter summary
  |- "extract terminology" / "make a vocabulary list" -> B3: Keyword glossary
```

## B1: Knowledge extraction output

```markdown
# <Video Title>
## Chapter 1: <Chapter Name>
### Key Concepts
- Concept 1: explanation
### Key Takeaways
- Main takeaway 1
### Examples / Demonstrations
- Example 1: explanation

### Glossary
| Term | Explanation |
|------|------|
```

## B2: Chapter summary

Topic-shift signals:
1. speaker transitions such as "Now let's talk about..."
2. gaps longer than 5 seconds in the subtitle timeline
3. heavy introduction of new terminology or concepts
4. explicit ordering such as "first", "second", or numbered lists

Output format:

```markdown
## Chapter N: <Inferred Chapter Name>
### Time Range: 00:00 - 05:30
### Core Summary: 2-3 sentences
### Key Points
- Point 1
```

## B3: Keyword glossary

Extraction targets:
- domain-specific terms
- vocabulary repeated three or more times
- clearly defined concepts
- acronyms and their expanded forms

Output table:

| Term | Translation | Context Explanation | Location |
|------|------|------|------|

## Subtitle quality handling

| Problem | Handling |
|------|------|
| Misheard names | Mark as `[possible transcription error]` |
| Broken technical terms | Merge them into the correct term |
| Mixed Chinese and English | Preserve the original wording |
| Multiple speakers merged together | Mark as `[possible multi-speaker dialogue]` |
| Purely visual content | Mark as `[visual content here]` |
