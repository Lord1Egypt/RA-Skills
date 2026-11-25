# Voice discovery and selection

Use live catalog records for voice IDs and descriptions. Listing and searching do not
generate audio, use credits, or create a personal voice.

## List every voice and its description

```bash
# All system voices across all languages plus this account's personal voices:
node scripts/uydi.mjs voices --all -o voices.json

# Human-readable descriptions, or JSON for an agent:
node scripts/uydi.mjs voices --all
node scripts/uydi.mjs voices --all --json

# Restrict the source, without confusing system voices with personal voice slots:
node scripts/uydi.mjs voices --source user --json
node scripts/uydi.mjs voices --source system --language en --json
node scripts/uydi.mjs system-voices --all
```

`voices` without flags keeps the personal-library view for compatibility. `--all` is
the complete system-and-personal catalog. Both source views include full descriptions.
The CLI follows all system pages and deduplicates IDs, checks the catalog version and
total, then filters locally. A failed page aborts the read; partial data is never
reported as a complete catalog. For long lists, deliver the JSON file and a short
summary instead of dropping entries to fit a chat message.

Each normalized result has `id`, `voiceType` (`system` or `user`), `name`, `description`,
`descriptionAvailable`, `languages`, `gender`, `age`, `ageGroup`, `traits`, `scenario`,
`kind`, `provider`, `status`, and a preview URL when available. Personal descriptions
come from the account's saved voice prompt. Missing descriptions are `null`; missing
age/gender metadata stays unknown. Do not invent an accent, emotion, age or timbre.

## Find voices for a user's brief

Extract hard requirements (language, source, gender, age) into explicit filters and
put desired style/use-case words into `--query`. For example, “找五个中文温柔女声做旁白”:

```bash
node scripts/uydi.mjs find-voices --language zh --gender female --query "温柔 旁白" --limit 5
node scripts/uydi.mjs find-voices --language en --gender male --age adult --query "deep documentary" --limit 5
node scripts/uydi.mjs find-voices --source user --query "warm narrator"
node scripts/uydi.mjs find-voices --query "Elias"
```

Search flags:

| Flag | Meaning |
| --- | --- |
| `--source all\|system\|user` | Defaults to all for `find-voices` |
| `--language <code>` | Must be listed in the voice's supported languages |
| `--gender male\|female\|unknown` | Structured catalog metadata |
| `--age child\|young\|adult\|senior\|unknown` | Catalog age group |
| `--min-age n --max-age n` | Numeric age bounds; unknown numeric ages are excluded |
| `--scenario <text>` | Case-insensitive substring of the catalog scenario |
| `--provider uydi\|cosyvoice` | Provider filter |
| `--kind <value>` | Such as design, clone, system or basic |
| `--status ready` | Exclude personal voices not ready for synthesis |
| `--query <text>` | Names, IDs, description/style and use-case keywords |
| `--match all\|any` | All keyword groups must match by default; any allows partial alternatives |
| `--limit n` | Output count after searching all pages; defaults to 10 |
| `-o matches.json` | Save complete JSON results for the selected output limit |

Language codes: `zh`, `en`, `ja`, `ko`, `fr`, `de`, `ru`, `pt`, `th`, `id`, `vi`, `es`,
`it`, `ms`, `fil`, `ar`. Omit language or use `all` to browse every language.

The ranking is keyword-based with common Chinese/English expansions, not an audio
similarity or semantic model. Hard filters must all match. By default, every query
keyword group must also match catalog evidence. Use `--match any` only to explore
explicitly labelled alternatives; those may match only some requested traits. Inspect `matchedTerms`,
`unmatchedTerms`, `matchEvidence`, and the actual description before recommending it.
`total` is the matching count; `returned` and `truncated` say whether the output limit
hid results. Remove or increase `--limit` to show more matches.

If a literal query misses a useful concept, try a shorter English/Chinese equivalent
while keeping the user's hard filters. If no voice satisfies them, say which
requirement lacks evidence and offer nearby alternatives; do not silently relax it.
When an exact numeric age or gender is missing for a personal voice, a hard metadata
filter excludes it even if its description mentions a related style. Explain this
limitation or inspect the personal-description results separately.

Present a shortlist with name, exact ID, source/type, languages, full or concise
description and the concrete reason it fits. Keep identity and description tied to
the returned record. For synthesis/Canvas, select a `ready` voice and preserve its
`voiceType`; for system TTS always specify the language:

```bash
node scripts/uydi.mjs tts --voice q31-flash-beth --voice-type system --language en --text "Hello." -o beth.wav
```
