---
name: quick-note
description: Fast note-taking and snippet storage. Use when user says "note:", "remember this", "save snippet", "quick note", or wants to save/read short text snippets.
---

# Quick Note

Fast note-taking and snippet storage with tags and search.

## File Location

`notes/quick-notes.md` in workspace root

## Commands

### Create Note
When user says: "note: X", "remember: X", "save this: X"

**PowerShell (Windows):**
```powershell
powershell -ExecutionPolicy Bypass -File skills/quick-note-1.0.0/scripts/note.ps1 add "Meeting at 3pm" --tags important,work
```

**Bash (Linux/Mac/WSL):**
```bash
bash skills/quick-note-1.0.0/scripts/note.sh add "Meeting at 3pm" --tags important,work
```

Examples:
```bash
bash skills/quick-note-1.0.0/scripts/note.sh add "Meeting at 3pm tomorrow"
bash skills/quick-note-1.0.0/scripts/note.sh add "API key: xxx123" --tags important,api
bash skills/quick-note-1.0.0/scripts/note.sh add "Code snippet: console.log('test')" --tags code
```

### Search Notes
When user says: "find note about X", "search notes for X"
```bash
bash skills/quick-note-1.0.0/scripts/note.sh search "<keyword>"
```

### List Recent Notes
When user says: "show recent notes", "list notes"
```bash
bash skills/quick-note-1.0.0/scripts/note.sh list [--limit 10]
```

### List by Tag
When user says: "show notes tagged X"
```bash
bash skills/quick-note-1.0.0/scripts/note.sh tag "<tagname>"
```

### Delete Note
When user says: "delete note X", "remove note about X"
```bash
bash skills/quick-note-1.0.0/scripts/note.sh delete "<note-id>"
```

## Note Format

```markdown
# Quick Notes

## [ID-001] 2026-03-10 10:30
**Tags:** important, meeting
Meeting at 3pm tomorrow with team

---

## [ID-002] 2026-03-10 10:35
**Tags:** code, snippet
```javascript
console.log('Hello World');
```

---
```

## Response Format

When showing a note:
```
📝 **Note #ID-001** (2026-03-10 10:30)
**Tags:** #important #meeting

Meeting at 3pm tomorrow with team
```

When searching:
```
🔍 Found 2 notes matching "api":

📝 #ID-003 (2026-03-10)
API endpoint: https://api.example.com

📝 #ID-005 (2026-03-09)
API key stored in .env file
```
