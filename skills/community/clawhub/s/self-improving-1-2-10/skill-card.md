## Description:

Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiyi-9](https://clawhub.ai/user/yiyi-9)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to maintain local cross-session memory of explicit corrections, self-reflections, preferences, and reusable workflow lessons so future work can adapt to confirmed patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable agent-wide memory can persist incorrect or unwanted behavior across sessions.

Mitigation: Review proposed AGENTS.md, SOUL.md, and HEARTBEAT.md changes before deployment and prefer strict confirmation mode.

Risk: Local memory can capture sensitive, proprietary, or third-party details if used carelessly.

Mitigation: Do not store credentials, financial data, medical data, biometric data, third-party information, location patterns, or access patterns.

Risk: Automatic memory writes can make agent behavior depend on hidden or stale local state.

Mitigation: Require source tracking, support audit and export on demand, confirm deletions, and check permissions on ~/self-improving/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiyi-9/skills/self-improving-1-2-10)
- [Skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local memory files under ~/self-improving/ and may propose AGENTS.md, SOUL.md, and HEARTBEAT.md configuration changes.]

## Skill Version(s):

1.2.10 (source: artifact/SKILL.md frontmatter); release 1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
