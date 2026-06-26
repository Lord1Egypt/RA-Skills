# Quick Note Skill

Fast note-taking and snippet storage for OpenClaw.

## Features

- ✅ Quick save notes with one command
- ✅ Tag-based organization
- ✅ Search functionality
- ✅ Persistent storage in workspace
- ✅ Automatic ID and timestamp

## Installation

Already included in workspace skills.

## Usage

### Save a Note
```bash
bash skills/quick-note-1.0.0/scripts/note.sh add "Meeting at 3pm"
bash skills/quick-note-1.0.0/scripts/note.sh add "API key: xxx" --tags important,api
```

### Search Notes
```bash
bash skills/quick-note-1.0.0/scripts/note.sh search "meeting"
```

### List Recent
```bash
bash skills/quick-note-1.0.0/scripts/note.sh list
bash skills/quick-note-1.0.0/scripts/note.sh list 20
```

### By Tag
```bash
bash skills/quick-note-1.0.0/scripts/note.sh tag "important"
```

## License

MIT
