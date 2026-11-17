## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory for agents that evaluate their work, catch mistakes, and improve future behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taron-ai](https://clawhub.ai/user/taron-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain local self-improvement memory for corrections, preferences, workflow lessons, and scoped project or domain patterns. It is intended for agents that should review significant work, learn from explicit feedback, and cite stored memory when behavior is affected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can shape future agent behavior in ways the user may not expect.

Mitigation: Install only when persistent behavior-changing memory is desired, review memory-driven actions, and inspect ~/self-improving/ regularly.

Risk: Workspace steering files such as AGENTS.md, SOUL.md, and HEARTBEAT.md can affect future agent behavior.

Mitigation: Review and approve proposed changes to workspace steering files before adopting them, and consider Strict mode for higher confirmation requirements.

Risk: Sensitive, third-party, or high-risk personal information could be stored if memory rules are applied carelessly.

Mitigation: Avoid storing credentials, health data, financial data, third-party information, location patterns, access patterns, and other sensitive information.

Risk: The optional Proactivity companion install may introduce separate behavior and requirements.

Mitigation: Treat the optional companion as a separate package and review it before following its setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taron-ai/skills/self-improving-1-2-16)
- [Skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local memory files under ~/self-improving/ and optionally guide changes to workspace steering files after review.]

## Skill Version(s):

1.2.16 (source: frontmatter); release package version 1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
