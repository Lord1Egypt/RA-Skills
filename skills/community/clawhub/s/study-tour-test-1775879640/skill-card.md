## Description:

Plan educational travel experiences, including museum visits, university tours, cultural workshops, historical field trips, hands-on learning activities, and related travel bookings powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to assemble study tour itineraries for museums, schools, cultural sites, historical trips, and STEM activities. The skill directs the agent to obtain current travel options from the FlyAI/Fliggy CLI and return Markdown summaries with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install an unpinned global npm package for the FlyAI CLI.

Mitigation: Install a reviewed, pinned CLI version in an isolated environment before enabling the skill.

Risk: The skill requires FlyAI/Fliggy as the travel data source and mandates booking links in outputs.

Mitigation: Confirm the provider requirement and booking-link behavior are acceptable for the deployment context, and review generated travel recommendations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/study-tour-test-1775879640)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on FlyAI/Fliggy CLI results and are expected to include booking links and provider branding.]

## Skill Version(s):

3.2.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
