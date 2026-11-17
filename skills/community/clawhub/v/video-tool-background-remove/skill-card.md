## Description:

Remove or replace a video background with a solid color via WeryAI (video-background-remove). Use when the user wants background removal or a flat-color backdrop on an HTTPS video, not text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to remove or replace the background of an existing public HTTPS video through WeryAI. It is scoped to the background-remove workflow and requires confirmation before paid processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid live runs send the request body and video URL to WeryAI.

Mitigation: Confirm the HTTPS video URL and selected background color before running submit or wait, and avoid including secrets or private metadata in the JSON payload.

Risk: Undeclared JSON fields may be forwarded to the external API.

Mitigation: Inspect payloads before live runs and include only the documented video_url and background_color fields.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-background-remove)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and final video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and a public HTTPS video URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
