# Multi-device sync & backup

This document covers how to safely back up, sync, or migrate Soul Archive data — especially when you're on multiple machines.

## Where your data lives

```
~/.agent-commons/skills_data/soul-archive/
```

To check the actual path on your machine:

```bash
python scripts/soul_paths.py
```

## Recommended sync strategy

Soul Archive data lives under [Agent Commons](https://github.com/dqsjqian/agent-commons), so backing up the whole tree gives you everything at once:

```bash
# Private git on your own server
cd ~/.agent-commons && git init && git add . && git commit -m "snapshot"

# rsync to a NAS / external drive / another machine
rsync -avz --delete ~/.agent-commons/ user@host:~/.agent-commons/
```

One directory, all your AI-agent state.

## Privacy layering (important)

Soul Archive data has **two sensitivity levels**:

| Sensitivity | Files | Should sync? |
|---|---|---|
| **Public-ish** | `profile.json`, `config.json`, `identity/`, `style/`, `workflow/`, `aspirations.json` | ✅ usually safe — your basic profile and preferences |
| **Highly sensitive** | `memory/episodic/`, `memory/emotional/`, `agent/corrections.jsonl`, `agent/reflections.jsonl` | ⚠️ contains specific events, emotional patterns, AI self-critique logs |

**Recommended `.gitignore` if you version-control your soul data**:

```gitignore
# Highly sensitive — keep out of any git history
skills_data/soul-archive/memory/episodic/
skills_data/soul-archive/memory/emotional/
skills_data/soul-archive/agent/corrections.jsonl
skills_data/soul-archive/agent/reflections.jsonl
skills_data/soul-archive/agent/episodes/
skills_data/soul-archive/*.enc-bak

# OS clutter
.DS_Store
```

## Migrating to a new machine

```bash
# On the old machine: pack it up
tar czf soul-backup.tgz -C ~/.agent-commons skills_data/soul-archive

# Transfer soul-backup.tgz to the new machine.

# On the new machine:
mkdir -p ~/.agent-commons/skills_data/
tar xzf soul-backup.tgz -C ~/.agent-commons/
```

Or simpler with rsync:

```bash
rsync -avz ~/.agent-commons/skills_data/soul-archive/ \
  newhost:~/.agent-commons/skills_data/soul-archive/
```

## Multi-device gotchas

- **Don't sync `*.enc-bak` if you're regenerating encryption keys per machine** — the backups won't be readable.
- **Don't run two machines extracting at the same time without sync** — you'll get conflicting writes to JSON files (last write wins).
- **`config.json` is per-user, not per-machine** — sync it freely.
- **`registry.json` (Agent Commons protocol layer) is also per-user** — agents on different machines will all show up in it; that's fine.

## What NOT to do

- ❌ Don't push your soul data to a **public** git repository, even with `memory/` excluded — `identity/basic_info.json` and `aspirations.json` still contain personal info.
- ❌ Don't sync via cloud providers that read your file contents (e.g. third-party "AI-enhanced" backup services).
- ❌ Don't symlink across two physical machines via NFS / SMB and expect concurrent writes to be safe — Soul Archive's JSON files are not designed for multi-writer concurrency.
