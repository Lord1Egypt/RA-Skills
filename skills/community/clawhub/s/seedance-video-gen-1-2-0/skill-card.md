## Description:

Generates Seedance videos on WeryAI from text prompts or public HTTPS image inputs, defaulting to Seedance 2.0 while supporting version-aware choices for duration, aspect ratio, resolution, audio, negative prompts, multi-image inputs, and first/last-frame workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate Seedance video clips through WeryAI from text prompts or public HTTPS image references. It helps choose a Seedance model version and validate request fields before submitting paid generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeryAI receives the API key, prompts, and any public media URLs used for generation.

Mitigation: Install and run the skill only when WeryAI is trusted for those inputs; use a short-lived or isolated environment for higher assurance and never commit WERYAI_API_KEY.

Risk: Video generation can incur paid WeryAI charges.

Mitigation: Review the confirmation details before each run, especially model, duration, resolution, image URLs, and generated audio settings.

Risk: Unsupported model parameters can fail generation or submit an unintended request.

Mitigation: Validate duration, aspect ratio, resolution, image count, first/last-frame use, generated audio, and negative prompt support against the selected Seedance model before submission.

## Reference(s):

- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/seedance-video-gen-1-2-0)
- [WeryAI Video API Host](https://api.weryai.com)
- [WeryAI Models Registry Host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with confirmation details, shell commands, JSON CLI output, and playable video links when generation succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; generation uses fixed HTTPS WeryAI endpoints and may incur paid API charges.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
