## Description:

Diagnose and fix WhatsApp connectivity issues for OpenClaw agents. Use when: a PA is not responding, WhatsApp shows connected but messages don't arrive, the agent is online but not replying, or troubleshooting a new agent setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose WhatsApp channel connectivity, message ingest, and agent runtime response issues for OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health-check script can use live AI-provider API keys and contact external provider endpoints.

Mitigation: Review or edit the script before running it, make credential checks explicit, and prefer test or scoped keys.

Risk: The diagnostic workflow may run gateway commands while troubleshooting WhatsApp connectivity.

Mitigation: Run gateway checks in an appropriate maintenance context and confirm operational impact before restart commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/netanel-abergel/skills/whatsapp-diagnostics)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a diagnostic decision tree, CLI checks, curl-based provider checks, escalation guidance, and prevention notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
