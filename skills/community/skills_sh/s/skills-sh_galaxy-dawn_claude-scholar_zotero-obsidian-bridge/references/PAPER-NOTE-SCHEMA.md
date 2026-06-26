# Zotero-Sourced Paper Note Schema

## Frontmatter

```yaml
---
type: paper
project: project-slug
title: "Paper Title"
canvas_visibility: hidden
authors:
  - Author A
  - Author B
year: 2026
venue: "NeurIPS"
doi: "10.xxxx/xxxxx"
url: "https://doi.org/..."
citekey: "author2026paper"
zotero_key: "ABCDEFGH"
status: read
source_type: full paper
claim_strength: observed
keywords:
  - subject-invariance
  - contrastive-learning
concepts:
  - shared geometry
methods:
  - contrastive pretraining
subfield: speech-transfer
related_papers:
  - "Sources/Papers/Another-Paper"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
argument_claims:
  - "Shared geometry exists but is fragile"
argument_methods:
  - "Geometry-aware transfer"
argument_gaps:
  - "Still needs speech-specific validation"
paper_relationships:
  - "Sources/Papers/Another-Paper::complements"
updated: 2026-03-16T00:00:00Z
---
```

## Sections

```markdown
# Paper Title

## Claim

## Research question

## Method

## Evidence

Use the shared Evidence Record shape from `research-ideation/references/research-contract.md`.

## Strengths

## Limitation

## Direct relevance to repo

## Relation to other papers

## Knowledge links

## Optional downstream hooks
- Writing:
```

## Rules

- `related_papers` and `linked_knowledge` should prefer project-relative note paths.
- `paper_relationships` should record explicit semantic edges only when they are stable enough to support graph construction.
- `concepts` and `methods` may remain plain strings; do not create dedicated notes by default.
- Keep `Direct relevance to repo` concrete and actionable.
- Prefer one durable canonical note per paper; update in place instead of making sibling notes.
- If the user asked for a full collection pass, normalize the schema across the entire covered set before closing the task.
- Treat Zotero `webpage` items as weak-source inputs by default. If they are abstract-only or placeholder pages, set `source_type: webpage placeholder` or `source_type: abstract-only`, keep `status: to-read`, and do not use them to support `Knowledge`, manuscript, or rebuttal claims.
