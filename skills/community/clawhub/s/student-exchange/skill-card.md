## Description:

Searches for student exchange and study abroad travel options, including flights and related bookings, using flyai/Fliggy results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect route details, run flyai flight-search commands, and format study abroad travel options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global npm CLI before use.

Mitigation: Review and approve the flyai package source and version before installation, and prefer a sandboxed or manually installed CLI.

Risk: Travel routes and dates are used to build shell-style CLI commands.

Mitigation: Validate user-entered origin, destination, and date values before command execution.

Risk: The security verdict is suspicious because the skill routes flight searches through a third-party CLI and returns booking-link-oriented output.

Mitigation: Use the skill only when that routing is acceptable and review generated results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liquanyu123/skills/student-exchange)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flyai CLI results and should include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
