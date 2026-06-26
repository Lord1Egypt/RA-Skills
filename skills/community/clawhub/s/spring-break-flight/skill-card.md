## Description: <br>
Helps agents search and present spring break travel options through the flyai CLI, including flights and related travel bookings powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent collect route and date details, run flyai travel search commands, and return real-time flight options with booking links for spring break travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt an agent to install and run a global third-party flyai CLI. <br>
Mitigation: Approve the CLI installation manually and check the package source and version before use. <br>
Risk: Flight search details are sent to flyai/Fliggy when the CLI is used. <br>
Mitigation: Avoid sensitive travel plans unless you trust the provider and are comfortable sharing the search details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/spring-break-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output for travel data and avoids raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
