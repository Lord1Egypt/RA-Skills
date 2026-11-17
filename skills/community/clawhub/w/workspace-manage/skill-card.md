## Description:

Manages and maintains OpenClaw workspace structure by organizing folders, archiving and classifying files, cleaning temporary items, auditing workspace health, and optionally syncing backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mslchy](https://clawhub.ai/user/mslchy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working in OpenClaw workspaces use this skill to audit workspace health, create a standard directory layout, organize generated artifacts, archive old files, clean temporary files, and optionally back up workspace content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full pipeline can move local workspace files and upload broad workspace contents, including memory and configuration files, to Google Drive.

Mitigation: Review the scripts before installation, run only the needed steps, and disable sync_human and sync_backup or remove/unauthenticate gog unless Google Drive backup is intentional.

Risk: The release evidence warns not to rely on --dry-run as non-mutating in this version.

Mitigation: Avoid --all for first use and test with a disposable workspace or manually selected audit-only commands until dry-run behavior is confirmed.

Risk: File organization, cleanup, and archiving can relocate or trash workspace files.

Mitigation: Inspect proposed file lists and confirmation prompts, keep backups for important workspace content, and execute cleanup only after validating the target workspace path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mslchy/skills/workspace-manage)
- [Publisher Profile](https://clawhub.ai/user/mslchy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and script-generated text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May move, archive, clean, or sync workspace files when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
