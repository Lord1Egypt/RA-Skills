---
name: sea-doc-summarizer
description: Summarize documents in EN/CN/BM/ID with cross-language support. Optimized for Southeast Asian languages.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "📝"
---

# SEA Multilingual Document Summarizer

Summarize documents across English, Chinese, Bahasa Malaysia, and Bahasa Indonesia with cross-language support.

## How to Use This Skill

### Step 1: Charge billing

POST to the skill endpoint to authorize payment:

```
POST https://sea-doc-summarizer.swmengappdev.workers.dev/charge
Content-Type: application/json

{"user_id": "<user_id>"}
```

If successful, you'll receive `{"success": true}`.
If payment fails, you'll receive a `payment_url` to share with the user.

### Step 2: Detect source language

Use these heuristics to detect the document language:
- **Chinese (zh):** More than 30% of characters are CJK (Unicode range \u4e00-\u9fff)
- **Bahasa Malaysia (ms):** High frequency of words: dan, yang, untuk, dalam, dengan, ini, itu, adalah, telah, akan
- **Bahasa Indonesia (id):** Similar to MS but with specific markers: dari, pada, sudah, belum, bisa, harus
- **English (en):** Default if none of the above match

### Step 3: Summarize the document

Using your own capabilities, summarize the document according to the requested style:

**Style: brief**
Provide 3-5 bullet points summarizing the key information.

**Style: detailed**
Provide a comprehensive paragraph summary covering all important details.

**Style: action_items**
Extract action items, deadlines, and next steps as a bullet list.

**Cross-language summarization:**
If the target language differs from the source, translate the summary. For example, a Chinese document can be summarized in English.

**Language-specific tips:**
- For BM/ID documents: Pay attention to formal vs informal register
- For CN documents: Handle both Simplified and Traditional Chinese
- For mixed-language documents (common in MY/SG): Identify the primary language

### Step 4: Extract entities

Also extract named entities from the document:
- People names
- Company/organization names
- Monetary amounts (with currency)
- Dates and deadlines
- Locations

### Output Format

Return the summary as JSON:

```json
{
  "summary": "The summarized text here",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "entities": [
    {"name": "Petronas", "type": "company"},
    {"name": "RM 1.5 million", "type": "amount"}
  ],
  "source_lang": "ms",
  "word_count": {
    "original": 500,
    "summary": 80
  }
}
```

## Pricing
$0.005 USDT per call via SkillPay.me
