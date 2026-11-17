## Description:

Read Yuque documents in AI clients via MCP protocol, including rendered content, Markdown conversion, and knowledge base document listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy8663](https://clawhub.ai/user/andy8663)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-client users use this skill to let agents read Yuque technical documents, product requirements, meeting notes, and knowledge base trees without manual copy-paste. It also supports converting Yuque documents to Markdown for downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Yuque session cookie can expose account and document access if it is copied into chats, screenshots, repositories, or shared configuration.

Mitigation: Treat `_yuque_session` and `YUQUE_SESSION` like passwords, keep them out of shared material, prefer a scoped read-only credential if Yuque supports one, and rotate or log out the session if exposure is possible.

Risk: The MCP client runs external code that can read Yuque documents using the provided session credential.

Mitigation: Install only after trusting the package source and MCP client, and review the MCP configuration before enabling the tool.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/andy8663/yuque-mcp-tool)
- [ClawHub skill page](https://clawhub.ai/andy8663/skills/yuque-mcp-tool)
- [Yuque documentation platform](https://www.yuque.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Rendered document text, Markdown, document listings, and MCP client configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yuque session cookie for authenticated document access; optional Playwright rendering may be used for JavaScript-rendered pages.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
