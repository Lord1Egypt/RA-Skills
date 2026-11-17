## Description:

vsum summarizes YouTube and Bilibili videos by retrieving subtitles and producing Markdown summaries with an AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischaan](https://clawhub.ai/user/chrischaan)

### License/Terms of Use:


## Use Case:

External users and developers use vsum to summarize YouTube or Bilibili videos from a provided URL by retrieving subtitles, sending transcript content to an AI summarizer, and saving the result as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bilibili workflow can read Chrome login cookies through yt-dlp.

Mitigation: Use an explicit cookie file or a dedicated browser profile, and run the workflow only when sharing those cookies with yt-dlp is acceptable.

Risk: The helper script writes downloaded subtitle files to the user's Downloads directory without strong confirmation.

Mitigation: Confirm the intended output location before running the script and review generated files after execution.

Risk: URL safeguards are limited for user-provided video links.

Mitigation: Avoid running the helper script on untrusted links until URL validation and yt-dlp option-delimiting are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischaan/skills/vsum)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script writes subtitle files to the user's Downloads directory; final summaries are described as Markdown output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
