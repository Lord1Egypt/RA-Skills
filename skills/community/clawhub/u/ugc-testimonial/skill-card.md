## Description:

UGC 口播种草视频。商品 + 人设 → 口播脚本与成片，达人自拍质感。当用户说「口播视频」「种草视频」「达人风格」「UGC」「真人推荐」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce creators and marketers use the skill to turn a product and audience persona into a spoken UGC-style script, storyboard, and short promotional video. Generated performances should not be presented as genuine customer testimonials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied images may be sent to third-party generation services; the security review describes this release as benign with medium confidence.

Mitigation: Review prompts and images for sensitive content and check the selected provider's data handling before sending them.

Risk: Security review coverage is incomplete: 5 of 11 components were only partially inspected.

Mitigation: Review and scan the full release before deployment, especially components that were not fully inspected.

Risk: The security guidance notes that a referenced package is not version-pinned.

Mitigation: Check and pin unversioned dependencies before execution.

## Reference(s):

- [Provider CLI reference](references/provider-cli.md)
- [Video backend reference](references/video-backends.md)
- [dLazy CLI source](https://github.com/dlazy-ai/cli)
- [Brand kit reference](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/brand-kit/skill.md)

## Skill Output:

**Output Type(s):** [Text, Video files, Subtitle files]

**Output Format:** [Spoken scripts and storyboard text, generated video clips, and optional SRT subtitles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video model and provider availability affect generation; generated video does not provide reliable lip synchronization.]

## Skill Version(s):

1.0.30 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
