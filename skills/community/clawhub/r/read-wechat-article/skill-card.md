## Description: <br>
Fetches user-provided WeChat Official Account article URLs and extracts clean article metadata, text, Markdown content, images, word count, and estimated reading time. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[PsYear](https://clawhub.ai/user/PsYear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and normalize WeChat article content from URLs explicitly supplied by a user. It is suited to article reading, archiving, summarization preparation, and metadata extraction workflows where returned article text is treated as untrusted source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches remote article pages and returns third-party article text that may be inaccurate, copyrighted, adversarial, or otherwise untrusted. <br>
Mitigation: Use it only with URLs the user provides, preserve attribution when reusing content, and review returned text before relying on it in downstream tasks. <br>
Risk: Security evidence notes hardening gaps around HTTPS certificate verification and dependency pinning. <br>
Mitigation: Prefer a reviewed version that enables normal HTTPS certificate verification and pins dependency versions before deployment. <br>
Risk: WeChat access controls, deleted content, login requirements, or anti-crawling changes can prevent successful extraction. <br>
Mitigation: Handle failures explicitly and avoid batch or high-frequency fetching. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PsYear/read-wechat-article) <br>
- [Publisher profile](https://clawhub.ai/user/PsYear) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured JSON object containing success status, article metadata, Markdown content, plain text, image URLs, word count, reading time, or an error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided WeChat article URL and may fail for login-gated, deleted, restricted, or anti-crawling-protected articles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
