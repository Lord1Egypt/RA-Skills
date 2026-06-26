---
name: skill-creator-plus
description: "Enhanced skill creator with templates, validation, publishing workflow, and quality gates. Guides through skill creation process with best practices, common patterns, and ClawHub integration."
metadata:
  author: opencode
  version: 2.0
  tags: skill-creation, templates, validation, publishing
  compatibility: opencode
  license: MIT
---

# Skill Creator Plus

Enhanced skill creator with templates, validation, publishing workflow, and quality gates.

## Features

- **Skill Templates**: Ready-to-use templates for common skill types
- **Validation Rules**: Quality gates before publishing
- **Publishing Workflow**: ClawHub integration
- **Best Practices**: Proven patterns and anti-patterns
- **Testing Framework**: Validate skills before release

## Quick Reference

| Step | Action | Command |
|------|--------|---------|
| 1 | Plan skill | Define purpose, audience, triggers |
| 2 | Create structure | Use templates |
| 3 | Write SKILL.md | Follow guidelines |
| 4 | Add resources | Scripts, references, assets |
| 5 | Validate | Run validation |
| 6 | Test | Real-world testing |
| 7 | Publish | ClawHub publish |

## Skill Anatomy

### Directory Structure

```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
│   └── helper.py
├── references/ (optional)
│   └── guide.md
└── assets/ (optional)
    └── template.txt
```

### SKILL.md Structure

```yaml
---
name: skill-name
description: "Clear description of what the skill does and when to use it."
metadata:
  author: your-name
  version: 1.0.0
  tags: tag1, tag2
  compatibility: opencode
  license: MIT
---

# Skill Name

## Overview
Brief overview of the skill.

## Features
- Feature 1
- Feature 2

## Usage
How to use the skill.

## Examples
Concrete examples.
```

## Skill Templates

### Knowledge Skill

```yaml
---
name: knowledge-skill
description: "Domain knowledge for [topic]. Use when user asks about [specific topics]."
metadata:
  author: your-name
  version: 1.0.0
  tags: knowledge, domain
  compatibility: opencode
  license: MIT
---

# [Topic] Knowledge

## Overview
Brief overview of the domain.

## Key Concepts
- Concept 1: Definition
- Concept 2: Definition

## Common Patterns
1. Pattern 1: Description
2. Pattern 2: Description

## References
- [link1](url1)
- [link2](url2)
```

### Workflow Skill

```yaml
---
name: workflow-skill
description: "Automated workflow for [task]. Use when user wants to [action]."
metadata:
  author: your-name
  version: 1.0.0
  tags: workflow, automation
  compatibility: opencode
  license: MIT
---

# [Task] Workflow

## Overview
Brief overview of the workflow.

## Steps
1. Step 1: Description
2. Step 2: Description
3. Step 3: Description

## Commands
```bash
command1
command2
```

## Error Handling
- Error 1: Solution
- Error 2: Solution
```

### Tool Integration Skill

```yaml
---
name: tool-skill
description: "Integration with [tool/API]. Use when working with [tool]."
metadata:
  author: your-name
  version: 1.0.0
  tags: tool, integration
  compatibility: opencode
  license: MIT
---

# [Tool] Integration

## Overview
Brief overview of the tool.

## Setup
1. Install: `command`
2. Configure: `command`
3. Verify: `command`

## Usage
```bash
tool-command
```

## API Reference
- Method 1: Description
- Method 2: Description

## Examples
```bash
# Example 1
command

# Example 2
command
```
```

## Validation Rules

### Required Fields

- [ ] `name`: Skill name (lowercase, hyphens)
- [ ] `description`: Clear, comprehensive description

### Description Quality

- [ ] What the skill does
- [ ] When to use it (triggers)
- [ ] Specific use cases
- [ ] No vague language

### Structure Quality

- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure
- [ ] No extraneous files
- [ ] Clear organization

### Content Quality

- [ ] Imperative/infinitive form
- [ ] Concise examples
- [ ] No duplication
- [ ] Actionable instructions

## Publishing Workflow

### 1. Prepare

```bash
# Validate skill
clawhub validate skill-name

# Test locally
# Use skill in real scenarios
```

### 2. Publish

```bash
# Publish to ClawHub
clawhub publish skill-name --version "1.0.0"

# With options
clawhub publish skill-name \
  --name "Skill Display Name" \
  --slug "skill-slug" \
  --version "1.0.0" \
  --tags "tag1,tag2"
```

### 3. Verify

```bash
# Check publication
clawhub search skill-name

# Sync to local
clawhub sync
```

## Quality Gates

### Pre-Publish Checklist

- [ ] SKILL.md follows template
- [ ] Description is comprehensive
- [ ] No extraneous files
- [ ] Examples are clear
- [ ] Scripts are tested
- [ ] References are accurate
- [ ] License is specified

### Post-Publish Verification

- [ ] Skill appears in ClawHub search
- [ ] Installation works
- [ ] Skill triggers correctly
- [ ] Instructions are clear
- [ ] Examples work

## Common Patterns

### Pattern 1: Progressive Disclosure

```markdown
# Skill Name

## Quick Start
Basic usage example.

## Advanced Features
- Feature 1: See [FEATURE1.md](FEATURE1.md)
- Feature 2: See [FEATURE2.md](FEATURE2.md)
```

### Pattern 2: Domain Organization

```
skill-name/
├── SKILL.md
└── references/
    ├── domain1.md
    ├── domain2.md
    └── domain3.md
```

### Pattern 3: Conditional Loading

```markdown
# Skill Name

## Basic Usage
Simple example.

## Advanced Usage
For complex scenarios, see [ADVANCED.md](ADVANCED.md).
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Too verbose | Context bloat | Keep under 500 lines |
| No examples | Unclear expectations | Add concrete examples |
| Extraneous files | Clutter | Remove unnecessary files |
| Vague description | Poor triggering | Be specific |
| No progressive disclosure | Loading overhead | Split into references |

## Testing Framework

### Test Cases

1. **Trigger Test**: Does the skill activate correctly?
2. **Instruction Test**: Are instructions clear?
3. **Example Test**: Do examples work?
4. **Error Test**: Are errors handled?

### Test Script

```bash
#!/bin/bash
# test-skill.sh

SKILL_NAME=$1

echo "Testing skill: $SKILL_NAME"

# Validate structure
clawhub validate $SKILL_NAME

# Test installation
clawhub install $SKILL_NAME

# Verify installation
ls -la ~/.openclaw/workspace/skills/$SKILL_NAME

echo "Test complete"
```

## Best Practices

1. **Start simple** - Begin with basic skill, iterate
2. **Be specific** - Clear triggers and instructions
3. **Add examples** - Concrete use cases
4. **Test thoroughly** - Real-world testing
5. **Document well** - Clear SKILL.md
6. **Publish regularly** - Share improvements
7. **Gather feedback** - Iterate based on usage

## ClawHub Integration

### Search Skills

```bash
clawhub search "query"
```

### Install Skills

```bash
clawhub install skill-name
```

### Publish Skills

```bash
clawhub publish skill-name
```

### Sync Skills

```bash
clawhub sync
```
