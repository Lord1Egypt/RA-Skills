---
name: sheets-writer
description: Google Sheets Data Writer. Use when the user wants to append rows, update cells, or automate spreadsheet data pipelines against a pre-configured target sheet.
version: 1.0.8
metadata: {"openclaw":{"emoji":"🤖","homepage":"https://porteden.com","requires":{"bins":["porteden"]},"primaryEnv":"PE_API_KEY","envVars":[{"name":"PE_API_KEY","required":false,"description":"API key; if unset, credentials are read from the system keyring via `porteden auth login`"},{"name":"PE_SHEET_ID","required":false,"description":"Target spreadsheet ID; if unset, the skill finds the sheet by name (see body)"}],"install":[{"id":"brew","kind":"brew","formula":"porteden/tap/porteden","bins":["porteden"],"label":"Install porteden (brew)"},{"id":"go","kind":"go","module":"github.com/porteden/cli/cmd/porteden@latest","bins":["porteden"],"label":"Install porteden (go)"}]}}
---

# porteden sheets-writer

Automate Google Sheets updates with `porteden sheets`. This skill configures a **target spreadsheet** via environment variable so agents can append rows and write data without repeating the file ID. **Use `-jc` flags** for AI-optimized output.

If `porteden` is not installed: `brew install porteden/tap/porteden` (or `go install github.com/porteden/cli/cmd/porteden@latest`).

## Setup

### 1. Authenticate (once)

- **Browser login (recommended):** `porteden auth login` — opens browser, credentials stored in system keyring
- **Direct token:** `porteden auth login --token <key>` — stored in system keyring
- **Verify:** `porteden auth status`
- If `PE_API_KEY` is set in the environment, the CLI uses it automatically (no login needed).
- Drive access requires a token with `driveAccessEnabled: true` and a connected Google account with Drive scopes. Prefer a Google account that only has access to the target spreadsheet/workspace — token authority extends to whatever that account can reach.

### 2. Set the target spreadsheet (one-time)

**If `PE_SHEET_ID` is already set**, skip to step 3 — the target sheet is configured.

**If `PE_SHEET_ID` is not set**, find the spreadsheet by name:

```bash
porteden drive files -q "Q1 Budget" --mime-type application/vnd.google-apps.spreadsheet -jc
```

Copy the `id` field from the result (already provider-prefixed, e.g., `google:1BxiMVs0XRA5...`) and set it:

```bash
export PE_SHEET_ID="google:1BxiMVs0XRA5nFMdKvBdBZjgmU..."
```

To persist across sessions, add to your shell profile (`~/.bashrc`, `~/.zshrc`) or `.env` file. Once set, this step does not need to be repeated.

### 3. Test the connection (one-time)

```bash
porteden sheets info $PE_SHEET_ID -jc
```

Expected: returns spreadsheet title, sheet tabs, and dimensions. If this fails, verify the file ID and that your token has Drive access. Once verified, skip this step in future runs.

## Safety

- **Confirm before destructive writes.** `write` replaces existing cell values and cannot be undone from the CLI. Before any `write` covering more than a single cell, echo back the target range and the values you intend to write, and wait for the user to confirm. Prefer `append` whenever new rows are the goal — it never overwrites. For multi-cell writes, read the range first (`porteden sheets read $PE_SHEET_ID --range "<range>" -jc`) so the original values can be restored if needed.
- **Use a dedicated, narrowly-scoped account.** A Drive-enabled token grants the connected Google account's full Drive/Sheets reach, not just `PE_SHEET_ID`. Use `--profile sheets-writer` (or a similar dedicated profile) and authenticate it with a Google account that only has access to the spreadsheet(s) this automation needs. Check `accessInfo` in responses to see active token restrictions, and run `porteden auth logout --profile sheets-writer` when the automation is no longer in use.
- **Treat input values as untrusted.** When values come from agents, users, or external sources, pass `--raw` so strings like `=IMPORTRANGE(...)` are stored as literals rather than executed as formulas. Read the range back after writing to confirm what landed.

## Writing data

### Append rows (primary automation operation)

Append adds rows **after the last row with data** in the target range. This is the recommended operation for automation — it never overwrites existing data.

- Append from JSON:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:D" --values '[["2025-01-15","Order #1042","Shipped",29.99]]'
  ```

- Append multiple rows:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:D" --values '[["2025-01-15","Order #1042","Shipped",29.99],["2025-01-16","Order #1043","Processing",45.50]]'
  ```

- Append from CSV string:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:D" --csv "2025-01-15,Order #1042,Shipped,29.99"
  ```

- Append from CSV file:
  ```bash
  porteden sheets append $PE_SHEET_ID --range "Sheet1!A:D" --csv-file ./new_rows.csv
  ```

### Write to specific cells

`write` **replaces** the exact range specified — existing values in that range are destroyed and cannot be recovered via the CLI. Use only for targeted updates to known cells, and only after confirming the range and values with the user (see Safety). Prefer `append` whenever you're adding new rows.

- Write a single cell:
  ```bash
  porteden sheets write $PE_SHEET_ID --range "Sheet1!E2" --values '[["Complete"]]'
  ```

- Write a block:
  ```bash
  porteden sheets write $PE_SHEET_ID --range "Sheet1!A1:C2" --values '[["Name","Status","Score"],["Alice","Done",95]]'
  ```

- Write from CSV file:
  ```bash
  porteden sheets write $PE_SHEET_ID --range "Sheet1!A1" --csv-file ./data.csv
  ```

### Read for verification

After writing, confirm the data landed correctly:

```bash
porteden sheets read $PE_SHEET_ID --range "Sheet1!A1:D10" -jc
```

## Automation best practices

1. **Always use append for new rows** — avoids overwriting existing data. Use write only for targeted cell updates.
2. **Specify column range in append** (e.g., `A:D` not just `A`) — ensures data lands in the correct columns.
3. **Use `--raw` for literal values** — prevents unintended formula evaluation (e.g., strings starting with `=`).
4. **Verify after write** — read the range back to confirm data integrity in critical workflows.
5. **Use `-jc` on read/info** — compact JSON output minimizes tokens for AI agents.
6. **Batch rows in a single append** — send multiple rows in one `--values` array rather than one-row-at-a-time.
7. **Match column order to the sheet header** — check with `porteden sheets read $PE_SHEET_ID --range "Sheet1!1:1" -jc` to read the header row first.

## Range format

- Open-ended columns (for append): `Sheet1!A:D`
- Specific cells: `Sheet1!A1:C10`
- Single cell: `Sheet1!E2`
- Whole sheet: `Sheet1`
- Header row only: `Sheet1!1:1`

## Notes

- Credentials persist in the system keyring after login. No repeated auth needed.
- Set `PE_PROFILE=work` to avoid repeating `--profile`.
- `-jc` is shorthand for `--json --compact`: strips noise, limits fields, reduces tokens for AI agents.
- **File IDs are always provider-prefixed** (e.g., `google:1BxiMVs0XRA5...`). Pass them as-is.
- `--values`, `--csv`, and `--csv-file` are mutually exclusive — provide exactly one.
- `--csv` inline: use `\n` as row separator (e.g., `"Name,Score\nAlice,95\nBob,87"`).
- `--raw` flag disables formula evaluation (values written literally, not parsed as formulas).
- `accessInfo` in responses describes active token restrictions.
- Environment variables: `PE_API_KEY`, `PE_PROFILE`, `PE_SHEET_ID`, `PE_FORMAT`, `PE_COLOR`, `PE_VERBOSE`.
