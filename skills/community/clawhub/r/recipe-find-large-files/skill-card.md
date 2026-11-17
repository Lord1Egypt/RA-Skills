## Description:

Identify large Google Drive files consuming storage quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Users with Google Workspace Drive access use this recipe to list the largest files in Drive and decide which files to archive or move to reduce storage usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command output may reveal sensitive Google Drive file names, ownership details, and storage usage metadata.

Mitigation: Run the recipe only in accounts where Drive metadata listing is acceptable, and avoid sharing the resulting table outside the intended review context.

Risk: The recipe depends on Google Workspace CLI access and the gws-drive skill being available and authorized.

Mitigation: Confirm gws and gws-drive are installed and authenticated before running the listed command.

## Reference(s):

- [Recipe Find Large Files on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/recipe-find-large-files)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gws and the gws-drive skill; command output may include Google Drive file names, file sizes, MIME types, and owners.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
