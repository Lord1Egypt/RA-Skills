## Description: <br>
Weixin Reader extracts readable content from WeChat Official Account article links, including the article title, author, publication date, and body text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supengchao](https://clawhub.ai/user/supengchao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to read a WeChat Official Account article from an mp.weixin.qq.com link and return the article's title, author, publication date, and main text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on extraction from external WeChat article pages, so returned content may be incomplete or affected by page access constraints. <br>
Mitigation: Review extracted title, author, publication date, and body text before relying on the result. <br>
Risk: Security evidence reports no hidden or malicious behavior, but recommends reviewing high-impact workflows before use. <br>
Mitigation: Review and scan the skill before deployment, and install it only in environments where this article-extraction workflow is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text containing extracted article metadata and body content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters irrelevant HTML, navigation, and advertising content before returning article text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
