## Description: <br>
Reads article text from WeChat Official Account pages on mp.weixin.qq.com for extraction, summarization, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcwatergm-afk](https://clawhub.ai/user/lcwatergm-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a WeChat article URL and needs the article body extracted for review, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that a crafted URL can trigger unintended shell command execution. <br>
Mitigation: Before routine use, replace shell=True with a safe HTTP client or a subprocess argument list and accept only HTTPS mp.weixin.qq.com URLs. <br>
Risk: The skill depends on outbound network access and a local HTML parsing dependency. <br>
Mitigation: Document the network and beautifulsoup4 requirements and review fetched content before relying on extracted text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lcwatergm-afk/weixin-article-read) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Plain text or Markdown article content emitted by a Python command-line script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to mp.weixin.qq.com and the beautifulsoup4 Python dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
