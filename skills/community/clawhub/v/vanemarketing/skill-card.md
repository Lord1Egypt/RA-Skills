## Description:

AI 智能品牌营销工具：输入品牌名称，自动采集全网数据、分析当日热点、生成小红书图文内容

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongxiaoke](https://clawhub.ai/user/dongxiaoke)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketers and content teams use this skill to validate paid access, analyze a brand against current hot topics, and generate Xiaohongshu-style post titles, body copy, image suggestions, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide an App-Key and brand names for provider-side processing.

Mitigation: Install only if that data sharing is acceptable, and avoid pasting long-lived credentials into ordinary chat when possible.

Risk: The instructions include a real-looking example App-Key.

Mitigation: Treat the example key as unsafe, replace it with placeholders in operational copies, and rotate any credential that may have been exposed.

Risk: The content-generation example uses a localhost HTTP endpoint while the security guidance says to confirm the real HTTPS endpoint before use.

Mitigation: Verify the production HTTPS endpoint with the publisher before sending credentials or brand data.

Risk: Automated posting to Xiaohongshu can create account or content enforcement risk.

Mitigation: Use the generated copy manually in the Xiaohongshu app unless the user has separately accepted the platform-policy risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongxiaoke/skills/vanemarketing)
- [ClawHub publisher profile](https://clawhub.ai/user/dongxiaoke)
- [Zeelin Skill platform](https://skills.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with generated marketing copy, structured result summaries, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates Xiaohongshu-style titles, post body text, image URL suggestions, tags, balance/cost status, and publishing-risk reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
