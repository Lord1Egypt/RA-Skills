## Description:

Tóm tắt nội dung video YouTube từ đường link cung cấp, với hỗ trợ trích xuất transcript tự động bằng yt-dlp và phân tích các ý chính.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to extract available YouTube subtitles and produce concise, logically structured summaries of video content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses install commands and runs yt-dlp against user-provided YouTube links, while URL validation and dependency pinning are weak.

Mitigation: Review the sudo apt and pip commands before installation, consider installing yt-dlp in a virtual environment, and run the transcript script only with trusted YouTube links.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with transcript extraction command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript extraction prefers Vietnamese subtitles and falls back to English; long videos may be summarized in sections.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
