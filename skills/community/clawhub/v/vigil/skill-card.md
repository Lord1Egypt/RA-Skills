## Description:

Vigil adds safety guardrails for AI agent tool calls by checking proposed shell commands, file operations, API calls, and related parameters for destructive behavior, injection, exfiltration, traversal, and credential-leak risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinoppenstam](https://clawhub.ai/user/robinoppenstam)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent builders use Vigil to validate tool calls before execution, especially for agents that run shell commands, file operations, API calls, or MCP server actions. It can also be used to audit agent activity and add a safety layer around tool-calling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external npm package vigil-agent-safety, and unpinned npm or npx usage can change what code is executed.

Mitigation: Pin vigil-agent-safety to a reviewed exact version and avoid unpinned npx execution before relying on the checker.

Risk: Tool parameters passed for policy evaluation may include sensitive data such as secrets or credentials.

Mitigation: Avoid passing secrets unless required for evaluation, and run the checker with minimal filesystem, network, and environment-variable access.

Risk: A safety wrapper can miss novel or context-specific unsafe actions even when the scanner verdict for this release is clean.

Mitigation: Use Vigil as one control in a broader review and sandboxing process for agent tool execution.

## Reference(s):

- [Vigil GitHub repository](https://github.com/hexitlabs/vigil)
- [vigil-agent-safety npm package](https://www.npmjs.com/package/vigil-agent-safety)
- [Vigil documentation](https://hexitlabs.com/vigil)
- [ClawHub skill page](https://clawhub.ai/robinoppenstam/skills/vigil)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, code snippets, shell commands, and plain-text CLI status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapper exits with status 0 for ALLOW, 1 for BLOCK, and 2 for ESCALATE.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
