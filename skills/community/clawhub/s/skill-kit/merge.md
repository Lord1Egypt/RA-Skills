# Skill Merge

Combine multiple related skills into a single unified skill.

## When to Use

- Multiple skills on the same topic are scattered
- Want to consolidate skill directories
- Example: `argocd-helm-cleanup` + `argocd-oci-helm` → `argocd-helm`

## Workflow

### Step 1: Select Skills to Merge

Use AskUserQuestion to confirm:

```
Select skills to merge:
- argocd-helm-cleanup
- argocd-oci-helm
```

Or use skills specified by user directly.

### Step 2: Analyze Skills

Read each SKILL.md and analyze:
- frontmatter (name, description)
- body content
- common theme extraction
- **language check** (Korean/English)

#### Language Mismatch Handling

If skills have different languages, use AskUserQuestion:

```
Skills have different languages:
- skill-a: Korean
- skill-b: English

Select unified language:
1. Korean (Recommended) - Translate all to Korean
2. English - Translate all to English
3. Keep original - SKILL.md in Korean, topic files keep original
```

Based on selection:
- **Korean/English**: Translate to unify
- **Keep original**: SKILL.md in Korean, topic files retain original language

### Step 3: Determine New Skill Name

Extract common prefix for new name:

| Original Skills | New Name |
|-----------------|----------|
| `argocd-helm-cleanup`, `argocd-oci-helm` | `argocd-helm` |
| `k8s-deploy`, `k8s-debug` | `k8s` |

Confirm with user via AskUserQuestion.

### Step 4: Create New Structure

Follow the [Multi-Topic Skill Architecture](./architecture.md) to create:

```
~/.claude/skills/{new-name}/
├── SKILL.md          # Unified frontmatter + topic references
├── {topic1}.md       # First skill content (no frontmatter)
└── {topic2}.md       # Second skill content (no frontmatter)
```

**Key points:**
- Extract body from original SKILL.md (remove frontmatter) for topic files
- Use unified description format in SKILL.md
- Include Topics table for discoverability

See [architecture.md](./architecture.md) for templates and detailed structure.

### Step 5: Backup Original Skills

```bash
# Move to .bak folder (backup instead of delete)
mkdir -p ~/.claude/.bak
mv ~/.claude/skills/{old-skill1} ~/.claude/.bak/
mv ~/.claude/skills/{old-skill2} ~/.claude/.bak/
```

If same name exists, add timestamp:
```bash
mv ~/.claude/skills/{old-skill} ~/.claude/.bak/{old-skill}_$(date +%Y%m%d_%H%M%S)
```

### Step 6: Validate

1. Verify new skill directory structure
2. Check SKILL.md frontmatter validity
3. Confirm topic file reference links work
4. Guide trigger testing

## Example

### Input

```
Merge: argocd-helm-cleanup, argocd-oci-helm
```

### Output Structure

```
~/.claude/skills/argocd-helm/
├── SKILL.md
├── cleanup.md
└── oci.md
```

### SKILL.md Example

```yaml
---
name: argocd-helm
description: ArgoCD Helm chart management. cleanup - clean Helm metadata, oci - add OCI registry charts. "argocd helm", "helm metadata", "OCI helm", "managed-by Helm" triggers
---

# ArgoCD Helm

Guide for managing Helm charts with ArgoCD.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| cleanup | Clean metadata when migrating HelmChart→ArgoCD | [cleanup.md](./cleanup.md) |
| oci | Add Helm charts from OCI registries | [oci.md](./oci.md) |
```

## Notes

- Backed up skills remain in `.bak/` for manual cleanup
- Same pattern applies for 3+ skills
- Restart Claude Code after merging
- Clean `.bak/`: `rm -rf ~/.claude/.bak/{skill-name}`
