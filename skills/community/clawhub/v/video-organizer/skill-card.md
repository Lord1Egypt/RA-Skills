## Description:

Video Organizer helps agents guide users through batch video file organization and renaming by date or format, with preview and undo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to organize local video folders, preview planned changes, batch rename video files, and undo supported operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs local file organization and renaming, so mistakes can change or duplicate files in directories selected by the user.

Mitigation: Use preview before execution, run only against intended directories, and keep separate backups of important videos.

Risk: Rename patterns or regex replacements may introduce unsafe or unintended paths.

Mitigation: Avoid slashes, dot-dot path segments, and absolute paths in rename patterns or regex replacements.

Risk: Undo behavior depends on a local .video-organizer-backup.json file and may be unsafe if that file is missing or modified.

Mitigation: Do not rely on undo as the only recovery mechanism, and do not run undo in a directory where the backup file could have been changed by someone else.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/video-organizer)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview, organize, rename, and undo command guidance for user-selected local directories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
