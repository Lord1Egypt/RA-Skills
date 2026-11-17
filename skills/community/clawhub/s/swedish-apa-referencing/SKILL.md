---
name: "swedish-apa-referencing"
description: "Swedish APA 7 referencing with Sophiahemmet (SHH) deviations: reference lists, in-text citations, laws (SFS), ICN codes, secondary sources. Use for any assignment requiring referenslista enligt SHH APA / APA 7 på svenska."
---

# Swedish APA referencing (SHH)

Build correct Swedish APA 7 reference lists and in-text citations for academic coursework, with the Sophiahemmet Högskola (SHH) deviations. Swedish source language uses `I / Red. / s.`; English sources use `In / Ed. / p.` — match the language of the source.

## Steps

1. Read `references/APA-SHH-quickref.md` first. It is the operative quick reference for every rule below.

2. Determine the source type and language, then build the entry:
   - Article: `Efternamn, N. N. (År). Titel. Tidskrift, volym(nummer), s-ss. https://doi.org/…`
   - Book: `Efternamn, N. N. (År). Titel: Undertitel (x. uppl.). Förlag.` (edition from 2nd ed. onward)
   - Chapter in anthology: `Författare. (År). Kapiteltitel. I I. Redaktör (Red.), Bokens titel (x. uppl., s. xx-xxx). Förlag.`
   - Law: `SFS 2017:30. Hälso- och sjukvårdslag.`
   - ICN code: `International Council of Nurses. (2021). ICN:s etiska kod för sjuksköterskor (Rev. utg.). Svensk sjuksköterskeförening.`
   - Web page (non-PDF): add `Hämtad datum, från URL`; PDFs get the URL only, no Hämtad date.

3. Apply the SHH deviations (these differ from plain APA 7 and are the common fail points):
   - Page ranges use a hyphen, not an en dash: `s. 707-745`
   - No serial comma before `&` in editor lists: `A. Ehrenberg & L. Wallin`
   - No `a.a.`/`ibid.` anywhere
   - Laws and public documents: chronological order among the same type
   - Hanging indent optional; left-aligned is fine, be consistent

4. In-text citations: 1-2 authors written out, 3+ as `et al.`; `&` inside parentheses, `och` in running text. Page numbers mandatory for quotes, recommended otherwise: `(Arlebrink, 2019, s. 32)`. Laws: `(SFS 2017:30, 5 kap. 1 §)`.

5. Secondary source: cite only the source you actually read. In-text: `(Eriksson, 1989/1984, refererat i Willman, 2022, s. 203)`. Reference list: only Willman (2022).

6. Verify: every in-text citation matches a list entry by same lead author + year, and vice versa; alphabetical order (nothing before something: Löf < Löfgren < Lööf); same author+year → `2019a`/`2019b` suffixes in both text and list; no fabricated references.

## Pitfalls

- SHH courses require references for every claim, including reflections, with exact page numbers; avoid broad page ranges for specific definitions.
- Slides: no in-text references at all, reference list only (per SHH assignment formalia for presentations).
- Course AI policies may restrict AI use to language checking only; always check before drafting for a student.
- The full detailed guide with examples lives in `references/shh-apa-full.md`; consult it for edge cases (21+ authors, block quotes, personal communication, advance online publication).

## Provenance

Derived from Sophiahemmet Högskola's APA guide (2026), processed for agent use. Quickref and full guide authored in-workspace 2026-08-24. Verified against course feedback on SHH assignments.