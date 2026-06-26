# Changelog

All notable changes to **Skill Atlas** are documented here.

---

## v3.0.0 — "Skill Atlas · 技能图谱"

> 让每一个技能各归其位，让每一次搜索有所依据。

### What's New

- **🧭 Identity**: Rebranded with tagline "让每一个技能各归其位，让每一次搜索有所依据"
- **📦 Manifest v2.0**: Unified `.skill_manifest.json` as the single source of truth for all skills
  - `invoke_scope`, `layer`, `source_channel` now live in manifest
  - Removed redundant `invoke_scope_registry.json` and `invoke_scope_registry.md`
- **⚡ Core Layer Protection**: Core skills are now skipped by default during batch updates
  - Prevents accidental breakage of system management skills
  - `skill-atlas` self-update requires extra caution (backup recommended)
- **🔄 Unified Layer Management**: All layer operations (promote/demote/pause/resume) now modify `manifest.layer` only
  - No longer depends on `config/scenes.json` layer field
- **📋 Scope Source Clarified**: Skill审视 now explicitly reads `invoke_scope` from manifest
- **💬 Complete Speech Rules**: Added pause/resume utterances to agent 话术规范
- **🛡️ Backup Path Fixed**: Python backup implementation now correctly copies to `backups/<slug>/<timestamp>/` without redundant nesting
- **📊 Core Update Strategy**: Documented that core skills skip batch updates by default

### Changes

| Category | Change |
|----------|--------|
| **Install Flow** | Step 2 now checks `manifest.source_channel` instead of separate registry |
| **Update Flow** | Reads `manifest.source_channel` instead of `manifest.source` |
| **Upgrade/Demote** | Modifies `manifest.layer` instead of `config/scenes.json` |
| **审视** | "Trigger condition" now reads from manifest, not skill front matter |
| **Backup** | Fixed path: `backup_dir` directly (no extra `skills/<slug>/` nesting) |
| **Batch Update** | Core layer skipped by default; references "core layer strategy" section |
| **Speech Rules** | Added "pause" and "resume" utterances |
| **Version** | Reset to v3.0.0 for fresh identity |

### Data Migration

Skills previously tracked in `invoke_scope_registry.json` have been migrated to `.skill_manifest.json` with the following mapping:

| Old Field | New Field |
|-----------|-----------|
| N/A (separate file) | `invoke_scope` — now in manifest |
| N/A (separate file) | `layer` — now in manifest |
| N/A (separate file) | `source_channel` — now in manifest |
| `manifest.skills[].source` | `manifest.skills[].source` (kept) |
| `manifest.skills[].version` | `manifest.skills[].version` (kept) |

### Files

```
workspace/
├── skills/skill-atlas/
│   ├── SKILL.md           # v3.0.0
│   ├── reference.md       # v3.0.0
│   └── scripts/
│       └── skill_atlas.py
├── .skill_manifest.json  # v2.0 (manifest_version)
└── backups/
```

---

## v2.x — Internal Development

Pre-v3.0 versions were internal development iterations. Changelog begins here at v3.0.0.

---

_Last updated: 2026-04-10 v3.0.0_
