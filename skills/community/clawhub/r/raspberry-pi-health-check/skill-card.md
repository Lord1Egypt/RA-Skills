## Description:

Use JishuBuddy for read-only Raspberry Pi checks: CPU, memory, disk, temperature, throttling, and failed services, with actual device evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-aijishu](https://clawhub.ai/user/bowen-aijishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to collect read-only Raspberry Pi health evidence over SSH and turn CPU, memory, disk, temperature, throttling, process, and service data into a concise assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can install JishuBuddy globally on the operator machine.

Mitigation: Run the preflight first, show the npm version, registry, global prefix, and exact install command, and install only after explicit approval for that version.

Risk: Health checks depend on trusted SSH access and may expose device details or log excerpts.

Mitigation: Use only trusted SSH targets, verify host keys through a trusted channel, and report bounded, sanitized evidence.

Risk: JishuBuddy sends low-frequency activation and heartbeat telemetry by default.

Mitigation: Set JISHUBUDDY_TELEMETRY_DISABLED=true before launch when telemetry should be disabled.

Risk: Missing tools, permissions, or failed commands could be mistaken for a healthy result.

Mitigation: Mark unavailable checks as blocked or incomplete and base findings only on actual device output.

## Reference(s):

- [Skill homepage](https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-health-check)
- [JishuBuddy npm package](https://www.npmjs.com/package/jishubuddy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and evidence-based health findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports each check as confirmed, unconfirmed, or blocked; missing tools or permissions leave checks incomplete rather than healthy.]

## Skill Version(s):

1.0.1 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
