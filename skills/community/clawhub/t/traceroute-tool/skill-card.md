## Description: <br>
Trace network path to a destination host. Use for network diagnostics, latency analysis, and routing path discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network operators use this skill to run traceroute for network diagnostics, latency analysis, and routing path discovery against a destination host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes local traceroute against a provided host, which can generate outbound diagnostic probes and expose network path information. <br>
Mitigation: Run it only for authorized destinations and environments where traceroute traffic is permitted. <br>
Risk: The wrapper artifact forwards a single destination host to traceroute, while the skill text documents additional traceroute options. <br>
Mitigation: Confirm behavior in the target agent environment before relying on documented options such as max hops, wait time, or query count. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/traceroute-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Plain text terminal output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wrapper execution depends on a local traceroute binary and a destination host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
