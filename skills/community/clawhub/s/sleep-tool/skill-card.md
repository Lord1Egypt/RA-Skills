## Description:

Delay execution for a specified amount of time. Use for timing in scripts, waiting between operations, and scheduling delays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to pause execution between operations or schedule simple delays in workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long sleep durations can stall an agent workflow.

Mitigation: Review requested delay values before execution and avoid long blocking waits unless the workflow explicitly requires them.

Risk: The documentation advertises duration suffixes, but the included script accepts numeric seconds only.

Mitigation: Use numeric second values directly or add wrapper logic that converts suffixes before invoking the script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/sleep-tool)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces simple sleep command usage guidance; no data files or network calls are expected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
