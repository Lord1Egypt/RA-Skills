## Description:

Robot Evolve helps an agent perform low-risk workspace maintenance, memory compression, health checks, skill scans, knowledge-card generation, and evolution reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to run local maintenance checks and generate evolution reports for an OpenClaw-style workspace. It is intended for low-risk upkeep tasks such as health checks, temporary-file cleanup, memory compression, and skill-format scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent workspace memory and store selected session content.

Mitigation: Require explicit confirmation before MEMORY.md compression or knowledge-card generation, and back up MEMORY.md before running the skill.

Risk: The advertised safe-mode entry points may not be reliable read-only safeguards.

Mitigation: Do not rely on --dry-run or health_checker.py as a read-only guarantee; review planned actions before execution.

## Reference(s):

- [Robot Evolve ClawHub release page](https://clawhub.ai/pengpengliu1212-art/skills/robot-evolve)
- [Robot Evolve publisher profile](https://clawhub.ai/user/pengpengliu1212-art)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write audit logs, memory summaries, knowledge cards, and temporary-file cleanup results in the local workspace.]

## Skill Version(s):

3.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
