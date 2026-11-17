# Multi-Agent Installs — One Skill, Many Copies

The same skill can be installed in several agents and at several scopes. Updating "the skill" while another copy keeps loading stale is the most confusing failure in this domain: the user sees the new behavior in one tool and the old one in another.

## Where Copies Live

Check every location before declaring an inventory complete:

| Scope | Locations |
|---|---|
| Project | `.claude/skills/`, `.codex/skills/`, `.gemini/skills/`, `.openclaw/skills/`, `.agents/skills/`, `.cursor/skills/` under the project root |
| Global | The same agent folders under `~` (e.g. `~/.claude/skills/`), plus `~/.hermes/` |

```bash
npx clawic list    # shows installed skills with their locations and versions
```

A skill present at both project and global scope: the project copy wins inside that project (standard agent resolution). Updating only the global copy changes nothing in projects that shadow it — the inverse of the usual staleness, and worth saying to the user explicitly.

## Inventory Before Any Update

1. List every copy of the slug: agent, scope, version.
2. Same version everywhere → treat as one skill; update all copies in the same operation, one backup per copy.
3. Versions differ → skew. Resolve skew BEFORE applying the new update (next section); stacking an update onto skew produces copies of three different vintages.

## Diagnosing Version Skew

| Observation | Cause | Fix |
|---|---|---|
| One agent updated, others stale | A previous update ran against a single folder | Bring all copies to the target version in one pass |
| Project copy older than global | Project pinned an old version, or predates the global install | Ask which behavior the user wants in this project — shadowing may be intentional |
| One copy hand-edited, others clean | User customized in one agent only | `local-changes.md` for that copy; ask whether edits should propagate to the others |
| Copies of the same version behave differently | Data folders differ, not the skill — `~/Clawic/data/<slug>/` is shared, but agent-side state may not be | Compare what each agent actually loaded; the skill text is only one input |

## Updating All Copies

- One preview covers all copies (same diff), but the backup is per copy: `~/Clawic/data/skill-update/backups/<slug>-<version>-<timestamp>/` gains a subfolder per install location.
- Apply to every location in the inventory; re-list versions afterward — the verify step for multi-agent is "every copy reports the target version" PLUS one real task in the agent the user actually uses.
- Update log line records which agents were updated; a later "why is Cursor different?" resolves from the log.

## Migrations With Shared Data

`~/Clawic/data/<slug>/` is one folder serving every agent's copy. A data migration therefore runs ONCE — after all copies are on the new version, never between updating copy one and copy two: a migrated data folder under a stale copy is the both-broken state (`rollback.md`, restore rule 4).
