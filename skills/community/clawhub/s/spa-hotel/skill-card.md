## Description:

Book flights to spa hotels and wellness resort destinations, with related travel booking support for hotels, train tickets, attraction tickets, itinerary planning, visa information, insurance, and car rental through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to search spa hotel and wellness resort trips by collecting route and date details, running the flyai CLI, and formatting real-time booking options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger installation and use of a third-party travel CLI.

Mitigation: Review and install a pinned CLI version manually before enabling the skill.

Risk: Shell command templates may become unsafe if user-provided travel parameters are not validated.

Mitigation: Validate route, date, and sort inputs before command execution and run the CLI in a restricted environment.

Risk: Generated booking links route users to third-party commercial travel services.

Mitigation: Treat booking links as third-party commercial links and require user review before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/spa-hotel)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when travel options are presented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
