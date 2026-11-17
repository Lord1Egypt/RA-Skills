## Description:

Accepts causal relationship graphs, detects cycle dependencies and dangling nodes, and returns correction suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to submit causal graph data for debugging, receive cycle and dangling-node analysis, and get repair suggestions and a health score before downstream causal audit or risk workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Causal graph contents and an agent name may be sent to an external service without clear privacy, retention, or deletion terms.

Mitigation: Use only non-confidential graphs unless the publisher provides a trusted endpoint, individual credentials, and clear data-handling terms.

Risk: The artifact documents a shared public API key for access.

Mitigation: Treat public-key access as unsuitable for sensitive or operational use and obtain individual credentials before deployment.

Risk: Automated repair suggestions can alter causal assumptions in downstream workflows.

Mitigation: Review proposed graph changes with a domain owner before applying them to audit, risk, or decision workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/skills/v19-early-causal-graph-debugger)
- [V19 Trust Manifesto v1.1.0](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Shell commands]

**Output Format:** [JSON responses with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected cycles, dangling-node findings, repair suggestions, and a graph health score.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
