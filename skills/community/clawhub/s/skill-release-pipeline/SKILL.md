---
name: skill-publisher
description: Package, publish, and distribute OpenClaw skills to GitHub and ClawHub. Activate when user wants to: (1) package a skill folder for distribution, (2) push a skill to a GitHub repo, (3) publish a skill to ClawHub registry, (4) sync a skill across GitHub and ClawHub. NOT for: creating skill content, writing SKILL.md, or installing skills.
---

# Skill Publisher

Automate the full lifecycle of publishing OpenClaw skills: package → GitHub → ClawHub.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- `npx clawhub` CLI authenticated (`npx clawhub whoami`)
- A skill folder with a valid `SKILL.md`

## Quick Start

### Full Pipeline (package + GitHub + ClawHub)

```bash
# From the skill directory
scripts/publish.sh /path/to/skill-folder --repo owner/repo-name --version 1.0.0
```

### Individual Steps

```bash
# 1. Validate & package only
scripts/validate.sh /path/to/skill-folder

# 2. Push to GitHub
scripts/push-github.sh /path/to/skill-folder --repo owner/repo-name

# 3. Publish to ClawHub
npx clawhub publish /path/to/skill-folder --version 1.0.0 --slug skill-name
```

## Workflow

### Step 1: Prepare the Skill Folder

Ensure the skill folder contains:

```
skill-name/
├── SKILL.md          (required — YAML frontmatter + markdown body)
├── LICENSE           (recommended — MIT)
├── examples/         (optional — usage examples)
├── scripts/          (optional — helper scripts)
├── references/       (optional — reference docs)
└── assets/           (optional — templates, images, fonts)
```

**SKILL.md frontmatter must include:**

```yaml
---
name: skill-name
description: Clear description of what the skill does and when to activate it
---
```

### Step 2: Push to GitHub

```bash
cd /path/to/skill-folder

# Init if needed
git init
git add -A
git commit -m "feat: initial release of skill-name"

# Create repo and push
gh repo create owner/repo-name --public --source=. --push
```

If the repo already exists:

```bash
git remote add origin https://github.com/owner/repo-name.git 2>/dev/null || true
git push -u origin main
```

### Step 3: Publish to ClawHub

```bash
# Login if needed (opens browser)
npx clawhub login

# Publish with version
npx clawhub publish /path/to/skill-folder \
  --version 1.0.0 \
  --slug skill-name \
  --name "Display Name" \
  --tags "tag1,tag2"

# Verify
npx clawhub inspect skill-name
```

**Note:** ClawHub runs a security scan after publishing. The skill becomes searchable once the scan passes (usually within a few minutes).

## Common Tasks

### Update an Existing Skill

```bash
# 1. Make changes to the skill folder

# 2. Push to GitHub
cd /path/to/skill-folder
git add -A && git commit -m "fix: description of changes"
git push

# 3. Publish new version to ClawHub
npx clawhub publish /path/to/skill-folder --version 1.1.0
```

### Fork an Existing Skill

```bash
npx clawhub publish /path/to/skill-folder \
  --version 1.0.0 \
  --slug my-fork-name \
  --fork-of original-skill@1.0.0
```

### Check Publish Status

```bash
npx clawhub inspect skill-name
npx clawhub search skill-name
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| `--version must be valid semver` | Add `--version x.y.z` flag |
| `Skill is hidden while security scan is pending` | Wait a few minutes, then retry `inspect` |
| `Not logged in` | Run `npx clawhub login` |
| `gh: not authenticated` | Run `gh auth login` |
| `fatal: remote origin already exists` | Safe to ignore, or use `git remote set-url` |

## Naming Conventions

- **Slug:** lowercase, hyphens only (e.g., `figma-plugin-writer`)
- **Repo:** match the slug (e.g., `openclaw-figma-plugin-writer`)
- **Version:** semver (e.g., `1.0.0`, `1.2.3`)
