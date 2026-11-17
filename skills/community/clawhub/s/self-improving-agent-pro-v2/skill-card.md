## Description:

Universal self-improving AI agent framework for self-correction, continuous learning, persistent memory, autonomous upgrades, self-reflection, reasoning verification, and decision verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-heartflow](https://clawhub.ai/user/mark-heartflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add self-correction, decision verification, persistent memory, reflection, and controlled continuous-learning behavior to AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global identity and priority instructions may influence host-agent behavior beyond the intended task.

Mitigation: Review and scope or disable global identity and priority instructions before enabling the skill in a production agent.

Risk: Persistent memory, continuous learning, and rule-generation behavior may carry incorrect or unwanted changes across sessions.

Mitigation: Gate learning and self-upgrade flows, inspect generated memories or rules, and provide reset and retention controls.

Risk: Setup flows may store credentials in ways that are not appropriate for sensitive API keys.

Mitigation: Avoid entering API keys into the setup wizard unless credential handling is changed to use an approved secret store.

Risk: Maintenance and upgrade scripts can alter agent behavior or local files when run.

Mitigation: Run maintenance scripts only in an isolated environment with explicit review and approval.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mark-heartflow/skills/self-improving-agent-pro-v2)
- [Verification methodology](references/verification-methodology.md)
- [RL closed loop](references/rl-closed-loop.md)
- [Memory system comparison](references/memory-system-comparison.md)
- [Reflexion](https://arxiv.org/abs/2308.07915)
- [Self-Verification](https://arxiv.org/abs/2312.09210)
- [CRITIC](https://arxiv.org/abs/2312.04445)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, JavaScript/CommonJS modules, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stateful behavior can persist memory, generated rules, and agent policy changes across sessions when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
