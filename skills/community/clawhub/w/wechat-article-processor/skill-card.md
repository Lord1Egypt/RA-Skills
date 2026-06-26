## Description: <br>
微信公众号文章处理器会抓取用户提供的公众号文章链接，提取标题、作者、时间和正文，整理为 Markdown，并保存到飞书云文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyaryyj](https://clawhub.ai/user/hoyaryyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn trusted WeChat public-account article links into structured Feishu documents with article metadata, summary, and main content preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A matching WeChat article link may cause the agent to create a Feishu cloud document without a separate confirmation step. <br>
Mitigation: Use the skill only in workflows where creating a Feishu document from a provided article link is expected, and require a user confirmation step if document creation should be gated. <br>
Risk: WeChat articles can contain sensitive, copyrighted, login-gated, or otherwise restricted content. <br>
Mitigation: Process only trusted links and avoid sensitive or login-gated content unless the user has authorization to access and save it. <br>
Risk: Captcha, login prompts, or incomplete browser extraction can lead to partial article content. <br>
Mitigation: Ask the user to provide the article text manually when access controls prevent reliable extraction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoyaryyj/wechat-article-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Code] <br>
**Output Format:** [Structured Markdown content saved to a Feishu cloud document, with a returned document link or guidance when manual access is required.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser access to the WeChat article and Feishu authorization; login-gated articles or captcha challenges may require manual user input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
