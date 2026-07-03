# Changelog Generation Reference

Complete procedures for automatically generating CHANGELOG entries from git history and change analysis.

**When to read**: When entering Phase 2B (update & iteration), after version bump is confirmed. Read this file in full before generating CHANGELOG entries.

---

## Auto-Generation from Git Log

### Step 1: Extract Commit History

```bash
# Get commits since last version tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$LAST_TAG" ]; then
  # No tags yet, get all commits
  git log --oneline
else
  git log ${LAST_TAG}..HEAD --oneline
fi
```

### Step 2: Parse Commit Messages

**Conventional Commits parsing**:

| Pattern | Category | Example |
|---------|----------|---------|
| `feat(scope):` | Added | `feat(skill): add provenance block` |
| `fix(scope):` | Fixed | `fix(docs): correct palette hex values` |
| `docs(scope):` | Changed (docs) | `docs(design): add layout recipe section` |
| `style(scope):` | Changed (style) | `style: format README tables` |
| `refactor(scope):` | Changed | `refactor(workflow): restructure Step C` |
| `feat(scope)!:` or `breaking:` | Breaking Changes | `feat(skill)!: change delivery pipeline` |
| `chore(scope):` | Skip (meta) | `chore: update .gitignore` |

**Non-conventional commits fallback**:

If commit messages don't follow Conventional Commits, analyze the actual file changes:

| Changed Files | Category | Entry |
|--------------|----------|-------|
| New file in references/ | Added | "Added <filename> reference document" |
| SKILL.md rules added | Added | "Added <N> new rules: <rule summaries>" |
| SKILL.md rules removed | Breaking Changes | "Removed <rule description>" |
| SKILL.md workflow steps changed | Changed | "Updated workflow: <summary>" |
| README.md/README.en.md | Changed | "Updated documentation" |
| .github/ templates | Added | "Added community issue/PR templates" |
| plugin.json version only | Skip | No entry needed |

### Step 3: Generate CHANGELOG Entry

**Template**:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes
- **[scope]**: Description of breaking change

### Added
- **[scope]**: Description of new feature
- **[scope]**: Description of new feature

### Changed
- **[scope]**: Description of change
- **[scope]**: Description of change

### Fixed
- **[scope]**: Description of fix

### Removed
- **[scope]**: Description of removal
```

**Rules**:
1. **Always prepend** the new entry at the top of CHANGELOG.md (after the header)
2. **Date format**: `YYYY-MM-DD` (ISO 8601)
3. **Version format**: `[X.Y.Z]` (brackets, semver)
4. **Scope is optional** but recommended for skills with multiple reference files
5. **Each entry should be a complete sentence** starting with a verb (Added/Changed/Fixed/Removed)
6. **Skip empty categories** — don't include `### Fixed` if there are no fixes
7. **Breaking Changes always first** — users must see them immediately

### Step 4: Merge with Existing CHANGELOG

```bash
# Read existing CHANGELOG
HEAD_LINES=$(head -5 CHANGELOG.md)

# Prepend new entry
# New entry goes after the header line "# Changelog" and the description
```

**Example result**:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [7.1.0] - 2026-06-11

### Added
- **skill**: provenance block (quote + HTML comment) for source identification
- **skill**: version sync rule — SKILL.md → plugin.json → CHANGELOG.md consistency check
- **community**: bug_report.yml, feature_request.yml, question.yml, config.yml, pull_request_template.md

### Changed
- **docs**: README rewritten as product landing page with 21-chapter structure
- **docs**: bilingual strategy changed from inline `---` separator to independent README.en.md file

## [7.0.0] - 2026-06-11

### Breaking Changes
- **design**: 24 Layout Recipes replace 10 layout tags
- **typography**: three-tier font system replaces flat sizing

### Added
...
```

---

## Smart Entry Generation from File Analysis

When git log is unavailable or insufficient, generate entries by analyzing actual file diffs.

### SKILL.md Diff Analysis

```bash
# Extract added/removed rules
git diff origin/main..HEAD -- SKILL.md | grep "^+" | grep "^-.*Rule\|^+.*Rule"
```

**Rule change patterns**:

| Pattern | Category | Entry |
|---------|----------|-------|
| New `## Rules` subsection | Added | "Added <subsection> rules" |
| New numbered rule | Added | "Added rule: <first 50 chars of rule>" |
| Removed numbered rule | Removed | "Removed rule: <summary>" |
| Changed rule text | Changed | "Updated rule: <summary>" |
| New Mode Detection | Added | "Added <mode> mode" |
| New Step in workflow | Added | "Added Step <letter>: <name>" |

### references/ Diff Analysis

```bash
# New reference files
git diff --diff-filter=A --name-only origin/main..HEAD -- 'references/*'

# Modified reference files
git diff --diff-filter=M --name-only origin/main..HEAD -- 'references/*'
```

**Entry generation**:

| Change | Category | Entry |
|--------|----------|-------|
| New file `references/X.md` | Added | "Added <X> reference document" |
| Significant content change (>20 lines) | Changed | "Updated <X>: <summary from first changed section>" |
| Minor content change (<20 lines) | Changed | "Minor updates to <X>" |

### README Diff Analysis

| Change | Category | Entry |
|--------|----------|-------|
| New section added | Changed | "Added <section> section to README" |
| Section rewritten | Changed | "Rewrote <section> section in README" |
| New README.en.md created | Added | "Added English documentation (README.en.md)" |
| Badge changes | Changed | "Updated README badges" |

---

## Release Notes Generation

### From CHANGELOG to Release Notes

**Release Notes are a subset of CHANGELOG**, not a copy. Rules:

1. **Only include user-facing changes** — skip internal refactoring
2. **Max 8 items** — if more, group related items
3. **Use Highlights + Validation format** (see publish-procedures.md)
4. **Language**: English for Release Notes

**Conversion table**:

| CHANGELOG Category | Release Notes Treatment |
|-------------------|------------------------|
| Breaking Changes | Always include in Highlights, prefix with "BREAKING:" |
| Added | Include in Highlights |
| Changed | Include only if user-visible |
| Fixed | Include only if user-reported |
| Removed | Include only if user-visible |

### Example Conversion

**CHANGELOG**:
```markdown
## [7.1.0] - 2026-06-11

### Added
- **skill**: provenance block for source identification
- **skill**: version sync rule
- **community**: issue/PR templates

### Changed
- **docs**: README rewritten as product landing page
- **docs**: bilingual strategy changed to independent files
```

**Release Notes**:
```markdown
## Highlights

- Added provenance block for skill source identification and traceability.
- Added community issue/PR templates under `.github/`.
- Rewrote README as product landing page with 21-chapter structure.
- Changed bilingual strategy from inline separator to independent README.en.md file.

## Validation

- Version sync verified across SKILL.md, plugin.json, and CHANGELOG.md.
- Security audit passed: no credentials, no local paths, no dangerous commands.
```

---

## Workflow Integration

The CHANGELOG generation is integrated into the update workflow as follows:

```
Phase 2B: Update & Iteration
    │
    ├── Step 1-4: Change detection + version bump (change-detection.md)
    │
    ├── Step 5: Version sync (SKILL.md → plugin.json → CHANGELOG.md)
    │
    ├── Step 6: Auto-generate CHANGELOG entry ← THIS FILE
    │   ├── Extract git log
    │   ├── Parse conventional commits (or analyze file diffs)
    │   ├── Generate entry with proper categories
    │   └── Prepend to CHANGELOG.md
    │
    ├── Step 7: Security audit
    │
    ├── Step 8: Push changes
    │
    ├── Step 9: Create/update Release (use Release Notes from CHANGELOG)
    │
    └── Step 10: Update ClawHub version
```
