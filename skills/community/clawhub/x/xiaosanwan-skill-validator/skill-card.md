## Description:

Skill Validator checks installed skills for functional completeness, edge cases, security concerns, UX quality, and improvement opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skill Validator to test newly installed OpenClaw skills, generate validation reports, and receive concrete recommendations before relying on those skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator can execute scripts from a target skill on the host.

Mitigation: Use it only with trusted skills, or run validation in a disposable sandbox with no secrets, no important files, and no network access.

Risk: Script execution paths can trigger unexpected behavior when validating unknown skills.

Mitigation: Prefer static checks or syntax-only validation for unknown skills, and gate any execution behind explicit sandboxed opt-in.

Risk: Long-running or resource-heavy target scripts may disrupt the host environment.

Mitigation: Apply timeouts and resource limits when executing any target skill script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongrebeccahhh-boop/skills/xiaosanwan-skill-validator)
- [Security Hardening Guidance](artifact/SECURITY.md)
- [Validation Report Template](artifact/templates/report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and Markdown-style validation reports with status counts, scores, findings, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include pass, warning, failure, and skipped counts; UX scores; remediation guidance; and suggested shell commands for configuration fixes.]

## Skill Version(s):

1.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
