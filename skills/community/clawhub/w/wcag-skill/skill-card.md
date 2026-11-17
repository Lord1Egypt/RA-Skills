## Description:

Build, audit, and repair web content against WCAG 2.2. Use when: (1) creating accessible HTML/CSS/JS, (2) remediating accessibility defects, (3) running reproducible automated audits, (4) preparing WCAG 2.2 AAA evidence and human-test records, or (5) running the optional AI-WCAG-Gauntlet benchmark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbolego](https://clawhub.ai/user/turbolego)

### License/Terms of Use:

MIT

## Use Case:

Developers and accessibility practitioners use the skill to build accessible web pages, audit and repair WCAG 2.2 issues, and document manual test evidence for AAA work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign, but confidence is medium because Skillspector marked coverage partial after some skill references could not be resolved.

Mitigation: Review unresolved references and inspect the included scripts before execution; treat the scan result as guidance rather than a safety guarantee.

Risk: The browser audit follows redirects and loads the target page and its subresources, so an audit can reach third-party services.

Mitigation: Audit only URLs you are authorized to test, and prefer loopback or staging hosts as the skill recommends.

Risk: Automated accessibility reports alone cannot establish WCAG conformance, particularly for AAA or interactive states.

Mitigation: Complete the documented manual tests and evidence records for the routes, states, and criteria in scope before making a conformance claim.

## Reference(s):

- [Project home](https://github.com/turbolego/wcag-skill)
- [Validator workflow](artifact/references/validator-workflow.md)
- [WCAG 2.2 AAA evidence matrix](artifact/references/aaa-evidence-matrix.md)
- [Manual test protocol](artifact/references/manual-test-protocol.md)
- [Dynamic state test protocol](artifact/references/dynamic-state-test-protocol.md)
- [Legacy markup repair guide](artifact/references/legacy-markup-repair.md)
- [W3C WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [AI-WCAG-Gauntlet legacy-repair task](https://github.com/turbolego/AI-WCAG-Gauntlet/blob/main/BENCHMARK.md#legacy-repair-task)

## Skill Output:

**Output Type(s):** [Code, Shell commands, JSON reports, Accessibility findings, WCAG evidence records, Remediation guidance]

**Output Format:** [HTML/CSS/JavaScript examples, Markdown guidance and evidence records, shell commands, and JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit scripts write reports to a chosen output directory; automated findings support review but do not establish WCAG conformance.]

## Skill Version(s):

2.0.32 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
