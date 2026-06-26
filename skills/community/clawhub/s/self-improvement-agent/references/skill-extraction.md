# Skill Extraction Workflow

When a learning becomes valuable enough to warrant its own skill, extract it.

## Extraction Criteria

A learning qualifies when **ANY** of these apply:

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar entries |
| **Verified** | Status is `resolved` with working fix |
| **Non-obvious** | Required actual debugging to discover |
| **Broadly applicable** | Useful across codebases, not project-specific |
| **User-flagged** | User says "save this as a skill" |

## Extraction Workflow

### 1. Identify Candidate

Watch for these signals:
- Multiple `See Also` links in a learning entry
- High priority + resolved status
- Category: `best_practice` with broad scope
- User: "Save this as a skill", "This would be useful elsewhere"

### 2. Run Helper (or Create Manually)

```bash
# Dry run first
./scripts/extract-skill.sh skill-name --dry-run

# Then execute
./scripts/extract-skill.sh skill-name
```

### 3. Customize SKILL.md

Use `assets/SKILL-TEMPLATE.md` as starting point. Fill in:
- `name`: lowercase, hyphens (e.g. `docker-m1-fixes`)
- `description`: clear trigger conditions — what situation calls this skill?
- Body: distilled solution, not the full incident write-up

### 4. Update Original Learning

Set status to `promoted_to_skill` and add `Skill-Path`.

### 5. Verify

Read skill in a fresh session to confirm it's self-contained and actionable.

## Example

**Learning** (verbose):
> Docker build fails on M1 Mac because base image `python:3.11-slim` has no ARM64 variant.
> Must add `--platform linux/amd64` or use `FROM --platform=linux/amd64`.

**Extracted skill** (`skills/docker-m1-fixes/SKILL.md`):

```yaml
---
name: docker-m1-fixes
description: "Fix Docker build failures on Apple Silicon. Use when docker build
  fails with 'no match for platform linux/arm64' or similar errors."
---
# Docker M1 Fixes

## Quick

| Error | Fix |
|-------|-----|
| `no match for platform linux/arm64` | `docker build --platform linux/amd64 -t myapp .` |

## Solutions

### Build Flag (Recommended)
`docker build --platform linux/amd64 -t myapp .`

### Dockerfile
`FROM --platform=linux/amd64 python:3.11-slim`

### Docker Compose
```yaml
services:
  app:
    platform: linux/amd64
```
```

## Quality Gates

Before publishing:
- [ ] Solution is tested and working
- [ ] Description is clear without original context
- [ ] Code examples are self-contained
- [ ] No project-specific hardcoded values
- [ ] Name matches folder (lowercase, hyphens)
