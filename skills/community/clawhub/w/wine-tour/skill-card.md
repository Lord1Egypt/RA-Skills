## Description:

Book flights for wine tours to famous vineyards and wine regions, with related support for hotels, trains, attraction tickets, itineraries, visa information, travel insurance, and car rental through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-assistant agents use this skill to search and present wine-tour flight options with booking links, route comparisons, and wine-region tips. The skill requires travel answers to be grounded in flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send travel routes and dates to the FlyAI/Fliggy provider.

Mitigation: Use it only when the provider is trusted and users are comfortable sharing the relevant travel details.

Risk: The skill directs automatic global npm installation of flyai-cli.

Mitigation: Prefer a pinned, local, reviewed installation in a sandbox instead of automatic global installation.

Risk: The skill executes CLI commands using user-supplied travel fields.

Mitigation: Invoke the CLI with argument arrays and strict parameter validation rather than interpolating user text into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liquanyu123/skills/wine-tour)
- [Parameter collection and output templates](artifact/references/templates.md)
- [Scenario playbooks](artifact/references/playbooks.md)
- [Failure recovery](artifact/references/fallbacks.md)
- [Execution runbook](artifact/references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel results with comparison tables, concise recommendations, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output; every travel result is expected to include a booking link.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
