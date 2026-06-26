## Description: <br>
社交媒体爆款内容创作工具。一键生成高互动文案 + 3:4 视觉封面，专为小红书/抖音/视频号设计。支持 AI 科技、产品评测、工具对比等主题，自动输出带话题标签的完整发布内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javastarboy](https://clawhub.ai/user/javastarboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and marketing teams use this skill to generate short Chinese social-media copy, hashtags, interaction prompts, and matching 3:4 HTML cover pages for platforms such as Xiaohongshu, Douyin, and WeChat Channels. It is especially oriented toward AI technology, product comparison, and tool-review topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local HTML cover files in an output folder. <br>
Mitigation: Confirm the target output directory before running the skill and review generated files before sharing or publishing them. <br>
Risk: The skill may ask the agent to open the output folder after generation. <br>
Mitigation: Tell the agent to skip folder-opening commands unless you want the local UI action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javastarboy/social-creator) <br>
- [Copywriting guide](references/copywriting-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown response with social copy, local HTML files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local cover-page files in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
