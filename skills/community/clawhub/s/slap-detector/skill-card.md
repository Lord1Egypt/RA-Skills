## Description:

React to physical slaps and shakes detected on an Apple Silicon MacBook accelerometer. Use when the slap-your-openclaw MCP server is connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinhong2011](https://clawhub.ai/user/sinhong2011)

### License/Terms of Use:


## Use Case:

Developers and users running an Apple Silicon MacBook use this skill to monitor physical slap or shake events through a connected MCP server, review recent detector events, and tune detector sensitivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an external MCP server with sudo root privileges.

Mitigation: Install only after reviewing and trusting the `slap-your-openclaw` binary; prefer an unprivileged version or narrowly scoped hardware access.

Risk: Event waits and sensitivity changes can produce long blocking calls or noisy low-severity detections.

Mitigation: Use bounded timeouts, keep the default minimum severity at level 4, and avoid lowering sensitivity below level 3 unless the user explicitly asks.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May wait for slap or shake events with bounded timeouts; uses detector severity levels and sensitivity settings.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
