# video-finder — Agent Guidelines

## Project Nature

This is an **OpenClaw agent skill**, not a traditional application. The core logic lives in [SKILL.md](./SKILL.md) — a thin orchestrator that delegates to sub-skills. There is no build step, no test suite, and no runtime code.

## Architecture (Decoupled)

```
video-finder/
├── SKILL.md                          ← Orchestrator: YAML frontmatter + phase routing
├── preferences.md                    ← User preference init & management
├── proxy.md                          ← Network probing & proxy config
├── search.md                         ← Multi-engine search & filtering
├── download.md                       ← yt-dlp download + progress tracking
├── feedback.md                       ← Post-viewing feedback & tag maintenance
├── preferences.example.json          ← Template for user preferences
├── proxy.example.json                ← Template for proxy config
├── history.example.md                ← Template for download history
├── tracking/downloads.example.json   ← Template for download state
├── (.gitignore)                      ← Runtime files not committed
├── AGENTS.md                         ← This file
├── README.md                         ← End-user docs
└── LICENSE
```

## Skill Dependency Graph

```
video_finder (orchestrator)
  ├── video_finder_preferences
  ├── video_finder_proxy
  │     └── (standalone)
  ├── video_finder_search
  │     ├── → video_finder_preferences (reads prefs for filtering)
  │     └── → video_finder_proxy (site reachability probes)
  ├── video_finder_download
  │     ├── → video_finder_preferences (reads download_dir)
  │     └── → video_finder_proxy (proxy routing)
  └── video_finder_feedback
        └── → video_finder_preferences (writes tag_weights / author_weights)
```

## Key Conventions

### Placeholder Syntax
- `{{{user}}}` is a runtime placeholder — never edit or resolve it.

### Phase Workflow
The orchestrator routes through 6 phases, each delegated to a sub-skill:
0. **Proxy detection** → `video_finder_proxy`
1. **Task intake** → orchestrator (parse keywords vs links, route)
2. **Search** → `video_finder_search`
3. **Download** → `video_finder_download`
4. **Result** → orchestrator (report, append history)
5. **Feedback loop** → `video_finder_feedback`

### When to Edit Which File

| Change | File to Edit |
|--------|-------------|
| Add/remove trigger keywords | `SKILL.md` (YAML frontmatter) |
| Change preference questions or schema | `preferences.md` |
| Modify proxy probing logic | `proxy.md` |
| Change search engine selection or filtering | `search.md` |
| Modify download progress tracking | `download.md` |
| Tune feedback timing or tag extraction | `feedback.md` |
| Reorder/add/remove phases | `SKILL.md` (orchestrator) |

## Security

- `proxy.json` contains plaintext proxy credentials. Never echo or log its contents. Use `***` in examples.
- In code examples, always redact passwords.

