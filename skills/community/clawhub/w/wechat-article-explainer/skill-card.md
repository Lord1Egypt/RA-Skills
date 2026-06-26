## Description: <br>
Explains and summarizes WeChat public account articles in plain language from user-provided mp.weixin.qq.com links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhao11235813](https://clawhub.ai/user/chenhao11235813) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch a WeChat public account article, extract its title, source, publication date, author, and content, and produce a plain-language explanation or summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching arbitrary URLs could expose private or internal content if the skill is given links outside its intended scope. <br>
Mitigation: Use only intended mp.weixin.qq.com article links and avoid private or internal URLs. <br>
Risk: The optional output path can overwrite files the process can access. <br>
Mitigation: Review the output path before execution and run the helper in a controlled working directory or virtual environment. <br>
Risk: Network fetching depends on third-party page behavior and may fail or return incomplete article content. <br>
Mitigation: Keep dependencies current, prefer the documented browser mode when needed, and ask the user to provide article text manually when fetching fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenhao11235813/wechat-article-explainer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary with optional JSON article extraction from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch network content from intended mp.weixin.qq.com article links and may write JSON to a user-specified output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
