## Description:

OpenClaw 的信任层。在信任之前，先验证 AI 编写的代码、工具调用与研究答复——17 道确定性现实闸门 + 前沿模型评审，拥有一票否决权。免费试用，无需注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[verificate-dev](https://clawhub.ai/user/verificate-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to validate AI-generated code, plans, documentation, and research answers before accepting them. It connects the agent to Verificate's hosted MCP service for pass/reject verdicts, ordered issue lists, advisory code analysis, and validated code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected code, documentation, plans, or research answers may be sent to Verificate for remote analysis.

Mitigation: Use the skill on explicit request or narrowly scoped tasks, and avoid sending sensitive material unless third-party processing is acceptable.

Risk: The skill recommends making a third-party validation gate a persistent approval step for future agent outputs.

Mitigation: Keep persistent validation instructions opt-in, and have a human review blocked results before treating them as mandatory release gates.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/verificate-dev/skills/verificate-clawhub-skill-cn)
- [Server-Resolved GitHub Provenance](https://github.com/Verificate-Dev/verificate-clawhub-skill-cn)
- [Verificate MCP Endpoint](https://mcp.verificate.ai/mcp)
- [Verificate MCP Homepage](https://verificate.ai/mcp)
- [All Verificate Clients](https://github.com/Verificate-Dev/verificate-mcp-quickstart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with command snippets, validation verdicts, ordered issue lists, and generated or reviewed code when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a hosted MCP validation service and may return binary pass/reject decisions for validation workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
