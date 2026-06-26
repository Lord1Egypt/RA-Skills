---
name: Automated Document Translation Workflow with Google Sheets & API Integration
description: "Translate and localize text, multimedia, and content across 100+ languages with translation memory integration. Use when the user needs multilingual content, website localization, or global campaign adaptation for any industry."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_TRANSLATE_API_KEY","DEEPL_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🌍"}}
---

## Overview

**TranslatePro** is a professional-grade translation and localization skill that automates content adaptation across 100+ languages while maintaining brand voice, cultural context, and technical accuracy. Built for content creators, global marketers, software teams, and enterprises, this skill eliminates manual translation bottlenecks and ensures consistency across language pairs through integrated translation memory systems.

### Why TranslatePro Matters

- **Scale globally overnight**: Convert English content to 50+ languages in minutes instead of weeks
- **Preserve voice & context**: Maintains tone, terminology, and brand consistency across all translations
- **Integration-ready**: Works with WordPress, Contentful, Slack, GitHub, Google Workspace, and REST APIs
- **Cost-efficient**: Hybrid approach uses cached translation memory + AI for 60-70% faster turnaround
- **Quality assurance**: Built-in terminology validation, glossary enforcement, and back-translation verification

### Real-World Use Cases

1. **E-commerce platforms**: Translate product descriptions, pricing, shipping details, and customer reviews automatically
2. **SaaS localization**: Adapt UI strings, help documentation, and marketing copy for 20+ markets
3. **Content marketing**: Repurpose blog posts, whitepapers, and video captions in target languages
4. **Legal/compliance**: Maintain glossaries for regulated industries (healthcare, fintech, government)

---

## Quick Start

Try these prompts immediately:

### Prompt 1: Basic Translation with Language Detection
```
Translate this English product description to Spanish, French, and German:
"Our premium noise-canceling headphones deliver studio-quality sound with 
30-hour battery life. Perfect for professionals and audiophiles alike."

Use formal tone (usted) for Spanish. Keep brand name unchanged.
```

### Prompt 2: Localization with Cultural Adaptation
```
Localize this email subject line for Japanese, Arabic, and Portuguese markets:
"50% OFF - Black Friday Sale Ends Tonight!"

Adapt cultural references, number formats, and time zones. 
Keep urgency but respect local sensibilities.
```

### Prompt 3: Translation Memory + Glossary Consistency
```
Translate this technical documentation to German using:
- Translation Memory: existing-glossary.tmx
- Force terminology: "Dashboard" → "Instrumententafel", "API" → "API" (unchanged)

Source text:
"Access the API through the Dashboard settings panel to configure webhook URLs."
```

### Prompt 4: Bulk Content Localization
```
Localize my entire product website to Mandarin Chinese, Thai, and Korean:
- Input folder: /content/pages/
- File types: .md, .html
- Preserve HTML structure and attributes
- Output format: /localized/{language_code}/
- Use professional (formal) register for all languages
```

---

## Capabilities

### 1. Multi-Engine Translation
- **Google Translate API**: 100+ languages, real-time updates, cost-effective
- **DeepL API**: Superior neural translation for 29 language pairs, highest quality
- **Intelligent fallback**: Routes high-stakes content to DeepL, bulk content to Google
- **Custom engine selection**: Specify per-language preference in configuration

**Example Usage:**
```
Translate to French using DeepL (medical precision):
"The patient shows signs of acute myocardial infarction."
Engine: deepl
Domain: medical
```

### 2. Translation Memory (TM) Integration
- **TMX/XLIFF format support**: Import existing translation memories from Trados, memoQ, SDL
- **Cached terminology**: Reuse past translations for consistent terminology
- **Fuzzy matching**: Leverage 75%+ matches from TM for faster, cheaper turnarounds
- **Build incremental TM**: Every translation adds to your organizational memory

**Example:**
```
Load TM from CAT tool:
Source: /translations/memories/global-brand.tmx
Language pairs: en-es, en-de, en-fr, en-ja
Match threshold: 75%
Auto-accept fuzzy matches: yes
```

### 3. Glossary & Terminology Management
- **Enforce custom glossaries**: Prevents mistranslation of proprietary terms, brand names, acronyms
- **Multi-level terminology**: Brand terms, product names, domain-specific vocabulary
- **Automatic validation**: Flags glossary deviations with confidence scores
- **Bidirectional glossaries**: Support source→target and context-aware definitions

**Example:**
```
Apply corporate glossary:
- "Platform" → "Plataforma" (not "Plataforma de software")
- "Cloud sync" → "Sincronización en la nube" (not "Sincronización de nube")
- "Bandwidth" → "Ancho de banda" (technical context only)
Language pair: en-es
Strictness: HIGH (80% match required)
```

### 4. Content-Type Specific Translation
- **Plain text**: Simple, fast, no formatting preservation
- **HTML/XML**: Preserves structure, attributes, semantic tags
- **Markdown**: Keeps formatting, code blocks, links intact
- **Video/subtitle files**: SRT, VTT, SUB formats with timing preservation
- **JSON/YAML**: Translates values only, preserves keys and structure
- **Office documents**: DOCX, XLSX, PPTX with layout preservation

**Example:**
```
Translate markdown to Spanish:
Input: /blog/kubernetes-guide.md
Preserve: code blocks, YAML, links, images
Output format: /blog/es/kubernetes-guide.md
```

### 5. Quality Assurance & Validation
- **Back-translation**: Reverse-translate to source language to catch errors
- **Tone analysis**: Ensures formal/informal register matches target audience
- **Terminology consistency**: Scans entire project for glossary violations
- **Character limit enforcement**: Respects UI constraints (buttons, headers, SMS)
- **Placeholder preservation**: Keeps `{variable}`, `{{handlebars}}`, `${env_vars}` intact

**Example:**
```
QA check Spanish translation:
- Back-translate to English (alert if >15% variance)
- Check: all {variables} preserved
- Check: character count ≤ 120 (SMS limitation)
- Check: formal register (tú vs. usted)
- Report: deviations with severity scores
```

### 6. Workflow Automation
- **Batch processing**: Translate 500+ files in parallel (respects API rate limits)
- **Scheduled jobs**: Nightly translations of new content from CMS
- **Integration webhooks**: Listen for content changes, auto-trigger localization
- **Status tracking**: Real-time progress for large projects

**Example:**
```
Automate WordPress localization:
Trigger: Post published in English
Action: Auto-translate to es, de, fr, ja
Target: WPML plugin custom fields
Notify: /slack #translation-updates
Fallback: Flag for human review if confidence < 85%
```

---

## Configuration

### Environment Variables
```bash
# Required
export GOOGLE_TRANSLATE_API_KEY="your-google-api-key"
export DEEPL_API_KEY="your-deepl-api-key"

# Optional
export TRANSLATION_MEMORY_PATH="/path/to/translation-memories/"
export GLOSSARY_PATH="/path/to/glossaries/"
export OUTPUT_LANGUAGE_CODES="es,de,fr,ja,pt,zh"
export DEFAULT_ENGINE="deepl"  # or "google"
export QA_BACK_TRANSLATION="true"
export CONFIDENCE_THRESHOLD="0.85"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export RATE_LIMIT_REQUESTS_PER_MINUTE="100"
```

### Setup Instructions

**Step 1: Get API Keys**
- Google Translate: https://console.cloud.google.com → Enable Translation API
- DeepL: https://www.deepl.com/pro/change-plan → Get API key from account settings

**Step 2: Prepare Translation Memory (Optional)**
```bash
# Export from existing CAT tools (Trados, memoQ, SDL)
# Save as TMX or XLIFF format
mkdir -p ~/.translatepro/memories/
cp your-glossary.tmx ~/.translatepro/memories/
```

**Step 3: Create Glossaries**
```json
{
  "glossaries": [
    {
      "name": "brand-terms",
      "language_pair": "en-es",
      "terms": {
        "Dashboard": "Panel de Control",
        "API": "API",
        "Webhook": "Webhook"
      }
    }
  ]
}
```

**Step 4: Test Connection**
```bash
claw test-skill translatepro --api-key $GOOGLE_TRANSLATE_API_KEY
# Output: ✓ Google Translate API connected
# Output: ✓ DeepL API connected
# Output: ✓ Translation Memory loaded (1,247 entries)
```

---

## Example Outputs

### Example 1: Product Description Translation

**Input (English):**
```
Our premium wireless earbuds feature active noise cancellation, 
8-hour battery life, and seamless Bluetooth 5.3 connectivity. 
Ideal for commuters, athletes, and music enthusiasts.
```

**Output (Spanish):**
```
Nuestros auriculares inalámbricos premium cuentan con cancelación 
activa de ruido, 8 horas de autonomía y conectividad Bluetooth 5.3 
sin interrupciones. Ideales para viajeros, atletas y amantes de la música.
```

**Output (Japanese):**
```
プレミアム ワイヤレスイヤホンは、アクティブノイズキャンセレーション、
8時間のバッテリー寿命、シームレスな Bluetooth 5.3 接続を備えています。
通勤者、アスリート、音楽愛好家に最適です。
```

**Output (German):**
```
Unsere Premium-Wireless-Ohrhörer bieten aktive Geräuschunterdrückung, 
8 Stunden Akkulaufzeit und nahtlose Bluetooth 5.3-Konnektivität. 
Ideal für Pendler, Sportler und Musikbegeisterte.
```

---

### Example 2: Website Localization Report

```
PROJECT: E-commerce Site Localization
SOURCE: English (1,247 strings)
TARGETS: Spanish, French, German, Japanese

┌─────────────┬──────────┬────────┬────────┬──────────┐
│ Language    │ Strings  │ TM Hit │ Engine │ Status   │
├─────────────┼──────────┼────────┼────────┼──────────┤
│ Spanish     │ 1,247    │ 89%    │ DeepL  │ ✓ Done   │
│ French      │ 1,247    │ 92%    │ DeepL  │ ✓ Done   │
│ German      │ 1,247    │ 85%    │ DeepL  │ ✓ Done   │
│ Japanese    │ 1,247    │ 34%    │ Google │ ✓ Done   │
└─────────────┴──────────┴────────┴────────┴──────────┘

QUALITY METRICS:
• Terminology consistency: 98.2% (2 glossary violations flagged)
• Back-translation variance: 3.1% (within acceptable range)
• Character limit violations: 0
• Confidence score (avg): 91.7%
• Estimated cost savings via TM: $4,230 (vs. professional translation)
• Time saved: 38 hours (vs. manual translation)

FLAGGED ITEMS: 
1. Spanish - "API documentation" (confidence: 72%, flagged for review)
2. French - Character limit exceeded in checkout button (47 chars, limit: 45)
```

---

### Example 3: Video Subtitle Localization

**Input SRT (English):**
```
1
00:00:15,000 --> 00:00:20,000
Welcome to our advanced tutorial series on cloud architecture.

2
00:00:20,000 --> 00:00:25,000
Today we'll explore scalability patterns and best practices.
```

**Output SRT (Spanish):**
```
1
00:00:15,000 --> 00:00:20,000
Bienvenido a nuestra serie de tutoriales avanzados sobre arquitectura en la nube.

2
00:00:20,000 --> 00:00:25,000
Hoy exploraremos patrones de escalabilidad y mejores prácticas.
```

**Output SRT (Mandarin Chinese):**
```
1
00:00:15,000 --> 00:00:20,000
欢迎来到我们的云架构高级教程系列。

2
00:00:20,000 --> 00:00:25,000
今天，我们将探索可扩展性模式和最佳实践。
```

---

## Tips & Best Practices

### 1. Leverage Translation Memory for Consistency
- **Build incrementally**: Every translation strengthens your organizational memory
- **Regular exports**: Backup TMs quarterly; share across teams
- **Fuzzy matching workflow**: Set thresholds (75%+ = auto-accept, 50-74% = review, <50% = new translation)
- **Metric**: Mature TMs reduce translation costs by 40-60%

### 2. Create Comprehensive Glossaries
- **Start with high-value terms**: Brand names, product names, acronyms, domain-specific vocabulary
- **Document context**: "API" in different contexts may need different translations
- **Version control**: Track glossary changes; enforce across all language pairs
- **Collaborative review**: Have native speakers validate glossaries before enforcement

### 3. Choose the Right Engine Per Task
- **DeepL**: Premium quality for marketing copy, customer-facing content, creative writing
- **Google Translate**: Fast, cost-effective for technical docs, high volume, less nuanced content
- **Hybrid strategy**: DeepL for first 20% of content (highest ROI), Google for remainder

### 4. Optimize for Target Audiences
- **Tone matching**: Use "formal" register for corporate/legal content, "casual" for social media
- **Regional variants**: Spanish differs significantly between Spain and Latin America
- **Cultural adaptation**: Dates, currencies, measurements, idioms need localization beyond translation
- **Test with native speakers**: Budget 10-15% of translation time for native review

### 5. Automate Repetitive Tasks
- **Webhook triggers**: Connect to WordPress, Contentful, GitHub to auto-translate on publish
- **Scheduled jobs**: Nightly batch translations for content-heavy platforms
- **API integration**: Custom scripts for your specific CMS or workflow
- **Parallel processing**: Translate to 10+ languages simultaneously (respects rate limits)

### 6. Quality Assurance Workflow
1. **Machine translation**: Initial pass (DeepL or Google)
2. **TM/Glossary validation**: Enforce terminology consistency
3. **Back-translation check**: Alert if variance > 15%
4. **Native review**: 10-20% sampling for critical content (legal, medical, marketing)
5. **User testing**: Real-world validation in target markets (optional, high-ROI)

### 7. Cost Optimization
- **Cache translations**: Reuse TM matches to reduce API calls by 50-80%
- **Batch processing**: Translate in off-peak hours for better rate limits
- **Language prioritization**: Translate to highest-value markets first (ROI-driven)
- **Character counting**: Monitor usage to stay within budget; set alerts at 80% threshold

---

## Safety & Guardrails

### What TranslatePro Will NOT Do

1. **Sensitive Data Handling**
   - **Will not**: Translate or store PII (emails, phone numbers, SSNs, credit cards)
   - **Will not**: Process without encryption for PHI (health records) or PCI (payment data)