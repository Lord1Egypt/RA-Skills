## Description:

Your agent. Configured to you. Remembers everything. Includes setup wizard, 30-day roadmap, 25 ready-to-use prompts, and pre-built memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scaffoldworkspace](https://clawhub.ai/user/scaffoldworkspace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Scaffold to configure an OpenClaw agent workspace with identity, memory, lifecycle rules, onboarding prompts, and setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority over workspace files, memory, background checks, commits, and possible pushes.

Mitigation: Review and edit permission tiers before use; require confirmation for external actions, commits, pushes, and persistent memory updates.

Risk: Workspace memory and profile files may collect personal preferences, goals, operational details, or sensitive context.

Mitigation: Keep secrets out of workspace files, use environment variables for credentials, and run Scaffold in an isolated or dedicated workspace.

Risk: Autonomous heartbeat, email, calendar, or social checks can create unexpected actions, notifications, or cost.

Mitigation: Make background checks opt-in, disable unneeded heartbeat behavior, and audit memory and state files regularly.

## Reference(s):

- [Scaffold Skill Page](https://clawhub.ai/scaffoldworkspace/skills/scaffold)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and shell commands for configuring an OpenClaw workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace templates, onboarding prompts, lifecycle rules, memory files, and setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
