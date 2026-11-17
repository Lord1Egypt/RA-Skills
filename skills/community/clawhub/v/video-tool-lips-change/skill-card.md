## Description:

Lip-sync an existing HTTPS video to a separate audio URL via WeryAI (video-lips-change). Use when the user wants lip sync to new audio, not text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run WeryAI lip sync on an existing public HTTPS video with a separate public HTTPS audio track. It is intended for changing lip movement to match new audio, not for text-to-video, image-to-video, face replacement, or local upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the selected video URL, audio URL, and authenticated request to WeryAI.

Mitigation: Use only public HTTPS media URLs that are appropriate to share with WeryAI, and install the skill only if that data flow is acceptable.

Risk: Paid submissions are not idempotent and may consume credits.

Mitigation: Run a dry-run first and require explicit user confirmation of both URLs before submit or wait.

Risk: Extra JSON fields are not stripped before submission.

Mitigation: Provide only the documented video_url and audio_url fields unless the skill is updated and reviewed.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-lips-change)
- [Publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include dry-run request previews, task IDs, status results, and final video links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
