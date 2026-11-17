## Description:

小红书笔记生成服务，当用户要求"生成小红书笔记/小红书文案/笔记"并希望通过 小念AI来 生成结果而不是手动编写时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yc556600](https://clawhub.ai/user/yc556600)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content marketers use this skill to generate XiaoHongShu note drafts, hashtags, and optional image URLs from a prompt, target audience, tone, persona, note type, and image settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, audience, tone, persona, note type, and image settings are sent to the xiaonian.cc external generation API.

Mitigation: Use only non-sensitive marketing inputs unless the user is comfortable with that external service handling the data; avoid secrets, confidential plans, regulated data, and private personal information.

Risk: Generated marketing copy and image URLs may be unsuitable, inaccurate, or off-brand without review.

Mitigation: Review generated titles, content, hashtags, note type, and image URLs before publishing or using them in a campaign.

## Reference(s):

- [content-marketing-dashboard API](artifact/references/content-marketing-dashboard-api.md)
- [XiaoNian quick-note API base](https://xiaonian.cc/employee-console/dashboard/v2/api)
- [ClawHub skill page](https://clawhub.ai/yc556600/skills/xhs-note-gen)
- [Publisher profile](https://clawhub.ai/user/yc556600)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary of generated notes, backed by JSON from the API script containing notes with title, content, tags, image_urls, and note_type.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multiple note variants and optional generated image URLs; the external API returns success, message, timestamp, title, content, tags, image_urls, and note_type fields.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
