## Description:

根据商品信息批量生成信息流、品牌推广和社交媒体广告视频素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and advertisers use this skill to create multiple product video ads for social feeds, brand promotions, and paid campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Node and QHKit installation or upgrades can change the user's environment.

Mitigation: Request approval before installing or upgrading; prefer a preinstalled, pinned QHKit version.

Risk: Unpinned npx execution and storing a QHKit token can expose the environment or credentials.

Mitigation: Avoid unpinned npx commands and handle the token as a secret.

Risk: Uploading local product images and generating videos can disclose assets and spend Qinghu credits.

Mitigation: Confirm which assets may be uploaded and obtain cost approval before generation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-video-ad-assets)
- [QHKit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Video links]

**Output Format:** [Text with CLI commands and generated-video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task IDs, completed video URLs, and credit usage.]

## Skill Version(s):

0.1.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
