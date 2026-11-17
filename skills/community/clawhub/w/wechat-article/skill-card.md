## Description:

Fetches WeChat public-account articles, extracts titles and content, and outputs the result as Markdown using multiple extraction methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haweiyu](https://clawhub.ai/user/haweiyu)

### License/Terms of Use:


## Use Case:

Developers, content operators, and external users use this skill to convert public WeChat article links into Markdown for review, archiving, or downstream editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL checks can allow crafted inputs to trigger requests to unintended internal or private addresses.

Mitigation: Review before use in environments with private networks, cloud metadata services, intranet applications, or sensitive URLs; use only trusted WeChat article URLs.

Risk: URL handling does not prove that the final request target is the exact public WeChat article host.

Mitigation: Prefer an update that parses URLs, allowlists the exact mp.weixin.qq.com hostname, and blocks redirects to private addresses.

Risk: The extraction flow may send article URLs through r.jina.ai.

Mitigation: Clearly disclose r.jina.ai data sharing and use the skill only with URLs approved for that processing path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haweiyu/skills/wechat-article)
- [r.jina.ai reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown article content or concise error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and network access; no credential environment variables are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
