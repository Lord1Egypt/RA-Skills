## Description: <br>
Fetches and extracts public WeChat article titles, authors, publish times, account names, and cleaned article text from user-provided mp.weixin.qq.com URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvzaiyi-afk](https://clawhub.ai/user/lvzaiyi-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve WeChat public article text and metadata for reading, summarization, analysis, or archiving. It is intended for user-provided public article URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes HTTP requests to article URLs provided by the user. <br>
Mitigation: Use public WeChat article links only, and apply normal network review controls before running it in sensitive environments. <br>
Risk: Optional raw HTML output can include markup fetched from the remote article page. <br>
Mitigation: Prefer cleaned text and metadata outputs unless raw HTML is needed, and review raw HTML before storing it or passing it to downstream tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvzaiyi-afk/wechat-article-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python dictionary data, plain text article content, and Markdown/code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include remote page HTML when raw HTML output is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
