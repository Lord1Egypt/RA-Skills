---
name: splitsym
description: Extract comments and split symbols from source files. Use when users want to extract inline comments, docstrings, or block comments from code files to understand structure or generate documentation.
---

## splitsym

Extract split symbols (line or pair) from source files. Analyzes source code and extracts comments based on file type.

### Usage

```bash
splitsym <file> [--lines M-N] [--config CONFIG]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `file` | Source file to analyze (required) |
| `--lines` | Optional line range (e.g., `100-200`) |
| `--config` | Path to symbols.json config (default: `~/.config/splitsym/symbols.json`) |

### Supported File Types

| Extension | Comment Style |
|-----------|---------------|
| `.py`, `.rb`, `.sh`, `.yaml` | `# comment` |
| `.c`, `.js`, `.ts`, `.java` | `// comment` |
| `.sql`, `.hs` | `-- comment` |
| `.lisp`, `.clj` | `; comment` |
| `.tex`, `.erl` | `% comment` |
| `.html`, `.xml`, `.vue` | `<!-- comment -->` |
| `.py` | `"""docstring"""` or `'''docstring'''` |
| `.ml`, `.mli` | `(* comment *)` |

### Example

```bash
# Extract all comments from a Python file
splitsym myfile.py

# Extract comments from specific line range
splitsym myfile.py --lines 100-200

# Use custom config
splitsym myfile.py --config ./my-symbols.json
```

### Output Format

```
   123      PAIR: multi-line comment content...
     45    # This is a comment line
```

- Line numbers are right-aligned (6 digits)
- Indentation is preserved
- `PAIR:` prefix indicates multi-line block comments