# Documents — Long-Form, Structured, and Layout

A document is a translation problem plus a file problem plus a layout problem, and the file problem is where the hours go. Handle the container first; the prose is the easy part.

**Contents:** [The Order of Operations](#the-order-of-operations) · [File Formats](#file-formats) · [What Hides Outside the Body Text](#what-hides-outside-the-body-text) · [Layout After Translation](#layout-after-translation) · [Numbering, References, and Citations](#numbering-references-and-citations) · [Academic and Scientific](#academic-and-scientific) · [Patents](#patents) · [Financial Reports](#financial-reports) · [Technical Documentation](#technical-documentation) · [Slides and E-Learning](#slides-and-e-learning) · [Delivery Shapes](#delivery-shapes) · [What To Write Down](#what-to-write-down)

**Before starting a document for a client you have worked with**, read the pair's glossary and `styles/<locale>.md` if `## Boxes` names them, plus any `artifacts/brief-*.md` for that client. Document work is where terminology drift is most visible, because the reader sees fifty pages at once.

## The Order of Operations

1. **Get the editable source.** A PDF is a rendering, not a document; translating one means rebuilding it. Ask for the DOCX, IDML, or XML before quoting anything.
2. **Count and scope**: words, images containing text, tables, and whether the layout must match the original page for page (`jobs.md`).
3. **Freeze terminology first** — build or load the glossary before segment one, because a term changed on page 40 must be changed on pages 1-39 too (`terminology.md`).
4. **Translate in document order**, not in file order: a translation memory tool presents segments in the order they appear, which for headers, footers and text boxes is not reading order. Read the document as a document first.
5. **Reassemble and look at it.** Every defect in `Layout After Translation` is invisible in the segment editor and obvious on the page.

## File Formats

| Format | Translate via | What breaks |
|---|---|---|
| DOCX | The file itself, or XLIFF round-trip | Tracked changes and comments carried into the target; fields (`{ TOC }`, `{ REF }`) that need regenerating; text boxes and SmartArt outside the main flow |
| PPTX | The file itself | Speaker notes, slide masters, grouped shapes, charts whose labels live in an embedded workbook |
| XLSX | The file itself | Formulas containing text literals, sheet names, named ranges, column widths, cells that display `#####` after expansion |
| PDF (born digital) | Get the source; failing that, extract and rebuild | Reflow, fonts, tagging; a "translated PDF" is a new document and must be quoted as one |
| PDF (scanned) | OCR, then proofread the OCR against the image | OCR errors become translation errors nobody can trace; numbers and tables are the worst affected |
| IDML (InDesign) | The IDML, returned as IDML | Story order, anchored objects, paragraph styles, overset text that the exporter hides |
| LaTeX | The `.tex`, protecting commands | Commands and math must not be touched; `babel`/`polyglossia` language must change; hyphenation and bibliography style are locale-dependent |
| XML / DITA | The XML with a translate-aware filter | `conref`/`keyref` reuse, attributes that are translatable (`alt`, `title`), `translate="no"` respected |
| Markdown | Segment by block | Reference-style links, code fences, tables that need re-aligning (`web.md`) |
| Google Docs | Export to DOCX, or work in place with suggestions | Comments and suggestions are content someone will read |

## What Hides Outside the Body Text

Sweep every one of these before declaring a document complete: headers and footers · footnotes and endnotes · captions and figure titles · table headers and units in table cells · text inside images and diagrams · chart axis labels and legends · alt text · document properties (title, author, keywords) · comments and tracked changes · speaker notes · watermarks · form field labels and placeholder text · index and glossary entries · bookmarks and hyperlink display text · embedded objects from other applications.

Text baked into an image is the most common miss. It needs the source file for the image, and if there is none, it needs a decision from the client — quote it separately, never absorb it silently.

## Layout After Translation

- **Expansion hits documents as page count** (`SKILL.md` Rule 5): a 40-page English document becomes roughly 44-48 pages in German or Spanish. Say so before the client sees a bill for extra DTP.
- Regenerate the table of contents, indexes, and cross-references after translating; a TOC copied as text is a TOC that lies.
- Check for overset text in tables and shapes, `#####` in spreadsheet cells, and headings that now wrap to three lines.
- Hyphenation and justification are locale features: German needs hyphenation to avoid rivers, French sets its own spacing rules around punctuation (`locales.md`), CJK needs different line-break rules (`rtl-and-scripts.md`).
- Paper size: A4 nearly everywhere, Letter in North America. Different height means different pagination, which means every "see page 12" is now wrong.
- RTL documents bind on the other side: page order, margins, and the position of even and odd pages all mirror (`rtl-and-scripts.md`).
- Embed every font used, and verify on a machine that does not have them installed (`rtl-and-scripts.md`).

## Numbering, References, and Citations

- **Clause, section and article numbers are never renumbered.** In legal and technical documents they are addresses that other documents point at (`legal-medical.md`).
- Cross-references inside the document must resolve after translation. Automatic fields do this; typed references do not.
- **Citations are not translated.** Keep the original title, journal, and author names exactly; add a translated title in brackets only when the target's style guide asks for it.
- When the source quotes a work that has a published translation in the target language, **use the published translation and cite that edition** — retranslating a famous passage is both wrong and noticeable.
- Bibliographic style itself is locale-dependent (author-date, numeric, footnote-based). Ask which one applies rather than converting silently.
- Legal citations and case names stay in the source jurisdiction's form; a gloss in brackets is the right way to help the reader.

## Academic and Scientific

- The abstract and keywords are separately indexed and are what most readers see. Keywords are chosen from the target field's controlled vocabulary (MeSH and its translations, for instance), not translated word by word.
- Terminology follows the target field's usage, which sometimes keeps the English term: much of biology, computing and finance uses English terms in languages that could translate them. The glossary decides, and the field's own journals are the evidence.
- Preserve hedging exactly. "May suggest" is not "shows"; strengthening a claim in translation is a research-integrity problem, not a style choice.
- Author names, affiliations and funding statements are transliterated at most, never translated; use the author's own published form (`numbers-and-names.md`).
- Units, statistics and figures get re-read against the source at the end as a separate pass. A transposed digit in a p-value is the defect a reviewer will find.

## Patents

- **Literal to the point of awkwardness.** Claims define legal scope; improving the prose narrows or widens it. If the source is ambiguous, the target is ambiguous in the same way, with a translator's note flagging it — never resolved.
- One claim is one sentence, however long, and its structure (preamble, transitional phrase, elements) is preserved. The transitional phrase is a term of art: "comprising" (open) and "consisting of" (closed) are not interchangeable, and their target equivalents are fixed by the receiving office's practice.
- Terminology consistency is absolute: the same element is the same word every time it appears, including in the abstract and the drawings list. Synonym variation, which is good style elsewhere, is a defect here.
- Reference numerals must match the drawings exactly, and the element they name must not change between claims and description.
- Filing deadlines and required certifications are per-office (`legal-medical.md`).

## Financial Reports

- Figures are re-verified against the source as a dedicated pass: totals, percentages, footnote markers, and the sign convention (parentheses for negatives).
- Accounting terminology depends on the reporting standard, not only the language — IFRS and US GAAP name things differently, and a target market's statutory terms may differ from both. Ask which standard governs before choosing terms.
- Never convert currency, and keep the fiscal-year convention of the source with a note when it differs from the target market's (`numbers-and-names.md`).
- Forward-looking statements, audit opinions and legal disclaimers are boilerplate with settled target-language wording. Find the standard wording; do not compose it.

## Technical Documentation

- **Controlled source language pays for itself**: a manual written in a restricted vocabulary and one-instruction-per-sentence style (the ASD-STE100 tradition) translates faster, cheaper and more consistently. Where the source is not controlled, the highest-leverage advice is often to fix the source.
- Structured content (DITA, DocBook) is reused across products through `conref`; translating a reused topic twice means it will diverge. Respect the reuse map.
- **Safety notices are regulated text.** The signal-word hierarchy (danger / warning / caution / notice) maps to standardized target-language terms and a required visual treatment; picking a near-synonym breaks compliance. Instructions for use of a medical device or machinery go through `legal-medical.md`.
- Procedures stay imperative and one step per step. Merging two steps because the target reads better is a change to the procedure.
- UI strings quoted in a manual must match the shipped translation of the software exactly — pull them from the string catalog, do not retranslate them (`software-strings.md`).

## Slides and E-Learning

- Slides fail on expansion more than documents do, because the box is fixed. Condense the text rather than shrinking the font; below the deck's smallest defined size, it is a layout change and the client decides.
- Speaker notes are content and are usually forgotten in the quote.
- E-learning has on-screen text and narration that must stay in sync: if the narration is dubbed, the target script must fit the original timing (`subtitles.md`); if it is subtitled, reading speed applies.
- Quizzes carry hidden text: distractors, correct-answer feedback, wrong-answer feedback, and progress messages. Ask for the full string export rather than translating what is visible in the player.

## Delivery Shapes

`deliverable_shape` decides the default: target-only for finished documents, bilingual table for review and for legal work, inline comments when the client needs to see the decisions. Two extra conventions worth offering: a **clean and a tracked copy** when the client is revising an existing translation, and a **translator's note list** at the end for genuine ambiguities in the source — short, numbered, and only for things the client must decide.

## What To Write Down

- The client's document conventions — style guide, glossary, preferred delivery shape, whether DTP is included — belong in an **`artifacts/brief-<client>.md`**, born as its own file, with its `## Boxes` line naming when to read it.
- A finished document the client approved and will be measured against later is a **reference text**: keep the excerpt that anchors the voice in `artifacts/`, strip personal data, and never store the full confidential document (`memory-template.md`).
- Terminology settled during the document goes into the pair's glossary in the same session, not at the end of the project — the end of the project is when it gets skipped.
- A delivered document is a row in **`deliveries/<year>.md`** with its word count and reviewer.
