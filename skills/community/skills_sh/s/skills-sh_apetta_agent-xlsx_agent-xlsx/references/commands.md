# Command Reference

Complete flag reference for all agent-xlsx commands. All commands return JSON to stdout by default. When using `--format csv` or `--format markdown`, raw text is written to stdout instead.

## Table of Contents

- [probe](#probe) — Workbook profiling
- [read](#read) — Data extraction
- [search](#search) — Value search
- [export](#export) — Bulk export
- [overview](#overview) — Structural metadata
- [inspect](#inspect) — Deep metadata
- [format](#format) — Cell formatting
- [write](#write) — Write values/formulas
- [sheet](#sheet) — Sheet management
- [screenshot](#screenshot) — Visual capture
- [objects](#objects) — Embedded objects
- [recalc](#recalc) — Formula recalculation
- [vba](#vba) — VBA macros
- [license](#license) — Aspose licence

---

## Global Flags

| Flag | Description |
|------|-------------|
| `--no-meta` | Suppress `_data_origin` and `file_size_human` from output. Reduces token waste on repeated calls against the same file. Applies to all commands that output spreadsheet data |

---

## probe

Profile workbook structure. **Run first, always.** Uses fastexcel with zero data parsing by default.

```
agent-xlsx probe <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | all | Target specific sheet |
| `--types` | | bool | false | Add column types + null counts |
| `--sample` | `-n` | int | 0 | Add N head + N tail rows (sparse dict format) |
| `--stats` | | bool | false | Add numeric/string summaries (implies --types) |
| `--full` | | bool | false | Shorthand for --types --sample 3 --stats |
| `--no-header` | | bool | false | Treat row 1 as data, columns as Excel letters (A, B, C). Use for non-tabular sheets (P&L, dashboards) |
| `--head-cols` | | int | all | Limit profiling to first N columns (reduces output for wide files). Full headers are always included; column types/nulls/stats/samples are scoped |
| `--brief` | | bool | false | Condensed profile: headers + column_map + column_types + null_counts. No samples, no stats, no summaries. Ideal for multi-call pipelines |

**Output:** `sheets[].{name, index, visible, rows, cols, headers, last_col}`, `named_ranges`, `tables`

- Default: `column_map` maps header names → column letters (omitted when `--no-header` since letters map to themselves)
- With `--types`: adds `column_types` (fully-null columns omitted), `null_counts` (fully-null columns omitted), `fully_null_columns` count
- With `--types --no-header`: adds `potential_headers[]` — auto-detected header candidate rows with sparse values (e.g. month names row)
- With `--sample`: adds `sample.{head, tail}` as sparse dicts (only non-null cells, e.g. `{"H": "Food Sales", "I": 71847}`)
- With `--stats`: adds `numeric_summary`, `string_summary` (capped to 5 top values, skips >50% null string columns), `date_summary`

---

## read

Extract data from sheets/ranges. Default: Polars+fastexcel (fast). With `--formulas`: openpyxl (slower).

```
agent-xlsx read <file> [range] [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | first | Target sheet |
| `--limit` | `-l` | int | 100 | Max rows (hard cap: 10,000) |
| `--offset` | | int | 0 | Skip first N rows |
| `--sort` | | str | | Sort by column name |
| `--descending` | | bool | false | Reverse sort order |
| `--formulas` | | bool | false | Return formula strings (openpyxl fallback) |
| `--format` | `-f` | str | json | Output format: json, csv |
| `--no-header` | | bool | false | Treat row 1 as data, columns as Excel letters |
| `--headers` | | bool | false | Resolve column letters to row-1 header names in range reads. Adds `column_map` to output |
| `--compact/--no-compact` | | bool | **true** | Drop fully-null columns from output (strips separator columns). Use `--no-compact` to preserve all columns |
| `--all-sheets` | | bool | false | Read the same range(s) from every sheet |
| `--precision` | `-p` | int | full | Round float values to N decimal places |

**Range** is positional: `"A1:F50"` or `"Sheet1!A1:F50"`. Comma-separated for multi-range: `"Sheet1!A1:C10,E1:G10,H1:J10"` (sheet prefix carries forward).

**Multi-result output** (when using multi-range or `--all-sheets`):

```json
{"results": [{"range": "H54:AT54", "sheet": "2022", "headers": [...], "data": [...], "row_count": 1}], "total_ranges": 3, "compact": true, "read_time_ms": 12.5}
```

Single-range reads keep the existing flat format (backward compatible).

---

## search

Find values across all sheets. Returns cell references with each match.

```
agent-xlsx search <file> <query> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | all | Target specific sheet |
| `--regex` | `-r` | bool | false | Treat query as regex |
| `--ignore-case` | `-i` | bool | false | Case-insensitive match |
| `--columns` | `-c` | str | all | Columns to search: letters (A,B,C) or header names (comma-separated) |
| `--limit` | `-l` | int | 25 | Max results to return (max: 1000) |
| `--range` | | str | | Restrict search to range (e.g. 'A1:D100' or 'Sheet!A1:D100') |
| `--in-formulas` | | bool | false | Search formula strings (openpyxl fallback) |
| `--no-header` | | bool | false | Treat row 1 as data, columns as Excel letters |

**Output:** `matches[].{sheet, column, cell, value, row}` — `column` is always an Excel letter (A, B, H, etc.). Default 25 results (use `--limit` to adjust). Check `truncated` field. With `--in-formulas`: `matches[].{sheet, cell, formula}` (no `column`, `row`, or `value`). `--columns`, `--limit`, and `--range` compose naturally.

---

## export

Bulk export sheet data.

```
agent-xlsx export <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | first | Target sheet |
| `--format` | `-f` | str | json | Format: json, csv, markdown |
| `--output` | `-o` | str | stdout | Write to file |
| `--no-header` | | bool | false | Treat row 1 as data, columns as Excel letters |
| `--compact/--no-compact` | | bool | **true** | Drop fully-null columns from output. Use `--no-compact` to preserve all columns |
| `--json-envelope` | | bool | false | Wrap csv/markdown stdout in a JSON envelope with `_data_origin` tag (ignored when `--output` is set) |

---

## overview

Structural metadata summary. Uses openpyxl + fastexcel for true dimensions.

```
agent-xlsx overview <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--include-formulas` | | bool | false | Add deduplicated formula patterns per sheet (up to 10 unique patterns with counts) |
| `--include-formatting` | | bool | false | Add formatting summary |

**Output:** `sheets[].{name, row_count, col_count, data_rows, data_cols}`, `named_ranges`, `named_range_count`, `has_vba`, `vba_module_count`, `total_formula_count`, `total_chart_count`

---

## inspect

Deep metadata inspection. `--sheet` alone returns everything in one pass.

```
agent-xlsx inspect <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | | Full sheet inspection (formulas, merges, tables, charts, comments, conditional formatting, validation, hyperlinks, freeze panes) |
| `--range` | `-r` | str | | Scope to range (defaults to first sheet if --sheet not given) |
| `--names` | | bool | false | Named ranges only |
| `--charts` | | bool | false | Chart metadata only |
| `--vba` | | bool | false | Inspect VBA modules |
| `--format` | `-f` | str | | Inspect formatting at a cell |
| `--comments` | | bool | false | Cell comments only (max 20) |
| `--conditional` | | str | | Conditional formatting rules for a sheet |
| `--validation` | | str | | Data validation rules for sheet |
| `--hyperlinks` | | str | | Hyperlinks for sheet |

---

## format

Read or apply cell formatting. Supports comma-separated multi-range for applying the same formatting to multiple non-contiguous ranges in one call.

```
agent-xlsx format <file> <range> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | first | Target sheet |
| `--read` | | bool | false | Read formatting instead of writing |
| `--font` | | JSON | | `{"bold": true, "size": 14, "color": "FF0000", "name": "Arial"}` |
| `--fill` | | JSON | | `{"color": "FFFF00", "fill_type": "solid"}` |
| `--border` | | JSON | | `{"style": "thin", "color": "000000"}` |
| `--number-format` | `--number` | str | | Number format string (e.g. `"#,##0.00"`) |
| `--bold/--no-bold` | | bool | | Set font bold (shorthand, avoids JSON) |
| `--italic/--no-italic` | | bool | | Set font italic (shorthand) |
| `--font-size` | | float | | Font size in points (shorthand) |
| `--font-color` | | str | | Font color hex e.g. `FF0000` (shorthand) |
| `--fill-color` | | str | | Fill color hex e.g. `FFFF00` (shorthand, implies solid fill) |
| `--alignment` | | JSON | | `{"horizontal": "center", "vertical": "top", "wrap_text": true, "text_rotation": 45}` |
| `--wrap-text/--no-wrap-text` | | bool | | Enable or disable text wrapping (shorthand) |
| `--horizontal` | | str | | Horizontal alignment: left, center, right, justify (shorthand) |
| `--vertical` | | str | | Vertical alignment: top, center, bottom (shorthand) |
| `--copy-from` | | str | | Copy all formatting from this cell |
| `--batch` | | JSON | | Batch format spec as JSON array. Each entry: `[{"range": "A1:L1", "bold": true, "fill_color": "4472C4"}]`. Supports flat style keys: bold, italic, font_size, font_color, font_name, fill_color, fill_type, border_style, border_color, number_format, horizontal, vertical, wrap_text, text_rotation |
| `--batch-file` | | str | | Path to JSON file with batch format spec (alternative to inline --batch) |
| `--output` | `-o` | str | in-place | Save to new file |

**Range** is positional: `"A1"`, `"A1:D10"`, or `"Sheet1!A1:D10"`. Comma-separated for multi-range: `"A1:C1,B4"` (sheet prefix carries forward). Multi-range works with `--font`, `--fill`, `--border`, `--alignment`, `--number-format`, `--copy-from`, and `--read`.

**Batch mode** (`--batch` or `--batch-file`): Applies different styles to different ranges in a single file open/save. The range positional argument is ignored in batch mode. Each batch entry supports comma-separated ranges (e.g. `"A5:L5,A11:L11"`).

---

## write

Write values or formulas to cells.

```
agent-xlsx write <file> <cell> [value] [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | first | Target sheet |
| `--value` | `-v` | str | | Value to write (alternative to positional arg — handles negative numbers like `--value '-4.095'`) |
| `--formula` | | bool | false | Single cell: adds '=' prefix if missing. Batch (--json/--from-csv): strings starting with '=' are written as formulas, all other values written as-is |
| `--json` | | str | | Write 2D JSON array to range (inline) |
| `--from-json` | | str | | Path to JSON file containing 2D array data for range write |
| `--from-csv` | | str | | Import CSV file starting at cell |
| `--number-format` | | str | | Apply number format |
| `--output` | `-o` | str | in-place | Save to new file |

Auto-creates the target file if it doesn't exist (`.xlsx` and `.xlsm` only). VBA macros in .xlsm files are automatically preserved. Emits `"created": true` when a new file is bootstrapped.

---

## sheet

Manage sheets (create, rename, delete, copy, hide/unhide).

```
agent-xlsx sheet <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--list` | `-l` | bool | false | List all sheets |
| `--create` | | str | | Create new sheet |
| `--rename` | | str | | Sheet to rename (pair with --new-name) |
| `--new-name` | | str | | New name for rename/copy |
| `--delete` | | str | | Delete sheet |
| `--copy` | | str | | Copy sheet (pair with --new-name) |
| `--hide` | | str | | Hide sheet |
| `--unhide` | | str | | Unhide sheet |
| `--output` | `-o` | str | in-place | Save to new file |

---

## screenshot

HD PNG capture. Auto-fits column widths before capture. Auto-detects engine.

```
agent-xlsx screenshot <file> [range] [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | all | Sheet(s), comma-separated |
| `--range` | `-r` | str | | Cell range (e.g. 'A1:F20') |
| `--output` | `-o` | str | /tmp/agent-xlsx | Output directory |
| `--engine` | `-e` | str | auto | Force: excel, aspose, libreoffice |
| `--dpi` | | int | 200 | Resolution (Aspose/LibreOffice only) |
| `--timeout` | | int | 30 | Seconds (LibreOffice only) |
| `--base64` | | bool | false | Return image data inline in JSON |

**Range** is positional: `"Sales!A1:F20"` → filename `file_Sales_A1-F20.png`

---

## objects

List or export embedded objects (charts, shapes, pictures). Engines: Excel or Aspose.

```
agent-xlsx objects <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--sheet` | `-s` | str | all | Target sheet |
| `--export` | `-e` | str | | Export named chart as PNG |
| `--output` | `-o` | str | /tmp/agent-xlsx | Output path |
| `--engine` | | str | auto | Force: excel, aspose |

---

## recalc

Recalculate formulas or scan for errors. Auto-detects engine.

```
agent-xlsx recalc <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--check-only` | | bool | false | Scan for errors without recalculating (no engine needed) |
| `--engine` | `-e` | str | auto | Force: excel, aspose, libreoffice |
| `--timeout` | | int | 60 | Seconds (LibreOffice only) |

`--check-only` output: `error_summary.{error_type: {count, locations[]}}` — finds #REF!, #DIV/0!, #NAME?, #NULL!, #N/A, #VALUE!, #NUM!

**Env var:** `AGENT_XLSX_ENGINE` — pin the engine for all `--engine auto` commands (e.g. `AGENT_XLSX_ENGINE=libreoffice`). Useful for CI or sandboxed environments where Aspose's CoreCLR may crash.

---

## vba

VBA macro analysis and execution. oletools for read/analysis (cross-platform), xlwings for execution (Excel required).

```
agent-xlsx vba <file> [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--list` | `-l` | bool | false | List modules + security summary |
| `--read` | `-r` | str | | Read specific module code |
| `--read-all` | | bool | false | Read all modules (max 500 lines each) |
| `--security` | | bool | false | Full analysis (auto_execute, suspicious keywords, IOCs, risk_level) |
| `--run` | | str | | Execute macro (Excel required). Format: `"Module1.MacroName"` |
| `--args` | | JSON | | Arguments for macro: `'[1, "hello"]'` |
| `--save` | | bool | false | Save workbook after execution |
| `--allow-risky` | | bool | false | Override automatic `MACRO_BLOCKED` block (only when file source is explicitly trusted) |

> **Security (automatic):** Every `--run` silently performs a security analysis first. Macros with
> `risk_level=high` are blocked and return a `MACRO_BLOCKED` error containing the full
> `security_check` report. Pass `--allow-risky` to override. The `security_check` field
> (risk_level, auto_execute_triggers, suspicious_count) is always present in successful run results.
> The file must be `.xlsm` or `.xlsb`; macro names are validated for format.

---

## license

Manage Aspose.Cells licence for watermark-free rendering.

```
agent-xlsx license [flags]
```

| Flag | Alias | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--status` | | bool | false | Check Aspose install + licence status |
| `--set` | | str | | Save licence file path to config (`~/.agent-xlsx/config.json`) |
| `--clear` | | bool | false | Remove saved licence path |

**Env vars:** `ASPOSE_LICENSE_PATH` (file path) or `ASPOSE_LICENSE_DATA` (base64-encoded .lic content for CI/CD). Priority: env var → config file.
