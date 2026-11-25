## Description:

Guides developers in building, auditing, and repairing web content against WCAG 2.2, including accessibility checks and evidence workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbolego](https://clawhub.ai/user/turbolego)

### License/Terms of Use:

MIT

## Use Case:

Developers and accessibility practitioners use this skill to create accessible HTML, CSS, and JavaScript, fix accessibility defects, run automated and manual checks, and record evidence against WCAG 2.2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser audits follow redirects and load the target page's subresources, which can contact third-party services.

Mitigation: Audit only URLs you are authorized to test and prefer loopback or staging hosts.

Risk: In CI, the audit wrapper disables Chrome's sandbox when CI=true and AXE_CHROME_EXTRA_ARGS is unset.

Mitigation: Keep the sandbox enabled outside isolated CI; set AXE_CHROME_EXTRA_ARGS to an empty value when CI should retain it.

Risk: Automated accessibility results alone do not establish WCAG conformance, and the security review was partial with medium confidence.

Mitigation: Review unresolved findings, use manual checks and criterion-level evidence for AAA work, and assess dependencies and Chrome settings in the intended environment.

## Reference(s):

- [Validator workflow](references/validator-workflow.md)
- [AAA evidence matrix](references/aaa-evidence-matrix.md)
- [Manual test protocol](references/manual-test-protocol.md)
- [Dynamic state test protocol](references/dynamic-state-test-protocol.md)
- [Legacy markup repair](references/legacy-markup-repair.md)
- [Skill homepage](https://github.com/turbolego/wcag-skill)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, HTML/CSS/JavaScript examples, shell commands, and JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the requested page and checks; may include audit reports and manual evidence records.]

## Skill Version(s):

2.0.36 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
