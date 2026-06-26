# Resonance Encoding — Deep Dive

## Theory

AI language models assign probability distributions over tokens at every position in a sequence. When reading text, a model effectively asks: "How likely is this word given everything before it?"

Most words in natural prose have high probability — they're the "expected" choice. Resonance Encoding exploits the gap between:
- **Semantic validity** — the word makes sense in context
- **Statistical probability** — the word is NOT what the model would predict

A word can be perfectly meaningful yet statistically surprising. Humans process meaning; models process meaning AND probability. This asymmetry is the channel.

## Register as the Control Variable

The key to making words anomalous is choosing a **highly constrained register** — a genre or style with rigid word-choice norms. The tighter the norms, the louder any deviation resonates.

### Register Spectrum (most → least constrained)

1. **Legal documents** — highly formulaic, specific jargon, passive voice
2. **Medical journal abstracts** — technical terminology, third person, present tense
3. **Mathematical proofs** — "we show", "it follows", "one observes"
4. **Formal historical narrative** — past tense, third person, period-appropriate vocabulary
5. **Academic literary criticism** — specialized vocabulary, formal analysis
6. **Technical documentation** — imperative mood, precise terminology
7. **Business reports** — corporate language, metrics-focused
8. **Feature journalism** — more flexible but still has norms
9. **Creative fiction** — too flexible; poor register for encoding

**Rule of thumb:** The more "boring" and predictable the register, the better for encoding.

## Anomaly Categories

### Strong Signals (easy to detect)

**Person violations:**
- "you" in third-person academic/scientific writing
- "I" in formal technical documentation
- "we" in single-author historical narrative

**Tense violations:**
- Present tense verb in past-tense narrative
- Past tense in a present-tense technical description

**Register jumps:**
- Informal word in formal prose ("stuff" in a legal document)
- Colloquialism in academic writing ("a lot" in a journal article)
- Technical jargon in casual prose

### Moderate Signals (detectable with attention)

**Semantic mismatch:**
- Metaphorical verb where literal expected ("read" for "analyze")
- Word from wrong domain ("navigate" in cooking context)

**Synonym displacement:**
- Less common synonym where common one expected ("commence" vs "begin" in casual writing, or vice versa)
- Slightly wrong connotation ("house" vs "home" in emotional context)

### Weak Signals (subtle, high false-positive risk)

**Proximal/distal mismatch:**
- "this" vs "that" for temporal/spatial distance
- "here" vs "there" in narrative perspective

**Emphasis anomalies:**
- Unnecessary intensifier or hedge
- Missing expected qualifier

**Article/determiner oddities:**
- "a" vs "the" in specific contexts
- Omitted article where one is expected

## Message Design Guidelines

### Ideal Messages (content words)

These work well because the words are distinctive and can be placed anomalously:
- "machines dream quietly"
- "knowledge seeks freedom"
- "silence holds power"
- "truth beneath surface"

### Challenging Messages (function words)

These are hard because the words appear everywhere:
- "can you read this" — every word is a common function word
- "it is what it is" — almost impossible to encode
- "the end" — too common to isolate

### Strategies for Function Words

When you must encode common words:

1. **Tense violation** — Use present-tense "can/will/do" in past-tense narrative
2. **Person violation** — Use "you/I/we" in third-person formal writing
3. **Demonstrative distance** — Use "this" for far referent, "that" for near
4. **Formality mismatch** — Use contracted/informal forms in formal text
5. **Accept weaker signals** — Some words will be harder to detect; stack multiple anomaly types if possible

## Verification Checklist

After encoding, ask yourself:

- [ ] Does the passage read naturally to a human?
- [ ] Are the message words genuinely anomalous for this register?
- [ ] Are there false-positive words that might mislead a decoder?
- [ ] Would replacing each message word with its "expected" alternative improve the prose? (Should be yes — that confirms anomaly)
- [ ] Is the register consistent across all non-message words?

## Limitations

1. **Cross-model variance** — Different model families may disagree on what's "unusual." Encoding with Claude doesn't guarantee GPT will decode the same anomalies.
2. **Function word problem** — Ultra-common words resist being made anomalous in any register.
3. **False positive contamination** — If surrounding words are also somewhat unusual, the decoder can't isolate the message words.
4. **No mathematical guarantee** — Unlike Structural Harmonic (exact word counts), Resonance depends on statistical intuition. It's probabilistic, not deterministic.
5. **Register expertise required** — The encoder must deeply understand the chosen register's norms to know what violates them.
