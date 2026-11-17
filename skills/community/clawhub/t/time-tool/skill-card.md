## Description:

Measures command execution time for performance benchmarking, script optimization, and timing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a command and view elapsed timing information while benchmarking commands, optimizing scripts, or comparing performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timed commands execute with the same practical caution required for running those commands directly, including commands that change files, use credentials, or access the network.

Mitigation: Review each command before timing it and run only commands that are appropriate for the workspace and credentials available to the agent.

## Reference(s):

- [Time Tool on ClawHub](https://clawhub.ai/dinghaibin/skills/time-tool)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text timing summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports elapsed wall-clock time for the supplied command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
