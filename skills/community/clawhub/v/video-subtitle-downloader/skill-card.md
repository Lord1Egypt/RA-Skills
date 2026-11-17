## Description:

Download and convert subtitles from YouTube, Bilibili, Twitter, and other supported video platforms into SRT, JSON, or TXT files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to help an agent extract subtitles or transcript text from video URLs for study notes, translation, review workflows, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation or unpinned dependency versions may change runtime behavior.

Mitigation: Install in a virtual environment and review or pin dependency versions before use.

Risk: The skill contacts video platforms and writes subtitle files locally.

Mitigation: Run it only against intended video URLs and check the configured output directory before and after execution.

Risk: Processing private, sensitive, or copyrighted videos can create privacy, copyright, or platform-terms concerns.

Mitigation: Process only videos you are permitted to use and confirm the relevant platform terms before downloading or converting subtitles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/video-subtitle-downloader)
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and local subtitle file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create SRT, JSON, or TXT subtitle files in the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
