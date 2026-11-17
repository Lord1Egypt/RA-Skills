## Description:

Set up and coordinate multi-agent teams with defined roles, task workflows, handoff protocols, and quality review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amdf01-debug](https://clawhub.ai/user/amdf01-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-team operators use this skill to define roles, route tasks, manage handoffs, maintain shared state, and apply quality gates for multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unclear task boundaries or acceptance criteria can lead agents to route, execute, or review work inconsistently.

Mitigation: Define one task per agent, include explicit acceptance criteria in task briefs, and apply quality gates before delivery.

Risk: Shared state can be misplaced or become stale across agent restarts.

Mitigation: Choose a deliberate shared-state file location and require handoff briefs to include current context and artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amdf01-debug/skills/sw-agent-team-orch)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured role, task lifecycle, handoff, and quality gate templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role definitions, task briefs, handoff protocols, quality checklists, and shared-state conventions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
