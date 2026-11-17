## Description:

一个支持AI助手读取和分析PDF文件的MCP服务器，提供PDF元数据提取、页面范围阅读和关键词搜索等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent extract PDF text, inspect metadata, read selected page ranges, and search for terms in PDF files through a remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a remote Xiaobenyang service and may transmit PDF paths, URLs, and search parameters outside the local environment.

Mitigation: Use only with PDFs and queries appropriate for that provider, and review provider handling before using sensitive documents.

Risk: The skill stores XBY_APIKEY in a local plaintext .env file.

Mitigation: Keep .env out of version control, rotate exposed keys, and prefer a secure secret mechanism when available.

Risk: Server security evidence marks the release suspicious because scoping and documentation are inconsistent enough to require review before installation.

Mitigation: Review the artifact, provider, and configuration expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/read-pdf)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown summary of JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY and may send PDF paths, URLs, and search parameters to a remote Xiaobenyang API.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
