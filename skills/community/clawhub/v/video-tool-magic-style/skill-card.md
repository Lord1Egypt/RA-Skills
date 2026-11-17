## Description:

Apply WeryAI magic style transfer to an existing HTTPS video (video-magic). Use when the user wants preset visual restyling of a video URL, not text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to apply a supported WeryAI magic style preset to an existing public HTTPS video URL. It is intended for video restyling workflows, not for creating new videos from text or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends the supplied video URL and style-transfer request to WeryAI using a paid API key.

Mitigation: Use the skill only when that external processing is acceptable, keep WERYAI_API_KEY in the runtime environment, and confirm the video URL and style before submit or wait.

Risk: Paid submit or wait runs are not idempotent and may consume credits.

Mitigation: Use --dry-run to validate the JSON request first, and require explicit user confirmation before starting a paid run.

Risk: Over-broad installs or sibling scripts could expose workflows outside the documented magic-style scope.

Mitigation: Run only artifact/scripts/video_magic_style.js for this skill and inspect the tool spec before execution.

Risk: Local files are not supported by this skill and should not be uploaded through unrelated tools.

Mitigation: Provide only public https:// video URLs and avoid tools that accept local paths unless separately reviewed.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-magic-style)
- [ClawHub publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown links and JSON status or request results from the WeryAI CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WeryAI task IDs, polling status, errors, and final video URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
