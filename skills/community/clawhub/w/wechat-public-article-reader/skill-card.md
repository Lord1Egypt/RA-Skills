## Description: <br>
Reads public WeChat Official Account article links and returns the title, account name, publication time, article text, image link markers, and source URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianen](https://clawhub.ai/user/ianen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch and extract readable content from public mp.weixin.qq.com article URLs for summarization, translation, analysis, or review. It is not intended to search WeChat accounts, browse historical article lists, or access login-only content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loose URL validation can allow crafted inputs that are not genuine WeChat article URLs to be fetched. <br>
Mitigation: Use only known-good https://mp.weixin.qq.com/s/... links and prefer an update that parses the URL and requires the hostname to be exactly mp.weixin.qq.com before any network request. <br>
Risk: The skill performs outbound HTTP fetching from the local environment. <br>
Mitigation: Install and run it only in environments where outbound requests to supplied article URLs are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianen/wechat-public-article-reader) <br>
- [Publisher profile](https://clawhub.ai/user/ianen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON produced by a local Python script, typically relayed in Markdown by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes original URL, title, author, publication time, extracted content, and image links marked inline when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
