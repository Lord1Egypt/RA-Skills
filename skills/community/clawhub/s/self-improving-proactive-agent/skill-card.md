## Description:

A unified OpenClaw skill that merges self-improvement and proactivity: learn from corrections, maintain active state, recover context fast, and keep work moving with clear boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueyanc](https://clawhub.ai/user/yueyanc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an agent learn from explicit corrections, keep local task state, recover context, and make useful next-step proposals while preserving clear approval boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can capture sensitive preferences, corrections, or task details if used carelessly.

Mitigation: Avoid storing credentials, tokens, secrets, or sensitive context in memory files; review stored notes periodically.

Risk: Proactive follow-through can overstep user intent if it triggers external actions without approval.

Mitigation: Require explicit approval before sending messages, spending money, deleting data, publishing publicly, making commitments, or scheduling for others.

Risk: Incorrect or stale lessons can bias future behavior.

Mitigation: Learn only from explicit evidence, promote repeated or confirmed lessons, and ask when local state conflicts with newer instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yueyanc/skills/self-improving-proactive-agent)
- [README](artifact/README.md)
- [Boundaries](artifact/boundaries.md)
- [Learning Model](artifact/learning.md)
- [State Routing](artifact/state.md)
- [Recovery Flow](artifact/recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with local file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to maintain local memory, correction, heartbeat, and session-state files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
