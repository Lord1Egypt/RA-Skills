## Description: <br>
Reads WeChat Official Account article links from mp.weixin.qq.com and extracts the full article text, including title, author, publication date, and cleaned body content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reknottycat](https://clawhub.ai/user/reknottycat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to read user-provided public WeChat Official Account article URLs and return the article's title, author, publication date, and cleaned body text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-provided article URLs and returns page content, which may include private, paywalled, or account-restricted material if such URLs are supplied. <br>
Mitigation: Use it with explicit public mp.weixin.qq.com URLs and avoid sending private, paywalled, or account-restricted content unless the user is comfortable with the agent processing that page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reknottycat/weixin-reader-oc-local) <br>
- [Publisher profile](https://clawhub.ai/user/reknottycat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text containing extracted article metadata and body content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns cleaned text from a user-provided mp.weixin.qq.com article URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
