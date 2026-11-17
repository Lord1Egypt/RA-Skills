## Description:

Extracts transcripts and subtitles from video URLs and delivers cleaned transcript documents, including Chinese translations for non-Chinese videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vistalyq](https://clawhub.ai/user/vistalyq)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to turn supported video links into readable transcript files for review, reuse, translation, or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command construction may expose users to command-injection risk when video URLs, titles, or transcript text are interpolated into shell commands.

Mitigation: Review before installing and prefer a revised version that passes URLs, titles, and transcript text as structured process arguments or stdin.

Risk: Dependency installation without pinned versions or a lockfile creates supply-chain risk.

Mitigation: Pin dependencies and add a lockfile before using the skill in a sensitive environment.

Risk: Video URLs and transcript content may include sensitive information.

Mitigation: Use the skill only with public or non-sensitive video links unless the execution environment and handling process are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vistalyq/skills/video2txt)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated .docx transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one Chinese transcript document for Chinese videos, or original-language and Chinese-translation documents for non-Chinese videos when subtitles are available.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
