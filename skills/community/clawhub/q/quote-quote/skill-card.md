## Description:

「拾句」金句语录技能在用户需要金句、语录、名言警句摘抄、朋友圈文案或文案灵感时，从图语录和精选素材中按主题整理有共鸣的句子，标注出处与适用场景，并可按需生成日签卡片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[urselect](https://clawhub.ai/user/urselect)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to obtain themed Chinese quotations, short social-post copy, attribution notes, usage scenarios, and optional daily quote-card images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts tuyulu.com to retrieve public quote data.

Mitigation: Review network access expectations before installation and use the script only where this public data source is acceptable.

Risk: Quotation origins can be uncertain or unsuitable for public posting.

Mitigation: Review generated quotations and attributions before publication, especially when the skill marks an origin as uncertain or AI-created.

Risk: Generated daily quote-card images can contain text or attribution errors.

Mitigation: Check generated image text and attribution before sharing; correct mistakes with image editing when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urselect/skills/quote-quote)
- [Market baseline](references/market.md)
- [Tuyulu daily quotes](https://www.tuyulu.com/daily)
- [Tuyulu public quote API base](https://www.tuyulu.com/ur/openApi/tuyulu)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown quote entries with attribution and scenario notes; optional generated image-card files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language quotation output uses a consistent Tuyulu signature and marks uncertain or AI-created material when applicable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
