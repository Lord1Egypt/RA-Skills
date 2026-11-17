## Description:

一个提供QAnon帖子数据集访问的MCP服务器，用于人类学和社会学研究，支持搜索、过滤和分析功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, and developers can use this skill to retrieve, search, filter, summarize, and analyze QAnon post records through the XiaoBenYang service. Use requires a XiaoBenYang API key and trust in the upstream service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a mismatch between the claimed QAnon analysis purpose and Gaokao/XiaoBenYang identifiers in the package.

Mitigation: Verify the publisher, upstream service, and actual dataset before use; require the publisher to resolve the identity mismatch before trusted deployment.

Risk: The security evidence reports that the skill stores the user's API key in a plaintext local .env file.

Mitigation: Use a dedicated low-privilege API key, avoid shared workspaces, remove the .env entry when finished, and rotate the key if exposure is possible.

Risk: The security guidance says to use this package only if the XiaoBenYang backend is trusted and notes missing output sanitization guidance.

Mitigation: Treat upstream results as untrusted content, review outputs before reuse, and avoid feeding returned text directly into sensitive downstream actions.

Risk: The security guidance recommends pinning dependencies.

Mitigation: Install in a controlled environment with reviewed, pinned dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/qanon)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summaries and structured tool results derived from upstream JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; responses depend on upstream service availability and returned data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
