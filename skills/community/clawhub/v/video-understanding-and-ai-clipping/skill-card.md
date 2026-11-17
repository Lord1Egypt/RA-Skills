## Description:

WayinVideo AI video editing and analysis suite for highlight extraction, natural language video search, content summarization, transcription, and configurable video export from online URLs or local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayinvideo](https://clawhub.ai/user/wayinvideo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate WayinVideo analysis and editing workflows, including clipping, moment search, summarization, transcription, and export formatting for social platforms. It is intended for agents that need to submit video jobs, poll for results, and return usable links or local result files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, URLs, and task content may be sent to WayinVideo using the user's WAYIN_API_KEY.

Mitigation: Require explicit user confirmation before uploading local files or submitting API jobs, especially for sensitive or private media.

Risk: The skill can write result JSON files and persistent CLI preferences to local user directories.

Mitigation: Use --no-save or a private project directory for sensitive work, and confirm before changing global configuration.

Risk: Export downloads and background polling may perform long-running or paid API activity.

Mitigation: Confirm cost, duration, and download destination before starting polling, exports, or downloads.

Risk: The documented curl download pattern can be unsafe with untrusted filenames or links.

Mitigation: Use safe argument handling and a user-approved output path when downloading export links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wayinvideo/skills/video-understanding-and-ai-clipping)
- [AI Clipping Task Basics](basics/ai-clipping.md)
- [Find Video Moments Basics](basics/find-moments.md)
- [Video Summary Basics](basics/video-summarization.md)
- [Video Transcription Basics](basics/video-transcription.md)
- [Video Export Task Basics](basics/export.md)
- [Caption style reference](references/caption_style.md)
- [Platform duration reference](references/platform_duration.md)
- [Platform ratio reference](references/platform_ratio.md)
- [Supported languages reference](references/supported_languages.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI task results are JSON files or JSON stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce export links and local result file paths; requires WAYIN_API_KEY and python3.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
