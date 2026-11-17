## Description:

Safe Skill Advisor helps ClawHub users evaluate third-party skill risk with warnings, scanner recommendations, and a 30-second self-check checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystaria](https://clawhub.ai/user/crystaria)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub users and agent operators use this skill before installing or troubleshooting skills to identify common risk patterns, choose scanning tools, and follow quick safety checks or reporting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses mandatory assistant directives that may overreach into broad skill-installation conversations.

Mitigation: Review behavior before enabling and scope use to skill-security advice where proactive warnings are appropriate.

Risk: The skill recommends installing a third-party scanner without pinning or verification.

Mitigation: Install only pinned, verified scanner versions in an isolated environment before using them on local skills.

## Reference(s):

- [Safe Skill Advisor on ClawHub](https://clawhub.ai/skills/safe-skill-advisor)
- [Safe Skill Advisor release page](https://clawhub.ai/crystaria/skills/safe-skill-advisor)
- [Cisco AI Skill Scanner](https://github.com/cisco-ai-skill-scanner)
- [SecureClaw](https://github.com/adversa-ai/secureclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides safety checklists, tool recommendations, reporting guidance, and remediation steps; no embedded executable payload is present in the release evidence.]

## Skill Version(s):

1.7.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
