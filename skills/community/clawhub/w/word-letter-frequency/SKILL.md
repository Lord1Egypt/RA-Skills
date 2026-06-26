---
name: word-letter-frequency
description: Count how many times each letter appears in a word or short phrase. Trigger when a user asks for per-letter frequencies, distributions, or statistics inside a single word or very short string.
---

# Word Letter Frequency

## Quick start
1. Identify the input text (typically one word or a short phrase). Default behavior lowercases the text and ignores non-letters so repeated letters like `a`/`A` are merged.
2. Run `scripts/count_letters.py "<text>"` to get a frequency table. Use the optional flags when needed:
   - `--case-sensitive` keeps uppercase and lowercase separate.
   - `--include-non-alpha` counts digits/punctuation as-is.
   - `--json` returns machine-friendly JSON for downstream processing.
3. Summarize the counts for the user. Include clarifying notes (e.g., whether you ignored punctuation) when relevant.

## Script reference
### scripts/count_letters.py
Lightweight CLI/utility that powers this skill. It exposes two layers:
- **CLI usage**: `python3 scripts/count_letters.py "balloon" --json`
- **Import usage**: `from scripts.count_letters import count_letters` and call `count_letters(text, case_sensitive=False, include_non_alpha=False)` to get a `collections.Counter`.

Sample CLI output (default options):
```
$ python3 scripts/count_letters.py "balloon"
Character  Count
---------  -----
a          1
b          1
l          2
o          2
n          1
```

Sample JSON output (good for embedding directly into responses):
```
$ python3 scripts/count_letters.py "AaB!" --case-sensitive --include-non-alpha --json
{"A": 1, "a": 1, "B": 1, "!": 1}
```

## Response patterns
- **Concise summary**: “`balloon` contains `b×1, a×1, l×2, o×2, n×1` (case-insensitive, punctuation ignored).”
- **Tabular snippet**: Mirror the script’s table for readability. Mention any options you used.
- **JSON / dict**: When the user wants structured data, reuse the script’s `--json` flag.

## Edge cases & tips
- Make sure to state how you treated uppercase letters and punctuation, especially when the counts differ depending on options.
- If the input contains no alphabetic characters and `--include-non-alpha` is not set, the script intentionally reports “(no characters were counted)”. Explain why in the response.
- For multiple words, either run the script once on the full phrase (default) or note that the skill focuses on short strings; if the request expands to full documents, escalate to a general text-analysis workflow instead.
