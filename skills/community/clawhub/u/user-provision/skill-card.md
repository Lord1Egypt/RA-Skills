## Description:

Provisions single or batch Office 365 (21Vianet) and Adobe Creative Cloud user accounts, including license assignment, password reset, and notification email workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and service-desk agents use this skill to collect account details, configure required credentials, and run account creation and inspection workflows for Office 365 (21Vianet) and Adobe Creative Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external repository code and Python dependencies that are not pinned in the release evidence.

Mitigation: Pin the repository to a reviewed commit, pin dependency versions, and run installation and execution in an isolated administrator environment.

Risk: Provisioning uses powerful Office 365 and Adobe administrative credentials and can create users or assign licenses.

Mitigation: Use least-privileged approved credentials and require explicit confirmation of provider, target user, products, and side effects before creation.

Risk: Initial passwords can be exposed through chat output, logs, or ordinary email.

Mitigation: Use per-user one-time credentials or an approved activation flow, force password change on first login, and keep passwords out of chat transcripts and logs.

Risk: Existing accounts or license quotas can cause destructive or incorrect provisioning outcomes.

Mitigation: Inspect accounts before creation, ask for confirmation before reset or skip decisions, and verify seat or license availability before assigning products.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eggyrooch-blip/skills/user-provision)
- [office365-tools project repository](https://github.com/eggyrooch-blip/office365-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment configuration, and account provisioning summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account identifiers, assigned products, invitation status, verification results, and redacted error summaries.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
