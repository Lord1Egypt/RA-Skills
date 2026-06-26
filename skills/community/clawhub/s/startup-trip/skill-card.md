## Description: <br>
Book flights for startup events and entrepreneur travel, with support for related travel planning tasks through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search startup-event and entrepreneur travel options, collect route and date parameters, run the flyai CLI, and present booking-linked flight recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global @fly-ai/flyai-cli package for travel searches. <br>
Mitigation: Install or approve the CLI manually in an isolated environment before allowing the agent to run travel searches. <br>
Risk: The skill can produce booking links and travel recommendations from an external travel CLI. <br>
Mitigation: Review generated commands, returned prices, itineraries, and booking links before acting on them. <br>
Risk: Broad travel-planning triggers may activate the skill for general trip requests. <br>
Mitigation: Confirm the user intends to use this travel booking workflow before installing or running the CLI. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output for travel results; each presented result is expected to include a booking link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
