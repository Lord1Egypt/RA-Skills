# Change Detection & Version Bump Reference

Complete procedures for detecting changes between local and remote, and automatically calculating version bumps.

**When to read**: When entering Phase 2B (update & iteration). Read this file in full before executing any version bump.

---

## Change Detection

### Step 1: Detect Local Changes

```bash
# Check if there are uncommitted changes
git status --short

# Check diff between local and remote
git fetch origin main
git log origin/main..HEAD --oneline

# If no remote yet, check diff from last tag
git describe --tags --abbrev=0 2>/dev/null
git log <last-tag>..HEAD --oneline
```

### Step 2: Categorize Changed Files

```bash
# List changed files with categories
git diff --name-only origin/main..HEAD
```

**File Category Mapping**:

| File Pattern | Category | Version Impact |
|-------------|----------|---------------|
| `SKILL.md` frontmatter (`version`, `name`, `description`) | **Breaking** | MAJOR |
| `SKILL.md` rules (added/removed rules) | **Feature** | MINOR |
| `SKILL.md` workflow steps (added/removed steps) | **Feature** | MINOR |
| `SKILL.md` persona/task/scope changes | **Feature** | MINOR |
| `references/*.md` (new files) | **Feature** | MINOR |
| `references/*.md` (content changes) | **Enhancement** | MINOR or PATCH |
| `README.md` / `README.en.md` | **Docs** | PATCH |
| `CHANGELOG.md` | **Meta** | No bump |
| `.github/**` | **Community** | PATCH |
| `.claude-plugin/plugin.json` | **Meta** | No bump (follows SKILL.md) |
| `LICENSE` / `.gitignore` | **Meta** | No bump |

### Step 3: Determine Version Bump

**Decision Tree**:

```
Analyze all changed files
    │
    ├── Any SKILL.md frontmatter breaking change?
    │   (version/name/description changed, or rules removed)
    │   → MAJOR bump (X.0.0)
    │
    ├── Any new rules / new workflow steps / new reference files?
    │   → MINOR bump (0.X.0)
    │
    ├── Any reference content changes / new community templates?
    │   → MINOR bump (0.X.0) if significant
    │   → PATCH bump (0.0.X) if minor
    │
    └── Only README / docs / meta changes?
        → PATCH bump (0.0.X)
```

**Significance Test for "MINOR or PATCH"**:

| Criteria | MINOR | PATCH |
|----------|-------|-------|
| New reference file added | ✅ | |
| Reference file content significantly rewritten | ✅ | |
| Reference file typo fixes / minor clarifications | | ✅ |
| New community template added | ✅ | |
| README section restructured | | ✅ |
| Badge / link updates | | ✅ |

### Step 4: Calculate New Version

```bash
# Get current version from SKILL.md frontmatter
CURRENT_VERSION=$(grep '^version:' SKILL.md | sed 's/version: *"\(.*\)"/\1/')

# Calculate new version
# MAJOR: 7.0.0 → 8.0.0
# MINOR: 7.0.0 → 7.1.0
# PATCH: 7.0.0 → 7.0.1
```

**Version Calculation Rules**:
- Pre-release versions (e.g., `7.0.0-beta`) are not supported — always use stable semver
- If current version has no PATCH component (e.g., `7.0`), treat as `7.0.0`
- Version must always be 3 components: `MAJOR.MINOR.PATCH`

### Step 5: Confirm with User

**Always confirm the version bump with the user before proceeding.**

Present the analysis:

```
变更分析：
- SKILL.md: 新增 2 条规则，修改 1 条规则
- references/workflow.md: 新增 Step G 截图优化
- README.md: 新增已知限制章节

推荐版本: 7.0.0 → 7.1.0 (MINOR bump)
原因: 新增规则和工作流步骤

确认？(可以修改版本号)
```

---

## Version Bump Execution

### Step 1: Update SKILL.md frontmatter

```yaml
# Before
version: "7.0.0"

# After
version: "7.1.0"
```

### Step 2: Update plugin.json

```json
{
  "version": "7.1.0"
}
```

### Step 3: Verify Version Consistency

**Three-file sync check** (Rule 12):

```bash
# Extract versions
SKILL_VERSION=$(grep '^version:' SKILL.md | sed 's/version: *"\(.*\)"/\1/')
PLUGIN_VERSION=$(grep '"version"' .claude-plugin/plugin.json | sed 's/.*: *"\(.*\)".*/\1/')
CHANGELOG_VERSION=$(head -20 CHANGELOG.md | grep -oP '\[\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)

# Compare
if [ "$SKILL_VERSION" != "$PLUGIN_VERSION" ]; then
  echo "ERROR: SKILL.md ($SKILL_VERSION) != plugin.json ($PLUGIN_VERSION)"
  exit 1
fi
```

**If versions don't match**: Update all to the new version. SKILL.md is the source of truth.

---

## Conventional Commits Guide

### Commit Message Format

```
<type>(<scope>): <subject>

<body>
```

### Types

| Type | Version Impact | Description |
|------|---------------|-------------|
| `feat` | MINOR | New feature / rule / workflow step |
| `fix` | PATCH | Bug fix / rule correction |
| `docs` | PATCH | README / documentation changes |
| `style` | PATCH | Formatting, no content change |
| `refactor` | PATCH | Restructure without behavior change |
| `test` | PATCH | Add or update tests |
| `chore` | No bump | Build / tool / meta changes |
| `breaking` | MAJOR | Breaking change (or `feat!:` / `fix!:`) |

### Scope Examples

| Scope | Files |
|-------|-------|
| `skill` | SKILL.md |
| `docs` | README.md, README.en.md, CHANGELOG.md |
| `design` | references/design-system.md, references/assets.md |
| `workflow` | references/workflow.md |
| `quality` | references/quality-gates.md |
| `community` | .github/ |
| `meta` | plugin.json, .gitignore, LICENSE |

### Examples

```bash
git commit -m "feat(skill): add provenance block and version sync rule"
git commit -m "fix(docs): correct Swiss palette hex values in README.en.md"
git commit -m "docs(design): add 24 layout recipe section to README"
git commit -m "feat(workflow)!: change screenshot delivery from React to HTML"
```

**Breaking change indicator**: `!` after scope means MAJOR bump.

---

## Update Workflow Summary

```
用户说"更新 wx-peitu" / "迭代 react-design-draft"
    │
    ├── Step 1: git fetch + git diff → 检测变更文件
    │
    ├── Step 2: 按文件类别映射 → 判断变更类型
    │
    ├── Step 3: 决策树 → 推荐 MAJOR/MINOR/PATCH
    │
    ├── Step 4: 向用户确认版本号
    │
    ├── Step 5: 三文件同步更新版本号
    │   (SKILL.md → plugin.json → CHANGELOG.md)
    │
    ├── Step 6: 自动生成 CHANGELOG 条目
    │   (Read references/changelog-generation.md)
    │
    ├── Step 7: 安全审查（三类扫描）
    │
    ├── Step 8: 推送变更
    │   (git push → gh CLI → REST API 降级)
    │
    ├── Step 9: 创建/更新 Release
    │
    └── Step 10: 更新 ClawHub 版本
```
