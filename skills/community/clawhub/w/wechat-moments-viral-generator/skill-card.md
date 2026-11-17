## Description:

根据产品、场景和风格生成适合微信朋友圈发布的营销文案，并附带 emoji 组合、配图建议、发布时间和互动引导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessabuivolova-sketch](https://clawhub.ai/user/jessabuivolova-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

微信营销人员、私域运营者和内容创作者可用它为产品推广、社群转化、个人品牌和限时促销快速生成朋友圈文案。The skill is intended for human-reviewed promotional copy generation rather than autonomous posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid or unbounded count input could produce unexpected output volume if the skill is exposed through a public or automated interface.

Mitigation: Validate count against the documented 3-20 range before invoking the generator.

Risk: Generated promotional copy may use scarcity, anxiety, or conversion-oriented language that could be inaccurate or unsuitable for a specific product claim.

Mitigation: Require human review for factual accuracy, platform-policy fit, and brand suitability before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessabuivolova-sketch/skills/wechat-moments-viral-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style copy blocks and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates multiple WeChat Moments copy variants with emoji combinations, image suggestions, publish-time guidance, interaction prompts, and usage tips.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
