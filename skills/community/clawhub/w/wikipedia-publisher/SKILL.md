---
name: wikipedia-publisher
description: Draft, review, de-risk, and publish Wikipedia or Wikidata content with a bias toward policy-safe workflow. Use when creating or editing encyclopedia articles, sandbox drafts, Wikidata items, citations, notability/source assessments, conflict-of-interest reviews, or MediaWiki wikitext. Especially useful for company, founder, product, or client subjects where promotional tone, weak sourcing, or direct-to-mainspace publishing would be risky.
---

# Wikipedia Publisher

Use a conservative workflow. Prefer publishable drafts over impressive drafts.

## Default workflow

1. **Collect evidence first**
   - Gather independent secondary coverage before writing.
   - Separate independent sources from primary/company sources.
   - Do not treat the subject's own site as proof of notability.
   - Run `scripts/citation_fetch_enricher.py` first when URLs are bare, weak, or missing metadata.
   - Run `scripts/source_hygiene.py` and `scripts/notability_score.py` early.

2. **Decide the safest target**
   - Prefer `User:` sandbox or `Draft:` namespace for new articles.
   - Use mainspace only when the article is already established or the user explicitly wants that path and the sourcing is strong.
   - For conflict-of-interest situations, prefer sandbox + disclosure-minded language.

3. **Write plain, non-promotional prose**
   - State what the subject is, why it received coverage, and what reliable sources say.
   - Attribute claims when needed: "According to X..." or "Coverage in Y described..."
   - Avoid mission-language, puffery, rankings, and unverified superlatives.
   - If a paragraph smells like PR, run `scripts/coi_rewrite.py` and then edit manually.

4. **Run a risk pass before publishing**
   - Check tone with `scripts/coi_tone_lint.py`.
   - Check citation/source mix with `scripts/source_hygiene.py`.
   - Check likely rejection risk with `scripts/deletion_risk_check.py`.
   - Use `scripts/citation_normalizer.py` to clean weak references.
   - Remove unsupported claims, crowded lists, and anything sourced only to the subject.
   - Make sure the lead can stand on independent sources alone.

5. **Publish conservatively**
   - Save to sandbox/draft first unless there is a good reason not to.
   - Use `scripts/sandbox_publish.py --dry-run` before live save.
   - Use a factual edit summary.
   - Verify the live page after save.

## Writing rules

- Prefer independent news/features/books over press releases, directories, or the company site.
- Keep claims proportional to source strength.
- Use primary sources for routine facts only: founding date, location, official name, contact details, basic product list.
- Avoid these unless clearly and independently sourced:
  - "leading", "world-class", "premier", "innovative", "trusted"
  - "official" except when it is structurally true and relevant
  - unsourced rankings, market leadership, customer counts, geographic scale, or awards
- Do not pad new articles with trivia or exhaustive project catalogs.
- When in doubt, shorten.

## Article shape for company/org drafts

Use this default structure unless the sourcing suggests otherwise:

- Lead
- History
- Operations or Products/Services
- Reception / Coverage / Major projects (only if independently notable)
- See also

Skip sections that cannot be supported cleanly.

## Sandbox-first publishing pattern

When the user wants a new page:

1. Draft locally in `.wiki` or `.md`.
2. Convert to clean MediaWiki markup if needed.
3. Save to `User:<name>/<topic>` or `Draft:<topic>`.
4. Fetch the saved page and inspect the rendered result.
5. Only then discuss moving toward mainspace.

## Wikidata pattern

For Wikidata work:
- confirm an item does not already exist
- collect minimally sufficient identifiers and statements
- prefer low-controversy statements first: instance of, country, official website, inception, founders
- cite every claim you can
- avoid copying marketing copy into descriptions or aliases
- use `scripts/wikidata_helper.py` for a clean starter bundle

## Red flags that should slow you down

Read `references/red-flags.md` when any of these appear:
- only primary or affiliated sources
- article reads like PR
- many claims use the same weak source repeatedly
- the user wants direct mainspace publication for their own company/client
- notability seems to rest on routine business coverage or local mentions

## Helpful resources

- `scripts/source_hygiene.py` — classify citations as independent, primary, press-wire, directory, or review-needed
- `scripts/notability_score.py` — rough article-viability scoring from the citation mix
- `scripts/coi_tone_lint.py` — lightweight tone/source risk checker for drafts
- `scripts/deletion_risk_check.py` — heuristic rejection/deletion-risk checker
- `scripts/citation_fetch_enricher.py` — fetch live metadata from URLs and suggest richer cite templates
- `scripts/citation_normalizer.py` — suggest cleaner cite templates and missing metadata
- `scripts/coi_rewrite.py` — rewrite PR-ish text into more neutral attributed prose
- `scripts/sandbox_publish.py` — sandbox/draft publishing helper for MediaWiki API
- `scripts/wikidata_helper.py` — starter statement generator for Wikidata items
- `references/red-flags.md` — quick safety checklist for companies, people, and organizations
- `references/workflow.md` — recommended script order and interpretation
- `references/citation-guidelines.md` — citation cleanup guidance

## Output preferences

When showing a proposed edit:
- start with the target page title
- show the lead first
- summarize major sourcing assumptions
- call out any unsupported or COI-sensitive areas plainly
- recommend sandbox/draft vs mainspace explicitly
