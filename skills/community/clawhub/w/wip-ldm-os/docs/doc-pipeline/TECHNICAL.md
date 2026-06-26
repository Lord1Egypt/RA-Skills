# Documentation Pipeline: Technical Details

## File Paths

### Repo doc templates (in the LDM OS repo)

```
shared/docs/*.md.tmpl           Templates for home docs
shared/rules/*.md               Source for agent rules
shared/boot/                    Boot sequence config
```

Templates use placeholders from `~/.ldm/config.json` (workspace path, agent names, org name, etc.).

### Installed locations

```
~/.ldm/config.json                       Org config (agents, paths, co-authors)
~/.ldm/shared/rules/*.md                 Agent rules (source for ~/.claude/rules/)
~/.ldm/shared/dev-guide-*.md             Org dev guide
~/.ldm/shared/boot/                      Boot sequence config
~/.ldm/shared/prompts/                   Cron prompts
~/.ldm/templates/                        CLAUDE.md templates, install prompt, etc.
~/wipcomputerinc/library/documentation/  Personalized human docs (from templates)
~/.claude/rules/                         Deployed rules (copied from ~/.ldm/shared/rules/)
~/.claude/CLAUDE.md                      Level 1 global (generated from template + config)
```

### What ldm install deploys

| Source | Destination | When |
|--------|------------|------|
| `shared/rules/*.md` | `~/.ldm/shared/rules/` then `~/.claude/rules/` | Every install |
| `shared/docs/*.md.tmpl` | `~/wipcomputerinc/library/documentation/` | Every install |
| `shared/boot/` | `~/.ldm/shared/boot/` | Every install |
| `shared/prompts/` | `~/.ldm/shared/prompts/` | Every install |
| `shared/templates/` | `~/.ldm/templates/` | Every install |

**Known bug (April 2026):** The installer currently deploys shared rules on `ldm init` (first install) but not on every `ldm install`. This means rule updates in new versions don't propagate until the user re-initializes. This needs to be fixed so rules deploy on every install.

**Known bug (April 2026):** The installer previously deployed home docs to `settings/docs/`. This path was renamed to `library/documentation/` on March 28, 2026. The installer must deploy to the correct path.

## How templates work

Home doc templates at `shared/docs/*.md.tmpl` contain placeholders:

```
Workspace: {{workspace}}
Agents: {{agents}}
```

The installer reads `~/.ldm/config.json`, substitutes the placeholders, and writes the personalized docs to `~/wipcomputerinc/library/documentation/`.

## CLAUDE.md cascade

Three levels. Claude Code reads all of them, walking up from CWD:

```
Level 1: ~/.claude/CLAUDE.md              Global. ~30 lines. Universal rules.
Level 2: ~/wipcomputerinc/CLAUDE.md       Workspace. ~150 lines. Org context.
Level 3: <repo>/CLAUDE.md                 Per-repo. ~50-86 lines. Repo-specific.
```

After context compaction, CWD may shift to a repo. Without Level 3, all context is lost. Every repo must have a CLAUDE.md.

## Config paths (correct as of April 2026)

References in CLAUDE.md and rules must use absolute paths:

| Reference | Correct path |
|-----------|-------------|
| Org config | `~/.ldm/config.json` |
| Dev guide | `~/.ldm/shared/dev-guide-wipcomputerinc.md` |
| Human docs | `~/wipcomputerinc/library/documentation/` |
| Agent rules | `~/.ldm/shared/rules/` (source) or `~/.claude/rules/` (deployed) |
| Workspace CLAUDE.md | `~/wipcomputerinc/CLAUDE.md` |
| Global CLAUDE.md | `~/.claude/CLAUDE.md` |

NOT `settings/config.json`. NOT `settings/docs/`. Those paths are from before the March 28 rename.
