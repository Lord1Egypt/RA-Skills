## Description:

Runs local macOS scripts to switch desktop wallpaper from a user-provided image folder immediately or install a launchd task for scheduled wallpaper rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and desktop automation agents use this skill on macOS to inspect a local wallpaper folder, switch to a random wallpaper, or install and remove a scheduled launchd rotation task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts contain confirmed command-injection risks when handling user-provided paths or filenames.

Mitigation: Review before installing, use only trusted wallpaper directories and filenames, and avoid paths containing shell or XML metacharacters.

Risk: Installing the automation creates a persistent user LaunchAgent that continues running on a schedule.

Mitigation: Install the LaunchAgent only after confirming the schedule and directory, and use the provided uninstall command when automatic rotation is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/wallpaper-auto-switch-pro-executable)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report local directory paths, selected wallpaper file paths, launchd plist paths, command success, and explicit failure reasons.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
