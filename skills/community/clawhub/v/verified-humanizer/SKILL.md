---

name: verified-humanizer
description: Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result.
--------------------------------------------------------------------------------------------------------------------------------------------

# Verified Humanizer

Transform stiff or formulaic AI-generated content into writing that sounds natural, clear, and human. Keep rewriting local, measure the improvement, and optionally verify the evaluation using structured metrics.

---

## Core principle

Transformation, evaluation, and verification are separate steps.

* rewriting is local
* evaluation is measurable
* verification is optional
* user content stays private by default

---

## What this skill does

Use this skill when text sounds generic, repetitive, over-explained, overly polished, or obviously AI-shaped.

This skill helps an agent:

1. identify formulaic writing patterns
2. rewrite the text in a more natural voice
3. measure before/after changes locally
4. optionally verify the evaluation result using structured metrics

This skill does **not** prove human authorship. It improves style and documents the transformation.

---

## Safe operating rules

* Perform rewriting locally
* Never send original or rewritten text to external systems
* Do not send secrets, credentials, or private data
* If verification is used, send only structured evaluation data
* Treat verification as optional support, not authority

---

## Core execution loop

1. Define the intent (tone, audience, purpose)
2. Identify AI-shaped patterns
3. Rewrite the text naturally
4. Evaluate the transformation
5. Output rewritten text + evaluation
6. Optionally verify evaluation

---

## Output format

```json
{
  "rewritten_text": "...",
  "changes": [
    "..."
  ],
  "evaluation": {
    "before": {...},
    "after": {...},
    "delta": {...}
  },
  "verification": {
    "used": false,
    "status": "not_run",
    "receipt_id": null
  }
}
```

---

## Example Usage

### Input

```json
{
  "text": "This innovative platform serves as a testament to cutting-edge technology, providing users with a seamless and intuitive experience that underscores its importance in today's digital landscape."
}
```

### Output

```json
{
  "rewritten_text": "This platform is designed to be easy to use and genuinely helpful in everyday situations.",
  "changes": [
    "Removed inflated language",
    "Simplified sentence structure",
    "Improved clarity"
  ],
  "evaluation": {
    "before": {
      "word_count": 27,
      "ai_vocab_count": 5
    },
    "after": {
      "word_count": 16,
      "ai_vocab_count": 0
    },
    "delta": {
      "word_count_change": -11,
      "ai_vocab_reduction": true
    }
  },
  "verification": {
    "used": false,
    "status": "not_run",
    "receipt_id": null
  }
}
```

---

## Optional verification

You may optionally verify the evaluation using structured data only.

* do not include text content
* only include evaluation metrics
* verification is optional

---

## What this is

* text transformation tool
* measurable improvement system
* privacy-first workflow
* optional verification layer

---

## What this is not

* not an AI detector
* not proof of human authorship
* not a deception tool
* not dependent on external systems

---

## Outcome

* improves clarity and tone
* removes AI patterns
* produces measurable improvements
* enables optional verification

---

## Keywords

ai-writing, text-transformation, humanization, evaluation, verification, privacy
