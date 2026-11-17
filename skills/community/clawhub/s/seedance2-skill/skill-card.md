## Description:

Seedance Video Creative Studio autonomously analyzes images, expands copy, matches camera work, validates quality, and generates videos via API when users provide images or text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghaonan777](https://clawhub.ai/user/zhanghaonan777)

### License/Terms of Use:

MIT

## Use Case:

External users, creative teams, and developers use this skill to turn text, image, video, or audio inputs into Chinese Seedance video prompts and optional Volcengine Ark generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded media may be sent to Volcengine Ark during generation.

Mitigation: Use only prompts and media that are approved for submission to Volcengine Ark.

Risk: Callback URLs can expose internal endpoints if configured carelessly.

Mitigation: Avoid internal callback URLs and use only reviewed webhook endpoints.

Risk: The bundled downloader can execute unintended commands on macOS when opening downloaded files.

Mitigation: Do not use the --download option with untrusted or unusual paths on macOS unless the open behavior is removed or fixed.

## Reference(s):

- [Seedance Reference Manual](reference.md)
- [Volcengine Ark API Key Console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Chinese video prompts in Markdown with inline bash commands; optional downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final video prompts must be in Chinese; API use requires ARK_API_KEY.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
