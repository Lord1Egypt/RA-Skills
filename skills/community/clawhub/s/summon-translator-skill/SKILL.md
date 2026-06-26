---
name: summon_translator
description: Translate safety procedures, supplier documents, and Articulate Rise 360 
  eLearning content into 137+ languages using AI. Built for supply chain teams, HSE 
  professionals, and L&D teams who can't afford mistranslated compliance content.
version: 1.0.0
author: Summon Translator <support@summontranslator.com>
homepage: https://summontranslator.com
pricing: pay-as-you-go — $0.007/word + AI cost, $5 minimum/job
auth: bearer_token
metadata:
  openclaw:
    requires:
      config:
        - SUMMON_API_KEY
---

# Summon Translator Skill

Use this skill to translate compliance-critical files — XLIFF exports from Articulate 
Rise 360, supplier qualification forms, safety data sheets, JSAs, LOTOs, arc flash 
procedures, and more — into any target language with terminology precision.

## Who this is for

**Supply Chain Managers** — Onboard global suppliers faster. Translate qualification 
questionnaires, vendor codes of conduct, and procurement forms without waiting on 
LSP quotes.

**Articulate Rise 360 / L&D Teams** — Export your course XLIFF from Rise, translate 
it here, re-import. No manual copy-paste. Preserves all tags, inline formatting, 
and segment structure. Ideal for safety inductions, compliance modules, and 
onboarding courses across multilingual workforces.

**Heavy Industry HSE Professionals** — Translate JSAs, SDS sheets, arc flash warning 
labels, LOTO procedures, confined space permits, and toolbox talk scripts into the 
field languages your workers actually speak. Supports Arabic (RTL), Vietnamese, 
Tagalog, Hindi, Portuguese, and 130+ more.

---

## Prerequisites

1. Create an account at https://summontranslator.com
2. Add a payment method at https://summontranslator.com/billing
3. Generate an API key at https://summontranslator.com/account
4. Set the environment variable: `SUMMON_API_KEY=st_live_<your-key>`

## Verify your key is working
```bash
curl -s https://summontranslator.com/api/v1/ping \
  -H "Authorization: Bearer $SUMMON_API_KEY"
```

Expected response: `{"ok":true,"version":"1",...}`

---

## translate_file — Translate a local file

Use this command when the user wants to translate a file.

Parameters:
- `file_path` — path to the file on disk (required)
- `target_languages` — comma-separated BCP-47 codes, e.g. `ja-JP,fr-FR,de-DE` (required)
- `model` — AI model to use (optional, default: `claude-haiku-4-5-20251001`)
- `provider` — `anthropic` | `openai` | `gemini` | `deepseek` (optional, inferred from model)
- `source_language` — source language BCP-47 code (optional, default: `en-US`)
- `output_dir` — directory to save translated files (optional, default: same dir as input)

### Step 1 — Submit the translation job
```bash
curl -s -X POST https://summontranslator.com/api/v1/jobs \
  -H "Authorization: Bearer $SUMMON_API_KEY" \
  -F "file=@{file_path}" \
  -F "provider={provider}" \
  -F "model={model}" \
  -F "targetLanguages={target_languages}" \
  -F "sourceLanguage={source_language}" \
  -F "name=$(basename {file_path})"
```

Save the `jobId` from the response.

### Step 2 — Poll for completion
```bash
curl -s https://summontranslator.com/api/v1/jobs/{jobId} \
  -H "Authorization: Bearer $SUMMON_API_KEY"
```

Repeat every 15 seconds until `status` is `"completed"` or `"failed"`.
Each task in the `tasks` array shows per-language progress.

### Step 3 — Download each translated file

For each completed task, use the `downloadUrl` from the poll response:
```bash
curl -s -L -o "{output_dir}/{taskId}.{ext}" \
  -H "Authorization: Bearer $SUMMON_API_KEY" \
  "{downloadUrl}"
```

Or use the explicit URL:
```bash
curl -s -L -o "{output_dir}/{language}.{ext}" \
  -H "Authorization: Bearer $SUMMON_API_KEY" \
  "https://summontranslator.com/api/v1/jobs/{jobId}/tasks/{taskId}/download"
```

---

## check_job — Check translation status

Use when the user wants to check the status of a previously submitted job.
```bash
curl -s https://summontranslator.com/api/v1/jobs/{job_id} \
  -H "Authorization: Bearer $SUMMON_API_KEY"
```

---

## list_jobs — List recent translation jobs
```bash
curl -s "https://summontranslator.com/api/v1/jobs?limit=10" \
  -H "Authorization: Bearer $SUMMON_API_KEY"
```

---

## Supported file formats

| Extension | Format | Typical Use Case |
|---|---|---|
| .xliff / .xlf | XLIFF 1.2 bilingual | Articulate Rise 360 exports, TMS roundtrips |
| .json | JSON key-value | Supplier portal UI strings, web app content |
| .csv | CSV (id, value columns) | Qualification forms, audit checklists |
| .md | Markdown | SOPs, safety bulletins, internal wikis |
| .txt | Plain text | Toolbox talk scripts, permit-to-work templates |
| .xml | Android string resources | Mobile HSE apps, field inspection tools |
| .po | GNU gettext | Open-source EHS platforms |
| .strings | iOS/macOS Localizable.strings | Native mobile safety apps |
| .stringsdict | iOS/macOS plural rules | Mobile apps with count-based strings |
| .xcstrings | Xcode String Catalog | Modern iOS/macOS app localization |
| .arb | Flutter ARB | Cross-platform field inspection apps |
| .properties | Java resource bundles | Enterprise ERP / WMS localization |

---

## Articulate Rise 360 Workflow

Rise 360 exports course content as an XLIFF file (`.xlf`). Use Summon Translator 
to localize it without breaking your course structure:

1. In Rise, go to **Export → Translations → Export for Translation** → download the `.xlf`
2. Run `translate_file` with your `.xlf` and target languages (e.g., `es-ES,pt-BR,vi-VN`)
3. Download the translated `.xlf` files
4. Re-import into Rise: **Export → Translations → Import Translation**

All inline tags (`<g>`, `<x/>`, `<mrk>`) are preserved. No broken segments.

> Recommended model for eLearning: `claude-sonnet-4-6` — best at maintaining 
> instructional tone, safety register, and consistent terminology across modules.

---

## HSE Content Tips

For safety-critical translations, use `claude-sonnet-4-6` and add a system prompt 
or glossary note in your job name to signal the domain:
```bash
-F "name=arc-flash-loto-procedure_HSE"
```

High-stakes content types that benefit most from AI translation review:
- Arc flash boundary labels and PPE category callouts
- SDS Sections 2, 4, 7 (hazard ID, first aid, handling/storage)
- LOTO energy isolation sequences
- Confined space entry permits
- Emergency response and evacuation procedures

> ⚠️ For regulatory submissions or legally binding safety documents, 
> always have a qualified human reviewer validate the final translation.

---

## Common target language codes for industrial workforces

| Language | Code | Common regions |
|---|---|---|
| Spanish (Latin America) | `es-419` | Mexico, Central/South America |
| Spanish (Spain) | `es-ES` | Spain, EU supplier base |
| Portuguese (Brazil) | `pt-BR` | Brazil manufacturing |
| Vietnamese | `vi-VN` | Southeast Asia operations |
| Tagalog | `tl-PH` | Philippines, offshore marine |
| Hindi | `hi-IN` | India supply chain |
| Arabic | `ar-SA` | Gulf region, oilfield |
| French | `fr-FR` | France, West Africa, Canada |
| Mandarin (Simplified) | `zh-CN` | China manufacturing |
| Mandarin (Traditional) | `zh-TW` | Taiwan, HK procurement |
| Thai | `th-TH` | Thailand, ASEAN |
| Indonesian | `id-ID` | Indonesia, mining |
| Polish | `pl-PL` | Eastern Europe manufacturing |

---

## Supported models

| Model ID | Provider | Best for |
|---|---|---|
| claude-sonnet-4-6 | anthropic | HSE docs, eLearning, compliance content requiring precision |
| claude-haiku-4-5-20251001 | anthropic | High-volume supplier forms, UI strings, fast turnaround |
| gpt-4o | openai | Alternative premium option |
| gpt-4o-mini | openai | Cost-conscious batch jobs |
| gemini-2.0-flash | gemini | Bulk processing, lower cost |
| deepseek-chat | deepseek | Budget option for non-critical content |

**Recommended default:** `claude-haiku-4-5-20251001` — fast and affordable for most 
supply chain and onboarding content.

**For safety-critical or Rise 360 eLearning:** use `claude-sonnet-4-6`.

---

## Pricing

- $0.007 per source word (platform fee)
- Plus AI model cost × 5 markup
- $5.00 minimum per job
- Billed monthly to card on file
- **First 1,000 words free:** add `-F "promoCode=1TIME"` to your first job

> A typical 30-minute Rise 360 safety induction course (~3,000 source words) 
> costs roughly **$21–$45** depending on model — vs. $300–$600+ from a traditional LSP.

---

## Support

Email: support@summontranslator.com  
API docs: https://summontranslator.com/llms.txt