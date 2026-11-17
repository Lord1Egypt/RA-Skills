# voice-restore

**Find out whether a text was AI-touched — then put the author's own voice back.**

Not "humanize". Humanizing optimises for *reads like a person*. This optimises for
*reads like **this** person*. On real corpora those two goals conflict, and when they
do, this skill sides with the author.

---

## Why the obvious approach is wrong

Every "reduce AI detection" guide says the same thing: vary sentence length, add short
sentences, insert personal voice. That advice assumes the target is a generic human.

It isn't. Take one measured case — an 8,962-word finance thesis flagged at 46%:

| | the thesis (flagged 46%) | the same author's undetected earlier essay |
|---|---|---|
| sentence-length cv | **0.478** | **0.286** |
| article-initial sentences | 37.1% | **41.0%** |
| short sentences (≤10w) | 15% | 6% |

The flagged document is **more varied** than the author's own writing, and uses **fewer**
article-initial sentences. By the standard burstiness playbook, it was already "more human"
than he is.

So the playbook would have made it worse. What it needed was the opposite: flatten it
toward *his* distribution.

> ⛔ Shape metrics measure **how smoothed a text is**, not **whether a model wrote it**.
> A writer with imperfect English is flat by default. Flat is his fingerprint, not his crime.

---

## What actually survives AI editing

Three things, and they are cheap to count:

| Tell | What it looks like | Why it's hard to explain away |
|---|---|---|
| **First person = 0** | 8,962 words, not one `I / we / us / our / my` | Nobody writes their own thesis without once saying `remind us` |
| **Prose semicolons appear** | author's own writing: **0** in 3,371 words; polished draft: **18** | Semicolons weld two independent sentences together — that is an *editing* move, not a *drafting* move |
| **`The` up, `This` down** | author: `The` 14.1% / `This` 19.2%; draft: `The` 26.3% / `This` 5.4% | He delegates anaphora to `This`. The polish pass rewrote every one as `The` |

The judgement is not "exceeds threshold → AI". It is **the three being mutually
inconsistent**. A writer can avoid first person (disciplinary norm), or love semicolons
(personal style) — but not all three at once, because those habits belong to different
stages of writing.

Corroborating evidence in the other direction matters too. In the same case, the sample
construction numbers were internally consistent across four deletion stages, the
introduction kept the author's own opener distribution, and the AI-word list scored
**lower** than his own writing. That is the shape of *"the human did the analysis, a
model polished the sentences"* — not wholesale generation.

---

## What it does

```
Phase 1  forensics   count the three tells; check the counter-evidence
Phase 2  baseline    measure the author's own undetected samples
Phase 3  restore     syntax layer → vocabulary layer → verify against baseline
```

**Phase 3 is ordered, and the order is not cosmetic.**

1. **Syntax** — `The X…` → `This …`; split prose semicolons; restore `us` (not `I`);
   break 60-word sentences at argument joints.
2. **Vocabulary** — re-measure *after* syntax. Rebuilding sentences tempts you to add
   connectives, and that is how `therefore` ends up at 2.3× the author's density.
3. **Verify** — against the baseline, not against an ideal. Anything still off gets
   reported as off.

One real restoration, measured from the author's LaTeX source, every number preserved:

| | author | §4 before | §4 after | §5 before | §5 after |
|---|---|---|---|---|---|
| sentence mean | 18.5 | 21.4 | **18.1** | 20.5 | **18.4** |
| sentence cv | 0.286 | 0.479 | 0.459 | 0.448 | **0.353** |
| `The` initial | 14.1% | 33.1% | **17.9%** | 35.7% | **20.2%** |
| `This` initial | 19.2% | 0.8% | **16.4%** | 6.1% | **21.1%** |
| prose semicolons | 0 | 13 | **0** | 1 | **0** |
| first person | 3 | 0 | **1** | 0 | **1** |

The tells were concentrated, not spread: §2 and §3 of the same document already sat at
`The` 9.7% and 12.8%, so they were left alone. §4 held `This` in **one sentence out of
118**. Measuring per section is what turned this into a six-thousand-word job instead of
a nine-thousand-word one.

---

## Install

```bash
npx skills add CatsMansion/voice-restore

# or
cp -r voice-restore ~/.claude/skills/
```

## Usage

```bash
# what does this author actually sound like?
python scripts/voice_metrics.py report old_essay.txt

# how far has the draft drifted?
python scripts/voice_metrics.py compare old_essay.txt draft.txt
```

Stdlib only, Python 3.8+. No network, no dependencies.

⚠️ Rates per 1,000 words are unstable below ~800 words — the script says so when it applies.

---

## Design notes

**Sentence splitting is the whole ballgame.** An early version used
`re.split(r'(?<=[.!?])\s+')` and shredded `Smith et al. (2012), de Jong et al. (2011)`
into three "sentences" of 3, 4 and 18 words. Sentence-length mean, cv and short-ratio
were all fabricated. The splitter here protects abbreviations and decimals, because
every number downstream depends on it.

**Counting punctuation requires knowing where it lives.** The semicolon tell was first
reported as 24. Filtering table footnotes (`Notes: … ; …`) and citation separators inside
parentheses brought it to 16 — and the LaTeX source later said 18. So the first number was
too high by a third and the second too low by two. Both mistakes had the same shape: the
count was taken over the wrong span of text, and nothing in the number said so.

**The instrument failed three times before it was right.** Each failure was the same
family: *a metric that looked reasonable and measured the wrong thing*. The fix each
time was to print intermediate values rather than re-read the code.

---

## Scope

This is a forensic and editorial tool for **text you wrote yourself** and are allowed to
edit. It is not a detector-bypass guarantee: detectors change, and no local measurement
predicts a hosted classifier. If a submission requires disclosing AI assistance, disclose
it — this skill helps you restore your own voice on top of that, not avoid the disclosure.

## License

MIT
