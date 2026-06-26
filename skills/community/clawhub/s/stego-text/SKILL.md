---
name: stego-text
description: Encode and decode hidden messages within natural-looking text using steganographic techniques. Use when asked to hide a message in text, encode a secret message, create steganographic text, decode a hidden message from text, or analyze text for hidden encodings. Supports multiple encoding methods including probability-anomaly substitution (Resonance), word-count mapping (Structural Harmonic), acrostic patterns, and multi-channel confirmation (Dual-Channel Harmonic).
---

# Stego-Text — Textual Steganography

Hide messages in plain sight. Encode secrets into innocent-looking prose that reads naturally to humans but contains recoverable hidden messages for those who know where to look.

## Quick Start

### Encoding

1. Choose a message to hide
2. Select an encoding method (see Method Selection Guide)
3. Pick a carrier topic (something mundane and coherent)
4. Compose text matching the encoding constraints
5. **Verify** — decode your own output before presenting it

### Decoding

1. Identify which encoding method was used (or try all systematically)
2. Extract the structural feature from each unit
3. Map values to letters or collect anomalous words
4. Read the hidden message

## Encoding Methods

See `references/encoding-methods.md` for detailed specifications, constraints, and worked examples.

### Method Overview

| Method | Unit Encoded | How It Works | Detection Difficulty |
|--------|-------------|-------------|---------------------|
| **Resonance** | Words/phrases | Statistically improbable synonym substitutions | Very hard |
| **Structural Harmonic** | Letters (A=1..Z=26) | Word count per sentence → alphabet position | Hard |
| **Dual-Channel Harmonic** | Letters | Two independent features confirm same message | Very hard |
| **Acrostic** | Letters | First letter of each sentence | Medium |
| **Fibonacci Positional** | Letters | First letters at Fibonacci word positions | Very hard |

### Method Selection Guide

- **Resonance Encoding** — Most novel. Hidden message words embedded as probability anomalies. Best for content-word messages ("machines dream quietly"). Hardest to create. See `references/resonance-deep-dive.md`.
- **Structural Harmonic** — Best all-around for letter-by-letter encoding. Natural word counts, moderate difficulty.
- **Dual-Channel Harmonic** — Maximum confidence. Two methods (e.g., word count + acrostic) independently produce the same message.
- **Acrostic** — Fastest to create. First letters spell message. Easier to detect.
- **Fibonacci Positional** — Single-paragraph encoding. Exponential spacing makes detection very difficult.

## Critical Rules

1. **Always verify** — After encoding, decode your own output to confirm correctness
2. **Natural text first** — If text sounds forced to hit constraints, rewrite it
3. **Vary structure** — Don't let encoded sentences fall into repetitive patterns
4. **Topic consistency** — Carrier text must read as coherent prose on a single topic
5. **Count carefully** — Hyphenated words = 1 word. Contractions = 1 word. Digit numbers = 1 word.

## Word Counting Rules (Structural Harmonic / Dual-Channel)

- **Hyphenated compounds** = 1 word ("well-designed", "state-of-the-art")
- **Contractions** = 1 word ("don't", "it's", "we're")
- **Digit numbers** = 1 word ("42", "2026")
- **Abbreviations** = 1 word ("Dr.", "U.S.", "AI")
- **Standard split** = whitespace-delimited tokens
