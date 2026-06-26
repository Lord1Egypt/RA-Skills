# Research: CLAUDE.md Organization Across Multi-Repo Organizations

**Date:** 2026-04-03
**Author:** CC Mini
**Purpose:** Comprehensive research into how CLAUDE.md files work, how others organize them, and what we should do for our 100-repo org.

---

## Part 1: How CLAUDE.md Technically Works (The Cascade)

### The Full Loading Hierarchy

Claude Code loads CLAUDE.md files from multiple locations in a specific order. Because the model attends more to content that appears later in context, later files have **higher effective priority**. Here is the complete resolution order:

```
1. /Library/Application Support/ClaudeCode/CLAUDE.md  (macOS managed policy)
   /Library/Application Support/ClaudeCode/rules/*.md
   /etc/claude-code/CLAUDE.md                         (Linux/WSL managed policy)
   /etc/claude-code/rules/*.md
   -- Cannot be excluded. Organization-wide. Always loaded. --

2. ~/.claude/CLAUDE.md                                 (user global)
   ~/.claude/rules/*.md
   -- Personal preferences across all projects. --

3. Every CLAUDE.md in every directory from filesystem root
   down to the current working directory.
   -- Walks the ENTIRE tree from / to $CWD. --

4. ./CLAUDE.md or ./.claude/CLAUDE.md                  (project root)
   ./.claude/rules/*.md
   -- Committed to git. Shared with team. --

5. ./CLAUDE.local.md                                   (local project)
   -- Personal project-specific. Auto-added to .gitignore. --
```

**Source:** [Claude Code Memory Docs](https://code.claude.com/docs/en/memory), [Claude Code Settings](https://code.claude.com/docs/en/settings)

### Key Technical Details

**Parent directory walking:** Claude Code walks UP from the current working directory to the filesystem root at launch, collecting CLAUDE.md and CLAUDE.local.md files at every level. All of these are loaded in full at startup.

**Subdirectory loading (on-demand):** CLAUDE.md files in directories BELOW the working directory are NOT loaded at launch. They load on demand when Claude reads files in those subdirectories. This is important for monorepos: a top-level CLAUDE.md sets org-wide standards, while package-level CLAUDE.md files add context only when needed.

**File size:** CLAUDE.md files are loaded in full regardless of length. There is no hard truncation. However, shorter files produce measurably better adherence. The community consensus (validated by HumanLayer and Anthropic's own teams) is to target under 200 lines per file. The recommended maximum for any single memory file is 40,000 characters (MAX_MEMORY_CHARACTER_COUNT). Files exceeding this are flagged.

**Token cost:** CLAUDE.md consumes roughly 500-800 tokens per 100 lines, loaded on every request. This is a constant tax on your context window budget.

**Instruction budget:** Frontier thinking models follow roughly 150-200 instructions before compliance drops. Claude Code's own system prompt takes up about 50 of those slots. That leaves roughly 100-150 slots for YOUR rules across all CLAUDE.md files combined.

**Re-reading:** CLAUDE.md is re-read on every query iteration, not just at session start. After compaction, the CLAUDE.md files from the current working directory's hierarchy are re-loaded.

**The CWD bug we discovered (2026-04-02):** After context compaction, Claude Code's internal CWD can shift to the last repo touched by a bash command. If that repo has no CLAUDE.md, the cascade breaks and all project context vanishes. This is the bug that motivated our Level 3 initiative.

### The .claude/rules/ System

Rules files in `.claude/rules/` provide modular, conditional instructions:

- **Unconditional rules:** `.md` files without a `paths` frontmatter field load at launch, apply to everything.
- **Path-scoped rules:** Files with a `paths` field using glob patterns (e.g., `paths: ["src/**/*.{ts,tsx}"]`) load on demand when Claude reads matching files.
- **Subdirectory support:** Rules can be organized into subdirectories. All `.md` files are discovered recursively.
- **Symlink support:** The rules directory supports symlinks, so you can maintain shared rules and link them into multiple projects.
- **Known bug:** Path-scoped rules in `.claude/rules/` subdirectories sometimes fail to auto-load when working with matching files ([Issue #16853](https://github.com/anthropics/claude-code/issues/16853)).

### File Include Syntax

CLAUDE.md files can import other files using `@path/to/file` syntax. When Claude Code encounters these references, it pulls the linked file's content into context. This enables a "hub and spoke" pattern where CLAUDE.md stays lean and references detail files on demand.

### The claudeMdExcludes Setting

The `claudeMdExcludes` setting in `settings.json` uses glob patterns or absolute paths to skip specific CLAUDE.md files from loading. Patterns are matched against absolute paths using picomatch. **Critical:** This setting only applies to User, Project, and Local memory types. Managed policy files cannot be excluded.

```json
{
  "claudeMdExcludes": [
    "/home/user/monorepo/vendor/CLAUDE.md",
    "**/third-party/.claude/rules/**"
  ]
}
```

### Managed Policy (Enterprise)

Organizations can deploy non-excludable CLAUDE.md files to system directories:
- **macOS:** `/Library/Application Support/ClaudeCode/CLAUDE.md`
- **Linux/WSL:** `/etc/claude-code/CLAUDE.md`

These are always loaded, always first, and cannot be overridden or excluded by any user or project setting. IT teams use `managed-settings.json` at the same paths for enforced configuration.

---

## Part 2: What Anthropic Recommends

### Official Best Practices

From [Anthropic's Best Practices page](https://code.claude.com/docs/en/best-practices) and the ["How Anthropic teams use Claude Code" PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf):

1. **Check CLAUDE.md into git** so your team can contribute. The file compounds in value over time.
2. **Keep it concise.** Under 200 lines. Only include things that apply broadly.
3. **Use skills for domain-specific knowledge.** CLAUDE.md is loaded every session. Skills load on demand.
4. **Use .claude/rules/ for conditional instructions.** Path-scoped rules prevent bloating the base context.
5. **In a monorepo, put shared conventions in the root CLAUDE.md** and service-specific context in child directories (on-demand loading).
6. **For style enforcement, use linters** (ESLint, Prettier, Ruff, Biome), not CLAUDE.md rules. Style rules in CLAUDE.md are expensive and unreliable.
7. **Use MCP servers** rather than CLI for sensitive data access.
8. **Agent teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) enable multi-session coordination.

### What Anthropic's Own Teams Do

From the internal case study PDF:
- Teams held sessions where members demonstrated their Claude Code workflows, spreading best practices organically.
- The better the CLAUDE.md files are, the better Claude Code performs. This especially matters for routine tasks that follow existing patterns.
- Their setups are reportedly **surprisingly minimal**. Boris Cherny (creator of Claude Code) uses far less configuration than most external users.

### The Anthropic Insight on Over-Prompting

This is critical and directly relevant to our 366-line Level 2 CLAUDE.md:

> "Before adding any instruction, ask: could Claude figure this out on its own?"

Anthropic's own prompting documentation acknowledges that excessive scaffolding makes the AI perform worse. Their teams found that removing unnecessary instructions improved output quality. This aligns with Ole Lehmann's widely-shared finding: "I deleted half my Claude setup and every output got BETTER."

The mechanism: when you give the model too many instructions, it tries to follow everything simultaneously and does none of it well. It second-guesses correct default behavior. The "instruction budget" of 100-150 effective rules is a real constraint.

---

## Part 3: Gary Tan's GStack Approach

### Overview

Y Combinator CEO Garry Tan open-sourced [GStack](https://github.com/garrytan/gstack) on March 12, 2026. Within days it hit 20,000+ GitHub stars. It is the most visible example of organized Claude Code configuration in the wild.

**Source:** [GStack GitHub](https://github.com/garrytan/gstack), [TechCrunch coverage](https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/), [HN discussion](https://news.ycombinator.com/item?id=47355173)

### How GStack Organizes CLAUDE.md

GStack does NOT use a multi-level CLAUDE.md cascade. Instead, it uses a **skills-first architecture**:

1. **Installation:** Skills live at `~/.claude/skills/gstack/` (global) or `.claude/skills/gstack/` (per-project).
2. **CLAUDE.md integration:** Each project's CLAUDE.md gets a ~15-line "gstack" section that lists available skills and routing rules.
3. **Skills as roles:** Each skill file (SKILL.md) represents a specialized role: CEO reviewer, design consultant, QA engineer, release manager, etc. 23 skills total.
4. **Slash commands:** `/ship`, `/review`, `/qa`, `/investigate`, `/office-hours`, `/plan-ceo-review`, etc.
5. **Progressive disclosure:** The CLAUDE.md only lists skill names. The full skill content loads on demand when invoked.

### GStack's Key Design Decisions

- **Skills, not CLAUDE.md bloat.** Domain knowledge lives in SKILL.md files, not CLAUDE.md. The CLAUDE.md stays lean (just the routing table).
- **Global installation.** Skills install to `~/.claude/skills/gstack/`, making them available in every project without per-repo configuration.
- **No multi-level hierarchy.** GStack does not use parent-directory CLAUDE.md walking or workspace-level files. It is repo-centric.
- **Vendoring option.** Skills can be copied into `.claude/skills/gstack/` inside a repo and committed to git. Then `git clone` just works for the whole team.
- **The Completeness Principle.** GStack's CLAUDE.md advises against shortcuts when complete implementations are achievable. It shows both human-team and AI-with-gstack time estimates.

### How GStack Differs From Our Approach

| Aspect | GStack | Our System |
|--------|--------|------------|
| Organization | Single repo of skills | Multi-level CLAUDE.md cascade + skills |
| Shared context | Skills at ~/.claude/skills/ | CLAUDE.md hierarchy + Crystal search |
| Per-repo config | ~15 lines in CLAUDE.md | Full Level 3 CLAUDE.md (~50-80 lines) |
| Cross-repo awareness | None (repo-centric) | Crystal MCP, workspace CLAUDE.md |
| Agent identity | None | Boot sequence, SOUL.md, IDENTITY.md |
| Multi-agent | None | Workspace boundaries, branch prefixes |
| Enterprise features | None | Managed policy, hooks, guards |

**Key takeaway:** GStack solves a different problem. It is a solo developer's toolkit for making Claude Code act as a virtual team. It does not address multi-repo context, multi-agent coordination, or organizational conventions. Our problem is fundamentally different: we need 100 repos to share conventions while each maintaining their own context.

---

## Part 4: Community Patterns

### Pattern 1: The Spine Pattern (Titus Soporan)

**Source:** [The Spine Pattern](https://tsoporan.com/blog/spine-pattern-multi-repo-ai-development/)

A separate git repository that sits above your actual codebases and serves as a context orchestration layer:

- **Layered CLAUDE.md files** that establish a routing hierarchy telling agents where they are and what patterns to follow.
- **Task system** with templatized checklists capturing planning, decisions, and implementation phases.
- **Cross-cutting documentation** spanning multiple codebases.
- **Actual code repositories remain independent** and unaware of the spine.

The spine is "operator-level tooling for the person orchestrating work across systems, not something imposed on a team."

**Relevance to us:** Our `~/wipcomputerinc/CLAUDE.md` (Level 2) functions exactly like a spine. The workspace root is the orchestration layer. Individual repos are independent. The spine provides the map.

### Pattern 2: Polyrepo Synthesis (Rajiv Pant)

**Source:** [Polyrepo Synthesis](https://rajiv.com/blog/2025/11/30/polyrepo-synthesis-synthesis-coding-across-multiple-repositories-with-claude-code-in-visual-studio-code/)

Uses VS Code multi-root workspaces to open multiple repos in a single window. Each repo has its own CLAUDE.md. Together they form a "context mesh" where Claude Code understands dependencies and can trace impact across layers.

**Key idea:** Every CLAUDE.md mentions its siblings. The ecosystem table is kept identical across all repositories by copy-pasting.

**Relevance to us:** We use a different approach (Crystal MCP for cross-repo search) rather than copy-pasting ecosystem tables. The context mesh idea validates our "pointer" approach where Level 3 says "use crystal_search for cross-repo context."

### Pattern 3: Central Standards Repository (Enterprise CI/CD)

**Source:** [Big Hat Group Enterprise Guide](https://www.bighatgroup.com/blog/claude-md-guide-enterprise-teams/)

Maintain a central `claude-standards` repo with your org's base rules, distributed via CI/CD:
- A pipeline step syncs shared `.claude/rules/` files into each repo.
- Naming conventions, security baselines, compliance rules authored once, inherited everywhere.
- Hooks (`.claude/settings.json`) provide enforcement guarantees rather than suggestions.

**Relevance to us:** Our `ldm install` deploying shared rules from `~/.ldm/shared/rules/` to `~/.claude/rules/` is exactly this pattern. We already do it. The difference is we deploy locally via installer rather than via CI/CD.

### Pattern 4: Symlinked Rules

Multiple sources mention using symlinks in `.claude/rules/` to maintain a single source of truth:

```bash
# Every repo links to the same shared rules
ln -s ~/org/shared-rules/git-conventions.md .claude/rules/git-conventions.md
ln -s ~/org/shared-rules/security.md .claude/rules/security.md
```

**Relevance to us:** We could symlink from each repo's `.claude/rules/` to `~/wipcomputerinc/settings/docs/` or shared rules. But this requires setup per-repo and breaks on clone. The installer approach is more robust.

### Pattern 5: Monorepo Scaffolding (Vuong Ngo)

**Source:** [Scaling AI-Assisted Development](https://medium.com/@vuongngo/scaling-ai-assisted-development-how-scaffolding-solved-my-monorepo-chaos-4838fb3b4dd6)

For monorepos, uses a root CLAUDE.md with architecture overview and package-level CLAUDE.md files that provide detailed context. Claude Code's on-demand subdirectory loading keeps token usage efficient.

**Relevance to us:** We are NOT a monorepo (each repo under ldm-os/ is independent), but the on-demand loading concept applies. When CC works in a specific repo, it should get that repo's context without paying for all 100 repos.

### The Open Feature Request (GitHub Issue #14467)

**Source:** [Organization-wide shared CLAUDE.md via GitHub org](https://github.com/anthropics/claude-code/issues/14467)

The most-requested feature for multi-repo orgs: Claude Code would automatically fetch a shared CLAUDE.md from a GitHub organization level (like `.github` repos work for community health files). Currently not implemented. Teams work around it with:
- Manually symlinking `~/.claude/CLAUDE.md` to a shared repo
- Enterprise managed-policy file deployment
- CI/CD syncing of `.claude/rules/`
- Our approach: installer-deployed rules

---

## Part 5: The HumanLayer Framework

HumanLayer's ["Writing a good CLAUDE.md"](https://www.humanlayer.dev/blog/writing-a-good-claude-md) is the most cited practical guide. Key points:

### The Three Questions for Every Line

For every line in your CLAUDE.md, ask:
1. **Would Claude make a mistake without this?** If Claude already does something correctly on its own, the instruction is noise.
2. **Is this a style rule?** Use a linter instead. Style rules in CLAUDE.md are expensive and unreliable.
3. **Does this apply to every session?** If not, put it in a skill or path-scoped rule.

### Structure: WHAT, WHY, HOW

- **WHAT:** Tech stack, project structure, codebase map.
- **WHY:** Purpose of the project, what everything is doing.
- **HOW:** How Claude should work on the project. Build/test commands, conventions.

### Practical Targets

- HumanLayer keeps their own CLAUDE.md under 60 lines.
- Recommended target: under 200 lines per file.
- Use `<important if="condition">` tags for conditional sections.
- Avoid: stuffing every possible command, style guidelines, exhaustive documentation.

---

## Part 6: Analysis of Our Current System

### What We Have Now

```
Level 1: ~/.claude/CLAUDE.md                              37 lines (global)
Level 2: ~/wipcomputerinc/CLAUDE.md                      366 lines (workspace)
Level 3: repos/ldm-os/wip-ldm-os-private/CLAUDE.md       86 lines (per-repo, first one)
```

Plus:
- `~/.claude/rules/*.md` (5 files, ~80 lines total, deployed by ldm install)
- `~/wipcomputerinc/settings/docs/` (14 docs, read on demand)
- `~/wipcomputerinc/settings/config.json` (org identity)
- Boot sequence: 10 mandatory files read at session start

### Total Token Load at Session Start

When CC opens from `~/wipcomputerinc/`:
```
System prompt:                     ~50 instruction slots
Level 1 (~37 lines):              ~200-300 tokens
Level 2 (~366 lines):             ~2000-2900 tokens
Rules (~80 lines):                ~400-640 tokens
Boot files (10 mandatory reads):  ~5000-10000 tokens (estimated)
                                   ─────────────
Total instruction surface:         ~8000-14000 tokens before any work begins
```

When CC opens from a repo with Level 3:
```
System prompt + Level 1 + Level 2 + Level 3 + Rules
= everything above + ~500-700 more tokens
```

### Problems Identified

1. **Level 2 is too large.** 366 lines is nearly 2x the recommended 200-line maximum. It contains agent-specific instructions (Lesa's architecture, boot sequence, MCP tools, Dream Weaver) that are irrelevant in many repo contexts.

2. **Massive duplication.** Level 1 (global ~/.claude/CLAUDE.md) and Level 2 (workspace) share ~83 lines of identical content (writing style, co-authors, 1Password, merge rules, shared file protection, memory-first rule). This was documented in the Mar 25 plan.

3. **The Level 2 file tries to be everything.** It is simultaneously:
   - An org conventions file (git rules, release pipeline, co-authors)
   - An agent identity file (who Lesa is, who CC is, Dream Weaver)
   - A system operations manual (plugins, config, health monitoring)
   - A memory/persistence guide (boot sequence, end-of-session)
   - A tool reference (mdview, 1Password, Crystal)

4. **Over-prompting risk.** With ~366 lines in Level 2 alone, plus Level 1 and rules, we are likely past the 150-200 instruction compliance threshold. Some instructions may be actively degrading output quality.

5. **11 repos still have no Level 3.** Only wip-ldm-os-private has a CLAUDE.md. The CWD compaction bug means every other repo is a context blackhole after compaction.

### What Works Well

1. **The three-level architecture is correct.** It matches Anthropic's recommended hierarchy (global, project, repo) and the community's best patterns (Spine, polyrepo synthesis).

2. **Crystal MCP for cross-repo context.** Better than copy-pasting ecosystem tables. Better than trying to inline everything.

3. **Installer-deployed rules.** Our `ldm install` deploying shared rules to `~/.claude/rules/` is the same pattern enterprise teams use, just local instead of CI/CD.

4. **On-demand doc pointers.** Rules that say "read settings/docs/how-worktrees-work.md when doing repo work" is exactly the pattern Anthropic and HumanLayer recommend.

5. **Skills for domain knowledge.** Our SKILL.md files and the Agent Skills Spec align perfectly with the "skills, not CLAUDE.md bloat" philosophy.

---

## Part 7: Recommendations for Our 100-Repo Org

### Recommendation 1: Complete Level 3 Before Touching Level 2

The master plan (2026-04-03) already says this. The Mar 25 failure proved it. Do not thin Level 2 until every active repo has a working Level 3. The reversed plan (2026-03-27) got this right: bottom-up, not top-down.

**Priority repos (11 total):**
1. wip-ldm-os-private (done)
2. memory-crystal-private
3. wip-ai-devops-toolbox-private
4. wip-agent-pay-private
5. wip-1password-private
6. wip-xai-grok-private
7. wip-xai-x-private
8. wip-markdown-viewer-private
9. dream-weaver-protocol-private
10. wip-healthcheck-private
11. wip-bridge-private

### Recommendation 2: Level 3 Template (Per-Repo CLAUDE.md)

Based on all research, each repo's CLAUDE.md should be 40-80 lines covering:

```markdown
# <Repo Name>

<One paragraph: what this repo does>

## Build and test
<actual commands>

## Key files
<tree of important paths>

## Conventions
- Branch prefix, merge rules, co-authors (or pointer to shared rules)
- Repo-specific conventions

## Product context
<What product this serves, current state>

## Full system context
For complete project context, boot sequence, and agent instructions:
- Read ~/wipcomputerinc/CLAUDE.md
- Read ~/wipcomputerinc/settings/docs/ for conventions
- Use crystal_search for cross-repo context
```

### Recommendation 3: Audit and Trim Level 2

After Level 3 is in every repo, apply the HumanLayer three-question test to every line of Level 2:

1. **Would Claude make a mistake without this?**
2. **Is this already covered by Level 1, Level 3, rules, or skills?**
3. **Does this apply to every workspace session?**

Likely candidates for removal or relocation:
- **Plugin table** (move to a skill or reference doc, not needed every session)
- **Health monitoring details** (move to healthcheck repo's Level 3)
- **Rebuild/deploy plugin instructions** (move to a skill)
- **Config architecture details** (move to openclaw repo docs or a skill)
- **Boot sequence** (could become a skill that activates on session start)
- **End-of-session** (could become a hook-triggered skill)

Target: Level 2 under 150 lines. Ideally under 100.

### Recommendation 4: Use .claude/rules/ More Aggressively

Move org conventions OUT of CLAUDE.md and INTO `.claude/rules/`:

```
~/.claude/rules/
  git-conventions.md        (already exists)
  release-pipeline.md       (already exists)
  workspace-boundaries.md   (already exists)
  writing-style.md          (already exists)
  security.md               (already exists)
  co-authors.md             (new: extract from CLAUDE.md)
  1password.md              (new: extract from CLAUDE.md)
  shared-file-protection.md (new: extract from CLAUDE.md)
```

Rules are loaded separately from CLAUDE.md and can use path-scoping for conditional loading. This reduces the CLAUDE.md line count without losing any instructions.

### Recommendation 5: Use Skills for Agent-Specific Knowledge

The boot sequence, Lesa's MCP tools, Dream Weaver protocol, and agent identity content should NOT be in a CLAUDE.md that loads on every session in every context. Move them to:

- A **boot skill** that activates on session start (reads the boot files)
- A **lesa-comms skill** that activates when communicating with Lesa
- A **dream-weaver skill** for memory consolidation
- A **release skill** (already exists as wip-release)

This follows GStack's core insight: skills load on demand, CLAUDE.md is the routing table.

### Recommendation 6: The Level 3 Generator (Future)

Ticket #165 (`wip-repos claude`) would auto-generate Level 3 CLAUDE.md files from repo metadata. Based on research, the generator should:

- Read `package.json` for name, description, scripts, bin
- Read `SKILL.md` for product context
- Read `README.md` for key files and architecture
- Generate a 40-80 line CLAUDE.md
- Include the standard pointers (Level 2, Crystal, settings/docs)
- Be idempotent (safe to re-run, preserves manual additions)

### Recommendation 7: Consider Managed Policy for True Org-Wide Rules

For rules that must NEVER be skipped (co-authors, no squash merge, no push to main):

```
/Library/Application Support/ClaudeCode/CLAUDE.md
```

This is the enterprise deployment path. Managed policy files cannot be excluded. Every CC session on this machine, in any repo, always gets these rules. Our `ldm install` could deploy to this path.

**Caution:** This only works on machines we control. For team members using their own machines, the installer + `~/.claude/rules/` approach is more appropriate.

### Recommendation 8: Measure and Prune Regularly

Set up a quarterly audit:
1. Count total lines across all CLAUDE.md files loaded in a typical session.
2. Apply the HumanLayer three-question test to every instruction.
3. Check for drift between Level 1, Level 2, Level 3, and rules.
4. Verify the instruction count is under 100-150 effective rules.
5. Ask: "Did Claude make a mistake that this rule would have prevented?"

---

## Part 8: The Ideal End State

After all recommendations are implemented:

```
Level 1: ~/.claude/CLAUDE.md (~30 lines)
  Generated from settings/config.json by ldm install.
  Writing style, timezone, memory-first rule.
  Pointer: "Read ~/wipcomputerinc/CLAUDE.md for full context."

~/.claude/rules/ (~8 files, ~100 lines total)
  git-conventions.md, release-pipeline.md, workspace-boundaries.md,
  writing-style.md, security.md, co-authors.md, 1password.md,
  shared-file-protection.md
  Each with on-demand pointer to settings/docs/ for details.

Level 2: ~/wipcomputerinc/CLAUDE.md (~100-150 lines)
  Directory structure (what lives where)
  Agent identity (brief: who Lesa is, who CC is)
  Memory tools (Crystal, conversation search, workspace search)
  Workspace boundaries
  Pointer: "For conventions, read settings/docs/ on demand"
  Pointer: "For boot sequence, use the boot skill"

Level 3: <repo>/CLAUDE.md (~40-80 lines each, 11+ repos)
  What this repo does
  Build/test commands
  Key files
  Product context
  Pointer to Level 2 and Crystal

Skills:
  Boot sequence skill (reads 10 boot files on session start)
  Lesa comms skill (MCP tools, how to talk to Lesa)
  wip-release skill (already exists)
  ... other domain skills

Total instruction surface per session:
  Level 1 + rules + Level 2 + Level 3 = ~280-360 lines
  Well under the 500-line danger zone.
  Effective instruction count: ~80-120 (under the 150 compliance threshold).
```

---

## Part 9: Key Sources

### Official Anthropic Documentation
- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory) ... the definitive reference for hierarchy and loading
- [Claude Code Settings](https://code.claude.com/docs/en/settings) ... claudeMdExcludes, managed policy
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) ... official recommendations
- [How Anthropic Teams Use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) ... internal case studies
- [Claude Code .claude Directory](https://code.claude.com/docs/en/claude-directory) ... anatomy of the config folder
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands) ... skills system

### Gary Tan / GStack
- [GStack GitHub](https://github.com/garrytan/gstack) ... the repo (20K+ stars)
- [GStack CLAUDE.md](https://github.com/garrytan/gstack/blob/main/CLAUDE.md) ... how he structures it
- [TechCrunch: Why Garry Tan's Claude Code setup has gotten so much love](https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=47355173)

### Community Patterns
- [The Spine Pattern (Titus Soporan)](https://tsoporan.com/blog/spine-pattern-multi-repo-ai-development/) ... meta-repo for context orchestration
- [Polyrepo Synthesis (Rajiv Pant)](https://rajiv.com/blog/2025/11/30/polyrepo-synthesis-synthesis-coding-across-multiple-repositories-with-claude-code-in-visual-studio-code/) ... VS Code multi-root + CLAUDE.md mesh
- [Big Hat Group Enterprise Guide](https://www.bighatgroup.com/blog/claude-md-guide-enterprise-teams/) ... enterprise templates and patterns
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) ... the practical "three questions" framework
- [GitHub Issue #14467: Org-wide shared CLAUDE.md](https://github.com/anthropics/claude-code/issues/14467) ... the most-requested feature for multi-repo

### Token and Context Management
- [Your CLAUDE.md is Eating Your Token Budget (Medium)](https://medium.com/@kjramsy/your-claude-md-is-eating-your-token-budget-heres-how-to-fix-it-b8d6c4d1c986)
- [Claude Code CLAUDE.md Hierarchy: Lessons from 10 Days of Misconfiguration](https://dev.to/shimo4228/claude-codes-claudemd-hierarchy-lessons-from-10-days-of-misconfiguration-1afa)
- [How I Organized My CLAUDE.md in a Monorepo with Too Many Contexts](https://dev.to/anvodev/how-i-organized-my-claudemd-in-a-monorepo-with-too-many-contexts-37k7)

### Over-Prompting and Minimalism
- [Ole Lehmann: Your Claude setup rots over time](https://x.com/itsolelehmann/status/2036533756572639611)
- [I Cut My Claude Prompts by 90% and Got Better Code](https://tylerfolkman.substack.com/p/i-cut-my-claude-prompts-by-90-and)
- [Claude Code Rules: Stop Stuffing Everything into One CLAUDE.md](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433)

---

## Part 10: Summary

### The Three Things That Matter Most

1. **The cascade is real and well-defined.** Claude Code walks up from CWD to root, loading every CLAUDE.md it finds. Later (more specific) files have higher priority. Subdirectory files load on demand. This architecture supports our three-level plan perfectly.

2. **Less is more.** The universal finding across Anthropic, GStack, HumanLayer, and the community is that shorter, more focused CLAUDE.md files produce better results. Our 366-line Level 2 is actively hurting performance. The instruction compliance threshold of ~150 rules is real.

3. **Our architecture is right. The execution is incomplete.** The three-level cascade with Crystal for cross-repo search and skills for domain knowledge is the correct design. What is missing: Level 3 in every repo, trimming Level 2, and moving agent-specific content into skills. The master plan (2026-04-03) has the right order of operations. Execute it.
