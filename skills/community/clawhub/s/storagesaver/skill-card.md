## Description:

Watch and explain Mac disk usage for users who need to identify what is consuming disk space, generate a visual report, or schedule storage alerts without deleting files automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelsonscott](https://clawhub.ai/user/nelsonscott)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and support agents use this skill to inspect Mac storage usage, explain likely reclaim opportunities, and prepare safe user-reviewed cleanup guidance. It also supports scheduled disk-usage checks with configurable notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher can run mutable npm-installed code if installed without a pinned trusted version.

Mitigation: Install only from a trusted package source and prefer a pinned version before scheduling recurring runs.

Risk: NOTIFY_CMD executes a user-supplied shell notification command.

Mitigation: Review the exact NOTIFY_CMD value and destination before scheduling the watcher.

Risk: Generated HTML and JSON reports can reveal local filenames, project paths, installed apps, cloud-storage locations, and usage patterns.

Mitigation: Treat reports as private local data and avoid sharing them in public channels.

Risk: Suggested cleanup commands may remove important local or cloud-backed data if copied without review.

Mitigation: Verify each target path and backup or cloud-sync status before running any suggested delete command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nelsonscott/skills/storagesaver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and cron command snippets; watcher runs can also produce HTML and JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations; notification output may go to stdout or a user-supplied NOTIFY_CMD, and reports are written under ~/.config/storagesaver/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
