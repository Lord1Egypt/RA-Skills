## Description:

Helps agents pursue user-defined goals through evidence-based milestones, iterative execution, progress tracking, and optional cross-session continuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can turn a goal into measurable success criteria, plan and execute steps, check evidence, and maintain a progress ledger until completion or a stop condition. Optional heartbeat scheduling supports continuation across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The progress ledger may be written to an unintended location.

Mitigation: Agree on the ledger path before starting and review where progress is stored.

Risk: Goal execution can include file changes, external actions, or spending.

Mitigation: Keep strict confirmation enabled unless you deliberately pre-authorize a specific list of sensitive actions.

Risk: Optional heartbeat continuation may keep acting across sessions.

Mitigation: Enable it only when needed, confirm its schedule and deadline, and stop it when the goal changes or ends.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wangjiaocheng/skills/relentless-goal-executor)
- [Goal execution task catalog](artifact/references/relentless-goal-catalog.md)
- [Goal execution requirements](artifact/references/relentless-goal-requirements.md)
- [Progress ledger template](artifact/templates/goal-ledger-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Configuration instructions]

**Output Format:** [Markdown plans, evidence checks, progress ledgers, and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can maintain a ledger and propose optional heartbeat scheduling when supported and authorized.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
