## Description:

Remove watermark overlays from an existing HTTPS video via WeryAI (video-watermark-remove). Use when the user wants watermark cleanup, not subtitles-only or text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to remove watermark overlays from an existing public HTTPS video with WeryAI, optionally specifying normalized regions or relying on auto-detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends public HTTPS video URLs to WeryAI and may consume paid API credits.

Mitigation: Confirm the video URL and any custom regions before submit or wait, and avoid private or sensitive video URLs unless third-party processing is acceptable.

Risk: The WeryAI API key could be exposed if written into files or prompts.

Mitigation: Keep WERYAI_API_KEY only in the runtime environment and do not store it in skill files or command examples.

Risk: A copied package may contain sibling scripts outside this skill's intended contract.

Mitigation: Run only scripts/video_watermark_remove.js for this skill and inspect the local package layout before execution.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-watermark-remove)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WERYAI_API_KEY, accepts a public HTTPS video URL, and can include optional normalized watermark-region boxes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
