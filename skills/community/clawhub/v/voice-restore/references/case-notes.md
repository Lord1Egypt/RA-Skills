# Case notes — one forensic pass, including three corrections I had to make

Anonymised. Numbers are real; names, institution and course are not.

**Subject.** A 54-page honours thesis in finance: 8,962 words of body prose across 463 sentences
in 122 paragraphs. Measured from the LaTeX source, not the PDF (see §6).
Turnitin returned **46%** with 69 segments flagged as AI-generated. The author's declaration
openly states that GenAI was used "to assist with language editing, code checking, and
debugging" — so the question was never *whether*, but *which layer*.

**Reference corpus.** Two sources, both undetected:
- 1,421 words the same author wrote alone, same discipline, different course
- 1,950 words split across two co-authors on a group project (used to place the author's
  position between a fluent writer and a recent arrival)

> **Measurement note.** Every count below comes from one instrument
> (`scripts/voice_metrics.py`, v1.0.0), so the numbers are comparable to each other but
> not necessarily to yours. Word counts run about 2% lower than Word's, because the script
> only counts tokens that begin with a letter — `0.51`, `2021` and `13,700` are words in
> Word and not here. Percentages move with the denominator, so a 2% word difference is a
> 2% difference in every per-1k rate. Treat these as **readings from a named instrument**,
> not as constants of the text.

---

## 1. What the forensics found

| Tell | Thesis body | Author's own writing |
|---|---|---|
| first person (`I/we/us/our/my/me`) | **0** in 8,962 words | 3 in 1,421 (`us` ×3) |
| prose semicolons | **18** | **0** |
| `The` initial | **26.3%** | 14.1% |
| `This` initial | **5.4%** | 19.2% |

All three at once is the signature of a **polish pass**, not a generation:

- zero first person across 8,962 words is not restraint, it is deletion
- his first person is not `I` — it is argumentative `us` (`remind us`, `does not tell us`).
  That habit was zeroed out entirely
- semicolons weld two sentences into one. Nobody drafts that way; editors do
- he delegates anaphora to `This`. Where he would have written `This …`, the polished draft
  has `The …`: 26.3% `the`-initial against his 14.1%, and `this` down to 5.4% from 19.2%

## 2. What argued against wholesale generation

| Evidence | Why it matters |
|---|---|
| Sample-construction counts consistent across four deletion stages (15.7M → 139,904 → 41,945 observations) | A model does not invent a coherent multi-stage attrition chain |
| Section 1.1 opens with `this` at 25.0% and `the` at 6.2%, against 26.3% `the` for the body | That is his own opener habit, intact in the section he wrote first |
| Nominalisation density 63.7/1k vs his 59.1/1k | Polish usually pushes this up; it barely moved |
| AI-word list scored 0.5/1k vs his 2.1/1k | The draft was *cleaner* than he is. The word list is useless on this corpus |

Conclusion delivered: **human analysis, machine-polished sentences.**

---

## 3. Three corrections

### 3.1 "Semicolons: 24" → 16

The first count included table footnotes (`Notes: … ; …`, which are conventionally
semicolon-heavy) and citation separators inside parentheses (`(A 2019; B 2021)`).
Counting only prose, outside parentheses: **16**. Still zero on his side, but the tell
was overstated by 50%.

**Rule:** before reporting a character count, ask *where* that character lives and whether
it belongs to the text class you are describing.

### 3.2 "Raise sentence-length cv to 0.42–0.52" → wrong direction

His own cv is **0.286**. The thesis was already **0.478**. The instruction to increase
variance would have moved it *away* from him. Two gate values built on "human writing
averages" had to be withdrawn after the reference corpus arrived:

- `cv 0.36–0.85` — his genuine writing scores 0.286, i.e. **fails the gate**
- `article-initial ≤24%` — his genuine writing is 41.0%, i.e. **fails the gate**

### 3.3 "Add `I`" → should be `us`

The first rewrite added first-person `I`. Wrong: all three of his first-person tokens
are argumentative `us`. A rhetorical `us` restores his stance; an `I argue` invents a
different author.

---

## 4. A rewrite that overshot

First restoration of one 284-word section produced:

| | target | first attempt |
|---|---|---|
| sentence mean | 18.5 | **16.9** |
| short sentences | 6% | **29%** |

It had been "de-flattened" into choppy prose — the generic humanising reflex, applied
by default. Second attempt, merging back to 13–27 word sentences:

| | author | draft | restored |
|---|---|---|---|
| sentence mean | 18.5 | 34.2 | **18.8** |
| cv | 0.286 | 0.464 | 0.255 |
| `The` initial | 14.1% | 55.6% | 11.8% |
| `This` initial | 19.2% | 0% | 17.6% |
| prose semicolons | 0 | 1 | 0 |
| first person | 3 | 0 | 1 (`us`) |

## 5. Vocabulary layer, forgotten on the first pass

Syntax-only editing left the word layer untouched — and made two densities worse:

| per 1k words | original | syntax-only pass | after vocabulary pass | author |
|---|---|---|---|---|
| `therefore` | 1.7 | **3.2** ✗ | 1.1 | 1.4 |
| `rather than` | 1.8 | **2.1** ✗ | 0.7 | 0.7 |
| `associated with` | 1.2 | 1.4 | 1.1 | 0.7 |
| `however` | 0.4 | 0.4 | 0.7 | 1.4 |
| `consistent with` | 0.5 | 0.7 | 1.1 | 1.4 |

Rebuilding sentences tempts you to add connectives; that is exactly how `therefore` reached
2.3× the author's density. **Re-measure vocabulary after every syntax pass.**

Note the last two rows: he uses `however` and `consistent with` *more* than the polished
draft did. Polishing removed them. Not every difference points the same way.

---

## 6. Why the document was not rebuilt from the PDF

Attempting to reconstruct the flagged document from its PDF produced four different body
word counts (8,656 / 9,047 / 9,193 / 8,958) across four extraction passes. The text layer
had three defects:

1. **Page-break truncation** — paragraphs cut in two, tails landing on the next page
2. **Table text welded into paragraphs** — captions and `Notes:` lines became body prose,
   and two sentences separated by an entire table were joined end to end
3. **Display equations missing** — only the surrounding `where f denotes …` survived

Rewriting from that source would have written table notes into the body and deleted the
equations. The correct input is the author's original `.docx` — or, better, the `.tex`.

**Rule:** never rebuild a submission-ready document from a PDF text layer. Measure from it,
yes; regenerate from it, no.

---

## 7. The same document, measured twice

The LaTeX source arrived after the first pass. Re-running the *same instrument* on it gave
a different set of numbers — and this is the most useful thing in the file, because it
bounds how much a PDF-derived measurement can be trusted.

| | from the PDF | from the `.tex` | error |
|---|---|---|---|
| body words | 7,766 | **8,962** | +15.4% |
| sentences | 357 | **463** | +29.7% |
| sentence mean | 21.8 | **19.4** | −11.0% |
| sentence cv | 0.518 | **0.478** | −7.7% |
| `the` initial | 25.8% | **26.3%** | +1.9% |
| `this` initial | 6.2% | **5.4%** | −12.9% |
| prose semicolons | 16 | **18** | +12.5% |
| first person | 0 | **0** | 0 |

Read that carefully. The **direction of every tell survived**. The **magnitudes did not**:
sentences were undercounted by 30%, which inflated mean sentence length by 11% and
deflated `this`-initial by 13%. A report that said "cv 0.518 versus his 0.286" was
overstating the gap by 8%; one that said "357 sentences" was wrong by a third.

**Rule:** a rate with a wrong denominator is not a rough estimate, it is a different claim.
If the source exists, measure the source.

---

## 8. The tells are not spread evenly — they are concentrated

Per-section measurement of the same document is what makes the case actionable:

| section | words | `the` initial | `this` initial | prose semicolons |
|---|---|---|---|---|
| §1 Introduction | 966 | 25.0% | 12.5% | 1 |
| §2 Literature | 1,259 | **9.7%** | 6.5% | 2 |
| §3 Hypotheses | 618 | **12.8%** | 7.7% | 0 |
| §4 Data & Method | 2,531 | **33.1%** | **0.8%** | **13** |
| §5 Results | 2,011 | **35.7%** | 6.1% | 1 |
| §6 Discussion | 1,577 | 25.6% | 4.4% | 1 |

§2 and §3 already sit near the author's own 14.1% — those sections were barely touched.
§4 has `this` in **one sentence out of 118**, and 13 of the 18 semicolons. 82% of all
`The`-openers in the document are in §4–§6.

**So the work is not "rewrite the paper", it is "rewrite §4–§6".** Measuring per section
turned a 9,000-word job into a 6,000-word one, and told us where the damage actually was.

## 9. `this` density is not a constant — do not chase it

The same document ranges from **0.8%** `this`-initial (§4) to **25.0%** (§1.1). A
three-fold spread inside one author's one document means opener distribution tracks
**section function**, not personal identity. Taking 19.2% from a separate 1,440-word sample
and treating it as a target would have been over-fitting a short sample.

The defensible target is local: bring the outlier sections back into the band the author
uses *elsewhere in the same document*. After restoration §4 sits at 17.9% `the` / 16.4%
`this` and §5 at 20.2% / 21.1% — inside the band, not at a number pulled from elsewhere.

