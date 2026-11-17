## Description:

Trace network path to a destination host. Use for network diagnostics, latency analysis, and routing path discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to run traceroute-style diagnostics for a destination host and inspect hop latency, routing path, and potential network bottlenecks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the local traceroute command and sends diagnostic packets to requested hosts.

Mitigation: Use it only for hosts you are authorized to diagnose and in environments where traceroute traffic is acceptable.

Risk: Hostnames are user-controlled input, and the current wrapper forwards only the first positional argument to traceroute.

Mitigation: Validate or constrain destination hosts before use, and verify expected options manually until the wrapper supports documented flags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/traceroute-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text traceroute output with concise diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs the local traceroute command for a user-provided host.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
