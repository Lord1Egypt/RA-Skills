---
name: skill-factory
version: "2.4.0"
description: >
  Turn any idea into a polished, versioned, publishable OpenClaw skill — no
  scaffolding, no guesswork. Just say "新 skill" or "build a skill" and Skill
  Factory handles the rest: captures the spec, collects sources, distills
  knowledge, and packages it into a GitHub-ready repo. Also supports upgrading
  existing skills with "升级 skill" or "upgrade skill". Built for makers who
  want quality without reinventing the process. Triggers: "新 skill", "做一个skill",
  "build a skill", "create skill", "skill制作", "把这个做成skill", "帮我把...打包成skill",
  "skill升级", "skill发行", "skill factory", "制造skill", "skill工厂", "skill from scratch",
  "我有个skill想法", "skill迭代", "skill打磨", "做一个关于...的skill",
  "skill版本管理", "skill如何发行", "skill如何升级", "skill生产", "skill自动化",
  "更新skill", "升级skill", "维护skill", "升级已有skill", "upgrade skill",
  "update skill", "维护现有skill", "skill版本升级", "skill生命周期".
---

# Skill Factory — The Meta-Skill for Making Skills

> "The first industrial revolution was marked by using machines to make machines.
> Skill Factory is the machine that makes skills."

## Purpose

Skill Factory provides a **repeatable, human-AI collaborative SOP** for going from a raw idea to a polished, publishable OpenClaw skill. It handles:

- **0→1**: Rapid capture of fuzzy ideas → structured BRIEF → distilled skill
- **1→N**: Iterating an existing skill with new sources or structural improvements
- **N→∞**: Publishing, versioning, ClawHub distribution, and ongoing maintenance

The key insight: **this is not about capability, it's about workflow.** Any Claw instance with this skill loaded can build production-quality skills — the process is the product.

---

## How to Trigger This Skill

Just say something like:

> `New skill: [name], [1-2 sentences], [source URL (optional)]`
> `Upgrade skill: [skill name/path], [change request], [new source URL (optional)]`

### New skill examples:
- `New skill: prompt-engineering, best practices from Anthropic and OpenAI`
- `New skill: git-workflow, standardize my branching and PR flow, https://...`
- `新 skill：简历筛选，用关键词匹配和语义分析筛选简历`

### Upgrade skill examples:
- `Upgrade skill: nova-reader, add Semantic Scholar data source`
- `Upgrade skill: harness, strengthen governance rules from Phase 3.5 lessons`
- `升级 skill：skill-factory，增加显式升级模式`

Claw will enter **Phase 0** for new skills or the **Upgrade Workflow** for existing skills — no more information needed to start.

**中文用户**: `新 skill：[名字]，[1-2句说明]，[来源URL（可选）]` for new; `升级 skill：[skill名字/路径]，[变更要求]，[新来源URL（可选）]` for upgrades.

---

## Four-Phase SOP

### Phase 0 · Capture（≤5 min）

**Goal**: Lock down the spec before any work begins.

1. Save raw idea to `inbox/<skill-name>.md` (防止遗失)
2. Ask exactly **3 questions** — no more:
   - What is the target scenario / user?
   - Are there reference sources? (If not, Claw will search)
   - Publish scope: local-only / GitHub / ClawHub distribution?
3. Generate `wip/<skill-name>/BRIEF.md`

**Key principle**: Phase 0 prevents over-engineering (LRN-003). Don't start building until the 3 questions are answered.

---

### Phase 1 · Collect（automated）

**Goal**: Gather raw material without processing.

1. `web_fetch` each source → save to `wip/<skill-name>/raw/`
2. If no sources provided, `web_search` for 2–3 high-quality references
3. Prioritize: official docs > primary blog posts > secondary analysis

**Rule**: At least 1 first-party source (official docs / original author's post). Raw content is saved as-is — no processing yet.

---

### Phase 2 · Distill（core work）

**Goal**: Extract signal, discard noise.

1. Read all `raw/` files
2. Write per skill-creator spec:
   - `SKILL.md` — triggers + workflow (≤200 lines)
   - `references/` — detailed knowledge, split by topic
   - `scripts/` — reusable code, only if needed
3. **Mandatory verification** (LRN-001): Re-fetch original source, diff against draft, check for gaps

**Quality checklist**:
- [ ] Trigger words are broad enough to cover all user phrasings
- [ ] SKILL.md has a clear "when to use" section
- [ ] Detail lives in `references/`, not bloating `SKILL.md`
- [ ] At least one mandatory re-read of primary source after distillation

---

### Phase 3 · Publish

**Goal**: Clean, versioned, standalone repo ready for GitHub/ClawHub.

#### Repo Structure (Minimal)

```
<skill-name>/
├── SKILL.md          # Entry point (triggers + workflow)
├── README.md         # Human-facing intro — bilingual (EN + ZH)
├── CHANGELOG.md      # Version history
├── LICENSE           # MIT recommended
├── .gitignore
└── references/       # Knowledge base
    └── *.md
```

For script-heavy skills, add:
```
└── scripts/
    └── *.py
```

#### README Spec

A skill README must answer 3 questions in ≤60 seconds of reading:
1. **What problem does it solve?** (1-2 sentences, no jargon)
2. **What makes it better than asking without it?** (key differentiator)
3. **How do I use it?** (one concrete example)

**Bilingual (EN + ZH)**: Use two separate files for maximum clarity.

```
README.md       # English only — no Chinese text anywhere
README_zh.md    # Chinese only — full detail, selling points, usage
```

Each file includes a badge linking to the other version. This allows GitHub to render clean language-specific views and enables future ClawHub to surface the right version per locale.

#### ClawHub Distribution

When the user wants to publish to ClawHub:
1. Ensure `SKILL.md` frontmatter has: `name`, `version`, `description`
2. `description` must contain broad trigger phrases covering multiple phrasings
3. `LICENSE` file present (MIT recommended)
4. Tag the release: `git tag v1.0.0 && git push --tags`

#### ClawHub CLI Publishing (实操工作流)

When the skill is already published and needs a version update on ClawHub, use the `clawhub` CLI:

**Prerequisites:**
- Node.js environment with clawhub package installed:
  ```
  npm install clawhub
  ```
- ClawHub account with device flow login (headless-friendly):
  ```
  clawhub login --device
  # Visit the provided URL, enter the code, authorize in browser
  # Note: login process must stay running in background while user authorizes
  ```

**Publish update workflow:**
```bash
# 1. Push latest commit to GitHub first
git push origin main

# 2. Tag the release
git tag v<new-version>
git push --tags

# 3. Publish to ClawHub
clawhub skill publish <repo-path> --slug <slug> --version <new-version> --changelog "<summary>"

# 4. Verify
clawhub inspect <slug>

# 5. Sync to local workspace
Copy-Item -Recurse -Force "D:\Agent\WorkBuddy\skills\<skill-name>\*" "$env:USERPROFILE\.workbuddy\skills\<skill-name>\"
```

**Protocol: GitHub first, ClawHub second.** Always push to GitHub before publishing to ClawHub. This ensures the source code is available for moderation review and users can link back to the repo.

**Windows + Proxy note:** Use HTTPS remote (not SSH) on Windows environments with proxy/VPN. SSH port 22 may be intercepted by proxy tools (Clash/V2Ray). Configure:
```
git remote set-url origin https://github.com/<owner>/<repo>.git
```

**Limitation:** ClawHub Summary is derived from SKILL.md frontmatter `description` field. To update the summary, edit `description` in SKILL.md and republish.

#### Auto-Sync Automation (Optional)

A local workbuddy automation can periodically check and sync all skills:

```yaml
# One-time manual: for each repo, push + publish + sync
# Or set a weekly cron via workbuddy automation
```

See `automation` system in WorkBuddy for setting up recurring sync tasks.

#### Sync to Local Workspace

After publishing, sync to `~/.workbuddy/skills/<skill-name>/` so Claw can use it immediately:

```powershell
Copy-Item -Recurse -Force "D:\Agent\WorkBuddy\skills\<skill-name>\*" "$env:USERPROFILE\.workbuddy\skills\<skill-name>\"
```

---

## Upgrade Workflow (1→N Maintenance)

**Goal**: Update an existing skill without starting from scratch.

This is a **first-class workflow**, distinct from creating a new skill. When the user invokes `Upgrade skill:`, follow these steps:

### Step 1 · Inspect (read existing state)

1. Read the existing skill repo:
   - `SKILL.md` — current version, triggers, workflow
   - `CHANGELOG.md` — version history (especially recent entries)
   - `README.md` — public description
   - `references/` — existing knowledge base
   - Git log — recent changes and commit history
2. Identify the current version (from `SKILL.md` frontmatter or git tag)

### Step 2 · Classify the change

Compare the requested change against the skill's **public API** — its documented behavior:

| Public API element | Examples |
|-------------------|----------|
| Use cases | What scenarios the skill serves |
| Input format | What the user says to trigger the skill |
| Output format | What files/code the skill produces |
| Workflow phases | The SOP structure |
| Safety boundaries | What the agent must not do |
| File structure | Repo layout conventions |
| Publishing behavior | How the skill is distributed |

Determine the version bump:

| Bump | When | Examples |
|------|------|----------|
| **PATCH** `x.x.1` | Fixes that don't change behavior | Typo fix, clarification, trigger word tweak |
| **MINOR** `x.1.0` | Backward-compatible additions | New workflow mode, new reference source, optional publishing path |
| **MAJOR** `x.0.0` | Breaking changes | Changed triggering format, restructured SOP, removed phase, changed safety assumptions |

### Step 3 · Propose (generate upgrade plan)

Before making any changes, produce an upgrade plan:

```markdown
## Upgrade Plan

Current version: <version from SKILL.md>
Proposed version: <computed bump>
Change type: PATCH / MINOR / MAJOR

Reason:
<why this change belongs in this category>

Files to modify:
<list of files that need changes>

Risk level: low / medium / high
Backward compatibility: yes / no

Proposed changelog entry:
### Added
- <new features>

### Changed
- <behavior changes>

### Fixed
- <bug fixes>

Suggested commit message:
<semantic commit message>

Suggested tag:
v<new version>
```

Present this plan to the user. Do not apply changes until the user confirms.

### Step 4 · Apply

After user confirmation:

1. Update files (SKILL.md, README, CHANGELOG, references)
2. Bump version in SKILL.md frontmatter and README badges
3. Update `CHANGELOG.md` with proper format (see below)
4. Commit with semantic message
5. Tag the release: `git tag v<new-version> && git push --tags`
6. Re-sync to local workspace

### Step 5 · Upgrade Summary

After applying, produce a summary:

```
## Upgrade Complete

<old version> → <new version>
Files changed: <list>
Changelog: <link or excerpt>
Next steps: <optional>
```

---

## Version Management

Version semantics follow **Semantic Versioning** adapted for skills:

```
MAJOR.MINOR.PATCH
```

| Version bump | When | Example trigger |
|---|---|---|
| **PATCH** `x.x.1` | Typo fix, trigger word tweak, minor clarification | "修复了一个例子描述不准" |
| **MINOR** `x.1.0` | New reference source, new phase step, extended trigger coverage | "加入 Anthropic 最新文档" |
| **MAJOR** `2.0.0` | Scope change, structural refactor, paradigm shift | "从单文档改为多 reference 结构" |

### What warrants a MAJOR bump?

A MAJOR version (e.g. 1.x → 2.0) signals a **breaking change in the skill's mental model**:
- The core SOP phases are restructured
- The skill's scope is fundamentally redefined
- Files are reorganized in ways that break the previous structure
- The activation paradigm changes (e.g. from "ask anything" to "four-phase SOP")

**MAJOR ≠ more content**. A skill that doubles its references but keeps the same structure is still a MINOR bump.

### What warrants a MINOR bump?

A MINOR version (e.g. 1.0 → 1.1 → 1.2) signals **additive improvements** that don't break the existing pattern:
- New knowledge source added to `references/`
- New trigger words added to frontmatter
- New section added to SOP without restructuring existing phases
- README improvements, badge updates

### Commit message convention

```
feat: add [source] to references        → MINOR
fix: correct [description]              → PATCH
refactor: restructure [component]       → could be MAJOR
release: v2.0.0 - [summary]            → tag release commits
```

### Changelog discipline

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

Every release must update `CHANGELOG.md` with:
- `[Unreleased]` section at the top (collects next-version changes)
- Version section for each release: `[X.Y.Z] — YYYY-MM-DD`
- Grouped changes under: **Added**, **Changed**, **Fixed**, **Deprecated**, **Removed**, **Security**
- User-readable summaries, not raw git diffs
- A single-line **Summary** at the top of each version

The `[Unreleased]` section captures changes that will go into the next release. Before cutting a new version, review `[Unreleased]`, classify entries, and move them into the version section.

**Distinction**: git history = developer log; CHANGELOG = user-facing narrative. Do not substitute one for the other.

---

## Skill Iteration (Legacy — use Upgrade Workflow above)

The legacy iteration path is preserved for quick edits. For structured upgrades, use the **Upgrade Workflow** (produces planned changes and version bump).

When doing a quick upgrade:

1. Create a new branch or directly update `D:/Agent/WorkBuddy/skills/<skill-name>/`
2. Add new source to `references/` with dated filename (`source-YYYYMMDD.md`)
3. Update `SKILL.md` version field and trigger words if needed
4. Update `CHANGELOG.md`
5. Bump version (MAJOR / MINOR / PATCH per rules above)
6. Commit with semantic message
7. Re-sync to local workspace

**Upgrade triggers**: User sends new URL, user says "skill has a gap", Claw detects missing knowledge during a task execution.

---

## Workspace Layout

```
D:/WorkBuddy/
└── .workspace-index.md      # Master skill status board

D:/Agent/WorkBuddy/skills/
├── skill-factory/           # This meta-skill repo
│   ├── SKILL.md             # This file
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── LICENSE
│   ├── .gitignore
│   ├── CLAWHUB.md
│   ├── inbox/               # Raw ideas drop zone
│   └── wip/                 # Active work-in-progress
│       └── <skill-name>/
│           ├── BRIEF.md
│           ├── raw/
│           └── draft/
│
├── harness/                 # ✅ v1.2.0 — ready for GitHub
├── nova-reader/             # ✅ v1.1.0 — ready for GitHub
└── <future-skills>/
```

---

## Lessons Learned (from .learnings)

| ID | Lesson | Fix in SOP |
|----|--------|-----------|
| LRN-001 | Missed content after distillation without re-reading source | Phase 2 mandatory re-fetch |
| LRN-002 | Skill evolved in workspace, hard to publish as standalone | Phase 3 independent repo |
| LRN-003 | Over-engineered before confirming real need | Phase 0 three-question lock |
| LRN-004 | Research notes mixed with skill docs | `raw/` vs `references/` separation |
| LRN-005 | ClawHub login needs background process to wait for user auth | Device Flow requires staying alive |
| LRN-006 | Git push blocked by proxy/VPN (SSH 22) on Windows | Use HTTPS + PAT, configure remote |
| LRN-007 | Requirement creep during simple tasks | Core first, periphery later |
