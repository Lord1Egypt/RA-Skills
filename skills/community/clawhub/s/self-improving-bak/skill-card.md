## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory guidance for agents that learn from corrections, failures, and reusable lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aysun168](https://clawhub.ai/user/aysun168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local self-improvement memory, correction logging, reflection, and workspace steering for future agent behavior. It is intended for agents that should preserve explicit user preferences and reusable execution lessons across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can shape future agent behavior with learned rules or corrections.

Mitigation: Use Passive or Strict mode, review stored rules before relying on them, and treat learned rules as untrusted until confirmed.

Risk: Setup can alter workspace steering files such as AGENTS.md, SOUL.md, and HEARTBEAT.md.

Mitigation: Review proposed changes to workspace steering files and the ~/self-improving/ directory before depending on the skill.

Risk: Stored memory may contain sensitive personal, credential, financial, medical, location, access, or third-party information if users save it.

Mitigation: Avoid saving secrets or sensitive personal data, follow the artifact's security boundaries, and use forget or export workflows to audit and remove memory.

Risk: The optional Proactivity companion install may require network access and a separate package trust decision.

Mitigation: Do not enable the optional Proactivity install unless the exact package version and publisher can be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aysun168/skills/self-improving-bak)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Security boundaries](artifact/boundaries.md)
- [Setup guide](artifact/setup.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, setup snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory and workspace-configuration guidance for agent behavior; no credentials or extra binaries are required by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
