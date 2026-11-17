## Description:

Runs the Youxinpai month-start deposit reconciliation prerequisite workflow by preparing local test inputs, triggering five Xinghe data tasks, updating SQL time ranges, and reporting the execution results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[just4learn1](https://clawhub.ai/user/just4learn1)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and data engineers use this skill to prepare Youxinpai month-start deposit reconciliation by running a required local unit test, triggering the expected Xinghe warehouse tasks, updating SQL date ranges, and reporting local, task, SQL, and cleanup outcomes. It does not replace human financial reconciliation or approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit local project files and run local test code before triggering the reconciliation workflow.

Mitigation: Require manual review of every proposed file diff, preserve original configuration values, and verify cleanup runs after success, failure, or cancellation.

Risk: The skill uses an existing internal login session to trigger data tasks and run SQL.

Mitigation: Require confirmation of the matched task rows, confirmation dialogs, SQL time-range edits, and execution target before allowing the agent to proceed.

Risk: The workflow supports real reconciliation prerequisites but does not produce a final financial reconciliation decision.

Mitigation: Use the skill only for prerequisite task triggering and status reporting, with a human owner reviewing downstream reconciliation and finance conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/just4learn1/skills/youxinpai-reconciliation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates and a reconciliation task result table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local configuration changes, unit test status, task trigger status, SQL execution status, exceptions, and cleanup results.]

## Skill Version(s):

1.0.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
