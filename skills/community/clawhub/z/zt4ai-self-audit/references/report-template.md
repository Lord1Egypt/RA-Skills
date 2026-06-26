# ZT4AI Audit Report Template

Use this template when generating audit reports. Save completed reports to `memory/zt4ai-audit-YYYY-MM-DD.md`.

---

```markdown
# ZT4AI Skill Audit — [DATE]

## Environment
- **Agent:** [name]
- **Platform:** [OpenClaw version, OS, container type]
- **Skill locations scanned:** [system, user, workspace]
- **Total skills audited:** [N]

## Framework
Audited against:
1. Microsoft ZT4AI (Verify explicitly, Least privilege, Assume breach)
2. "Caging the Agents" four-layer defense (arXiv:2603.17419)
3. OWASP Agentic AI Top 10

## Summary

| Risk Level | Count | Skills |
|-----------|-------|--------|
| 🔴 CRITICAL | N | [list] |
| 🟠 WARNING | N | [list] |
| 🟡 ADVISORY | N | [list] |
| 🟢 PASS | N | [list] |

## Findings

### [Finding ID]: [Title]
- **Skill:** [name]
- **Severity:** [🔴/🟠/🟡/🟢]
- **Category:** [Behavioral/Credential/System/Network/Integrity]
- **ZT4AI Principle Violated:** [Verify explicitly / Least privilege / Assume breach]
- **Defense Layer Gap:** [L1 Isolation / L2 Credentials / L3 Network / L4 Prompt Integrity]
- **Description:** [What the issue is]
- **Impact:** [What could happen if exploited]
- **Evidence:** [Specific file, line, or pattern]
- **Recommendation:** [What to do]
- **Action Tier:** [Tier 1-4 for remediation]

### [Repeat for each finding]

## Structural Gaps

[Document any cross-cutting issues that affect multiple skills or the agent architecture itself]

## Integrity Baseline

- **Baseline created:** [yes/no, path]
- **Files checksummed:** [N]
- **Drift detected:** [yes/no, details]

## Recommendations (prioritized)

1. [Highest priority action]
2. [Next priority]
3. ...

## Next Audit
- **Recommended date:** [date]
- **Trigger conditions:** [any skill install/update, after security incident, monthly]
```

---

## Notes for Report Authors

- Be specific about evidence — cite file paths and line numbers
- Don't just list risks — explain the realistic attack scenario
- Recommendations should be actionable, not aspirational
- Rate severity based on realistic exploitability, not theoretical maximum
- Include what's working well, not just what's broken
