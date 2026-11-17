## Description:

Create an independent branch from a session's history so work can continue from an earlier point, while workspace files remain in their current state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamingmou](https://clawhub.ai/user/yamingmou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use the skill to branch an in-progress conversation or task and continue from a chosen point without changing the original session. Workspace files remain at their current state unless they have their own version history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WorkBuddy repair mode may alter original conversations, including when used with --dry-run.

Mitigation: Avoid WorkBuddy --fix, including with --dry-run, until its safeguards are corrected.

Risk: A copied session may omit referenced Codex history or malformed entries even when verification succeeds.

Mitigation: Back up application session data independently, select an explicit source session ID, and inspect the copied history before resuming.

Risk: Live application compatibility for this version remains unverified.

Mitigation: Review this version before using it on important conversations.

## Reference(s):

- [Session Fork English overview](https://github.com/yamingmou/session-fork-core/blob/main/README.en.md)
- [Session Fork Chinese overview](https://github.com/yamingmou/session-fork-core/blob/main/README.md)
- [Session Fork project repository](https://github.com/yamingmou/session-fork-core)
- [ClawHub skill page](https://clawhub.ai/yamingmou/skills/session-fork)

## Skill Output:

**Output Type(s):** [Session branch, Text]

**Output Format:** [A new session branch with a concise creation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The branch copies session history through the selected cutoff; workspace files and external actions are not reverted.]

## Skill Version(s):

2.4.23 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
