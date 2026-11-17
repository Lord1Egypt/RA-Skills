## Description:

Mines YouTube video comments for user pain points, feature requests, competitor feedback, and market research signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthere](https://clawhub.ai/user/synthere)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, market researchers, and developers use this skill to collect YouTube comments for a topic or competitor video set and turn them into categorized pain-point and feature-request analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script has an argument-handling flaw that could expose local file contents through outbound requests.

Mitigation: Review the script before use, run it only in an isolated environment, and avoid passing untrusted values as the count argument.

Risk: The workflow stores YouTube comment data locally, including author-related fields.

Mitigation: Treat collected comments as user data, restrict access to output folders, and delete local datasets when they are no longer needed.

Risk: The skill depends on external command-line and Python packages.

Mitigation: Pin and audit dependencies before installation and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synthere/skills/youtube-comment-miner)
- [Publisher profile](https://clawhub.ai/user/synthere)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [youtube-search](https://pypi.org/project/youtube-search/)
- [yt-dlp-nb](https://github.com/theghostjw/yt-dlp-nb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code, JSON comment data, JSON analysis output, and terminal summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fetched YouTube comment data under youtube_comments/ and writes analysis_result.json in the analyzed folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
