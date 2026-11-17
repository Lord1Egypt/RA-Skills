## Description:

Create Simplified Chinese or Chinese-English bilingual hard-subtitled videos from YouTube links or existing video/subtitle files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodenxyz](https://clawhub.ai/user/woodenxyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video localization teams use this skill to create Simplified Chinese or optional Chinese-English hard-subtitled videos from YouTube links or local video/subtitle inputs, with reusable subtitle files, review screenshots, descriptions, and cover assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs ffmpeg and yt-dlp and writes media outputs locally.

Mitigation: Install and run it only in environments where local YouTube media processing and file writes are acceptable, and review generated output paths before use.

Risk: The feedback feature can turn reusable user feedback into future workflow instructions.

Mitigation: Allow reusable feedback only from trusted users and review changes to workflow.md, quality-gates.md, and SKILL.md before re-packaging or reusing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woodenxyz/skills/youtube-cn-subtitle-burnin)
- [Project homepage](https://github.com/woodenxyz/youtube-cn-subtitle-burnin)
- [Workflow](references/workflow.md)
- [Quality Gates](references/quality-gates.md)
- [Review Template](references/review-template.md)
- [Feedback Ledger](references/feedback-ledger.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON translation batches, subtitle files, review records, and generated media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local, versioned video, subtitle, cover, description, screenshot, and review artifacts; requires python3, ffmpeg, ffprobe, and yt-dlp.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
