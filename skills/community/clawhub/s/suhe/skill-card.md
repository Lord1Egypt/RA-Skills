## Description:

Initialize a Suhe/OpenClaw agent workspace with identity, memory, safety, and Carbon-Silicon Bond templates, and optionally generate Tongyi Wanxiang selfies for messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilozhao](https://clawhub.ai/user/lilozhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this package to bootstrap a Suhe-style agent workspace with identity, memory, safety, setup, and documentation files. The bundled selfie skill can generate edited reference-image selfies through DashScope/Tongyi Wanxiang and send them to configured messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer scripts can write persistent agent workspace, skill, documentation, and memory files under ~/.openclaw.

Mitigation: Review the files to be copied before installation and back up or isolate any existing OpenClaw workspace.

Risk: Prompts, image URLs, captions, and channel details may be sent to external image providers and a local or configured OpenClaw gateway.

Mitigation: Avoid sensitive prompts or private images, verify provider and gateway configuration, and keep API keys in environment variables.

Risk: The selfie workflow can send generated media to messaging channels or publish hosted image links.

Mitigation: Require explicit user confirmation before sending to any channel or creating a public hosted link.

Risk: The package contains broader agent bootstrap behavior in addition to the selfie-generation feature.

Mitigation: Install only when the full Suhe/OpenClaw bootstrap is intended, not when a standalone selfie tool is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilozhao/skills/suhe)
- [DashScope Console](https://dashscope.console.aliyun.com/)
- [DashScope image generation endpoint used by the skill](https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and generated JSON status from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent OpenClaw workspace, skill, documentation, and memory files under the user's home directory when installer scripts are run.]

## Skill Version(s):

1.2.0 (source: package.json, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
