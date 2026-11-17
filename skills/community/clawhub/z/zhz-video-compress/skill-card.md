## Description:

Compresses and organizes video files with FFmpeg, with options for quality, speed, output location, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users managing video libraries can batch-compress files to save storage or organize them by date. They can preview affected files and choose output quality and whether to replace originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner identified a path-handling flaw that could place compressed output outside the selected folder; scanner coverage was partial.

Mitigation: Run `--dry-run`, verify each displayed destination, and review path handling before processing important folders.

Risk: The skill does not declare its tool scope, and scanner analysis was incomplete.

Mitigation: Review the script's filesystem access and required tools before installation or use.

## Reference(s):

- [Project homepage](http://openclaw.bjbook.net/)
- [ClawHub skill release](https://clawhub.ai/bjbook/skills/zhz-video-compress)

## Skill Output:

**Output Type(s):** [Video files, Shell commands, Guidance]

**Output Format:** [Compressed video files and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [H.265 or H.264 outputs with optional date-based organization.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
