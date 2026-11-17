## Description:

Synchronizes skills from a team Git repository into a local OpenClaw skills directory, with setup, scheduled updates, manual sync, log viewing, and uninstall guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzj666666](https://clawhub.ai/user/wzj666666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to initialize, schedule, manually run, inspect, and uninstall synchronization of team-maintained skills from a configured Git repository into their local OpenClaw skills directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled synchronization creates an unattended remote update path into local OpenClaw skills.

Mitigation: Use only a trusted repository, prefer manual sync or a pinned and reviewed revision, and inspect changes before relying on newly synchronized skills.

Risk: Synchronization can overwrite or delete existing files in synchronized skill directories.

Mitigation: Back up local skills before enabling sync and confirm the configured repository path and skills subdirectory before running setup or sync commands.

Risk: Cron jobs and synchronized skill directories may remain active or present after uninstall steps.

Mitigation: Remove the named OpenClaw cron jobs and manually clean any synchronized skill directories that should no longer be available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzj666666/skills/qg-skill-sync)
- [Default configured team skills repository](https://github.com/wzj666666/ai-platform-skills.git)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git and bash; writes local synchronization configuration, logs, and copied skill files when the generated commands are executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
