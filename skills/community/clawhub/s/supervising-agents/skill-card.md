## Description:

Use when YOU are dispatching tasks to subagents (Agent tool, openclaw, parallel workers). You become the supervisor by default. This skill guides how to monitor, intervene, and verify your subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenclove](https://clawhub.ai/user/allenclove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to supervise delegated AI subagent work through a prepare, dispatch, monitor, verify, and report workflow. It supports active progress checks, intervention when work drifts or stalls, and evidence-based verification before reporting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run verification commands chosen for a delegated task.

Mitigation: Review task-specific commands before execution and keep normal command-execution safeguards in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenclove/skills/supervising-agents)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with checklists, prompt templates, command examples, and reporting templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces supervision procedures and verification guidance; it does not run hidden code or require credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
