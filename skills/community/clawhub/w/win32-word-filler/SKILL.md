# Word Template Filler Skill

Fill/edit Word `.docx` templates on Windows via **win32com COM automation** — preserves ALL formatting, images, underlines, page breaks, and table layout.

## Why win32com instead of python-docx

| Approach | Format/Image Preservation | Requires Word |
|---|---|---|
| **win32com** (this skill) | ✅ 100% — Word does the work | ✅ Yes |
| `python-docx` | ❌ Drops images, corrupts complex formatting | ❌ No |
| `docxtpl` (Jinja) | ⚠️ Better than python-docx, still risks layout drift | ❌ No |

## Requirements

- **Windows** with **Microsoft Word** installed
- **pywin32** (`pip install pywin32`)

## Quick Start

```bash
# Fill cover fields, append answers, add page breaks — all in one command
python {scripts}/word_template_filler.py template.docx report.docx ^
  --cover-field "所在学院:铁道工程学院" ^
  --cover-field "专业年级:车辆工程 2023级" ^
  --page-break-before "C2.转向架" ^
  --find-replace "。？:。"
```

## Commands

All operations use the bundled `scripts/word_template_filler.py` CLI tool.

### --cover-field / -c
Fill a cover page field (preserves underline lines).

```
--cover-field "label:value"
```

The label must exactly match the text before the colon (including spaces).
The value is inserted before the underlined spaces, so the fill-in line remains.

### --append-answer / -a
Append answer text after a question in a table cell.

```
--append-answer "TableIdx:Row:Col:question text||answer text"
```

Example: `--append-answer "2:3:1:1、转向架的作用是什么？||1. 可相对车体回转..."`

### --insert-blank-para / -p
Insert text into a blank paragraph within a table cell (for sub-tables).

```
--insert-blank-para "TableIdx:Row:Col:Para1B:text"
```

`Para1B` = 1-based paragraph index within the cell. Use debug mode to find indices.

### --page-break-before / -b
Insert a page break before a heading.

```
--page-break-before "C2.转向架"
```

### --find-replace / -r
Find and replace text across the entire document (preserves formatting).

```
--find-replace "find:replace"
```

### --set-time-score / -t
Set 实训时间 and 得分 fields in a section table row.

```
--set-time-score "TableIdx:time|score"
```

Example: `--set-time-score "2:2026年6月|95"`

### --visible
Show the Word window during processing (for debugging).

## Debug Mode

```bash
# First, kill any hanging Word processes
taskkill /f /im WINWORD.EXE

# Show Word window to watch the process
python {scripts}/word_template_filler.py template.docx debug.docx --visible
```

To find paragraph indices within a table cell, use this diagnostic snippet:

```python
import win32com.client as win32
word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False
doc = word.Documents.Open(r'path\to\template.docx')
cell = doc.Tables(2).Cell(4, 1)  # Table 2, Row 4, Col 1
paras = cell.Range.Paragraphs
for i in range(paras.Count):
    txt = repr(paras(i+1).Range.Text)[:80]
    print(f"  Para {i}: {txt}")
doc.Close(False)
word.Quit()
```

## Verification Checklist

1. **Cover**: underlined spaces preserved
2. **Page breaks**: sections start on correct pages
3. **Punctuation**: no `。？` or `！？` double-patterns
4. **Content**: tables have data, text is readable

## Known Pitfalls

| Don't Do | Why |
|---|---|
| `doc.Range().Text = ...` | Destroys ALL formatting, images, tables |
| Replace paragraph containing `\f` | Loses page break |
| Use `python-docx` to save modified template | Loses images, complex formatting |
| `\n` in Find patterns | Word uses `\r` (chr 13) for paragraph marks |
| Replace cover paragraph text blindly | Destroys underlined spaces |
| Forget cleanup after `--append-answer` | May leave extra `？` characters |
