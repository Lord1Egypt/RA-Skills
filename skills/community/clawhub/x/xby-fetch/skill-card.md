## Description:

一个模型上下文协议服务器，提供网页内容抓取功能，将HTML转换为Markdown以便于处理。适用于需要从网页提取和处理内容的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web pages through the XiaoBenYang service and convert HTML content into Markdown for downstream reading, extraction, and summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched URLs and request parameters are sent to the XiaoBenYang service.

Mitigation: Use the skill only with URLs and parameters that are appropriate to share with XiaoBenYang.

Risk: The API key may be stored in a local plaintext .env file.

Mitigation: Use a narrowly scoped API key, avoid broadly privileged credentials, and rotate or remove the local key when it is no longer needed.

Risk: Server security evidence marks the release as suspicious and recommends review before installation.

Mitigation: Review the skill and its credential handling before deployment, especially in shared or sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/xby-fetch)
- [XiaoBenYang Service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or raw HTML content returned in a structured result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential and may truncate fetched content according to max_length and start_index parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
