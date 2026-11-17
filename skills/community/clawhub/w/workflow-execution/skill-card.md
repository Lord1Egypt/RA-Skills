## Description:

Plan-first workflow for non-trivial work: plan with done criteria, create a tracking issue, package context as documents on the issue, decide where code lives, hand off to an executing agent, verify completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan, track, package, hand off, execute, and verify non-trivial work with explicit done criteria and durable context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to create or update public tracker records, branches, PRs, local plan files, and agent handoffs when the task may not need that level of process.

Mitigation: Use the local-file fallback or narrow the workflow when public tracker updates or agent handoffs are unnecessary, and review proposed tracker or PR actions before execution.

Risk: Local-file tracking may provide weaker revision history and coordination than a shared tracker.

Mitigation: Use a shared issue tracker for multi-agent or long-running work, or commit local plans when durable history is needed.

## Reference(s):

- [Workflow Execution Skill Page](https://clawhub.ai/levineam/skills/workflow-execution)
- [Tracker Reference: GitHub Issues](references/tracker-github.md)
- [Tracker Reference: None (Local Files)](references/tracker-none.md)
- [Tracker Reference: Paperclip](references/tracker-paperclip.md)
- [Paperclip](https://paperclip.ing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and tracker request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions, planning/checklist structures, tracker-specific references, and verification guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
