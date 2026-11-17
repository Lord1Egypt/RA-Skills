## Description:

Synapse Layer provides persistent memory infrastructure for AI agents with a 4-layer Cognitive Security Pipeline covering PII redaction, AES-256-GCM encryption, intent validation, and differential privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to configure SynapseLayer memory integration, store and retrieve agent memories, share memory across agents, and troubleshoot connectivity and trust scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores or processes agent memory through a remote SynapseLayer service.

Mitigation: Use it only when remote memory processing is intended, and avoid sending secrets or regulated personal data.

Risk: Published privacy and zero-knowledge claims are not proven by the included client implementation.

Mitigation: Do not rely on those claims unless the publisher provides implementation evidence and security review.

Risk: Cross-agent search can expose memories outside the intended agent scope.

Mitigation: Restrict cross-agent search to authorized scopes and use consistent, least-privilege agent identifiers.

Risk: The test script exercises live memory operations and may run with real credentials.

Mitigation: Run tests only with non-production credentials and non-sensitive test memories.

## Reference(s):

- [API Reference](references/api.md)
- [Security Details](references/security.md)
- [Framework Integrations](references/integrations.md)
- [SynapseLayer MCP endpoint](https://forge.synapselayer.org/mcp)
- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/synapse-layer)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-call guidance for a remote memory service and configuration snippets for MCP or Python SDK integration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
