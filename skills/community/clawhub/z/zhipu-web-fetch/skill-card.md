## Description:

Zhipu Web Fetch fetches a specific web page URL through Zhipu AI's Reader API and returns parsed content as Markdown or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch a specific web page by URL and convert it to Markdown or plain text with optional metadata, image, cache, and summary controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and retrieval requests are sent to Zhipu's service under the configured API key.

Mitigation: Use only URLs appropriate for external processing, and avoid confidential intranet pages, localhost or cloud-metadata targets, authenticated links, and pre-signed URLs.

Risk: The wrapper script has weak input validation for option values.

Mitigation: Pass only trusted option values and review generated requests before using the wrapper in automated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whyhit2005/skills/zhipu-web-fetch)
- [Publisher Profile](https://clawhub.ai/user/whyhit2005)
- [Zhipu Reader API Endpoint](https://open.bigmodel.cn/api/paas/v4/reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON responses containing parsed Markdown or plain text, with shell command examples for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY and curl; the requested URL is sent to Zhipu's Reader API.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
