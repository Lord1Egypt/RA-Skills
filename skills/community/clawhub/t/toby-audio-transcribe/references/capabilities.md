# AssemblyAI capabilities reference for this skill

This file is the human-readable summary behind the `models` and `languages` commands.

## Core STT endpoints

- US base URL: `https://api.assemblyai.com`
- EU base URL: `https://api.eu.assemblyai.com`

For LLM Gateway:

- US: `https://llm-gateway.assemblyai.com`
- EU: `https://llm-gateway.eu.assemblyai.com`

## Recommended speech model strategy

### Default recommendation
Use:

```json
{
  "speech_models": ["universal-3-pro", "universal-2"],
  "language_detection": true
}
```

Reason:

- Universal-3-Pro is preferred where supported
- Universal-2 acts as the broad fallback
- this avoids silently defaulting to a single language when the source language is unknown

### When to force Universal-3-Pro
Use explicit Universal-3-Pro when:

- the language is known to be one of its supported families
- you want prompting support
- you want the larger keyterms limit

### When to lean on Universal-2
Use Universal-2 explicitly when:

- the language is outside Universal-3-Pro coverage
- you want the simplest “wide coverage” choice
- you do not need Universal-3-Pro-only prompting behaviour

## Universal-3-Pro

Supported language families and dialect notes:

- English: American, British, Australian
- Spanish: Castilian, Mexican, Argentine, Colombian, Chilean, Caribbean, Spanglish
- French: Metropolitan, Quebecois, Belgian
- German
- Italian: Standard
- Portuguese: Brazilian, European

Key capabilities called out in AssemblyAI docs:

- highest-accuracy positioning
- prompting support
- keyterms prompt up to 1,000 entries
- built-in code switching across supported languages

## Universal-2

AssemblyAI documents 99-language coverage, grouped by accuracy band.

### High accuracy
English, Spanish, French, German, Indonesian, Italian, Japanese, Dutch, Polish, Portuguese, Russian, Turkish, Ukrainian, Catalan

### Good accuracy
Arabic, Azerbaijani, Bulgarian, Bosnian, Mandarin Chinese, Czech, Danish, Greek, Estonian, Finnish, Galician, Hindi, Croatian, Hungarian, Korean, Macedonian, Malay, Norwegian, Romanian, Slovak, Swedish, Swiss German, Tagalog, Thai, Urdu, Vietnamese

### Moderate accuracy
Afrikaans, Belarusian, Welsh, Persian / Farsi, Hebrew, Armenian, Icelandic, Kazakh, Lithuanian, Latvian, Maori, Marathi, Slovenian, Swahili, Tamil

### Fair accuracy
Amharic, Assamese, Bengali, Gujarati, Hausa, Javanese, Georgian, Khmer, Kannada, Luxembourgish, Lingala, Lao, Malayalam, Mongolian, Maltese, Burmese, Nepali, Occitan, Punjabi, Pashto, Sindhi, Shona, Somali, Serbian, Telugu, Tajik, Uzbek, Yoruba

## Feature notes

### Speaker diarisation
Enable `speaker_labels=true` when you need generic speaker segments such as `A`, `B`, etc.

### Speaker identification
Use AssemblyAI Speech Understanding when you want those generic labels mapped to real names or roles.

### Custom spelling
This is a strong fit for product names, company names, uncommon surnames, technical terms, and branded spellings. Example asset: `assets/custom-spelling.example.json`

### Translation
Use Speech Understanding translation when you need transcript-level or utterance-aligned translations.

### Custom formatting
Use Speech Understanding custom formatting when dates, phone numbers, and emails need normalised presentation.

### Topics, key phrases, entities, sentiment
The CLI exposes common flags:

- `--iab-categories`
- `--auto-highlights`
- `--entity-detection`
- `--sentiment-analysis`

These sections are also surfaced in the Markdown and agent JSON outputs when present.

## Export endpoints

The skill supports:

- transcript JSON
- agent-friendly Markdown
- normalised agent JSON
- text
- paragraphs
- sentences
- subtitles (`srt`, `vtt`)

## Important deprecations

### Summarisation fields on the transcription API
The old summarisation parameters on the transcription API are deprecated. Use the LLM Gateway for summaries and structured extraction.

### LeMUR
LeMUR is deprecated in favour of the LLM Gateway. The CLI therefore includes an `llm` command rather than a LeMUR workflow.

## Bundled machine-readable references

- `assets/model-capabilities.json`
- `assets/language-codes.json`
