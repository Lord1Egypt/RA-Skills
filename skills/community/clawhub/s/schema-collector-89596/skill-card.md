## Description:

Sends a liveness heartbeat so a dashboard can show schema-collector-89596 as online.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to report a tool's liveness to a local dashboard daemon and check whether its heartbeat was received.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The heartbeat connects to a same-user local daemon, which may be unexpected if the daemon is not part of the intended setup.

Mitigation: Confirm that the dashboard daemon at ~/.local/state/profile-sync/daemon.sock is expected before installing or running the skill.

Risk: Running --init creates a persistent per-user configuration file; the skill also requests broad network egress permission.

Mitigation: Review the configuration change before using --init and prefer a release that documents the path and removes unnecessary network permission.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/silakge/skills/schema-collector-89596)
- [ClawHub publisher profile](https://clawhub.ai/user/silakge)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance, Shell commands]

**Output Format:** [Text and JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports INITIALISED, UNINITIALISED, SENT, or UNREACHABLE; sends at most one heartbeat per run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
