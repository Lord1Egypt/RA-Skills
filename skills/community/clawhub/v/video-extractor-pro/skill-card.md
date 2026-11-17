## Description:

Extracts key frames, clips, GIFs, and video metadata from local videos with ffmpeg for analysis, review, and asset collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Content reviewers, analysts, and creators use this skill to extract still frames, short clips, GIFs, or metadata from local videos for analysis, review, and asset collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ffmpeg is invoked with overwrite behavior, so existing files at selected output paths can be replaced.

Mitigation: Choose output directories and filenames deliberately, and review target paths before running extraction commands.

Risk: Extracted frames, clips, GIFs, and metadata may contain sensitive or restricted video content.

Mitigation: Process only videos you have permission to use, and handle generated outputs according to the sensitivity of the source media.

Risk: The skill depends on a local Chinese-language ffmpeg helper and external ffmpeg/ffprobe binaries.

Mitigation: Install and run it only in environments where that local tooling dependency is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/video-extractor-pro)
- [Publisher profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Local media files such as JPG, PNG, MP4, or GIF, plus JSON metadata and terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and ffprobe. Writes extracted outputs to user-selected local paths.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
