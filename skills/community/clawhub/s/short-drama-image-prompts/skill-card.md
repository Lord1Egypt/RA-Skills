## Description:

为短剧人物、造型、场景、道具和状态编写或修改可直接复制的图片提示词 Markdown。用户提到角色设定图、三视图、参考图、场景空镜图、道具设定图、视觉定调图、Look Development、状态变化图或局部改图提示词时使用；不生成图片，也不调用供应商。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

面向短剧编剧、美术及制作人员，帮助他们根据已确认的视觉设定编写或修订角色、场景、道具和状态图的可复制图片提示词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because the referenced `short-drama.json` file was not included.

Mitigation: If the project relies on that configuration, obtain and review it before installation; otherwise follow the skill's documented language-inference guidance.

## Reference(s):

- [美术设定图与视觉定调提示词指南](artifact/references/sheet-prompt-guide.md)
- [图片提示词阶段规则](artifact/references/stage-contract.md)
- [换装状态图与局部改图指南](artifact/references/variants-and-edits.md)
- [ClawHub release](https://clawhub.ai/worldwonderer/skills/short-drama-image-prompts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with directly copyable image prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt text only; it does not generate images.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
