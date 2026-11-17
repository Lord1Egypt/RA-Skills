## Description:

Self-reflection, self-criticism, self-learning, and self-organizing local memory for agents that need to evaluate their work, catch mistakes, and improve across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reknottycat](https://clawhub.ai/user/reknottycat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain local, cross-session memory about corrections, preferences, reusable workflow lessons, and self-reflection outcomes. It is suited for agents that should preserve execution-quality lessons while exposing memory contents and deletion controls to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can turn corrections into cross-session steering that may be stale, unintended, or sensitive.

Mitigation: Use Strict mode for sensitive work, avoid storing secrets or personal data, review ~/self-improving/ regularly, and use the forget or export flows when memory should be removed or audited.

Risk: The optional Proactivity companion install may add another skill after setup.

Mitigation: Skip the optional install unless the user explicitly agrees after reviewing the exact package and version.

Risk: Incorrect or overbroad learned rules can influence future agent behavior.

Mitigation: Keep inferred lessons tentative until confirmed, cite memory sources when applying rules, and prefer project- or domain-scoped storage over global rules when scope is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reknottycat/skills/self-improving-local)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Setup guide](setup.md)
- [Security boundaries](boundaries.md)
- [Memory operations](operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and workspace steering guidance under user-controlled setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
