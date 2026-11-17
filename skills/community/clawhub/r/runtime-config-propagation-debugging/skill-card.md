## Description:

Debug settings that work in one execution path but vanish in another by tracing config resolution through every runtime entry point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug runtime configuration settings that persist in one path but disappear or are ignored in another. It guides tracing entry points, config resolution, precedence, focused tests, and live verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to inspect source, add focused tests, run builds, check logs, and execute a real request through an affected path.

Mitigation: Use an appropriate development or staging environment where possible, keep tests narrow, review planned code or configuration changes, and confirm the target entry point before live verification.

Risk: Persisted configuration or stale process state can be mistaken for the live runtime value.

Mitigation: Re-read the effective configuration and revision or hash after reload or restart, then verify the returned artifact or metadata and downstream logs before declaring success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/runtime-config-propagation-debugging)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with ordered debugging steps and verification criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No credentials, external tools, code execution hooks, or persistence are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
