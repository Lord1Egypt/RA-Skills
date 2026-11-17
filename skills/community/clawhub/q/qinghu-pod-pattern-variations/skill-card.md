## Description:

基于一个印花快速生成多个设计版本，支持不同风格、颜色及元素组合，提高 POD 设计效率。当用户要求印花裂变、图案变体、衍生设计、一个图案出多版时必须触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

POD designers and ecommerce teams use the skill to create coordinated pattern variations from a supplied print, exploring new palettes, themes, elements, and arrangements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI upgrades can change software running in the user's environment.

Mitigation: Use a reviewed fixed CLI version in a user-scoped environment and approve upgrades manually.

Risk: Selected images are sent to the image-generation service, which can consume credits; provider credentials may be stored locally.

Mitigation: Share only images appropriate for external processing, check the expected credit cost, and keep credentials in a user-scoped configuration.

Risk: The downloaded CLI implementation is outside the artifact review, and tool messages may include commands.

Mitigation: Review commands shown in tool messages before running them.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI POD materials](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell command examples and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides prompts and CLI commands for image variation; generated pattern details may differ slightly from the source.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
