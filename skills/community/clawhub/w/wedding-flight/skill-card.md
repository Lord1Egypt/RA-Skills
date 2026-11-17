## Description:

Helps agents search wedding and honeymoon flight options using the flyai CLI with flexible dates, seat class preferences, and booking-link output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users, travel planners, and agents use this skill to collect wedding or honeymoon flight parameters, run real-time flyai searches, and return concise flight comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install an unverified global npm CLI, which can change the global npm environment.

Mitigation: Use a pinned and reviewed flyai CLI version, prefer a project-local or sandboxed install, and require explicit approval before installation.

Risk: User-filled shell command templates can be unsafe if dates or locations are passed through shell interpolation without validation.

Mitigation: Validate date and location inputs and invoke the CLI with structured arguments instead of concatenated shell strings.

Risk: Flight booking links depend on the flyai provider and may route users to transactions outside the agent environment.

Mitigation: Verify that flyai is the intended Fliggy-backed provider and review booking links before users act on them.

## Reference(s):

- [Wedding Flight Skill](https://clawhub.ai/liquanyu123/skills/wedding-flight)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown flight comparisons with booking links and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for flight data; each listed result should include a Book link sourced from detailUrl.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
