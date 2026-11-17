## Description:

Book spring break flights for student vacations and spring holiday travel, with related travel support for hotels, trains, attraction tickets, itineraries, visa information, insurance, and car rental powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to have an agent collect travel parameters, run the flyai CLI for spring break flight searches, and summarize bookable options in Markdown. It is intended for travel booking assistance where live CLI output is required before presenting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to globally install and run an unpinned third-party CLI.

Mitigation: Install a reviewed, pinned CLI version manually and run it in a restricted environment before allowing the skill to execute flight searches.

Risk: The skill directs agents to execute user-filled shell commands without clear consent or input-safety guidance.

Mitigation: Require explicit approval before command execution and validate origin, destination, date, and sort parameters against the documented parameter list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/spring-break-flight)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when flight options are shown.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
