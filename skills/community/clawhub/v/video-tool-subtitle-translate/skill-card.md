## Description:

Translates subtitles in an existing HTTPS video via WeryAI when the user wants subtitle translation rather than subtitle erasure or text-to-video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit a public HTTPS video URL to WeryAI and translate its subtitles into a requested target language. It is scoped to subtitle translation on existing videos and does not perform local file upload, subtitle removal, or new video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a public HTTPS video URL to WeryAI, a paid external processor.

Mitigation: Use only public HTTPS video URLs that the user has confirmed, and proceed only when the user is comfortable with WeryAI processing the video.

Risk: Submitting or waiting on a job can consume paid WeryAI credits and may not be idempotent.

Mitigation: Confirm the exact video URL and target language before submission, and use dry-run mode to validate the request payload first.

Risk: The WERYAI_API_KEY credential could be exposed if written into files or prompts.

Mitigation: Keep WERYAI_API_KEY only in the runtime environment and never write it to files.

Risk: Running out-of-scope sibling tools could use different inputs or upload behavior.

Mitigation: Run only scripts/video_subtitle_translate.js for this skill and inspect the local package layout before execution.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-subtitle-translate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, task status, translated video URLs, validation errors, or dry-run request previews.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
