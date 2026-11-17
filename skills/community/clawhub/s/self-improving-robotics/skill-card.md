## Description:

Captures robotics incidents, autonomy failures, and engineering learnings in persistent logs to support safer, repeatable improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Robotics developers and engineers use this skill to document localization, planning, control, sensor, hardware, and safety incidents; track recurring failures; and propose reviewed improvements to operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent incident logs could retain sensitive telemetry or infrastructure details.

Mitigation: Redact telemetry, secrets, and infrastructure details before logging; use only a robotics workspace where persistent logs are wanted.

Risk: Optional hooks can trigger unwanted reminders or inspect tool output.

Mitigation: Keep hooks project-scoped and leave PostToolUse disabled unless output-term detection is explicitly needed.

Risk: Unreviewed learnings could become unsafe agent instructions or reusable skills.

Mitigation: Require an approved, reviewed diff before promoting entries into agent memory, prompt documents, hooks, or new skills.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jose-compu/skills/self-improving-robotics)
- [OpenClaw integration](references/openclaw-integration.md)
- [Hook setup](references/hooks-setup.md)
- [Logging examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown files, Guidance, Shell commands]

**Output Format:** [Markdown entries and instructions with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-local learning logs and optional reviewed checklists or reusable skills]

## Skill Version(s):

1.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
