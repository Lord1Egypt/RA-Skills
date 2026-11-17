# Book type: arxiv-paper

**Kind markers:** claim, method, result, limitation
**Length band:** 40-70
**Template sections:** Claim, Method, Evidence, Limitations, Tests, See also
**Source line:** Source: <paper>, <locator> (<kind>)

Research papers and preprints in the arxiv shape: an abstract, numbered sections, a references list. The doc set extracts the paper's assertions and machinery as separate concepts: what it claims, how it works, what it measured, and where it breaks.

## What counts

A source routes here when it carries original research with an abstract and numbered sections: preprints, conference papers, and technical reports of the same shape. A book-length treatment of the same material routes to `non-fiction.md`, and a thesis routes to `thesis.md` even when one chapter is a paper.

## Segmentation

- The Abstract maps as front matter, one section.
- Numbered sections map by their numbers, `1` and `2.1` both, with subsections held inside their enclosing section.
- References maps as back matter, one section.
- Appendices map separately when present, `Appendix A` and onward.

Confirm the outline against the paper's own table of contents or section list before planning. A missing appendix is missing results, and results are doc material here.

## Concept grain

One claim, method component, result, or limitation per doc. A paper that makes five claims is five docs. Its training procedure and its evaluation harness are two docs. Each reported number that matters is a candidate result doc. The paper's own section boundaries do not decide the cut: a results section holds several results, and a method the paper spreads across three sections is one doc.

## Template

```markdown
# <Title>

Source: <paper>, <locator> (<kind>)

## Claim

The assertion this doc carries, stated plainly and scoped to what the paper shows.

## Method

How the component works, in the order a reader would rebuild it.

## Evidence

What was measured, over what, and with what comparison.

## Limitations

Where the claim breaks, as the paper states it or as its evidence implies.

## Tests

- A structural question a reader can ask of the paper or of a claim like it.

## See also

- <sibling>.md
```

## Kind markers

- `claim`: what the paper asserts, one assertion per doc.
- `method`: how it works, one component per doc.
- `result`: what was measured, one finding per doc.
- `limitation`: where the claim breaks, stated as the paper states it or as its evidence implies.

Every doc carries exactly one, on its Source line, and the index Kind column repeats it.

## Fan-out

The whole paper in one batch. A paper is short enough that one subagent sees all of it, and its claims, methods, and limitations cross section boundaries too tightly to split without losing the cross-references between them.
