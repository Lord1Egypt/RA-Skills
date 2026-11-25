## Description:

Creates an independent branch of a work in progress by copying session context while leaving workspace artifacts in their current state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamingmou](https://clawhub.ai/user/yamingmou)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use the skill to branch work in supported coding assistants, carry forward selected conversation context, and continue an alternate path independently. Workspace files remain in their current state unless managed separately with version control or backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scanning reports concerns that forking may lose or alter conversation history or affect original sessions; the scan was partial.

Mitigation: Follow the scan guidance and avoid installation until the reported session-history and original-session integrity concerns are resolved.

Risk: A fork copies session context but does not restore workspace files or undo external actions, which can leave the branch context out of sync with current artifacts.

Mitigation: Check the working tree and preserve needed versions or backups before branching when artifacts must match the fork point.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yamingmou/skills/session-fork)
- [English usage overview](https://github.com/yamingmou/session-fork-core/blob/main/README.en.md)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Forked session snapshot with a short status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies session context; workspace artifacts remain in their current state.]

## Skill Version(s):

2.4.24 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
