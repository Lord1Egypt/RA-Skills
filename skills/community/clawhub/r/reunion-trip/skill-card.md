## Description: <br>
Book flights for family and class reunion trips, with related travel support for hotels, train tickets, attractions, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search reunion travel options and receive Markdown flight recommendations with booking links from the flyai CLI. The skill is intended for family reunion, class reunion, alumni trip, and broader trip-planning requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to install a global third-party npm package. <br>
Mitigation: Require explicit user approval before installing @fly-ai/flyai-cli and verify the package and version independently. <br>
Risk: Travel search details may be sent to the provider through flyai commands. <br>
Mitigation: Confirm the user's consent before running searches and avoid submitting unnecessary personal or sensitive trip details. <br>
Risk: Broad trigger phrases may activate the skill for general travel planning requests. <br>
Mitigation: Confirm that the user wants flyai-backed travel search before executing commands when intent is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivan97/reunion-trip) <br>
- [Publisher profile](https://clawhub.ai/user/ivan97) <br>
- [Parameter collection and output templates](artifact/references/templates.md) <br>
- [Scenario playbooks](artifact/references/playbooks.md) <br>
- [Failure recovery](artifact/references/fallbacks.md) <br>
- [Execution runbook](artifact/references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, brief guidance, and inline shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be grounded in flyai CLI results, include booking links when results are shown, and include the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
