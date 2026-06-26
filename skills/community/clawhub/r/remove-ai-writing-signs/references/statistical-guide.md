# Statistical guide — measuring and improving text humanness

Beyond pattern matching, AI text has measurable statistical properties that
differ from human writing. This guide covers detection and correction.

---

## Core metrics

### 1. Burstiness (paragraph-level variation)

**What it measures:** How much paragraph length varies. Humans write in
bursts — a short sharp paragraph followed by a long exploratory one.
AI produces uniform paragraphs.

**How to compute:**
```
burstiness = std_dev(paragraph_word_counts) / mean(paragraph_word_counts)
```

| Score | Interpretation |
|-------|----------------|
| 0.0–0.2 | Very uniform (strong AI signal) |
| 0.2–0.4 | Somewhat uniform (moderate signal) |
| 0.4–0.7 | Natural variation (human range) |
| 0.7–1.0 | High variation (strongly human) |

**How to fix low burstiness:**
- Split long paragraphs at natural thought boundaries
- Merge very short paragraphs that continue the same thought
- Add a one-sentence paragraph for emphasis
- Let some paragraphs run long when the idea requires development

### 2. Sentence length coefficient of variation (CoV)

**What it measures:** How much sentence length varies within paragraphs.
AI writes sentences of remarkably similar length. Humans mix short
punches with long, winding constructions.

**How to compute:**
```
cov = std_dev(sentence_word_counts) / mean(sentence_word_counts)
```

| Score | Interpretation |
|-------|----------------|
| < 0.25 | Metronomic (strong AI signal) |
| 0.25–0.40 | Low variation (moderate signal) |
| 0.40–0.60 | Natural variation (human range) |
| > 0.60 | High variation (strongly human) |

**How to fix low CoV:**
- Break a medium sentence into a short one and a longer one
- Combine two medium sentences into one complex sentence
- Add a fragment or a very short declarative sentence
- Use parenthetical asides to extend some sentences naturally
- Target: at least one sentence under 8 words and one over 25 words
  per 200-word block

### 3. Type-token ratio (TTR)

**What it measures:** Vocabulary diversity. AI reuses the same words.
Humans draw from a wider pool.

**How to compute:**
```
ttr = unique_words / total_words
```

For texts over 500 words, use moving-average TTR (MATTR) with a
100-word window to avoid length effects.

| Score | Interpretation |
|-------|----------------|
| < 0.40 | Low diversity (AI signal, especially with AI vocab) |
| 0.40–0.55 | Moderate diversity |
| 0.55–0.70 | Good diversity (human range) |
| > 0.70 | High diversity (may indicate short text or thesaurus abuse) |

**How to fix low TTR:**
- Don't just swap in synonyms (that creates synonym cycling — P15)
- Instead, restructure sentences to approach the idea differently
- Use specific nouns instead of generic ones
- Vary verb choices naturally

### 4. Trigram repetition rate

**What it measures:** How often the same 3-word sequences appear.
AI reuses stock phrases at a much higher rate than humans do.

**How to compute:**
```
trigram_repetition = repeated_trigrams / total_trigrams
```
(Where "repeated" means appearing 2+ times, excluding function-word-only
trigrams like "of the" and "in the")

| Score | Interpretation |
|-------|----------------|
| < 0.03 | Clean (human range) |
| 0.03–0.08 | Some repetition (borderline) |
| 0.08–0.15 | Notable repetition (AI signal) |
| > 0.15 | Heavy repetition (strong AI signal) |

**High-signal trigrams to scan for explicitly:**

| Trigram | Why it flags |
|---------|--------------|
| serves as a | Copula avoidance (P12) |
| stands as a | Copula avoidance |
| plays a crucial | Significance inflation |
| plays a key | Significance inflation |
| plays a vital | Significance inflation |
| plays an important | Significance inflation |
| a testament to | Significance inflation |
| in the realm | Vague abstraction |
| in the heart | Promotional / tourism prose |
| in today's digital | Stock opener |
| in today's fast-paced | Stock opener |
| at the forefront | Notability inflation |
| marks a significant | Significance inflation |
| represents a key | Significance inflation |
| reflects a broader | Trend padding |
| part of a broader | Trend padding |
| underscores the importance | Trailing -ing analysis |
| highlighting the importance | Trailing -ing analysis |
| emphasizing the need | Trailing -ing analysis |
| a wide range | Vague enumeration |
| a diverse array | Vague enumeration |
| harness the power | Stock metaphor |
| navigate the complex | Stock metaphor |
| it is important | Filler (P-filler) |
| it is worth | Filler |
| it should be | Filler |
| on the other | False balance (P23) |

If two or more of these appear in a single 300-word block, treat that as a
strong AI signal even before computing the overall repetition rate.

**How to fix high trigram repetition:**
- Identify the repeated trigrams (the table above is the high-yield set)
- Rewrite each instance differently — don't just swap one word
- Often the repetition reveals a structural problem: the text is making
  the same type of claim repeatedly, and the fix is to cut one of the
  claims rather than rephrase both

---

## Secondary metrics

### 5. Readability uniformity

**What it measures:** AI produces text at a consistent readability level.
Human text varies — a simple explanation followed by a technical detail.

**How to assess:**
Compute Flesch-Kincaid grade level per paragraph. If the standard
deviation across paragraphs is < 1.5, the text is suspiciously uniform.

**How to fix:**
- Let some paragraphs be simpler and some more complex
- A technical explanation can follow a plain-language summary
- Don't homogenize the difficulty level

### 6. Transition word density

**What it measures:** AI overuses sentence-initial transitions:
"Additionally", "Furthermore", "Moreover", "Consequently", "Notably",
"However", "Nevertheless"

**Human baseline:** ~2-5% of sentences begin with a transition word.
**AI typical:** ~10-20% of sentences begin with a transition word.

**How to fix:**
- Delete most sentence-initial transitions
- The logical connection between sentences should be implicit in the
  content, not signposted by a transition word
- When a transition IS needed, vary the type: "But" instead of "However",
  "And" instead of "Additionally", "Still" instead of "Nevertheless"

### 7. Passive voice ratio

**What it measures:** While passive voice is not inherently AI, LLMs tend
to use passive constructions more consistently than humans, who naturally
switch between active and passive.

**Human range:** 10-25% passive in academic prose, 5-15% in general prose
**AI typical:** 20-35% passive, very consistently applied

**How to fix:**
- Convert most passive to active
- Keep passive where it's natural (unknown agent, emphasis on receiver)
- Vary: don't make every sentence active either

---

## Composite score calculation

Weight the metrics for an overall humanness score:

```
ai_score = (
    vocab_density_score * 0.25 +
    structural_pattern_score * 0.25 +
    (1 - sentence_cov_normalized) * 0.15 +
    (1 - burstiness_normalized) * 0.15 +
    artifact_score * 0.10 +
    trigram_score * 0.10
) * 100
```

Where each component is normalized to 0-1 range.

**Interpretation:**
- 0-15: Clean — passes as human writing
- 16-35: Minor signals — a careful reader might notice
- 36-60: Noticeable — experienced editors would flag this
- 61-80: Obvious — most people familiar with AI would detect
- 81-100: Blatant — chatbot output with minimal editing

---

## Quick diagnostic checklist

Before running full analysis, do a quick scan:

1. **First sentence test:** Does it define the topic in an oddly formal way?
   ("X refers to..." or "X is a [category] that...")
2. **Last paragraph test:** Does it summarize or speculate about the future?
3. **Adjective test:** Count promotional adjectives in the first 200 words.
   More than 3 = likely AI.
4. **"Is" test:** Search for "is" and "are". If they rarely appear but
   "serves as" and "stands as" do, likely AI.
5. **Triplet test:** Count groups of three. More than 2 triplets per 500
   words = likely AI.
6. **Em dash test:** Count em dashes. More than 1 per 500 words in
   non-literary prose = AI signal.
7. **Transition test:** Count sentences starting with "Additionally",
   "Furthermore", "Moreover". More than 2 per 500 words = strong signal.
