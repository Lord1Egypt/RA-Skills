## Description: <br>
Searches WeChat public-account articles by keyword and reads article text from mp.weixin.qq.com links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find WeChat public-account articles, read article links, and extract article titles, authors, snippets, and paragraphs for summarization, analysis, or translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches and fetches public web content, so sensitive search terms or private URLs could be exposed to external services. <br>
Mitigation: Use public mp.weixin.qq.com article URLs and avoid sensitive queries or confidential article links. <br>
Risk: The release installs unpinned Python packages and Chromium, which can change the runtime dependency set over time. <br>
Mitigation: Review and pin dependencies in the deployment environment before enabling the skill for routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/wechat-articles-cn) <br>
- [Publisher profile](https://clawhub.ai/user/onlyloveher) <br>
- [Project homepage](https://github.com/johan-oilman/wechat-articles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, and Python dictionary data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include article metadata and links; read output includes title, author, paragraphs, and the read mode used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
