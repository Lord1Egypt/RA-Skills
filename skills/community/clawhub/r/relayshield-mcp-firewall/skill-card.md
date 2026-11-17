## Description:

Guide OpenClaw users in routing MCP tool calls and results through the RelayShield proxy for threat screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nzdsf2-gif](https://clawhub.ai/user/nzdsf2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and verify screening of OpenClaw MCP traffic through a local RelayShield proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing MCP calls and results through the proxy may expose sensitive data, credentials, or PII to external RelayShield code.

Mitigation: Review the RelayShield repository and documentation before running the proxy; assess what data and credentials the selected MCP servers handle.

Risk: Home-scope mcporter configuration persistently changes MCP routing.

Mitigation: Confirm the intended server and proxy endpoint before applying the configuration, and review or remove it when proxy routing is no longer needed.

Risk: The documented proxy allows calls to proceed when threat-intelligence screening times out.

Mitigation: Monitor screening and timeout logs, and do not rely on the proxy as the sole control for sensitive MCP operations.

## Reference(s):

- [RelayShield developer documentation](https://api.relayshield.net/developers)
- [RelayShield proxy repository referenced in the skill](https://github.com/nzdsf2-gif/relayshield)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup and screening verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
