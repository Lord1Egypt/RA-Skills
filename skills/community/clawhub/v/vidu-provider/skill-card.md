## Description:

Video generation provider plugin for Vidu (viduq3-pro, viduq3-turbo, viduq2, viduq1) that supports text-to-video, image-to-video, reference-to-video, and start-end-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaonan-ss](https://clawhub.ai/user/xiaonan-ss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this provider to connect agents to Vidu video generation for text, image, reference, and start-end video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated videos are downloaded from provider-supplied URLs without clear destination or size controls.

Mitigation: Run in an environment where downloads cannot reach internal services; validate generated-video URLs, block private-network destinations and redirects, and cap download size before deployment.

Risk: Prompts and uploaded images or videos are sent to Vidu for generation.

Mitigation: Use only data that is appropriate for Vidu processing, and document provider data handling for users before deployment.

## Reference(s):

- [Vidu Platform](https://platform.vidu.com)
- [Vidu Global API endpoint](https://api.vidu.com)
- [Vidu China API endpoint](https://api.vidu.cn)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Files, API Calls, Configuration]

**Output Format:** [Generated video assets with provider metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIDU_API_KEY; supports Global and China Vidu endpoints; returns one generated video per request.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter/package.json: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
