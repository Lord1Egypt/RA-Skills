# Live Control Patterns — Word

These are operational patterns, not generic tutorials.

## 1. Read the active document on macOS

```bash
osascript <<'APPLESCRIPT'
tell application "Microsoft Word"
  if not running then return "Word not running"
  if (count of documents) is 0 then return "No open documents"
  return name of active document
end tell
APPLESCRIPT
```

Why: active document identity must be verified before any selection-based action.

## 2. Insert text at the current selection

```bash
osascript <<'APPLESCRIPT'
tell application "Microsoft Word"
  set content of text object of selection to "Ready"
end tell
APPLESCRIPT
```

Why: selection-based insertions are powerful but risky, so verify selection context first.

## 3. Update fields before export

```bash
osascript -e 'tell application "Microsoft Word" to update fields of active document'
```

Why: TOC, references, and fields can be stale until Word refreshes them.

## 4. Export the live document to PDF

```bash
osascript -e 'tell application "Microsoft Word" to save as active document file format format PDF file name "/absolute/path/to/output.pdf"'
```

Why: this uses Word's own layout engine instead of reconstructing the document elsewhere.

## 5. Leave the user's session intact

- Do not quit Word if you attached to a user-owned session.
- Do not close unrelated documents.
- Report which document and view were left active at the end.
