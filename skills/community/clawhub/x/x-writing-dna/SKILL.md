---
name: x-writing-dna
description: Build auditable writing profiles for X accounts from complete public posts and articles. Use for reference-author research, separate short and long-form analysis, and evidence-linked writing practice.
license: MIT-0
---

# X Writing DNA

Work from a user-selected account to an inspected corpus, then derive bounded writing methods. The host agent supplies browser access; the included Python program checks records already collected. Nothing in this package starts a crawler or grants access to private data.

## Research sequence

1. Identify the requested author, genre and destination. Consult [collection](references/collection.md). A full branch requires 50 independent posts or 20 independent articles; requesting both means meeting both independently.
2. Operate a supported browser or explicitly authorized official API. Capture only public, complete author text. Do not collect credentials, private messages or hidden application data. Keep primary narration distinct from quotation cards.
3. Persist each work to `capture.jsonl`; checkpoint within five works. Retain original observations and use a separate normalized corpus for corrections. Open previews to the ending before calling a body complete.
4. Audit normalized records with `python3 scripts/corpus_audit.py /absolute/path/corpus.jsonl --author example --out /absolute/path/new-audit`. Read rejected records as well as counts. This standard-library helper checks explicit observations; it cannot independently authenticate an author or prove that text is complete. Its output separates raw records, eligible bodies, confirmed identities and native-X sources.
5. Read every accepted work and annotate it using [analysis](references/analysis.md). Build separate post and article profiles. Reserve five previously unread works per genre before profiling, freeze predictions, then record held-out successes and failures. An already-read corpus has no retrospective blind test.
6. Save `post-dna.md` and/or `article-dna.md`, work annotations, audits and `run-status.md`. Produce `genre-comparison.md` only when the same author has evidence in both branches.

## Minimum evidence discipline

A grouped thread is one work. Reposts, other speakers' quoted bodies, URL-only supplements, duplicate text, unfinished placeholders and incomplete bodies do not count. Coauthored material and repeated campaigns need separate treatment. A matching nickname does not establish that an external archive belongs to the X author.

After three successive page-load failures, checkpoint the visible error and remaining work, stop that route and try one legitimate alternative. Independent accessible branches may continue. Report unfinished branches as partial without borrowing counts from another format. An error without a rate-limit signal does not prove rate limiting.

A finished profile contains three to five observable mechanisms, with at least three independent supporting works for each, a denominator, exceptions and a practical exercise. Include six expression lenses and separate findings for judgment origin, choices/tradeoffs and recurring evaluation criteria. Missing evidence is an explicit result. Topic-heavy or campaign-heavy sampling limits the conclusion; counts alone do not make it representative.

## Transfer to writing

Suggest methods that fit the user's existing editorial rules, separately for short and long form. Two or three options should each have one main organizing principle. Never transfer another author's identity, life experiences, earnings or beliefs to the user. Public metrics are dated observations, not proof of a style's causal effect.

A handoff to `personal-content-dna` includes a method, genre, three or more source-work IDs, applicable conditions, limitations and one practice action. The user's actual edits or explicit decision determine adoption. Draft imitation, real user acceptance and publication performance are separate checks.

## Edition and credit

This registry edition contains independently written instructions and the project's original audit helper under MIT-0. The general idea of examining several aspects of writing was informed by [writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill); no upstream templates or workflow prose are bundled here. The GitHub root edition retains its own MIT licensing and attribution. See [LICENSE](LICENSE).
