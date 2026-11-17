## Description:

Fetches public WeChat article content, including title, author, publish time, account name, body text, URL, and optional raw HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvzaiyi-afk](https://clawhub.ai/user/lvzaiyi-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, summarize, analyze, or archive public WeChat articles from supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests to any user-supplied URL rather than only WeChat article URLs.

Mitigation: Use only trusted public WeChat article URLs, preferably in an isolated environment, and validate URLs to https://mp.weixin.qq.com before use.

Risk: Raw HTML output may expose untrusted page content when enabled.

Mitigation: Keep raw HTML output disabled unless needed, and do not render or execute returned HTML.

Risk: Dependencies are not pinned in the artifact instructions.

Mitigation: Install reviewed, pinned versions of requests and beautifulsoup4 in a controlled environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lvzaiyi-afk/skills/wechat-article-fetch)

## Skill Output:

**Output Type(s):** [Text, Structured data, Guidance]

**Output Format:** [Plain text summaries and JSON-like article metadata dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include optional raw HTML when explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact documentation notes 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
