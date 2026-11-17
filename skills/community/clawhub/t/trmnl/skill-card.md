## Description:

Generates TRMNL e-ink display content with TRMNL CSS framework layouts and sends it through the trmnl CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peetzweg](https://clawhub.ai/user/peetzweg)

### License/Terms of Use:


## Use Case:

Developers and TRMNL users use this skill to generate e-ink optimized HTML dashboards, messages, notifications, and status displays, then send them to configured TRMNL display plugins through the trmnl CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update a mutable global trmnl CLI package.

Mitigation: Pin the CLI version or install it locally, and avoid elevated installation with sudo.

Risk: Generated content may be sent to a configured TRMNL webhook target.

Mitigation: Verify the plugin URL and require explicit confirmation of the target and content before each send.

Risk: Private, personal, or confidential content could be displayed or transmitted to TRMNL.

Mitigation: Avoid sending secrets, personal data, or confidential summaries unless the user explicitly intends that content to be sent.

## Reference(s):

- [TRMNL Design Patterns](references/patterns.md)
- [TRMNL Framework Overview](references/framework-overview.md)
- [CSS Utilities Reference](references/css-utilities.md)
- [Layout Systems Reference](references/layout-systems.md)
- [Components Reference](references/components.md)
- [Webhook API Reference](references/webhook-api.md)
- [Anti-Patterns to Avoid](assets/anti-patterns.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary HTML content for validation and sending through a configured TRMNL plugin.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
