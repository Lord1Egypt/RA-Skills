## Description:

Finds water parks and related travel services by directing agents to use the flyai CLI and format booking-centered results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find water parks, compare options, and produce concise Markdown responses with booking links from the configured travel provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global travel-booking CLI.

Mitigation: Approve installation manually, pin or verify the package before use, and run the CLI in a restricted environment.

Risk: The skill relies on one travel provider as the source of water park and booking data.

Mitigation: Treat returned listings as provider-sourced travel data and review booking details before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/water-park)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires results to come from flyai CLI output and include provider booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
