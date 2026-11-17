## Description:

Self Evolve guides an AI agent through a disciplined loop for identifying capability gaps, testing alternative improvements, selecting winners, and solidifying measured workflow or tool upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikonos](https://clawhub.ai/user/mikonos)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run controlled self-improvement ticks for agent capabilities, workflows, schedules, tools, and skills. It is intended for measured experiments with explicit baselines, telemetry, review checkpoints, and rollback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent broad authority over commands, configuration, source code, schedules, installed skills, and persistent agent instructions.

Mitigation: Run it in a sandbox or disposable workspace and require human review before command execution, tool or skill installation, schedule changes, or persistent edits to agent instructions, memory, or source code.

Risk: Automatic heartbeat or cron use can allow self-modifying experiments to proceed without enough control gates.

Mitigation: Keep cron and heartbeat automation disabled by default, then enable only reviewed schedules with clear stop conditions and monitoring.

Risk: Installer and third-party sources used during experiments may introduce unreviewed behavior.

Mitigation: Pin installers and third-party sources to reviewed versions and scan proposed changes before deployment.

## Reference(s):

- [Self Evolve ClawHub Page](https://clawhub.ai/mikonos/skills/self-evolve-agent)
- [Execution Protocol](references/execution-protocol.md)
- [Constraints and Rules](references/constraints-and-rules.md)
- [Quality Checklist](references/quality-checklist.md)
- [Evolution Report Template](assets/evolution-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON state updates, JSONL telemetry records, shell commands, and configuration or source edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include measurable baselines, telemetry hooks, evaluation deadlines, winner decisions, and rollback-aware solidification notes.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
