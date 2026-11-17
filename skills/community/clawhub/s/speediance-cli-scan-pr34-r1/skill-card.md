## Description:

This skill lets an agent read Speediance workout history, browse exercise data, and create training programs for the user's Speediance device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT

## Use Case:

Speediance Gym Monster users can ask an agent to review completed workouts and exercise details, browse the exercise catalog, and prepare programs for their machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workout history and per-set details may be retrieved after a broad mention of exercise.

Mitigation: Access workout records only when the user clearly asks to use their Speediance workout data.

Risk: Browsing the exercise catalog saves the full catalog locally, even when the displayed results are filtered.

Mitigation: Tell the user the catalog will be saved and select an intentional output path with --out.

Risk: Account passwords and live session tokens are stored locally by the CLI.

Mitigation: Prefer exported environment variables and the protected OS user-cache token location; keep credential and token files out of source control.

Risk: Pushing a plan creates a program on the user's Speediance account.

Mitigation: Review the proposed plan with --dry-run and get the user's approval before pushing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/stozo04/skills/speediance-cli-scan-pr34-r1)
- [Project repository](https://github.com/stozo04/speediance-cli)
- [Speediance CLI machine contract](https://github.com/stozo04/speediance-cli/blob/main/docs/MACHINE_CONTRACT.md)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Workout plan configuration]

**Output Format:** [Structured JSON and CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workout and catalog responses preserve Speediance data; pushing a plan creates a program on the user's account.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
