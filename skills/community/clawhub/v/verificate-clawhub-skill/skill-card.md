## Description:

The trust layer for OpenClaw. Verify AI-written code, tool calls and research answers before you trust them \u2014 17 deterministic reality gates + a frontier-model review with veto power. Free to try, no signup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[verificate-dev](https://clawhub.ai/user/verificate-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Verificate to validate AI-written code, plans, documents, tool calls, and research answers before treating them as complete. It can also analyze code for performance, scalability, and failure modes or generate code behind a validation gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends work being validated to Verificate's hosted service.

Mitigation: Use it only for content approved for external validation, and avoid sending private code, internal documents, credentials, or sensitive plans unless that use is authorized.

Risk: The skill recommends making the hosted validation service a persistent gate over future agent work.

Mitigation: Prefer invoking validation explicitly per task, especially when working with sensitive or confidential material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/verificate-dev/skills/verificate-clawhub-skill)
- [Server-resolved source repository](https://github.com/Verificate-Dev/verificate-clawhub-skill)
- [Verificate MCP homepage](https://verificate.ai/mcp)
- [Verificate MCP server](https://mcp.verificate.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown validation results, advisory analysis, configuration snippets, and generated code when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation results may include binary approve or reject decisions with severity-ranked findings; code analysis is advisory and non-blocking.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
