# Skill Upgrade

Analyzes an existing skill and **discovers issues to fix** — adds topics, enhances frontmatter, restructures scripts.

## When to Use

- When adding new topics/features to an existing skill
- When adding new trigger keywords to SKILL.md description
- When migrating scripts within a skill to a proper `scripts/` structure
- When improving this skill (skill-manager) itself

## Core: Conversation-based Problem Discovery

The core of upgrade is **identifying skill limitations, missing topics, and structural issues**.

### Problem Discovery Workflow

1. **Read through the entire conversation and detect these signals**:

| Signal | Example |
|--------|---------|
| Skill did not activate | "Why isn't the skill triggering?" |
| Manual corrections after skill execution | Skill runs → immediate Edit/manual fix |
| User used a workaround | Used bash/edit directly instead of the skill |
| Repeated patterns | Same task performed manually 3+ times |
| Mentions of insufficient output | "This should be included too", "It's missing" |

2. **List discovered problems concretely**:
   - Which skill? → What situation? → What output was insufficient?

3. **Derive improvement proposals**:
   - Can it be solved with a new topic/section?
   - Can it be solved by adding trigger keywords to description?
   - Is a new script needed?

### Example: Session Skill Problems Discovered in This Conversation

```
Problem: /session <id> name it → naming feature didn't exist in skill, implemented manually
Fix: Added rename topic + rename-session.sh script
→ Done
```

```
Problem: Used Edit directly without skill-manager when improving skill
Fix: Added skill-usage.md rule + created skill-manager upgrade topic
→ Done
```

## Language Check (MANDATORY — before any Edit/Write)

Every upgrade operation must detect and match the existing skill's language.

### Detection (Step 0 of every upgrade)

1. Read `SKILL.md` and 1-2 existing topic files
2. Determine the skill's language from existing content (headings, body text, descriptions)
3. Record: `skill_language = English | <other>`

### Enforcement

| Detected language | Rule |
|---|---|
| English | All new content must be English — topic files, AskUserQuestion text, code comments, table content, frontmatter trigger keywords |
| Other | Match existing language. Technical terms in English OK |
| Mixed | Follow majority language |

### Post-write verification

After every Edit/Write on a skill file, read back the modified section and confirm it matches `skill_language`. If a mismatch is found, fix immediately before proceeding.

## External-system Structure Check (MANDATORY — before any Edit/Write)

When the upgrade introduces content describing **external systems the skill does not own** (user environment layout, infrastructure topology, cross-tool symlink/hardlink wiring, host-to-host sync mechanism, on-disk path conventions outside the skill itself), the structure must be confirmed via `AskUserQuestion` **before drafting** — not after. Drafting from assumption produces a "draft → user correction → redraft" cycle that wastes ask budget and pollutes the skill with stale guesses.

### Trigger conditions (any one)

- Topic body describes paths outside the skill's own directory (e.g., `~/.agents/`, `~/.claude/plugins/`, `/etc/`, `/mnt/c/...`)
- Topic body asserts sync/share/separation policy between hosts or OS environments
- Topic body documents wiring (symlink, hardlink, bind mount, junction) between paths
- Topic body claims a specific tool (Syncthing, chezmoi, rsync) is used for a specific purpose

### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Write a draft assuming a topology, then ask for corrections | Ask the structural questions first (share mechanism / separation rationale / topic scope) → write the draft from the answers |
| 2 | Assume "Windows source → WSL symlink (unidirectional)" or any other plausible topology | Confirm direction (which side is SoT, which is mirror) and mechanism (symlink vs hardlink vs Syncthing) via AskUserQuestion |
| 3 | Map common patterns (e.g., "this is like the chezmoi pattern") without confirming | Each environment has its own conventions. Pattern similarity ≠ structural identity |
| 4 | Defer ask until the user objects | Ask before the first Write/Edit. Post-Write corrections cost more (rewrite + re-verify) |
| 5 | Bundle 4+ structural questions into a single Edit and hope they're right | Break structural axes into separate `questions` array entries (max 4). Get each axis confirmed |

### Self-check (before the first Write/Edit producing the new topic body)

1. Does the topic describe paths/systems outside the skill's own directory? → If yes, this rule applies
2. List the structural axes the topic asserts (direction, mechanism, scope, related tools)
3. For each axis where you would write a specific claim (e.g., "symlink", "Windows source"), did the user explicitly confirm that claim in this session? → If no, ask before Write
4. Only after all structural axes are confirmed → proceed to Step 1 (Identify Target Skill)

### Example mapping

| Topic body claim | Structural axis | Required confirmation |
|------------------|----------------|----------------------|
| "~/.agents is shared via symlink" | share mechanism | AskUserQuestion: symlink / Syncthing / chezmoi / other |
| "WSL ~/.agents symlinks to /mnt/c/.../.agents" | direction (which side hosts the storage) | AskUserQuestion: Windows-hosted / WSL-hosted / both SoT (per-host) |
| "~/.claude/plugins/ is separated to avoid marketplace cache races" | separation rationale | AskUserQuestion: OS binary incompatibility / cache race / other |
| "Bootstrap script lives in ~/.agents/ root" | script ownership | AskUserQuestion: script location and owner |

## Workflow

### 1. Identify Target Skill

```bash
# Search for skill location
ls ~/.claude/skills/
ls .claude/skills/    # project skills
```

### 2. Analyze Current Structure

- Read `SKILL.md`: check current topics list, description, frontmatter
- Read topic files: understand content, check for duplicates
- Check if `scripts/` exists

### 3. Get Approval for Improvement Candidates via AskUserQuestion ⚠️ Required

**Conversation-based problem discovery → must get user approval before execution.**

Like agentify, present discovered problems first and let the user choose which ones to improve.

```
AskUserQuestion {
  question: "Here are improvement candidates discovered from this conversation. Which ones should be applied?",
  multiSelect: true,
  options: [
    { label: "Add rename topic", description: "Session naming feature was missing, implemented manually" },
    { label: "Add description trigger keywords", description: "Skill activation failure case detected" },
    ...discovered problems
  ]
}
```

**Forbidden**: Immediately fixing upon discovery. Must only modify items selected after AskUserQuestion.

### 3-1. Version Change Rule ⚠️ Required

**Version bump rules** — note: Step 3's AskUserQuestion requirement always applies to **content modifications** before any version bump is considered. This rule governs the **version-bump act itself**, not the content edits that precede it.

- **Patch** (0.1.1 → 0.1.2): the version-bump act may proceed without an additional AskUserQuestion (the Step 3 ask already approved the content change). Applies to topic content reinforcement, bug fixes, frontmatter tweaks.
- **Minor** (0.1.x → 0.2.0): **AskUserQuestion required for the bump act** — new topic, feature change. The Step 3 ask covers the content; this second ask confirms the publish-worthy classification.
- **Major** (0.x → 1.0): **AskUserQuestion required for the bump act** — compatibility break.
- Local-only changes (not intended for publish) may keep the existing version regardless of change size.

**HARD STOP enforcement mechanism**:

1. **Before any Edit call that modifies the frontmatter `version:` field, self-ask**: "Is this change a new topic addition / feature change / compatibility break?" — If yes, run `AskUserQuestion` first
2. **Performing a Minor/Major bump without `AskUserQuestion` = this step incomplete** — if the user discovers it, re-enter Step 4 to revert and re-ask
3. **Forbidden thinking: "new topic added = auto 0.1.x → 0.2.0"** — a new topic is one instance of minor, but the bump requires **explicit publish intent from the user**. Local-only changes keep the version
4. **Default recommendation = "keep"** — unless the user explicitly says "I'm going to publish", keep the version
5. **`AskUserQuestion` option format** (Recommended marker):
   - `Keep version (no publish planned) (Recommended)` — default
   - `Patch (0.1.x → 0.1.x+1)` — reinforcement / fix
   - `Minor (0.1.x → 0.2.0)` — new topic / feature
   - `Decide at publish time` — defer the decision

### 3-2. Do & Don't Table Format (Recommended)

When writing behavioral constraints (forbidden patterns + correct alternatives), prefer **Do & Don't table** over prose. Tables are faster to scan and have higher compliance rates.

| When to use | Format |
|-------------|--------|
| Forbidden pattern + correct alternative exist as a pair | Do & Don't table |
| Rule has been violated 2+ times | Do & Don't table (mandatory) |
| Simple principle declaration | Prose OK |

```markdown
| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|------------------------|
| 1 | `Bash("cmd1 && cmd2")` | `Bash("cmd1")` then `Bash("cmd2")` |
```

**Apply to**: SKILL.md procedure steps, topic files, PROMPT.md sections, failed-attempts.md prevention sections.

### 4. Plan Improvements

| Improvement Type | Task |
|-----------------|------|
| Add new topic | **First run the route `2b` remote ecosystem search** (`Skill("skill-kit", "find <capability>")` / `Skill("clawhub", "find ...")`) to confirm the capability is not already published — reuse over rebuild. Then create topic file → update SKILL.md topics table |
| Improve frontmatter | Add new trigger keywords to description |
| Integrate scripts | Create `scripts/` folder → migrate scripts → document execution in SKILL.md |
| Add Quick Reference | Add usage section to SKILL.md |
| Add Do & Don't table | Convert prose rules to Do & Don't format (see 3-2) |

**Add-topic remote-dup gate (MANDATORY)**: adding a topic/feature is where capability duplication slips in — a feature already published elsewhere gets re-authored locally. Before creating the topic file, search the remote ecosystem (route topic Step 2b). If a remote skill covers it, reuse/install instead of authoring.

### 3-3. External Doc Embedding (Catalog Form)

When embedding content fetched from external sources (`context7`, official docs, GitHub README, vendor blog) into a topic file, **never paste verbatim**. Transform to a reader-friendly catalog form before writing.

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|-----------------------|
| 1 | Paste a context7 JSON block as-is with no inline comments | Annotate every key with `// effect, default, accepted values` inline so the reader can decide what to toggle without leaving the code block |
| 2 | Show only the minimal form (`{"omcLabel": false}`) and rely on a separate table for the meaning of other keys | Emit the full default catalog with every key visible and commented; use a separate table only for cross-key relationships |
| 3 | Drop the original `preset` / `mode` / `threshold` defaults | Preserve the source defaults next to each option so users see the baseline before overriding |
| 4 | Translate identifier names or rephrase value enums | Keep keys / enum literals exact (`'focused'`, `'grouped'`) — only the `//` comment is prose |

**Default catalog pattern** for JSON-shaped option references:

```jsonc
{
  "groupName": {
    "preset": "focused",       // bulk selector: "minimal" | "focused" | "full" | "dense" | "analytics" | "opencode"
    "elements": {
      "omcLabel": true,        // [OMC#x.x.x] version prefix
      "ralph": true,           // Ralph loop counter
      "todos": true,           // todo counter (uses todoFeatureEnabled)
      "contextBar": true,      // visual context-usage bar
      "agents": true           // spawned agent panel
    },
    "thresholds": {
      "contextWarning": 70,    // % → yellow tint
      "contextCritical": 85    // % → red tint
    }
  }
}
```

**Why no `...` shorthand** — listing the full enum is the whole point of the catalog form. `...` defeats the catalog because the reader still has to leave the block to find the missing values. The Self-check below catches this.

Every key carries a `//` comment with the field's purpose and (when known) the default value or accepted values. Booleans get one-line role descriptions; enums list the alternatives; numbers note the unit.

**Self-check before writing a catalog block**:
1. Does each key have an inline `//` comment? (No comment = forbidden paste)
2. Are *all* keys from the source defaults present, not only the one you currently care about?
3. Did you preserve original casing for keys and enum string literals?
4. Are defaults from the source recorded next to each key?
5. For enum-valued keys, are *all* accepted values listed in the comment? (`...`, "etc.", or "see method A" = forbidden — the reader must not need to leave the block)
6. For cross-reference between blocks (e.g., "same enum as method A"), re-emit the full enum in each block — DRY does not apply to reader-facing references.

If any answer is "no," rewrite before saving the file.

### 3-4. Case-history meta detection (MANDATORY — before every Edit/Write on a skill file)

**Before saving any topic body or SKILL.md section, scan `new_string` for case-history meta keywords.** Match → move that text to `~/.claude/skills/cleanup/data/failed-attempts.md` (HOT) and replace with a one-line pointer (`see failed-attempts.md "<keyword>"`) or remove entirely.

This duplicates `fix/SKILL.md` Step 2 Don't/Do #8 inside the upgrade flow so the rule fires at the moment of Edit, not only when `/fix` is triggered after the fact.

#### Forbidden patterns (any match = move to failed-attempts.md HOT)

| Pattern | Example |
|---------|---------|
| Explicit dated event line | `YYYY-MM-DD (1st occurrence):`, `YYYY-MM-DD session:`, `(YYYY-MM-DD, Nth recurrence)` |
| "Violation case" / equivalent in any language + date | `Violation case (YYYY-MM-DD, 1st)` |
| "Skill content history" / "case history meta" | `## Skill content history` |
| "verified YYYY-MM-DD" / "prior versions claimed X" | inline meta about prior skill versions |
| "Nth recurrence" / "Nth occurrence" / equivalents in any language | recurrence count baked into body |
| Session UUID or short session id reference | `session 5bfda407`, `(session abc1234)` |

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Include dated event meta or violation-case section inside the topic body to justify the rule | Keep topic body abstract (Don't/Do + self-check + procedure only). Move case context to failed-attempts.md HOT |
| 2 | "Author motivation makes the rule traceable, so embed the session context" | Motivation lives in commit message + failed-attempts.md entry. Topic body stays evergreen |
| 3 | Add `### Origin` / `### Example YYYY-MM-DD <event>` section to the topic | Either remove the section, or replace with one-line pointer `(see failed-attempts.md "<keyword>")` |
| 4 | Mention a specific past event in the body to strengthen the rule's emotional weight | The rule's strength comes from clarity (Don't/Do table + self-check), not from inline case anchoring |

#### Self-check (before EVERY Edit/Write on a skill file in this upgrade)

1. Scan `new_string` for any of the forbidden patterns above
2. If 1+ match → halt Edit, extract the matching text
3. Append the extracted text to `~/.claude/skills/cleanup/data/failed-attempts.md` (HOT) as a new section, or merge into an existing matching section
4. Replace the topic-body text with one-line pointer if a reference is essential, or omit entirely
5. Re-scan `new_string` post-extraction — confirm zero remaining matches
6. Only then proceed with the Edit/Write

### 4. Execute

**Topic addition pattern:**

```markdown
<!-- New topic file: skill-name/new-topic.md -->
# New Topic

[Content]

## Procedure
...
```

**SKILL.md update checklist:**
- [ ] **Measure current `description:` length** — `DESC=$(awk '/^description:/,/^---$/' SKILL.md | sed -E 's/^description: //; /^---$/d' | tr -d '\n'); echo "len: ${#DESC}"` (see `lint.md` "Description Length Budget"). If `current + new content > 1024`, **compress first** using reduction strategies #1~4 before adding new topic info
- [ ] Add new topic name and trigger keywords to `description:` frontmatter
- [ ] Add row to Topics table in alphabetical order
- [ ] Update Quick Reference section
- [ ] Check `depends-on` field (see procedure below)
- [ ] Update Topic Dependencies section if topics reference each other or external skills (see below)
- [ ] **Re-measure `description:` length after Edit** — confirm ≤ 1024. If over, run `/skill-kit lint` for guidance

**Topic Dependencies section (multi-topic skills):**

When the skill has topics that depend on each other or on external skill topics, add/update a **Topic Dependencies** section in SKILL.md after the Topics table:

```markdown
## Topic Dependencies

\```
skill-name (main workflow)
  └─→ external-skill/topic (used in step N)
  └─→ topic-b (optional: extends main workflow)
\```

- topic-a: always executed
- topic-b: optional, opt-out with `--no-flag`
```

This makes cross-topic and cross-skill relationships explicit, preventing confusion about execution order and optional steps.

**safe-delete rule when removing/replacing skills (⚠️ Required):**

When deleting skills under `.claude`, always:

```bash
mkdir -p ~/.claude/.bak
mv ~/.claude/skills/{old-skill} ~/.claude/.bak/
```

**Never**: Add `.bak` suffix in the same directory (`mv skill skill.bak`)
- This causes Claude Code to still load the `.bak` folder as a skill
- Must move to the `~/.claude/.bak/` root folder

**Skill rename backward compatibility (⚠️ Required):**

When renaming a skill (directory rename + `name` field update), create a **command alias** for the old name:

```bash
# ~/.claude/commands/{old-name}.md
$ARGUMENTS

Invoke skill: /{new-name} $ARGUMENTS
```

This allows `/old-name` to still work as a slash command. **Do not use symlinks** — Claude Code loads symlinked directories as duplicate skills.

Also update all `depends-on` references in other skills from old name to new name.

### 4-1. Auto-detect depends-on ⚠️ Required

**When running upgrade, detect references to other skills in the target skill's topic files and automatically update the `depends-on` field.**

Detection patterns:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `/skill-name` | Slash command reference | `/safe-delete`, `/skill-manager upgrade` |
| `Skill("name"` | Skill tool invocation | `Skill("safe-delete", ...)` |
| `skill-manager` (in topic files) | Uses skill-manager procedure | `When malfunction discovered, /skill-manager upgrade` |

Procedure:

1. Grep all `.md` files of the target skill for the above patterns
2. Verify that extracted skill names exist in `~/.claude/skills/` or `.claude/skills/`
3. Add only existing skills to the `depends-on` array
4. If `depends-on` already exists, merge (remove duplicates)

```yaml
# Before (no depends-on)
---
name: ralph
description: ...
---

# After (/safe-delete reference detected in PROMPT.md)
---
name: ralph
depends-on: [safe-delete]
description: ...
---
```

**This step is required, not optional.** It is always performed as a default behavior of upgrade.

### 5. Lint Verification

After upgrade, always run lint:

```
/skill-manager lint <skill-name>
```

### 5.5. Skill Scope Detection (MANDATORY — before Step 6)

**Before entering the commit flow, classify the modified skill as public or local-only.** Local-only skills (operator skills, personal infra tooling) must **not** be pushed through worktree / PR flows. Direct edit only — Step 6 is skipped.

#### 1st-class signal: `published.json`

The `es6kr` skill maintains `published.json` listing every skill published to ClawHub. Membership in this list is the canonical "public" signal:

```bash
# Locate published.json (path may drift — check both common locations)
PUB_JSON=$(find ~/.claude/skills/es6kr ~/.agents/skills/es6kr -maxdepth 3 -name "published.json" 2>/dev/null | head -1)

# Public: slug appears in published.json
jq -r --arg slug "<skill-name>" '.skills[] | select(.slug == $slug or .local == $slug) | .slug' "$PUB_JSON"

# Cross-check: tracked in the monorepo's main branch
git -C ~/.agents ls-files skills/<skill-name>/ | head -1
git -C ~/.agents ls-tree origin/main skills/<skill-name>/ 2>/dev/null | head -1
```

**Path verification (HARD STOP — when query returns empty)**: Before applying the "Not in `published.json`" matrix row, verify the file itself exists and the path is correct. An empty `jq` result has TWO causes — (a) skill genuinely absent, (b) path wrong / file missing. Conflating them silently downgrades a Public skill to Local-only.

```bash
# If jq returned empty, verify file:
[ -f "$PUB_JSON" ] || echo "published.json NOT FOUND — locate it before classifying"
```

#### Public-repo fallback (when published.json unreachable)

If `published.json` is missing/unreadable AND the skill is tracked in `~/.agents` AND `~/.agents` remote is the canonical public skills repo (`git@github.com:es6kr/skills.git` or equivalent), classify as **Public** by default. The remote URL is itself a public signal — every tracked path in a public repo is published.

```bash
REMOTE=$(git -C ~/.agents remote get-url origin 2>/dev/null)
case "$REMOTE" in
  *es6kr/skills*) PUBLIC_REPO=1 ;;
  *) PUBLIC_REPO=0 ;;
esac
```

#### Scope matrix

| Signals | Scope | Step 6 behavior |
|---------|-------|-----------------|
| In `published.json` + tracked in `origin/main` | **Public** | Run Step 6 commit + PR flow as written |
| `published.json` unreachable + tracked + `~/.agents` remote = `es6kr/skills` (or canonical public repo) | **Public** (fallback) | Treat as Public — Step 6 commit + PR flow |
| Not in `published.json` + tracked in `origin/main` (+ public-repo fallback fails) | **Repo-internal** (test fixtures, CI helpers — rare) | Commit directly to working branch; no public PR unless user requests |
| Not in `published.json` + **untracked** (`?? skills/<name>/`) | **Local-only** | **Skip Step 6 entirely**. Direct file edit only. Do not stage / commit / push / PR |
| In `published.json` but file untracked | First publish baseline | Apply "Publish-baseline split" subsection of Step 6 |

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Assume every `skills/<name>/` directory in `~/.agents` is publishable | Run the `jq` + `git ls-files` check first. Decide scope from signals, not directory presence |
| 2 | Propose a new worktree / PR for a local-only skill | Local-only = direct Edit on the existing working tree. No worktree split, no `gh pr create` |
| 3 | "Untracked = need to add" reflex (Step 6 Notes #3) | "Untracked + absent from published.json" = local-only signal. Do not add. The Step 6 Notes line about adding new files applies only to **public skills** introducing new topic files |
| 4 | Build a per-skill allowlist or check `LICENSE` presence to decide scope | `published.json` is the single 1st-class signal. Avoid composite matrices (see Step 2 Don't/Do row 6 — "Prefer the simplest 1st-class signal first") |
| 5 | Ask the user "should we commit?" before checking signals | Detect scope first, then act. Only ask if signals conflict (e.g., in `published.json` but path-ignored) |

#### Self-check (before entering Step 6)

1. Run the `jq` published.json query for `<skill-name>` — was it present?
2. **If jq returned empty: verify the path itself**. Run `[ -f "$PUB_JSON" ] && echo OK || echo MISSING`. If `MISSING`, run `find ~/.claude/skills/es6kr ~/.agents/skills/es6kr -name "published.json"` to relocate. **Do not classify as "Not in published.json" until you have confirmed the file actually exists at the queried path.**
3. Run `git -C ~/.agents ls-files skills/<skill-name>/` — was there at least one tracked file?
4. If jq returned empty but the file is missing/unreachable AND the skill is tracked AND `git -C ~/.agents remote get-url origin` matches the canonical public repo (`es6kr/skills`) → apply the **Public-repo fallback** row → classify as **Public**.
5. Map the answers onto the scope matrix
6. If **Local-only**, skip Step 6 entirely. Report to the user: "Local-only skill detected (not in published.json, untracked). Edit applied directly; no commit."
7. If **Public** (incl. fallback), proceed to Step 6.

### 6. Commit Changes (MANDATORY — after every skill modification, **Public or Repo-internal scope**)

**Gate**: Step 5.5 must have classified the skill as **Public** or **Repo-internal**. If classified as **Local-only**, this entire Step 6 is skipped — the file edit is the final deliverable.

After upgrade Edit/Write is complete, **commit the changed skill files in the `~/.agents` repo**. Skill changes left uncommitted accumulate and become hard to attribute later.

#### Branch guard (HARD STOP): PUBLIC skill → feat/fix branch, never develop/main direct

**For a PUBLIC skill (in `published.json`), the commit MUST land on a dedicated `feat/<slug>-...` or `fix/<slug>-...` branch (worktree-isolated), never directly on `develop`/`master`/`main`.** The es6kr/skills repo flow is feat/fix branch → PR → main (release-please runs on main). `develop` is NOT a change-accumulation branch for published skills. This mirrors `es6kr` `deploy-skill.md` §6 Branch strategy — keep the two consistent.

| # | Don't | Do |
|---|-------|-----|
| 1 | Offer "commit directly on develop" as an option for a PUBLIC skill change | Create/use a `fix/<slug>-...` or `feat/<slug>-...` branch (reuse-first via git-repo worktree) → commit there → PR |
| 2 | Treat the current branch (e.g., `develop`) as the commit target without checking | Check `git branch --show-current`. If develop/master/main + PUBLIC skill → switch to a feat/fix branch first |
| 3 | Commit on develop "because other uncommitted changes already sit there" | Other branches' dirty state is not a reason to add a published-skill commit to develop. Isolate on a feat/fix branch (worktree) |
| 4 | `git worktree add` a fresh worktree blindly | Follow git-repo worktree decision tree — reuse an inactive worktree first |

**Self-check (before the commit procedure below)**:
1. Is the skill PUBLIC (Step 5.5 result)? → If yes, this guard applies
2. `git branch --show-current` — is it develop/master/main? → If yes, **do not commit here**. Acquire a `fix/<slug>-...` branch via the git-repo `worktree` topic (reuse-first) and commit there
3. Only Repo-internal (rare) or Local-only skills may commit on the current working branch without a feat/fix branch

#### Procedure

1. **Identify modified files**: `git -C ~/.agents status --short skills/<skill-name>/`
2. **Stage by path** (no `git add .` / `-A`): `git -C ~/.agents add skills/<skill-name>/SKILL.md skills/<skill-name>/<topic>.md ...`
3. **Verify staging**: `git -C ~/.agents status` — confirm only the intended skill files are staged
4. **Commit**: `git -C ~/.agents commit -m "skill(<skill-name>): <one-line summary>"`
   - For new topic addition: `feat(skill-<skill-name>): add <topic-name> topic`
   - For existing topic edit: `docs(skill-<skill-name>): <what changed>`
   - For frontmatter/structure: `refactor(skill-<skill-name>): <what changed>`

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Edit a skill and end the task without staging | Stage and commit in the same flow as the upgrade execution |
| 2 | `git add .` or `git add -A` to stage everything | Stage only the files this upgrade modified, by explicit path |
| 3 | Bundle unrelated skill changes into one commit | One commit per skill (or per logical group). Scope by skill name |
| 4 | Skip commit because "other skills already have stale modifications" | Other skills' stale state is out of scope — commit only what this upgrade touched |
| 5 | Commit without verifying `git status` first | Always read `git status` output before commit to confirm scope |

#### Notes

- The commit step is part of the upgrade procedure, not a separate task. Do not stop after Step 5 (lint).
- If `git status` shows pre-existing modifications in other skills, **leave them alone** — they belong to the user / other sessions.
- New `.md` files under `skills/<new-skill>/` must be added explicitly (`git add skills/<new-skill>/`) because they are untracked.
- **PR bundling across multiple skills**: when this upgrade modifies 2+ skills (e.g., the target skill + a cross-cutting fix to `skill-kit/upgrade.md` itself), PR scoping follows **bump type**, not per-skill. **All patch-level changes go in one PR**; minor/major need their own PR. See `~/.agents/skills/es6kr/deploy-skill.md` "PR bundling by version bump type" section for the matrix. Commits stay per-skill (conventional commit header for release-please component routing), but the PR aggregates by bump type.

#### Publish-baseline split (MANDATORY when registering an externally-published skill for the first time)

When a skill is **already published externally** (ClawHub, npm, PyPI, VSCode marketplace, etc.) but
has never been committed to `~/.agents`, the first commit must **split into two**:

1. **Baseline commit**: the published version content, as-is. Captures what the external artifact
   currently represents.
2. **Follow-up commit(s)**: changes made in this session (new sections, fixes, refactors).

Bundling published baseline + new changes into a single commit makes attribution impossible:
"what was in the release" vs "what we added after" cannot be distinguished from `git log`.

##### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `git add skills/<published-skill>/` and commit everything as one | Stage published-version files first → commit "baseline" → stage in-session changes → commit "follow-up" |
| 2 | "It's untracked anyway, so one commit is fine" | Untracked + already-published = special case. Split required |
| 3 | Skip baseline split because the user didn't explicitly say "split" | If a user says "commit the published state first" or similar, treat it as a baseline-split request |
| 4 | Use `git reset --hard` to redo a bundled commit | `git reset --soft HEAD~1` only — preserves working tree, allows re-staging |

##### Procedure

1. **Identify the published-version content**: read the external artifact (ClawHub page, npm tarball,
   release tag) and reproduce its file state, **or** ask the user which session edits are
   "follow-up" vs baseline. The default is: every file in the in-session working tree minus the
   edits the LLM made this session = baseline.
2. **Stash in-session changes** if needed: `git stash` after a temporary in-tree copy, or use the
   filesystem to back up modified files before checking out clean.
3. **Commit baseline**: `git add skills/<skill>/<baseline-files>` → `git commit -m "feat(<skill>): import published vX.Y.Z baseline"`
4. **Re-apply in-session changes** to the working tree (stash pop, manual restore, or file copy)
5. **Commit follow-up**: `git add skills/<skill>/<changed-files>` → `git commit -m "<type>(<skill>): <what changed>"`

##### When user signals "publish baseline" intent

User phrases like "commit the deployed state to the worktree first", "publish state as baseline", or
"commit release as-is" all signal this split. Per the ambiguous-verb principle, the phrase
"as-deployed / at publish time / release as-is", the default interpretation is **baseline split**,
not "single commit in some order".

## Notes

- Topic files have no frontmatter (only exists in SKILL.md)
- Topics table in SKILL.md must always be kept in alphabetical order
- Scripts are created as permanent files in `scripts/` (tmp files forbidden)
