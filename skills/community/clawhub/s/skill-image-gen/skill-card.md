## Description:

Generates AI images with the Gitee AI API, saves them locally, and can optionally upload generated images to Tencent Cloud COS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weznai](https://clawhub.ai/user/weznai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate images from text prompts with Gitee AI, save PNG outputs locally, and optionally publish generated images to a Tencent COS bucket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Gitee AI, and generated images may be uploaded to Tencent COS when COS upload is enabled.

Mitigation: Use only prompts and generated content suitable for those services, and keep COS upload disabled unless cloud storage is required.

Risk: Gitee API keys and Tencent COS credentials may be collected through setup flows or stored in configuration files.

Mitigation: Store credentials outside chat transcripts with restrictive file permissions or a secret manager, use narrowly scoped keys, and avoid logging full secrets.

Risk: The URL-download helper can fetch external image URLs without additional network or size controls.

Mitigation: Do not expose URL downloads to untrusted URLs unless the caller adds allowlists, content-size limits, and timeout checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weznai/skills/skill-image-gen)
- [Gitee AI](https://ai.gitee.com/)
- [Gitee AI documentation](https://ai.gitee.com/docs)
- [Gitee AI API key guide](references/GET_API_KEY.md)
- [Configuration example](references/config.example.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, shell commands, Python snippets, JSON status, and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gitee AI API key; optional Tencent COS credentials enable cloud upload.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
