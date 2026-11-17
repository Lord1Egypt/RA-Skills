# ClawHub Best Practices & Advanced Examples

## Overview

This document compiles best practices from ClawHub official documentation and advanced skill examples from the OpenClaw community.

---

## ClawHub Statistics (as of Feb 2026)

- **Total Skills on Registry**: 13,729
- **Filtered Quality Skills**: ~5,400
- **Categories**: 25+

---

## Best Practices from Official Documentation

### 1. Folder Structure

```
workspace-architect/
├── SKILL.md              # Required - Main skill file
├── references/           # Optional - Support documentation
│   ├── arquivo-specs.md
│   ├── patterns.md
│   └── questionnaire.md
├── scripts/              # Optional - Helper scripts
│   └── validate.sh
└── sandbox/              # Working directory (not uploaded)
```

**Naming Tips:**
- Use lowercase and hyphenated folder names
- Keep names concrete so the trigger intent is obvious
- Example: `workspace-architect` not `WA` or `workspace_tool`

### 2. SKILL.md Structure

```markdown
---
name: skill-name
description: Clear, action-oriented description of what the skill does.
metadata:
  {
    "openclaw": {
      "emoji": "🏗️",
      "user-invocable": true
    }
  }
---

# Skill Name

## What it does
[One sentence purpose]

## Inputs needed
- Input 1
- Input 2

## Workflow
1. Step 1
2. Step 2
3. Step 3

## Guardrails
- Do not X
- Always Y

## References
See {baseDir}/references/ for details.
```

### 3. Quality Indicators

When evaluating skills (from ClawHub):

| Indicator | Good Threshold |
|-----------|----------------|
| Downloads | > 1,000 |
| Stars | > 20 |
| Recent Update | < 30 days |
| Description | Clear and specific |

### 4. Security Checklist

**Before Publishing:**
- [ ] No secrets or API keys in files
- [ ] No hardcoded URLs (use configurable endpoints)
- [ ] Clear input validation
- [ ] Guardrails for sensitive operations
- [ ] Error handling documented

**From Security Guide:**
- 341 malicious skills discovered in ClawHavoc incident
- Always review source code before installing
- Check VirusTotal report on ClawHub
- Wait for community validation on new skills

---

## Advanced Skill Patterns

### Pattern 1: References for Large Content

**Problem:** SKILL.md should be concise and load quickly — condense aggressively without losing clarity
**Solution:** Move detailed content to references/

```
SKILL.md (2KB) → Just workflow and guardrails
references/
  ├── detailed-specs.md (50KB) → Detailed specifications
  ├── examples.md (30KB) → Examples library
  └── troubleshooting.md (10KB) → Common issues
```

**How to Reference:**
```markdown
See {baseDir}/references/detailed-specs.md for complete specifications.
```

### Pattern 2: Deterministic Workflow

**Good:**
```markdown
## Workflow
1. **Collect** required inputs (ask if missing)
2. **Validate** inputs against schema
3. **Process** using defined algorithm
4. **Output** in specified format
5. **Confirm** results with user
```

**Bad:**
```markdown
## Workflow
Do things and try to help the user.
```

### Pattern 3: Input Validation Guardrails

```markdown
## Guardrails
- Never proceed without required inputs
- Validate file paths before operations
- Ask for confirmation before overwriting
- Use sandbox for all modifications
- Never modify original files directly
```

### Pattern 4: Error Handling

```markdown
## Error Handling
1. **Input Missing:** Ask user clearly for what's needed
2. **File Not Found:** Suggest alternatives or ask to create
3. **Permission Denied:** Explain limitation and suggest workaround
4. **Unexpected Error:** Log details, ask for user guidance
```

### Pattern 5: Multi-Mode Skills

Skills that can operate in different modes:

```markdown
## Modes
### CREATE Mode
Create new workspace files with guided questions.

### ANALYZE Mode
Analyze existing files for patterns and issues.

### OPTIMIZE Mode
Suggest improvements with comparison.

## Trigger Phrases
- "criar novo agente" → CREATE
- "analisar workspace" → ANALYZE  
- "otimizar arquivos" → OPTIMIZE
```

---

## Popular Skills Examples

From Reddit r/AI_Agents (top recommended):

| Skill | Purpose | Downloads |
|-------|---------|-----------|
| `github` | GitHub integration | 10k+ |
| `linear` | Project management | 2.5k+ |
| `playwright-mcp` | Browser automation | 5k+ |
| `obsidian-direct` | Knowledge base integration | 3k+ |
| `automation-workflows` | Workflow builder | 2k+ |

---

## Skill Categories (from awesome-openclaw-skills)

1. **Git & GitHub** (170 skills)
2. **Marketing & Sales** (104 skills)
3. **Communication** (149 skills)
4. **Coding Agents & IDEs** (1,222 skills)
5. **Productivity & Tasks** (206 skills)
6. **Browser & Automation** (335 skills)
7. **AI & LLMs** (196 skills)
8. **DevOps & Cloud** (408 skills)
9. **Data & Analytics** (28 skills)
10. **Search & Research** (350 skills)

---

## Testing Best Practices

### Test Matrix Template

| Scenario | Expected Result | Time | Pass/Fail |
|----------|-----------------|------|-----------|
| Happy path input | Summary generated | 30-60s | Pass |
| Missing required input | Clear error message | 10-20s | Pass |
| Permission denied | Explicit warning + fallback | 20-45s | Pass |
| Edge case | Graceful handling | Varies | Pass |

### Pre-flight Checklist

- [ ] Required file exists (SKILL.md)
- [ ] Frontmatter includes name and description
- [ ] Required sections present (What it does, Workflow)
- [ ] Guardrails defined
- [ ] Dry-run test passed
- [ ] Edge case tested

---

## Publishing to ClawHub

### Commands

```bash
# Install CLI
npm i -g clawhub

# Login
clawhub login

# Publish
clawhub publish ./workspace-architect \
  --slug workspace-architect \
  --name "Workspace Architect" \
  --version 1.0.0 \
  --tags latest

# Update
clawhub update workspace-architect
```

### Publishing Checklist

- [ ] Tested locally
- [ ] Documentation complete
- [ ] No secrets in files
- [ ] Clear description
- [ ] Proper versioning
- [ ] Changelog provided

---

## Versioning Strategy

Use semver (semantic versioning):

- **Major (X.0.0)**: Breaking changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, backward compatible

---

## Common Mistakes to Avoid

| Mistake | Impact | Fix |
|---------|--------|-----|
| Generic name/description | Skill never triggers | Use specific, action-oriented wording |
| Missing guardrails | Unsafe operations | Add explicit constraints |
| No input validation | Errors mid-workflow | Validate upfront |
| Large SKILL.md | Slow loading | Move details to references/; condense, don't delete |
| No test cases | Unreliable behavior | Document test scenarios |

---

## Security Considerations

From ClawHavoc incident analysis:

1. **Review source code** before installing
2. **Check VirusTotal report** on ClawHub
3. **Sandbox testing** before production
4. **Regular updates** for security patches
5. **Report suspicious skills** through official channels

---

## References

- [ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [OpenClaw Hub Best Practices](https://openclaw-hub.org/openclaw-hub-best-practices.html)