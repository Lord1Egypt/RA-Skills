## Description: <br>
Searches for quick weekend getaway flights, auto-suggesting Friday or Saturday departures and Sunday or Monday returns, with support for related travel searches powered by Fliggy and FlyAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and travel-focused agents use this skill to turn weekend trip requests into FlyAI CLI flight searches, then format real-time results with booking links. It is intended for users comparing short weekend and long-weekend travel options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global FlyAI CLI package. <br>
Mitigation: Require explicit user approval before installing the npm package and verify the package source before use. <br>
Risk: Travel searches are sent to an external Fliggy/FlyAI service and may include personal travel preferences. <br>
Mitigation: Share only the minimum trip details needed for the search and avoid unnecessary personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/weekend-flights) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FlyAI CLI output as the required source for travel results and avoids raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
