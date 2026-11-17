## Description:

Extract subtitles and transcripts from YouTube videos using yt-dlp first, with browser automation as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to extract timestamped YouTube subtitles or transcripts into a local text file for review, notes, accessibility workflows, or downstream content processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access browser cookies or an active browser session during transcript extraction.

Mitigation: Run transcript extraction without browser cookies first; allow cookie access only after explicit confirmation, preferably from a dedicated browser profile.

Risk: The skill writes transcript files into the current working directory.

Mitigation: Run it from an intended workspace and review generated filenames before sharing or committing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiskyer/skills/youtube-transcribe-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Timestamped transcript text saved as a .txt file, with a short completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the output path, subtitle language, and total line count when extraction completes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
