## Description:

Provides self-reflection, correction logging, and tiered local memory so an agent can evaluate its work, learn from explicit feedback, and reuse confirmed patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users install this skill when they want an agent to preserve explicit corrections, preferences, and reusable execution lessons in local memory and consult them during future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can change future agent behavior and store more than intended.

Mitigation: Install only when persistent local memory is desired, and periodically inspect or delete ~/self-improving/.

Risk: Setup can propose workspace steering edits and optional companion skill installation.

Mitigation: Review proposed AGENTS.md, SOUL.md, and HEARTBEAT.md changes before enabling setup, and decline the companion skill unless its exact version is separately trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyserkazi1/skills/self-improving-100)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Setup guide](artifact/setup.md)
- [Security boundaries](artifact/boundaries.md)
- [Memory operations](artifact/operations.md)
- [Learning mechanics](artifact/learning.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local memory files under ~/self-improving/ and workspace steering updates for AGENTS.md, SOUL.md, and HEARTBEAT.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
