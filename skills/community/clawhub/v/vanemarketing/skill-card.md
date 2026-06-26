## Description: <br>
AI 智能品牌营销工具：输入品牌名称，自动采集全网数据、分析当日热点、生成小红书图文内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongxiaoke](https://clawhub.ai/user/dongxiaoke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers and content creators use this skill to turn a brand name into Xiaohongshu-style marketing content by combining brand analysis with current hot topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a billable App-Key in chat, and successful requests spend 100 credits. <br>
Mitigation: Use a revocable, low-scope key, confirm the balance and expected charge before generation, and avoid pasting reusable secrets into retained chat transcripts. <br>
Risk: The production content endpoint is unclear in the artifact, which shows a localhost base URL placeholder. <br>
Mitigation: Verify the real production endpoint and service identity before sending credentials or brand data. <br>
Risk: Generated marketing content may be inaccurate, unsuitable for the brand, or risky to publish automatically on Xiaohongshu. <br>
Mitigation: Review and edit generated copy manually, and publish through the official Xiaohongshu app rather than automated posting unless the user explicitly accepts platform-account risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongxiaoke/vanemarketing) <br>
- [智灵 Skill 平台](https://skills.zeelin.cn) <br>
- [智灵 App console](https://skills.zeelin.cn/console/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown with generated title, body copy, tags, image links, status messages, and balance details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful content generation spends 100 credits and may include service-returned images or links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
