## Description:

Track time with Toggl via the toggl CLI for starting and stopping timers, checking the current timer, viewing reports, listing recent entries, and managing time entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clvrobj](https://clawhub.ai/user/clvrobj)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers who use Toggl Track can ask an agent to operate Toggl timers, reports, projects, and time-entry management through the toggl CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned global third-party npm CLI with access to the user's Toggl account.

Mitigation: Pin and review a specific CLI package version before installation.

Risk: The Toggl API token is stored locally and could expose account access if file permissions are weak or the token is leaked.

Mitigation: Keep the token file restricted, use environment secrets where appropriate, and rotate the token if exposure is suspected.

Risk: The skill can edit or delete time entries through CLI commands.

Mitigation: Require explicit user confirmation before modifying or deleting time records.

## Reference(s):

- [Toggl Track Profile](https://track.toggl.com/profile)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Toggl CLI commands that access or modify the user's Toggl Track data.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
