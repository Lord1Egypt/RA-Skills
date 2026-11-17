## Description:

Audits OpenClaw skills for malicious code, prompt injection, dangerous APIs, insecure practices, and related ClawHavoc-style attacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this Portuguese-language skill to review third-party OpenClaw skills before installation and to generate risk-ranked audit reports with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the package does not include scanner code, so referenced audit commands may not work unless the surrounding platform supplies them.

Mitigation: Confirm the platform provides the audit command and treat generated findings as guidance rather than a complete automated scan.

Risk: The skill is used to evaluate third-party skills, but guidance-only output can miss issues that a platform scanner or manual review would catch.

Mitigation: Review and scan target skills with platform controls or an additional security tool before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engsathiago/skills/seguranca-auditoria)
- [Publisher profile](https://clawhub.ai/user/engsathiago)
- [Artifact-declared project homepage](https://github.com/eve-agent/seguranca-auditoria)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or HTML report with risk-ranked findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese-language output; release evidence reports no bundled executable scanner code.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
