## Description:

Summarizes WeChat Official Account articles from mp.weixin.qq.com links and produces concise Chinese summaries of the article's main points, data, conclusions, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mick2458pan](https://clawhub.ai/user/mick2458pan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quickly understand WeChat Official Account articles by extracting article content and generating concise Chinese summaries. It is optimized for mp.weixin.qq.com links and can fall back to a Python fetcher when direct web extraction fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback fetcher can retrieve arbitrary user-supplied URLs from the agent environment.

Mitigation: Restrict use to HTTPS WeChat article URLs, validate redirects, block private and metadata IP ranges, and disclose or ask before using the Python fallback.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown Chinese summary, with optional shell command for fallback article retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are adjusted by article length and may include key data, conclusions, timing information, and action recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
