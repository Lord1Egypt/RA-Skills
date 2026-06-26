---
name: text-compressor
description: Compress and decompress text files using smart abbreviation and whitespace normalization. Use when user asks to compress, shrink, reduce, or optimize text file size while preserving readability. Also use for batch text processing, file size reduction, or text cleanup.
---

# Text Compressor Skill

Compress text files using configurable levels of text abbreviation while keeping content readable.

## Usage

### Basic Compression
```
python scripts/compress.py <input_file> [output_file] [--level 1-3]
```

### Decompress (restore approximation)
```
python scripts/compress.py <input_file> [output_file] --decompress [--level 1-3]
```

### Levels
- **Level 1** — Clean whitespace, normalize line breaks, preserve all words
- **Level 2** — + Smart phrase contractions (that is -> that's, you are -> ur, etc.)
- **Level 3** — + Aggressive abbreviations (because -> bc, through -> thru, etc.)

## Examples

- `compress.py report.txt` — compress report.txt → report.txt.compressed
- `compress.py input.txt output.txt --level 2` — medium compression to specific output
- `compress.py compressed.txt --decompress` — attempt to restore (approximate)

## Output

Shows bytes saved and percentage reduction.

## Notes

- Compression is one-way by default. Use `--decompress` to attempt restoration (approximate only).
- Level 1 is safe for all content. Higher levels may affect readability.
- Always preserves line break structure.