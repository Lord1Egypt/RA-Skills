## Description:

Manage Smartlead campaigns, leads, and webhooks from the command line via the smartlead CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzakirov](https://clawhub.ai/user/jzakirov)

### License/Terms of Use:


## Use Case:

External users, developers, and operations teams use this skill to manage Smartlead campaigns, leads, webhooks, and reply-alert workflows through the smartlead CLI and OpenClaw handoff guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can enable a persistent OpenClaw plugin from an unaudited hardcoded local path.

Mitigation: Review the OpenClaw plugin separately, prefer pinned and reviewed CLI/plugin versions, and avoid linked development-mode installs in production.

Risk: Smartlead reply data may be routed through OpenClaw into Slack or other delivery channels.

Mitigation: Confirm the workspace permits this data flow, configure webhook secrets and hook tokens, and limit delivery channels to approved destinations.

Risk: Webhook-driven agent behavior can act on incoming lead replies without an interactive operator in the loop.

Mitigation: Review hook mappings and transforms before enabling wakeMode behavior, and test with representative Smartlead EMAIL_REPLY events before production use.

## Reference(s):

- [Smartlead ClawHub Skill Listing](https://clawhub.ai/jzakirov/skills/smartlead)
- [Smartlead API Base URL](https://server.smartlead.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the smartlead CLI and SMARTLEAD_API_KEY; setup guidance can emit OpenClaw hook and plugin configuration snippets.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
