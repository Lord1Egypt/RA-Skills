# Changelog

## 0.1.1

- Exclude the test harness from ClawHub publish bundles so installed skill scans only inspect runtime files.

## 0.1.0

First public release. savenow is a single-purpose OpenClaw + Telegram skill: it picks durable notes from the active conversation and writes them to `memory/YYYY-MM-DD.md` with a preview-and-confirm flow.

### Highlights

- **Semantic dedupe via agent actions.** The agent reads today's memory before extracting candidates and labels each one with `action: "add" | "skip" | "merge"`. Merges are applied in-place to the matched section. The merge script keeps a lexical Jaccard check as a safety-net fallback for `add` entries.
- **Preview / apply / cancel / auto flow.** `/savenow` previews by default and writes nothing. The preview is rendered as a markdown diff in chat with Telegram inline `✅ Apply` and `❌ Cancel` buttons. `/savenow auto` skips the preview and writes directly. `/savenow apply` and `/savenow cancel` act on the most recent pending preview.
- **Pending state** at `temp/savenow-pending.json` with a 30-minute TTL plus session and topic guards. A second preview in another topic clobbers the pending; the apply step refuses if the pending doesn't match the current session.
- **In-place merges.** When new bullets are merged into an existing section, the script appends them in place and adds a single trailing `- (merged HH:MM)` marker bullet. A second merge into the same section replaces the marker rather than stacking.
- **Zero runtime dependencies.** Scripts use only Node's standard library. Node 18 or newer.
- **Test suite.** 12 cases covering add, skip, merge, fallback, marker replacement, mixed batch, preview output, and pending writing. Runs cross-platform on Linux, macOS, and Windows on Node 18, 20, and 22.

### Commands

| Command                       | Behavior                                                                  |
|-------------------------------|---------------------------------------------------------------------------|
| `/savenow`                    | Preview only. Renders the markdown diff plus Apply / Cancel buttons.      |
| `/savenow apply`              | Write the most recent pending preview.                                    |
| `/savenow cancel`             | Discard the pending preview without writing.                              |
| `/savenow auto`               | Extract and write directly, skipping the preview.                         |
| `/savenow auto <sessionKey>`  | Auto on an explicit session.                                              |
| `/savenow list`               | List same-topic candidate sessions without writing.                       |
| `/savenow <sessionKey>`       | Preview against an explicit session.                                      |

### Entries JSON schema

The agent writes candidates to `temp/savenow-entries.json` with this shape:

```json
{
  "candidate_index": 0,
  "title": "...",
  "bullets": ["..."],
  "action": "add" | "skip" | "merge",
  "merge_target_title": "...",
  "reason": "..."
}
```

The bare `{ "title": "...", "bullets": [...] }` shape (no `action` field) is also accepted and treated as `"add"` — useful for callers that don't yet emit the full schema.

### Scope

OpenClaw + Telegram by design. The skill depends on `sessions_list` / `sessions_history`, the runtime `MessageThreadId`, and Telegram inline keyboards. Vanilla Claude Code, CLI, and web surfaces are out of scope.

### Notes

- Memory file names use the local date stamp. Sessions that span midnight may write to "yesterday".
- Pending state is workspace-singleton. Only one pending preview at a time per workspace.
