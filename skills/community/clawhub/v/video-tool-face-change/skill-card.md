## Description:

Swap the face in an existing HTTPS video using a reference face image via WeryAI (video-face-change). Use when the user wants face replacement on a video URL, not text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run WeryAI face replacement on an existing public HTTPS video with a public HTTPS reference face image. It helps an agent validate inputs, submit or poll the WeryAI job, and return generated video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unexpected extra JSON fields may be forwarded to the external WeryAI API.

Mitigation: Pass only the documented video_url and image_url fields, inspect the spec output, and use dry-run before submitting a job.

Risk: Paid submit or wait runs are documented as requiring confirmation, but that confirmation gate is not enforced by the script.

Mitigation: Require explicit user confirmation of both URLs before any non-dry-run submit or wait command.

Risk: The workflow sends provided media URLs to WeryAI for processing.

Mitigation: Use only public HTTPS media URLs that the user intends to send to WeryAI, and keep WERYAI_API_KEY only in the runtime environment.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-face-change)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, public HTTPS video and image URLs, and explicit confirmation before paid submit or wait runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
