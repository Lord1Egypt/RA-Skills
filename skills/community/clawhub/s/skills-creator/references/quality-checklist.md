# Quality Checklist

Use this checklist to review a skill before publishing, or to audit an existing skill for improvement.

## Pre-Publication Checklist

### Frontmatter (6 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| F1 | `name` is lowercase kebab-case and matches folder name | | |
| F2 | `description` starts with action verb and includes 5+ trigger phrases | | |
| F3 | `version` is present and follows semver | | |
| F4 | `metadata` is single-line JSON (not multiline YAML) | | |
| F5 | `requires.bins` lists ALL executables the skill needs (including `node`, `npx`) | | |
| F6 | No `_meta.json` file committed (ClawHub auto-generates it) | | |

### Description Quality (4 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| D1 | Starts with action verb (not "A skill that..." or passive voice) | | |
| D2 | Includes 5+ specific trigger phrases in quotes | | |
| D3 | Covers at least 2 topic areas ("discusses X, Y") | | |
| D4 | Under 500 characters (long descriptions get truncated) | | |

### Content Structure (5 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| C1 | Quick Reference table present within first 30 lines of body | | |
| C2 | Decision logic uses tables, not prose paragraphs | | |
| C3 | Workflow modes defined for distinct use cases | | |
| C4 | Negative cases handled (what to do when things fail) | | |
| C5 | Concrete examples at each step (not just abstract rules) | | |

### Self-Consistency (3 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| S1 | Skill follows every rule it teaches | | |
| S2 | No conflicting instructions between sections | | |
| S3 | All referenced files (`references/`, `scripts/`, `assets/`) actually exist | | |

### Security (3 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| X1 | No sensitive terms that trigger VirusTotal ("upload", "public URL", "CDN") | | |
| X2 | All npx/package references use pinned versions (not `@latest`) | | |
| X3 | No secrets, tokens, or credentials in skill files | | |

### Supporting Files (3 checks)

| # | Check | Pass? | Notes |
|---|-------|-------|-------|
| P1 | `references/` used for content that would push SKILL.md past 300 lines | | |
| P2 | `scripts/` use `{baseDir}` for portable paths, not absolute paths | | |
| P3 | `assets/` templates use `[TODO: ...]` placeholders, not hardcoded values | | |

---

## Retrofit Process

For improving existing skills that don't follow best practices:

### Step 1: Audit

Run the full checklist above. Mark every failure.

### Step 2: Sort by impact

Fix in this order (highest impact first):

1. **Description** (D1–D4) — determines whether the skill activates at all
2. **Content structure** (C1–C5) — determines how well the LLM executes
3. **Security** (X1–X3) — determines whether ClawHub accepts the skill
4. **Frontmatter** (F1–F6) — determines metadata correctness
5. **Self-consistency** (S1–S3) — determines trust and reliability
6. **Supporting files** (P1–P3) — determines maintainability

### Step 3: Rewrite description

Apply the formula: `[Action verb] + [value proposition]. Use when [triggers] or discusses [topics].`

**Before**:
> A tool for managing Docker containers and configurations.

**After**:
> Manage Docker containers, fix build failures, and optimize configurations. Use when someone asks to "fix Docker build", "container not starting", "optimize Dockerfile", "Docker on M1", or discusses Docker troubleshooting, container management, or build optimization.

### Step 4: Add Quick Reference table

Extract the skill's main capabilities into a dispatch table:

**Before** (prose):
> This skill can help with building images, managing containers, debugging network issues, and optimizing Dockerfiles.

**After** (table):

```markdown
| User wants... | Do this |
|---------------|---------|
| Build an image | → Mode 1: Check Dockerfile, run build with platform flag |
| Debug container | → Mode 2: Check logs, inspect network, verify env vars |
| Optimize Dockerfile | → Mode 3: Multi-stage build, layer caching, size reduction |
```

### Step 5: Convert prose to tables

Find paragraphs with conditional logic and restructure:

**Before**:
> If the error is a platform mismatch, add the --platform flag. If it's a missing dependency, check the Dockerfile's RUN commands. If it's a permission issue, verify the USER instruction.

**After**:

```markdown
| Error type | Fix |
|-----------|-----|
| Platform mismatch | Add `--platform linux/amd64` to build command |
| Missing dependency | Check `RUN` commands in Dockerfile |
| Permission denied | Verify `USER` instruction and file ownership |
```

### Step 6: Add guard clauses and negative cases

Ensure the skill handles failures:

```markdown
### When No Fix Works

If none of the above resolves the issue:
1. Check Docker version: `docker --version` (require 20.10+)
2. Try clean build: `docker build --no-cache .`
3. Suggest the user file an issue with the error output
```

### Step 7: Extract deep content

If SKILL.md exceeds 300 lines after improvements:
- Move detailed examples to `references/examples.md`
- Move troubleshooting to `references/troubleshooting.md`
- Keep SKILL.md as the dispatch layer with `{baseDir}/references/` links

### Step 8: Re-audit

Run the full checklist again. All 24 checks should pass.

---

## Scoring Rubric

Quick assessment scale for skill quality:

| Score | Description | Typical issues |
|-------|-------------|----------------|
| **5** | All 24 checks pass. Excellent description with 5+ triggers. Clean table-driven structure. | None |
| **4** | Minor issues. Missing 1–2 trigger phrases, or one section could be a table. | Cosmetic |
| **3** | Functional but description is weak or structure is prose-heavy. Triggers unreliably. | Description + structure |
| **2** | Missing key elements: no Quick Reference, no workflow modes, poor description. | Multiple structural gaps |
| **1** | Fundamental issues: broken frontmatter, no trigger phrases, conflicting instructions. | Needs full rewrite |

**Target**: Score 4+ before publishing. Score 3 skills should be retrofitted before release.
