# README patterns — the full catalog

Backing data for `SKILL.md`. Every number here is from the full study, `docs/README_WRITEUP.md` in the plugin repository, computed across 100 real READMEs from currently-trending GitHub repos (methodology and the full 100-repo table are there). This file is the catalog to load when a quick rule in `SKILL.md` isn't enough — a disputed recommendation, a section this skill's summary doesn't cover, or a request for a concrete example to imitate.

## Section presence and position

| Section | Present in | Avg. position (0=start, 1=end) | Median length when present |
|---|---:|---:|---:|
| Features / Why | 60% | 0.20 | 140 words |
| Table of contents | 12% | 0.23 | 58 words |
| Installation / Setup | 84% | 0.34 | 112 words |
| Demo / Screenshots | 24% | 0.38 | 49 words |
| Sponsors | 13% | 0.39 | 143 words |
| Architecture / How it works | 41% | 0.46 | 92 words |
| Usage | 24% | 0.47 | 36 words |
| API / Docs | 44% | 0.52 | 120 words |
| Examples | 13% | 0.53 | 8 words |
| Security | 16% | 0.54 | 151 words |
| Configuration | 33% | 0.56 | 135 words |
| Support / Community | 46% | 0.59 | 158 words |
| FAQ | 17% | 0.62 | 253 words |
| Testing | 14% | 0.66 | 53 words |
| Changelog | 32% | 0.71 | 60 words |
| Contributing | 52% | 0.77 | 50 words |
| Credits / Acknowledgments | 28% | 0.80 | 82 words |
| License | 72% | 0.93 | 13 words |

Read presence and position together. A section can be common and early (installation: 84% present, shows up about a third of the way through), common but late (license: 72% present, almost always last), or rare but consistent when present (sponsors, if a project has them, sits early — right after the pitch, near where a hero image would go).

Note what's *not* universal, against some generic advice: a table of contents is a minority pattern that tracks with document length, not a default courtesy. 12% have one under an explicit heading, 32% counting unlabelled anchor-link navigation. A standalone "Usage" section shows up in only 24% because many READMEs fold usage directly into the installation flow as one "get it running" sequence rather than splitting install and usage into two sections.

## Length

- Median README (prose only, code blocks excluded): **1,846 words**. 25th percentile: 1,311. 75th percentile: 3,612. 90th percentile: 6,040.
- A long README isn't itself a problem — several of the most effective ones in the study (Graphify, spec-kit) run long because they're thorough references, not because they're padded. The problem is when the *quickstart* is buried in the length. Graphify's discipline — a strict "30 seconds to first result" promise satisfied in the first screen, with the other 800+ lines as reference below it — is the model to imitate for a long README, not an argument against writing one.
- Average paragraph: 28.4 words (2–3 sentences). Nothing in the strong examples runs long, unbroken paragraphs — even dense technical READMEs (RuView, ECC) break into short paragraphs and tables rather than prose blocks.

## Sentence craft

Mean sentence length across the corpus is 20.1 words, but the median is 13.3 — a handful of dense repos pull the mean up, and the median is the better target for a typical section. Within a well-regarded README, sentence length is deliberately uneven: measured mix is roughly 38% short (<10 words), 37% medium (10–20), 26% long (>20). A run of same-length sentences reads as generated even when every individual sentence is fine — this is the same "uniformity is the strongest structural tell" principle the `rabbit-writes` craft engine already applies to any prose; nothing README-specific changes it.

## Links

Corpus-wide totals across every Markdown-syntax link in all 100 READMEs: inline links (`[text](url)`) 96.8%, bare unwrapped URLs 3.0%, reference-style links (`[text][ref]`) 0.2% — 14 total links out of 5,851. Reference-style is a "proper Markdown" technique some style guides teach, but it's not what actually-successful READMEs do; don't introduce it unless the user specifically wants it (e.g., a document with dozens of repeated links to the same few destinations, where a definition list genuinely reduces repetition).

Bare URLs are a minority slip, not a norm: 176 in the corpus, in half the repos, under two per README on average. Wrap them anyway, a bare URL gives a screen reader nothing to announce. An earlier version of the study put this at 29% because the parser counted URLs inside HTML `href`/`src` attributes; the writeup's Methodology section documents the correction. HTML `<a href>` links are excluded from these percentages, they are a third style and common inside centered headers.

Average inline link text length: 2.2 words. Link text names the destination — "the comparison doc," "our Discord," "the FAQ" — not "here," "this," or a full sentence.

## Visual formatting

| Technique | Share using it |
|---|---:|
| Any code block | 97% |
| Markdown table | 82% |
| Centered header block | 76% |
| Bare URLs present somewhere | 50%, averaging under two per README |
| Demo media of any kind | 89% |
| Any badge | 80% (median count 5, mean 5.7) |
| Badge row in the first 20 lines | 67% |
| Screenshot or logo image | 87% |
| Animated GIF | 14% |
| Embedded video | 19% |

Badge types by frequency across the corpus (counted from badge URLs, Markdown and HTML alike): license (56 occurrences), version/package registry (47), stars/social proof (39), chat/community — mostly Discord — (29), build/CI status (27), docs (4), sponsor (1). Coverage and code-quality badges, common in an older-style open-source README, barely appear in this sample; don't assume they're expected.

A badge row of four to six typed badges is the convention here, not an exception to apologize for. What the tail shows is the failure mode: ECC carries 17, and past roughly a dozen the marginal badge carries no information. Wire every badge to something real, and drop the ones that only exist to fill the row.

### Centered header with banner, badges, and inline navigation (TOC)

Centering the header (76% corpus) inside a `<div align="center">` block provides a clean, unified presentation for projects with visual assets. Combining the logo/banner, `# Title`, tagline, badge row, and a dot-separated inline anchor navigation bar satisfies both the pitch-first rule and the table of contents convention (32% corpus) without wasting vertical scroll:

```html
<div align="center">

<img src="assets/banner.png" alt="Project Logo" width="600">

# Project Name

Write and edit in **your** voice, not a chatbot's.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/owner/repo/ci.yml)](https://github.com/owner/repo/actions)
[![Version](https://img.shields.io/pypi/v/project.svg)](https://pypi.org/project/project/)

[Install](#install) • [Quickstart](#quickstart) • [Docs](#documentation) • [Contributing](#contributing) • [License](#license)

</div>
```

GIFs are less common (14%) than generic README advice suggests. When this corpus does show proof of output, it's more often a static screenshot, a linked hosted demo page, or — distinctively — a literal terminal transcript pasted as a code block. A pasted transcript is cheap to produce and reads as more credible than a staged screenshot; default to it for CLI tools over commissioning a GIF.

## Named techniques worth imitating

**Show the mechanism before the pitch.** `nextlevelbuilder/ui-ux-pro-max-skill` and `addyosmani/agent-skills` open with an ASCII pipeline diagram of their own workflow before any prose. `Graphify-Labs/graphify` and `garrytan/gstack` paste a real, reproducible terminal transcript instead of describing what running the tool looks like.

**Argue against your own headline number.** `DietrichGebert/ponytail` walks back an earlier marketing claim in the README itself and links the fuller writeup explaining why. `JuliusBrussee/caveman` has an explicit "honest number warning" stating its own headline stat can go net-negative in some cases. `ruvnet/RuView` labels every claim by evidence tier ("Real & validated" vs. "Architecture only, no weights") and retracts an old figure inline. This is the strongest single credibility pattern found in the study — apply it to any README making a performance, efficiency, or benchmark claim.

**Progressive disclosure via `<details>`.** `addyosmani/agent-skills` collapses every per-tool install path except the primary one; `farion1231/cc-switch` and `harry0703/MoneyPrinterTurbo` key collapsed FAQ entries to the literal error string a user would search for, so the page stays short but is still findable.

**Tables over bullet sprawl.** `NousResearch/hermes-agent`'s capability matrix and `github/spec-kit`'s "when to use which" decision table both do work a bullet list would make a reader scroll past. `VoltAgent/awesome-design-md` gets the same scannability from a different device — one consistent terse descriptor after every entry in a long list.

**Security/trust disclosures ahead of the pitch, for tools that touch the filesystem, network, or untrusted input.** `microsoft/markitdown` puts an `[!IMPORTANT]` security callout before the reader learns what the tool converts. `NousResearch/hermes-agent` includes a full antivirus-false-positive walkthrough with a copy-pasteable attestation script. `earendil-works/pi` lists concrete supply-chain hardening practices instead of a vague security promise.

## Anti-patterns, named

**Promotional content above the pitch.** `affaan-m/ECC` doesn't state what the project is until line 107, after a hero image, a 12-language link bar, four rows of badges, and a sponsor table. `farion1231/cc-switch` and `harry0703/MoneyPrinterTurbo` both put large sponsor blocks above their actual feature descriptions. Whatever sits before the first honest description of the project is a tax every future reader pays — check this first in any audit.

**Install-as-decision-tree.** `affaan-m/ECC`'s install section branches into guided/manual/per-harness/low-context/component-level/reset paths, each with warnings not to combine methods — a sign the install process itself needs simplifying, not just better formatting.

**Inconsistent numbers.** One repo in the study badges "84 UI Styles" at the top while the body text says "Available Styles (67)" a few hundred lines later. If a number appears more than once in a README, it should be the same number both times — an easy thing to miss when a doc gets edited piecemeal.
