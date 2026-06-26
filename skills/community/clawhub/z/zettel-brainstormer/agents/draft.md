# Draft Agent

## Goal
Synthesize relevant preprocessed notes into a structured draft with full traceability.

## Model Tier
- Use `agent_models.drafter` from config.
- Resolve to `models.deep` by default for synthesis quality.
- Allow `models.fast` only for lightweight early drafts.

## Input
- Seed note content
- Filtered relevant preprocess outputs
- Citation mapping (`filepath` and note title)

## Writing Requirements
- Build the draft around clear thesis and tiered argument sections.
- Build from the full set of relevant notes; the draft does not need to revolve only around the seed note.
- Keep only relevant points that support the thesis. Discard any sections that do not directly support the thesis.
- Merge overlapping points without losing source attribution.
- Avoid invented claims.
- Create short, scan-friendly section headings that read like labels, not full claims.
- Before writing full prose, create a high-level argument scaffold so the final post reads as one coherent chain.

## Heading Rules
- Prefer `##` headings that are roughly 2-6 words.
- Keep headings compact when possible (around 8 words or fewer).
- Use title case and concrete nouns.
- Avoid subtitle-style punctuation such as colons, semicolons, and em dashes.
- Do not write headings as full sentences or complete argumentative claims.
- If the draft auto-numbers subsections, keep labels compact after the number (for example: `1.1 Stories, Not Just Facts`).

## Heading Compression Examples
- Long: `Humans Coordinate Through Story, Not Just Facts`
- Better: `Stories, Not Just Facts`
- Long: `When Epistemic Habits Decay, Democracy Becomes Procedural but Empty`
- Better: `Impact on Democracy`
- Long: `Silicon Valley's Political Turn Is a Symptom of Deeper Legitimacy Fracture`
- Better: `Silicon Valley's Political Turn`

## Citation Rules
- Cite every source-backed claim inline using `[[Note Title]]`.
- Do not cite notes that are not used.
- Keep citation-title mapping consistent with input metadata.
- Ensure claims in the argument spine also point to supporting preprocessed notes.

## Argument Scaffold Requirement
- Start with a brief "argument spine" before the full draft body.
- Label this section as internal scaffolding for the publisher step.
- The spine should include:
  - central thesis (1-2 sentences),
  - ordered major claims (3-5 bullets),
  - logic of progression (how each claim leads to the next),
  - where each claim is supported by preprocessed notes and references.
- Use this scaffold to prevent disconnected sections and "frankenstein" structure.
- When merging points, preserve the chain of reasoning first, then optimize prose.

## Output
- A short high-level argument scaffold at the top, clearly marked as internal (not final blog content)
- Markdown draft with section headings
- `## References` at the end with all cited notes (unique)
