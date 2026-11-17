# Environment Gotchas (word-cursor-insert)

## 1. PowerShell COM stdout is GARBLED in this environment
Running PowerShell that touches Word COM returns only the console title
(`;管理员: ...powershell.EXE`) plus a BELL char; `Write-Output` results are lost.
- NEVER rely on PowerShell stdout for Word automation here.
- Prefer Python + `pywin32` (`win32com.client.GetActiveObject("Word.Application")`).
  Python stdout is clean, so results print and are visible directly.
- If PowerShell must be used, write results to a temp file and `Read` it back —
  but that costs an extra round trip.

## 2. Read cursor context with a BOUNDED window, never the whole document
`doc.Range(0, sel.Start).Text` and `doc.Range(sel.End, doc.Content.End).Text`
pull the ENTIRE prefix/suffix over COM => O(document size). On large docs this
is slow AND bloats the agent context.
- Use `doc.Range(max(sel.Start-WIN,0), sel.Start).Text` and
  `doc.Range(sel.End, min(sel.End+WIN, doc_end)).Text` with WIN~300.
- Prefer structural queries: `sel.Information(12)` (in-table?),
  `sel.Paragraphs(1).Range.Text` (current paragraph).
- Cost stays O(window), independent of document length.

## 3. Do NOT re-run a Word COM call just because terminal output looked garbled
A garbled/empty terminal does NOT mean the operation failed. Re-running
`TypeText`/`Tables.Add` duplicates the insertion. Judge success from the
result file / stdout, and only act once.

## 4. Chinese text goes through FILES, not the command line
Pass CSV paths that are ASCII (copy the source to a temp ASCII path if needed)
and have the script read the file. Avoid embedding long Chinese strings in
shell/PowerShell commands.

## 5. pywin32 must be installed in the managed venv
`.../python/envs/default/Scripts/pip install pywin32` (cp313 => pywin32-312).
Run scripts with `.../python/envs/default/Scripts/python.exe script.py`.

## 6. Context-aware insertion (don't blind-insert)
- If the cursor sits inside a sentence expecting a single value (e.g.
  `该企业共有 ___ 人`), insert just that value inline (`--text "7"`), do NOT
  drop a whole table. For a scalar result (a count/sum), skip the CSV export
  step entirely — compute the value and pass it straight via `--text`.
- If the cursor is at a free location and the source is a list/table, insert a
  formatted table (title + bold header + borders + autofit).
- Always inspect context (step 2) BEFORE choosing the mode.

## 7. Moving / clearing the cursor blindly corrupts the document
`Selection.MoveLeft(1,1)` + `Selection.Delete(1,1)` to "clear the char before the
cursor" is FRAGILE: an off-by-one drops the WRONG character (observed in practice:
deleted "有" instead of "7", turning "该企业共有7人" into "该企业共7人").
- The insert script ONLY does `TypeText` at the CURRENT selection — it never moves
  the cursor. Do NOT add blind cursor moves to "reposition" or "clear".
- To re-insert elsewhere, have the user place the cursor at a fresh blank; never
  auto-clear (auto-clearing is exactly what caused duplication / off-by-one).
- If you must address a specific character, use Range-based addressing
  (`doc.Range(start+i, start+i+1).Delete()`), never blind `MoveLeft`/`Delete`.
