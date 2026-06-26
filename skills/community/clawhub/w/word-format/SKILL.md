---
name: word_format_standardize
description: Convert uploaded Word documents (.docx) into the fixed Chinese official-document format defined by the bundled government-style template bundle. Use when Codex needs to restyle a user-provided Word file to match this house style, enforce title/body/heading/table rules, and stop with a clear missing-font notice if required fonts are unavailable.
---

# Word Format Standardize

Convert a user-uploaded `.docx` into the target format and return the converted `.docx`.

## Workflow

1. Confirm the source file is a `.docx`.
2. Run `scripts/convert_to_house_style.py` with the input file and a target output path.
3. If the script exits with code `2`, tell the user which fonts are missing and do not return a converted file.
4. If conversion succeeds, return the generated `.docx`.
5. Mention that complex layout documents should still be manually checked after conversion.

## Command

```powershell
python scripts/convert_to_house_style.py `
  --input "C:\path\to\input.docx" `
  --output "C:\path\to\output.docx"
```

## Converter Guarantees

- Check required fonts before conversion.
- Apply page setup, theme, styles, font table, and section settings derived from the bundled template bundle.
- Normalize paragraphs into title, body, heading 1-4, attachment label, date/signature, and table text using deterministic heuristics.
- Return a hard failure instead of pretending conversion worked when critical fonts are missing.

## Resources

- `assets/template-bundle.json`: text-only export of the reference template settings required for ClawHub upload.
- `references/format-rules.md`: concise formatting rules and heuristics.
- `scripts/convert_to_house_style.py`: converter script.


