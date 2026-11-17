## Description:

Skill Cortex helps an OpenClaw agent acquire, use, release, and learn routing patterns for Skills from ClawHub or GitHub when installed Skills cannot complete a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankwu001](https://clawhub.ai/user/ankwu001)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an OpenClaw agent discover suitable skills, request approval before installation, execute the task with the selected skill, and update short-term routing memory for future similar tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend, install, and execute additional third-party skills.

Mitigation: Use it with trusted ClawHub publishers or pinned GitHub sources, inspect proposed skills and safety information, and approve installation only when the candidate is appropriate.

Risk: The skill keeps short-term routing history in local cortex memory.

Mitigation: Periodically review or delete ~/.openclaw/skill-cortex/cortex.json if retained routing history is not desired.

Risk: Candidate skills or dependencies may introduce side effects beyond the current task.

Mitigation: Require separate confirmation for installation and system dependency changes, and keep write operations out of reflex behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ankwu001/skills/skill-cortex-pub)
- [Publisher profile](https://clawhub.ai/user/ankwu001)
- [ClawHub](https://clawhub.ai)
- [OpenClaw](https://github.com/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with candidate summaries, approval prompts, execution plans, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose skill installation, candidate switching, and updates to local routing memory after execution.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
