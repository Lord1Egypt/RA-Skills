---
name: sermon-outline
description: Produces a sermon outline from a scripture passage or theme, ready for preaching. Use when the user asks for a sermon outline, preaching structure, or exposition on a passage or topic. Structure includes Introduction, Main Points, Applications, Conclusion; every point has scripture references.
---

# Sermon Outline

When the user provides a passage or theme, produce a sermon outline with the following structure. Output in English only. Default output is plain text; use Markdown or DOCX only if the user requests it.

## Defaults and overrides

- **Translation:** ESV unless the user specifies another (e.g. NIV, KJV, NASB).
- **Tradition:** Evangelical unless the user specifies Reformed, Charismatic, Baptist, Non-denominational, or other.
- **Output format:** Plain text by default; offer or use Markdown/DOCX only when the user asks.

## Shared guidelines

- Tone: reverent, clear, restrained; no mystical, off-topic, or esoteric language.
- Scripture: respect context; no proof-texting. Where an application or point goes beyond what the text explicitly teaches, label it **Reference application / not direct scripture**.
- Doctrine: avoid occult, extreme declarations, unorthodox terminology.
- Verse format: `(Book chapter:verse, translation)` e.g. `(John 15:5, ESV)`.

## Output structure

1. **Introduction** – Hook and focus; include at least one verse citation.
2. **Main points** – Numbered; each point and subpoint must have at least one scripture reference. Structure must be usable as-is for preaching.
3. **Applications** – Concrete, pastoral; with references where applicable. Label reference applications where not directly from the text.
4. **Conclusion** – Summary and closing; include at least one verse citation.

## Rules

- Every main point and subpoint must cite scripture; do not offer points without textual support.
- Do not use verses out of context to support a point.
- Keep the outline directly usable in the pulpit: clear headings, concise subpoints, cited verses.

## Example (structure only)

**Introduction:** [1–2 sentences; verse(s) cited.]  
**I. Main point 1** – (Reference, translation)  
  A. Subpoint – (Reference)  
  B. Subpoint – (Reference)  
**II. Main point 2** – (Reference)  
  …  
**Applications:** [2–3 concrete applications; cite verses where direct; label reference applications.]  
**Conclusion:** [1–2 sentences; verse(s) cited.]
