---
name: update-docs
description: This skill should be used when the user asks to "update documentation for my changes", "check docs for this PR", "what docs need updating", "sync docs with code", "scaffold docs for this feature", "document this feature", "review docs completeness", "add docs for this change", "what documentation is affected", "docs impact", or mentions "docs/", "skills/", "MDX", "documentation update", "API reference", ".md files". Provides guided workflow for updating OpenClaw documentation based on code changes.
---

# OpenClaw Documentation Updater

Guides you through updating OpenClaw documentation based on code changes on the active branch. Designed for maintainers reviewing PRs for documentation completeness.

## Quick Start

1. **Analyze changes**: Run `git diff main...HEAD --stat` to see what files changed
2. **Identify affected docs**: Map changed source files to documentation paths
3. **Review each doc**: Walk through updates with user confirmation
4. **Validate**: Check formatting and links
5. **Commit**: Stage documentation changes

## Workflow: Analyze Code Changes

### Step 1: Get the diff

```bash
# See all changed files on this branch
git diff main...HEAD --stat

# See changes in specific areas
git diff main...HEAD -- skills/
git diff main...HEAD -- src/api/
```

### Step 2: Identify documentation-relevant changes

Look for changes in these areas:

| Source Path | Likely Doc Impact |
|-------------|------------------|
| `skills/` | Skill documentation |
| `src/api/` | API reference documentation |
| `src/config/` | Configuration guides |
| `examples/` | Tutorial and example guides |
| `src/core/` | Core architecture documentation |

### Step 3: Map to documentation files

Use the code-to-docs mapping in `references/CODE-TO-DOCS-MAPPING.md` to find corresponding documentation files.

Example mappings:

- `skills/browser-hosting/` → `docs/skills/browser-hosting.md`
- `src/api/browser.ts` → `docs/api/browser.md`
- `examples/basic-agent/` → `docs/guides/basic-agent.md`

## Workflow: Update Existing Documentation

### Step 1: Read the current documentation

Before making changes, read the existing doc to understand:

- Current structure and sections
- Frontmatter fields in use
- Code examples and their accuracy

### Step 2: Identify what needs updating

Common updates include:

- **New features/options**: Add to reference tables and create sections explaining usage
- **Changed behavior**: Update descriptions and examples
- **Deprecated features**: Add deprecation notices and migration guidance
- **New examples**: Add code blocks following conventions

### Step 3: Apply updates with confirmation

For each change:

1. Show the user what you plan to change
2. Wait for confirmation before editing
3. Apply the edit
4. Move to the next change

### Step 4: Validate changes

Check documentation for common issues:
- Frontmatter has required fields (`title`, `description`)
- Code blocks are properly formatted
- Links point to valid paths
- Spelling and grammar

## Workflow: Scaffold New Feature Documentation

Use this when adding documentation for entirely new features.

### Step 1: Determine the doc type

| Feature Type | Doc Location | Template |
|--------------|-------------|----------|
| New skill | `docs/skills/` | Skill Reference |
| New API function | `docs/api/` | API Reference |
| New config option | `docs/config/` | Config Reference |
| New concept/guide | `docs/guides/` | Guide |
| Core architecture | `docs/architecture/` | Architecture Guide |

### Step 2: Create the file with proper naming

- Use kebab-case: `my-new-feature.md`
- Add numeric prefix if ordering matters: `05-my-new-feature.md`
- Place in the correct directory based on feature type

### Step 3: Use the appropriate template

**API Reference Template:** See `assets/api-reference-template.md`

**Guide Template:** See `assets/guide-template.md`

### Step 4: Add related links

Update frontmatter with related documentation:

```yaml
related:
  title: Next Steps
  description: Learn more about related features.
  links:
    - api/browser
    - guides/browser-automation
```

## Documentation Conventions

See `references/DOC-CONVENTIONS.md` for complete formatting rules.

### Quick Reference

**Frontmatter (required):**

```yaml
---
title: Page Title (2-3 words)
description: One or two sentences describing the page.
---
```

**Code blocks:**

```python
# Python example
code_here()
```

```javascript
// JavaScript example  
code_here();
```

**Notes:**

```markdown
> **Good to know**: Single line note.

> **Good to know**:
>
> - Multi-line note point 1
> - Multi-line note point 2
```

## Validation Checklist

Before committing documentation changes:

- [ ] Frontmatter has `title` and `description`
- [ ] Code blocks have proper language specification
- [ ] Links point to valid paths
- [ ] Spelling and grammar are correct
- [ ] Examples are tested and working
- [ ] Documentation matches current code behavior

## References

- `references/DOC-CONVENTIONS.md` - Complete frontmatter and formatting rules
- `references/CODE-TO-DOCS-MAPPING.md` - Source code to documentation mapping
- `assets/api-reference-template.md` - API reference template
- `assets/guide-template.md` - Guide template