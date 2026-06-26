## Description: <br>
Convert Unix timestamps to dates and back. Use when parsing epoch values, calculating time differences, debugging logs, or generating relative dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Unixtime to convert epoch timestamps, date strings, countdowns, and time ranges while parsing logs or debugging time-sensitive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local unixtime command could be miswired to a different script or executable. <br>
Mitigation: Confirm the unixtime command resolves to the included artifact script before relying on it. <br>
Risk: Date parsing and displayed local times can vary by host timezone and platform date utility behavior. <br>
Mitigation: Use explicit timestamps or timezone-aware date strings when outputs are used for audits, releases, or operational decisions. <br>


## Reference(s): <br>
- [Unixtime ClawHub page](https://clawhub.ai/bytesagain3/unixtime) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local timestamp conversions, duration breakdowns, countdowns, and current time details.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
