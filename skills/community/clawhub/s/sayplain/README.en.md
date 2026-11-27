# sayplain

[![skills.sh](https://skills.sh/b/shxuk/sayplain)](https://skills.sh/shxuk/sayplain)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-green.svg)](./scripts/style_check.py)

[简体中文](./README.md) | English

A de-AI editorial workflow for Chinese technical writing (Agent Skill + 4 zero-dependency Python linters).  
Strips AI clichés, translationese, and meta-narration from drafts while keeping every number, command, path, and proper noun intact.

## Quick Start

```bash
# Install as an Agent Skill (Claude Code / Cursor / Trae / Antigravity)
npx skills add shxuk/sayplain

# Or run the standalone Python 3 stdlib checks directly (no pip install)
python scripts/format_check.py draft.md
python scripts/fact_anchor_check.py 01_orig.md 02_edited.md
python scripts/style_check.py 02_edited.md
python scripts/consistency_check.py chapters/
```

## Four-Stage Pipeline

0. **Format & Terminology**: normalize casing, punctuation, and typos without changing meaning.
1. **De-AI Rewrite**: remove translationese and awkward syntax for non-expert readers.
2. **Subtraction Only**: cut meta-narration, fake colloquialisms, and redundant wrap-ups without adding new claims.
3. **Fact-Anchor & Style Audit**: diff numbers/code/proper nouns against the source draft and run the 21-rule final check.

## Boundaries

- Edits existing Chinese drafts only—not for cross-language translation or writing from scratch.
- Never invents facts or drops code/numbers from the source.
- Aborts immediately if suspected credentials (API keys, private keys, cookies) appear in the input.

## License

[MIT](./LICENSE)
