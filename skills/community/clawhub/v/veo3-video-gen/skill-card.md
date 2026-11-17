## Description:

Generate and stitch short videos via Google Veo 3.x using the Gemini API (google-genai). Use when you need to create video clips from prompts (ads, UGC-style clips, product demos) and want a reproducible CLI workflow (generate, poll, download MP4, optionally stitch multiple segments).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluelyw](https://clawhub.ai/user/bluelyw)

### License/Terms of Use:


## Use Case:

Developers and content-production teams use this skill to generate short MP4 video clips from prompts through Google Veo 3.x and to stitch multiple segments into longer outputs when ffmpeg is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, and last-frame images may be sent to Google's Gemini API during video generation.

Mitigation: Use the skill only with content that is appropriate to send to the external API, and avoid sensitive or unauthorized source material.

Risk: API keys can be exposed if passed directly on the command line or configured with broad quota and permissions.

Mitigation: Prefer GEMINI_API_KEY over the --api-key argument, restrict the key's quota and permissions where possible, and avoid logging credentials.

Risk: Runtime dependencies are declared with broad version ranges.

Mitigation: Pin and review dependencies before running the skill in sensitive or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluelyw/skills/veo3-video-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated MP4 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can emit MEDIA lines for generated MP4 files and can optionally retain intermediate segment files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
