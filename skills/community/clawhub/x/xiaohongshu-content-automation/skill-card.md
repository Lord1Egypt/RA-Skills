## Description: <br>
小红书内容创作自动化工作流，从选题、撰写、排版到发布的一站式自动化方案，帮助你快速产出高质量小红书内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiatian5](https://clawhub.ai/user/xiatian5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, and agent users use this skill to plan, draft, optimize, hashtag, and format Xiaohongshu posts. It supports copy-ready post output and delegates any browser-based publishing to separate automation skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing workflows can act on a logged-in Xiaohongshu account when paired with browser automation. <br>
Mitigation: Confirm each post manually and grant account or session access only when the agent is intended to act on that account. <br>
Risk: The skill prepares social content, but automated publishing behavior is handled by separate skills outside this artifact. <br>
Mitigation: Review the separate browser automation and Xiaohongshu skills before enabling any auto-publish path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiatian5/xiaohongshu-content-automation) <br>
- [xiaohongshu-cn related skill](https://clawhub.ai/skills/xiaohongshu-cn) <br>
- [playwright-browser-automation related skill](https://clawhub.ai/skills/playwright-browser-automation) <br>
- [copywriting related skill](https://clawhub.ai/skills/copywriting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted Chinese social post drafts, title options, hashtags, topic ideas, and publishing preparation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Content is intended for manual review before publishing; automatic posting is delegated to separate browser automation skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
