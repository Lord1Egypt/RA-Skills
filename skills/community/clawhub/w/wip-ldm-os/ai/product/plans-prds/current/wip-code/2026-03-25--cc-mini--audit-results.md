# Audit Results: Dead Weight in Instruction Files

**Date:** 2026-03-25
**Author:** cc-mini
**Method:** 5-question audit (default? conflict? duplicate? one-off? vague?)
**Inspiration:** Ole Lehmann (@itsolelehmann), Anthropic scaffolding findings

## Headlines

- Global CLAUDE.md is a stale copy of project CLAUDE.md. Both loaded every session = **734 lines of mostly-identical text with drift**
- Every `~/.claude/rules/` file is byte-identical to `~/.ldm/shared/rules/`. Both sets loaded = **doubled**
- TOOLS.md is 430 lines, ~80% duplicated from CLAUDE.md/rules with conflicting details
- Total instruction payload per CC session: **~1,200+ lines**

## Most Duplicated Rules

| Rule | Copies | Notes |
|------|--------|-------|
| Never run tools from repo clones | 7+ | CLAUDE.md x2, rules x2, workspace x2, repo-locations, TOOLS.md |
| Never squash merge | 6+ | AND TOOLS.md has --squash example that contradicts |
| Branch prefixes | 6 | 3 different naming schemes fighting each other |
| Co-author trailers | 5 | TOOLS.md has wrong emails |
| 1Password SA token | 5 | 3 copies in TOOLS.md alone |
| Shared file protection | 5 | |
| Never push to main | 4+ | |
| Memory-first rule | 4 | |
| Security audit before install | 4 | |
| Release pipeline | 4+ | P-CLAUDE has it twice internally |

## Critical Conflicts

| Conflict | File A | File B |
|----------|--------|--------|
| `--squash` in example | TOOLS.md line 60 | Every other file: never squash |
| Co-author emails | TOOLS.md: parker@wipcomputer.com | CLAUDE.md: parkertoddbrooks@users.noreply.github.com |
| Branch prefixes | TOOLS.md: lesa/, mini/, mba/ | CLAUDE.md: lesa-mini/, cc-mini/, cc-air/ |
| OpenClaw version | G-CLAUDE: v2026.2.15 | P-CLAUDE: v2026.2.22-2 |
| wip-release location | G-CLAUDE: ~/.ldm/extensions/ | P-CLAUDE: repos/ldm-os/devops/ |
| Healthcheck paths | G-CLAUDE: flat paths | P-CLAUDE: ldm-os/ paths |
| Journal path | boot-config: iCloud path | CLAUDE.md: wipcomputerinc/ path |
| CC home path | SOUL.md: cc/ | Everything else: cc-mini/ |
| Folder ownership | workspace-boundaries: staff/ | CLAUDE.md: team/ |
| Boot steps 6-9 | G-CLAUDE: "will migrate" | P-CLAUDE: "MANDATORY" |
| 1Password plan | TOOLS.md: "Business" | CLAUDE.md: "pro" |
| Dev Guide path | TOOLS.md vs CLAUDE.md | Different paths |

## What to Keep (Lesa-specific in TOOLS.md)

- Memory search fallback chain (her tools differ from CC's)
- X/Twitter oembed guidance
- Audio analysis / hearing capability
- Email access
- Daily backup details
- Auto-commit fork protection
- Skipped tool calls workaround (platform bug)

Everything else in TOOLS.md (~350 lines) is duplicated from CLAUDE.md/rules, often with wrong details.

## What to Keep (repo-locations.md)

- Repo map and folder structure (solid, unique)
- Tool locations

CUT: "Critical Rules" section (100% duplicated), "Boot Sequence Reminder" (duplicated), "Publish = four steps" (duplicated)

## Stale Content

- CONTEXT.md: 3 weeks stale ("Recent Work Mar 4-5")
- SOUL.md: cc/ path (should be cc-mini/)
- boot-config.json: iCloud journal path
- TOOLS.md line 268: "GitHub push not yet available" (works fine now)
- workspace-boundaries.md: staff/ (should be team/)
- G-CLAUDE: entire file is stale copy of P-CLAUDE

## Recommended Cuts (Summary)

1. **Delete or hollow G-CLAUDE** (~367 lines saved from double-loading)
2. **Symlink ~/.claude/rules/ to ~/.ldm/shared/rules/** (~80 lines saved from double-loading)
3. **Gut TOOLS.md** to Lesa-only content (~350 lines cut)
4. **Remove duplicated rules from repo-locations.md** (~40 lines cut)
5. **Fix all conflicts** (branch prefixes, emails, paths, versions)
6. **Update stale content** (CONTEXT.md, SOUL.md, boot-config.json)

**Estimated reduction: ~800+ lines of dead weight removed from every session**
