---
name: rolex-maybeai-sheet
description: "MaybeAI Sheet skill for full Excel/spreadsheet lifecycle management. Upload, read, edit, and analyze Excel files via the MaybeAI platform. Use when the user wants to: upload or import an Excel file, read spreadsheet data, update cell ranges, insert/delete rows or columns, manage worksheets, add charts or images, apply filters or conditional formatting, calculate formulas, export files, manage versions, or perform any Excel data operation."
version: 0.1.4
metadata:
  openclaw:
    requires:
      env:
        - MAYBEAI_API_TOKEN
    primaryEnv: MAYBEAI_API_TOKEN
    emoji: "📊"
    homepage: https://github.com/OmniMCP-AI/maybeai-uni
---

# MaybeAI Sheet Skill

Full Excel/spreadsheet lifecycle management powered by the [MaybeAI](https://maybe.ai) platform. Upload files, read and write data, manage worksheets, add charts, apply formatting, and more — all via natural language.

## Scripts

Ready-to-run curl examples are in the [`scripts/`](./scripts/) folder. Each script reads credentials from environment variables — no hardcoded tokens.

```bash
export MAYBEAI_API_TOKEN=your_token_here
export DOC_ID=your_document_id_here          # needed by most scripts

bash scripts/01-file-management.sh   # upload, import, list, rename, delete, export
bash scripts/02-read-data.sh         # read sheet, list worksheets, versions
bash scripts/03-write-data.sh        # update range, append rows, copy range
bash scripts/04-rows-columns.sh      # insert/delete/move rows & columns, widths/heights
bash scripts/05-worksheets.sh        # create, rename, move, duplicate, delete worksheets
bash scripts/06-formulas.sh          # calc single/batch formulas, recalculate all
bash scripts/07-charts-pictures.sh   # add/edit/delete charts and pictures
bash scripts/08-formatting.sh        # freeze panes, auto filter, conditional formats
bash scripts/09-end-to-end.sh        # 3 complete workflow examples (upload→edit→export)
```

> **Requires**: `curl` and `jq`. Install jq with `brew install jq` (macOS) or `apt install jq` (Linux).

---

## Setup

### Get your API token

1. Go to **[https://maybe.ai/user/my-plan](https://maybe.ai/user/my-plan)** in your browser.
   *(Or click your avatar / name at the bottom-left of the app → **My Plan**.)*
2. Find the **API Token** card below the plan summary — it shows a masked Bearer token with copy and reveal buttons.
3. Copy the token and set it as an environment variable:

```bash
export MAYBEAI_API_TOKEN=your_token_here
```

### Required environment variable

| Variable | Description |
|---|---|
| `MAYBEAI_API_TOKEN` | Your MaybeAI Bearer token. Get it from [maybe.ai/user/my-plan](https://maybe.ai/user/my-plan). |

### Base URL

```
https://play-be.omnimcp.ai
```

All authenticated endpoints require the header:

```
Authorization: Bearer <MAYBEAI_API_TOKEN>
```

---

## Quick Reference

| User says | Action |
|---|---|
| "Upload this Excel file" | `POST /api/v1/excel/upload` |
| "Import from URL" | `POST /api/v1/excel/import_by_url` |
| "Read Sheet1 data" | `POST /api/v1/excel/read_sheet` |
| "List my files" | `POST /api/v1/excel/list_files` |
| "List worksheets" | `POST /api/v1/excel/list_worksheets` |
| "Update cells A1:B3" | `POST /api/v1/excel/update_range` |
| "Append new rows" | `POST /api/v1/excel/append_rows` |
| "Insert 2 rows at row 5" | `POST /api/v1/excel/insert_rows` |
| "Delete rows 3–5" | `POST /api/v1/excel/delete_rows` |
| "Add a new worksheet" | `POST /api/v1/excel/write_new_worksheet` |
| "Add a bar chart" | `POST /api/v1/excel/add_chart` |
| "Freeze the header row" | `POST /api/v1/excel/freeze_panes` |
| "Add auto filter" | `POST /api/v1/excel/set_auto_filter` |
| "Calculate formula =SUM(A1:A10)" | `POST /api/v1/excel/calc_formulas` |
| "Export/download the file" | `GET /api/v1/excel/export/{document_id}` |
| "Copy this spreadsheet" | `POST /api/v1/excel/copy_excel` |

---

## API Reference

### File Management

#### Upload Excel File
```
POST /api/v1/excel/upload
Content-Type: multipart/form-data

file: <xlsx file>
user_id: (optional)
```
Returns `{ document_id, uri, ... }`. Use `document_id` (also called `uri`) in all subsequent calls.

#### Import File by URL
```
POST /api/v1/excel/import_by_url
Authorization: Bearer <token>

{ "url": "https://..." }
```
Downloads the file from the URL into MaybeAI storage. Returns `document_id`.

#### List Files
```
POST /api/v1/excel/list_files
Authorization: Bearer <token>

{}
```

#### Search Files
```
POST /api/v1/excel/search_files
Authorization: Bearer <token>

{ "keyword": "sales" }
```

#### Rename File
```
POST /api/v1/excel/rename_file
Authorization: Bearer <token>

{ "uri": "<document_id>", "name": "new_name.xlsx" }
```

#### Delete File
```
POST /api/v1/excel/delete_file
Authorization: Bearer <token>

{ "uri": "<document_id>" }
```

#### Export (Download) File
```
GET /api/v1/excel/export/{document_id}
```
Returns the raw `.xlsx` file.

#### Download File (from GridFS)
```
POST /api/v1/excel/download

{ "uri": "<document_id>" }
```

#### Copy Excel Document
```
POST /api/v1/excel/copy_excel
Authorization: Bearer <token>

{ "uri": "<document_id>" }
```

---

### Reading Data

#### Get Spreadsheet Data (JSON)
```
GET /api/v1/excel/spreadsheets/{doc_id}?gid=<sheet_index>
```
Returns spreadsheet data as JSON. `gid` selects the worksheet (0-indexed).

#### View Spreadsheet (HTML)
```
GET /api/v1/excel/spreadsheets/d/{doc_id}
```
Returns an HTML preview of the spreadsheet.

#### List Worksheets
```
POST /api/v1/excel/list_worksheets

{ "uri": "<document_id>" }
```

#### Read Sheet
```
POST /api/v1/excel/read_sheet

{ "uri": "<document_id>", "sheet": "Sheet1" }
```
Returns all cell data from the specified worksheet.

#### Read Headers
```
POST /api/v1/excel/read_headers

{ "uri": "<document_id>", "sheet": "Sheet1" }
```

#### List Versions
```
POST /api/v1/excel/list_versions

{ "uri": "<document_id>" }
```

#### Read Version
```
POST /api/v1/excel/read_version

{ "uri": "<document_id>", "version": "<version_id>" }
```

---

### Writing & Editing Data

#### Update Range
```
POST /api/v1/excel/update_range
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Sheet1",
  "range": "A1:B3",
  "values": [["Name", "Score"], ["Alice", 95], ["Bob", 87]]
}
```

#### Update Range by Lookup
```
POST /api/v1/excel/update_range_by_lookup
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Sheet1",
  "lookup_column": "ID",
  "lookup_value": "001",
  "updates": { "Status": "Done" }
}
```

#### Clear Range
```
POST /api/v1/excel/clear_range
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "range": "A1:D10" }
```

#### Append Rows
```
POST /api/v1/excel/append_rows
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Sheet1",
  "rows": [["Alice", 95], ["Bob", 87]]
}
```

#### Write New Sheet (full data at once)
```
POST /api/v1/excel/write_new_sheet
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Summary",
  "data": [["Col1", "Col2"], [1, 2], [3, 4]]
}
```

#### Copy Range with Formulas
```
POST /api/v1/excel/copy_range_with_formulas
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Sheet1",
  "src_range": "A1:D10",
  "dst_range": "F1"
}
```

#### Copy Range by Lookup
```
POST /api/v1/excel/copy_range_by_lookup
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "lookup_column": "ID", "lookup_value": "001", "dst_sheet": "Archive" }
```

---

### Row & Column Operations

#### Insert Rows
```
POST /api/v1/excel/insert_rows
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "row": 3, "count": 2 }
```
Inserts `count` blank rows starting at `row` (1-indexed).

#### Delete Rows
```
POST /api/v1/excel/delete_rows
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "row": 3, "count": 2 }
```

#### Move Row
```
POST /api/v1/excel/move_row
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "from_row": 5, "to_row": 2 }
```

#### Move Rows (batch)
```
POST /api/v1/excel/move_rows
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "rows": [5, 6], "to_row": 2 }
```

#### Undo Delete Rows
```
POST /api/v1/excel/undo_delete_rows
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1" }
```

#### Insert Columns
```
POST /api/v1/excel/insert_columns
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "column": "C", "count": 1 }
```

#### Delete Columns
```
POST /api/v1/excel/delete_columns
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "column": "C", "count": 1 }
```

#### Move Column
```
POST /api/v1/excel/move_column
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "from_column": "E", "to_column": "B" }
```

#### Move Columns (batch)
```
POST /api/v1/excel/move_columns
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "columns": ["E", "F"], "to_column": "B" }
```

#### Undo Delete Columns
```
POST /api/v1/excel/undo_delete_columns
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1" }
```

#### Add Header Columns
```
POST /api/v1/excel/add_header_columns
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "columns": ["NewCol1", "NewCol2"] }
```

#### Set Columns Width
```
POST /api/v1/excel/set_columns_width
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "columns": [{"column": "A", "width": 20}] }
```

#### Set Rows Height
```
POST /api/v1/excel/set_rows_height
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "rows": [{"row": 1, "height": 30}] }
```

---

### Worksheet Management

#### Write New Worksheet
```
POST /api/v1/excel/write_new_worksheet
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "NewSheet", "data": [["A", "B"], [1, 2]] }
```

#### Delete Worksheet
```
POST /api/v1/excel/delete_worksheet
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "OldSheet" }
```

#### Rename Worksheet
```
POST /api/v1/excel/rename_worksheet
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "new_name": "Sales" }
```

#### Move Worksheet
```
POST /api/v1/excel/move_worksheet
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Summary", "position": 0 }
```

#### Duplicate Worksheet
```
POST /api/v1/excel/copy_worksheet
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "new_name": "Sheet1_copy" }
```

#### List Worksheets (with versions)
```
POST /api/v1/excel/list_worksheets_version

{ "uri": "<document_id>" }
```

---

### Formulas

#### Calculate Single Formula
```
POST /api/v1/excel/calc-formula
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "formula": "=SUM(A1:A10)" }
```

#### Calculate Multiple Formulas
```
POST /api/v1/excel/calc_formulas
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "sheet": "Sheet1",
  "formulas": [
    { "cell": "B11", "formula": "=SUM(B1:B10)" },
    { "cell": "C11", "formula": "=AVERAGE(C1:C10)" }
  ]
}
```

#### Recalculate All Formulas
```
POST /api/v1/excel/recalculate_formulas
Authorization: Bearer <token>

{ "uri": "<document_id>" }
```

---

### Charts

#### Add Chart
```
POST /api/v1/excel/add_chart
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "worksheet_name": "Sheet1",
  "cell": "E2",
  "chart": {
    "type": "bar",
    "series": [{ "name": "Sales", "categories": "Sheet1!A2:A10", "values": "Sheet1!B2:B10" }],
    "title": { "name": "Monthly Sales" }
  }
}
```
Supported chart types: `line`, `bar`, `col`, `pie`, `scatter`, `area`, `doughnut`, `radar`.

#### Edit Chart
```
POST /api/v1/excel/set_chart
Authorization: Bearer <token>

{ "uri": "<document_id>", "worksheet_name": "Sheet1", "chart_id": 1, "chart": { ... } }
```

#### Delete Chart
```
POST /api/v1/excel/delete_chart
Authorization: Bearer <token>

{ "uri": "<document_id>", "worksheet_name": "Sheet1", "chart_id": 1 }
```

---

### Pictures

#### Add Picture
```
POST /api/v1/excel/add_picture
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "cell": "D2", "picture_url": "https://..." }
```

#### Read Picture
```
POST /api/v1/excel/read_picture

{ "uri": "<document_id>", "sheet": "Sheet1" }
```

#### Delete Picture
```
POST /api/v1/excel/delete_picture
Authorization: Bearer <token>

{ "uri": "<document_id>", "sheet": "Sheet1", "picture_id": 1 }
```

---

### Formatting

#### Freeze Panes
```
POST /api/v1/excel/freeze_panes
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "worksheet_name": "Sheet1",
  "freeze_rows": 1,
  "freeze_columns": 0
}
```
Set `freeze_rows: 1` to lock the header row while scrolling.

#### Set Auto Filter
```
POST /api/v1/excel/set_auto_filter
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "worksheet_name": "Sheet1",
  "auto_filter": {
    "ref": "A1:F100",
    "filter_columns": []
  }
}
```

#### Remove Auto Filter
```
POST /api/v1/excel/remove_auto_filter
Authorization: Bearer <token>

{ "uri": "<document_id>", "worksheet_name": "Sheet1" }
```

#### Set Conditional Formats
```
POST /api/v1/excel/set_conditional_formats
Authorization: Bearer <token>

{
  "uri": "<document_id>",
  "worksheet_name": "Sheet1",
  "formats": [
    {
      "sqref": "B2:B100",
      "type": "cell",
      "criteria": ">",
      "value": "90",
      "format": { "font": { "color": "FF0000" } }
    }
  ]
}
```

---

## Common Workflows

### Workflow 1: Upload and read a file

```
1. Upload: POST /api/v1/excel/upload  → get document_id
2. List sheets: POST /api/v1/excel/list_worksheets  {"uri": "<document_id>"}
3. Read data: POST /api/v1/excel/read_sheet  {"uri": "<document_id>", "sheet": "Sheet1"}
```

### Workflow 2: Create a report from scratch

```
1. Upload an empty template or import existing file
2. Write data: POST /api/v1/excel/update_range
3. Add header freeze: POST /api/v1/excel/freeze_panes  {"freeze_rows": 1}
4. Add auto filter: POST /api/v1/excel/set_auto_filter
5. Add summary chart: POST /api/v1/excel/add_chart
6. Export: GET /api/v1/excel/export/{document_id}
```

### Workflow 3: Update existing data

```
1. Find file: POST /api/v1/excel/search_files  {"keyword": "sales"}
2. Read current data: POST /api/v1/excel/read_sheet
3. Update changed rows: POST /api/v1/excel/update_range_by_lookup
4. Recalculate: POST /api/v1/excel/recalculate_formulas
```

### Workflow 4: Bulk data append

```
1. Identify document_id (list_files or upload)
2. Append new rows: POST /api/v1/excel/append_rows
3. Read back to verify: POST /api/v1/excel/read_sheet
```

---

## Notes

- **`uri` / `document_id`**: These terms are interchangeable throughout the API. The value returned from `/upload` or `/import_by_url` is used as `uri` in all body parameters.
- **Range format**: Use Excel-style ranges like `A1`, `A1:B10`, `A:A`.
- **Row/column indexing**: Row numbers are 1-indexed (row 1 = first data row). Columns use Excel letters (`A`, `B`, ...).
- **Authentication**: Endpoints marked `AUTH` require `Authorization: Bearer <MAYBEAI_API_TOKEN>`. Public endpoints work without a token.
- **Spreadsheet viewer URL**: `maybe.ai/docs/spreadsheets/d/{doc_id}` renders a live HTML preview of the file.
