---
name: vortex-notes
description: Read, search, and write the user's Vortex Notes vault — plain-markdown notes with local semantic search, daily notes, and durable facts with supersession. Use for "note this down", "remember that…", "what do my notes say about…", and daily journaling.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["vortex-notes"] },
        "install":
          [{ "id": "npm", "kind": "npm", "package": "vortex-notes", "bins": ["vortex-notes"] }],
      },
  }
---

# Vortex Notes

The user's knowledge base is a folder of plain markdown ("the vault"). You can
work with it two ways — prefer the CLI for search, plain file reads for content.

Find the vault: `$VORTEX_NOTES_VAULT` if set, else `~/VortexNotes`, else ask once
and remember it.

## Search (always start here)

```
vortex-notes search "<query>" --vault <vault>
```

Hybrid keyword + multilingual semantic search — natural-language queries work
("that idea about pricing"), and queries in one language find notes in another.
Results show `path › heading` plus a snippet; read the file for full content.

## Read

Notes are plain `.md` files with YAML frontmatter (`title`, `tags`, `created`,
`updated`). `[[Wikilinks]]` reference other notes by title or filename —
follow them for context.

## Write

- **Daily journal** (observations, decisions, things that happened):
  append a bullet to `daily/YYYY-MM-DD.md` in the vault:
  `- **HH:MM** <entry>`  — create the file with a `title: YYYY-MM-DD` frontmatter
  and a `daily` tag if it doesn't exist.
- **Durable facts** ("remember that X"): append to `memory/facts.md`
  (or `memory/<topic>.md`) as `- **YYYY-MM-DD** <fact> \`^f-<8 random chars>\``.
  If the fact REPLACES an earlier one, strike the old line through
  (`- ~~old line~~ → superseded YYYY-MM-DD by \`^f-new\``) and keep it —
  never delete history.
- **New notes**: create `<kebab-case-title>.md` (optionally in a folder) with
  frontmatter `title:` and `created:`/`updated:` ISO timestamps.
- **Edits**: edit surgically (append a section, fix a line). Never rewrite a
  whole note unless asked. Preserve frontmatter; bump `updated`.

After any write, the vault's watcher reindexes automatically — no extra step.

## MCP alternative

If this agent supports MCP, `vortex-notes mcp --vault <vault>` (stdio) exposes
task-shaped tools (`search_notes`, `read_note`, `write_note`, `edit_note`,
`append_daily`, `remember` with supersession, `build_context`) and a
`--read-only` flag. Prefer MCP when available — `remember` and `build_context`
encode the conventions above.
