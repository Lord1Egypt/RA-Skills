# Book type: fiction

**Kind markers:** craft, structure
**Length band:** 40-70
**Template sections:** The move, Where it shows up, How to do it, Fails when, Tests, See also
**Source line:** Source: <book>, <locator> (<kind>)

Novels and story collections, read as craft. The doc set extracts the moves: what the author does on the page that a writer can study, name, and do deliberately. The notes are about technique, never plot, and a doc names a move and points at where the text performs it.

## What counts

A source routes here when it is narrative prose the user wants craft notes from: a novel, a collection, a memoir with a strong narrative spine. A craft book that teaches writing, fiction or otherwise, routes to `non-fiction.md`, because its chapters carry advice rather than performances of it.

A plot summary is not a deliverable in this type. If the ask is "what happens in this book", that is a question to answer directly, not a doc set to build.

## Segmentation

- `Chapter N` headings, numbered, titled, or both.
- Part divisions, roman or plain numerals, as containers.
- Scene breaks where the author marks them, inside the enclosing chapter.
- A source with no headings at all maps by line bands of even length.

The Source line locator is a chapter or scene reference, `ch. 14` or `ch. 14, scene 2`, never a page number. A page number is an artifact of one edition, and a chapter or scene reference survives the next one.

## Concept grain

One craft move per doc: a type of transition, a way of handling time, a method of characterization, a sentence rhythm, a structure for withholding information. The doc is about the move, and the source is evidence for it rather than the subject of it. A move the author uses once is a candidate doc only when it lands hard enough to be worth a name.

## Template

```markdown
# <Title>

Source: <book>, <locator> (<kind>)

## The move

Two or three sentences. Name the move and what it does to the reader.

## Where it shows up

The chapters or scenes that perform it, each pointed at with a paraphrase, never a quotation.

## How to do it

1. One imperative sentence per step, numbered.

## Fails when

- What the move costs when it is done badly or overused.

## Tests

- A structural question a reader can ask of a real manuscript.

## See also

- <sibling>.md
```

## Kind markers

- `craft`: a move at the sentence or scene level.
- `structure`: a move at the arc, chapter, or whole-book level.

Every doc carries exactly one, on its Source line, and the index Kind column repeats it.

## Fan-out

One doc per subagent, over a wide range, often the whole source. The evidence for a craft move is scattered across the text, and a subagent holding several docs at once summarizes the chapters it was given instead of extracting the one move wherever it appears. Because running whole-source reads across dozens of subagents carries a high token cost, aim for a focused set (typically 10 to 20 signature moves) rather than an unbounded extraction.
