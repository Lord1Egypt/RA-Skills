## Description:

Plan educational travel experiences such as museum visits, university tours, cultural workshops, historical field trips, and hands-on learning activities, with Fliggy-powered travel search and booking support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to assemble educational trips and compare provider-backed flights, hotels, attractions, and itinerary options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned global third-party npm package.

Mitigation: Require explicit user approval before installation, prefer a pinned package version, and use an isolated environment for execution.

Risk: Travel recommendations are constrained to provider-backed booking links rather than neutral travel research.

Mitigation: Disclose that results come from the flyai provider workflow and verify suitability, price, availability, and booking terms before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/study-tour)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands when setup is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in flyai CLI results and include provider booking links when presenting travel options.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
