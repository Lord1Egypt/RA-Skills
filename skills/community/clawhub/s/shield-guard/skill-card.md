## Description:

OpenClaw security scanning and protection skill that checks port exposure, authentication configuration, plugin safety, credential management, and 2026 MIIT warning risk points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review OpenClaw deployments for exposed gateway ports, weak authentication, untrusted skills or plugins, credential placement, and messaging channel policy issues. It can produce a local Markdown security report and propose high-priority configuration fixes for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects OpenClaw configuration, local skill directories, and credential placement as part of its audit workflow.

Mitigation: Run it only when you explicitly want an OpenClaw security review and review the generated report before acting on recommendations.

Risk: The skill may propose gateway configuration changes, including changes intended to address weak console authentication.

Mitigation: Approve configuration patches only after reviewing the exact patch and confirming it matches the intended deployment policy.

Risk: The workflow writes a local Markdown security report that may contain deployment details or risk findings.

Mitigation: Store and share the report according to the organization's handling rules for security review artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/shield-guard)
- [Publisher profile](https://clawhub.ai/user/clawhub-master)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with command snippets and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local security report and may propose gateway configuration changes that require user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
