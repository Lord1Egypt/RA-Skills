## Description:

Book flights for sports events, game days, and match travel with flexible date options, with related travel support powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search for flights around sports events, match days, and tournament windows, then present bookable options with provider-supplied links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running an unpinned global flyai npm CLI.

Mitigation: Install a reviewed, pinned CLI version in an isolated environment before using the skill.

Risk: The skill presents provider-supplied booking links for flights or related travel purchases.

Mitigation: Verify booking-link domains and purchase details before clicking links or completing transactions.

Risk: Travel results can be misleading if the agent answers from memory instead of current CLI output.

Mitigation: Require results to come from flyai CLI output and omit any option that lacks a provider detailUrl booking link.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/sports-flight)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recommendations with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results and booking detailUrl links; raw JSON is not intended for end-user output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
