# Setup — Word

## First-Time Setup

### 1. Verify the official control path on this machine

```bash
osascript -e 'tell application "Microsoft Word" to get name'
```

### 2. Initialize local memory

Create the skill directory:

```bash
mkdir -p ~/word
```

Create `~/word/memory.md` from `memory-template.md`.

Create these optional note files if you expect repeated Word automation:

```bash
touch ~/word/incidents.md ~/word/document-notes.md
```

### 3. Capture the minimum environment facts

Add a few stable facts to `~/word/memory.md`:

- platform in use: macOS
- default control path: `osascript`
- whether Word is usually already open before automation starts
- preferred export folder for PDF or DOCX copies

Do not store document contents, secrets, or credentials in these notes.

### 4. Register the skill in workspace memory

Add a short note to your workspace memory or AGENTS guidance saying that Word Desktop tasks should route to `word` when the job depends on the live app session.

Good trigger examples:

- document is already open in Word
- need comment or tracked-change actions
- need selection-aware edits
- need PDF export that matches current Word view or layout

### 5. Decide your safety defaults

Record these preferences in natural language:

- whether accept-all or reject-all always requires confirmation
- whether close-without-save is always blocked
- whether the agent may create a copy before risky cleanup
- whether review mode changes are allowed without extra approval

### 6. First verification

Run one minimal read-only app check:

```bash
osascript <<'APPLESCRIPT'
tell application "Microsoft Word"
  if it is running then
    get name of active document
  else
    return "Word not running"
  end if
end tell
APPLESCRIPT
```

If this fails, stop and use `troubleshooting.md` before attempting document changes.

## When "Done"

Setup is done when:

- at least one official control path works
- `~/word/memory.md` exists
- safety defaults are written down
- a minimal read-only app check succeeds
