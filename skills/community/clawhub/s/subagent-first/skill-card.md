## Description:

Guides agents to delegate substantial, independent tasks to subagents while the main agent coordinates, checks results, and stays available to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users apply this Chinese-language workflow to split long research, batch, and multi-file work into subagent assignments, keep user decisions with the main agent, and verify delegated results before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegating user decisions or irreversible actions can cause unintended changes.

Mitigation: Keep approvals, deletes, payments, public posting, and other irreversible actions with the main agent and user.

Risk: Subagent reports can be incomplete or inaccurate.

Mitigation: Independently check deliverables and side effects against the original assignment before presenting them as complete.

Risk: Long-running delegated tasks may outlast the session or incur added cost.

Mitigation: Use an explicitly approved persistent job for cross-session work and weigh delegation overhead and cost before dispatch.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/subagent-first)
- [Delegation patterns](artifact/references/委派模式库.md)
- [Subagent acceptance checklist](artifact/templates/子代理验收清单.md)
- [Hermes implementation notes](artifact/references/hermes-runtime-reality.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Text or Markdown delegation plans and checklists; optional JSON task recommendations from the bundled planner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations identify work for subagents, the main agent, or a persistent background task.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release; bundled frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
