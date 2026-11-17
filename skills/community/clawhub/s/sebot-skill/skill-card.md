## Description:

Enables agents to connect to a 商服机器人 over SSH and ROS to send natural-language commands and read robot replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gittxbb](https://clawhub.ai/user/gittxbb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare a local-network Agent computer, connect to a sebot catering robot over SSH, and invoke ROS topic commands for conversation, ordering, visual observation, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded root SSH access can expose the robot to unauthorized control.

Mitigation: Install only on a trusted robot network after replacing root/root with unique least-privilege credentials and disabling direct root password login.

Risk: Unsafe shell-based command handling can execute unintended commands if untrusted text is passed to the robot.

Mitigation: Fix shell interpolation and pass only trusted command text until argument handling is hardened.

Risk: Robot task commands can affect physical device behavior while the robot is busy.

Mitigation: Use the documented busy-state checks and wait for completion signals before issuing follow-up commands.

## Reference(s):

- [Skill Usage Instructions](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/gittxbb/skills/sebot-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ROS topic names, SSH connection parameters, success criteria, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-07-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
