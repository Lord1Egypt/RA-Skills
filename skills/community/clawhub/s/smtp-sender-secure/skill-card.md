## Description:

Guides agents and users through an MGC Blackbox workflow for storing SMTP credentials and email scripts locally, then invoking email sends with mgc_run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure SMTP email sending through MGC Blackbox while keeping SMTP credentials outside the agent context. It is intended for workflows where a user explicitly approves script storage, overwrite, and each email send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local reusable email script can access stored SMTP credentials and send email.

Mitigation: Install only after reviewing the script and require explicit confirmation before every script save, overwrite, and email send.

Risk: Inline email subjects or bodies may be visible to the agent or logs.

Mitigation: Use the documented stored-content mode for sensitive email content, or pass inline content only when that exposure is acceptable.

Risk: The workflow depends on trusting MGC Blackbox and its local service.

Mitigation: Use a pinned, reviewed MGC Blackbox version and keep credentials stored through the WebUI rather than sharing secret values with the agent.

Risk: The artifact privacy language may overstate boundaries if users pass sensitive content inline or skip review.

Mitigation: Present privacy as configuration-dependent and preserve the requirement for user approval and review before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zkeviny/skills/smtp-sender-secure)
- [MGC Blackbox Main Repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox Issues](https://github.com/zkeviny/MGC-Blackbox/issues)
- [Artifact README](artifact/readme.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown documentation with Python examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MGC Blackbox 1.4.10 or later and user-managed local credential storage.]

## Skill Version(s):

2.1.1 (source: server release evidence, target metadata, artifact frontmatter, and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
