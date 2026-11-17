## Description:

Solo CEO coordinates multiple worker agents by planning work, delegating tasks, collecting results, and summarizing the final outcome for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moistenxx](https://clawhub.ai/user/moistenxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and solo builders use this skill to have a main CEO agent break multi-step work into parallel or sequential tasks, delegate to persistent or temporary worker agents, and consolidate worker reports into a final response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Worker MEMORY.md files may retain sensitive task, customer, or project context.

Mitigation: Use the skill only where persistent worker memory is acceptable, and periodically inspect or clear worker MEMORY.md files.

Risk: Delegating work to spawned agents can spread confidential context beyond the main agent conversation.

Mitigation: Review tasks before delegation and avoid using the skill with regulated or confidential information unless the worker environments are approved for that data.

Risk: Persistent plan files may preserve task details after completion.

Mitigation: Store plans only in approved workspaces and remove plan files when the task no longer requires them.

## Reference(s):

- [Employee SOUL template](artifact/references/employee_soul_template.md)
- [Task plan template](artifact/references/plan_template.md)
- [ClawHub skill page](https://clawhub.ai/moistenxx/skills/solo-ceo)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with configuration snippets and agent delegation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent plan files and instruct worker agents to read or update MEMORY.md files.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
