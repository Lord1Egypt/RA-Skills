# Agent Skills Spec Summary

**Source:** agentskills.io/specification
**Retrieved:** 2026-03-25

## SKILL.md Format

Required: YAML frontmatter + Markdown body.

### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| name | Yes | Max 64 chars, lowercase + hyphens only |
| description | Yes | Max 1024 chars. What it does AND when to use it. |
| license | No | License name or reference |
| compatibility | No | Max 500 chars. Environment requirements. |
| metadata | No | Arbitrary key-value map |
| allowed-tools | No | Space-delimited pre-approved tools |

### Body Content

No format restrictions. Recommended sections:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

**Keep under 500 lines.** Move detailed content to referenced files.

### Progressive Disclosure

1. **Metadata** (~100 tokens): name + description loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): full SKILL.md body on activation
3. **Resources** (as needed): files in scripts/, references/, assets/ loaded on demand

### Directory Structure

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...
```

### File References

Use relative paths from skill root:
```markdown
See [the reference guide](references/REFERENCE.md) for details.
```

Keep references one level deep. Avoid nested chains.

## Key Takeaway

"Process goes in SKILL.md, context goes in reference files."
SKILL.md body < 5000 tokens. References loaded on demand.
