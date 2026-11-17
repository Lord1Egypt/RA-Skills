## Description:

Analyzes YouTube video content from SRT, VTT, TXT files, or direct YouTube URLs, then prepares summaries, key points, topics, notable quotes, and basic content statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content analysts use this skill to turn YouTube subtitles or transcript files into concise analysis reports. It supports single-video and folder-based workflows where an agent reviews the generated report and fills in the analysis sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended install path downloads executable code from a mutable GitHub branch without integrity verification.

Mitigation: Use the packaged script as reviewed, or install from a pinned commit or release with a checksum before running it.

Risk: The tool can read subtitle files or folders, fetch subtitles for user-supplied YouTube URLs, and write analysis files locally.

Mitigation: Run it only on intended inputs in a controlled workspace and review generated analysis files before relying on or sharing them.

## Reference(s):

- [Analysis Prompt Guide](references/analysis-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/skills/youtube-content-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Text analysis report with Markdown-style sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local analysis files under Youtube_Analysis and may include truncated source transcript text for agent review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
