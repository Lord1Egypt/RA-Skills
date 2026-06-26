# md2docx — Implementation Spec

Implement this as: `md2docx.py`

This document tells your AI exactly how to implement a Markdown → .docx converter
compatible with the superthink pipeline output format.

---

## What It Does

Converts a Markdown file to a formatted Word document (.docx).

```
python3 md2docx.py input.md output.docx
```

---

## Environment Requirements

- Python 3.8+
- `python-docx` library — install with: `pip install python-docx`
- No other third-party packages

---

## Markdown Elements to Support

The superthink pipeline produces output using these elements — support all of them:

| Element | Markdown syntax | Word output |
|---|---|---|
| H1 heading | `# Title` | Heading 1 style, 20pt, bold, dark navy |
| H2 heading | `## Title` | Heading 2 style, 16pt, bold, dark blue |
| H3 heading | `### Title` | Heading 3 style, 13pt, bold, medium blue |
| H4 heading | `#### Title` | Heading 4 style, 11pt, bold, dark grey |
| Bold | `**text**` | Bold run |
| Italic | `*text*` | Italic run |
| Inline code | `` `code` `` | Courier New, 9pt, dark red |
| Code block | ` ```...``` ` | Indented block, Courier New 8.5pt, dark grey |
| Bullet list | `- item` or `* item` | List Bullet style |
| Nested bullet | `  - item` (2 spaces) | List Bullet 2 style |
| Numbered list | `1. item` | List Number style |
| Nested numbered | `  1. item` | List Number 2 style |
| Horizontal rule | `---` | Line of `─` characters, light grey |
| Empty line | blank line | Skip (do not add blank paragraphs) |
| Regular paragraph | any other line | Normal style, 11pt |

---

## Document Styling

### Page layout:
- Top/bottom margin: 1 inch
- Left/right margin: 1.25 inches
- Default font: Calibri 11pt

### Heading colours (RGB):
- H1: `#1a1a2e` (very dark navy)
- H2: `#16213e` (dark navy blue)
- H3: `#0f3c78` (medium blue)
- H4: `#333333` (dark grey)

### Horizontal rule:
- A paragraph of `─` (box drawing character U+2500) repeated 60 times
- Light grey colour: `#cccccc`
- 6pt space before and after

### Code blocks:
- Left indent: 0.3 inches
- Font: Courier New 8.5pt
- Colour: `#2d2d2d`
- Preserve newlines within the block

### Inline code:
- Font: Courier New 9pt
- Colour: `#c7254f` (dark red/crimson)

---

## Parsing Logic

Process the file line by line with a state machine:

### State: in_code_block
- Enters on a line starting with ` ``` `
- Exits on the next line starting with ` ``` `
- While inside: accumulate lines, do not parse as any other element
- On exit: write accumulated lines as a single code block paragraph

### Heading detection:
```
line starts with one or more `#` followed by a space
level = count of leading `#` characters (1-4)
text = remainder of line, stripped
strip any remaining `*` characters from heading text before writing
```

### Bullet list detection:
```
line matches: optional whitespace + (- or * or +) + space + text
indent level = len(leading whitespace) // 2
level 0 → List Bullet style
level 1+ → List Bullet 2 style
```

### Numbered list detection:
```
line matches: optional whitespace + digits + . + space + text
indent level = len(leading whitespace) // 2
level 0 → List Number style
level 1+ → List Number 2 style
```

### Horizontal rule detection:
```
stripped line matches: ---+ or ***+
```

### Inline formatting (applied within paragraph and list text):
Process inline markdown using a regex split on these patterns:
- `**...**` → bold run
- `*...*` → italic run (must not match `**`)
- `` `...` `` → inline code run

Apply to all regular paragraphs and list items. Do NOT apply inside code blocks.

---

## Implementation Notes for Your AI

- Use `doc.add_heading(text, level=N)` for headings, then override font properties
  because python-docx heading styles vary by template
- Use `doc.add_paragraph(style='List Bullet')` for bullets — catch `KeyError` and
  fall back to `doc.add_paragraph()` if the style doesn't exist in the template
- Write the code block as a single paragraph with `\n`.join of accumulated lines,
  not as multiple separate paragraphs
- Do not add a blank paragraph for every empty line in the source — just skip them
- Strip YAML frontmatter if present (lines between `---` at the very start of the file)
- Save with `doc.save(output_path)` and print confirmation to stdout

### Frontmatter stripping:
If the file starts with `---`, skip all lines until the closing `---` before parsing.

### Error handling:
- If input file doesn't exist: print error and exit with code 1
- If output directory doesn't exist: create it automatically
- If `python-docx` is not installed: print a clear install instruction and exit with code 1

---

## CLI Interface

```
python3 md2docx.py <input.md> <output.docx>
```

- Positional args: input path, output path
- Both required — no defaults
- Print `"Saved: <output path>"` on success
- Exit code 0 on success, 1 on error

---

## Minimal Implementation Checklist

File to create: `md2docx.py`

- [ ] Parses all element types listed in the table above
- [ ] State machine for code blocks (no bleed-through)
- [ ] Inline bold/italic/code within paragraphs and list items
- [ ] Heading colours set correctly
- [ ] Page margins set (1in top/bottom, 1.25in left/right)
- [ ] Calibri 11pt default font
- [ ] Horizontal rule renders as a grey line
- [ ] Frontmatter stripped if present
- [ ] Graceful error if python-docx not installed
- [ ] Exit code 0 on success, 1 on error
