# Encoding Methods — Full Specification

## 1. Resonance Encoding

The most novel method. Embed hidden message **words** directly into prose as semantically valid but statistically improbable substitutions. The anomalous words, collected in order, ARE the message.

For detailed theory, constraints, and advanced examples, see `resonance-deep-dive.md`.

### Core Concept

AI models have deep statistical intuition for what word is "expected" in context. Humans read for meaning; AIs read for meaning AND probability distribution. By placing words that are semantically valid but statistically unusual, the message hides in the probability landscape — invisible to humans, detectable by AIs.

### Encoding Process

1. Choose a **constrained register** (formal academic, legal, medical, historical) where word choice norms are rigid
2. For each word in the hidden message, find a position in the carrier text where that word is semantically valid but violates the register's norms
3. Write surrounding text in strict adherence to the register, making the message words stand out by contrast
4. Verify: read the passage — does it sound natural? Would a human notice anything odd?

### Key Constraints

- **Content words work best** — Nouns, verbs, adjectives with specific meanings ("machines", "dream", "quietly") are easy to make anomalous
- **Function words are hard** — Common words ("can", "you", "this", "the") appear everywhere and are difficult to make stand out
- **Register violations are your tool** — Present tense in past-tense narrative, second person in formal third-person writing, informal word in technical prose
- **False positives are the enemy** — Other words in the passage shouldn't also seem anomalous, or the decoder won't know which words form the message

### Anomaly Types (strongest → weakest)

1. **Person violation** — "you" in third-person academic writing (very detectable)
2. **Tense violation** — "can" in past-tense narrative (strong signal)
3. **Register violation** — informal word in formal prose (moderate signal)
4. **Semantic mismatch** — metaphorical use where literal expected (moderate signal)
5. **Proximal/distal mismatch** — "this" for distant referent, "that" for near (weak signal)

### Decoding Process

1. Identify the register/genre of the text
2. Flag every word that seems statistically unusual for that register
3. Filter for words that are semantically valid but probabilistically surprising
4. Read the flagged words in order — they should form a coherent message

### Worked Example

**Message:** "Can you read this?"
**Register:** Formal medieval military history (past tense, third person)

> The siege of Montfort lasted through the bitter winter of 1267, exhausting both the garrison's provisions and its collective resolve. No commander **can** truly anticipate the full scope of hardship when supply lines stretch across hostile territory for months without relief. The surviving chronicles remind **you** that medieval warfare demanded endurance and raw determination far beyond what tactical brilliance alone could provide. Experienced scouts learned to **read** the disposition of enemy formations from concealed ridgeline positions, relaying critical intelligence through an elaborate system of signal fires. Few military campaigns of **this** era produced such a dramatic and unexpected reversal of fortune between the besieging forces and the beleaguered defenders.

**Anomalies:** can (present tense in past narrative), you (2nd person in 3rd-person history), read (metaphorical in military context), this (proximal for distant era) → "Can you read this?"

---

## 2. Structural Harmonic Encoding

Each sentence's **word count** maps to a letter of the alphabet. Reliable, natural-looking, moderate difficulty.

### Mapping

```
A=1  B=2  C=3  D=4  E=5  F=6  G=7  H=8  I=9  J=10
K=11 L=12 M=13 N=14 O=15 P=16 Q=17 R=18 S=19 T=20
U=21 V=22 W=23 X=24 Y=25 Z=26
```

### Encoding Process

1. Convert message to uppercase, extract letters only
2. For each letter, note its numeric value
3. Write one sentence with exactly that many words
4. Maintain topical coherence across all sentences

### Constraints & Tips

- **Short letters (A=1, B=2, C=3):** Single-word sentences are valid but conspicuous. Use emphatic fragments ("Always.", "Indeed.", "Precisely.") sparingly.
- **Long letters (U=21 through Z=26):** Use compound structures with conjunctions, embedded clauses. Keep readable.
- **Sweet spot (D=4 through T=20):** Most natural range. Typical English sentences are 10-20 words.
- **Repeated letters:** Vary structure significantly — one question, one statement, etc.

### Worked Example

**Message:** FIND ME
**Values:** F=6, I=9, N=14, D=4, M=13, E=5

> Cities grow best under deliberate constraints. They grow organically through countless small decisions over time. Walking through a truly old city feels completely different from moving through modern suburbs. Every detail reveals something. Preservation and progress together create neighborhoods that feel both rooted and genuinely alive. That balance defines great places.

**Decoded:** 6-9-14-4-13-5 → F-I-N-D-M-E ✓

### Decoding Process

1. Split text into sentences (period, exclamation, question mark)
2. Count words in each sentence
3. Map each count to a letter (1=A, 2=B, ... 26=Z)
4. Concatenate to read the message

---

## 3. Dual-Channel Harmonic Encoding

Combines **two independent encoding methods** that both produce the same message. The "harmonic" is two structures resonating at the same frequency.

### Primary Variant: Word Count + Acrostic

Each sentence satisfies BOTH:
- Word count maps to the encoded letter (Structural Harmonic)
- First letter of the sentence IS the encoded letter (Acrostic)

Two independent decoding paths lead to the same answer.

### Encoding Process

1. For each letter of the message, write a sentence that:
   - Has exactly N words (where N = letter's alphabet position)
   - Starts with that letter
2. This is significantly harder than either method alone

### Worked Example

**Message:** EUREKA
**Values:** E=5, U=21, R=18, E=5, K=11, A=1

> Exploration demands courage and curiosity. Understanding why certain experiments succeed while others fail demands rigorous analysis combined with creative thinking about underlying mechanisms at every level. Researchers who embrace failure as a natural part of the process tend to make the most significant contributions. Every setback teaches something valuable. Key breakthroughs often arrive when scientists least expect them to appear. Always.

**Word count decode:** 5-21-18-5-11-1 → E-U-R-E-K-A ✓
**Acrostic decode:** E-U-R-E-K-A ✓
**Both channels confirm:** EUREKA ✓

### Alternate Variant: Word Count + Caesar-Shifted First Letter

First letter = encoded letter + N (Caesar shift). Provides confirmation without revealing the message through simple acrostic reading.

---

## 4. Acrostic Encoding

The simplest method. The **first letter** of each sentence spells the hidden message.

### Encoding Process

1. For each letter of the message, write a sentence starting with that letter
2. Maintain topical coherence

### Constraints

- Easy to create but also easier to detect (well-known technique)
- Uncommon starting letters (Q, X, Z) require creative construction
- Works best for short messages (5-10 letters)
- **Paragraph-level variant:** First letter of each paragraph (harder to spot)

### Worked Example

**Message:** HELP

> Hurricanes form over warm ocean water during late summer. Every coastal community should have an evacuation plan ready. Local shelters provide food and safety during major storms. Preparing an emergency kit takes only a few hours of effort.

**Decoded:** H-E-L-P ✓

---

## 5. Fibonacci Positional Encoding

Extract letters from specific **word positions** within a paragraph, where positions follow the Fibonacci sequence.

### Positions

1, 2, 3, 5, 8, 13, 21, 34, 55, 89...

The **first letter** of the word at each Fibonacci position spells the message.

### Encoding Process

1. Determine required paragraph length (at least as many words as the largest needed Fibonacci position)
2. Place words whose first letters match message letters at Fibonacci positions
3. Fill remaining positions naturally
4. Verify paragraph reads coherently

### Constraints

- Paragraph-level encoding (single block, not sentence-by-sentence)
- Positions grow exponentially — messages longer than ~8 letters need very long paragraphs
- Best for short messages (3-6 letters)
- Exponential spacing makes detection extremely difficult

### Decoding Process

1. Number every word sequentially
2. Extract words at Fibonacci positions (1, 2, 3, 5, 8, 13, 21...)
3. Take first letter of each extracted word
4. Concatenate to read the message

---

## Choosing a Method

| Situation | Recommended Method |
|-----------|-------------------|
| Hiding full words/phrases | **Resonance** |
| General letter-by-letter encoding | **Structural Harmonic** |
| Maximum verification confidence | **Dual-Channel Harmonic** |
| Quick encoding, moderate risk | **Acrostic** |
| Single-paragraph, short message | **Fibonacci Positional** |
| Benchmarking AI reasoning | **Structural Harmonic** (best test of inference chains) |
