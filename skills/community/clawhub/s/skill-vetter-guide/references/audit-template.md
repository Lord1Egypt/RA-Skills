# Audit Report Template

Use this format for periodic security audits of installed skills:

```markdown
# Skills Security Audit

Time: [YYYY-MM-DD HH:MM timezone]
Host: [hostname]
Scope: ~/.agents/skills/

## Summary
- Total skills reviewed: X
- ✅ Normal: X
- ⚠️ Needs attention: X
- ❌ Problematic: X

## Findings

### [skill-name]
- Source:
- Files reviewed:
- Red flags:
- Permissions:
- Risk:
- Verdict:
- Notes:

## Recommendations
- [ ] Remove suspicious skill(s)
- [ ] Re-review changed skill(s)
- [ ] Keep monitoring
```

Save audit files with timestamps: `security-audits/skills-audit-YYYY-MM-DD_HHMM.md`
