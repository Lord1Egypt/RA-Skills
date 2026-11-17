## Description:

一个支持多种命理系统（紫微斗数、八字等）的MCP协议服务器，为AI工具提供命理分析与运势查询功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route fortune-analysis requests to XiaoBenYang tools for Zi Wei Dou Shu charts, Ba Zi charts, fortune queries, palace analysis, and five-element analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XBY API key in a local plaintext .env file.

Mitigation: Use only an API key that is acceptable for local plaintext storage and avoid installing the skill in shared or untrusted working directories.

Risk: The skill can send birth time, gender, location, credentials, and fortune-analysis inputs to a configurable remote endpoint.

Mitigation: Review the configured endpoint before use and avoid submitting sensitive personal data unless the user accepts the remote-service exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-mingli)
- [ClawHub publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key and service site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown or structured text summarizing JSON returned by the remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key before tool calls can succeed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
