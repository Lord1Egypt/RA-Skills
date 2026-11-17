## Description:

通过模型上下文协议（MCP）访问苹果官方开发者文档、框架、API及WWDC视频，支持AI驱动的自然语言查询，提供Swift/Objective-C代码示例和技术指南。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search Apple Developer Documentation, inspect API pages, explore frameworks, review platform compatibility, and retrieve WWDC session or code-example context through a third-party MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple documentation queries and the XBY API key are sent to a third-party XiaoBenYang MCP service.

Mitigation: Use the skill only when that service boundary is acceptable, and prefer a disposable or least-privilege API key.

Risk: The skill saves the XBY API key in a local .env file.

Mitigation: Treat the .env file as a local secret and avoid committing, sharing, or exposing it.

Risk: The security review describes the packaging and credential handling as under-disclosed and inconsistent.

Mitigation: Review the service boundary and credential handling before deployment.

## Reference(s):

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [XiaoBenYang API Key and Service](https://xiaobenyang.com)
- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/search-apple-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and sends documentation queries to XiaoBenYang's MCP service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
