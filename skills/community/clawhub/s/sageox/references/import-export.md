# Import/Export — Knowledge Bridge

Import documents, recordings, and OpenClaw memory into SageOx. Export
SageOx knowledge as portable local files.

## Import into SageOx

### File import

```bash
ox import <file> [--text <extracted.md>] [--date YYYY-MM-DD] [--team <id>] [--force]
```

Import documents (PDF, markdown, Word, etc.) into team context. Files
are stored as LFS pointers with metadata in `data/docs/YYYY/MM/DD/{slug}/`.

- `--text` — path to pre-extracted text/markdown for indexing
- `--date` — override file modification date
- `--force` — re-import even if content hash matches an existing import
- `--team` — explicit team (auto-discovers if single team)

### Video/URL import

```bash
ox import <url> --title "..." [--team <id>]
```

Import video URLs (Loom, Cap, direct video links) for cloud processing.
The server transcribes, summarizes, and extracts facts.

**Check processing status:**

```bash
ox import --status <recording_id> [--watch]
```

`--watch` polls until processing completes or fails.

**List all imports:**

```bash
ox import --list
```

### Bridge: OpenClaw memory → SageOx

To push knowledge from OpenClaw memory into SageOx team context:

1. Read the relevant `~/.openclaw/memory/*.json` file.
2. Extract the content to import.
3. Choose the import method:

   **As an observation** (for facts, decisions, conventions):
   ```bash
   ox memory put '{"content": "<extracted content>"}'
   ```
   Observations are processed during the next distill run and become
   part of the team's memory layers.

   **As a document** (for structured content):
   Write the content to a temp markdown file, then:
   ```bash
   ox import /tmp/extracted-knowledge.md --team <team_id>
   ```

4. If multiple teams exist, ask the user which team to import into.
5. Track the import in `~/.openclaw/memory/sageox-bridge-state.json`:
   ```json
   {
     "updated_at": "RFC3339",
     "imports": [
       {"source": "~/.openclaw/memory/file.json", "team_id": "...", "imported_at": "RFC3339"}
     ]
   }
   ```

## Export from SageOx (portable extraction)

There is no `ox export` command. Knowledge flows out via query, distill
history, and fetch. The agent orchestrates the extraction:

### Extract a decision or convention

1. `ox query "<topic>" --source team --limit 5`
2. Present results to the user.
3. If the user wants to save: write the relevant content to a local
   markdown file at a user-chosen path.

### Extract distilled insights

1. `ox distill history list --since <duration> --layer daily --format json`
2. Show available entries.
3. `ox distill history show <id> --format content`
4. Write content to a local file at user-chosen path.

### Hydrate an imported file

```bash
ox fetch <pointer-file> [-o <output-path>]
```

Downloads the actual content behind an LFS pointer (PDF, image, etc.)
from the LFS server. Caches locally and verifies SHA256.

### Track exports

Record exports in `~/.openclaw/memory/sageox-bridge-state.json`:

```json
{
  "exports": [
    {"query": "auth patterns", "team_id": "...", "output_path": "/path/to/file.md", "exported_at": "RFC3339"}
  ]
}
```

This prevents re-exporting the same content and provides an audit trail.
