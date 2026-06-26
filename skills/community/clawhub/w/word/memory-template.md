# Memory Template — Word

Create `~/word/memory.md` with this structure:

```markdown
# Word Memory

## Status
status: active
version: 1.0.0
last_verified: YYYY-MM-DD
platform: macOS
control_path: osascript
word_attach_mode: attach-existing | launch-new | mixed

## Safety Defaults
- Accept all changes: ask every time
- Reject all changes: ask every time
- Close without save: blocked unless user confirms
- Risky cleanup: prefer Save As or document copy first

## Environment Notes
- Word version:
- Default control shell:
- Typical document locations:
- Preferred export folder:
- Known review policy:

## Document Notes
- Store only document identifiers, stable paths, and non-sensitive structure notes
- Never paste document contents, secrets, or personal information here

## Recent Incidents
- YYYY-MM-DD: short failure signature -> short fix
```

## Storage Rules

- Keep only reusable environment facts and safety preferences.
- Do not store document body text unless the user explicitly asks for a local note.
- Put repeatable failures in `~/word/incidents.md`.
- Put non-sensitive recurring document metadata in `~/word/document-notes.md`.

## Optional Companion Files

`~/word/incidents.md`:

```markdown
# Word Incidents

## YYYY-MM-DD
- Symptom:
- Document:
- Cause:
- Fix:
```

`~/word/document-notes.md`:

```markdown
# Document Notes

## Document: /absolute/path/to/file.docx
- Default view:
- Review mode:
- Export target:
- Known quirks:
```
