## Description:

A multi-language static web application security audit skill that scans PHP, Java, Python, and Go codebases with 60+ regex-based vulnerability rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to run a local static scan against authorized web application codebases and generate Security.md findings with remediation guidance and PoC material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can include ready-to-run exploit scripts that could be used against systems.

Mitigation: Keep generated reports private and run PoCs only on systems the user owns or is explicitly authorized to test.

Risk: Some generated payloads may probe metadata services, out-of-band callbacks, sensitive file reads, or webshell upload behavior.

Mitigation: Review, remove, or gate those payloads before deployment or distribution.

Risk: The security verdict is suspicious because the skill combines legitimate static scanning with executable exploit material.

Mitigation: Install only when this behavior is deliberate and review the skill before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/web-security-audit-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown Security.md report with optional JSON summary and Python PoC code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reports from local source scans; PoC material should be handled as sensitive and used only with authorization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
