# Book type: thesis

**Kind markers:** method, convention, finding
**Length band:** 40-70
**Template sections:** The expectation, Practices, Anti-patterns, Tests, See also
**Source line:** Source: <book>, <locator> (<kind>)

Masters and doctoral theses. The doc set extracts what the thesis form expects: the conventions each chapter answers to, the methods discipline it follows, and the findings it reports, each as one doc a reader can check their own work against or study from.

## What counts

A source routes here when it is a thesis or a dissertation: front matter carrying an abstract and a table of contents, chapters in the thesis order (introduction, literature review, method, results, discussion, conclusion), then a bibliography and appendices. A single paper routes to `arxiv-paper.md` even when its author files it as a thesis chapter.

## Segmentation

- Thesis front matter maps as sections: abstract, table of contents, list of figures, list of tables, list of abbreviations.
- Each chapter maps by its `Chapter N` heading.
- The bibliography maps as one back-matter section.
- Each appendix maps separately, `Appendix A` and onward.

Confirm the outline against the thesis's own table of contents before planning. The front matter declares conventions the chapters then perform, so a missing abstract or abbreviations list is missing convention material.

## Concept grain

One expectation or convention per doc: what the committee expects a literature review to do, how a method chapter justifies its choices, what a contribution statement must carry, what the results chapter owes a figure. Findings the thesis reports can each take a doc under the `finding` marker.

## Template

```markdown
# <Title>

Source: <book>, <locator> (<kind>)

## The expectation

Two or three sentences. What the thesis form expects here, and why the form expects it.

## Practices

1. One imperative sentence per practice, numbered.

## Anti-patterns

- The failure mode, and what it costs at review or defense.

## Tests

- A structural question a reader can ask of a real thesis chapter.

## See also

- <sibling>.md
```

## Kind markers

- `method`: how the thesis conducted or analyzed its work, one component per doc.
- `convention`: what the form expects, structural or formatting.
- `finding`: a result the thesis reports, one per doc.

Every doc carries exactly one, on its Source line, and the index Kind column repeats it.

## Fan-out

2 to 3 docs per subagent, batched by chapter. A convention draws on the chapter that demonstrates it plus the front matter that declares it, and a batch bigger than one chapter mixes the grain.
