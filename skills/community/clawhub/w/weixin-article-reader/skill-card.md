## Description: <br>
Extracts the title, author, publish date, and full body text from public Weixin official account article links on mp.weixin.qq.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricknote](https://clawhub.ai/user/ricknote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to retrieve text and basic metadata from a public Weixin article URL before returning the full article or summarizing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to user-provided Weixin article URLs. <br>
Mitigation: Use genuine mp.weixin.qq.com article links and review future versions if they add broader domains, credentials, storage, or automatic publishing behavior. <br>
Risk: Some Weixin pages may block extraction, omit publish dates, or use page structures that produce partial or empty content. <br>
Mitigation: Confirm the extracted content is non-empty before summarizing, and do not invent missing publish dates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ricknote/weixin-article-reader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ricknote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and JSON extracted article data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script returns title, author, publish_date, content, source_url, and status fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
