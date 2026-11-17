## Description:

Qwen视频智能分析 helps agents analyze local video files or public video URLs with Qwen 3.5 Plus by using custom prompts and frame sampling rates to produce scene descriptions, summaries, object and action recognition, content review, and question-answering results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and automation users can use this skill to inspect local videos or public video URLs for scene descriptions, summaries, object and action recognition, content review, and video-focused question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send local videos or public video URLs to Alibaba Cloud DashScope/Qwen for analysis.

Mitigation: Use only videos and URLs approved for third-party processing, avoid sensitive or internal URLs, and disclose the external transfer before use.

Risk: API-key handling and examples that print configuration values could expose secrets.

Mitigation: Use a single protected secret source with restrictive file permissions or environment-variable handling, and do not run commands that print API keys.

Risk: Broad activation text and command execution may cause the agent to run inappropriate media-processing commands.

Mitigation: Review proposed commands before execution, limit use to the documented video-analysis workflow, and avoid copyright-protected or unauthorized media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/qwen-video-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the user prompt, frame sampling rate, video length, model availability, and whether the video source can be safely accessed.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
