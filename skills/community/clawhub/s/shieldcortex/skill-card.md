## Description:

Memory and defence for AI agents: semantic recall, knowledge graph and decay, plus a memory firewall that scans and enforces against prompt injection, credential leaks and poisoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using AI agents use ShieldCortex to retain searchable memory across sessions and scan for prompt injection, credential leakage, and poisoned content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence and reports unpinned package downloads and execution, changes outside the declared write scope, and access to agent and MCP configuration paths; reference resolution is incomplete.

Mitigation: Review the agent and MCP configuration handling, package execution, and automatic hook changes before installing. Proceed only if those behaviors fit your needs and you trust the publisher.

## Reference(s):

- [ShieldCortex documentation](https://shieldcortex.ai/docs)
- [ShieldCortex npm package](https://www.npmjs.com/package/shieldcortex)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [MCP text and structured results, CLI text, and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first memory and security results; cloud sync is optional.]

## Skill Version(s):

5.20.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
