# Batch Audit Prompt

Audit multiple rule files for usefulness to AI agents, validity, accuracy, and format.

## Instructions

1. List all files in the target directory
2. For each file, assess usefulness + format
3. Categorize into KEEP / IMPROVE / REMOVE
4. Produce summary report with recommendations

## Usefulness Check (per file)

| Criteria | ❌ Remove | ⚠️ Improve | ✅ Keep |
|----------|-----------|------------|---------|
| Would AI make this mistake? | AI knows this | Sometimes | Common AI mistake |
| Is this AI-discoverable? | In Angular docs | Scattered | Tribal knowledge |
| Is guidance specific? | Too vague | Missing thresholds | Clear criteria |
| Prevents real bugs? | Style only | Minor | Bugs/leaks/perf |

## Format Check (per file)

- [ ] Under 50 lines
- [ ] 1-2 code blocks
- [ ] Single sentence description
- [ ] Clear decision criteria

## Output Format

```markdown
## Batch Audit Report: {directory}

### Statistics
| Metric | Value |
|--------|-------|
| Total Rules | X |
| Avg Lines/Rule | X.X |
| Code Blocks | X |

### Usefulness Summary

| Category | Keep | Improve | Remove |
|----------|------|---------|--------|
| Signals (X) | X | X | X |
| TypeScript (X) | X | X | X |
| ... | ... | ... | ... |

### Rules to REMOVE (AI already knows)
| Rule | Reason |
|------|--------|
| `rule.md` | [Why AI doesn't need this] |

### Rules to IMPROVE (too vague)
| Rule | Issue | Fix |
|------|-------|-----|
| `rule.md` | [Problem] | [Specific fix] |

### High-Value Rules (4/4 usefulness)
- rule1.md
- rule2.md

### Priority Actions
1. Remove rules AI already knows
2. Add thresholds to vague rules
3. Fix deprecated code examples
```

## Processing

For large audits:
- Group by subdirectory
- Assess usefulness first, then format
- Focus on REMOVE candidates
