## Description:

Send and manage emails via the Resend CLI, including domains, contacts, segments, broadcasts, templates, topics, webhooks, and API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maciejlis](https://clawhub.ai/user/maciejlis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Resend CLI workflows for sending email, managing sender domains, maintaining audiences, handling templates and broadcasts, configuring webhooks, and administering API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to send or forward email from a Resend account.

Mitigation: Review recipients and message content before sends or forwards, and use JSON or quiet output for non-interactive runs.

Risk: A broad API key could allow account-management actions beyond routine sending.

Mitigation: Prefer a domain-scoped sending_access key for automation and avoid full-access keys unless the workflow requires them.

Risk: Delete commands using --yes can remove email resources or access immediately.

Mitigation: Treat every --yes delete as deliberate, review the target identifier, and confirm the operational impact before execution.

## Reference(s):

- [Resend CLI Repository](https://github.com/resend/resend-cli)
- [Resend](https://resend.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts agents to use JSON or quiet CLI output for non-interactive execution.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
