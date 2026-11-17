## Description:

Build or review a safety-gated Google Colab workflow that installs Hermes Agent and uses it for read-only Unitree Robotics repository analysis, simulation runbooks, log triage, and contribution planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to create or review Colab workflows for read-only Unitree repository analysis, simulation planning, log triage, contribution scouting, and IK evidence review. It is not for live robot control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because automatic activation and an incomplete safety checker require review before installation.

Mitigation: Install only when a read-only Unitree/Hermes Colab review helper is intended; enforce the no-live-robot boundary and manually review generated reports and runbooks before following robotics or network instructions.

Risk: The artifact can produce robotics runbooks and command-oriented guidance that could be misapplied outside the intended read-only Colab workflow.

Mitigation: Keep robot-control, DDS, ROS, SSH, SCP, tunneling, and robot-LAN actions out of Colab execution paths; treat risky local-host commands as quoted human-reviewed runbook text only.

## Reference(s):

- [Unitree G1 Colab IK](https://github.com/zack-dev-cm/unitree-g1-colab-ik)
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/unitree-hermes-colab)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON review artifacts, notebook or runner code, and quoted shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs include unitree-hermes-report.md, unitree-hermes-review.json, AGENTS.md, and a flow visualization.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
