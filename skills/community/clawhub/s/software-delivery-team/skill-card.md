## Description:

Manages software delivery by designing, coding, testing, reviewing, auditing security, and releasing code with defined roles and processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate a multi-role software delivery workflow from specification through design, implementation, testing, review, security check, and release readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to edit code and run development commands.

Mitigation: Install it only in intended workspaces, give clear repository scope, and review generated changes before merging.

Risk: Release or publish steps may affect delivered software artifacts.

Mitigation: Require explicit confirmation before release or publish actions.

Risk: Workflow memory may retain task context.

Mitigation: Do not ask the skill to store credentials or unrelated private data in memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/t3ratech/skills/software-delivery-team)
- [Publisher Profile](https://clawhub.ai/user/t3ratech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, and review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to edit files, run development commands, use web access, and store workflow memory.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
