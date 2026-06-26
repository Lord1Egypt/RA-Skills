## Description: <br>
How to check weather forecasts using wttr.in service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbbyqsyea](https://clawhub.ai/user/fbbyqsyea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query wttr.in weather forecasts, moon phases, and location-specific weather data in terminal, JSON, PNG, and status-line formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to wttr.in and may reveal searched locations or IP-derived location context. <br>
Mitigation: Prefer explicit public city or landmark names and avoid querying internal hostnames, private IP addresses, or sensitive locations. <br>
Risk: PNG weather image downloads can write to a user-specified output path. <br>
Mitigation: Use explicit safe output paths and review file destinations before writing downloaded weather images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fbbyqsyea/wttr-weather) <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [wttr.in service source repository](https://github.com/chubin/wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional JSON or PNG weather outputs from wttr.in.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call wttr.in over the network and may write PNG output when the user requests an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
