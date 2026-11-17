# Book type: non-fiction

**Kind markers:** practice, context
**Length band:** 40-70
**Template sections:** What this is, Practices, Anti-patterns, Tests, See also
**Source line:** Source: <book>, <locator> (<kind>)
**Free-form files:** glossary.md

Practice and craft books: anything that argues for a way of working and tells the reader what to do about it. The doc set extracts the practices and the theory behind them as separate concepts, one thing a reader can act on per doc, or one thing that explains why the practices have the shape they do. The worked example of this whole template is `docs-best-practices/` at this repository's root.

## What counts

A source routes here when its chapters carry advice, practices, methods, or the reasoning behind a discipline: professional practice books, craft books, books on technical communication, management, or writing. A book of writing advice about fiction still routes here rather than to `fiction.md`, which is for novels themselves. A research report with an abstract and numbered sections routes to `arxiv-paper.md`.

The source's own glossary becomes `glossary.md`, the one free-form file this type declares: it carries no template sections, no Source line, and no index row. `check_notes.py` only requires it to have exactly one `# ` heading and content.

## Segmentation

- `Chapter N` headings, with or without a title.
- Bare numbered titles, `5.8 The role of lists`, which map as sections inside the enclosing chapter.
- Roman-numeral parts, `Part II`, as containers of the chapters under them.
- Named front and back matter from Preface through Index: Foreword, Preface, Acknowledgments, Introduction at the front, and Afterword, Appendix, Bibliography, Glossary, Index at the back, all mapped as sections rather than skipped.

Confirm the outline against the source's own table of contents before planning. A back-matter section the map missed is material the plan never sees.

## Concept grain

One concept per doc. A concept may sit inside one section of one chapter, or merge the same idea as the book develops it across chapters, which is the common case in a book that returns to its themes. Do not cut by chapter: three practices in one chapter are three docs, and one practice the book builds across four chapters is one doc.

## Template

```markdown
# <Title>

Source: <book>, <locator> (<kind>)

## What this is

Two or three sentences. What the concept is and what problem it answers.

## Practices

1. One imperative sentence per practice, numbered, concrete enough to act on without the book.

## Anti-patterns

- The failure mode, and what it costs.

## Tests

- A structural question a reader can ask of a real page or doc.

## See also

- <sibling>.md
```

## Kind markers

- `practice`: the rules themselves. What to do to a page, a doc set, or a codebase.
- `context`: the theory behind the rules. Why the discipline or the medium forces this shape.

Every doc carries exactly one, on its Source line, and the index Kind column repeats it.

## Fan-out

3 to 5 docs per subagent, batches under roughly 2,000 source lines. A practice doc needs its own section plus the places the book returns to the practice, and a batch much past that size invites summary instead of extraction.
